"""Generate and execute bilingual standard notebooks with self-contained data."""
from pathlib import Path
import argparse, ast, base64, copy, datetime, gzip, hashlib, html, inspect, json, sys, time
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
import runtime
import science_runtime
from catalog import COURSES, SECTIONS, EXERCISES, SUBJECTS, data_label

ROOT=Path(__file__).resolve().parent
DOWNLOADS=ROOT.parent/"cookbook/downloads"
QA=ROOT/"qa"
DOWNLOADS.mkdir(parents=True,exist_ok=True);QA.mkdir(exist_ok=True)

def markdown(text):
    return nbformat.v4.new_markdown_cell(text)

def code(text, **metadata):
    return nbformat.v4.new_code_cell(text.strip()+"\n",metadata=metadata)

def introduction(course,locale):
    """Gallery-style HTML cell, using VibeIt's standard raw text/html format."""
    zh=locale=="zh-hans"
    icons={"01":"🧬","02":"🔎","03":"📊","04":"🧭","05":"🕸️","06":"🧪"}
    title=html.escape(course["title"][locale])
    summary=html.escape(course["summary"][locale])
    subject=SUBJECTS[course.get('discipline','bioinformatics')]
    number=f'{course.get("number",int(course["id"][:2]) if course["id"][:2].isdigit() else 1):02}'
    badges=[(subject['zh']+" · 第 "+number+" 课" if zh else subject['en']+" · Lesson "+number),
            ("🔋 离线核心分析" if zh else "🔋 Offline core analysis"),
            (f'⏱ {course["minutes"]} 分钟' if zh else f'⏱ {course["minutes"]} min'),
            (data_label(course,locale) if course.get('data_kind') else ("内嵌真实数据" if zh else "Embedded real data")),
            "📦 "+" · ".join(course["packages"])]
    pills="".join('<span style="display:inline-block;max-width:100%;box-sizing:border-box;margin:4px 6px 0 0;padding:4px 10px;border-radius:999px;background:rgba(255,255,255,.18);color:#fff;font-size:13px;font-weight:600;overflow-wrap:anywhere">'+html.escape(label)+'</span>' for label in badges)
    markup=f'''<section class="lesson-intro" lang="{"zh-CN" if zh else "en"}" aria-label="{title}" style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;box-sizing:border-box;max-width:100%;background:linear-gradient(135deg,#00b894 0%,#0984e3 100%);border-radius:22px;padding:26px 28px;color:#fff;line-height:1.6;box-shadow:0 12px 30px rgba(0,0,0,.18);overflow-wrap:anywhere">
  <div aria-hidden="true" style="font-size:52px;line-height:1">{course.get('icon') or icons.get(course["id"][:2],subject['icon'])}</div>
  <h1 style="font-size:26px;font-weight:800;line-height:1.3;letter-spacing:normal;margin:8px 0 0;color:#fff">{title}</h1>
  <p style="font-size:16px;line-height:1.6;opacity:.95;margin:6px 0 0;max-width:640px;color:#fff">{summary}</p>
  <div style="margin-top:12px">{pills}</div>
</section>
'''
    return nbformat.v4.new_raw_cell(markup,metadata={"raw_mimetype":"text/html","tags":["lesson-intro"]})

def refresh_introduction(path,course,locale):
    """Change presentation only, retaining all executed cells and embedded data."""
    nb=nbformat.read(path,as_version=4)
    before=copy.deepcopy(nb.cells[1:])
    intro=introduction(course,locale);intro.id=nb.cells[0].id
    nb.cells[0]=intro
    assert nb.cells[1:]==before
    nbformat.validate(nb);nbformat.write(nb,path)

def refresh_prose(path,course,locale):
    """Synchronize explanatory cells/provenance only when executed code and data match."""
    nb=nbformat.read(path,as_version=4);fresh=make_notebook(course,locale)
    assert len(nb.cells)==len(fresh.cells), 'Cell structure changed; rerun this lesson'
    assert nb.metadata.vibeit_cookbook.snapshots==fresh.metadata.vibeit_cookbook.snapshots
    for old,new in zip(nb.cells,fresh.cells):
        assert old.cell_type==new.cell_type
        if old.cell_type=='code':assert old.source==new.source, 'Calculation changed; rerun this lesson'
        else:old.source=new.source;old.metadata=new.metadata
    nb.metadata.vibeit_cookbook.sources=fresh.metadata.vibeit_cookbook.sources
    nbformat.validate(nb);nbformat.write(nb,path)

def source_context(keys):
    sources=json.loads((ROOT/"data/sources.json").read_text())
    needles={"sequences":["RefSeq"],"airway":["airway"],"reactome":["Reactome"],
             "network":["STRING"],"structure":["PDB","RCSB"]}
    return [s for s in sources if set(s.get('snapshots',[]))&set(keys) or
        any(n in s["name"] for key in keys for n in needles.get(key,[]))]

def make_notebook(course,locale):
    zh=locale=="zh-hans"
    blobs={}
    for key in course["snapshots"]:
        compressed=(ROOT/"data"/(key+".json.gz")).read_bytes()
        blobs[key]=dict(sha256=hashlib.sha256(gzip.decompress(compressed)).hexdigest(),
                        gzip_base64=base64.b64encode(compressed).decode())
    cells=[introduction(course,locale)]
    cells.append(markdown(("## 目标与运行方法\n\n下载完整 `.ipynb`，在 VibeIt Studio 文件浏览器中使用 **+ → Import from Files** 导入并打开。按从上到下的顺序运行代码单元；阅读模式中的图表是已保存的真实运行输出。重新运行会从内嵌数据计算结果。\n\n本课适合具备 Python 基础的本科生。先阅读每一步的方法与图注，再修改参数。AI 练习为可选部分，不需要 AI 账号即可完成核心课程。数据写在 notebook metadata 中，不需要另下载数据文件。请保持 notebook 已保存到当前工作文件夹。\n\n学习任务是理解本课的研究问题、执行透明的计算、校验结果，并说明结论的边界。"
        if zh else "## Goal and how to run\n\nDownload the complete `.ipynb`. In VibeIt Studio's file browser use **+ → Import from Files**, then open it. Run code cells from top to bottom. Saved charts show actual executed results; rerunning recomputes them from embedded data.\n\nThis lesson assumes basic Python knowledge. Read each method and caption before changing parameters. AI exercises are optional; no AI account is needed for the core workflow. Data lives in notebook metadata, so there is no companion data download. Keep the notebook saved in the active working folder.\n\nYour goal is to understand the biological question, execute transparent calculations, check the results, and state the limits of the conclusion.")))
    if course.get("discipline")!="bioinformatics":
        cells[-1].source=cells[-1].source.replace("the biological question","the research question")
    cells.append(markdown("## 环境与参数" if zh else "## Setup and parameters"))
    extra=course.get('setup_imports','')
    if "overrepresentation" in course["functions"]:extra+="from scipy.stats import hypergeom\n"
    if "networkx" in course["packages"]:extra+="import networkx as nx\n"
    if course.get('discipline')!='bioinformatics' or course.get('scroll_tables'):
        extra+='''from IPython.display import display as _display
def display(value):
    if isinstance(value,pd.DataFrame):
        table=value.to_html(max_rows=12,escape=True)
        style="<style>.vibeit-readable-table{max-width:100%;overflow-x:auto}.vibeit-readable-table table{width:max-content;max-width:none;border-collapse:collapse}.vibeit-readable-table td,.vibeit-readable-table th{white-space:nowrap!important;word-break:normal!important;overflow-wrap:normal!important}</style>"
        return _display(HTML(style+'<div class="vibeit-readable-table">'+table+'</div>'))
    return _display(value)
'''
    cells.append(code('''from pathlib import Path
import base64, gzip, hashlib, json, platform
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, HTML
'''+extra+f'''RECIPE_ID={course["id"]!r}
OUTPUT_DIR=Path.cwd()/"results"/RECIPE_ID
plt.rcParams.update({{"figure.dpi":120,"font.size":10,"axes.spines.top":False,"axes.spines.right":False,
                      "axes.prop_cycle":plt.cycler(color=["#18785f","#416aa6","#bc6541","#9974a5"])}})
print("Python:",platform.python_version(),"; NumPy:",np.__version__,"; Pandas:",pd.__version__)
print("Working folder:",Path.cwd())
print("Core data mode: embedded snapshot; no network requests")'''))
    cells.append(markdown(("### 读取内嵌快照\n\n下面的加载函数按课程 ID 与 SHA-256 在当前文件夹定位本 notebook，解压后再次校验。文件改名不影响匹配。若找不到数据，确认当前工作目录与文件位置；不要用编造的数据替换它。metadata 随 `.ipynb` 保存及导出，复制代码到单独 `.py` 不会自动复制数据。"
        if zh else "### Load the embedded snapshot\n\nThe loader locates this notebook in the working folder by recipe ID and SHA-256, then decompresses and verifies the data. Renaming the file does not change its identity. If loading fails, check the working folder and saved file. Metadata travels with `.ipynb` save/export; copying code to a standalone `.py` does not copy the dataset.")))
    hashes={key:blob["sha256"] for key,blob in blobs.items()}
    cells.append(code(inspect.getsource(runtime.load_snapshot)+f'\nSNAPSHOT_HASHES={hashes!r}\n'+
        '''def snapshot(key):
    return load_snapshot(RECIPE_ID,SNAPSHOT_HASHES[key],key)
print("Embedded snapshots:",list(SNAPSHOT_HASHES))'''))
    cells.append(markdown(("### 方法函数\n\n本课所需函数的完整代码就在下面。它们只使用已列出的预装包与标准库，运行时不会导入任何 cookbook 辅助模块。先检查输入约束和返回值；如果修改算法，后面的校验也需要继续通过。"
        if zh else "### Read the method functions\n\nThe full implementations appear below. They use the listed bundled packages and standard library; no cookbook helper module is imported at runtime. Inspect input requirements and return values. If you change an algorithm, its checks must still pass.")))
    for function in course["functions"]:
        module=runtime if hasattr(runtime,function) else science_runtime
        cells.append(code(inspect.getsource(getattr(module,function))+f'\nprint("Method ready: {function}")'))
    if course.get('data_note'):
        cells.append(markdown(("### 数据与模型边界\n\n" if zh else "### Data and model boundary\n\n")+course['data_note'][locale]))
    cells.append(markdown("## 分步分析" if zh else "## Steps"))
    for number,section in enumerate(SECTIONS[course["id"]],1):
        cells.append(markdown(f'### {number}. {section["title"][locale]}\n\n'+section["text"][locale]))
        if section["code"]:
            cells.append(code(section["code"],**({"tags":["cover"]} if section.get("tag")=="cover" else {})))
    task1,task2,answer,ai1,ai2,checks=EXERCISES[course["id"]][locale]
    cells.append(markdown((f"## 自主练习与参考答案\n\n1. {task1}\n2. {task2}\n\n**参考解释。** {answer}\n\n先保留当前 notebook 副本，再修改参数。把新图与原图一起比较，并记录改变了哪些输入、哪些计算和哪些结论。"
        if zh else f"## Exercises and reference explanation\n\n1. {task1}\n2. {task2}\n\n**Reference explanation.** {answer}\n\nKeep a copy before changing parameters. Compare old and new figures and record which inputs, calculations and conclusions changed.")))
    cells.append(markdown((f"## 可选的 AI 编程练习\n\n在 VibeIt 的 Coding Agent 中打开当前 notebook，先让助手阅读相关单元。核心课程不依赖 AI 服务；服务可用性与账号设置以应用帮助中心为准。\n\n**提示词 1**\n\n> {ai1}\n\n**提示词 2**\n\n> {ai2}\n\n**人工验收。** {checks}\n\n检查修改后的源代码，再手动运行受影响单元及后续校验。要求助手解释修改的目的、使用的包和数据来源，并用实际输出核对解释。"
        if zh else f"## Optional AI coding exercises\n\nOpen the current notebook in VibeIt's Coding Agent and ask it to read the relevant cells. The core lesson does not depend on AI access; see the Help Center for provider and account setup.\n\n**Prompt 1**\n\n> {ai1}\n\n**Prompt 2**\n\n> {ai2}\n\n**Human acceptance.** {checks}\n\nReview the edited source, then manually run affected cells and subsequent checks. Ask the assistant to explain the purpose, packages and data provenance of its changes, and reconcile that explanation with actual output.")))
    cells.append(markdown(("## 可选联网扩展\n\n默认关闭下面的联网操作。它只显示数据库版本及快照来源，不会替换核心数据。若要重新获取数据，应另存一个实验版本并记录新的 URL、数据库版本、获取日期与 SHA-256；新版结果需要重新执行和核验。"
        if zh else "## Optional online extension\n\nThe network action below is disabled by default. It reports a database version/source without replacing the core data. To refresh data, save a separate experimental version and record the new URL, database release, retrieval date and SHA-256. New results require rerunning and validation.")))
    urls={"sequences":"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NM_000518.5&rettype=fasta&retmode=text",
          "airway":"https://raw.githubusercontent.com/bioconductor-source/airway/596678815f4ade04a9711997150949b9782aeddc/DESCRIPTION",
          "reactome":"https://reactome.org/ContentService/data/database/version",
          "network":"https://string-db.org/api/json/version","structure":"https://data.rcsb.org/rest/v1/core/entry/1A3N"}
    key=course["snapshots"][-1] if course["id"]!="06-hemoglobin-structure" else "structure"
    online_url=course.get('online_url') or urls.get(key) or source_context([key])[0]['url']
    cells.append(code(f'''RUN_ONLINE_UPDATE=False
if RUN_ONLINE_UPDATE:
    import requests
    try:
        response=requests.get({online_url!r},timeout=20)
        response.raise_for_status()
        print("Source:",response.url)
        print(response.text[:700])
    except requests.RequestException as error:
        print("Online extension unavailable:",type(error).__name__,str(error)[:160])
else:
    print("Online extension skipped; embedded core data unchanged")''',tags=["optional-online"]))
    sources=source_context(course["snapshots"])
    lines=[("## 来源、快照与下一步" if zh else "## Sources, snapshots and next steps")]
    for s in sources:
        lines.append(f'- [{s["name"]}]({s["url"]}) — {s["license"]}; retrieved {s["retrieved_at"][:10]}. SHA-256 `{s["sha256"]}`.\n  '+s.get("conversion","Original response preserved in the embedded snapshot.")+("\n  "+s['citation'] if s.get('citation') else ''))
    lines.append("\n"+("**下一步。** 在保留本课的数据检查、参数记录和结果校验之后，将相同方法用于自己的公开或已获授权数据。记录研究设计与方法限制，不把示例结果当成新实验的验证。完整数据许可与生成说明见 cookbook 网页。"
        if zh else "**Next steps.** Transfer these methods to your own public or authorized data while retaining input checks, recorded parameters and result validation. Document the new experimental design and method limits; this example does not validate a new experiment. Full data licenses and generation instructions accompany the cookbook."))
    cells.append(markdown("\n\n".join(lines)))
    nb=nbformat.v4.new_notebook(cells=cells,metadata=dict(
        kernelspec=dict(name="python3",display_name="Python 3",language="python"),
        language_info=dict(name="python",version="3.13",file_extension=".py",mimetype="text/x-python"),
        vibeit_cookbook=dict(recipe_id=course["id"],locale=locale,version=1,snapshots=blobs,sources=sources,
            packages=course["packages"],offline_core=True)))
    for i,cell in enumerate(nb.cells):
        cell.id=hashlib.sha256(f'{course["id"]}:{locale}:{i}'.encode()).hexdigest()[:12]
    nbformat.validate(nb)
    return nb

def execute(path):
    nb=nbformat.read(path,as_version=4)
    guard=code('''import socket
def _deny_network(*args,**kwargs):
    raise RuntimeError("Network disabled during cookbook core validation")
socket.socket.connect=_deny_network
socket.create_connection=_deny_network''')
    guard.id="offline-guard";nb.cells.insert(0,guard)
    km=KernelManager(kernel_name="python3")
    km.kernel_spec.argv=[sys.executable,"-m","ipykernel_launcher","-f","{connection_file}"]
    started=time.monotonic()
    try:
        NotebookClient(nb,km=km,timeout=300,resources={"metadata":{"path":str(path.parent)}}).execute()
    finally:
        if km.has_kernel:
            km.shutdown_kernel(now=True)
    nb.cells.pop(0)
    for cell in nb.cells:
        if cell.cell_type=="code" and cell.execution_count is not None:
            cell.execution_count-=1
            for output in cell.outputs:
                if output.get("execution_count") is not None:
                    output.execution_count-=1
    nb.metadata.vibeit_cookbook["execution"]={"status":"passed","offline_guard":True,
        "python":sys.version.split()[0],"seconds":round(time.monotonic()-started,2)}
    nbformat.validate(nb);nbformat.write(nb,path)
    figures=sum("image/png" in o.get("data",{}) for c in nb.cells for o in c.get("outputs",[]))
    assert figures>=3,f"Missing figures: {path.name}"
    return dict(filename=path.name,cells=len(nb.cells),figures=figures,seconds=nb.metadata.vibeit_cookbook.execution.seconds,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),status="passed",offline=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    modes=parser.add_mutually_exclusive_group()
    modes.add_argument("--generate-only",action="store_true")
    modes.add_argument("--refresh-intro",action="store_true",help="Update HTML introduction cards while preserving executed cells and data")
    modes.add_argument("--refresh-prose",action="store_true",help="Sync explanatory cells and source references only if executed code/data are unchanged")
    parser.add_argument("--only",help="Recipe ID; useful for one changed lesson")
    parser.add_argument("--subject",help="Build one discipline without rebuilding the published bioinformatics lessons")
    args=parser.parse_args();report=[]
    for course in COURSES:
        if args.only and course["id"]!=args.only:continue
        if args.subject and course.get('discipline')!=args.subject:continue
        for locale in ("en","zh-hans"):
            path=DOWNLOADS/f'{course["id"]}.{locale}.ipynb'
            if args.refresh_intro:
                refresh_introduction(path,course,locale)
                print("Updated introduction",path.name,flush=True)
                continue
            if args.refresh_prose:
                refresh_prose(path,course,locale)
                print("Updated prose",path.name,flush=True)
                continue
            nbformat.write(make_notebook(course,locale),path)
            print("Generated",path.name,flush=True)
            if not args.generate_only:
                result=execute(path);report.append(result);print(result,flush=True)
    if not args.generate_only and not args.refresh_intro and not args.refresh_prose:
        report_path=QA/"notebook-execution.json"
        old=json.loads(report_path.read_text()) if report_path.exists() and (args.only or args.subject) else []
        filenames={r['filename'] for r in report}
        old=[r for r in old if r['filename'] not in filenames]
        report_path.write_text(json.dumps(old+report,ensure_ascii=False,indent=2)+"\n")
