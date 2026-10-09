"""Read simulator-saved notebook evidence after actual UI Run All. No app mutation."""
from pathlib import Path
import argparse,datetime,json,time
p=argparse.ArgumentParser();p.add_argument("folder");p.add_argument("filename");p.add_argument("--timeout",type=int,default=30)
p.add_argument("--device",choices=["ipad","iphone"],default="ipad")
args=p.parse_args();path=Path(args.folder)/args.filename;deadline=time.monotonic()+args.timeout
while time.monotonic()<deadline:
    notebook=json.loads(path.read_text());cells=[c for c in notebook['cells'] if c['cell_type']=='code']
    errors=[dict(name=o.get('ename'),message=o.get('evalue')) for c in cells for o in c.get('outputs',[]) if o.get('output_type')=='error']
    if errors:raise SystemExit(json.dumps(errors))
    streams=[''.join(o.get('text','')) for c in cells for o in c.get('outputs',[]) if o.get('output_type')=='stream']
    environment=next((s for s in streams if s.startswith('Python:')),'')
    if all(c.get('execution_count') is not None for c in cells) and '3.13.14' in environment:
        images=sum('image/png' in o.get('data',{}) for c in cells for o in c.get('outputs',[]))
        html=sum('text/html' in o.get('data',{}) for c in cells for o in c.get('outputs',[]))
        device='iPad Simulator / iPadOS 27.0' if args.device=='ipad' else 'iPhone Simulator / iOS 27.0'
        row=dict(filename=args.filename,status='passed',app_version='1.0.2 (8)',device=device,
            executed_cells=len(cells),png_figures=images,html_outputs=html,python=environment.splitlines()[0],
            validated_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
        report=Path(__file__).resolve().parent/('qa/'+args.device+'-execution.json')
        old=json.loads(report.read_text()) if report.exists() else []
        report.write_text(json.dumps([r for r in old if r['filename']!=args.filename]+[row],indent=2)+'\n')
        print(json.dumps(row));break
    time.sleep(.5)
else:raise SystemExit('App run incomplete: '+args.filename)
