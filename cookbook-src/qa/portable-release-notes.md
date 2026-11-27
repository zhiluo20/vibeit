# Portable Cookbook artifact correction

Base: `6ee0ddb`. This change is local only; it has not been pushed or deployed.

## Changes

- The shared notebook setup uses `results/<recipe ID>` relative to the active
  notebook folder. Neither setup nor export messages print the build machine's
  absolute directory.
- Numerical calculus and least-squares conditioning no longer read unused model
  inputs. Their calculations are unchanged.
- Model lessons embed only their explicitly declared model fields. Monte Carlo
  retains seed `20261009`; calibration and RC tolerance simulation retain their
  original seeds too. Snapshot SHA-256 checks still verify the actual embedded
  bytes, including after notebook rename/move.
- IAPWS attribution remains in the water-saturation lesson and the full source
  registry. Other model lessons cite only the authored teaching parameters they
  actually use. Original archived source files, hashes and licenses are unchanged.
- Both language versions, lesson HTML, nine downloadable archives and public
  manifests were rebuilt.

## Output preservation and validation

Saved scientific output objects, tables and all 310 PNG figures in the 100
notebooks are byte-identical to the base revision after narrowly normalizing only
working-folder/results-path messages and the two removed snapshot-list messages.
The stored execution metadata describes the original scientific run; this refresh
preserves those results rather than replacing all outputs with a new runtime's
rendering. `portable-output-parity.json` records the artifact coverage.

To check the release:

```sh
python cookbook-src/test_methods.py
python cookbook-src/test_science_methods.py
python cookbook-src/test_drug_methods.py
python cookbook-src/test_markdown_rendering.py
python cookbook-src/validate_release.py
python cookbook-src/validate_site.py
python cookbook-src/test_portable_artifacts.py --baseline 6ee0ddb
```

A separate offline execution of the 11 scoped-model lessons, the two deterministic
mathematics lessons and Iris audit checks the modified code in temporary folders;
see `portable-reexecution.json`. This does not overwrite released outputs. No new
native VibeIt GUI test or production deployment is claimed.

The owner's original checkout is not modified. Its existing README/build-site/
site-validator preview work must be preserved when integrating this branch. The
site-validator change here is limited to verifying lesson-scoped snapshot bytes.
