"""Teaching functions copied verbatim into notebooks; no cookbook module is needed at runtime."""
from pathlib import Path
import base64, gzip, hashlib, json
import numpy as np
import pandas as pd
from scipy.stats import hypergeom
import networkx as nx

def load_snapshot(recipe_id, expected_sha256, snapshot_key):
    """Read embedded data from this notebook, including a renamed copy."""
    for path in sorted(Path.cwd().glob("*.ipynb")):
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
            metadata = notebook.get("metadata", {}).get("vibeit_cookbook", {})
            blob = metadata.get("snapshots", {}).get(snapshot_key)
            if metadata.get("recipe_id") != recipe_id or not blob:
                continue
            if blob.get("sha256") != expected_sha256:
                continue
            raw = gzip.decompress(base64.b64decode(blob["gzip_base64"], validate=True))
            if hashlib.sha256(raw).hexdigest() != expected_sha256:
                raise ValueError("Embedded snapshot checksum mismatch: " + snapshot_key)
            return json.loads(raw)
        except (OSError, json.JSONDecodeError):
            continue
    raise FileNotFoundError(
        "Save/open the complete .ipynb in the active working folder. "
        "The embedded snapshot could not be located for " + recipe_id)

def parse_fasta(text):
    records, label, chunks = [], None, []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if label is not None:
                records.append((label, "".join(chunks).upper()))
            label, chunks = line[1:].strip(), []
            if not label:
                raise ValueError("FASTA header is empty")
        else:
            if label is None:
                raise ValueError("FASTA requires a header before sequence lines")
            chunks.append(line)
    if label is not None:
        records.append((label, "".join(chunks).upper()))
    if not records:
        raise ValueError("No FASTA records")
    if len({label.split()[0] for label, seq in records}) != len(records):
        raise ValueError("Duplicate FASTA identifiers")
    for label, seq in records:
        if not seq or set(seq) - set("ACGTRYSWKMBDHVN"):
            raise ValueError("Empty or invalid DNA sequence: " + label)
    return records

def translate_cds(sequence):
    sequence = sequence.upper()
    if len(sequence) % 3:
        raise ValueError("Complete CDS length must be divisible by three")
    bases = "TCAG"
    amino_acids = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
    codons = [a+b+c for a in bases for b in bases for c in bases]
    table = dict(zip(codons, amino_acids))
    protein = "".join(table.get(sequence[i:i+3], "X") for i in range(0,len(sequence),3))
    if "*" in protein[:-1]:
        raise ValueError("Internal stop codon: check the reading frame or genetic code")
    return protein.removesuffix("*")

def gc_fraction(sequence):
    sequence = sequence.upper()
    denominator = sum(sequence.count(base) for base in "ACGT")
    if denominator == 0:
        return float("nan")
    return (sequence.count("G") + sequence.count("C")) / denominator

def affine_align(a, b, local=False, match=2, mismatch=-1, gap_open=-3, gap_extend=-1):
    """Three-state affine alignment. X consumes a; Y consumes b. Ties favor M,X,Y."""
    if not a or not b or len(a) > 2000 or len(b) > 2000:
        raise ValueError("Use two nonempty sequences, each at most 2,000 bases")
    if gap_open > 0 or gap_extend > 0:
        raise ValueError("Gap penalties must be nonpositive")
    n, m = len(a), len(b)
    scores = np.full((3,n+1,m+1), -np.inf)
    trace = np.full((3,n+1,m+1), 255, dtype=np.uint8)
    scores[0,0,0] = 0
    if local:
        scores[:] = 0
    else:
        for i in range(1,n+1):
            scores[1,i,0] = gap_open + (i-1)*gap_extend
            trace[1,i,0] = 0 if i == 1 else 1
        for j in range(1,m+1):
            scores[2,0,j] = gap_open + (j-1)*gap_extend
            trace[2,0,j] = 0 if j == 1 else 2
    best = (0.0,0,0,0)
    for i in range(1,n+1):
        for j in range(1,m+1):
            values = scores[:,i-1,j-1]
            parent = int(np.argmax(values))
            scores[0,i,j] = values[parent] + (match if a[i-1] == b[j-1] else mismatch)
            trace[0,i,j] = parent
            values = (scores[0,i-1,j]+gap_open, scores[1,i-1,j]+gap_extend)
            parent = int(np.argmax(values))
            scores[1,i,j] = values[parent]; trace[1,i,j] = (0,1)[parent]
            values = (scores[0,i,j-1]+gap_open, scores[2,i,j-1]+gap_extend)
            parent = int(np.argmax(values))
            scores[2,i,j] = values[parent]; trace[2,i,j] = (0,2)[parent]
            if local:
                for state in range(3):
                    if scores[state,i,j] <= 0:
                        scores[state,i,j] = 0; trace[state,i,j] = 255
                state = int(np.argmax(scores[:,i,j]))
                if scores[state,i,j] > best[0]:
                    best = (float(scores[state,i,j]),state,i,j)
    if local:
        score, state, i, j = best
    else:
        i, j = n, m; state = int(np.argmax(scores[:,i,j])); score = float(scores[state,i,j])
    end = (i,j); aa, bb, path = [], [], [(i,j)]
    while i or j:
        if local and scores[state,i,j] == 0:
            break
        parent = int(trace[state,i,j])
        if parent == 255:
            raise ValueError("Invalid traceback")
        if state == 0:
            aa.append(a[i-1]); bb.append(b[j-1]); i-=1; j-=1
        elif state == 1:
            aa.append(a[i-1]); bb.append("-"); i-=1
        else:
            aa.append("-"); bb.append(b[j-1]); j-=1
        state = parent; path.append((i,j))
    return dict(a="".join(reversed(aa)),b="".join(reversed(bb)),score=score,
                start=(i,j),end=end,path=list(reversed(path)),matrix=np.max(scores,axis=0))

def alignment_summary(result, length_a, length_b):
    a, b = result["a"], result["b"]
    columns = len(a)
    matches = sum(x == y and x != "-" for x,y in zip(a,b))
    nongap = sum(x != "-" and y != "-" for x,y in zip(a,b))
    return dict(score=result["score"],columns=columns,matches=matches,
        identity_all_columns=matches/columns if columns else 0,
        identity_nongap_columns=matches/nongap if nongap else 0,
        coverage_a=(len(a)-a.count("-"))/length_a,
        coverage_b=(len(b)-b.count("-"))/length_b,
        gap_characters=a.count("-")+b.count("-"))

def validate_counts(counts, metadata):
    if not counts.index.is_unique or not counts.columns.is_unique:
        raise ValueError("Gene and sample identifiers must be unique")
    if not metadata.index.is_unique or list(counts.columns) != list(metadata.index):
        raise ValueError("Sample columns must match metadata order exactly")
    values = counts.to_numpy()
    if not np.isfinite(values).all() or (values < 0).any() or not np.equal(values,np.floor(values)).all():
        raise ValueError("Counts must be finite nonnegative integers")
    if (values.sum(axis=0) == 0).any():
        raise ValueError("A sample has no reads")
    if set(metadata.condition) != {"control","treated"}:
        raise ValueError("Expected control and treated conditions")
    for donor, rows in metadata.groupby("donor", sort=True):
        if len(rows) != 2 or set(rows.condition) != {"control","treated"}:
            raise ValueError("Each donor needs one control and one treated sample: " + str(donor))

def normalize_counts(counts, min_count=10, min_samples=4):
    values = counts.to_numpy(dtype=float)
    keep = (values >= min_count).sum(axis=1) >= min_samples
    filtered = counts.loc[keep].astype(float)
    positive = (filtered.to_numpy() > 0).all(axis=1)
    if positive.sum() == 0:
        raise ValueError("Median-ratio method needs genes positive in every sample")
    reference_values = filtered.to_numpy()[positive]
    geometric_means = np.exp(np.log(reference_values).mean(axis=1))
    factors = np.median(reference_values / geometric_means[:,None], axis=0)
    if not np.isfinite(factors).all() or (factors <= 0).any():
        raise ValueError("Invalid size factors")
    factors /= np.exp(np.log(factors).mean())
    normalized = filtered / factors
    return filtered, pd.Series(factors,index=counts.columns,name="size_factor"), normalized

def paired_response(log_counts, metadata, min_effect=1.0, min_consistent=3):
    differences = {}
    for donor, rows in metadata.groupby("donor",sort=True):
        control = rows.index[rows.condition == "control"][0]
        treated = rows.index[rows.condition == "treated"][0]
        differences[donor] = log_counts[treated] - log_counts[control]
    differences = pd.DataFrame(differences)
    response = pd.DataFrame(dict(mean_log2_change=differences.mean(axis=1),
                                 positive_pairs=(differences>0).sum(axis=1),
                                 negative_pairs=(differences<0).sum(axis=1)))
    response["direction"] = "other"
    response.loc[(response.mean_log2_change>=min_effect)&(response.positive_pairs>=min_consistent),"direction"]="up"
    response.loc[(response.mean_log2_change<=-min_effect)&(response.negative_pairs>=min_consistent),"direction"]="down"
    return differences, response

def bh_adjust(pvalues):
    p = np.asarray(pvalues,dtype=float)
    if not len(p):
        return p.copy()
    if not np.isfinite(p).all() or (p<0).any() or (p>1).any():
        raise ValueError("p-values must be finite and in [0,1]")
    order = np.argsort(p,kind="stable")
    adjusted = np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1]
    result = np.empty_like(p); result[order] = np.minimum(adjusted,1)
    return result

def overrepresentation(up, down, expressed, pathways, min_size=10, max_size=500):
    annotated = set().union(*(set(row["genes"]) for row in pathways)) if pathways else set()
    background = set(expressed) & annotated
    columns = ["direction","pathway","name","background_size","query_size","term_size","overlap","pvalue","genes","qvalue"]
    rows = []
    for direction, supplied in (("up",up),("down",down)):
        query = set(supplied) & background
        for term in pathways:
            members = set(term["genes"]) & background
            if not min_size <= len(members) <= max_size:
                continue
            hits = sorted(query & members)
            p = float(hypergeom.sf(len(hits)-1,len(background),len(members),len(query))) if query else 1.0
            rows.append(dict(direction=direction,pathway=term["id"],name=term["name"],
                background_size=len(background),query_size=len(query),term_size=len(members),
                overlap=len(hits),pvalue=p,genes=";".join(hits)))
    result = pd.DataFrame(rows)
    if len(result):
        result["qvalue"] = bh_adjust(result.pvalue.to_numpy())
        result = result.sort_values(["qvalue","pvalue","pathway","direction"],kind="stable")
    else:
        result = pd.DataFrame(columns=columns)
    return background,result

def physical_graph(snapshot, threshold=0.7):
    if not 0 <= threshold <= 1:
        raise ValueError("Network threshold must be between 0 and 1")
    graph = nx.Graph()
    for mapping in snapshot["mapping"]:
        graph.add_node(mapping["preferredName"],string_id=mapping["stringId"])
    for row in snapshot["edges"]:
        a, b = row["preferredName_A"], row["preferredName_B"]
        if a == b or row["score"] < threshold:
            continue
        if row["ncbiTaxonId"] != 9606 or a not in graph or b not in graph:
            raise ValueError("Unexpected network species or neighbor")
        attrs = {key:float(row.get(key,0)) for key in ("score","escore","dscore","tscore")}
        if not graph.has_edge(a,b) or graph[a][b]["score"] < attrs["score"]:
            graph.add_edge(a,b,**attrs)
    return graph

def parse_pdb(text):
    """First model; choose highest occupancy altloc, then blank/A/lexical order."""
    rows, first_model, inside = {}, None, True
    for line in text.splitlines():
        record = line[:6].strip()
        if record == "MODEL":
            number = line[10:14].strip()
            if first_model is None:
                first_model = number
            inside = number == first_model
        if record == "ENDMDL" and inside:
            break
        if record not in ("ATOM","HETATM") or not inside:
            continue
        try:
            atom = dict(record=record,serial=int(line[6:11]),atom=line[12:16].strip(),altloc=line[16:17].strip(),
                residue=line[17:20].strip(),chain=line[21:22].strip(),resnum=int(line[22:26]),icode=line[26:27].strip(),
                x=float(line[30:38]),y=float(line[38:46]),z=float(line[46:54]),
                occupancy=float(line[54:60].strip() or 0),bfactor=float(line[60:66].strip() or 0),element=line[76:78].strip())
        except ValueError as exc:
            raise ValueError("Invalid PDB numeric fields") from exc
        key = (record,atom["chain"],atom["resnum"],atom["icode"],atom["residue"],atom["atom"])
        rank = (atom["occupancy"],atom["altloc"]=="",atom["altloc"]=="A")
        old = rows.get(key)
        if old is None or rank > old[0] or (rank == old[0] and atom["altloc"] < old[1]["altloc"]):
            rows[key] = (rank,atom)
    columns = ["record","serial","atom","altloc","residue","chain","resnum","icode","x","y","z","occupancy","bfactor","element"]
    atoms = pd.DataFrame([entry[1] for entry in rows.values()],columns=columns)
    if atoms.empty:
        raise ValueError("No atoms in the first model")
    if not np.isfinite(atoms[["x","y","z","occupancy"]].to_numpy()).all():
        raise ValueError("Nonfinite coordinates or occupancy")
    return atoms
