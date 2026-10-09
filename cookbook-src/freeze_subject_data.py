"""Freeze primary public sources for the seven-subject expansion (authoring only)."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,csv,datetime,gzip,hashlib,io,json,re,zipfile
import numpy as np
import pandas as pd
import requests

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data';RAW=DATA/'raw';MANIFESTS=DATA/'extension-sources'
RAW.mkdir(exist_ok=True);MANIFESTS.mkdir(exist_ok=True)

def save(key,payload):
    raw=json.dumps(payload,ensure_ascii=False,separators=(',',':'),sort_keys=True,allow_nan=False).encode()
    path=DATA/(key+'.json.gz');path.write_bytes(gzip.compress(raw,mtime=0))
    print(key,len(raw),'JSON bytes; sha256',hashlib.sha256(raw).hexdigest(),flush=True)

class SourceGroup:
    def __init__(self,name,refresh=False):
        self.name=name;self.refresh=refresh;self.records=[]
        path=MANIFESTS/(name+'.json')
        self.previous={r['name']:r for r in json.loads(path.read_text())} if path.exists() else {}
    def get(self,name,url,snapshots,license,conversion,**details):
        previous=self.previous.get(name)
        if previous and not self.refresh:
            raw=gzip.decompress((ROOT/previous['raw_file']).read_bytes())
            assert hashlib.sha256(raw).hexdigest()==previous['sha256']
            self.records.append(previous);return raw
        response=requests.get(url,timeout=(20,120),headers={'User-Agent':'VibeIt-Cookbook-Educational-Snapshot'})
        response.raise_for_status();raw=response.content
        filename='extension-'+self.name+'-'+re.sub('[^a-z0-9]+','-',name.lower()).strip('-')+'.gz'
        path=RAW/filename;path.write_bytes(gzip.compress(raw,mtime=0))
        self.records.append(dict(name=name,url=response.url,sha256=hashlib.sha256(raw).hexdigest(),
            retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),license=license,
            snapshots=snapshots,conversion=conversion,raw_file='data/raw/'+filename,bytes=len(raw),**details))
        return raw
    def finish(self):
        (MANIFESTS/(self.name+'.json')).write_text(json.dumps(self.records,ensure_ascii=False,indent=2)+'\n')

def zip_member(raw,suffix):
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        matches=[n for n in archive.namelist() if n.endswith(suffix)]
        if len(matches)!=1:raise ValueError('Expected one archive member: '+suffix)
        return archive.read(matches[0])

def freeze_uci(group):
    definitions=[('iris',53,'iris.zip','iris.data'),('wine',109,'wine.zip','wine.data'),
                 ('bike',275,'bike+sharing+dataset.zip','day.csv'),
                 ('energy',374,'appliances+energy+prediction.zip','energydata_complete.csv')]
    citations={53:"Fisher, R. (1936). Iris. UCI Machine Learning Repository. DOI: 10.24432/C56C76.",109:"Aeberhard, S. & Forina, M. (1992). Wine. UCI Machine Learning Repository. DOI: 10.24432/C5PC7J.",275:"Fanaee-T, H. (2013). Bike Sharing. UCI Machine Learning Repository. DOI: 10.24432/C5W894.",374:"Candanedo, L. (2017). Appliances Energy Prediction. UCI Machine Learning Repository. DOI: 10.24432/C5VC8G."}
    for key,identifier,filename,member in definitions:
        url=f'https://archive.ics.uci.edu/static/public/{identifier}/{filename}'
        raw=group.get('UCI '+key,url,[key],'CC BY 4.0; credit UCI and original dataset authors',
            'Extract '+member+' from original download; preserve all rows and declared units; no imputation.',
            documentation=f'https://archive.ics.uci.edu/dataset/{identifier}',version='UCI frozen download',citation=citations[identifier])
        text=zip_member(raw,member).decode('utf-8-sig')
        if key=='iris':
            records=[line.split(',') for line in text.splitlines() if line.strip()]
            assert len(records)==150
            columns=['sepal_length_cm','sepal_width_cm','petal_length_cm','petal_width_cm','species']
            rows=[[float(v) for v in row[:4]]+[row[4]] for row in records]
            save(key,dict(columns=columns,rows=rows,variant='Original UCI iris.data; no silent correction of the two documented transcription discrepancies',units={c:'cm' for c in columns[:4]}))
        elif key=='wine':
            records=[line.split(',') for line in text.splitlines() if line.strip()];assert len(records)==178
            columns=['cultivar','alcohol','malic_acid','ash','alkalinity_of_ash','magnesium','total_phenols','flavanoids','nonflavanoid_phenols','proanthocyanins','color_intensity','hue','od280_od315','proline']
            save(key,dict(columns=columns,rows=[[int(r[0])]+[float(v) for v in r[1:]] for r in records],units='Source does not specify consistent units for every feature; standardized values are dimensionless'))
        else:
            frame=pd.read_csv(io.StringIO(text));assert len(frame)==(731 if key=='bike' else 19735)
            assert not frame.isna().any().any()
            save(key,dict(columns=list(frame.columns),rows=frame.to_numpy().tolist(),
                units={'cnt':'rentals per day','temp':'source-normalized temperature; conversion to Celsius not assumed for daily rows'} if key=='bike' else {'Appliances':'Wh per 10 minute interval','lights':'Wh per 10 minute interval','T1':'deg C','RH_1':'percent'},
                sampling_interval_seconds=86400 if key=='bike' else 600))

def freeze_ecb(group):
    url='https://data-api.ecb.europa.eu/service/data/EXR/D.USD+GBP+JPY+CNY.EUR.SP00.A?startPeriod=2019-01-01&endPeriod=2024-12-31&format=csvdata'
    raw=group.get('ECB SDMX euro reference exchange rates',url,['ecb'],
        'ECB copyright / free reuse with accurate source attribution; data obtained free from ECB; derived returns explicitly labelled',
        'Retain 2019-01-01 through 2024-12-31 and USD, GBP, JPY, CNY; preserve missing values and quotation direction.',
        documentation='https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html',
        terms='https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html')
    observations=pd.read_csv(io.BytesIO(raw))
    assert observations.FREQ.eq('D').all() and observations.CURRENCY_DENOM.eq('EUR').all()
    assert observations.TIME_PERIOD.between('2019-01-01','2024-12-31').all()
    assert not observations.duplicated(['TIME_PERIOD','CURRENCY']).any()
    assert observations.OBS_VALUE.dropna().gt(0).all()
    frame=observations.pivot(index='TIME_PERIOD',columns='CURRENCY',values='OBS_VALUE').sort_index().rename_axis('Date').reset_index()
    frame=frame[['Date','USD','GBP','JPY','CNY']]
    rows=json.loads(frame.to_json(orient='records',double_precision=15))
    assert len(rows)>1400 and frame.Date.is_unique
    save('ecb',dict(rows=rows,quote='Foreign currency units per 1 EUR',period=['2019-01-01','2024-12-31'],currency_order=['USD','GBP','JPY','CNY'],source_notice='Source: European Central Bank. The original reference rates are available free from the ECB. Course returns, inversions and risk estimates are derived calculations, not ECB statistics.'))

def freeze_worldbank(group):
    root='https://api.worldbank.org/v2'
    raw=group.get('World Bank economy metadata',root+'/country?format=json&per_page=400',['worldbank'],
        'World Bank CC BY 4.0 with additional terms; retain original indicator attribution',
        'Preserve economy IDs, region and income-group metadata; exclude aggregates in student analyses.',terms='https://data.worldbank.org/summary-terms-of-use')
    metadata=json.loads(raw)[1]
    economies=[dict(iso3=r['id'],iso2=r['iso2Code'],name=r['name'],region=r['region']['value'],income_group=r['incomeLevel']['value']) for r in metadata if r['region']['id']!='NA']
    indicators=['NY.GDP.PCAP.KD','NY.GDP.MKTP.KD','SP.POP.TOTL','SP.DYN.LE00.IN','FP.CPI.TOTL','FP.CPI.TOTL.ZG','SI.POV.GINI']
    series=[];descriptions={}
    for indicator in indicators:
        url=root+f'/country/all/indicator/{indicator}?date=2010:2024&format=json&per_page=20000&footnote=y'
        raw=group.get('World Bank '+indicator,url,['worldbank'],'World Bank CC BY 4.0 with additional terms; original sources retained in indicator metadata',
            'Retain official observations including null values and footnotes, 2010–2024; no interpolation; no aggregate-country mixing.',indicator=indicator,terms='https://data.worldbank.org/summary-terms-of-use')
        payload=json.loads(raw);assert payload[0]['pages']==1
        for r in payload[1]:
            series.append(dict(indicator=indicator,iso3=r['countryiso3code'],year=int(r['date']),value=r['value'],footnote=r.get('footnote',''),obs_status=r.get('obs_status','')))
        doc=group.get('World Bank indicator metadata '+indicator,root+f'/indicator/{indicator}?format=json',['worldbank'],
            'World Bank CC BY 4.0 with additional terms','Preserve indicator definition, source organization and source note.',indicator=indicator)
        descriptions[indicator]=json.loads(doc)[1][0]
    save('worldbank',dict(economies=economies,indicators=descriptions,observations=series,period=[2010,2024]))

def freeze_pubchem(group):
    compounds=[(702,'ethanol'),(176,'acetic acid'),(241,'benzene'),(887,'methanol'),(180,'acetone'),(2519,'caffeine'),(2244,'aspirin'),(750,'glycine')]
    ids=','.join(str(cid) for cid,name in compounds)
    props='MolecularFormula,MolecularWeight,HBondDonorCount,HBondAcceptorCount,HeavyAtomCount,XLogP,TPSA,Charge'
    raw=group.get('PubChem calculated molecular properties',f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{ids}/property/{props}/JSON',['molecules'],
        'NCBI public data; PubChem computed properties only; credit PubChem; no third-party narrative annotations included',
        'Keep the returned calculated fields for eight declared CIDs; molecular weight converted from API numeric string.',documentation='https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest')
    rows=json.loads(raw)['PropertyTable']['Properties'];names=dict(compounds)
    for r in rows:r['name']=names[r['CID']];r['MolecularWeight']=float(r['MolecularWeight'])
    sdf={}
    for cid,name in compounds:
        raw=group.get('PubChem 2D SDF '+str(cid),f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/SDF?record_type=2d',['molecules'],
            'NCBI public data; PubChem standardized structure; credit PubChem','Preserve complete standardized SDF, including CID and explicit hydrogen/bond fields.',cid=cid)
        sdf[str(cid)]=raw.decode()
    raw=group.get('PubChem caffeine 3D conformer','https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2519/SDF?record_type=3d',['molecules'],
        'NCBI public data; PubChem computed conformer; credit PubChem','Preserve calculated coordinates and conformer identifiers; not an experimental crystal structure.',cid=2519)
    save('molecules',dict(properties=rows,sdf_2d=sdf,caffeine_3d_sdf=raw.decode(),data_kind='calculated molecular properties and conformers'))

def freeze_books(group):
    books=[]
    for identifier,title,author in [(1342,'Pride and Prejudice','Jane Austen'),(84,'Frankenstein','Mary Shelley')]:
        raw=group.get('Historical novel '+str(identifier),f'https://www.gutenberg.org/cache/epub/{identifier}/pg{identifier}.txt',['novels'],
            'Original novel public domain in USA; complete source ebook and its Project Gutenberg license retained; free distribution and acknowledgment links',
            'Preserve unmodified UTF-8 source including ebook headers and complete license; preprocessing occurs visibly in the notebook.',
            documentation=f'https://www.gutenberg.org/ebooks/{identifier}',terms='https://www.gutenberg.org/policy/license.html')
        text=raw.decode('utf-8-sig');assert 'END OF THE PROJECT GUTENBERG EBOOK' in text.upper()
        books.append(dict(id=identifier,title=title,author=author,raw_text=text))
    save('novels',dict(books=books,source_notice='These source ebooks are available free of charge. Complete unmodified source texts and their licenses are included in this snapshot. Project Gutenberg is acknowledged as the transcription source; its name is not used as a course title or endorsement.'))

def freeze_gwosc(group):
    raw=group.get('GWOSC GW150914 v3 event metadata','https://gwosc.org/eventapi/json/GWTC-1-confident/GW150914/v3/',['gw150914'],
        'CC BY 4.0; acknowledge GWOSC, LIGO, Virgo and KAGRA; GWTC-1 DOI 10.7935/82H3-HH23',
        'Preserve event GPS, release and strain download parameters; event catalog values are not recomputed detection significance.',terms='https://gwosc.org/acknowledgement/')
    event=next(iter(json.loads(raw)['events'].values()))
    strain=next(r for r in event['strain'] if r['detector']=='H1' and r['sampling_rate']==4096 and r['duration']==32 and r['format']=='txt')
    raw=group.get('GWOSC H1 32 second strain',strain['url'],['gw150914'],'CC BY 4.0; credit GWOSC and collaborations; DOI 10.7935/82H3-HH23',
        'Decompress original ASCII data and parse all 131072 strain samples; preserve GPS start and sampling rate.',version='GW150914 v3, GWOSC 4 kHz R1',request_parameters=strain)
    text=gzip.decompress(raw).decode();values=np.loadtxt(io.StringIO(text));assert values.shape==(131072,) and np.isfinite(values).all()
    save('gw150914',dict(strain=values.tolist(),gps_start=strain['GPSstart'],sample_rate=4096,duration=32,event_gps=event['GPS'],detector='H1',version='GW150914 v3 / 4KHZ_R1'))

def freeze_constants(group):
    raw=group.get('NIST CODATA physical constants','https://physics.nist.gov/cuu/Constants/Table/allascii.txt',['constants'],
        'NIST public reference data; credit NIST/CODATA','Preserve official ASCII table; extract seven explicitly named SI constants and their units.',documentation='https://physics.nist.gov/cuu/Constants/')
    text=raw.decode();wanted={'Planck constant':'h','Boltzmann constant':'k_B','speed of light in vacuum':'c','molar gas constant':'R','standard acceleration of gravity':'g_0','Newtonian constant of gravitation':'G','Avogadro constant':'N_A'}
    selected={}
    for line in text.splitlines():
        name=line[:60].strip()
        if name not in wanted:continue
        numeric=line[60:85].replace(' ','').replace('...','')
        selected[wanted[name]]=dict(value=float(numeric),name=name,unit=line[110:].strip())
    assert set(selected)==set(wanted.values())
    save('constants',dict(constants=selected,release='2022 CODATA' if '2022' in text[:1000] else text.splitlines()[0]))

def freeze_models(group):
    group.get('IAPWS saturation reference release','https://iapws.org/public/documents/6dGkr/Supp-sat.pdf',['models'],
        'IAPWS SR1-86(1992): unrestricted publication allowed in all countries (cover page)',
        'Reference equations and numerical coefficients transcribed from release pages 2–3; pedagogical model values are not new experiments.',
        documentation='https://iapws.org/technical-guidance/release/Supp-sat',version='SR1-86(1992)')
    payload=dict(kind='Authored numerical teaching models, not measured experimental data',seed=20261009,
        pendulum=dict(length_m=1.0,angles_deg=[5,30,90],duration_s=20),
        oscillator=dict(mass_kg=1.0,stiffness_N_per_m=16.0,damping_N_s_per_m=[.4,1.6,4.0],force_N=1.0),
        projectile=dict(mass_kg=.145,diameter_m=.073,drag_coefficient=.47,air_density_kg_per_m3=1.225,speed_m_per_s=30.0,angle_deg=45),
        heat=dict(length_m=1.0,diffusivity_m2_per_s=1e-4,ambient_degC=20.0,amplitude_degC=50.0),
        beam=dict(length_m=3.0,young_modulus_Pa=200e9,second_moment_m4=8.333e-6,tip_force_N=300),
        circuit=dict(resistance_ohm=1000.0,capacitance_F=100e-6,input_voltage_V=5.0,tolerance_fraction=.05),
        pid=dict(ambient_degC=20.0,setpoint_degC=60.0,time_constant_s=60.0,plant_gain_degC_per_percent=1.0,step_s=1.0,duration_s=600),
        titration=dict(acid_initial_mol_per_L=.1,acid_volume_L=.025,base_mol_per_L=.1,pKa=4.76,Kw=1e-14,temperature_degC=25),
        calibration=dict(path_length_cm=1.0,absorptivity_L_per_mol_cm=1500.0,blank_absorbance=.02,noise_sd_absorbance=.005,unknown_concentration_mol_per_L=3e-5),
        water_saturation=dict(critical_temperature_K=647.096,critical_pressure_Pa=22.064e6,coefficients=[-7.85951783,1.84408259,-11.7866497,22.6807411,-15.9618719,1.80122502],exponents=[1,1.5,3,3.5,4,7.5],reference='IAPWS SR1-86(1992); equation coefficients are reference-model parameters, not new measurements'))
    save('models',payload)
    raw=json.dumps(payload,ensure_ascii=False,sort_keys=True).encode()
    filename='extension-models-authored-parameters.gz';(RAW/filename).write_bytes(gzip.compress(raw,mtime=0))
    group.records.append(dict(name='Authored numerical teaching model parameters',url='https://github.com/zhiluo20/vibeit/blob/main/cookbook-src/freeze_subject_data.py',snapshots=['models'],license='Original teaching parameters/code MIT; reference equation coefficients attributed to IAPWS SR1-86(1992)',sha256=hashlib.sha256(raw).hexdigest(),raw_file='data/raw/'+filename,bytes=len(raw),retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),conversion='Declared parameters and seed; generated trajectories and calibration observations must be labelled simulated.',reference='https://iapws.org/technical-guidance/release/Supp-sat'))

GROUPS={'uci':freeze_uci,'ecb':freeze_ecb,'worldbank':freeze_worldbank,'pubchem':freeze_pubchem,'books':freeze_books,'gwosc':freeze_gwosc,'constants':freeze_constants,'models':freeze_models}

def merge_sources():
    path=DATA/'sources.json';existing=json.loads(path.read_text());base=[r for r in existing if not r.get('snapshots')]
    extensions=[r for p in sorted(MANIFESTS.glob('*.json')) for r in json.loads(p.read_text())]
    assert len({r['name'] for r in base+extensions})==len(base+extensions)
    path.write_text(json.dumps(base+extensions,ensure_ascii=False,indent=2)+'\n')
    path=DATA/'raw-manifest.json';original=[r for r in json.loads(path.read_text()) if not r['file'].startswith('data/raw/extension-')]
    rows=[dict(name=r['name'],file=r['raw_file'],bytes=r['bytes'],compressed_bytes=(ROOT/r['raw_file']).stat().st_size,sha256=r['sha256']) for r in extensions]
    path.write_text(json.dumps(original+rows,indent=2)+'\n')
    print('Merged',len(extensions),'extension source responses',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--group',choices=list(GROUPS));parser.add_argument('--refresh',action='store_true');parser.add_argument('--merge',action='store_true');args=parser.parse_args()
    if args.group:
        group=SourceGroup(args.group,args.refresh);GROUPS[args.group](group);group.finish()
    if args.merge:merge_sources()
    if not args.group and not args.merge:parser.error('Choose --group or --merge')
