"""Prepare an internal QA notebook for actual on-device kernel compatibility checks.

This author-only harness executes each released notebook's verbatim code in an
isolated namespace/folder, records actual outputs, and does not replace editor UI QA.
"""
from pathlib import Path
import argparse,hashlib,json,shutil
import nbformat
from catalog import COURSES

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--destination',required=True);parser.add_argument('--subject');parser.add_argument('--only',action='append',help='Explicit course IDs, including bioinformatics');args=parser.parse_args()
destination=Path(args.destination);destination.mkdir(parents=True,exist_ok=True)
manifest=[]
for course in COURSES:
    if args.only and course['id'] not in args.only:continue
    if not args.only and course['discipline']=='bioinformatics':continue
    if args.subject and course['discipline']!=args.subject:continue
    for language in ['en','zh-hans']:
        source=ROOT.parent/'cookbook/downloads'/(course['id']+'.'+language+'.ipynb')
        relative=Path('.fixtures')/(course['id']+'.'+language)
        subfolder=destination/relative;subfolder.mkdir(parents=True,exist_ok=True)
        notebook=nbformat.read(source,4)
        for cell in notebook.cells:
            if cell.cell_type=='code':cell.execution_count=None;cell.outputs=[]
        target=subfolder/source.name;nbformat.write(notebook,target)
        manifest.append(dict(filename=source.name,folder=str(relative),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),recipe_id=course['id'],discipline=course['discipline'],locale=language))
(destination/'native-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

program=r'''from pathlib import Path
import os,sys,json,base64,io,time,platform,socket,contextlib,traceback
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import IPython.display as ipython_display

BASE_FOLDER=Path.cwd()
manifest=json.loads((BASE_FOLDER/'native-manifest.json').read_text(encoding='utf-8'))
REPORT=BASE_FOLDER/'native-report.json'
original_connect=socket.socket.connect;original_create=socket.create_connection
def deny_network(*args,**kwargs):raise RuntimeError('Network disabled in native cookbook QA')
socket.socket.connect=deny_network;socket.create_connection=deny_network
original_display=ipython_display.display;original_show=plt.show
results=[];active_outputs=[]
def collect_display(value,*args,**kwargs):
    if hasattr(value,'_repr_html_'):
        raw=value._repr_html_()
        if raw is not None:
            active_outputs.append({'output_type':'display_data','metadata':{},'data':{'text/html':raw}});return
    active_outputs.append({'output_type':'display_data','metadata':{},'data':{'text/plain':repr(value)}})
def collect_figures(*args,**kwargs):
    for number in plt.get_fignums():
        figure=plt.figure(number);buffer=io.BytesIO();figure.savefig(buffer,format='png',dpi=120)
        active_outputs.append({'output_type':'display_data','metadata':{},'data':{'image/png':base64.b64encode(buffer.getvalue()).decode()}})
    plt.close('all')
try:
    ipython_display.display=collect_display;plt.show=collect_figures
    for entry in manifest:
        path=BASE_FOLDER/entry['folder']/entry['filename'];os.chdir(path.parent)
        notebook=json.loads(path.read_text(encoding='utf-8'));namespace={'__name__':'__main__'};started=time.monotonic();execution=0
        row=dict(entry,status='running',python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__)
        try:
            for index,cell in enumerate(notebook['cells']):
                if cell['cell_type']!='code':continue
                execution+=1;active_outputs=[];stdout=io.StringIO();stderr=io.StringIO()
                source=''.join(cell['source']) if isinstance(cell['source'],list) else cell['source']
                with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
                    exec(compile(source,entry['filename']+':cell'+str(index),'exec'),namespace)
                if stdout.getvalue():active_outputs.insert(0,{'output_type':'stream','name':'stdout','text':stdout.getvalue()})
                if stderr.getvalue():active_outputs.append({'output_type':'stream','name':'stderr','text':stderr.getvalue()})
                cell['execution_count']=execution;cell['outputs']=active_outputs
            images=sum('image/png' in output.get('data',{}) for cell in notebook['cells'] for output in cell.get('outputs',[]))
            if images<3:raise AssertionError('Missing actual figures: '+str(images))
            row.update(status='passed',executed_code_cells=execution,png_figures=images,seconds=round(time.monotonic()-started,2),offline_guard=True)
            notebook['metadata']['vibeit_cookbook']['native_qa']=row
            path.write_text(json.dumps(notebook,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
        except Exception as error:
            row.update(status='failed',executed_code_cells=execution,error=str(error),traceback=traceback.format_exc())
        results.append(row);REPORT.write_text(json.dumps({'mode':'actual app kernel batch; distinct from editor UI validation','results':results,'complete':len(results)==len(manifest)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(row['status'],entry['filename'],flush=True)
finally:
    os.chdir(BASE_FOLDER);ipython_display.display=original_display;plt.show=original_show;plt.close('all')
    socket.socket.connect=original_connect;socket.create_connection=original_create
print('Native completed:',len(results),'of',len(manifest),'; failures:',sum(row['status']!='passed' for row in results))
'''
nb=nbformat.v4.new_notebook(cells=[
    nbformat.v4.new_markdown_cell('# Internal Cookbook native-kernel QA\n\nAuthor-only compatibility harness. Runs the exact code from each isolated course fixture, blocks Python network connections and records real images/tables. Individual editor import, HTML/3D display, mobile reading and exports are validated separately.'),
    nbformat.v4.new_code_cell(program)
],metadata={'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'}})
nbformat.write(nb,destination/'00-native-kernel-qa.ipynb')
print('Prepared',len(manifest),'isolated notebook fixtures in',destination)
