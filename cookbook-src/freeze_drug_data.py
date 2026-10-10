"""Author-only freeze of experimental drug complexes; reruns use archived bytes."""
from pathlib import Path
import argparse, datetime, gzip, hashlib, json
import requests

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
RAW = DATA / 'raw'
RECORDS = DATA / 'extension-sources/drug-complexes.json'


def main(refresh=False):
    previous = {r['name']: r for r in json.loads(RECORDS.read_text())} if RECORDS.exists() else {}
    records = []

    def get(name, url, key, filename, conversion):
        if name in previous and not refresh:
            record = dict(previous[name], conversion=conversion)
            raw = gzip.decompress((ROOT / record['raw_file']).read_bytes())
            assert hashlib.sha256(raw).hexdigest() == record['sha256']
        else:
            response = requests.get(url, timeout=60, headers={'User-Agent': 'VibeIt educational cookbook'})
            response.raise_for_status()
            raw, final_url = response.content, response.url
            path = RAW / filename
            path.write_bytes(gzip.compress(raw, mtime=0))
            record = dict(name=name, url=final_url, snapshots=[key],
                          raw_file='data/raw/' + filename, bytes=len(raw),
                          sha256=hashlib.sha256(raw).hexdigest(),
                          retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                          license='CC0 1.0 (wwPDB data); credit depositors and primary publication',
                          conversion=conversion)
        records.append(record)
        return raw

    for pdb_id, key, count in [('1IEP', 'imatinib', 1), ('1N8Z', 'trastuzumab', 3)]:
        pdb = get('Drug complex ' + pdb_id + ' coordinates',
                  'https://files.rcsb.org/download/' + pdb_id + '.pdb', key,
                  'drug-' + pdb_id.lower() + '-coordinates.gz',
                  'Preserve complete original PDB; first-model, occupancy and chain selections are visible student code. No docking or coordinate registration.')
        entry = json.loads(get('Drug complex ' + pdb_id + ' entry metadata',
                          'https://data.rcsb.org/rest/v1/core/entry/' + pdb_id, key,
                          'drug-' + pdb_id.lower() + '-entry.gz',
                          'Preserve experiment, revision and primary citation metadata.'))
        entities = [json.loads(get('Drug complex ' + pdb_id + ' polymer entity ' + str(i),
                           'https://data.rcsb.org/rest/v1/core/polymer_entity/' + pdb_id + '/' + str(i), key,
                           'drug-' + pdb_id.lower() + '-entity-' + str(i) + '.gz',
                           'Preserve entity identity, source species, sequences and author chain IDs; do not infer a chain role from color.'))
                    for i in range(1, count + 1)]
        payload = dict(pdb_id=pdb_id, pdb=pdb.decode('ascii'), entry=entry, entities=entities)
        if key == 'imatinib':
            payload['compound'] = json.loads(get('Drug complex STI chemical component',
                      'https://data.rcsb.org/rest/v1/core/chemcomp/STI', key, 'drug-sti-component.gz',
                      'Preserve chemical identity, formula, descriptors and reported atom counts. Atom names and bound coordinates come from 1IEP, not ideal CCD coordinates.'))
        encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
        (DATA / (key + '.json.gz')).write_bytes(gzip.compress(encoded, mtime=0))
        print(key, len(encoded), hashlib.sha256(encoded).hexdigest())

    RECORDS.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
    sources = json.loads((DATA / 'sources.json').read_text())
    names = {r['name'] for r in records}
    sources = [r for r in sources if r['name'] not in names] + records
    (DATA / 'sources.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2) + '\n')
    manifest = json.loads((DATA / 'raw-manifest.json').read_text())
    manifest = [r for r in manifest if r['name'] not in names]
    manifest += [dict(name=r['name'], file=r['raw_file'], bytes=r['bytes'],
                      compressed_bytes=(ROOT / r['raw_file']).stat().st_size, sha256=r['sha256']) for r in records]
    (DATA / 'raw-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('Archived', len(records), 'drug-complex source responses')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh', action='store_true')
    main(parser.parse_args().refresh)
