"""Independent numerical/edge-case checks for the new teaching algorithms."""
import itertools,math,unittest,json,gzip
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.spatial.distance import cdist
from scipy.stats import binomtest
from science_runtime import standardized_pca,stratified_holdout,stratified_folds,knn_predict,classification_metrics,kmeans,ridge_fit_predict,trapezoid_integral,bisection,wilson_interval,bootstrap_mean,permutation_mean_test
import science_runtime as methods

class ScienceMethods(unittest.TestCase):
    def test_source_calendar_without_pandas_datetime(self):
        dates=methods.iso_datetimes(['2012-02-28','2012-02-29','2012-03-01'])
        self.assertEqual([d.weekday() for d in dates],[1,2,3])
        self.assertEqual([(b-a).total_seconds() for a,b in zip(dates,dates[1:])],[86400,86400])
        samples=methods.iso_datetimes(['2016-01-11 17:00:00','2016-01-11 17:10:00'])
        self.assertEqual((samples[1]-samples[0]).total_seconds(),600)
        with self.assertRaises(ValueError):methods.iso_datetimes(['2012-02-30'])
    def test_pca_covariance_reference(self):
        rng=np.random.default_rng(21);values=rng.normal(size=(40,5))*[1,2,4,8,16]+[3,0,2,0,-5]
        result=standardized_pca(values,5)
        eigen=np.linalg.eigvalsh(np.cov(result['standardized'],rowvar=False))[::-1]
        np.testing.assert_allclose(result['explained_ratio'],eigen/eigen.sum())
        np.testing.assert_allclose(result['scores']@result['loadings'],result['standardized'],atol=1e-12)
        with self.assertRaises(ValueError):standardized_pca(np.ones((4,3)))
    def test_stratification_and_knn_distance_reference(self):
        labels=np.repeat(np.arange(3),50);train,test=stratified_holdout(labels,.3,42)
        self.assertFalse(set(train)&set(test));np.testing.assert_array_equal(np.bincount(labels[test]),[15,15,15])
        folds=stratified_folds(labels[train],5,7)
        np.testing.assert_array_equal(np.sort(np.concatenate(folds)),np.arange(105))
        x=np.array([[0,0],[0,1],[2,1],[3,0]],float);y=np.array([0,0,1,1]);query=np.array([[.1,.1],[2.3,.8]])
        distances=cdist(query,x,'euclidean')
        expected=np.array([np.argmax(np.bincount(y[indices],minlength=2)) for indices in np.argsort(distances,axis=1,kind='stable')[:,:3]])
        np.testing.assert_array_equal(knn_predict(x,y,query,3),expected)
        result=classification_metrics([0,0,1,1,2,2],[0,1,1,1,2,0],[0,1,2])
        self.assertAlmostEqual(result['macro_f1'],(.5+.8+2/3)/3)
        with self.assertRaises(ValueError):knn_predict(x,y,query,0)
    def test_kmeans_known_minimum(self):
        x=np.array([[0,0],[0,1],[10,0],[10,1]],float);result=kmeans(x,2,42,10)
        self.assertAlmostEqual(result['inertia'],1.0)
        self.assertTrue(np.all(np.diff(result['history'])<=1e-10))
        self.assertEqual(result['labels'][0],result['labels'][1]);self.assertNotEqual(result['labels'][0],result['labels'][2])
        with self.assertRaises(ValueError):kmeans(x,5)
        with self.assertRaises(ValueError):kmeans(x,2,restarts=0)
    def test_ridge_normal_equation_reference(self):
        x=np.array([[1,2],[2,1],[3,4],[4,2],[5,5]],float);y=np.array([2,3,4,5,6],float);query=np.array([[2,3],[5,4]],float)
        result=ridge_fit_predict(x,y,query,2)
        a=np.column_stack([np.ones(5),(x-x.mean(axis=0))/x.std(axis=0)])
        penalty=np.diag([0,2,2]);reference=np.linalg.solve(a.T@a+penalty,a.T@y)
        np.testing.assert_allclose(result['coefficients'],reference)
        expected=np.column_stack([np.ones(2),(query-x.mean(axis=0))/x.std(axis=0)])@reference
        np.testing.assert_allclose(result['predictions'],expected)
        with self.assertRaises(ValueError):ridge_fit_predict(x,y,query,penalty=-1)
    def test_quadrature_and_root_certificates(self):
        x=np.array([0,.2,1,3]);self.assertAlmostEqual(trapezoid_integral(x,3*x+2),19.5)
        root,history=bisection(lambda v:v*v-2,0,2,1e-12)
        self.assertLessEqual(abs(root-brentq(lambda v:v*v-2,0,2)),history[-1][-1]/2+1e-13)
        self.assertTrue(all((lo*lo-2)*(hi*hi-2)<=0 for _,lo,hi,*_ in history))
        with self.assertRaises(ValueError):bisection(lambda v:v*v+1,-1,1)
        with self.assertRaises(ValueError):trapezoid_integral(x[::-1],x[::-1])
    def test_resampling_references(self):
        for n in [1,10,100]:
            for successes in sorted({0,n//2,n}):
                reference=binomtest(successes,n).proportion_ci(.95,method='wilson')
                np.testing.assert_allclose(wilson_interval(successes,n),[reference.low,reference.high],atol=1e-12)
        constant=bootstrap_mean([5,5,5],200,7)
        self.assertEqual(constant['standard_error'],0);np.testing.assert_array_equal(constant['percentile_95'],[5,5])
        pool=np.array([0,1,2,3]);exact=[]
        for selected in itertools.combinations(range(4),2):
            mask=np.zeros(4,bool);mask[list(selected)]=True;exact.append(pool[mask].mean()-pool[~mask].mean())
        reference=np.mean(np.abs(exact)>=2)
        result=permutation_mean_test([0,1],[2,3],6000,42)
        self.assertLess(abs(result['p_value']-reference),.03)
        self.assertEqual(permutation_mean_test([1,1],[1,1],19,42)['p_value'],1)

    def test_physical_closed_limits(self):
        pendulum=methods.pendulum_solution(1,9.80665,5)
        self.assertLess(abs(pendulum['period_s']/(2*np.pi/np.sqrt(9.80665))-1),.002)
        energy=pendulum['energy_per_mass'];self.assertLess(np.max(abs(energy-energy[0]))/energy[0],1e-6)
        flight=methods.projectile_with_drag(.145,.073,0,1.225,30,45,height_m=1.5)
        vertical=30/np.sqrt(2);reference=(vertical+np.sqrt(vertical**2+2*9.80665*1.5))/9.80665
        self.assertAlmostEqual(flight['flight_s'],reference,places=7)
        heat=methods.heat_diffusion_explicit(nodes=41)
        exact=20+50*np.sin(np.pi*heat['x'])*np.exp(-1e-4*np.pi**2*600)
        self.assertLess(np.max(abs(heat['temperature'][-1]-exact)),.03)
        with self.assertRaises(ValueError):methods.heat_diffusion_explicit(ratio=.6)

    def test_chemistry_source_records_and_equilibrium(self):
        root=Path(__file__).resolve().parent/'data'
        molecules=json.loads(gzip.decompress((root/'molecules.json.gz').read_bytes()))
        for row in molecules['properties']:
            parsed=methods.parse_molfile(molecules['sdf_2d'][str(row['CID'])]);graph,summary=methods.molecular_graph(parsed)
            self.assertEqual(summary['atoms'],parsed['atom_count'])
            self.assertEqual(sum(a['formal_charge'] for a in parsed['atoms']),row['Charge'])
        self.assertEqual(methods.parse_simple_formula('C8H10N4O2'),{'C':8,'H':10,'N':4,'O':2})
        with self.assertRaises(ValueError):methods.parse_simple_formula('Mg(OH)2')
        model=json.loads(gzip.decompress((root/'models.json.gz').read_bytes()))
        pressure=methods.water_saturation_pressure(np.array([273.16,647.096]),model['water_saturation'])
        np.testing.assert_allclose(pressure,[611.657,22.064e6],rtol=5e-6)
        titration=methods.weak_acid_titration(.1,.025,.1,np.array([0,.0125,.025,.05]))
        self.assertLess(abs(titration['pH'][1]-4.76),.01)
        self.assertLess(np.max(abs(titration['charge_residual_mol_per_L'])),1e-10)
        x=np.arange(9,dtype=float);calibration=methods.linear_calibration(x,.02+.0015*x)
        np.testing.assert_allclose(calibration['coefficients'],[.02,.0015],atol=1e-14)

    def test_engineering_closed_references(self):
        beam=methods.cantilever_fem(4,3,200e9,8.333e-6,300)
        reference=300*beam['x']**2*(9-beam['x'])/(6*200e9*8.333e-6)
        np.testing.assert_allclose(beam['displacement_m'],reference,rtol=1e-10,atol=1e-14)
        self.assertAlmostEqual(beam['reaction'][0],-300,places=6)
        self.assertAlmostEqual(beam['reaction'][1],-900,places=6)
        circuit=methods.rc_step_response(1000,100e-6,5)
        self.assertAlmostEqual(circuit['tau_s'],.1)
        self.assertAlmostEqual(circuit['analytic_voltage'][20],5*(1-np.exp(-1)))
        controlled=methods.pid_thermal_simulation()
        self.assertTrue(np.all((controlled['control_percent']>=0)&(controlled['control_percent']<=100)))
        self.assertLess(abs(controlled['temperature_degC'][-1]-60),.2)

    def test_financial_exact_fixtures(self):
        covariance=np.array([[.04,.01],[.01,.09]])
        weights=methods.minimum_variance_weights(covariance)
        np.testing.assert_allclose(weights,[.08/.11,.03/.11],atol=1e-7)
        result=methods.empirical_tail_risk(np.array([0,1,2,3]),.625)
        self.assertAlmostEqual(result['expected_shortfall'],8/3)
        self.assertEqual(result['VaR'],2)
        with self.assertRaises(ValueError):methods.empirical_tail_risk([0,1],1)
        draws=methods.circular_block_resample(np.arange(20),5,42)
        self.assertEqual(len(draws),20);self.assertTrue(np.isin(draws,np.arange(20)).all())

    def test_text_boundaries_and_explicit_tfidf(self):
        root=Path(__file__).resolve().parent/'data'
        novels=json.loads(gzip.decompress((root/'novels.json.gz').read_bytes()))
        for book,count in zip(novels['books'],[61,24]):
            chapters=methods.split_novel_chapters(methods.strip_ebook_wrapper(book['raw_text']))
            self.assertEqual(len(chapters),count)
        self.assertEqual(len(methods.keyword_contexts(['pride','prides','pride'],'pride')),2)
        model=methods.tfidf_svd(['red blue red','blue green','red green'],set(),1,1,3,2)
        raw=np.array([[2,1,0],[0,1,1],[1,0,1]],float)
        self.assertEqual(model['terms'],['red','blue','green'])
        expected=raw*(np.log(4/3)+1);expected/=np.linalg.norm(expected,axis=1)[:,None]
        np.testing.assert_allclose(model['tfidf'],expected)
        empty=methods.mention_cooccurrence(['none'],{'one':r'\bone\b','two':r'\btwo\b'})
        self.assertEqual(empty['graph'].number_of_nodes(),2);self.assertEqual(empty['graph'].number_of_edges(),0)

if __name__=='__main__':unittest.main(verbosity=2)
