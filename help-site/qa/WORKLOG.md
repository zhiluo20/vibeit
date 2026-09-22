# Implementation status — 2026-09-21

## Delivered in the isolated preview

- Astro Starlight project at `help-site/`; static output at `help/`.
- 32 tutorial source topics: complete English, Simplified Chinese and French drafts; a Traditional Chinese variant derived from the Chinese text, awaiting editorial review. The remaining seven languages are not yet authored. Starlight fallback pages are explicitly excluded from translation completion counts.
- Step navigation, keyboard selection, stable hashes, original screenshots with normalized target coordinates, tap/hold/input/swipe annotation support, zoom, mobile device selection, code-copy control, print layout, and reduced-motion rules.
- The first seventeen reviewed screenshots are in the manifest. Other raw captures remain private and must pass visual review before import.
- Synthetic sample workspace and ZIP; both notebooks execute in an isolated Python 3.12 environment. Public sample repository: https://github.com/zhiluo20/vibeit-tutorials (initial commit 5ab577f).
- Local Docker SSH fixture reachable at localhost:2222. SSH public-key login and server Python path verified from the Mac; Vibeit password/key/SFTP/remote-kernel validation is still outstanding.
- Product navigation and legacy support landing pages updated locally. No website changes have been pushed or deployed.
- Release validator checks 32 topics, all language fields, 120 named base captures, image hashes, coordinates, related links, samples, and acceptance gates.

## Verified browser behavior

- English HF tutorial at 390×844: document width 390, no horizontal overflow.
- iPhone screenshot loads at 1206 pixels wide and the overlay matches the token field when enlarged.
- Arrow keys change the selected step and update its stable URL hash.
- Language switch keeps the same tutorial route.
- Chinese built-in controls now use the Starlight zh-CN dictionary; source route remains zh-hans.
- Arabic layout uses RTL without horizontal overflow. Its body is still explicitly marked as untranslated.
- Pagefind returns the HF article for `hugginface`.
- Public assets contain only reviewed demo screens; no credential values are included.

## Native capture evidence and defects found

The capture checkout is separate from the user's dirty App checkout and contains a Release-only capture scheme. Real StoreKit test purchases are used, with no fabricated entitlement/provider/model fixtures. Test credentials are imported privately using a capture-only bootstrap; the import file is removed immediately. Screenshots still require real successful operations where claimed.

- The first failed run used CGImage storage dimensions rather than orientation-aware UIImage dimensions. Native rendering now resolves orientation into pixels; normalized target coordinates are checked against the full-screen aspect ratio.
- iPhone Environment capture passed and was reviewed.
- iPhone first Python execution passed with the expected two lines. Some screenshots from that run caught keyboard onboarding or a sheet transition and were rejected for publication.
- Added a render-settle interval, keyboard-onboarding dismissal and a visible-target requirement. Provider configuration recaptures passed and four were visually reviewed and imported. The repeat notebook run exposed an off-screen-file lookup; the helper now scrolls to targets. The final notebook capture passed after opening the iPhone ellipsis menu for kernel controls. The verified result and kernel-menu screenshots were imported; the pre-run screenshot still needs clean example outputs.
- Settings rows gained accessibility button traits only in the isolated capture checkout.
- For manual token entry, a capture-only launch option opens the real iPad Settings → Environment page. It is not used by screenshot tests and does not inject a success state.

## Outstanding

1. Hugging Face verification completed: the user entered the token directly; a real restarted App kernel saw HF_TOKEN, HfApi.whoami accepted it, and an authenticated forced config.json download parsed correctly. English and Chinese capture runs passed. No Token or account details were printed.
2. Complete actual Codex model discovery, Git clone/commit/push, SSH password/key/SFTP and remote Python workflows from the App.
3. Finish all capture states in both languages and the required iPhone differences, including privacy review and exact target mapping. Several logical topics need additional screen variants when controls cannot coexist in one screenshot.
4. Write and review German, Thai, Japanese, Korean, Spanish, Arabic and Italian bodies, plus all localized component labels/requirements/troubleshooting.
5. Complete device-specific step text, print/zoom/hash-history tests, all-locale search checks, download/link validation, legacy support browser checks, and iOS 26.2 sampling.
6. Review all tutorial labels against the final release UI. In particular, Chinese Light currently displays 浅色; SSH Key accepts a local key-file path, not pasted key contents.
7. Confirm App Store 1.0.1 availability before enabling indexing and deploying. The last verified public version was 1.0. Keep the preview unpublished until the release validator passes.

The normal dedicated iPad app was launched with `--help-enter-hf` after the timed test ended. Its real Environment token field was confirmed visible. It remains open for the user without a test timeout.

Latest native result: `capture-iphone-kernel-en.xcresult` passed the notebook execution/capture flow. `S09.iphone.en` highlights Restart Kernel by its actual label; the legacy `.restart` identifier on iPhone belongs to Restart and Clear Outputs and must not be used for the normal restart instruction.

HF examples now use the verified code in `src/data/hf-examples.json` and the downloadable workspace. This separates token presence, service authorization, a small configuration download, gated access and actual inference.

## Hugging Face handoff completed

- User confirmed manual token entry. No secret value was retrieved into the chat or public files.
- `hf-validation-en.xcresult`, `hf-validation-zh.xcresult`, `hf-complete-en.xcresult` and `hf-complete-zh.xcresult` passed.
- Reviewed and imported iPad Environment (EN), Restart (EN/ZH), authorization result (EN/ZH), and authenticated configuration download result (EN/ZH).
- The Chinese HF article’s four interactive steps all load their expected screenshot and target. French retains the article route and maps all four steps to English screenshots. Result steps now use an observation label rather than implying the output must be tapped.
- French has all 32 source articles, complete component labels, requirements and troubleshooting. Step counts were compared against the source and match. Remaining source languages: German, Thai, Japanese, Korean, Spanish, Arabic, Italian.
- Public tutorial examples updated in commit `15e765a`; the downloadable ZIP includes the same credential-free HF notebooks, with outputs cleared.
- Separate captures are now required for environment-variable output, package-import output and table output. Unrelated HF success screenshots must not be reused for those results.
- The help website remains unpublished and noindex. Release validation still blocks publication due to the remaining work.

## Screenshot completion pass — 2026-09-21 (latest)

- Reviewed/imported 146 public screenshot assets: 101 of 120 required device/language base captures and 45 supplementary state captures.
- Added verified iPhone screenshots for the workspace menu, file browser, HTML preview/editing, interactive result, Codex model menu, Git source-control panel, Agent reasoning menu, subscription pages, Environment and remote-host forms. Added iPad screenshots for package install/reinstall, Git state, host-key verification, SFTP listing, remote environment discovery and the feedback form.
- Real model discovery used the authenticated Codex catalog and captured the current account catalog; no fixed model list or fixture was used.
- Rejected a remote-form frame with the software keyboard covering fields. Rejected the feedback submission result because the required human-verification widget was not completed; no dummy report was submitted.
- Website build passed (`astro build`) and Pagefind indexed 364 pages. The release validator remains intentionally blocked: 101/120 base captures, four complete source languages, and unresolved acceptance checks. The site remains preview/noindex and has not been published.
- Remaining screenshot gaps are enumerated in `qa/readiness.json` and per-step in `qa/screenshot-coverage.json`; this status is a release gate, not a claim that missing screens are covered by a fallback image.

## Follow-up completion pass — 2026-09-22

- Imported 13 additional reviewed captures from the dedicated iPad runs: Simplified Chinese Codex model catalog, package installation, Git panel, terminal system selection menu, SSH forms, host-key verification, SFTP listing, remote environment, Cloudflare form, and issue report form; the corresponding English remote form variants were also reviewed.
- Base coverage is now 111/120; supplementary state coverage is 48. The remaining missing base states are mostly alternate-language/iPhone variants and a few end-to-end Git/remote result screens that did not complete in the real service run.
- Fixed screenshot crop normalization so crop bounds are calculated from the full normalized rectangle; this keeps cropped model menus and target rectangles inside the published image.
- Published build remains structurally valid and builds successfully. The release validator still reports incomplete translations and end-to-end acceptance gates; these remain explicit follow-up work rather than hidden fallback content.
