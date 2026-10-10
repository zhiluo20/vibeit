"""Readable teaching methods embedded verbatim into multidisciplinary notebooks."""
import numpy as np
import re
import networkx as nx
import pandas as pd
from datetime import datetime
from collections import Counter
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize
from scipy.spatial.distance import cdist

def residue_minimum_distances(left, right):
    """Minimum Euclidean atom distance per residue pair, retaining chain/insertion IDs.

    Caller explicitly selects positive-occupancy heavy atoms. This measures
    geometric proximity, not a hydrogen bond, affinity, buried area or energy.
    At most one residue's atom-distance block is held in memory at a time.
    """
    keys = ['chain', 'resnum', 'icode', 'residue']
    columns = keys + ['atom_count']
    if left.empty or right.empty:
        raise ValueError('Both atom selections must be nonempty')
    if not np.isfinite(left[['x','y','z']].to_numpy()).all() or not np.isfinite(right[['x','y','z']].to_numpy()).all():
        raise ValueError('Coordinates must be finite')
    left = left.reset_index(drop=True)
    right = right.reset_index(drop=True)
    left_groups = list(left.groupby(keys, sort=False).indices.items())
    right_groups = list(right.groupby(keys, sort=False).indices.items())
    left_residues = pd.DataFrame([list(key)+[len(indices)] for key,indices in left_groups], columns=columns)
    right_residues = pd.DataFrame([list(key)+[len(indices)] for key,indices in right_groups], columns=columns)
    right_codes = np.empty(len(right), dtype=int)
    for j, (_, indices) in enumerate(right_groups):
        right_codes[indices] = j
    matrix = np.full((len(left_groups),len(right_groups)), np.inf)
    right_xyz = right[['x','y','z']].to_numpy(dtype=float)
    for i, (_, indices) in enumerate(left_groups):
        block = cdist(left.iloc[indices][['x','y','z']].to_numpy(dtype=float), right_xyz)
        np.minimum.at(matrix[i], right_codes, block.min(axis=0))
    return left_residues, right_residues, matrix

def residue_labels(frame):
    """Display author residue identifiers without discarding insertion codes."""
    return [f'{r.chain}:{r.residue}{int(r.resnum)}{r.icode}' for r in frame.itertuples()]

def pdb_atom_text(atoms):
    """Serialize an explicitly selected atom table for 3D display, without reorienting it."""
    lines = []
    for r in atoms.itertuples():
        lines.append(f'{r.record:<6}{r.serial:5d} {r.atom:>4} {r.residue:>3} {r.chain:1}{r.resnum:4d}{r.icode:1}   '
                     f'{r.x:8.3f}{r.y:8.3f}{r.z:8.3f}{r.occupancy:6.2f}{r.bfactor:6.2f}          {r.element:>2}  ')
    return '\n'.join(lines) + '\nEND\n'

def iso_datetimes(values):
    """Parse source ISO dates with the standard library; keep tables as ISO strings."""
    return [datetime.fromisoformat(str(value)) for value in values]

def audit_numeric_table(frame,columns):
    """Audit observed rows; never silently impute or remove them."""
    if frame.empty or frame.index.has_duplicates:
        raise ValueError('Expected a nonempty table with unique row IDs')
    missing=[name for name in columns if name not in frame.columns]
    if missing:raise ValueError('Missing required columns: '+str(missing))
    values=frame[columns].to_numpy(dtype=float)
    if not np.isfinite(values).all():raise ValueError('Non-finite measurements; inspect missing values explicitly')
    return {'rows':len(frame),'features':len(columns),'finite':True,'duplicate_measurement_rows':int(frame[columns].duplicated().sum())}

def standardized_pca(values,components=2):
    """Population-SD standardization followed by an SVD of centered observations."""
    values=np.asarray(values,dtype=float)
    if values.ndim!=2 or min(values.shape)<2 or not np.isfinite(values).all():
        raise ValueError('PCA requires a finite observations × features matrix')
    if not 1<=components<=min(values.shape):raise ValueError('Invalid number of components')
    mean=values.mean(axis=0);scale=values.std(axis=0,ddof=0)
    if np.any(scale==0):raise ValueError('Constant features must be removed or handled explicitly')
    standardized=(values-mean)/scale
    left,singular,loadings=np.linalg.svd(standardized,full_matrices=False)
    # Fix signs for reproducible plots, without changing distances or explained variance.
    for j in range(len(singular)):
        pivot=np.argmax(np.abs(loadings[j]))
        if loadings[j,pivot]<0:loadings[j]*=-1;left[:,j]*=-1
    variance=singular**2/(len(values)-1)
    return dict(mean=mean,scale=scale,scores=left[:,:components]*singular[:components],
                loadings=loadings[:components],explained_ratio=variance/variance.sum(),standardized=standardized)

def stratified_holdout(labels,test_fraction=.3,seed=42):
    """Reserve a deterministic class-stratified test set before fitting anything."""
    labels=np.asarray(labels)
    if labels.ndim!=1 or not 0<test_fraction<1:raise ValueError('Invalid labels or test fraction')
    rng=np.random.default_rng(seed);train=[];test=[]
    for label in np.unique(labels):
        indices=np.flatnonzero(labels==label)
        if len(indices)<3:raise ValueError('Each class needs at least three observations')
        indices=rng.permutation(indices)
        count=max(1,min(len(indices)-1,int(round(len(indices)*test_fraction))))
        test.extend(indices[:count]);train.extend(indices[count:])
    return np.sort(train),np.sort(test)

def stratified_folds(labels,count=5,seed=42):
    """Return validation indices relative to the training subset only."""
    labels=np.asarray(labels);rng=np.random.default_rng(seed);folds=[[] for _ in range(count)]
    if count<2:raise ValueError('At least two folds are required')
    for label in np.unique(labels):
        indices=np.flatnonzero(labels==label)
        if len(indices)<count:raise ValueError('A class has fewer observations than folds')
        for j,chunk in enumerate(np.array_split(rng.permutation(indices),count)):folds[j].extend(chunk)
    return [np.sort(fold) for fold in folds]

def knn_predict(train_values,train_labels,test_values,k=5):
    """Euclidean kNN with a deterministic smallest-label tie rule."""
    train_values=np.asarray(train_values,dtype=float);test_values=np.asarray(test_values,dtype=float)
    train_labels=np.asarray(train_labels)
    if train_values.ndim!=2 or test_values.ndim!=2 or train_values.shape[1]!=test_values.shape[1]:
        raise ValueError('Training/test feature dimensions differ')
    if len(train_labels)!=len(train_values) or not isinstance(k,(int,np.integer)) or not 1<=k<=len(train_values):raise ValueError('Invalid k or labels')
    if not np.isfinite(train_values).all() or not np.isfinite(test_values).all():raise ValueError('Non-finite features')
    classes=np.unique(train_labels);predictions=[]
    for row in test_values:
        neighbors=np.argsort(np.sum((train_values-row)**2,axis=1),kind='stable')[:k]
        votes=[np.sum(train_labels[neighbors]==label) for label in classes]
        predictions.append(classes[np.argmax(votes)])
    return np.asarray(predictions)

def classification_metrics(truth,predictions,classes):
    truth=np.asarray(truth);predictions=np.asarray(predictions);classes=np.asarray(classes)
    if truth.shape!=predictions.shape or truth.size==0:raise ValueError('Invalid comparison')
    if not np.isin(truth,classes).all() or not np.isin(predictions,classes).all():raise ValueError('Unknown class')
    confusion=np.array([[np.sum((truth==a)&(predictions==b)) for b in classes] for a in classes])
    true_positive=np.diag(confusion)
    precision=np.divide(true_positive,confusion.sum(axis=0),out=np.zeros(len(classes),dtype=float),where=confusion.sum(axis=0)>0)
    recall=np.divide(true_positive,confusion.sum(axis=1),out=np.zeros(len(classes),dtype=float),where=confusion.sum(axis=1)>0)
    f1=np.divide(2*precision*recall,precision+recall,out=np.zeros(len(classes),dtype=float),where=precision+recall>0)
    return dict(confusion=confusion,accuracy=float(np.mean(truth==predictions)),macro_f1=float(f1.mean()),precision=precision,recall=recall)

def kmeans(values,k=3,seed=42,restarts=10,max_iterations=100):
    """Lloyd's algorithm with k-means++ seeds; labels are excluded from fitting."""
    values=np.asarray(values,dtype=float)
    if values.ndim!=2 or not isinstance(k,(int,np.integer)) or not np.isfinite(values).all() or not 1<=k<=len(np.unique(values,axis=0)):
        raise ValueError('Invalid observations or number of distinct clusters')
    if not isinstance(restarts,(int,np.integer)) or not isinstance(max_iterations,(int,np.integer)) or min(restarts,max_iterations)<1:
        raise ValueError('Restarts and maximum iterations must be positive integers')
    rng=np.random.default_rng(seed);best=None
    for restart in range(restarts):
        centers=[values[rng.integers(len(values))]]
        for _ in range(1,k):
            distance=np.min(np.sum((values[:,None,:]-np.asarray(centers)[None,:,:])**2,axis=2),axis=1)
            centers.append(values[rng.choice(len(values),p=distance/distance.sum())])
        centers=np.asarray(centers);history=[]
        for _ in range(max_iterations):
            distance=np.sum((values[:,None,:]-centers[None,:,:])**2,axis=2)
            assigned=np.argmin(distance,axis=1)
            updated=np.array([values[assigned==j].mean(axis=0) if np.any(assigned==j) else centers[j] for j in range(k)])
            objective=float(np.sum((values-updated[assigned])**2));history.append(objective)
            if np.allclose(updated,centers,atol=1e-10,rtol=0):centers=updated;break
            centers=updated
        assigned=np.argmin(np.sum((values[:,None,:]-centers[None,:,:])**2,axis=2),axis=1)
        objective=float(np.sum((values-centers[assigned])**2))
        if best is None or objective<best['inertia']:
            best=dict(centers=centers,labels=assigned,inertia=objective,history=np.asarray(history))
    return best

def ridge_fit_predict(train_values,train_target,test_values,penalty=1.0):
    """Scale using training statistics and solve ridge by an augmented least-squares system."""
    train_values=np.asarray(train_values,dtype=float);test_values=np.asarray(test_values,dtype=float)
    target=np.asarray(train_target,dtype=float)
    if train_values.ndim!=2 or len(train_values)==0 or target.shape!=(len(train_values),) or penalty<0:raise ValueError('Invalid training data or penalty')
    if test_values.ndim!=2 or train_values.shape[1]!=test_values.shape[1]:raise ValueError('Training/test feature dimensions differ')
    if not np.isfinite(train_values).all() or not np.isfinite(test_values).all() or not np.isfinite(target).all():raise ValueError('Non-finite training data')
    mean=train_values.mean(axis=0);scale=train_values.std(axis=0);scale=np.where(scale==0,1,scale)
    design=np.column_stack([np.ones(len(train_values)),(train_values-mean)/scale])
    test_design=np.column_stack([np.ones(len(test_values)),(test_values-mean)/scale])
    regularizer=np.sqrt(penalty)*np.eye(design.shape[1]);regularizer[0,0]=0
    coefficients=np.linalg.lstsq(np.vstack([design,regularizer]),np.r_[target,np.zeros(design.shape[1])],rcond=None)[0]
    return dict(predictions=test_design@coefficients,coefficients=coefficients,mean=mean,scale=scale,train_predictions=design@coefficients)

def regression_metrics(truth,predictions):
    truth=np.asarray(truth,dtype=float);predictions=np.asarray(predictions,dtype=float)
    if truth.shape!=predictions.shape or truth.size==0 or not np.isfinite(truth-predictions).all():raise ValueError('Invalid regression comparison')
    error=predictions-truth;denominator=np.sum((truth-truth.mean())**2)
    return dict(mae=float(np.mean(np.abs(error))),rmse=float(np.sqrt(np.mean(error**2))),r_squared=float(1-np.sum(error**2)/denominator) if denominator>0 else float('nan'))

def trapezoid_integral(x,y):
    """Integrate a tabulated curve with explicitly increasing abscissae."""
    x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=float)
    if x.ndim!=1 or x.shape!=y.shape or len(x)<2 or not np.isfinite(x+y).all():raise ValueError('Invalid curve')
    widths=np.diff(x)
    if np.any(widths<=0):raise ValueError('x must be strictly increasing')
    return float(np.sum(widths*(y[:-1]+y[1:])/2))

def bisection(function,lower,upper,tolerance=1e-10,max_iterations=100):
    """Bracket a continuous scalar root; retain each actual interval update."""
    if not np.isfinite([lower,upper,tolerance]).all() or lower>=upper or tolerance<=0:raise ValueError('Invalid bracket or tolerance')
    f_lower=float(function(lower));f_upper=float(function(upper))
    if not np.isfinite([f_lower,f_upper]).all():raise ValueError('Non-finite endpoint values')
    if f_lower==0:return lower,[]
    if f_upper==0:return upper,[]
    if np.sign(f_lower)==np.sign(f_upper):raise ValueError('The bracket does not change sign')
    history=[]
    for iteration in range(max_iterations):
        midpoint=(lower+upper)/2;value=float(function(midpoint))
        if not np.isfinite(value):raise ValueError('Non-finite function value')
        history.append([iteration,lower,upper,midpoint,value,upper-lower])
        if value==0 or (upper-lower)/2<=tolerance:return midpoint,history
        if np.sign(value)==np.sign(f_lower):lower=midpoint;f_lower=value
        else:upper=midpoint;f_upper=value
    raise RuntimeError('Requested root tolerance not reached')

def wilson_interval(successes,trials,z=1.959963984540054):
    """A binomial Wilson score interval; the returned endpoints are probabilities."""
    if not isinstance(trials,(int,np.integer)) or trials<=0 or not 0<=successes<=trials or z<=0:
        raise ValueError('Invalid success count, trial count or z')
    proportion=successes/trials;denominator=1+z*z/trials
    center=(proportion+z*z/(2*trials))/denominator
    half=z*np.sqrt(proportion*(1-proportion)/trials+z*z/(4*trials*trials))/denominator
    return float(max(0,center-half)),float(min(1,center+half))

def bootstrap_mean(values,repetitions=2000,seed=42):
    """Ordinary iid bootstrap; exchangeability is a statistical assumption."""
    values=np.asarray(values,dtype=float)
    if values.ndim!=1 or len(values)<2 or not np.isfinite(values).all() or repetitions<2:
        raise ValueError('Need finite observations and at least two resamples')
    rng=np.random.default_rng(seed)
    resamples=rng.choice(values,size=(repetitions,len(values)),replace=True)
    means=resamples.mean(axis=1)
    return dict(estimate=float(values.mean()),means=means,percentile_95=np.quantile(means,[.025,.975]),standard_error=float(means.std(ddof=1)))

def permutation_mean_test(a,b,repetitions=1999,seed=42):
    """Two-sided independent-group mean permutation test, with the +1 correction."""
    a=np.asarray(a,dtype=float);b=np.asarray(b,dtype=float)
    if a.ndim!=1 or b.ndim!=1 or min(len(a),len(b))<2 or not np.isfinite(np.r_[a,b]).all() or repetitions<1:
        raise ValueError('Need two finite groups and positive permutation count')
    observed=float(a.mean()-b.mean());pool=np.r_[a,b];rng=np.random.default_rng(seed)
    null=np.empty(repetitions)
    for j in range(repetitions):
        shuffled=rng.permutation(pool);null[j]=shuffled[:len(a)].mean()-shuffled[len(a):].mean()
    exceedances=int(np.sum(np.abs(null)>=abs(observed)))
    return dict(difference=observed,p_value=(exceedances+1)/(repetitions+1),null_differences=null,exceedances=exceedances)

def pendulum_solution(length_m,gravity,angle_deg,duration_s=20,samples=2001):
    """Nonlinear ideal pendulum; energy is per unit mass in J/kg."""
    if length_m<=0 or gravity<=0 or not 0<abs(angle_deg)<180 or duration_s<=0 or samples<3:
        raise ValueError('Use positive length/gravity/time and a nonzero angle below 180 degrees')
    def dynamics(t,state):return [state[1],-gravity/length_m*np.sin(state[0])]
    t=np.linspace(0,duration_s,samples)
    solved=solve_ivp(dynamics,[0,duration_s],[np.deg2rad(angle_deg),0],t_eval=t,rtol=1e-9,atol=1e-11)
    if not solved.success:raise RuntimeError(solved.message)
    theta,omega=solved.y;energy=.5*length_m**2*omega**2+gravity*length_m*(1-np.cos(theta))
    indices=np.flatnonzero((theta[:-1]>0)&(theta[1:]<=0))
    crossings=[t[j]-theta[j]*(t[j+1]-t[j])/(theta[j+1]-theta[j]) for j in indices]
    period=float(np.mean(np.diff(crossings))) if len(crossings)>1 else float('nan')
    return dict(t=t,theta=theta,omega=omega,energy_per_mass=energy,period_s=period)

def oscillator_solution(mass,stiffness,damping,force_amplitude=0,drive_frequency=0,duration_s=20,initial_displacement=1,samples=2001):
    if mass<=0 or stiffness<=0 or damping<0 or duration_s<=0 or samples<3:
        raise ValueError('Invalid oscillator parameters')
    def dynamics(t,state):
        x,v=state;return [v,(force_amplitude*np.cos(drive_frequency*t)-damping*v-stiffness*x)/mass]
    t=np.linspace(0,duration_s,samples)
    solved=solve_ivp(dynamics,[0,duration_s],[initial_displacement,0],t_eval=t,rtol=1e-8,atol=1e-10)
    if not solved.success:raise RuntimeError(solved.message)
    return dict(t=t,x=solved.y[0],velocity=solved.y[1])

def projectile_with_drag(mass,diameter,drag_coefficient,air_density,speed,angle_deg,gravity=9.80665,height_m=1.5):
    """Constant-density quadratic drag; terminate at a descending ground crossing."""
    if mass<=0 or diameter<=0 or drag_coefficient<0 or air_density<0 or speed<=0 or gravity<=0 or height_m<0:
        raise ValueError('Invalid projectile parameters')
    area=np.pi*(diameter/2)**2;factor=.5*air_density*drag_coefficient*area/mass
    angle=np.deg2rad(angle_deg);initial=[0,height_m,speed*np.cos(angle),speed*np.sin(angle)]
    def dynamics(t,state):
        x,z,vx,vz=state;velocity=np.hypot(vx,vz)
        return [vx,vz,-factor*velocity*vx,-gravity-factor*velocity*vz]
    def ground(t,state):return state[1]
    ground.direction=-1;ground.terminal=True
    solved=solve_ivp(dynamics,[0,60],initial,events=ground,dense_output=True,rtol=1e-9,atol=1e-11,max_step=.1)
    if not solved.success or len(solved.t_events[0])!=1:raise RuntimeError('Descending ground event not found')
    flight=float(solved.t_events[0][0]);t=np.linspace(0,flight,501);state=solved.sol(t)
    velocity=np.hypot(state[2],state[3]);energy=.5*mass*velocity**2+mass*gravity*state[1]
    drag_power=-.5*air_density*drag_coefficient*area*velocity**3
    return dict(t=t,state=state,flight_s=flight,range_m=float(state[0,-1]),energy_J=energy,drag_power_W=drag_power)

def heat_diffusion_explicit(nodes=51,length_m=1,alpha=1e-4,duration_s=600,ratio=.4,ambient=20,amplitude=50):
    """FTCS heat equation with fixed-temperature ends and a known sine-mode initial condition."""
    if nodes<3 or length_m<=0 or alpha<=0 or duration_s<=0 or not 0<ratio<=.5:
        raise ValueError('Require >=3 nodes, positive parameters and FTCS ratio <=0.5')
    x=np.linspace(0,length_m,nodes);spacing=x[1]-x[0]
    count=int(np.ceil(duration_s/(ratio*spacing**2/alpha)));dt=duration_s/count;actual_ratio=alpha*dt/spacing**2
    times=np.linspace(0,duration_s,count+1);temperature=np.empty((count+1,nodes))
    temperature[0]=ambient+amplitude*np.sin(np.pi*x/length_m);temperature[:,0]=ambient;temperature[:,-1]=ambient
    for j in range(count):
        temperature[j+1,1:-1]=temperature[j,1:-1]+actual_ratio*(temperature[j,2:]-2*temperature[j,1:-1]+temperature[j,:-2])
    return dict(x=x,t=times,temperature=temperature,spacing_m=spacing,step_s=dt,ratio=actual_ratio)

def planck_radiance(wavelength_m,temperature_K,h,c,k_B):
    """Spectral radiance per metre of wavelength: W m^-2 sr^-1 m^-1."""
    wavelength=np.asarray(wavelength_m,dtype=float)
    if not np.isfinite(wavelength).all() or np.any(wavelength<=0) or temperature_K<=0 or min(h,c,k_B)<=0:
        raise ValueError('Planck law requires positive finite wavelengths, temperature and constants')
    exponent=h*c/(wavelength*k_B*temperature_K);values=np.zeros_like(wavelength)
    safe=exponent<700
    values[safe]=2*h*c*c/(wavelength[safe]**5*np.expm1(exponent[safe]))
    return values

def parse_simple_formula(formula):
    """Parse plain elemental formulas; refuse isotopes, groups and charge notation."""
    tokens=re.findall(r'([A-Z][a-z]?)(\d*)',formula)
    if not tokens or ''.join(element+count for element,count in tokens)!=formula:
        raise ValueError('This teaching parser accepts plain elemental formulas only')
    counts={}
    for element,text in tokens:
        count=int(text) if text else 1
        if count<1:raise ValueError('Element counts must be positive')
        counts[element]=counts.get(element,0)+count
    return counts

def parse_molfile(text):
    """Read V2000 atoms/bonds and formal-charge annotations from one SDF record."""
    lines=text.splitlines()
    if len(lines)<4 or 'V2000' not in lines[3]:raise ValueError('Expected one V2000 molfile/SDF record')
    atom_count=int(lines[3][:3]);bond_count=int(lines[3][3:6])
    if atom_count<=0 or len(lines)<4+atom_count+bond_count:raise ValueError('Truncated molfile')
    atoms=[];charge_codes={0:0,1:3,2:2,3:1,5:-1,6:-2,7:-3}
    for j,line in enumerate(lines[4:4+atom_count]):
        element=line[31:34].strip();position=[float(line[:10]),float(line[10:20]),float(line[20:30])]
        if not element or not np.isfinite(position).all():raise ValueError('Invalid atom record')
        charge_code=int(line[36:39].strip() or 0)
        if charge_code not in charge_codes:raise ValueError('Unsupported atom charge/radical code')
        atoms.append(dict(index=j,element=element,position=position,formal_charge=charge_codes[charge_code]))
    bonds=[];seen=set()
    for line in lines[4+atom_count:4+atom_count+bond_count]:
        a=int(line[:3])-1;b=int(line[3:6])-1;order=int(line[6:9]);pair=tuple(sorted([a,b]))
        if not 0<=a<atom_count or not 0<=b<atom_count or a==b or pair in seen or order not in [1,2,3,4]:
            raise ValueError('Invalid or duplicate bond')
        seen.add(pair);bonds.append(dict(a=a,b=b,order=order))
    for line in lines[4+atom_count+bond_count:]:
        if line.startswith('M  CHG'):
            fields=line.split();count=int(fields[2])
            for j in range(count):
                index=int(fields[3+2*j])-1;charge=int(fields[4+2*j])
                if not 0<=index<atom_count:raise ValueError('Invalid formal-charge atom index')
                atoms[index]['formal_charge']=charge
    return dict(atoms=atoms,bonds=bonds,title=lines[0],atom_count=atom_count,bond_count=bond_count)

def molecular_graph(parsed):
    graph=nx.Graph()
    for atom in parsed['atoms']:graph.add_node(atom['index'],element=atom['element'],formal_charge=atom['formal_charge'])
    for bond in parsed['bonds']:graph.add_edge(bond['a'],bond['b'],reported_bond_type=bond['order'])
    components=nx.number_connected_components(graph)
    return graph,dict(atoms=graph.number_of_nodes(),bonds=graph.number_of_edges(),connected_components=components,cycle_rank=graph.number_of_edges()-graph.number_of_nodes()+components)

def weak_acid_titration(acid_molar,acid_volume_L,base_molar,added_volume_L,pKa=4.76,Kw=1e-14):
    """Ideal dilute monoprotic-acid/strong-base charge balance, concentration model."""
    volumes=np.asarray(added_volume_L,dtype=float)
    if min(acid_molar,acid_volume_L,base_molar,Kw)<=0 or not np.isfinite(volumes).all() or np.any(volumes<0):
        raise ValueError('Invalid titration concentrations or volumes')
    Ka=10**(-pKa);pH=[];fractions=[];residuals=[]
    for added in volumes:
        total_volume=acid_volume_L+added;total_acid=acid_molar*acid_volume_L/total_volume;sodium=base_molar*added/total_volume
        def balance(log_h):
            H=10**log_h;anion=total_acid*Ka/(Ka+H)
            return H+sodium-Kw/H-anion
        log_h=brentq(balance,-16,1,xtol=1e-13)
        H=10**log_h;pH.append(-log_h);fractions.append(Ka/(Ka+H));residuals.append(balance(log_h))
    return dict(pH=np.asarray(pH),anion_fraction=np.asarray(fractions),charge_residual_mol_per_L=np.asarray(residuals))

def water_saturation_pressure(temperature_K,parameters):
    """IAPWS SR1-86(1992) saturation-pressure correlation, output in pascals."""
    T=np.asarray(temperature_K,dtype=float);Tc=parameters['critical_temperature_K'];Pc=parameters['critical_pressure_Pa']
    if not np.isfinite(T).all() or np.any(T<273.16) or np.any(T>Tc):
        raise ValueError('Reference correlation requires triple-point through critical temperatures')
    tau=1-T/Tc;series=np.zeros_like(T)
    for coefficient,power in zip(parameters['coefficients'],parameters['exponents']):series+=coefficient*tau**power
    return Pc*np.exp(Tc/T*series)

def linear_calibration(concentration,absorbance):
    """OLS with an intercept; concentrations must state their units in the calling cell."""
    x=np.asarray(concentration,dtype=float);y=np.asarray(absorbance,dtype=float)
    if x.ndim!=1 or x.shape!=y.shape or len(x)<3 or not np.isfinite(x+y).all() or np.ptp(x)==0:
        raise ValueError('Need finite, varying calibration concentrations and >2 observations')
    design=np.column_stack([np.ones(len(x)),x]);coefficient=np.linalg.lstsq(design,y,rcond=None)[0]
    residual=y-design@coefficient;variance=float(residual@residual/(len(x)-2))
    covariance=variance*np.linalg.inv(design.T@design)
    return dict(coefficients=coefficient,residual=residual,variance=variance,covariance=covariance,fitted=design@coefficient)

def cantilever_fem(elements,length_m,young_Pa,second_moment_m4,tip_force_N):
    """Euler–Bernoulli Hermite beam elements: transverse displacement and rotation DOFs."""
    if not isinstance(elements,(int,np.integer)) or elements<1 or min(length_m,young_Pa,second_moment_m4)<=0:
        raise ValueError('Need positive beam geometry/material and an integer element count')
    nodes=elements+1;ell=length_m/elements;stiffness=np.zeros((2*nodes,2*nodes));load=np.zeros(2*nodes)
    local=young_Pa*second_moment_m4/ell**3*np.array([[12,6*ell,-12,6*ell],[6*ell,4*ell**2,-6*ell,2*ell**2],[-12,-6*ell,12,-6*ell],[6*ell,2*ell**2,-6*ell,4*ell**2]])
    for element in range(elements):
        indices=np.arange(2*element,2*element+4);stiffness[np.ix_(indices,indices)]+=local
    load[-2]=tip_force_N;displacement=np.zeros(2*nodes)
    displacement[2:]=np.linalg.solve(stiffness[2:,2:],load[2:])
    reaction=stiffness@displacement-load
    return dict(x=np.linspace(0,length_m,nodes),displacement_m=displacement[::2],rotation_rad=displacement[1::2],stiffness=stiffness,load=load,all_DOFs=displacement,reaction=reaction)

def rc_step_response(resistance_ohm,capacitance_F,input_voltage_V,steps_per_tau=20,duration_tau=5):
    if resistance_ohm<=0 or capacitance_F<=0 or steps_per_tau<1 or duration_tau<=0:
        raise ValueError('Positive R/C and valid sampling settings are required')
    tau=resistance_ohm*capacitance_F;count=int(np.ceil(duration_tau*steps_per_tau))
    time=np.arange(count+1)*tau/steps_per_tau;voltage=np.zeros(count+1);dt=time[1]-time[0]
    for j in range(count):voltage[j+1]=voltage[j]+dt*(input_voltage_V-voltage[j])/tau
    exact=input_voltage_V*(-np.expm1(-time/tau))
    return dict(t=time,numerical_voltage=voltage,analytic_voltage=exact,tau_s=tau,step_s=dt)

def pid_thermal_simulation(Kp=4,Ki=.2,Kd=6,tau_s=60,gain_degC_per_percent=1,setpoint_degC=60,ambient_degC=20,dt_s=1,duration_s=600,antiwindup=True,maximum_percent=100,disturbance_start_s=300,disturbance_equilibrium_offset_degC=-10):
    """Declared thermal plant and conditional-integration PID; derivative on measurement."""
    if min(tau_s,dt_s,duration_s,maximum_percent)<=0 or min(Kp,Ki,Kd)<0 or dt_s>=tau_s:
        raise ValueError('Invalid controller parameters or overly large plant time step')
    count=int(np.floor(duration_s/dt_s));time=np.arange(count+1)*dt_s
    temperature=np.full(count+1,ambient_degC,dtype=float);control=np.zeros(count+1);integral_trace=np.zeros(count+1);unclamped=np.zeros(count+1)
    integral=0;previous=ambient_degC
    for j in range(count):
        error=setpoint_degC-temperature[j];derivative=(temperature[j]-previous)/dt_s
        request=Kp*error+integral-Kd*derivative;applied=float(np.clip(request,0,maximum_percent))
        blocked=(request>=maximum_percent and error>0) or (request<=0 and error<0)
        if not antiwindup or not blocked:integral+=Ki*error*dt_s
        control[j]=applied;integral_trace[j]=integral;unclamped[j]=request
        disturbance=disturbance_equilibrium_offset_degC if time[j]>=disturbance_start_s else 0
        previous=temperature[j]
        temperature[j+1]=temperature[j]+dt_s*(ambient_degC-temperature[j]+gain_degC_per_percent*applied+disturbance)/tau_s
    control[-1]=control[-2];integral_trace[-1]=integral_trace[-2];unclamped[-1]=unclamped[-2]
    return dict(t=time,temperature_degC=temperature,control_percent=control,integral_percent=integral_trace,unclamped_percent=unclamped,error_degC=setpoint_degC-temperature)

def worldbank_panel(payload):
    """Preserve missing observations; official economy metadata excludes aggregates."""
    economies=pd.DataFrame(payload['economies']).set_index('iso3')
    observations=pd.DataFrame(payload['observations'])
    observations=observations[observations.iso3.isin(economies.index)].copy()
    if observations.duplicated(['iso3','year','indicator']).any():raise ValueError('Duplicate economy/year/indicator observations')
    observations['value']=pd.to_numeric(observations.value,errors='raise')
    wide=observations.pivot(index=['iso3','year'],columns='indicator',values='value').sort_index()
    return wide,economies,observations

def minimum_variance_weights(covariance):
    """Long-only fully invested variance minimization; no expected-return prediction."""
    covariance=np.asarray(covariance,dtype=float)
    if covariance.ndim!=2 or covariance.shape[0]!=covariance.shape[1] or len(covariance)<2 or not np.isfinite(covariance).all():
        raise ValueError('Need a finite square covariance matrix')
    if not np.allclose(covariance,covariance.T) or np.linalg.eigvalsh(covariance).min()<-1e-10:
        raise ValueError('Covariance must be symmetric positive semidefinite')
    n=len(covariance);initial=np.full(n,1/n)
    result=minimize(lambda w:1e4*float(w@covariance@w),initial,jac=lambda w:2e4*covariance@w,
        method='SLSQP',bounds=[(0,1)]*n,constraints={'type':'eq','fun':lambda w:w.sum()-1,'jac':lambda w:np.ones(n)},
        options={'ftol':1e-12,'maxiter':500})
    if not result.success:raise RuntimeError(result.message)
    weights=result.x
    if np.any(weights<-1e-8) or not np.isclose(weights.sum(),1):raise RuntimeError('Optimizer violated weight constraints')
    return weights

def empirical_tail_risk(losses,confidence=.95):
    """Inverse empirical-CDF VaR and fractional upper-tail expected shortfall."""
    losses=np.asarray(losses,dtype=float)
    if losses.ndim!=1 or len(losses)<2 or not np.isfinite(losses).all() or not 0<confidence<1:
        raise ValueError('Need finite losses and confidence strictly between zero and one')
    ordered=np.sort(losses)[::-1];mass=(1-confidence)*len(ordered);full=int(np.floor(mass));fraction=mass-full
    tail_sum=float(ordered[:full].sum())
    if fraction>0:tail_sum+=fraction*ordered[full]
    return dict(VaR=float(np.quantile(losses,confidence,method='inverted_cdf')),expected_shortfall=tail_sum/mass,tail_sample_mass=mass)

def circular_block_resample(values,block_length=5,seed=42):
    """One circular block bootstrap draw; stationary resampling is assumed."""
    values=np.asarray(values,dtype=float)
    if values.ndim!=1 or len(values)<2 or not np.isfinite(values).all() or not isinstance(block_length,(int,np.integer)) or not 1<=block_length<=len(values):
        raise ValueError('Invalid sequence or block length')
    rng=np.random.default_rng(seed);count=int(np.ceil(len(values)/block_length))
    starts=rng.integers(0,len(values),count)
    indices=(starts[:,None]+np.arange(block_length)[None,:])%len(values)
    return values[indices.ravel()[:len(values)]]

def strip_ebook_wrapper(raw_text):
    """Return the analysis body while the unmodified source/complete license remain in metadata."""
    text=raw_text.replace('\r\n','\n').replace('\r','\n')
    start=re.search(r'\*\*\* START[^\n]*\*\*\*',text,re.I)
    end=re.search(r'\*\*\* END[^\n]*\*\*\*',text,re.I)
    if not start or not end or end.start()<=start.end():raise ValueError('Ebook start/end markers not found')
    return text[start.end():end.start()]

def split_novel_chapters(body):
    """Declared two-ebook rule: repeated labels resolve to last heading, excluding their TOCs."""
    headings=list(re.finditer(r'(?im)^\s*chapter\s+([ivxlcdm]+|\d+)[.\]]*\s*$',body))
    if not headings:raise ValueError('No supported chapter headings')
    last={match.group(1).upper():match for match in headings}
    chosen=sorted(last.values(),key=lambda match:match.start());chapters=[]
    for j,match in enumerate(chosen):
        text=body[match.end():chosen[j+1].start() if j+1<len(chosen) else len(body)]
        text=re.sub(r'\[Illustration\b[^\]]*\]',' ',text,flags=re.I|re.S)
        text=text.replace('_','').replace('’',"'").strip()
        if len(text)<300:raise ValueError('Unexpected short chapter after declared TOC rule')
        chapters.append(dict(label=match.group(1).upper(),order=j+1,text=text))
    return chapters

def tokenize_words(text):
    """Transparent English-letter tokenizer; punctuation/case decisions are part of the method."""
    return re.findall(r"[a-z]+(?:'[a-z]+)?",text.lower().replace('’',"'"))

def keyword_contexts(tokens,query,window=7):
    query=query.lower()
    if not re.fullmatch(r"[a-z]+(?:'[a-z]+)?",query) or window<0:raise ValueError('Expected one normalized word and nonnegative window')
    rows=[]
    for index,word in enumerate(tokens):
        if word==query:
            rows.append(dict(token_index=index,before=' '.join(tokens[max(0,index-window):index]),keyword=word,
                after=' '.join(tokens[index+1:index+1+window])))
    return rows

def mention_cooccurrence(paragraphs,patterns,minimum_count=3):
    """Paragraph-level surface-pattern cooccurrence; preserve all declared entity nodes."""
    if minimum_count<1:raise ValueError('Minimum cooccurrence count must be positive')
    labels=list(patterns);compiled={name:re.compile(pattern,re.I) for name,pattern in patterns.items()}
    matrix=np.zeros((len(labels),len(labels)),dtype=int);presence=np.zeros(len(labels),dtype=int)
    for paragraph in paragraphs:
        found=np.array([bool(compiled[name].search(paragraph)) for name in labels]);presence+=found
        matrix+=np.outer(found,found).astype(int)
    np.fill_diagonal(matrix,0);graph=nx.Graph();graph.add_nodes_from(labels)
    for i in range(len(labels)):
        for j in range(i+1,len(labels)):
            if matrix[i,j]>=minimum_count:graph.add_edge(labels[i],labels[j],paragraph_count=int(matrix[i,j]))
    return dict(graph=graph,labels=labels,matrix=matrix,paragraph_presence=presence)

def tfidf_svd(documents,stopwords,min_df=3,max_df_fraction=.9,max_terms=500,components=3):
    """Exploratory TF-IDF + uncentered SVD; signed components are not topic probabilities."""
    if len(documents)<3 or components<1 or max_terms<2:raise ValueError('Need documents and valid model sizes')
    counts=[Counter(word for word in tokenize_words(text) if word not in stopwords) for text in documents]
    frequency=Counter();totals=Counter()
    for count in counts:frequency.update(count.keys());totals.update(count)
    eligible=[word for word in frequency if min_df<=frequency[word]<=max_df_fraction*len(documents)]
    terms=sorted(eligible,key=lambda word:(-totals[word],word))[:max_terms]
    if len(terms)<components:raise ValueError('Vocabulary too small for the requested components')
    matrix=np.array([[count.get(word,0) for word in terms] for count in counts],dtype=float)
    idf=np.log((1+len(documents))/(1+np.count_nonzero(matrix,axis=0)))+1
    matrix*=idf
    norms=np.linalg.norm(matrix,axis=1)
    if np.any(norms==0):raise ValueError('A document has no retained terms')
    matrix/=norms[:,None]
    left,singular,right=np.linalg.svd(matrix,full_matrices=False)
    for j in range(min(components,len(singular))):
        if right[j,np.argmax(abs(right[j]))]<0:right[j]*=-1;left[:,j]*=-1
    return dict(terms=terms,tfidf=matrix,idf=idf,scores=left[:,:components]*singular[:components],components=right[:components],singular_values=singular)
