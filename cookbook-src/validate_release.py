"""Audit the requested release scope and portable, current executed artifacts."""
from pathlib import Path
import ast,base64,gzip,hashlib,json,os,socket,tempfile
import nbformat
from catalog import COURSES,DISCIPLINES,subject_courses
from build_notebooks import make_notebook

ROOT=Path(__file__).resolve().parent
DOWNLOADS=ROOT.parent/'cookbook/downloads'

def main():
    assert len(DISCIPLINES)==8 and len(COURSES)==50
    assert all(len(subject_courses(d['id']))==(8 if d['id']=='bioinformatics' else 6) for d in DISCIPLINES)
    assert {c['id'] for c in COURSES if c['number']>6}=={'07-imatinib-pocket','08-trastuzumab-interface'}
    rows=[];start=Path.cwd()
    original_connect=socket.socket.connect;original_create=socket.create_connection
    def deny(*args,**kwargs):raise RuntimeError('Network disabled during portability validation')
    socket.socket.connect=deny;socket.create_connection=deny
    try:
        for course in COURSES:
            for language in ('en','zh-hans'):
                path=DOWNLOADS/(course['id']+'.'+language+'.ipynb')
                notebook=nbformat.read(path,4);fresh=make_notebook(course,language)
                codes=[c.source for c in notebook.cells if c.cell_type=='code']
                assert codes==[c.source for c in fresh.cells if c.cell_type=='code'],path.name
                assert notebook.metadata.vibeit_cookbook.snapshots==fresh.metadata.vibeit_cookbook.snapshots
                assert notebook.metadata.vibeit_cookbook.sources==fresh.metadata.vibeit_cookbook.sources
                intro=notebook.cells[0]
                assert intro.cell_type=='raw' and intro.metadata.raw_mimetype=='text/html'
                assert 'lesson-intro' in intro.source and 'http' not in intro.source
                figures=sum('image/png' in o.get('data',{}) for c in notebook.cells for o in c.get('outputs',[]))
                assert figures>=3
                loader=next(n for source in codes for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='load_snapshot')
                namespace=dict(Path=Path,base64=base64,gzip=gzip,hashlib=hashlib,json=json)
                exec(compile(ast.Module(body=[loader],type_ignores=[]),'embedded-loader','exec'),namespace)
                with tempfile.TemporaryDirectory(prefix='vibeit-portable-') as temporary:
                    moved=Path(temporary)/'new folder';moved.mkdir()
                    target=moved/'renamed lesson.ipynb'
                    # Actual JSON roundtrip after rename/move, with no sidecar files.
                    target.write_text(json.dumps(json.loads(path.read_text(encoding='utf-8')),ensure_ascii=False),encoding='utf-8')
                    os.chdir(moved)
                    for key,blob in notebook.metadata.vibeit_cookbook.snapshots.items():
                        loaded=namespace['load_snapshot'](course['id'],blob.sha256,key)
                        assert loaded==json.loads(gzip.decompress((ROOT/'data'/(key+'.json.gz')).read_bytes()))
                    os.chdir(start)
                rows.append(dict(filename=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                    current_code_and_sources='passed',rename_move_roundtrip='passed',png_figures=figures,offline_guard=True))
    finally:
        os.chdir(start);socket.socket.connect=original_connect;socket.create_connection=original_create
    assert len(rows)==100
    sources=json.loads((ROOT/'data/sources.json').read_text())
    raw=json.loads((ROOT/'data/raw-manifest.json').read_text())
    assert len(sources)==53 and len(raw)==53
    source_hashes={row['name']:row['sha256'] for row in sources}
    for row in raw:
        decoded=gzip.decompress((ROOT/row['file']).read_bytes())
        assert hashlib.sha256(decoded).hexdigest()==row['sha256']==source_hashes[row['name']]
    report=dict(scope={d['id']:len(subject_courses(d['id'])) for d in DISCIPLINES},courses=50,notebooks=rows,
        source_records=len(sources),raw_responses=len(raw),source_artifact_parity='passed')
    (ROOT/'qa/release-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: original 48 workflows plus 2 drug complexes; 100 current portable executed notebooks')

if __name__=='__main__':main()
