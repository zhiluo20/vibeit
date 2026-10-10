# Drug–protein cookbook validation

Two new workflows, English and Chinese: `07-imatinib-pocket` and `08-trastuzumab-interface`. The catalog now contains 50 workflows / 100 notebooks / 120 static pages. The original 96 notebooks remain byte-identical to the published `origin/main` baseline.

| Evidence | Result | Scope |
| --- | --- | --- |
| `qa/notebook-execution.json` | Four new notebooks executed from cleared state with Python network connections denied; 4/5 PNG figures per lesson | Actual saved outputs, author environment |
| `qa/drug-method-validation.json` | Independent KD-tree radius search; direct point-wise norms; residue/insertion identity; coordinate roundtrip; rigid transforms and symmetry | Geometry correctness, not pharmacological efficacy |
| `qa/drug-empty-cases.json` | Both entire workflows execute after rename/move with 0.01 Å cutoff and export zero-contact results | Valid empty analysis, no fabricated contacts |
| `qa/release-validation.json` | 100 current notebooks, source/code parity, rename/move JSON roundtrip, 53 original archived responses with matching SHA-256 | Full catalog integrity |
| `qa/artifact-validation.json` | Format, allowed imports, shared bilingual code, saved outputs, routes/archives/links | Full static site |
| `qa/drug-browser-validation.json` | Four reading pages at desktop/tablet/phone sizes; correct 3D atom selections with external HTTPS blocked; search/filter; four actual downloads match source SHA-256 | Browser rendering and download integrity |
| `qa/drug-native-kernel.json` | All four cleared fixtures executed in VibeIt 1.0.2 (8), Python 3.13.14, NumPy 2.5.0, Pandas 3.0.3, on the isolated iPadOS 27.0 Simulator | Exact final calculation code and snapshots; distinct from individual editor Run All |
| `qa/drug-native-imports.json` | Four actual browser-downloaded files imported through the installed app's external-file callback, preserving cells, raw HTML, snapshots and outputs | Actual import/persistence; distinct from manual Files picker |

The native kernel record retains the real staged file hashes. The 1IEP chemical-component provenance sentence and 1N8Z humanized-antibody explanation were subsequently clarified without changing any code or snapshot; both staged and final hashes are recorded, with exact code/data parity checks. Current-file imports use the final browser downloads.

Native batch execution captures actual HTML/PNG outputs and exports. It does not claim individual interactive 3D rendering, every editor Run All/export flow, iPhone touch interactions or physical-device acceptance. These presentation checks remain separate. Nothing in this report establishes affinity, interaction energy, hydrogen bonds, causal hotspots or clinical efficacy.

The new source archives preserve complete 1IEP/1N8Z PDB coordinates, entry metadata, polymer identities and STI chemical identity. A rerun of `freeze_drug_data.py` uses the verified archives; deliberate updates require `--refresh`. Each student notebook independently carries its complete compressed snapshot in metadata and requires no R, RDKit, Biopython, docking executable or sidecar data file.

Classroom interpretation and the distinction between experimentally observed complexes and unrelated standalone coordinates are in `DRUG_BINDING_TEACHER_GUIDE.zh-hans.md`.
