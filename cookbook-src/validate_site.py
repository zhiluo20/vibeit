"""Validate public artifact integrity, supported imports, routes and bilingual parity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import ast,base64,gzip,hashlib,json,zipfile,re
import xml.etree.ElementTree as ET
import nbformat
from courses import COURSES
ROOT=Path(__file__).resolve().parent
SITE=ROOT.parent
OUT=SITE/"cookbook"
SUPPORTED={"pathlib","base64","gzip","hashlib","json","platform","numpy","pandas","matplotlib","IPython",
           "collections","html","scipy","networkx","py3Dmol","requests"}

class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.canonical=[];self.alternates=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag in ["a","script","img","link"]:
            value=attrs.get("href") or attrs.get("src")
            if value:self.links.append(value)
        if tag=="link" and attrs.get("rel")=="canonical":self.canonical.append(attrs["href"])
        if tag=="link" and attrs.get("rel")=="alternate":self.alternates.append(attrs.get("hreflang"))

def normalize_code(source):
    # Setup localizes neither calculation nor output labels; source must be byte-identical.
    return source

def main():
    checks=[]
    for course in COURSES:
        versions=[]
        for locale in ["en","zh-hans"]:
            path=OUT/"downloads"/(course["id"]+"."+locale+".ipynb")
            notebook=nbformat.read(path,4);nbformat.validate(notebook)
            assert notebook.metadata.vibeit_cookbook.execution.status=="passed"
            for name,blob in notebook.metadata.vibeit_cookbook.snapshots.items():
                raw=gzip.decompress(base64.b64decode(blob.gzip_base64,validate=True))
                assert hashlib.sha256(raw).hexdigest()==blob.sha256
                assert raw==gzip.decompress((ROOT/"data"/(name+".json.gz")).read_bytes())
            codes=[c for c in notebook.cells if c.cell_type=="code"]
            assert all(c.execution_count is not None and c.outputs for c in codes)
            for cell in codes:
                for node in ast.walk(ast.parse(cell.source)):
                    if isinstance(node,ast.Import):imports=[n.name.split('.')[0] for n in node.names]
                    elif isinstance(node,ast.ImportFrom):imports=[node.module.split('.')[0]]
                    else:continue
                    assert set(imports)<=SUPPORTED,imports
                assert not any(o.output_type=="error" for o in cell.outputs)
            versions.append([normalize_code(c.source) for c in codes])
            checks.append(dict(filename=path.name,format="passed",snapshots="passed",imports="passed",execution="passed",
                bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        assert versions[0]==versions[1],"Calculation differs by locale: "+course["id"]
    pages=list(OUT.rglob("index.html"));assert len(pages)==32
    product_root=re.search(r":root\s*\{(.*?)\}",(SITE/"index.html").read_text(),re.S).group(1)
    brand=(OUT/"assets/brand.css").read_text()
    for name in ["bg","surface","text","muted","accent","accent-2"]:
        expected=re.search(r"--"+name+r"\s*:\s*([^;]+);",product_root).group(1).strip()
        assert "--"+name+":"+expected+";" in brand
    links_checked=0
    for page in pages:
        parser=Links();parser.feed(page.read_text())
        if page.parent.name in {c['slug'] for c in COURSES}:
            assert 'class="source-code"' in page.read_text() and '<span class="k' in page.read_text()
        assert len(parser.canonical)==1 and parser.canonical[0].startswith("https://www.mecury.co.uk/vibeit/cookbook/")
        assert {"en","zh-CN","x-default"}<=set(parser.alternates)
        for link in parser.links:
            parts=urlsplit(link)
            if parts.scheme not in ("","https","http"):continue
            if parts.netloc and parts.netloc!="www.mecury.co.uk":continue
            if not parts.path.startswith("/vibeit/"):continue
            target=SITE/unquote(parts.path[len("/vibeit/"):])
            if parts.path.endswith("/"):target=target/"index.html"
            assert target.exists(),f"Missing local target {page}: {link}"
            links_checked+=1
    with zipfile.ZipFile(OUT/"downloads/vibeit-bioinformatics-cookbook.zip") as archive:
        assert len(archive.namelist())==12
        for name in archive.namelist():assert archive.read(name)==(OUT/"downloads"/name).read_bytes()
    locations=[el.text for el in ET.parse(SITE/"sitemap.xml").getroot().iter() if el.tag.endswith('}loc')]
    assert len([u for u in locations if '/cookbook/' in u])==32
    report=dict(notebooks=checks,pages=len(pages),local_links_checked=links_checked,bilingual_code_parity="passed",brand_palette="exact product tokens",python_highlighting="static Pygments; offline",
                download_archive="passed",sitemap="passed")
    (ROOT/"qa/artifact-validation.json").write_text(json.dumps(report,indent=2)+"\n")
    print(f"PASS: 12 notebooks, {len(pages)} pages, {links_checked} local links, all snapshots and bilingual code verified")

if __name__=="__main__":main()
