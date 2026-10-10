"""Independent geometric references and failure cases for the two drug lessons."""
from pathlib import Path
import gzip, hashlib, json, math
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from runtime import parse_pdb
from science_runtime import residue_minimum_distances, residue_labels, pdb_atom_text

ROOT = Path(__file__).resolve().parent
KEYS = ['chain','resnum','icode','residue']


def main():
    fixture = pd.DataFrame([
        dict(chain='A',resnum=1,icode='',residue='GLY',x=0.,y=0.,z=0.),
        dict(chain='A',resnum=1,icode='A',residue='GLY',x=3.,y=4.,z=0.),
        dict(chain='B',resnum=1,icode='',residue='GLY',x=0.,y=0.,z=2.)])
    left,right,matrix = residue_minimum_distances(fixture,fixture)
    assert residue_labels(left)==['A:GLY1','A:GLY1A','B:GLY1']
    reference = np.array([[math.dist(a,b) for b in fixture[['x','y','z']].to_numpy()]
                          for a in fixture[['x','y','z']].to_numpy()])
    assert np.allclose(matrix,reference)
    for bad in [fixture.iloc[:0],fixture.assign(x=np.inf)]:
        try: residue_minimum_distances(bad,fixture)
        except ValueError: pass
        else: raise AssertionError('Invalid geometry accepted')
    results=[]
    for key in ['imatinib','trastuzumab']:
        snapshot=(ROOT/'data'/(key+'.json.gz')).read_bytes()
        data=json.loads(gzip.decompress(snapshot));atoms=parse_pdb(data['pdb'])
        heavy=atoms[(atoms.occupancy>0)&~atoms.element.isin(['H','D'])]
        if key=='imatinib':
            drug=heavy[(heavy.chain=='A')&(heavy.residue=='STI')]
            target=heavy[(heavy.chain=='A')&(heavy.record=='ATOM')]
        else:
            drug=heavy[(heavy.record=='ATOM')&heavy.chain.isin(['A','B'])]
            target=heavy[(heavy.record=='ATOM')&(heavy.chain=='C')]
        left,right,matrix=residue_minimum_distances(drug,target)
        # Independent radius-neighbor search builds residue identities from atoms.
        tree=cKDTree(target[['x','y','z']].to_numpy())
        neighbors=tree.query_ball_point(drug[['x','y','z']].to_numpy(),r=4.)
        left_keys=list(drug[KEYS].itertuples(index=False,name=None))
        right_keys=list(target[KEYS].itertuples(index=False,name=None))
        pairs={(left_keys[i],right_keys[j]) for i,indices in enumerate(neighbors) for j in indices}
        mask=matrix<=4.
        assert len(pairs)==mask.sum()
        assert len({p[0] for p in pairs})==mask.any(axis=1).sum()
        assert len({p[1] for p in pairs})==mask.any(axis=0).sum()
        # Independent point-wise norm reduction for the entire small-molecule pocket.
        if key=='imatinib':
            brute=np.array([min(float(np.linalg.norm(a-b))
                       for a in drug[['x','y','z']].to_numpy()
                       for b in group[['x','y','z']].to_numpy())
                       for _,group in target.groupby(KEYS,sort=False)])
            assert np.allclose(matrix[0],brute,atol=1e-12)
            assert len(drug)==37 and mask.sum()==21
        else:
            assert matrix.shape==(434,581)
            assert (mask.any(axis=1).sum(),mask.any(axis=0).sum(),mask.sum())==(14,17,32)
        # PDB subset roundtrip preserves IDs, insertion codes and coordinates.
        selection=pd.concat([target,drug])
        reread=parse_pdb(pdb_atom_text(selection))
        assert list(reread[KEYS+['atom']].itertuples(index=False,name=None))==list(selection[KEYS+['atom']].itertuples(index=False,name=None))
        assert np.array_equal(reread[['x','y','z']].to_numpy(),selection[['x','y','z']].to_numpy())
        # Rigid rotation and translation, transposed selections and empty contacts.
        rotation=np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]])
        transformed=[]
        for frame in [drug,target]:
            copy=frame.copy();copy[['x','y','z']]=frame[['x','y','z']].to_numpy()@rotation+np.array([20.,-5.,7.])
            transformed.append(copy)
        _,_,transformed_matrix=residue_minimum_distances(*transformed)
        _,_,reverse=residue_minimum_distances(target,drug)
        assert np.allclose(matrix,transformed_matrix,atol=1e-12)
        assert np.allclose(matrix,reverse.T,atol=1e-12)
        assert not (matrix<=.01).any()
        counts=[int((matrix<=t).sum()) for t in [3.,3.5,4.,4.5,5.,6.]]
        assert np.all(np.diff(counts)>=0)
        results.append(dict(snapshot=key,sha256=hashlib.sha256(gzip.decompress(snapshot)).hexdigest(),
            drug_heavy_atoms=len(drug),target_heavy_atoms=len(target),matrix_shape=list(matrix.shape),
            contacting_drug_residues=int(mask.any(axis=1).sum()),contacting_target_residues=int(mask.any(axis=0).sum()),
            residue_pair_edges=int(mask.sum()),cutoff_angstrom=4.,
            independent_radius_search='passed',pdb_coordinate_and_insertion_roundtrip='passed',
            rigid_rotation_translation='passed',distance_symmetry='passed',empty_contacts='passed'))
    report=dict(results=results,fixture_and_invalid_inputs='passed',real_device_tested=False,
                scope='Geometry validation; does not validate pharmacological efficacy or binding affinity')
    (ROOT/'qa/drug-method-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: independent KD-tree and direct norms; residue identity, coordinate roundtrip and geometry invariants')


if __name__=='__main__':main()
