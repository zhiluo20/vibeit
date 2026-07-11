/*
 * vibeit-feedback: turns the contact-form POST into a GitHub issue.
 *
 * Secrets (wrangler secret put):
 *   GITHUB_TOKEN      fine-grained PAT, ONLY the vibeit repo, ONLY Issues: Read+Write
 *   TURNSTILE_SECRET  Cloudflare Turnstile secret key
 * Vars (wrangler.jsonc):
 *   REPO              owner/repo the issues go to
 *   ALLOWED_ORIGINS   comma-separated list of origins allowed to call this
 *   GITHUB_API        override for tests; defaults to https://api.github.com
 */

const AREAS = [
  "Notebooks & editor", "AI assistant", "Remote & SSH",
  "Packages", "Lessons", "Pricing & account", "Other",
];

function json(data, status, cors) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", ...cors },
  });
}

/* Strip control chars (keep \n \t), collapse CRLF, trim, cap length. */
function clip(value, max) {
  return String(value ?? "")
    .replace(/\r\n?/g, "\n")
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "")
    .trim()
    .slice(0, max);
}

export default {
  async fetch(request, env) {
    const allowed = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
    const origin = request.headers.get("Origin") || "";
    const cors = {
      "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0] || "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Max-Age": "86400",
      "Vary": "Origin",
    };

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (request.method !== "POST") return json({ error: "method_not_allowed" }, 405, cors);
    if (!allowed.includes(origin)) return json({ error: "forbidden_origin" }, 403, cors);

    let data;
    try {
      data = await request.json();
    } catch {
      return json({ error: "bad_json" }, 400, cors);
    }

    /* Honeypot: bots that fill every field get a fake success and no issue. */
    if (clip(data.website, 10)) return json({ ok: true }, 200, cors);

    /* Turnstile is the real spam gate; verify server-side. */
    const ip = request.headers.get("CF-Connecting-IP") || "";
    const verify = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        secret: env.TURNSTILE_SECRET,
        response: String(data.turnstileToken || ""),
        remoteip: ip,
      }),
    }).then((r) => r.json()).catch(() => ({ success: false }));
    if (!verify.success) return json({ error: "captcha_failed" }, 403, cors);

    /* Best-effort per-IP cooldown (per-colo cache; Turnstile carries the real load). */
    const cache = caches.default;
    const cooldownKey = new Request(`https://cooldown.invalid/${encodeURIComponent(ip)}`);
    if (ip && (await cache.match(cooldownKey))) return json({ error: "too_many" }, 429, cors);

    /* Validate + normalize into the same shape as the issue-form templates. */
    const kind = data.kind === "bug" ? "bug" : data.kind === "feature" ? "feature" : null;
    if (!kind) return json({ error: "bad_kind" }, 400, cors);
    const area = AREAS.includes(data.area) ? data.area : "Other";
    const title = clip(data.title, 140);
    const main = clip(kind === "feature" ? data.description : data.happened, 4000);
    if (!title || !main) return json({ error: "missing_required" }, 400, cors);

    const parts = [`### Area\n\n${area}`];
    if (kind === "feature") {
      parts.push(`### What would you like Vibeit to do?\n\n${main}`);
      const usecase = clip(data.usecase, 2000);
      if (usecase) parts.push(`### Use case\n\n${usecase}`);
    } else {
      parts.push(`### What happened?\n\n${main}`);
      const steps = clip(data.steps, 2000);
      const device = clip(data.device, 120);
      const appversion = clip(data.appversion, 60);
      if (steps) parts.push(`### Steps to reproduce\n\n${steps}`);
      if (device) parts.push(`### Device and OS version\n\n${device}`);
      if (appversion) parts.push(`### Vibeit version\n\n${appversion}`);
    }
    parts.push(`---\n_Submitted from the website contact form._`);

    const gh = await fetch(`${env.GITHUB_API || "https://api.github.com"}/repos/${env.REPO}/issues`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "vibeit-feedback-worker",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: (kind === "bug" ? "[Bug] " : "[Feature] ") + title,
        body: parts.join("\n\n"),
        labels: kind === "bug" ? ["bug", "from-website"] : ["enhancement", "from-website"],
      }),
    });
    if (!gh.ok) return json({ error: "github_error" }, 502, cors);
    const issue = await gh.json();

    if (ip) {
      await cache.put(cooldownKey, new Response("1", { headers: { "Cache-Control": "max-age=60" } }));
    }
    return json({ ok: true, url: issue.html_url, number: issue.number }, 200, cors);
  },
};
