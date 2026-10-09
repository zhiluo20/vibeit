"""Freeze public source data. Authoring only; no R or native bioinformatics tools."""
from pathlib import Path
import csv, datetime, gzip, hashlib, io, json, warnings
import xml.etree.ElementTree as ET
import numpy as np
import requests
import rdata

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
SOURCES = []
SESSION = requests.Session()
SESSION.headers["User-Agent"] = "VibeIt-Studio-Cookbook/1.0 (educational data snapshot)"

def fetch(url, **kwargs):
    response = SESSION.get(url, timeout=(20, 180), **kwargs)
    response.raise_for_status()
    return response

def record(name, url, raw, license, **extra):
    SOURCES.append(dict(name=name, url=url, sha256=hashlib.sha256(raw).hexdigest(),
                        retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        license=license, **extra))

def save(name, obj):
    raw = json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode()
    (DATA / (name + ".json.gz")).write_bytes(gzip.compress(raw, mtime=0))
    print(name, len(raw), "JSON bytes", hashlib.sha256(raw).hexdigest(), flush=True)

def freeze_sequences():
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = dict(db="nuccore", id="NM_000518.5,NM_000519.4", rettype="gb", retmode="xml")
    response = fetch(url, params=params)
    records = []
    for rec in ET.fromstring(response.content).findall("GBSeq"):
        for f in rec.findall(".//GBFeature"):
            if f.findtext("GBFeature_key") != "CDS":
                continue
            qualifiers = {q.findtext("GBQualifier_name"): q.findtext("GBQualifier_value")
                          for q in f.findall(".//GBQualifier")}
            location = f.findtext("GBFeature_location")
            start, end = map(int, location.split(".."))
            seq = rec.findtext("GBSeq_sequence").upper()
            records.append(dict(accession=rec.findtext("GBSeq_accession-version"),
                description=rec.findtext("GBSeq_definition"), gene=qualifiers["gene"],
                sequence=seq, cds_start=start, cds_end=end,
                protein_id=qualifiers["protein_id"], translation=qualifiers["translation"]))
    assert {r["gene"] for r in records} == {"HBB", "HBD"}
    record("RefSeq HBB/HBD", response.url, response.content, "NCBI public sequence data",
           accessions=[r["accession"] for r in records], conversion="GenBank XML CDS uses 1-based inclusive coordinates")
    save("sequences", dict(records=records))

def freeze_airway():
    commit = "596678815f4ade04a9711997150949b9782aeddc"
    url = f"https://raw.githubusercontent.com/bioconductor-source/airway/{commit}/data/airway.RData"
    response = fetch(url)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        airway = rdata.conversion.convert(rdata.parser.parse_data(response.content))["airway"]
    counts = np.asarray(airway.assays.data.listData["counts"])
    genes = airway.rowRanges.partitioning.NAMES.tolist()
    samples = airway.colData.rownames.tolist()
    columns = airway.colData.listData
    metadata = [dict(sample=samples[i], donor=str(columns["cell"][i]),
                     condition="treated" if str(columns["dex"][i]) == "trt" else "control",
                     geo=str(columns["SampleName"][i])) for i in range(len(samples))]
    assert counts.shape == (63677, 8) and len(genes) == counts.shape[0]
    assert np.equal(counts, np.floor(counts)).all() and (counts >= 0).all()
    record("airway read counts", url, response.content, "LGPL (airway package); original experiment: Himes et al. 2014",
           commit=commit, geo="GSE52778", doi="10.1371/journal.pone.0099625", shape=list(counts.shape),
           conversion="rdata 1.1.0: assays.data.listData['counts'], rowRanges.partitioning.NAMES, colData; no scaling or gene subsetting")
    save("airway", dict(genes=genes, samples=samples, counts=counts.astype(int).tolist(), metadata=metadata,
                       library_totals=counts.sum(axis=0).astype(int).tolist()))
    return set(genes)

def freeze_reactome(genes):
    # Stream the full mapping to compute the upstream hash without storing a large archive.
    url = "https://reactome.org/download/current/Ensembl2Reactome.txt"
    response = fetch(url, stream=True)
    digest = hashlib.sha256()
    pathways = {}
    buffer = b""
    total = 0
    for chunk in response.iter_content(1024 * 1024):
        digest.update(chunk); total += len(chunk); buffer += chunk
        lines = buffer.split(b"\n"); buffer = lines.pop()
        for line in lines:
            fields = line.decode("utf-8").rstrip("\r").split("\t")
            if len(fields) != 6 or fields[5] != "Homo sapiens" or fields[0] not in genes:
                continue
            gene, pid, link, name, evidence, species = fields
            row = pathways.setdefault(pid, dict(id=pid, name=name, url=link, genes=set(), evidence=set()))
            row["genes"].add(gene); row["evidence"].add(evidence)
    # The published mapping is newline-terminated; fail if its schema changes.
    assert not buffer.strip(), "Unexpected unterminated Reactome mapping"
    assert len(pathways) > 500
    version = fetch("https://reactome.org/ContentService/data/database/version").text.strip()
    SOURCES.append(dict(name="Reactome human Ensembl pathway mapping", url=url, sha256=digest.hexdigest(),
                        retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        license="CC0 1.0", version=version, bytes=total,
                        conversion="Lowest-level pathways; Homo sapiens; retain genes present in the complete airway matrix; deduplicate memberships"))
    rows = [dict(**{k:v for k,v in row.items() if k not in ("genes", "evidence")},
                 genes=sorted(row["genes"]), evidence=sorted(row["evidence"])) for row in pathways.values()]
    save("reactome", dict(version=version, pathways=sorted(rows, key=lambda r:r["id"])))

def freeze_network():
    names = ["TP53", "MDM2", "MDM4", "ATM", "ATR", "CHEK1", "CHEK2", "BRCA1", "BRCA2", "CDKN1A", "BAX", "BCL2"]
    params = dict(identifiers="\r".join(names), species=9606,
                  caller_identity="vibeit-studio-cookbook", network_type="physical",
                  required_score=400, add_nodes=0)
    url = "https://string-db.org/api/json/network"
    response = SESSION.post(url, data=params, timeout=(20,60)); response.raise_for_status()
    edges = response.json()
    mapping_url = "https://string-db.org/api/json/get_string_ids"
    mapping_params = dict(identifiers="\r".join(names), species=9606, limit=1, echo_query=1,
                          caller_identity=params["caller_identity"])
    mapping = SESSION.post(mapping_url, data=mapping_params, timeout=(20,60)); mapping.raise_for_status()
    version_url = "https://string-db.org/api/json/version"
    version = fetch(version_url).json()
    assert edges and all(int(r["ncbiTaxonId"]) == 9606 for r in edges)
    assert len(mapping.json()) == len(names)
    record("STRING physical network",url,response.content,"CC BY 4.0 (STRING data)",request=params,version=version)
    record("STRING identifier mapping",mapping_url,mapping.content,"CC BY 4.0 (STRING data)",request=mapping_params)
    for row in edges:
        row["ncbiTaxonId"] = int(row["ncbiTaxonId"])
    resolved = mapping.json()
    for row in resolved:
        row["ncbiTaxonId"] = int(row["ncbiTaxonId"])
    save("network",dict(query=names,request=params,version=version,mapping=resolved,edges=edges))

def freeze_structure():
    url = "https://files.rcsb.org/download/1A3N.pdb"
    response = fetch(url)
    meta_url = "https://data.rcsb.org/rest/v1/core/entry/1A3N"
    meta = fetch(meta_url)
    assert response.text.startswith("HEADER") and "HETATM" in response.text
    record("PDB 1A3N coordinates",url,response.content,"CC0 1.0",pdb_id="1A3N")
    record("RCSB 1A3N entry metadata",meta_url,meta.content,"CC0 1.0")
    save("structure",dict(pdb_id="1A3N",pdb=response.text,entry=meta.json()))

if __name__ == "__main__":
    freeze_sequences()
    genes = freeze_airway()
    freeze_reactome(genes)
    freeze_network()
    freeze_structure()
    (DATA/"sources.json").write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2)+"\n")
