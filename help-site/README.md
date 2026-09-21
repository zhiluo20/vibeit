# Vibeit Help Center

Static Astro Starlight documentation for Vibeit 1.0.1 (7). Production destination: `https://www.mecury.co.uk/vibeit/help/`.

## Preview

```sh
npm ci
npm run content
npm run validate
npm run dev
```

Open the reported local URL with `/vibeit/help/`. Draft pages carry `noindex,nofollow`; missing screenshots are visible draft notices. They are not publication-ready substitutes.

## Content

`src/data/topics.mjs` defines stable topic and step identities. `src/data/ui.mjs` holds translated labels, requirements and symptom guidance. `scripts/generate-content.mjs` produces MDX source. A locale is complete only when all fields exist; Starlight's fallback pages do not count as translations.

`src/data/screenshots.json` points to real Simulator images under `public/screenshots/`. Each entry records version/build, device, language, normalized pixel dimensions, normalized target rectangles, capture time, SHA-256, evidence type, and review status. Original images and private credentials remain outside this repository. Never substitute fabricated connected states.

## Checks and release

```sh
npm run content
npm run validate
npm run build
npm run release:check
```

`qa/readiness.json` reports structural errors and outstanding delivery work. `qa/acceptance.json` records actual end-to-end evidence. Release requires 32 topics in all 11 languages, all screenshot references and reviewed targets, 120 screenshots, tested service workflows, browser/accessibility checks, and the matching public App version.

Only after the release check passes, build with `HELP_RELEASE=1 npm run build`. The output goes to `../help/`. Keep the existing GitHub Pages legacy deployment: include this static output and the reviewed support/navigation updates in the site release. Do not switch the site's deployment mechanism implicitly.

## Evidence and fixtures

The disposable SSH fixture in `fixtures/ssh` binds only to localhost. Inject its test password and public key as runtime-mounted files outside the repository. The downloadable examples use synthetic measurements only. Hardware-specific Apple Intelligence or Metal claims require a physical device; Simulator configuration views are not performance evidence.

Reference patterns: [Starlight](https://starlight.astro.build/), [Working Copy](https://workingcopy.app/manual.html), [Linear Docs](https://linear.app/docs/start-guide).
