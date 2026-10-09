"""Six numerical/statistical workflows with analytic or independent reference checks."""
from ._common import lesson,step,exercises,bilingual
from .data_science import IRIS_LOAD

COURSES=[
 lesson('ma01-numerical-calculus',1,'numerical-calculus','Measure differentiation and integration error','测量数值微分与积分误差','Compare tabulated Gaussian curves, finite differences and trapezoidal integration with analytic references.','将高斯曲线表、有限差分和梯形积分与解析结果比较。',['models'],['trapezoid_integral'],'numerical','Numerical methods','数值方法',discipline='mathematics',data_kind='model',difficulty=1,icon='∫',setup_imports='import math\nfrom scipy.integrate import quad\n',packages=['numpy','pandas','scipy','matplotlib','IPython']),
 lesson('ma02-bracketed-roots',2,'bracketed-roots','Find a physical root with a verifiable bracket','用可核验区间寻找物理根','Trace bisection, compare a trusted solver and derive Wien displacement from frozen SI constants.','追踪二分迭代，对照参考求解器，并从冻结的 SI 常数推导维恩位移。',['constants'],['bisection'],'numerical','Numerical methods','数值方法',discipline='mathematics',data_kind='reference',icon='🔍',setup_imports='from scipy.optimize import brentq\n',packages=['numpy','pandas','scipy','matplotlib','IPython']),
 lesson('ma03-conditioning',3,'least-squares-conditioning','Inspect a poorly conditioned least-squares problem','检查病态最小二乘问题','Build a polynomial design matrix, inspect singular values, compare solvers and separate coefficient stability from prediction error.','构造多项式设计矩阵，检查奇异值、比较求解器，并区分系数稳定性与预测误差。',['models'],[],'numerical','Numerical methods','数值方法',discipline='mathematics',data_kind='model',icon='🔢'),
 lesson('ma04-monte-carlo',4,'monte-carlo-uncertainty','Quantify Monte Carlo uncertainty','量化 Monte Carlo 不确定性','Estimate a circle area with seeded random points, use Wilson intervals and inspect repeated-experiment coverage.','用固定随机点估计圆面积，计算 Wilson 区间，并检查重复实验的覆盖率。',['models'],['wilson_interval'],'uncertainty','Sampling uncertainty','采样不确定性',discipline='mathematics',data_kind='simulation',icon='🎲',setup_imports='import math\nfrom scipy.stats import binomtest\n',packages=['numpy','pandas','scipy','matplotlib','IPython']),
 lesson('ma05-bootstrap',5,'bootstrap-measurements','Bootstrap uncertainty in real measurements','对真实测量做 Bootstrap 分析','Resample an observed Iris group, compare percentile intervals and standard-error formulas, and state the sampling assumptions.','对真实 Iris 组内测量重采样，比较百分位区间和标准误公式，并说明采样假设。',['iris'],['audit_numeric_table','bootstrap_mean'],'uncertainty','Sampling uncertainty','采样不确定性',discipline='mathematics',icon='📏'),
 lesson('ma06-permutation-tests',6,'permutation-multiple-tests','Run permutation tests and correct the full family','执行置换检验并校正完整检验族','Test predeclared Iris group comparisons, use the Monte Carlo +1 correction and reconcile joint Benjamini–Hochberg adjustment.','检验预先声明的 Iris 组间比较，使用 Monte Carlo +1 修正，并核对联合 BH 校正。',['iris'],['audit_numeric_table','permutation_mean_test','bh_adjust'],'inference','Statistical inference','统计推断',discipline='mathematics',minutes=60,difficulty=3,icon='⚖️',setup_imports='from scipy.stats import false_discovery_control\n',packages=['numpy','pandas','scipy','matplotlib','IPython']),
]
for c in COURSES:
 c['online_url']='https://archive.ics.uci.edu/dataset/53/iris' if 'iris' in c['snapshots'] else 'https://physics.nist.gov/cuu/Constants/' if 'constants' in c['snapshots'] else 'https://docs.scipy.org/doc/scipy/tutorial/integrate.html'
 c['data_note']=bilingual('Analytic functions and Monte Carlo points are mathematical teaching models, not experimental measurements. When Iris observations are used, row exchangeability and the sampling design remain assumptions; convenience records alone do not establish population representativeness. Numerical discretization error is distinct from sampling uncertainty.','解析函数与 Monte Carlo 点属于数学教学模型，不是实验测量。使用 Iris 观测时，可交换性和采样设计仍是统计假设；方便样本不自动代表总体。数值离散误差与采样不确定性应分别解释。')

SECTIONS={}
SECTIONS[COURSES[0]['id']]=[
 step('Declare the function and reference integral','声明函数与参考积分','Use f(x)=exp(−x²) on the finite interval [−2,2]. x and f are dimensionless in this benchmark. The exact finite-interval integral is sqrt(pi)·erf(2); do not compare it with the infinite-interval value sqrt(pi).','使用 [−2,2] 区间上的 f(x)=exp(−x²)。本基准的 x 与函数值无量纲。有限区间积分为 sqrt(pi)·erf(2)，不能与无限区间积分 sqrt(pi) 混淆。','''model_inputs=snapshot("models");seed=model_inputs["seed"]
LOWER,UPPER=-2.0,2.0;POINTS=161
x=np.linspace(LOWER,UPPER,POINTS);y=np.exp(-x*x)
reference=math.sqrt(math.pi)*math.erf(2)
quad_reference,quad_error=quad(lambda value:np.exp(-value*value),LOWER,UPPER)
assert np.isclose(reference,quad_reference,rtol=1e-12)
fig,ax=plt.subplots(figsize=(7,4));ax.plot(x,y,label="exp(−x²)");ax.fill_between(x,y,alpha=.2)
ax.set(xlabel="x (dimensionless)",ylabel="f(x)",title="Finite-interval integration problem");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Differentiate the tabulated curve','对曲线表求导','Interior central differences are second-order for this smooth function. Endpoint rules can have a different error order; calculate interior error separately. np.gradient receives the actual x grid rather than assuming a unit spacing.','平滑函数的内部中心差分为二阶误差。端点公式可能具有不同误差阶，因此单独计算内部误差。np.gradient 使用真实 x 网格，不假定间距为一。','''derivative=np.gradient(y,x,edge_order=2);exact_derivative=-2*x*np.exp(-x*x)
fig,ax=plt.subplots(figsize=(7,4));ax.plot(x,exact_derivative,label="Analytic",lw=2);ax.plot(x,derivative,"--",label="Tabulated finite difference")
ax.set(xlabel="x",ylabel="df/dx",title="Derivative from explicit grid spacing");ax.legend();plt.tight_layout();plt.show()
print("Maximum interior derivative error:",float(np.max(np.abs(derivative[1:-1]-exact_derivative[1:-1]))))'''),
 step('Refine the integration grid','细化积分网格','Trapezoid error should decrease approximately like h² while rounding error is small. Both axes of the convergence plot are logarithmic. A falling error curve here concerns a known smooth model; it is not an uncertainty interval for noisy measurements.','舍入误差较小时，梯形积分误差应近似按 h² 下降。收敛图双轴取对数。这里的误差描述已知平滑模型，不是有噪声测量的置信区间。','''intervals=np.array([20,40,80,160,320]);estimates=[];widths=[]
for count in intervals:
 grid=np.linspace(LOWER,UPPER,count+1);widths.append((UPPER-LOWER)/count)
 estimates.append(trapezoid_integral(grid,np.exp(-grid*grid)))
error=np.abs(np.array(estimates)-reference)
fig,ax=plt.subplots(figsize=(7,4));ax.loglog(widths,error,"o-",label="Observed absolute error")
ax.loglog(widths,error[0]*(np.array(widths)/widths[0])**2,"--",label="h² comparison")
ax.set(xlabel="Grid spacing h",ylabel="Absolute integral error",title="Trapezoid grid refinement");ax.legend();plt.tight_layout();plt.show()'''),
 step('Reconcile and export the numerical audit','核对并导出数值审计','Compare the readable implementation with NumPy’s tabulated trapezoid rule, and check grid-order validation. Keep analytic values, quadrature tolerances and discretization errors in different columns.','将可读实现与 NumPy 梯形规则对照，并检查网格顺序约束。解析值、求积容差和离散误差分别记录。','''assert np.isclose(trapezoid_integral(x,y),np.trapezoid(y,x))
assert error[-1]<error[0] and np.all(error>0)
try:trapezoid_integral(x[::-1],y[::-1])
except ValueError:print("Reversed abscissae rejected")
else:raise AssertionError("Invalid grid accepted")
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"x":x,"f":y,"finite_difference":derivative,"analytic_derivative":exact_derivative}).to_csv(OUTPUT_DIR/"curve-and-derivative.csv",index=False)
pd.DataFrame({"intervals":intervals,"h":widths,"integral":estimates,"absolute_error":error}).to_csv(OUTPUT_DIR/"grid-refinement.csv",index=False)
(OUTPUT_DIR/"references.json").write_text(json.dumps({"finite_interval":[LOWER,UPPER],"analytic_integral":reference,"quad_reference":quad_reference,"quad_error_estimate":quad_error},indent=2))
print("Reference checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[1]['id']]=[
 step('Exclude the trivial root','排除平凡根','The wavelength form of Planck’s law gives 5(1−exp(−x))−x=0. x=0 is a mathematical root but not the positive spectral maximum sought here. The bracket [1,10] has a sign change and isolates the relevant positive root.','普朗克波长形式给出 5(1−exp(−x))−x=0。x=0 是数学根，但不是本课所求的正谱峰。区间 [1,10] 存在变号，可隔离所需正根。','''constants=snapshot("constants")["constants"]
def equation(value):return 5*(-np.expm1(-value))-value
root,history=bisection(equation,1.0,10.0,tolerance=1e-10)
reference=brentq(equation,1.0,10.0,xtol=1e-13)
trace=pd.DataFrame(history,columns=["iteration","lower","upper","midpoint","f_midpoint","width"])
print("Positive root:",root,"; independent brentq:",reference)
display(trace.head(8))
grid=np.linspace(0,10,501)
fig,ax=plt.subplots(figsize=(7,4));ax.plot(grid,equation(grid));ax.axhline(0,color="black",lw=1);ax.axvline(root,color="red",linestyle="--")
ax.set(xlabel="x",ylabel="5(1−exp(−x))−x",title="Trivial zero and the positive Wien root");plt.tight_layout();plt.show()''',cover=True),
 step('Inspect the bracket certificate','检查区间证书','Every iteration retains an interval with opposite endpoint signs. Width shrinks by a factor of two. The stopping rule bounds midpoint location error by half the current interval width; a small residual alone does not guarantee the same coordinate error for a flat function.','每次迭代保留两端异号区间，宽度逐次减半。终止条件将中点位置误差约束为当前区间半宽。对于平坦函数，仅有较小残差不保证同等位置精度。','''fig,ax=plt.subplots(figsize=(7,4));ax.semilogy(trace.iteration,trace.width/2,label="Certified half-width")
ax.semilogy(trace.iteration,np.maximum(np.abs(trace.midpoint-reference),1e-16),label="Observed error to reference")
ax.set(xlabel="Iteration",ylabel="x error bound / observed error",title="Bisection convergence certificate");ax.legend();plt.tight_layout();plt.show()'''),
 step('Convert the dimensionless root into physical units','将无量纲根转换为物理量','Using frozen h, c and k_B, b=hc/(k_B x) has units metre·kelvin. The curve shows predicted peak wavelength in nm at each assumed blackbody temperature in K. These are ideal-model values, not measured stellar spectra.','使用冻结的 h、c、k_B，b=hc/(k_B x) 的单位为米·开尔文。曲线展示假定黑体温度 K 对应的峰值波长 nm。这些是理想模型值，不是恒星实测光谱。','''b=constants["h"]["value"]*constants["c"]["value"]/(constants["k_B"]["value"]*root)
temperatures=np.linspace(2500,10000,101);peak_nm=1e9*b/temperatures
fig,ax=plt.subplots(figsize=(7,4));ax.plot(temperatures,peak_nm)
ax.set(xlabel="Assumed temperature (K)",ylabel="Peak wavelength (nm)",title="Wien displacement derived from a verified root");plt.tight_layout();plt.show()
print("Derived displacement constant (m K):",b)'''),
 step('Check signs, tolerances and exported units','检查符号、容差及导出单位','Compare the returned root with the independent solver and check every recorded bracket. A non-bracketing interval must raise an error. A numerical tolerance is a computation setting, not an experimental measurement uncertainty.','将根与参考求解器核对，并检查全部记录区间。不包含变号的区间必须报错。数值容差是计算设置，不是实验测量不确定性。','''assert abs(root-reference)<=trace.width.iloc[-1]/2+1e-12
assert all(equation(lo)*equation(hi)<=0 for lo,hi in zip(trace.lower,trace.upper))
assert np.isclose(b,2.897771955e-3,rtol=1e-8)
try:bisection(equation,6,10)
except ValueError:print("Non-bracketing interval rejected")
else:raise AssertionError("Missing sign change accepted")
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);trace.to_csv(OUTPUT_DIR/"bisection-trace.csv",index=False)
pd.DataFrame({"temperature_K":temperatures,"peak_wavelength_nm":peak_nm}).to_csv(OUTPUT_DIR/"wien-curve.csv",index=False)
print("Root certificate and unit checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[2]['id']]=[
 step('Build a deterministic model benchmark','构造确定性模型基准','Use 25 x values on [0,1] and y=exp(x). A degree-10 Vandermonde design has powers with very different scales. These are analytic teaching values; no measurement noise or statistical confidence interval is implied.','取 [0,1] 上 25 个 x，并令 y=exp(x)。十阶 Vandermonde 矩阵的幂次量级不同。这是解析教学数据，没有隐含测量噪声或统计置信区间。','''inputs=snapshot("models")
DEGREE=10;x=np.linspace(0,1,25);y=np.exp(x)
design=np.vander(x,DEGREE+1,increasing=True)
singular=np.linalg.svd(design,compute_uv=False);condition=np.linalg.cond(design)
print("Design shape:",design.shape,"; condition number:",condition)
fig,ax=plt.subplots(figsize=(7,4));ax.semilogy(np.arange(1,len(singular)+1),singular,"o-")
ax.set(xlabel="Singular-value index",ylabel="Singular value",title="Different resolvability of polynomial directions");plt.tight_layout();plt.show()'''),
 step('Solve through SVD and compare normal equations','用 SVD 求解并比较正规方程','The SVD least-squares solver avoids squaring the condition number. The normal-equation comparison explicitly solves AᵀA; it can be unstable or singular even when A has full mathematical rank. Report solver failures instead of silently replacing them.','SVD 最小二乘避免平方条件数。对照方法显式求解 AᵀA，即使 A 在数学上满秩也可能不稳定或奇异。应报告失败，不能静默替换结果。','''stable=np.linalg.lstsq(design,y,rcond=None)[0]
try:
 normal=np.linalg.solve(design.T@design,design.T@y);normal_failure=None
except np.linalg.LinAlgError as error:
 normal=None;normal_failure=str(error)
print("Condition(A):",condition,"; condition(A.T @ A):",np.linalg.cond(design.T@design))
print("Normal-equation failure:",normal_failure)
dense=np.linspace(0,1,501);dense_design=np.vander(dense,DEGREE+1,increasing=True)
fig,ax=plt.subplots(figsize=(7,4));ax.plot(dense,np.exp(dense),color="black",label="Analytic exp(x)")
ax.plot(dense,dense_design@stable,"--",label="SVD least squares")
if normal is not None:ax.plot(dense,dense_design@normal,":",label="Normal equations")
ax.scatter(x,y,s=12);ax.set(xlabel="x",ylabel="y",title="Predictions can agree despite coefficient instability");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Perturb the input response at a recorded scale','以记录的尺度扰动响应','Add a deterministic 10⁻⁸-scale sinusoidal perturbation. Compare relative changes in response and coefficients, then inspect prediction error on the same interpolation interval. Large coefficient changes need not translate directly into the same prediction change.','加入确定的 10⁻⁸ 量级正弦扰动。比较响应与系数的相对变化，再检查同一插值区间的预测误差。较大的系数变化不一定造成同等预测变化。','''perturbed=y+1e-8*np.sin(17*x)
altered=np.linalg.lstsq(design,perturbed,rcond=None)[0]
relative_input=np.linalg.norm(perturbed-y)/np.linalg.norm(y)
relative_coefficients=np.linalg.norm(altered-stable)/np.linalg.norm(stable)
print("Relative response perturbation:",relative_input,"; relative coefficient change:",relative_coefficients)
fig,ax=plt.subplots(figsize=(7,4));ax.plot(dense,dense_design@stable-np.exp(dense),label="Original response")
ax.plot(dense,dense_design@altered-np.exp(dense),label="Perturbed response")
ax.set(xlabel="x in interpolation interval",ylabel="Prediction − analytic value",title="Observable prediction errors");ax.legend();plt.tight_layout();plt.show()'''),
 step('Check orthogonality and export diagnostics','检查正交条件并导出诊断','A least-squares residual should be approximately orthogonal to design columns, subject to floating-point precision. Record the matrix condition, solver choice, coefficient vectors and observation/prediction errors separately. Do not interpret these deterministic coefficients as causal effects.','最小二乘残差应在浮点精度范围内近似正交于设计列。分别记录条件数、求解器、系数向量和观测/预测误差。确定性多项式系数不是因果效应。','''residual=design@stable-y
assert np.linalg.norm(design.T@residual)<1e-8
assert np.isfinite(stable).all() and np.max(np.abs(dense_design@stable-np.exp(dense)))<1e-5
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"power":np.arange(DEGREE+1),"SVD_coefficient":stable,"perturbed_coefficient":altered,"normal_equation_coefficient":normal if normal is not None else np.full(DEGREE+1,np.nan)}).to_csv(OUTPUT_DIR/"coefficients.csv",index=False)
pd.DataFrame({"x":dense,"analytic":np.exp(dense),"SVD_prediction":dense_design@stable,"perturbed_prediction":dense_design@altered}).to_csv(OUTPUT_DIR/"interpolation.csv",index=False)
(OUTPUT_DIR/"diagnostics.json").write_text(json.dumps({"degree":DEGREE,"condition_design":condition,"condition_gram":float(np.linalg.cond(design.T@design)),"relative_input_perturbation":relative_input,"relative_coefficient_change":relative_coefficients,"normal_equation_failure":normal_failure},indent=2))
print("Least-squares checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[3]['id']]=[
 step('Sample a known geometric probability','采样已知几何概率','Uniform points in the unit square fall inside the quarter-unit circle with probability pi/4. Multiplying the fraction by four estimates pi. The points are explicitly simulated; seed controls reproducibility, not scientific representativeness.','单位正方形的均匀点落在四分之一单位圆内的概率为 pi/4，比例乘四可估计 pi。这些点明确属于模拟，随机种子控制复现，不代表科学采样代表性。','''seed=int(snapshot("models")["seed"]);rng=np.random.default_rng(seed)
TRIALS=20000;points=rng.uniform(0,1,size=(TRIALS,2));inside=np.sum(points**2,axis=1)<=1
estimate=4*inside.mean();interval=4*np.asarray(wilson_interval(int(inside.sum()),TRIALS))
print("Estimated pi:",estimate,"; Wilson-derived 95% interval:",interval)
part=points[:1500];mask=inside[:1500]
fig,ax=plt.subplots(figsize=(5,5));ax.scatter(*part[mask].T,s=4,label="Inside");ax.scatter(*part[~mask].T,s=4,label="Outside")
theta=np.linspace(0,np.pi/2,101);ax.plot(np.cos(theta),np.sin(theta),color="black")
ax.set(xlabel="Simulated x",ylabel="Simulated y",xlim=(0,1),ylim=(0,1),aspect="equal",title="Simulated quarter-circle experiment");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Follow a single experiment','追踪一次实验','At checkpoints, calculate the binomial Wilson interval before scaling its endpoints by four. Point estimates can fluctuate as sample size grows; convergence does not require every successive error to decrease.','在检查点先计算二项 Wilson 区间，再将端点乘四。估计随样本量增加仍会波动；收敛不要求每一步误差都下降。','''sizes=np.array([100,200,500,1000,2000,5000,10000,20000]);cumulative=np.cumsum(inside)
estimates=4*cumulative[sizes-1]/sizes
intervals=np.array([4*np.asarray(wilson_interval(int(cumulative[n-1]),int(n))) for n in sizes])
fig,ax=plt.subplots(figsize=(8,4));ax.plot(sizes,estimates,"o-");ax.fill_between(sizes,*intervals.T,alpha=.2)
ax.axhline(math.pi,color="black",linestyle="--",label="Known pi")
ax.set(xscale="log",xlabel="Simulated trial count",ylabel="Pi estimate",title="Single-run estimates and 95% Wilson intervals");ax.legend();plt.tight_layout();plt.show()'''),
 step('Inspect repeated-experiment coverage','检查重复实验的覆盖率','Repeat 40 independent simulated runs at n=2000. The displayed intervals illustrate finite-simulation coverage: around 95% is a long-run target, not a guarantee that exactly 38 of 40 will contain pi.','在 n=2000 下重复 40 次独立模拟。图中的区间展示有限模拟覆盖率：约 95% 是长期目标，不保证本次恰有 38 个区间包含 pi。','''repeated=[]
for run in range(40):
 sample=rng.uniform(0,1,size=(2000,2));success=int(np.sum(np.sum(sample**2,axis=1)<=1))
 lo,hi=4*np.asarray(wilson_interval(success,2000));repeated.append([run,4*success/2000,lo,hi,lo<=math.pi<=hi])
repeat=pd.DataFrame(repeated,columns=["run","estimate","lower","upper","contains_pi"])
fig,ax=plt.subplots(figsize=(8,5))
for row in repeat.itertuples():ax.plot([row.lower,row.upper],[row.run,row.run],color="green" if row.contains_pi else "orange",lw=1)
ax.axvline(math.pi,color="black",linestyle="--");ax.set(xlabel="Pi interval",ylabel="Simulated run",title="Repeated Wilson intervals");plt.tight_layout();plt.show()
print("Observed repeated-run coverage:",float(repeat.contains_pi.mean()))'''),
 step('Compare with an independent implementation and export','对照独立实现并导出','Use SciPy’s binomial test object to obtain a Wilson proportion interval and compare before scaling. Distinguish probability, point estimate, interval confidence level and observed simulation coverage.','使用 SciPy 二项检验对象取得 Wilson 比例区间，先核对再缩放。区分概率、点估计、置信水平和本次模拟覆盖率。','''reference=binomtest(int(inside.sum()),TRIALS).proportion_ci(confidence_level=.95,method="wilson")
assert np.allclose(interval,4*np.array([reference.low,reference.high]))
assert np.all((intervals>=0)&(intervals<=4))
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"n":sizes,"estimate":estimates,"lower":intervals[:,0],"upper":intervals[:,1]}).to_csv(OUTPUT_DIR/"monte-carlo-checkpoints.csv",index=False)
repeat.to_csv(OUTPUT_DIR/"repeated-intervals.csv",index=False)
(OUTPUT_DIR/"simulation.json").write_text(json.dumps({"seed":seed,"trials":TRIALS,"known_probability":math.pi/4,"known_pi":math.pi,"interval":"binomial Wilson, scaled by four"},indent=2))
print("Independent interval check passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[4]['id']]=[
 step('Define a within-group measurement target','定义组内测量目标','Use the 50 source setosa petal lengths in centimetres. The target is their mean under an iid resampling model. Bootstrap uncertainty does not correct sampling bias, duplicated plants or an unrepresentative source collection.','使用来源中 50 条 setosa 花瓣长度，单位为厘米。在 iid 重采样模型下研究均值。Bootstrap 不会自动纠正采样偏差、重复植株或来源缺乏代表性。',IRIS_LOAD+'''
observed=frame.loc[frame.species.eq("Iris-setosa"),"petal_length_cm"].to_numpy(float)
assert len(observed)==50
bootstrap=bootstrap_mean(observed,repetitions=2000,seed=42)
print("Observed mean (cm):",bootstrap["estimate"],"; percentile interval:",bootstrap["percentile_95"])
fig,ax=plt.subplots(figsize=(7,4));ax.hist(observed,bins=np.arange(1,2.11,.1),edgecolor="white")
ax.set(xlabel="Observed petal length (cm)",ylabel="Source observations",title="Empirical group measurements");plt.tight_layout();plt.show()'''),
 step('Read the resampled mean distribution','解读重采样均值分布','Every bootstrap sample has 50 draws with replacement from the same 50 measurements. The histogram shows 2000 means, not 2000 newly measured plants. The shaded range marks percentile endpoints, conditional on this resampling model.','每次从相同 50 条测量中有放回抽取 50 个值。直方图是 2000 个均值，不是 2000 株新测量植物。着色范围表示给定重采样模型的百分位区间。','''fig,ax=plt.subplots(figsize=(7,4));ax.hist(bootstrap["means"],bins=35,edgecolor="white")
ax.axvspan(*bootstrap["percentile_95"],alpha=.2,color="orange",label="Percentile 95% range")
ax.axvline(bootstrap["estimate"],color="black",linestyle="--",label="Observed mean")
ax.set(xlabel="Bootstrap mean (cm)",ylabel="Resamples",title="Conditional bootstrap mean distribution");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Inspect dependence on resample count','检查重采样次数的影响','Resampling Monte Carlo error changes as the number of resamples grows, while the original 50-plant dataset stays fixed. More resamples improve numerical stability of this conditional distribution; they do not enlarge the observational sample.','增加重采样次数会改变 Monte Carlo 误差，但原始 50 条观测不变。更多重采样改善条件分布的数值稳定性，不会扩大实际观测样本。','''counts=[100,300,1000,2000];intervals=np.array([np.quantile(bootstrap["means"][:n],[.025,.975]) for n in counts])
fig,ax=plt.subplots(figsize=(7,4));ax.plot(counts,intervals[:,0],"o-",label="2.5th percentile");ax.plot(counts,intervals[:,1],"o-",label="97.5th percentile")
ax.set(xlabel="Resamples used",ylabel="Percentile endpoint (cm)",title="Monte Carlo stability with fixed source data");ax.legend();plt.tight_layout();plt.show()'''),
 step('Check resampling variability and export','检查重采样变异并导出','For the empirical distribution, the theoretical bootstrap standard error of the mean is population-SD/sqrt(n). Compare that with the observed resample SD, allowing finite-resampling noise. The textbook sample-SD/sqrt(n) is a different finite-n estimate.','经验分布的均值 Bootstrap 标准误为总体标准差/sqrt(n)。与实际重采样标准差比较，并允许有限重采样误差。教科书样本标准差/sqrt(n) 是另一有限样本估计。','''empirical_se=observed.std(ddof=0)/np.sqrt(len(observed));sample_se=observed.std(ddof=1)/np.sqrt(len(observed))
assert np.isclose(bootstrap["standard_error"],empirical_se,rtol=.08)
assert bootstrap["percentile_95"][0]<=bootstrap["percentile_95"][1]
print("Empirical-distribution SE:",empirical_se,"; sample-SD SE:",sample_se,"; resample SE:",bootstrap["standard_error"])
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"bootstrap_mean_cm":bootstrap["means"]}).to_csv(OUTPUT_DIR/"bootstrap-means.csv",index=False)
(OUTPUT_DIR/"bootstrap-summary.json").write_text(json.dumps({"source_group":"Iris-setosa","n":50,"resamples":2000,"seed":42,"mean_cm":bootstrap["estimate"],"percentile_95_cm":bootstrap["percentile_95"].tolist(),"empirical_distribution_SE_cm":empirical_se,"resample_SE_cm":bootstrap["standard_error"],"assumption":"iid exchangeable observations; source sampling bias not corrected"},indent=2))
print("Bootstrap variance check passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[5]['id']]=[
 step('Predeclare the entire comparison family','预先声明完整比较族','Compare every pair of the three source groups for each of four measurements: 12 tests. The null requires group-label exchangeability for each pooled comparison. Taxonomic convenience measurements do not provide randomized treatment assignment or representative population sampling.','对三组的所有成对组合及四个测量特征进行比较，共 12 个检验。每次比较的零假设要求合并记录的组标签可交换。分类方便样本不提供随机处理分配，也不保证总体代表性。',IRIS_LOAD+'''
groups=sorted(frame.species.unique());pairs=[(groups[i],groups[j]) for i in range(3) for j in range(i+1,3)]
records=[];first=None
for feature in features:
 for a,b in pairs:
  result=permutation_mean_test(frame.loc[frame.species.eq(a),feature],frame.loc[frame.species.eq(b),feature],repetitions=1999,seed=42)
  records.append({"feature":feature,"group_a":a,"group_b":b,"mean_difference_cm":result["difference"],"p_value":result["p_value"],"exceedances":result["exceedances"]})
  if first is None:first=result
results=pd.DataFrame(records);assert len(results)==12
display(results.head(8))'''),
 step('Inspect the null resampling distribution','检查零假设重采样分布','The histogram is the first comparison’s mean difference after randomly permuting pooled group labels. The observed difference is marked as a line. Use (extreme+1)/(B+1), so a finite Monte Carlo test never reports p=0.','直方图展示首次比较在合并组标签随机置换后产生的均值差，观测差异用竖线标记。使用 (极端次数+1)/(B+1)，有限 Monte Carlo 检验不会报告 p=0。','''fig,ax=plt.subplots(figsize=(7,4));ax.hist(first["null_differences"],bins=40,edgecolor="white")
ax.axvline(first["difference"],color="red",label="Observed difference")
ax.set(xlabel="Permuted mean difference (cm)",ylabel="Permutations",title="First predeclared comparison under exchangeability");ax.legend();plt.tight_layout();plt.show()'''),
 step('Correct all twelve tests together','对全部十二个检验联合校正','BH is applied to the whole predeclared family, including large p values. The chart uses log-scale p/q values and a 0.05 reference line. BH error-rate guarantees have dependence assumptions; adjustment does not fix sampling bias or turn association into causation.','BH 应用于完整预先声明检验族，包括较大的 p 值。图上对数坐标展示 p/q 值及 0.05 参考线。BH 错误率保证具有依赖结构假设；校正不能修复采样偏差，也不把关联变成因果。','''results["BH_q"]=bh_adjust(results.p_value.to_numpy())
results["Bonferroni"]=np.minimum(results.p_value*len(results),1)
labels=[f"{r.feature.replace('_cm','')} {r.group_a.replace('Iris-','')} / {r.group_b.replace('Iris-','')}" for r in results.itertuples()]
fig,ax=plt.subplots(figsize=(9,6));ax.plot(results.p_value,np.arange(12),"o",label="Raw p");ax.plot(results.BH_q,np.arange(12),"x",label="BH q")
ax.axvline(.05,color="gray",linestyle="--");ax.set_yticks(np.arange(12),labels,fontsize=8)
ax.set(xscale="log",xlabel="Probability / adjusted value",ylabel="Predeclared test",title="All comparisons share one adjustment family");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Separate measured effect size from p values','将测量效应量与 p 值分开','The heatmap uses mean differences in cm, not adjusted p values. Its sign depends on the declared group order. A small p value does not supply an effect-size unit, population claim or causal interpretation.','热图显示均值差，单位为厘米，而不是校正 p 值。符号取决于已声明组序。小 p 值不会自动给出效应量单位、总体结论或因果解释。','''effect=results.mean_difference_cm.to_numpy().reshape(4,3)
limit=np.max(np.abs(effect));fig,ax=plt.subplots(figsize=(7,4));im=ax.imshow(effect,cmap="coolwarm",vmin=-limit,vmax=limit)
ax.set_yticks(range(4),features);ax.set_xticks(range(3),[a.replace("Iris-","")+" / "+b.replace("Iris-","") for a,b in pairs],rotation=20,ha="right")
for i in range(4):
 for j in range(3):ax.text(j,i,f"{effect[i,j]:.2f}",ha="center",va="center")
fig.colorbar(im,ax=ax,label="Mean A − mean B (cm)");ax.set_title("Observed measurement differences");plt.tight_layout();plt.show()'''),
 step('Reconcile the Monte Carlo floor and independent BH','核对 Monte Carlo 下限及独立 BH','Verify the +1 formula, the 1/(B+1) lower bound and agreement with SciPy’s independent BH implementation. Export the entire family, not only comparisons passing a threshold.','核对 +1 公式、1/(B+1) 下限及与 SciPy 独立 BH 实现的一致性。导出完整检验族，不能只保存超过阈值的比较。','''assert np.allclose(results.p_value,(results.exceedances+1)/2000)
assert results.p_value.between(1/2000,1).all()
assert np.allclose(results.BH_q,false_discovery_control(results.p_value.to_numpy(),method="bh"))
assert (results.BH_q+1e-15>=results.p_value).all()
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);results.to_csv(OUTPUT_DIR/"all-permutation-tests.csv",index=False)
pd.DataFrame({"null_mean_difference_cm":first["null_differences"]}).to_csv(OUTPUT_DIR/"first-null-distribution.csv",index=False)
print("Joint family:",len(results),"; Monte Carlo p floor:",1/2000,"; independent BH check passed")''')]

EXERCISES={}
notes=[
 (['Explain the finite- versus infinite-interval Gaussian integral.','Compare interior and endpoint derivative errors.','The tails outside [−2,2] are excluded. Interior central differences and endpoint formulas need separate error analysis.','Using NumPy/SciPy/Matplotlib, double every integration grid and report observed error ratios without changing the analytic reference.','With the same packages, compare edge_order=1 and 2 and plot endpoint versus interior errors.','Check strictly increasing grids, agreement with NumPy trapezoid and the exact finite-interval erf expression.'],['说明高斯函数有限区间和无限区间积分的区别。','比较内部与端点微分误差。','[−2,2] 外的尾部被排除。内部中心差分与端点公式需要分别分析。','仅用 NumPy、SciPy、Matplotlib 将每个积分网格加密一倍，报告误差比并保持解析参考值。','使用同样的包比较 edge_order=1、2，分别画端点和内部误差。','核对严格递增网格、NumPy 梯形规则及有限区间 erf 解析表达式。']),
 (['Why is x=0 excluded from the Wien maximum search?','What does halving the bracket certify?','The trivial root is not the positive interior spectral maximum. Half-width bounds midpoint coordinate error for the retained continuous-function bracket.','Using NumPy/SciPy/Matplotlib, compare tolerances 1e-6, 1e-8 and 1e-10 and preserve every bracket certificate.','Using the same packages, annotate predicted peak wavelengths at 3000, 5000 and 8000 K with units.','Every retained bracket changes sign, roots agree with brentq within half-width and wavelengths are positive.'],['为何求维恩谱峰时排除 x=0？','区间减半能证实什么？','平凡根不是正的内部谱峰。对于保留的连续函数变号区间，半宽约束中点位置误差。','仅用 NumPy、SciPy、Matplotlib 比较 1e-6、1e-8、1e-10 容差，保留全部区间证书。','使用同样的包标注 3000、5000、8000 K 的预测峰值波长及单位。','各保留区间变号，与 brentq 的根误差不超过半宽，波长为正。']),
 (['Why can normal equations worsen conditioning?','Why can coefficients be unstable while interpolation remains accurate?','Forming AᵀA approximately squares the condition number. Correlated basis directions can cancel in predictions; coefficient and prediction stability are different targets.','Using NumPy/Matplotlib, compare degrees 3, 6 and 10 while keeping the same analytic observations and solver diagnostics.','Using the same packages, add a centered/scaled polynomial basis and compare condition numbers and interpolation errors.','Record failures explicitly, check normal-equation residuals and keep synthetic/model labels.'],['为何正规方程可能恶化条件数？','为何系数不稳定而插值仍可能准确？','形成 AᵀA 会近似平方条件数。相关基方向可能在预测中相互抵消；系数与预测稳定性是不同目标。','仅用 NumPy、Matplotlib 比较三、六、十阶，同时保留解析观测和求解诊断。','使用同样的包增加中心化/缩放后的多项式基，比较条件数及插值误差。','明确记录失败，检查最小二乘正交残差，保持模型数据标注。']),
 (['Why multiply the proportion interval by four?','Does a 95% confidence level guarantee coverage in a particular run?','The probability target is pi/4. Long-run confidence does not guarantee that one interval or exactly 95% of a small simulation batch covers the parameter.','Using NumPy/SciPy/Matplotlib, compare n=500, 2000 and 8000 across independent seeded simulations.','With the same packages, compare Wilson with the normal Wald interval, including success counts 0 and n.','Check probability endpoints before scaling, reproduce the SciPy Wilson reference and report all simulation seeds.'],['为何把比例区间乘四？','95% 置信水平是否保证本次覆盖？','概率目标为 pi/4。长期置信水平不能保证某一区间或一小批模拟恰有 95% 覆盖参数。','仅用 NumPy、SciPy、Matplotlib，在独立固定种子模拟中比较 n=500、2000、8000。','使用同样的包比较 Wilson 与正态 Wald 区间，包含成功次数为零或 n 的情况。','缩放前检查概率端点，复现 SciPy Wilson 参考，并记录所有种子。']),
 (['Why are resampled means not new plants?','Why use population SD for the empirical bootstrap variance identity?','Resampling reuses the observed empirical distribution. Its variance uses denominator n, while a sample estimate conventionally uses n−1. Neither removes sampling bias.','Using NumPy/Pandas/Matplotlib, repeat the bootstrap for another declared species group and retain cm units and source assumptions.','Using the same packages, plot interval endpoints across three independent seeds without claiming extra observed sample size.','Keep n=50 fixed, distinguish resample count from observations and compare empirical-distribution SE.'],['为何重采样均值不代表新植物？','经验 Bootstrap 方差恒等式为何使用总体标准差？','重采样重复使用观测经验分布，其方差分母为 n；常规样本估计用 n−1。两者均不能消除采样偏差。','仅用 NumPy、Pandas、Matplotlib 对另一个已声明物种组重复 Bootstrap，保留厘米单位及采样假设。','使用同样的包比较三个独立种子的区间端点，不将其当作新增观测。','观测 n=50 不变，区分重采样次数与观测数，并核对经验分布标准误。']),
 (['Explain the minimum attainable Monte Carlo p value.','Explain why correction must include all predeclared tests.','The +1 formula has minimum 1/(B+1). Restricting adjustment to already-small p values changes the family after observing data; BH also needs dependence assumptions.','Using NumPy/SciPy/Pandas/Matplotlib, increase permutations to 9999 while preserving the same twelve-test family.','Using the same packages, compare BH and Bonferroni and annotate their different error-rate targets.','Verify the +1 correction, all twelve exported rows, independent SciPy BH agreement and cm effect-size units.'],['解释 Monte Carlo p 值的最小可取值。','解释为何校正须包含全部预先声明检验。','+1 公式的最小值是 1/(B+1)。观察结果后只校正小 p 值会改变检验族；BH 还有依赖结构假设。','仅用 NumPy、SciPy、Pandas、Matplotlib 将置换增加至 9999，保留十二个检验。','使用同样的包比较 BH 和 Bonferroni，标明其错误率目标的差别。','核对 +1 修正、导出全部十二行、SciPy BH 一致性及厘米效应量单位。'])]
for c,(en,zh) in zip(COURSES,notes):EXERCISES[c['id']]=exercises(en,zh)
