"""Independent numerical checks and failure cases, separate from teaching datasets."""
import gzip, json, math, tempfile, unittest
from pathlib import Path
from functools import lru_cache
from unittest.mock import patch
import numpy as np
import pandas as pd
from scipy.stats import false_discovery_control, gmean
import runtime as r

DATA=Path(__file__).resolve().parent/"data"
def snapshot(key):return json.loads(gzip.decompress((DATA/(key+".json.gz")).read_bytes()))

def brute_score(a,b,match=2,mismatch=-1,opening=-3,extension=-1):
    # Enumerate all monotone alignments. Include only non-opposing adjacent gaps.
    @lru_cache(None)
    def visit(i,j,last):
        if i==len(a) and j==len(b):return 0
        choices=[]
        if i<len(a) and j<len(b):choices.append((match if a[i]==b[j] else mismatch)+visit(i+1,j+1,0))
        if i<len(a) and last!=2:choices.append((extension if last==1 else opening)+visit(i+1,j,1))
        if j<len(b) and last!=1:choices.append((extension if last==2 else opening)+visit(i,j+1,2))
        return max(choices,default=-math.inf)
    return visit(0,0,0)

def rescored(a,b):
    score,last=0,None
    for x,y in zip(a,b):
        if x=="-" or y=="-":
            state="a" if x=="-" else "b"
            score+=-1 if last==state else -3;last=state
        else:
            score+=2 if x==y else -1;last=None
    return score

class Methods(unittest.TestCase):
    def test_refseq_translation_and_coordinates(self):
        for row in snapshot("sequences")["records"]:
            cds=row["sequence"][row["cds_start"]-1:row["cds_end"]]
            self.assertEqual(len(cds),444)
            self.assertEqual(r.translate_cds(cds),row["translation"])
            self.assertEqual(len(row["translation"]),147)
        for bad in ["ACGT",">a\nAC?G",">a\n",">a\nAC\n>a\nGT"]:
            with self.assertRaises(ValueError):r.parse_fasta(bad)
        self.assertTrue(math.isnan(r.gc_fraction("NNN")))
        self.assertEqual(r.gc_fraction("GGNN"),1)
        with self.assertRaises(ValueError):r.translate_cds("ATGG")
        with self.assertRaises(ValueError):r.translate_cds("ATGTAAATG")

    def test_alignment_exhaustive_small_cases(self):
        strings=["A","C","AA","AC","CA","AAC","ACA","CCC"]
        for a in strings:
            for b in strings:
                result=r.affine_align(a,b)
                self.assertEqual(result["score"],brute_score(a,b),(a,b))
                self.assertEqual(rescored(result["a"],result["b"]),result["score"])
                self.assertEqual(result["a"].replace("-",""),a)
                self.assertEqual(result["b"].replace("-",""),b)
                local=r.affine_align(a,b,local=True)
                expected=max([0]+[brute_score(a[i:j],b[k:l]) for i in range(len(a)) for j in range(i+1,len(a)+1)
                    for k in range(len(b)) for l in range(k+1,len(b)+1)])
                self.assertEqual(local["score"],expected,(a,b))
                i,k=local["start"];j,l=local["end"]
                self.assertEqual(local["a"].replace("-",""),a[i:j])
                self.assertEqual(local["b"].replace("-",""),b[k:l])
        gap=r.affine_align("AAAACCCC","AAAA")
        self.assertEqual(gap["score"],8-6)
        for a,b in [("","A"),("A",""),("A"*2001,"A")]:
            with self.assertRaises(ValueError):r.affine_align(a,b)

    def test_normalization_and_pairs(self):
        data=snapshot("airway")
        counts=pd.DataFrame(data["counts"],index=data["genes"],columns=data["samples"])
        meta=pd.DataFrame(data["metadata"]).set_index("sample")
        r.validate_counts(counts,meta)
        filtered,factors,norm=r.normalize_counts(counts)
        positive=filtered.loc[(filtered>0).all(axis=1)]
        reference=positive.div(gmean(positive,axis=1),axis=0).median(axis=0)
        reference=reference/gmean(reference)
        np.testing.assert_allclose(factors,reference,rtol=1e-12)
        self.assertEqual(counts.sum(axis=0).tolist(),data["library_totals"])
        with self.assertRaises(ValueError):r.validate_counts(counts,meta.iloc[::-1])
        bad=counts.copy();bad.iloc[0,0]=-1
        with self.assertRaises(ValueError):r.validate_counts(bad,meta)
        bad_meta=meta.copy();bad_meta.iloc[0,bad_meta.columns.get_loc("condition")]="treated"
        with self.assertRaises(ValueError):r.validate_counts(counts,bad_meta)
        changes,response=r.paired_response(np.log2(norm+1),meta)
        self.assertEqual(changes.shape[1],4)
        self.assertTrue((response.loc[response.direction=="up","positive_pairs"]>=3).all())

    def test_ora_and_bh_independent_references(self):
        p=np.array([.01,.03,.002,1,.04,.03])
        np.testing.assert_allclose(r.bh_adjust(p),false_discovery_control(p),atol=1e-15)
        pathways=[dict(id="term",name="Test",genes=[str(i) for i in range(20)])]
        universe={str(i) for i in range(50)}
        # Add annotations covering the full measured background, but in a term excluded by size.
        pathways.append(dict(id="coverage",name="Coverage",genes=list(universe)))
        background,result=r.overrepresentation({"0","1","2","30"},set(),universe,pathways,max_size=30)
        row=result.loc[result.direction=="up"].iloc[0]
        expected=sum(math.comb(20,x)*math.comb(30,4-x)/math.comb(50,4) for x in range(3,5))
        self.assertAlmostEqual(row.pvalue,expected,places=14)
        empty=r.overrepresentation(set(),set(),universe,pathways,max_size=30)[1]
        self.assertTrue((empty.pvalue==1).all() and (empty.qvalue==1).all())
        no_terms=r.overrepresentation(set(),set(),set(),pathways)[1]
        self.assertEqual(len(no_terms),0)
        self.assertIn("qvalue",no_terms)

    def test_physical_graph_and_isolates(self):
        data=snapshot("network")
        counts=[]
        for threshold in [.4,.7,.9,.95,1]:
            graph=r.physical_graph(data,threshold)
            self.assertEqual(len(graph),12)
            self.assertFalse(list(__import__("networkx").selfloop_edges(graph)))
            counts.append(graph.number_of_edges())
        self.assertEqual(counts,sorted(counts,reverse=True))
        empty=dict(data,edges=[])
        self.assertEqual(len(list(__import__("networkx").isolates(r.physical_graph(empty)))),12)
        with self.assertRaises(ValueError):r.physical_graph(data,1.1)

    def test_pdb_and_alternate_models(self):
        atoms=r.parse_pdb(snapshot("structure")["pdb"])
        self.assertEqual(set(atoms.loc[atoms.record=="ATOM","chain"]),set("ABCD"))
        text=snapshot("structure")["pdb"]
        original=next(l for l in text.splitlines() if l.startswith("ATOM"))
        # Make the same atom have insertion code A and competing alternative locations.
        def alt(letter,occupancy,x):
            return original[:16]+letter+original[17:26]+"A"+original[27:30]+f"{x:8.3f}"+original[38:54]+f"{occupancy:6.2f}"+original[60:]
        fixture="MODEL        1\n"+alt("A",.3,1)+"\n"+alt("B",.7,2)+"\nENDMDL\nMODEL        2\n"+alt("A",1,9)+"\nENDMDL\n"
        selected=r.parse_pdb(fixture)
        self.assertEqual(len(selected),1)
        self.assertEqual(selected.iloc[0].icode,"A")
        self.assertEqual(selected.iloc[0].altloc,"B")
        self.assertEqual(selected.iloc[0].x,2)
        with self.assertRaises(ValueError):r.parse_pdb("HEADER EMPTY\n")

if __name__=="__main__":unittest.main(verbosity=2)
