"""Catch unrendered emphasis in tutorial prose, while preserving Python operators."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,json,subprocess
from build_site import markdown_html
from subjects._drug_plain_language import clean_explanation
from catalog import COURSES

ROOT=Path(__file__).resolve().parent

class NarrativeText(HTMLParser):
    def __init__(self):
        super().__init__();self.code_depth=0;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('pre','code','script','style'):self.code_depth+=1
    def handle_endtag(self,tag):
        if tag in ('pre','code','script','style'):self.code_depth-=1
    def handle_data(self,text):
        if not self.code_depth:self.parts.append(text)

def main(baseline_ref=None):
    examples=[('**柱形图这样看：**一条柱子','<strong>柱形图这样看</strong>：一条柱子'),
              ('**哪些部件靠得近？**量一下','<strong>哪些部件靠得近</strong>？量一下'),
              ('**黄色偏近，蓝紫色偏远。**右边是尺子','<strong>黄色偏近，蓝紫色偏远</strong>。右边是尺子')]
    for source,expected in examples:
        assert expected in markdown_html(clean_explanation(source,'zh-hans'),allow_html=True)
    adjacent='名叫 **ABL** 的蛋白有一个位置。**伊马替尼**在这里。**在哪里？**量一下。'
    rendered=markdown_html(clean_explanation(adjacent,'zh-hans'),allow_html=True)
    assert '<strong>ABL</strong>' in rendered and '<strong>伊马替尼</strong>' in rendered
    assert '<strong>在哪里</strong>？量一下' in rendered and '**' not in rendered
    columns='**一行**是一个原子，**一列**是一个部件。'
    assert clean_explanation(columns,'zh-hans')==columns
    code=markdown_html('```python\nvalue = 2 ** 3\n```',allow_html=True)
    assert '2 ** 3' in code
    narrative=NarrativeText();narrative.feed(code);assert '**' not in ''.join(narrative.parts)
    checked=0;changed=[]
    for course in COURSES:
        for locale in ('en','zh-hans'):
            path=ROOT.parent/'cookbook/downloads'/(course['id']+'.'+locale+'.ipynb')
            notebook=json.loads(path.read_text())
            for index,cell in enumerate(notebook['cells']):
                if cell['cell_type']!='markdown':continue
                reader=NarrativeText();reader.feed(markdown_html(''.join(cell['source']),notebook['metadata']['vibeit_cookbook'].get('plain_language',False)))
                assert '**' not in ''.join(reader.parts),(path.name,index)
                checked+=1
            if baseline_ref:
                previous=json.loads(subprocess.run(['git','show',baseline_ref+':'+str(path.relative_to(ROOT.parent))],cwd=ROOT.parent,capture_output=True,check=True).stdout)
                codes=lambda n:[c['source'] for c in n['cells'] if c['cell_type']=='code']
                outputs=lambda n:[c.get('outputs',[]) for c in n['cells'] if c['cell_type']=='code']
                assert codes(notebook)==codes(previous)
                assert outputs(notebook)==outputs(previous)
                assert notebook['metadata']['vibeit_cookbook']['snapshots']==previous['metadata']['vibeit_cookbook']['snapshots']
                if notebook!=previous:changed.append(path.name)
    if baseline_ref:
        assert set(changed)=={'07-imatinib-pocket.zh-hans.ipynb','08-trastuzumab-interface.zh-hans.ipynb'}
    report=dict(narrative_cells_checked=checked,unrendered_emphasis=[],changed_notebooks=changed,
        baseline_ref=baseline_ref,calculation_code='unchanged' if baseline_ref else 'not compared',
        saved_outputs='unchanged' if baseline_ref else 'not compared',scientific_snapshots='unchanged' if baseline_ref else 'not compared',
        cjk_punctuation_fixtures='passed',python_exponent_operator='preserved')
    (ROOT/'qa/markdown-rendering.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',checked,'narrative cells; Chinese emphasis renders and Python operators remain intact')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--baseline-ref');main(parser.parse_args().baseline_ref)
