"""Regression checks for portable outputs and lesson-scoped model provenance.

Run after building notebooks/site. --baseline compares saved scientific outputs
against a known git revision, allowing only path/snapshot-list message changes.
"""
from pathlib import Path
import argparse, base64, copy, gzip, hashlib, json, re, subprocess, zipfile
import nbformat
from build_notebooks import make_notebook, snapshot_payload, ROOT
from catalog import COURSES

LEAK = re.compile(r'/(?:Users|home|private|tmp|workspace|mnt)/')

def normalize(outputs, recipe):
    result = copy.deepcopy(outputs)
    for out in result:
        if out.get('output_type') != 'stream':
            continue
        text = ''.join(out['text'])
        text = re.sub(r'^Working folder: .+$', 'Results folder: results/'+recipe, text, flags=re.M)
        text = re.sub(r'/(?:Users|home|private|tmp|workspace|mnt)/[^\n]*?/cookbook/downloads/results/', 'results/', text)
        if recipe in ('ma01-numerical-calculus', 'ma03-conditioning'):
            text = text.replace("Embedded snapshots: ['models']", 'Embedded snapshots: []')
        out['text'] = text
    return result

def main(baseline=None):
    count = figures = 0
    for course in COURSES:
        for locale in ('en', 'zh-hans'):
            relative = Path('cookbook/downloads')/(course['id']+'.'+locale+'.ipynb')
            path = ROOT.parent/relative
            text = path.read_text()
            assert not LEAK.search(text), path
            notebook = nbformat.reads(text, 4)
            fresh = make_notebook(course, locale)
            assert [c.source for c in notebook.cells] == [c.source for c in fresh.cells]
            meta = notebook.metadata.vibeit_cookbook
            has_water = 'water_saturation' in course.get('model_fields', [])
            iapws = any('IAPWS' in s['name'] for s in meta.sources)
            assert iapws == has_water, course['id']
            if course['id'].startswith('ma'):
                assert 'IAPWS' not in text
            for key, blob in meta.snapshots.items():
                raw = gzip.decompress(base64.b64decode(blob.gzip_base64))
                assert hashlib.sha256(raw).hexdigest() == blob.sha256
                assert raw == gzip.decompress(snapshot_payload(course, key))
                if key == 'models':
                    values = json.loads(raw)
                    original = json.loads(gzip.decompress((ROOT/'data/models.json.gz').read_bytes()))
                    assert set(values) == set(course['model_fields'])
                    assert all(values[k] == original[k] for k in values)
                    if course['id'] == 'ma04-monte-carlo':
                        assert values == {'seed': 20261009}
            outputs = [o for c in notebook.cells for o in c.get('outputs', [])]
            figures += sum('image/png' in o.get('data', {}) for o in outputs)
            if baseline:
                old = json.loads(subprocess.check_output(['git', 'show', f'{baseline}:{relative}'],cwd=ROOT.parent))
                # nbformat joins multiline source/output lists. Normalize both via
                # the parser before comparison, preserving every numeric/chart byte.
                old_nb = nbformat.reads(json.dumps(old), as_version=4)
                old_outputs = [o for c in old_nb.cells for o in c.get('outputs', [])]
                assert normalize(old_outputs, course['id']) == normalize(outputs, course['id']), path
            count += 1
    for path in (ROOT.parent/'cookbook').rglob('*.html'):
        assert not LEAK.search(path.read_text()), path
    archives = list((ROOT.parent/'cookbook').rglob('*.zip'))
    for path in archives:
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                if name.endswith('.ipynb'):
                    data = archive.read(name)
                    assert not LEAK.search(data.decode()), (path, name)
                    assert data == (ROOT.parent/'cookbook/downloads'/Path(name).name).read_bytes()
    print(f'PASS: {count} notebooks; {figures} PNG figures; {len(archives)} archives; scoped provenance and no build paths'
          + ('; scientific outputs match baseline '+baseline if baseline else ''))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline')
    main(parser.parse_args().baseline)
