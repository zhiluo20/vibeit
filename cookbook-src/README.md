# VibeIt Studio bioinformatics cookbook

Six workflows, twelve independent English/Simplified Chinese notebooks, and a static subject catalog. Intended for undergraduate students with basic Python knowledge. **Publication is pending review; this branch does not deploy the website.**

## Download and run / 下载与运行

The generated site is in `../cookbook/`. Individual executed notebooks and the twelve-notebook ZIP are in `../cookbook/downloads/`.

In VibeIt Studio, use **+ → Import from Files**, select a complete `.ipynb`, open it, and run cells from top to bottom. One notebook contains its own real data; no ZIP extraction, sidecar module, account or network connection is required for core computation. Optional AI exercises and online extensions are clearly separated.

在 VibeIt Studio 中使用 **+ → Import from Files** 导入完整 `.ipynb`，打开后从上到下运行。每份 notebook 独立包含真实数据，无需解压数据包、安装额外模块、登录 AI 服务或联网即可完成核心分析。修改参数前保留副本；结果导出到当前目录下的 `results/<recipe-id>/`。

| Lesson | Dataset | Method | Expected handoff |
| --- | --- | --- | --- |
| 01 FASTA → protein | RefSeq HBB/HBD, versioned transcripts | FASTA parsing, coordinate conversion, translation checks | Transcript/protein FASTA, composition summary |
| 02 Sequence alignment | The same annotated CDS records | Three-state affine global/local DP, traceback, scoring sensitivity | Alignment, metrics and differing columns |
| 03 RNA-seq exploration | Official airway/GSE52778, 63,677 × 8 counts | Sample audit, median-ratio normalization, paired EDA and PCA | Sample audit, size factors, PCA, descriptive responses |
| 04 Pathway enrichment | airway + frozen human Reactome Ensembl mapping | Measured universe, effect screening, hypergeometric ORA, combined-family BH | Entire test family and background identifiers |
| 05 Protein interactions | STRING human physical network, 12 query proteins | Evidence audit, graph topology and threshold sensitivity | Node/edge CSV, GraphML and threshold audit |
| 06 Protein structure | PDB 1A3N + RefSeq HBB | First-model parsing, py3Dmol, distances, contacts, heme neighbors | Original PDB and coordinate-derived tables |

## Runtime boundary

Notebook code uses only the standard library and app-bundled NumPy, Pandas, Matplotlib, IPython, SciPy, NetworkX and py3Dmol. The disabled-by-default online cell uses Requests. No Biopython, BLAST executable, R, shell command, cloud kernel or installation cell is needed on the student device.

`rdata` and Jupyter authoring tools belong to the build environment only. Full teaching functions are copied from `runtime.py` into notebook cells, so `runtime.py` is not a student-side dependency.

Large snapshots live in `metadata.vibeit_cookbook.snapshots`: gzip/base64 payload and SHA-256 of decoded JSON. The loader finds the saved notebook by recipe ID and expected data hash in its working directory. The filename can change. Copying cells alone to a `.py` does not transfer the metadata. Format validation and rename/move/roundtrip checks cover this boundary.

## Rebuild without network

Use Python 3.13. Create an authoring environment with the frozen lock file:

```sh
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -r cookbook-src/requirements-lock.txt
.venv/bin/python cookbook-src/test_methods.py
.venv/bin/python cookbook-src/build_notebooks.py
.venv/bin/python cookbook-src/build_site.py
.venv/bin/python cookbook-src/validate_site.py
.venv/bin/python cookbook-src/serve.py --port 8764
```

Run from the website repository root. Preview at `http://127.0.0.1:8764/vibeit/cookbook/` or its `zh-hans/` version. Dependency installation needs network on an uncached machine; notebook execution and site generation use already frozen data without data-source requests. `build_notebooks.py` denies Python socket connections during execution and saves actual outputs. `--only <recipe-id>` rebuilds one changed lesson; `--generate-only` emits unexecuted development notebooks and must not be used for release artifacts.

To refresh source data intentionally, run `freeze_data.py`, then `archive_sources.py`, and repeat every execution/validation step. The archive step requires each upstream response to match its recorded SHA-256; it fails if upstream bytes changed. Existing public artifacts are not overwritten by optional online notebook cells.

## Data provenance and licenses

`data/sources.json` records original URLs, source hashes, retrieval times, API parameters, upstream versions, licenses and conversion rules. `data/raw-manifest.json` links byte-identical gzip archives of all seven original responses. `data/*.json.gz` contains compact, documented teaching snapshots. Reactome's original archive contains all species; the student snapshot retains only human Ensembl memberships present in the complete airway matrix.

The airway source is pinned to official commit `596678815f4ade04a9711997150949b9782aeddc`. The complete integer count matrix and its donor metadata are extracted with pure Python `rdata`; no scaling or gene subsetting occurs during snapshot creation. Filtering and normalization remain visible student computations.

Upstream data rights remain with their original licenses:

- airway package: LGPL as declared by the official package; original source is linked in the manifest. Experiment: Himes et al., *PLoS ONE* 2014, DOI `10.1371/journal.pone.0099625`, GEO GSE52778.
- NCBI RefSeq: public sequence records, accessions NM_000518.5 and NM_000519.4; credit NCBI/RefSeq.
- Reactome annotation data: CC0 1.0; credit Reactome and retain the release version.
- PDB coordinate/archive data: CC0 1.0; credit RCSB/wwPDB and the 1A3N primary citation.
- STRING data: CC BY 4.0; retain STRING attribution, network version and physical-network query parameters.
- 3Dmol.js: BSD-3-Clause, with GLmol/Three.js/jQuery notices in `vendor/3Dmol-LICENSE`. The bundled library is served locally for offline-compatible previews.

Original VibeIt lesson code is MIT licensed; original teaching prose is CC BY 4.0. These choices do not relicense embedded third-party data or the existing website.

## Scientific interpretation

The RNA-seq lesson starts at a gene count matrix. It does not perform FASTQ alignment or formal DEG inference. Log-normalized counts are not VST/rlog, and response candidates are selected by observed paired effect size and directional agreement. ORA reports overrepresentation, not pathway activation. STRING confidence is not affinity, centrality is not causality, and geometric proximity in an experimental structure is not a binding-energy prediction. Experimental B-factors are distinct from predicted-model pLDDT.

## Verification and review

Machine-readable evidence in `qa/` distinguishes authoring execution, independent numerical checks, actual app runs, browser downloads and portability. Simulator evidence records app version 1.0.2 (8), embedded Python/package versions and completed cell counts. A build or a pre-saved output alone is not app execution evidence.

The site generator reads executed notebooks for every code cell, table and figure. Notebook calculations are not duplicated in separate webpage source. `manifest.json` describes six recipes, languages, routes, packages, snapshot version and validation state. New subjects use honest "Coming soon" landing cards until runnable material exists.

Website integration adds the Cookbook entry to the existing main navigation and Help Center landing pages, while preserving their existing language selection. Cookbook pages use the `www.mecury.co.uk` canonical host and paired English/Chinese hreflang links. The root product sitemap includes all 32 cookbook pages.

Merge/deployment remain a later review step. After publication, rerun the download/hash/import checks against the public origin rather than treating local preview as deployed acceptance.

The Cookbook palette is generated directly from the product page CSS tokens. Python code is highlighted statically with Pygments; syntax colors and brand assets require no CDN. Scientific plots preserve their executed colors.
