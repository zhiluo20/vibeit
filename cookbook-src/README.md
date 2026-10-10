# VibeIt Studio multidisciplinary cookbook

**8 disciplines, 50 workflows and 100 independent, executed bilingual notebooks.** The original 48-course catalog is extended with two experimental drug–protein lessons (bioinformatics 07/08); the other seven disciplines retain six courses each. Intended for undergraduate students with basic Python knowledge.

The official catalog is [VibeIt Cookbook](https://www.mecury.co.uk/vibeit/cookbook/), with a [Chinese edition](https://www.mecury.co.uk/vibeit/cookbook/zh-hans/). GitHub Pages serves committed static artifacts from `main`; a development branch or local preview is not deployment evidence.

## Download and run

Use **+ → Import from Files** in VibeIt Studio, select a complete `.ipynb`, open it and run cells from top to bottom. Every notebook embeds its own frozen inputs; no sidecar files, shell commands, server, R, package installation or AI account is required for core computation. The optional AI and online exercises are separate and require manual review/execution.

在 VibeIt Studio 中使用 **+ → Import from Files** 导入完整 `.ipynb`，打开后从上到下运行。每份 notebook 内嵌自己的冻结输入，不需要旁侧数据文件、服务器或 AI 账号。结果导出到当前目录的 `results/<recipe-id>/`。修改参数前保留副本。

Downloads in `../cookbook/downloads/` include 100 single notebooks, eight bilingual subject ZIPs and `vibeit-cookbook.zip` containing all 100. A single lesson requires only its `.ipynb`.

Each first cell is a Gallery-style standard `raw` / `text/html` introduction card. Every lesson includes a research question, source/model audit, transparent computation, at least three actual figures, result checks, exports, two independent exercises with answers and two AI modification exercises with acceptance criteria. Explanations and figure captions are bilingual; computation and inputs are identical across languages.

## Learning paths

| Discipline | Independent workflows | Input boundary |
| --- | --- | --- |
| Bioinformatics | FASTA/CDS translation; affine alignment; RNA-seq exploration; ORA; physical interactions; hemoglobin; imatinib pocket; trastuzumab Fab interface | RefSeq, airway, Reactome, STRING and experimental PDB frozen records |
| Data science & ML | Iris audit; standardized PCA; held-out kNN; Wine clustering; chronological bike regression; sequential forecast backtesting | Original UCI measurements, source discrepancies and units retained |
| Mathematics & statistics | Numerical calculus; bracketed roots; conditioning; Monte Carlo; bootstrap; permutation/BH | Explicit mathematical models and public Iris observations |
| Physics | Nonlinear pendulum; damping/resonance; projectile drag; heat equation; GW150914 signal; blackbody radiation | Models distinguished from real GWOSC strain and CODATA reference constants |
| Chemistry | Formula/property audit; molecular graphs; caffeine conformer; acid/base titration; water vapor pressure; calibration | PubChem computed fields, IAPWS reference formulation, explicitly simulated calibration |
| Engineering | Building-energy audit; chronological regression; low-rate signal processing; beam FEM; RC response; thermal PID | Real UCI energy measurements and separately labelled engineering models |
| Economics & finance | Real growth; CPI/real values; dated inequality; quotation/returns; train-only variance weights; empirical tail risk | Historical World Bank/ECB data; hypothetical price-only strategies |
| Humanities & social sciences | Corpus audit; length-controlled diversity; KWIC; name mention network; TF-IDF/SVD; social indicators | Two complete historical ebook sources and dated World Bank observations |

The requested lesson scope is recorded in `EXPANSION_PLAN.md`. `catalog.py` is the single course manifest; `subjects/*.py` and `courses.py` contain bilingual prose and calculation cells. `runtime.py` / `science_runtime.py` contain readable helpers copied verbatim into notebooks. Students do not import these author-side modules.

## Supported runtime

Core code uses the standard library and app-bundled NumPy, Pandas, SciPy, Matplotlib, NetworkX, py3Dmol and IPython. Requests appears only in disabled-by-default online extensions. Jupyter, Pygments and `rdata` are authoring/conversion dependencies, not student requirements.

Dates remain ISO strings in tables and are parsed with the standard-library `datetime` for cadence, calendar features and Matplotlib axes. This avoids a native datetime dtype crash observed in VibeIt 1.0.2 (8), Pandas 3.0.3 / NumPy 2.5.0, while preserving real calendar spacing, sample splits and source-local timestamps. No timezone is invented.

Snapshots are gzip/base64 payloads in `metadata.vibeit_cookbook.snapshots`, with SHA-256 of decoded JSON. The loader locates the complete saved notebook in its working directory by course ID and expected hash, supporting rename, move and save/roundtrip. Copying only cells into a `.py` does not transfer metadata.

## Rebuild and validate

Run from the website repository root with Python 3.13:

```sh
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -r cookbook-src/requirements-lock.txt
.venv/bin/python cookbook-src/test_methods.py
.venv/bin/python cookbook-src/test_science_methods.py
.venv/bin/python cookbook-src/build_notebooks.py
.venv/bin/python cookbook-src/build_site.py
.venv/bin/python cookbook-src/validate_site.py
.venv/bin/python cookbook-src/validate_release.py
.venv/bin/python cookbook-src/serve.py --port 8764
```

Preview `/vibeit/cookbook/` and `/vibeit/cookbook/zh-hans/` at `http://127.0.0.1:8764`. Installing author dependencies needs network on an uncached machine; execution and generation use frozen inputs. Notebook execution denies Python socket connections, clears state and saves actual outputs.

Use `build_notebooks.py --only <id>` or `--subject <discipline>` for changed computations. `--refresh-intro` or `--refresh-prose` can preserve executed outputs only when computation and snapshots match; historical executed hashes are retained in QA records. `--generate-only` emits unexecuted development artifacts and must not be used for release.

Intentional source updates use `freeze_data.py` for bioinformatics or `freeze_subject_data.py --group <group> --merge` for extensions, followed by `archive_sources.py` and all relevant execution/QA. A changed upstream response must receive a new reviewed source record; archive verification rejects unexpected hashes. Optional online cells do not silently replace frozen inputs.

`make_native_batch_qa.py --destination <own QA folder>` prepares isolated cleared fixtures and an internal QA notebook. Opening and running that QA notebook inside VibeIt executes each fixture's exact visible code in the actual embedded kernel, records outputs, blocks Python network and writes an incremental report. This is kernel compatibility evidence; it does not establish every editor import/render/export flow. Individual editor UI checks and simulator evidence are recorded separately. `validate_native_imports.py` validates the actual installed app external-file import callback and saved-cell/metadata preservation on an isolated Simulator; it is separately labelled from the manual Files picker and export UI. `browser_release_qa.js` is an author-only Playwright function for rendered route/filter/mobile/3D checks.

## Provenance, licenses and interpretation

`data/sources.json` records 53 sources with original URLs, retrieval dates, SHA-256, parameters, versions, rights and transformations. `data/raw-manifest.json` links all 53 byte-identical gzip archives. Raw books include their complete license text; authored model inputs are labelled model parameters, not measurements.

- RefSeq: public sequence records NM_000518.5 / NM_000519.4, credited to NCBI.
- airway: official commit `596678815f4ade04a9711997150949b9782aeddc`, LGPL package source; Himes et al., DOI `10.1371/journal.pone.0099625`, GSE52778. Full 63,677 × 8 integer matrix and sample annotations extracted with author-only pure Python `rdata`.
- Reactome and wwPDB/PDB: CC0; release and primary-source credits retained. STRING: CC BY 4.0, physical-network parameters and evidence fields retained.
- UCI Iris, Wine, Bike Sharing and Appliances Energy Prediction: dataset-specific credits and CC BY 4.0 source records retained. The Air Quality dataset was excluded after its additional use restriction was found. No unsupported daily weather unit conversion or silent Iris transcription correction is made.
- ECB: source-specific free-reuse conditions and notices retained; original rates available free at ECB. Inversions, returns and hypothetical baskets are identified as derived course calculations. The rejected stale legacy CSV is documented in `qa/source-quality.json`; official SDMX data is used.
- World Bank: source-specific CC BY 4.0 notice, definitions, missing values and observation dates retained. Aggregate economies are excluded from country analyses; present-day income labels are not historical classifications.
- PubChem: public source credits; calculated properties and conformers are not described as experimental measurements. GWOSC: public data-use/citation policy and event/product version retained. NIST/CODATA constants are reference values. IAPWS permits publication; the archived official release provides the actual saturation coefficients.
- Historical ebooks: full Project Gutenberg source/license headers are archived and embedded. The name is used for attribution/reference; no endorsement is claimed. Analysis scope and wrapper/chapter removal are visible computations. Local public-domain status may differ by jurisdiction.
- 3Dmol.js: BSD-3-Clause and bundled dependency notices in `vendor/3Dmol-LICENSE`; hosted locally for website rendering and supplied by VibeIt's offline viewer.

Original lesson code is MIT (`LICENSE-CODE`); original teaching prose is CC BY 4.0 (`LICENSE-CONTENT`). These do not relicense upstream inputs or the existing website.

Expression courses are exploratory, not formal DEG inference; ORA does not prove pathway activation. Graph centrality or structural proximity is not causality/affinity. Prediction workflows isolate fitting from test outcomes. Models, simulated noise and reference formulations are explicitly labelled; GW filtering does not establish event significance. Historical price returns omit interest/carry, tax and transaction costs and do not recommend investments. Surface name co-occurrence and text projection do not prove literary relationships or author intention. Cross-sectional indicators do not establish personal or causal effects.

## Website and release evidence

The generator builds 120 static pages, reads all code/tables/figures from executed notebooks, and adds routes, canonical/hreflang, schema, search/topic filters and current-language downloads. Product Lessons links and header/palette are shared with the product page. Code highlighting is static Pygments; fixed guidance uses accessible callouts. No server/database/CDN is introduced.

`qa/` separates author execution, independent references, native kernel runs, individual UI checks, portability, browser checks and download hashes. Simulator observations are not real-device testing. `VERIFICATION.md` describes current coverage and limitations.

Publication requires merging the reviewed website changes into `main`, then checking the GitHub Pages deployment and public artifact hashes. A successful build, saved output or simulator screenshot alone is not publication acceptance. App source, Gallery examples and App Store releases are outside this website change.

## Drug–protein teaching extension

Lessons 07/08 use experimental complexes 1IEP (mouse c-Abl kinase domain / imatinib, STI) and 1N8Z (human HER2 extracellular construct / trastuzumab Fab light and heavy chains). These are observed complex coordinates, not docking outputs. Pocket/interface metrics are positive-occupancy heavy-atom minimum distances in Å; no binding-energy, affinity or clinical efficacy estimate is inferred. Antibody insertion codes are retained, and sugars are not misidentified as the drug.

See [the Chinese classroom guide](DRUG_BINDING_TEACHER_GUIDE.zh-hans.md) for the heme → chemical drug → antibody analogy, actual results, questions and answers. Both courses use the same readable geometry helpers and support valid zero-contact results. `test_drug_methods.py` independently checks a KD-tree radius search, direct point-wise norms, coordinate/insertion-code roundtrip, symmetry and rigid transformations. `freeze_drug_data.py` uses nine archived original RCSB responses on rerun; `--refresh` intentionally fetches new snapshots.

Build only the new lessons with `build_notebooks.py --only 07-imatinib-pocket` and `--only 08-trastuzumab-interface`, then rebuild/validate the site. `make_native_batch_qa.py --only 07-imatinib-pocket --only 08-trastuzumab-interface --destination <own QA folder>` isolates the exact new code for on-device kernel checks. `drug_browser_qa.js` checks bilingual pages, category/search, desktop/tablet/phone layouts, locally rendered 3D and actual notebook downloads with external HTTPS blocked. Native kernel evidence and editor/real-device acceptance remain separately labelled.
