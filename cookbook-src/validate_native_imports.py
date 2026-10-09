"""Validate actual installed-app file imports on an isolated, author-owned Simulator.

Uses simctl's documented external-URL opening; does not substitute for Files picker,
editor Run All, or export UI validation. The app's saved files are checked directly.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,time
from catalog import COURSES

ROOT=Path(__file__).resolve().parent

def normalized(value):return ''.join(value) if isinstance(value,list) else value

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--udid',required=True)
    parser.add_argument('--documents',type=Path,required=True)
    parser.add_argument('--downloads',type=Path,required=True)
    parser.add_argument('--progress',type=Path,required=True)
    args=parser.parse_args()
    incoming=args.documents/'QA-Incoming';incoming.mkdir(exist_ok=True)
    rows=json.loads(args.progress.read_text()) if args.progress.exists() else []
    complete={row['filename']:row for row in rows}
    for course in COURSES:
        if course['discipline']=='bioinformatics':continue
        for locale in ['en','zh-hans']:
            filename=course['id']+'.'+locale+'.ipynb'
            source=args.downloads/filename;digest=hashlib.sha256(source.read_bytes()).hexdigest()
            if filename in complete:
                assert complete[filename]['source_sha256']==digest
                continue
            name='import-'+digest[:8]+'-'+filename;staged=incoming/name;staged.write_bytes(source.read_bytes())
            target=args.documents/'Vibeit'/name
            # A timeout may still complete an asynchronous import. Check the existing
            # target first, avoiding duplicate imports when resuming an interrupted run.
            if not target.exists():
                result=subprocess.run(['xcrun','simctl','openurl',args.udid,staged.as_uri()],capture_output=True,text=True,timeout=60)
                assert result.returncode==0,result.stderr
            expected=json.loads(source.read_text(encoding='utf-8'));deadline=time.monotonic()+120
            imported=None
            while time.monotonic()<deadline:
                try:
                    candidate=json.loads(target.read_text(encoding='utf-8'))
                    if [(c['cell_type'],normalized(c['source'])) for c in candidate['cells']]==[(c['cell_type'],normalized(c['source'])) for c in expected['cells']]:
                        imported=candidate;break
                except (OSError,json.JSONDecodeError):pass
                time.sleep(.2)
            assert imported is not None,'Import did not produce matching saved cells: '+filename
            assert imported['metadata']['vibeit_cookbook']['snapshots']==expected['metadata']['vibeit_cookbook']['snapshots']
            assert imported['cells'][0]['metadata']['raw_mimetype']=='text/html'
            row=dict(filename=filename,imported_filename=name,discipline=course['discipline'],source_sha256=digest,
                imported_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),cells_prose_snapshots_and_raw_html='passed',status='passed')
            rows.append(row);complete[filename]=row
            args.progress.write_text(json.dumps(rows,indent=2)+'\n')
            print('Imported',len(rows),filename,flush=True)
    assert len(rows)==84
    report=dict(mode='Actual installed-app external file-URL import; distinct from manual Files picker, editor Run All, and export UI',
        device='Cookbook Expansion QA iPad / iPadOS 27.0 Simulator',app='1.0.2 (8)',results=rows,complete=True,real_device_tested=False)
    (ROOT/'qa/expansion-native-imports.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 84 actual installed-app imports with complete cells and snapshots')

if __name__=='__main__':main()
