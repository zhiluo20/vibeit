# Simulator capture workflow

The runner navigates the real workspace, notebooks, provider settings and model catalog, native terminal, package installer, subscription/restore screens, GitHub clone/commit/push/PR flow, SSH/SFTP and remote Python. `src/data/capture-plan.json` lists the 120 required base captures. Additional screenshots cover states that cannot share the same frame. `qa/screenshot-coverage.json` lists the image and target status for every tutorial step. The set is still incomplete until the release validator passes.

## Prepare

1. Use a separate App checkout containing the final 1.0.1 (7) sources, native inputs and generated Xcode project. Add the capture test and bootstrap below only to that checkout.
2. Add the `VibeitHelpCapture` scheme: build `PyDev_iOS` and `PyDev_iOSUITests`; test only the UI test target using Release and `PyDev.storekit`. Do not include the Release-incompatible unit-test host.
3. Create dedicated simulators named `Vibeit Tutorials iPad` and `Vibeit Tutorials iPhone`. Use normal dynamic type, light theme, iPad landscape/iPhone portrait, and a fixed status bar.
4. Copy the sample workspace into the App's actual Documents/Vibeit directory. Keep credentials outside source control; the optional capture-only bootstrap imports existing authorized credentials and immediately deletes the temporary import file.
5. Complete any real service authorization that requires user input. Never substitute fabricated connected/model states. The `--help-enter-hf` launch option opens the real Environment page solely for manual token entry; capture tests do not use it.

## Run

```sh
python3 scripts/capture.py \
  --checkout /absolute/path/to/capture-checkout \
  --simulator DEDICATED_SIMULATOR_UDID \
  --locale en \
  --output /absolute/private/capture-output \
  --derived-data /absolute/private/derived-data \
  --build
```

Repeat with `--locale zh-Hans` and the other device. Use `--test testCaptureEnvironment` for a single flow. The manual token-entry test is deliberately excluded from the automatic runner.

## Review and import

Inspect every image for completed rendering, correct screen, real device/language, legible controls, overlays and private data. A passing XCTest is not a visual review. Reject keyboard onboarding, half-presented sheets, blank frames and unrelated state.

```sh
node scripts/import-captures.mjs /private/run/attachments \
  --reviewed=S24.ipad.zh-Hans
npm run validate
```

The importer resolves orientation metadata into pixels, compresses losslessly, records hashes and imports only explicitly reviewed IDs. It does not invent target coordinates. For states needing redaction, keep the original private, record the redaction rectangles separately and verify the sanitized image before adding it. Private captures never belong in `public/` or Git.

The test source below is a snapshot of the capture harness. The App capture branch remains authoritative during implementation; synchronize this copy after harness changes.

## Live-service flows

- SSH tests read `HELP_SSH_PASSWORD` and `HELP_SSH_FINGERPRINTS` in the runner. Supply them using the corresponding `TEST_RUNNER_` environment variables from a private credential source. The fingerprint must come from the isolated server itself. Do not print or commit credentials.
- Clone through the App first. Prepare a separate demonstration branch before `testCaptureGitCommitPushAndPR`; the App has no branch-creation button. The test stages only the greeting file. Verify the remote branch SHA after a push.
- Creating a PR is optional and requires `TEST_RUNNER_HELP_CREATE_PR=1`. Use this only for the approved tutorial repository; the test otherwise stops at the form.
- `testCaptureAgentConfirmation` sends a real request to the configured Codex account and captures the returned decision card. It does not inject a tool response or approve an action.
- Never solve the feedback form's human check or submit a dummy issue just to obtain a screenshot. The submission control can be documented in its disabled state with the prerequisite explained.
- Close/reopen Vibeit to apply changed Environment settings on this baseline; see `qa/environment-restart-issue.md`.

## Image review

Create a private contact sheet with `node scripts/review-sheet.mjs /private/run/attachments /private/review.png`. The review helper applies recorded masks and crops. Model menu crops must exclude the underlying account row without covering model names. Reject blank HTML previews even if the editor button is already accessible. The 120-image count excludes supplementary variants, so extra images cannot hide missing device/language captures.
