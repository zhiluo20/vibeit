"""Render the site from executed notebooks; never maintain separate calculation code."""
from pathlib import Path
from urllib.parse import urlsplit
import base64, gzip, hashlib, html, json, re, shutil, zipfile
import xml.etree.ElementTree as ET
import mistune
import nbformat
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.style import Style
from pygments.token import Comment,Keyword,Name,String,Number,Operator,Generic
from courses import COURSES

ROOT=Path(__file__).resolve().parent
SITE=ROOT.parent
OUT=SITE/"cookbook"
BASE="/vibeit/cookbook/"
HOST="https://www.mecury.co.uk"
ASSETS=OUT/"assets"
ASSETS.mkdir(parents=True,exist_ok=True)
PRODUCT=(SITE/"index.html").read_text(encoding="utf-8")
md=mistune.create_markdown(plugins=["table","url"])
class VibeitCodeStyle(Style):
    background_color="#101014"
    default_style="#f4f4f6"
    styles={Comment:"#89909f",Keyword:"bold #79e6ff",Name.Builtin:"#5aa9ff",
        Name.Function:"#b6c8ff",Name.Class:"bold #b6c8ff",Name.Decorator:"#a7d0ff",
        String:"#eab885",Number:"#d8b4fb",Operator:"#bac2d0",Generic.Error:"#ff8f9a"}
CODE_FORMATTER=HtmlFormatter(nowrap=True,style=VibeitCodeStyle)
PAGES=[]
SEARCH_TAGS={
    "sequences":"FASTA DNA GC codon translation alignment affine gap Needleman Wunsch Smith Waterman RefSeq 序列 比对 翻译",
    "expression":"RNA-seq PCA count normalization donor dexamethasone CRISPLD2 Reactome ORA FDR BH hypergeometric 表达 富集 归一化",
    "networks":"PPI STRING TP53 physical interaction network evidence 蛋白互作 网络",
    "structure":"PDB 1A3N py3Dmol hemoglobin C-alpha contact distance protein structure 蛋白结构 距离 血红蛋白",
}

DISCIPLINES=[
 ("bioinformatics","Bioinformatics","生物信息学","Six complete workflows, from sequence records to expression, interactions and structure.","六个完整工作流，从序列记录到表达、互作与结构。",True),
 ("data-science","Data science & machine learning","数据科学与机器学习","From a measured dataset to an interpretable model and its evaluation.","从实测数据到可解释模型及其评估。",False),
 ("mathematics","Mathematics & statistics","数学与统计","Explore numerical methods, uncertainty and statistical reasoning.","探索数值方法、不确定性与统计推理。",False),
 ("physics","Physics","物理","Turn physical models into transparent calculations and visual experiments.","将物理模型转化为透明计算与可视化实验。",False),
 ("chemistry","Chemistry","化学","Connect molecular data with quantitative analysis and visualization.","将分子数据与定量分析及可视化联系起来。",False),
 ("engineering","Engineering","工程","Measure, simulate and inspect engineering systems with reproducible code.","使用可复现代码测量、模拟及检查工程系统。",False),
 ("economics","Economics & finance","经济与金融","Examine public economic data, assumptions and model sensitivity.","研究公开经济数据、模型假设及敏感性。",False),
 ("humanities","Humanities & social sciences","人文与社会科学","Use computational methods to investigate texts and social datasets.","使用计算方法研究文本与社会数据。",False),
]

def esc(value):return html.escape(str(value),quote=True)

def callout(title,content):
    """A static note card; content has already been rendered as Markdown."""
    icon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7v1"/></svg>'
    return f'<aside class="callout" role="note" aria-label="{esc(title)}"><div class="callout-heading">{icon}<strong>{esc(title)}</strong></div><div class="callout-content">{content}</div></aside>'

# Shared notebook sections identify reusable guidance. Scientific explanations and
# exercise prompts retain their original paragraph and quotation formatting.
GUIDANCE_TITLES={
    "## 目标与运行方法":"在 VibeIt 中运行",
    "## Goal and how to run":"Run in VibeIt",
    "### 读取内嵌快照":"内嵌数据说明",
    "### Load the embedded snapshot":"Embedded data",
    "### 方法函数":"方法代码说明",
    "### Read the method functions":"Method code",
    "## 可选的 AI 编程练习":"可选 AI 练习",
    "## Optional AI coding exercises":"Optional AI exercises",
    "## 可选联网扩展":"联网扩展说明",
    "## Optional online extension":"Online extension",
}

def markdown_html(source):
    sections=source.split("\n\n",2)
    title=GUIDANCE_TITLES.get(sections[0])
    if title and len(sections)>=2:
        # Render just the fixed introductory paragraph as a card. Keeping its
        # Markdown intact preserves inline code, emphasis and future links.
        return md(sections[0])+callout(title,md(sections[1]))+(md(sections[2]) if len(sections)==3 else "")
    return md(source)

def prefix(locale):return BASE+("zh-hans/" if locale=="zh-hans" else "")
def route(locale,tail=""):return prefix(locale)+tail

def site_header(locale,tail):
    """Reuse the product header markup and its navigation translations."""
    zh=locale=="zh-hans"
    header=re.search(r"<header>.*?</header>",PRODUCT,re.S).group(0)
    language="zh" if zh else "en"
    product_url="/vibeit/?lang="+language
    header=header.replace('<header>','<header class="site-header">')
    header=header.replace('<nav class="wrap">',f'<nav class="wrap" aria-label="{"主导航" if zh else "Main navigation"}">')
    header=header.replace('href="#top"',f'href="{product_url}"')
    header=header.replace('src="assets/','src="/vibeit/assets/')
    for anchor in ["capabilities","pricing"]:
        header=header.replace(f'href="#{anchor}"',f'href="{product_url}#{anchor}"')
    header=header.replace('href="cookbook/"',f'href="{prefix(locale)}" aria-current="page"')
    header=header.replace('href="help/"',f'href="/vibeit/help/{"zh-hans/" if zh else ""}"')
    translations=re.search(r'\b'+language+r':\{(.*?)\n      \}',PRODUCT.split('const T={',1)[1],re.S).group(1)
    labels=dict(re.findall(r'"(nav\.[^"]+)":"([^"]+)"',translations))
    def translate(match):
        return match[1]+esc(labels[match[2]])+match[3]
    header=re.sub(r'(<a[^>]*data-i18n="(nav\.[^"]+)"[^>]*>).*?(</a>)',translate,header)
    header=header.replace('>Help Center</a>',('>使用手册</a>' if zh else '>Help Center</a>'))
    header=header.replace('aria-label="Menu"',f'aria-label="{"菜单" if zh else "Menu"}"')
    header=header.replace('id="langBtn" aria-haspopup="true"',f'id="langBtn" aria-label="{"选择语言" if zh else "Choose language"}" aria-controls="langMenu" aria-haspopup="menu"')
    header=header.replace('<span id="langLabel">English</span>',f'<span id="langLabel">{"中文" if zh else "English"}</span>')
    languages=[]
    for code,label in [("en","English"),("zh-hans","中文")]:
        languages.append(f'<a href="{route(code,tail)}" lang="{code}" role="menuitem" data-code="{code}" aria-current="{str(code==locale).lower()}">{label}</a>')
    header=header.replace('<div class="lang-menu" id="langMenu" role="menu"></div>','<div class="lang-menu" id="langMenu" role="menu">'+''.join(languages)+'</div>')
    return header

def header_css():
    """Scope the actual product desktop/mobile header CSS to cookbook pages."""
    desktop=re.search(r'(header\{position:sticky;.*?)(?=\s*\.hero\{)',PRODUCT,re.S).group(1)
    mobile=re.search(r'/\* ===== Mobile: collapse the nav.*?\*/\s*@media\(max-width:820px\)\{(.*?)\n    \}',PRODUCT,re.S).group(1)
    def scope(rules):
        rules=re.sub(r'/\*.*?\*/','',rules,flags=re.S)
        def rule(match):
            selectors=[]
            for selector in match[1].strip().split(','):
                selector=selector.strip().replace('.lang-menu button','.lang-menu a')
                selectors.append('.site-header' if selector=='header' else '.site-header '+selector)
            return ','.join(selectors)+'{'+match[2].strip()+'}\n'
        return re.sub(r'([^{}]+)\{([^{}]*)\}',rule,rules)
    resets='''.site-header{background:transparent;border:0;line-height:1.5;font-size:16px}
.site-header .wrap{width:100%;max-width:var(--maxw);margin:0 auto;padding:0 24px}
.site-header .brand{font-size:16px;white-space:nowrap;color:var(--text)}
.site-header a{text-decoration:none}
.site-header .nav-links{align-items:normal;flex-wrap:nowrap}
.site-header .nav-links a[aria-current="page"]{color:var(--accent);font-weight:650}
'''
    return '/* Generated from the product page header CSS. */\n'+resets+scope(desktop)+'\n@media(max-width:820px){\n'+scope(mobile)+'}\n'

def document(title,description,body,locale,tail="",reader=False):
    zh=locale=="zh-hans";url=HOST+route(locale,tail)
    scripts='<script src="'+BASE+'assets/site.js" defer></script>'
    if reader:
        scripts+='<script src="'+BASE+'assets/3Dmol-min.js"></script><script>window.$3Dmol=window.$3Dmol||window["3Dmol"];window.$3Dmolpromise=Promise.resolve(true);</script>'
    structured=json.dumps({"@context":"https://schema.org","@type":"LearningResource" if reader else "CollectionPage",
        "name":title,"description":description,"url":url,"inLanguage":"zh-CN" if zh else "en",
        "isPartOf":{"@type":"WebSite","name":"Vibeit Studio","url":HOST+"/vibeit/"}},ensure_ascii=False).replace("</","<\\/")
    return f'''<!doctype html>
<html lang="{"zh-CN" if zh else "en"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Vibeit Studio Cookbook</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="en" href="{HOST+route('en',tail)}"><link rel="alternate" hreflang="zh-CN" href="{HOST+route('zh-hans',tail)}"><link rel="alternate" hreflang="x-default" href="{HOST+route('en',tail)}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website">
<link rel="icon" href="/vibeit/assets/pydev-icon.png"><link rel="stylesheet" href="{BASE}assets/brand.css"><link rel="stylesheet" href="{BASE}assets/site.css"><link rel="stylesheet" href="{BASE}assets/code.css"><link rel="stylesheet" href="{BASE}assets/header.css">{scripts}<script type="application/ld+json">{structured}</script></head>
<body><a class="skip" href="#main">{"跳到内容" if zh else "Skip to content"}</a>{site_header(locale,tail)}
<main id="main" class="wrap">{body}</main><footer class="site-footer"><div class="wrap footer-inner"><span>Vibeit Studio Cookbook · {"真实数据，可复现方法。" if zh else "Real data. Reproducible methods."}</span><div><a href="{route(locale,'sources/')}">{"数据与许可" if zh else "Data & licenses"}</a><a href="/vibeit/help/">{"应用帮助" if zh else "App help"}</a><a href="https://github.com/zhiluo20/vibeit/tree/main/cookbook-src">{"课程源文件" if zh else "Lesson source"}</a></div></div></footer></body></html>'''

def write_page(locale,tail,title,description,body,reader=False):
    path=OUT/("zh-hans" if locale=="zh-hans" else "")/tail/"index.html"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(document(title,description,body,locale,tail,reader),encoding="utf-8")
    PAGES.append(HOST+route(locale,tail))

def cover(course):
    notebook=nbformat.read(OUT/"downloads"/(course["id"]+".en.ipynb"),as_version=4)
    assert notebook.metadata.vibeit_cookbook.execution.status=="passed"
    for cell in notebook.cells:
        if "cover" not in cell.metadata.get("tags",[]):continue
        for output in cell.get("outputs",[]):
            if "image/png" in output.get("data",{}):
                name=course["slug"]+".png"
                (ASSETS/name).write_bytes(base64.b64decode(output.data["image/png"]))
                return BASE+"assets/"+name
    raise ValueError("Missing executed cover: "+course["id"])

def landing(locale):
    zh=locale=="zh-hans"
    title="用真实问题，学会可复现的分析。" if zh else "Real questions. Reproducible answers."
    intro="在 iPad 或 iPhone 上，从研究问题走到数据、代码和结果。每份 notebook 都包含真实数据、完整方法、图表解读和可检验的练习。" if zh else "Move from a research question to data, code and results on your iPad or iPhone. Each notebook brings real data, transparent methods, annotated figures and checkable exercises."
    hero=f'''<section class="hero"><div><div class="eyebrow">Vibeit Studio / Cookbook</div><h1>{title}</h1><p>{intro}</p><div class="actions"><a class="button" href="{route(locale,'bioinformatics/')}">{"开始生物信息学课程" if zh else "Explore bioinformatics"} →</a><a class="button secondary" href="{BASE}downloads/vibeit-bioinformatics-cookbook.zip" download>{"下载课程合集" if zh else "Download the collection"}</a></div><div class="facts"><span>{"6 个工作流" if zh else "6 workflows"}</span><span>{"中英双语" if zh else "English & Chinese"}</span><span>{"核心分析可离线运行" if zh else "Offline core analysis"}</span></div></div><figure><img src="{BASE}assets/rnaseq-expression.png" alt="{"真实 airway 数据的配对样本 PCA" if zh else "PCA of real paired airway samples"}"><figcaption>{"来自第 03 课的实际计算：4 个供体，8 个 RNA-seq 样本。" if zh else "Computed in lesson 03: four donors, eight RNA-seq samples."}</figcaption></figure></section>'''
    cards=[]
    for i,(slug,en,zht,desc,zhdesc,available) in enumerate(DISCIPLINES,1):
        cards.append(f'<article class="discipline-card"><span class="status {"" if available else "pending"}">{("6 个教程 · 已提供" if zh else "6 recipes · Available") if available else ("即将推出" if zh else "Coming soon")}</span><div class="discipline-number">{i:02}</div><h3>{zht if zh else en}</h3><p>{zhdesc if zh else desc}</p><a href="{route(locale,slug+"/")}">{("浏览教程" if zh else "Browse recipes") if available else ("查看学科方向" if zh else "Explore the subject")} →</a></article>')
    body=hero+f'<section aria-labelledby="disciplines"><div class="section-heading"><div><h2 id="disciplines">{"按学科探索" if zh else "Explore by discipline"}</h2><p>{"生物信息学现已提供；其他学科将逐步加入。" if zh else "Start with bioinformatics. More disciplines will follow."}</p></div></div><div class="grid">'+"".join(cards)+'</div></section>'
    write_page(locale,"",title,intro,body)

def recipes(locale):
    zh=locale=="zh-hans";cards=[]
    for c in COURSES:
        title,summary=c["title"][locale],c["summary"][locale]
        download=BASE+"downloads/"+c["id"]+"."+locale+".ipynb"
        keywords=" ".join([title,summary,c["slug"],*c["packages"],c["title"]["en"],c["title"]["zh-hans"],SEARCH_TAGS[c["category"]]])
        difficulty=(["入门","中级","进阶"] if zh else ["Introductory","Intermediate","Advanced"])[c["difficulty"]-1]
        cards.append(f'''<article class="recipe-card" data-recipe="{c['id']}" data-category="{c['category']}" data-search="{esc(keywords)}"><img class="recipe-image" src="{c['cover']}" alt="{esc(title)} — {"实际运行图表" if zh else "executed figure"}" loading="lazy"><div class="recipe-body"><div class="recipe-meta"><span>{c['id'][:2]} / {difficulty}</span><span>{c['minutes']} {"分钟" if zh else "min"}</span><span>{"离线核心" if zh else "Offline core"}</span></div><h2>{esc(title)}</h2><p>{esc(summary)}</p><div class="packages">{' · '.join(c['packages'])}</div><div class="actions"><a class="button" href="{route(locale,'bioinformatics/'+c['slug']+'/')}">{"阅读教程" if zh else "Read tutorial"}</a><a class="button secondary" href="{download}" download>{"下载 notebook" if zh else "Download notebook"}</a></div></div></article>''')
    categories=[("all","所有主题" if zh else "All topics"),("sequences","基因与序列" if zh else "Genes & sequences"),("expression","表达与富集" if zh else "Expression & enrichment"),("networks","蛋白互作" if zh else "Protein interactions"),("structure","蛋白结构" if zh else "Protein structure")]
    title="生物信息学" if zh else "Bioinformatics"
    intro="六个独立可运行的课程，把真实数据、方法与生物学解释连接起来。只需下载一个 notebook，即可开始每个工作流。" if zh else "Six independent, runnable lessons connecting real data, methods and biological interpretation. One notebook download starts each workflow."
    body=f'''<section class="page-intro"><div class="breadcrumbs"><a href="{prefix(locale)}">Cookbook</a> / {title}</div><div class="eyebrow">BIOINFORMATICS / 01–06</div><h1>{title}</h1><p>{intro}</p></section><div class="learning-path"><div><strong>{"序列路径" if zh else "Sequence path"}</strong> 01 → 02 → 06</div><div><strong>{"表达路径" if zh else "Expression path"}</strong> 03 → 04 → 05</div><a href="{BASE}downloads/vibeit-bioinformatics-cookbook.zip" download>{"下载 12 份 notebook 合集" if zh else "Download all 12 notebooks"}</a></div><div class="filter-bar"><div class="search-field"><label for="recipe-search">{"搜索教程或包" if zh else "Search recipes or packages"}</label><input id="recipe-search" type="search" placeholder="{"例如 PCA、序列、NetworkX" if zh else "Try PCA, sequence, NetworkX"}"></div><div><label for="recipe-category">{"主题" if zh else "Topic"}</label><select id="recipe-category">{''.join(f'<option value="{key}">{label}</option>' for key,label in categories)}</select></div></div><p class="results-count" id="result-count" role="status" aria-live="polite">6 recipes</p><section class="grid" aria-label="{"教程列表" if zh else "Recipes"}">{''.join(cards)}</section><p id="empty-state" class="empty-state" hidden>{"没有匹配教程，请修改搜索词或分类。" if zh else "No matching recipes. Try another query or topic."}</p>{callout("在 VibeIt 中运行" if zh else "Run in VibeIt",md("在 VibeIt 中使用 **+ → Import from Files** 导入 `.ipynb`，再按顺序运行单元。核心分析无需联网或 AI 账号。" if zh else "In VibeIt use **+ → Import from Files** to open the `.ipynb`, then run cells in order. Core analysis needs no network or AI account."))}'''
    write_page(locale,"bioinformatics/",title,intro,body)

def notebook_html(nb):
    parts=[];toc=[]
    for cell in nb.cells:
        if cell.cell_type=="markdown":
            rendered=markdown_html(cell.source)
            def heading(match):
                level,text=match.group(1),match.group(2)
                anchor="s-"+hashlib.sha256((cell.id+text).encode()).hexdigest()[:10]
                if level=="2":toc.append((anchor,re.sub("<[^>]+>","",text)))
                return f'<h{level} id="{anchor}">{text}</h{level}>'
            rendered=re.sub(r'<h([23])>(.*?)</h\1>',heading,rendered)
            parts.append(rendered)
        elif cell.cell_type=="code":
            outputs=[]
            for output in cell.outputs:
                data=output.get("data",{})
                if "image/png" in data:
                    outputs.append('<img alt="Computed figure from this code cell" loading="lazy" src="data:image/png;base64,'+data["image/png"].replace("\n","")+'">')
                elif "text/html" in data:
                    outputs.append('<div class="output-html">'+data["text/html"]+'</div>')
                elif "text/plain" in data:
                    outputs.append('<pre>'+esc(data["text/plain"])+'</pre>')
                elif output.output_type=="stream":
                    outputs.append('<pre>'+esc(output.text)+'</pre>')
                elif output.output_type=="error":raise ValueError("Notebook has an error output")
            highlighted=highlight(cell.source,PythonLexer(),CODE_FORMATTER)
            parts.append(f'<section class="code-cell"><div class="cell-prompt">In [{cell.execution_count}] · Python</div><pre class="source-code"><code>{highlighted}</code></pre><div class="output">'+"".join(outputs)+'</div></section>')
    return "\n".join(parts),toc

def reader(course,locale):
    zh=locale=="zh-hans";filename=course["id"]+"."+locale+".ipynb"
    nb=nbformat.read(OUT/"downloads"/filename,as_version=4)
    content,toc=notebook_html(nb)
    download=BASE+"downloads/"+filename
    body=f'''<div class="page-intro"><div class="breadcrumbs"><a href="{prefix(locale)}">Cookbook</a> / <a href="{route(locale,'bioinformatics/')}">{"生物信息学" if zh else "Bioinformatics"}</a> / {course['id'][:2]}</div><div class="facts"><span>{course['minutes']} {"分钟" if zh else "min"}</span><span>{"真实数据快照" if zh else "Real data snapshot"}</span><span>{"已执行的网页阅读版" if zh else "Executed reading edition"}</span></div><div class="actions"><a class="button" href="{download}" download>{"下载并在 VibeIt 中运行" if zh else "Download and run in VibeIt"}</a><a class="button secondary" href="{route(locale,'bioinformatics/')}">{"所有教程" if zh else "All recipes"}</a></div></div><div class="article-layout"><article class="notebook">{content}</article><aside class="reader-toc" aria-label="{"本页目录" if zh else "On this page"}"><strong>{"本页目录" if zh else "On this page"}</strong>{''.join(f'<a href="#{anchor}">{esc(label)}</a>' for anchor,label in toc)}<a class="button" href="{download}" download>.ipynb ↓</a></aside></div>'''
    write_page(locale,"bioinformatics/"+course["slug"]+"/",course["title"][locale],course["summary"][locale],body,reader=course["slug"]=="protein-structure")

def placeholder(discipline,locale):
    slug,en,zht,desc,zhdesc,available=discipline;zh=locale=="zh-hans"
    title=zht if zh else en;intro=zhdesc if zh else desc
    body=f'''<section class="page-intro"><div class="breadcrumbs"><a href="{prefix(locale)}">Cookbook</a> / {title}</div><span class="status pending">{"即将推出" if zh else "Coming soon"}</span><h1>{title}</h1><p>{intro}</p></section><div class="placeholder-plan"><p>{"本学科的 notebook 尚未提供。后续课程将遵循相同标准：可追溯的真实数据、应用支持的包、完整分析、实际图表与结果校验。" if zh else "Notebooks for this discipline are not available yet. Future lessons will follow the same standard: traceable real data, app-supported packages, complete methods, executed figures and result checks."}</p><a class="button" href="{route(locale,'bioinformatics/')}">{"先探索生物信息学" if zh else "Start with bioinformatics"} →</a></div>'''
    write_page(locale,slug+"/",title,intro,body)

def sources_page(locale):
    zh=locale=="zh-hans";sources=json.loads((ROOT/"data/sources.json").read_text())
    rows="".join(f'<tr><td><a href="{esc(s["url"])}">{esc(s["name"])}</a></td><td>{esc(s["license"])}</td><td>{esc(s["retrieved_at"][:10])}</td></tr>' for s in sources)
    title="数据、许可与复现" if zh else "Data, licenses and reproducibility"
    body=f'''<section class="page-intro"><div class="breadcrumbs"><a href="{prefix(locale)}">Cookbook</a> / {title}</div><h1>{title}</h1><p>{"每课内嵌冻结的数据快照，来源信息和原始响应哈希保留在 notebook 中。" if zh else "Every lesson embeds a frozen data snapshot. Provenance and original-response hashes are retained in notebook metadata."}</p></section><div class="table-wrap"><table class="license-table"><thead><tr><th>{"来源" if zh else "Source"}</th><th>{"上游许可" if zh else "Upstream license"}</th><th>{"获取日期" if zh else "Retrieved"}</th></tr></thead><tbody>{rows}</tbody></table></div><div class="note">{"数据的第三方许可独立于本课程的代码与讲解。airway 保留上游 LGPL 声明及原始源文件链接；Reactome 与 PDB 数据按 CC0 提供；STRING 数据注明来源及 CC BY 4.0。" if zh else "Third-party data licenses are separate from lesson code and prose. airway retains its upstream LGPL declaration and original source links; Reactome and PDB data are CC0; STRING data carries attribution and CC BY 4.0."}</div><p>{"完整来源清单、数据转换代码和验证报告随课程源文件提供。" if zh else "The complete source manifest, conversion code and validation reports accompany the lesson source."} <a href="https://github.com/zhiluo20/vibeit/tree/main/cookbook-src">cookbook-src</a></p>'''
    write_page(locale,"sources/",title,title,body)

def update_sitemap():
    namespace="http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("",namespace)
    path=SITE/"sitemap.xml";tree=ET.parse(path);root=tree.getroot()
    for node in list(root):
        loc=node.find(f'{{{namespace}}}loc')
        if loc is not None and "/vibeit/cookbook/" in loc.text:root.remove(node)
    for url in PAGES:
        node=ET.SubElement(root,f'{{{namespace}}}url');ET.SubElement(node,f'{{{namespace}}}loc').text=url
        ET.SubElement(node,f'{{{namespace}}}changefreq').text="monthly"
    ET.indent(tree,space="  ");tree.write(path,encoding="utf-8",xml_declaration=True)

if __name__=="__main__":
    # Product page remains the single source of brand colors, including future updates.
    product=(SITE/"index.html").read_text()
    product_root=re.search(r":root\s*\{(.*?)\}",product,re.S).group(1)
    brand_names=["bg","bg-2","surface","surface-2","text","muted","faint","line","line-2", "accent","accent-2","accent-ink","glass","glass-line","glass-blur","font","maxw"]
    tokens=[]
    for name in brand_names:
        value=re.search(r"--"+re.escape(name)+r"\s*:\s*([^;]+);",product_root).group(1).strip()
        tokens.append(f"--{name}:{value};")
    (ASSETS/"brand.css").write_text("/* Generated from the Vibeit product page. */\n:root{"+"".join(tokens)+"}\n")
    (ASSETS/"code.css").write_text(CODE_FORMATTER.get_style_defs(".source-code")+"\n")
    (ASSETS/"header.css").write_text(header_css())
    for name in ["site.css","site.js"]:shutil.copyfile(ROOT/name,ASSETS/name)
    vendor=ROOT/"vendor"
    for name in ["3Dmol-min.js","3Dmol-min.js.LICENSE.txt","3Dmol-LICENSE"]:
        shutil.copyfile(vendor/name,ASSETS/name)
    for c in COURSES:c["cover"]=cover(c)
    with zipfile.ZipFile(OUT/"downloads/vibeit-bioinformatics-cookbook.zip","w",zipfile.ZIP_DEFLATED) as archive:
        for path in sorted((OUT/"downloads").glob("*.ipynb")):archive.write(path,path.name)
    manifest=[]
    for c in COURSES:
        item={k:v for k,v in c.items() if k!="functions"}
        item.update(discipline="bioinformatics",data_version="snapshot-2026-10-09",validation="executed-offline")
        item["downloads"]={locale:BASE+"downloads/"+c["id"]+"."+locale+".ipynb" for locale in ["en","zh-hans"]}
        item["previews"]={locale:route(locale,"bioinformatics/"+c["slug"]+"/") for locale in ["en","zh-hans"]}
        manifest.append(item)
    (OUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    for locale in ["en","zh-hans"]:
        landing(locale);recipes(locale);sources_page(locale)
        for c in COURSES:reader(c,locale)
        for d in DISCIPLINES[1:]:placeholder(d,locale)
    update_sitemap()
    print("Generated",len(PAGES),"pages and",len(manifest),"recipe entries")
