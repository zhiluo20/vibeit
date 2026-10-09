"""Shared catalog for existing and new disciplines; only implemented lessons register."""
import importlib
import pkgutil
import subjects
from courses import COURSES as BIO_COURSES, SECTIONS as BIO_SECTIONS
from exercises import EXERCISES as BIO_EXERCISES

DISCIPLINES=[
    dict(id="bioinformatics",en="Bioinformatics",zh="生物信息学",icon="🧬",en_desc="Trace sequences, expression, pathways, interactions and structures.",zh_desc="连接序列、表达、通路、互作与结构。"),
    dict(id="data-science",en="Data science & machine learning",zh="数据科学与机器学习",icon="📊",en_desc="Audit measured data, build models and evaluate them without leakage.",zh_desc="审计实测数据，构建模型，并在避免信息泄漏的前提下评估。"),
    dict(id="mathematics",en="Mathematics & statistics",zh="数学与统计",icon="∑",en_desc="Connect numerical algorithms with uncertainty and statistical reasoning.",zh_desc="将数值算法与不确定性分析、统计推理联系起来。"),
    dict(id="physics",en="Physics",zh="物理",icon="🌌",en_desc="Explore measured signals, reference constants and transparent physical models.",zh_desc="研究实测信号、参考常数与透明的物理模型。"),
    dict(id="chemistry",en="Chemistry",zh="化学",icon="🧪",en_desc="Analyze molecules, chemical equilibria, reference correlations and calibration models.",zh_desc="分析分子、化学平衡、参考关联式与校准模型。"),
    dict(id="engineering",en="Engineering",zh="工程",icon="⚙️",en_desc="Inspect measured energy data, signal processing, circuits, structures and control.",zh_desc="研究实测能耗、信号处理、电路、结构与控制。"),
    dict(id="economics",en="Economics & finance",zh="经济与金融",icon="📈",en_desc="Audit public economic indicators and historical currency risk with explicit assumptions.",zh_desc="在明确假设的前提下审计公开经济指标与历史汇率风险。"),
    dict(id="humanities",en="Humanities & social sciences",zh="人文与社会科学",icon="📚",en_desc="Study historical texts and social indicators through reproducible computational methods.",zh_desc="用可复现的计算方法研究历史文本与社会指标。"),
]
SUBJECTS={d['id']:d for d in DISCIPLINES}
COURSES=[dict(c,discipline="bioinformatics",number=int(c['id'][:2])) for c in BIO_COURSES]
SECTIONS=dict(BIO_SECTIONS)
EXERCISES=dict(BIO_EXERCISES)
for info in sorted(pkgutil.iter_modules(subjects.__path__),key=lambda i:i.name):
    if info.name.startswith('_'):continue
    module=importlib.import_module('subjects.'+info.name)
    COURSES.extend(module.COURSES)
    SECTIONS.update(module.SECTIONS)
    EXERCISES.update(module.EXERCISES)
COURSES.sort(key=lambda c:([d['id'] for d in DISCIPLINES].index(c['discipline']),c['number']))
assert len({c['id'] for c in COURSES})==len(COURSES)

def course_path(course):
    return course['discipline']+'/'+course['slug']+'/'

def subject_courses(subject):
    return [c for c in COURSES if c['discipline']==subject]

DATA_LABELS={
    'measured':{'en':'Real data snapshot','zh-hans':'真实数据快照'},
    'reference':{'en':'Reference constants & model','zh-hans':'参考常数与模型'},
    'model':{'en':'Numerical teaching model','zh-hans':'数值教学模型'},
    'simulation':{'en':'Simulated teaching data','zh-hans':'教学模拟数据'},
    'text':{'en':'Historical text snapshot','zh-hans':'历史文本快照'},
    'computed':{'en':'Calculated database fields','zh-hans':'数据库计算值'},
}

def data_label(course,locale):
    return DATA_LABELS[course.get('data_kind','measured')][locale]
