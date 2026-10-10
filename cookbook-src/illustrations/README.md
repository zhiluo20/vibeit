# Plain-language teaching sketches

These illustrations explain an idea through a bead/block analogy. They are **not experimental structures, docking poses, motion simulations or measured contact diagrams**. The real coordinate snapshots, executed plots and quantitative methods remain in each lesson.

- `drug-pocket-sketch.png`: green protein, orange drug, purple example neighbors and one dashed distance mark. The same five-atom cartoon drug appears before/after placement. Five is a drawing simplification, not imatinib's real atom count.
- `antibody-surface-sketch.png`: green target surface with orange/blue Fab-chain portions approaching a local patch. Two dashed marks connect a Fab portion to a green target point, rather than connecting the Fab chains to each other. Shapes and bead counts are illustrative; this is not a complete antibody or an atomic Fab model.
- `counting-pairs.en.svg` / `.zh-hans.svg`: a deterministic counting analogy. Three children each greet two teachers: five people and six child–teacher pairs. The SVG contains exactly six `greeting-pair` paths. It does not represent the real 14/17/32 protein-interface counts.

The two PNGs were generated and revised with the built-in `image_gen` tool. The selected outputs were copied without pixel edits. Full prompt specifications are in `generation-prompts.json`; final file sizes, image dimensions and SHA-256 are in `manifest.json`. Text captions and accessible alternative text are supplied separately in both languages, avoiding generated in-image text errors.

The PNGs are embedded as `data:image/png` in the Gallery-style raw HTML introduction cell. The counting sketch is embedded as `data:image/svg+xml` in the corresponding lesson explanation. A complete downloaded `.ipynb` contains every sketch and needs no image sidecar or network access. Web reading pages are generated from that same notebook source.

The scientific calculation code, embedded coordinate data, execution counts and all previously saved actual outputs are preserved byte-for-byte/structurally. Reading pages let beginners open the code or scientific notes when ready; pictures and short explanations remain visible.
