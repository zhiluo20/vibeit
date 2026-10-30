"""Reproduce the fixed public 1A3N chain-B C-alpha distance example.

Run from this folder: python analysis.py
Inputs are never modified. Re-running replaces only files in results/.
"""
from __future__ import annotations

import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_analysis(root: Path | str = Path(__file__).parent) -> dict:
    root = Path(root)
    provenance = json.loads((root / "SOURCE-PROVENANCE.json").read_text())
    for item in provenance["package_inputs"]:
        assert sha256(root / item["file"]) == item["sha256"], "Fixed input hash mismatch"
    reference_path = root / "reference/b_ca_distance_matrix_reference.csv"
    assert sha256(reference_path) == provenance["reference_matrix_sha256"], "Reference hash mismatch"

    ca = pd.read_csv(root / "data/1a3n_ca.csv", keep_default_na=False)
    expected = "record,serial,atom,altloc,residue,chain,resnum,icode,x,y,z,occupancy,bfactor,element".split(",")
    assert list(ca.columns) == expected
    assert ca["record"].eq("ATOM").all() and ca["atom"].eq("CA").all()
    assert (ca["occupancy"] > 0).all()
    assert np.isfinite(ca[["x", "y", "z"]].to_numpy(dtype=float)).all()

    # Check that the fixed selected coordinates really occur in the supplied PDB.
    pdb_text = (root / "data/1A3N.pdb").read_text(encoding="utf-8")
    first_model = pdb_text.split("ENDMDL", 1)[0]
    pdb_atoms = {int(line[6:11]): line for line in first_model.splitlines() if line.startswith("ATOM  ")}
    for atom in ca.itertuples(index=False):
        line = pdb_atoms[int(atom.serial)]
        assert line[12:16].strip() == "CA" and line[21:22] == atom.chain
        assert int(line[22:26]) == int(atom.resnum) and line[26:27].strip() == str(atom.icode)
        actual = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
        assert np.allclose(actual, [atom.x, atom.y, atom.z], rtol=0, atol=1e-12)

    b = ca.loc[ca["chain"].eq("B")].sort_values(["resnum", "icode"], kind="stable").reset_index(drop=True)
    assert len(b) == 145 and not b.duplicated(["resnum", "icode"]).any()
    xyz = b[["x", "y", "z"]].to_numpy(dtype=float)
    numbers = b["resnum"].to_numpy(dtype=int)
    labels = [str(int(n)) + str(code) for n, code in zip(b["resnum"], b["icode"])]
    distances = np.linalg.norm(xyz[:, None, :] - xyz[None, :, :], axis=2)
    gaps = np.abs(numbers[:, None] - numbers[None, :])
    assert distances.shape == (145, 145) and np.isfinite(distances).all()
    assert np.allclose(distances, distances.T, rtol=0, atol=1e-12)
    assert np.allclose(np.diag(distances), 0, rtol=0, atol=1e-12)

    # Strict distance threshold, PDB numbering gap >2, unique pairs i<j.
    counts = {
        int(cutoff): int(np.triu((gaps > 2) & (distances < cutoff), k=1).sum())
        for cutoff in (6.0, 8.0, 10.0)
    }
    assert counts == {6: 174, 8: 390, 10: 920}
    i = b.index[b["resnum"].eq(7) & b["residue"].eq("GLU")].tolist()
    j = b.index[b["resnum"].eq(129) & b["residue"].eq("ALA")].tolist()
    assert len(i) == len(j) == 1
    pair_distance = float(distances[i[0], j[0]])
    assert abs(pair_distance - 5.024620483180794) < 1e-12

    reference = pd.read_csv(reference_path, index_col=0)
    assert list(reference.index.astype(str)) == list(reference.columns.astype(str)) == labels
    maximum_difference = float(np.abs(distances - reference.to_numpy(dtype=float)).max())
    assert maximum_difference <= 5.1e-9, "Distance matrix differs from the prior eight-decimal export"

    output = root / "results"
    output.mkdir(exist_ok=True)
    table = pd.DataFrame(distances, index=labels, columns=labels)
    table.index.name = "PDB_residue_id_chain_B"
    matrix_path = output / "b_ca_distance_matrix_angstrom.csv"
    table.to_csv(matrix_path, float_format="%.8f", lineterminator="\n")
    exported_matrix_identical = matrix_path.read_bytes() == reference_path.read_bytes()
    pd.DataFrame([
        {"chain": "B", "cutoff_angstrom": cutoff, "distance_rule": "<", "pdb_number_gap_rule": ">2",
         "pair_rule": "i<j", "unique_pair_count": count}
        for cutoff, count in counts.items()
    ]).to_csv(output / "cutoff_counts.csv", index=False)

    with plt.style.context("dark_background"):
        fig, ax = plt.subplots(figsize=(8, 7), facecolor="#0A0A0C")
        ax.set_facecolor("#0A0A0C")
        image = ax.imshow(distances, origin="lower", cmap="magma", interpolation="nearest")
        ticks = np.unique(np.linspace(0, len(numbers) - 1, 8, dtype=int))
        ax.set_xticks(ticks, labels=numbers[ticks])
        ax.set_yticks(ticks, labels=numbers[ticks])
        ax.set(xlabel="PDB residue number (chain B)", ylabel="PDB residue number (chain B)",
               title="1A3N chain B: C-alpha distance matrix")
        fig.colorbar(image, ax=ax, label="C-alpha distance (Å)")
        fig.tight_layout()
        fig.savefig(output / "distance-matrix.png", dpi=200)
        fig.savefig(output / "distance-matrix.svg")
        plt.close(fig)

    # The real fixed PDB coordinates are embedded; only the optional display library uses the network.
    structure_html = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Public 1A3N structure</title>
<style>body{margin:0;background:#0a0a0c;color:white;font:16px system-ui}#viewer{width:100vw;height:85vh;position:relative}p{padding:0 20px}</style>
<div id="viewer"></div><p>Public experimental structure 1A3N. Drag to rotate; scroll/pinch to zoom. This is not a predicted structure.</p>
<script src="https://3Dmol.org/build/3Dmol-min.js"></script><script>
const pdb = PDB_DATA;
const view = $3Dmol.createViewer("viewer", {backgroundColor:"#0a0a0c"});
view.addModel(pdb,"pdb");
for (const [chain,color] of Object.entries({A:"#55C9E8",B:"#FFAD66",C:"#AB91F2",D:"#71D6A3"})) view.setStyle({chain},{cartoon:{color}});
view.setStyle({resn:"HEM"},{stick:{colorscheme:"Jmol",radius:0.22}});view.zoomTo();view.render();
</script></html>""".replace("PDB_DATA", json.dumps(first_model + "\nEND\n"))
    (output / "structure-view.html").write_text(structure_html, encoding="utf-8")
    summary = {
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "execution_environment": "Host Python re-run of fixed public inputs; not a new physical-device run",
        "software": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "matplotlib": matplotlib.__version__},
        "chain": "B", "ca_count": len(b), "matrix_shape": list(distances.shape),
        "distance_unit": "angstrom", "contact_definition": "strict distance < cutoff; PDB number gap >2; unique i<j",
        "counts": counts, "GLU7_ALA129_CA_distance_angstrom": pair_distance,
        "reference_maximum_difference_angstrom": maximum_difference,
        "reference_comparison": "Prior exported matrix is rounded to eight decimal places",
        "exported_matrix_byte_identical_to_reference": exported_matrix_identical,
        "selected_coordinates_match_supplied_pdb": True, "validation_passed": True,
    }
    (output / "run-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print("Input hashes and PDB/CSV coordinate checks passed.")
    print("Chain B: 145 C-alpha atoms; distance matrix 145 x 145, unit Å.")
    print("Unique pair counts at strict <6/<8/<10 Å:", counts)
    print(f"Glu7-Ala129 C-alpha distance: {pair_distance:.12f} Å")
    print(f"Maximum difference vs prior rounded matrix: {maximum_difference:.3g} Å")
    print("Validation passed. Files saved in results/.")
    return summary


if __name__ == "__main__":
    run_analysis()
