"""Archive byte-identical upstream responses named in the frozen provenance manifest."""
from pathlib import Path
import gzip,hashlib,json,re
import requests
ROOT=Path(__file__).resolve().parent
sources=json.loads((ROOT/"data/sources.json").read_text())
out=ROOT/"data/raw";out.mkdir(exist_ok=True)
report=[]
for source in sources:
    filename=re.sub(r"[^a-z0-9]+","-",source["name"].lower()).strip("-")+".gz"
    request=source.get("request")
    response=requests.post(source["url"],data=request,timeout=(20,180),stream=True) if request else requests.get(source["url"],timeout=(20,180),stream=True)
    response.raise_for_status();digest=hashlib.sha256();size=0
    path=out/filename
    with path.open("wb") as file, gzip.GzipFile(fileobj=file,mode="wb",mtime=0) as compressed:
        for chunk in response.iter_content(1024*1024):
            digest.update(chunk);size+=len(chunk);compressed.write(chunk)
    if digest.hexdigest()!=source["sha256"]:
        raise RuntimeError("Upstream response changed; do not relabel it as the original: "+source["name"])
    row=dict(name=source["name"],file="data/raw/"+filename,bytes=size,compressed_bytes=path.stat().st_size,sha256=digest.hexdigest())
    report.append(row);print(row,flush=True)
(ROOT/"data/raw-manifest.json").write_text(json.dumps(report,indent=2)+"\n")
