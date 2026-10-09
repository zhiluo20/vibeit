"""Measured energy workflows plus verified, explicitly simulated engineering models."""
from ._common import lesson,step,exercises,bilingual

COURSES=[
 lesson('en01-energy-audit',1,'energy-sensor-audit','Audit a real building-energy record','审计真实建筑能耗记录','Check timestamps, sensor units, energy-to-power conversion and the observational scope of a single building.','检查时间戳、传感器单位、能量至功率换算及单栋建筑的观测范围。',['energy'],['audit_numeric_table'],'measurements','Measurements & signals','测量与信号',discipline='engineering',difficulty=1,icon='🔌'),
 lesson('en02-energy-regression',2,'energy-demand-regression','Evaluate a chronological energy regression','按时间顺序评估能耗回归','Fit training-only weather/calendar regressions, compare a mean baseline and inspect held-out energy errors.','只用训练时段拟合天气/日历回归，与均值基线比较，并检查测试能耗误差。',['energy'],['audit_numeric_table','ridge_fit_predict','regression_metrics'],'measurements','Measurements & signals','测量与信号',discipline='engineering',minutes=60,icon='🏠'),
 lesson('en03-energy-filtering',3,'energy-signal-filtering','Process a low-rate measured energy signal','处理低采样率实测能耗信号','Inspect a daily-unit spectrum, an explicitly acausal filter and the limits of ten-minute sampling.','检查日尺度频谱、明确的非因果滤波及十分钟采样的限制。',['energy'],['audit_numeric_table'],'measurements','Measurements & signals','测量与信号',discipline='engineering',icon='〰️',setup_imports='from scipy.signal import welch, butter, sosfiltfilt, sosfreqz\n',packages=['numpy','pandas','scipy','matplotlib','IPython']),
 lesson('en04-beam-fem',4,'cantilever-fem','Assemble and verify a beam finite-element model','组装并验证梁有限元模型','Assemble Hermite beam elements, enforce the clamp and compare nodal deflection and reactions with a closed reference.','组装 Hermite 梁单元、施加固定端，并将节点挠度与反力和闭式参考比较。',['models'],['cantilever_fem'],'design','Design models','设计模型',discipline='engineering',data_kind='model',minutes=60,difficulty=3,icon='📐'),
 lesson('en05-rc-circuit',5,'rc-circuit-response','Reconcile an RC circuit model','核对 RC 电路模型','Compare an explicit transient solution with an analytic step and frequency response, then inspect declared tolerance assumptions.','将显式暂态解与解析阶跃、频率响应核对，再检查声明的容差假设。',['models'],['rc_step_response'],'design','Design models','设计模型',discipline='engineering',data_kind='model',icon='🔋'),
 lesson('en06-pid-control',6,'pid-thermal-control','Inspect a bounded thermal PID simulation','检查有界热系统 PID 模拟','Simulate derivative-on-measurement control, actuator saturation and conditional integration, with an explicitly assumed plant.','在明确假定的对象模型中，模拟测量微分控制、执行器饱和及条件积分。',['models'],['pid_thermal_simulation'],'control','Control models','控制模型',discipline='engineering',data_kind='model',minutes=60,difficulty=3,icon='🎛️'),
]
for c in COURSES:
 c['online_url']='https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction' if 'energy' in c['snapshots'] else 'https://docs.scipy.org/doc/scipy/tutorial/linalg.html'
 c['data_note']=bilingual('The building record contains real ten-minute energy and environmental observations from one source building. Airport weather fields include upstream interpolation and are not colocated calibration references. Beam, circuit and PID examples are declared numerical design models; computed responses do not establish hardware performance or commissioning acceptance.','建筑记录包含来源中单栋建筑的真实十分钟能耗及环境观测。机场天气字段含来源插值，不是同位置校准参考。梁、电路和 PID 例子是明确的数值设计模型；计算响应不能证明硬件性能或实际验收。')

for c in COURSES[:3]:
 c['functions'].append('iso_datetimes');c['setup_imports']=c.get('setup_imports','')+'from datetime import datetime\n'

ENERGY_LOAD='''energy=snapshot("energy");frame=pd.DataFrame(energy["rows"],columns=energy["columns"])
frame["timestamp"]=frame["date"].astype(str);frame=frame.sort_values("timestamp").reset_index(drop=True)
assert len(frame)==19735 and frame.timestamp.is_unique
dates=iso_datetimes(frame.timestamp)
assert all((b-a).total_seconds()==600 for a,b in zip(dates,dates[1:]))
audit=audit_numeric_table(frame,["Appliances","lights","T1","RH_1"])
assert frame.Appliances.ge(0).all() and frame.lights.ge(0).all()
frame["appliance_average_power_W"]=frame.Appliances/(600/3600)
print("Observed rows:",len(frame),"; energy: Wh/10 min; derived interval-average power: W; source timezone unspecified")
display(frame[["timestamp","Appliances","appliance_average_power_W","T1","RH_1"]].head(8))'''
SECTIONS={}
SECTIONS[COURSES[0]['id']]=[
 step('Check temporal identity and declared units','检查时间身份及声明单位','The source records energy in Wh over ten-minute intervals, not instantaneous power. W=Wh/(10/60 h), so interval-average power is six times the numeric energy field. Timestamps are source-local and no unreported timezone conversion is applied.','来源记录十分钟内能量 Wh，不是瞬时功率。W=Wh/(10/60 h)，因此平均功率数值为能量字段的六倍。时间戳保留来源本地表示，不进行未声明时区转换。',ENERGY_LOAD),
 step('Inspect measured time patterns','检查实测时间模式','Show the first seven days of derived interval-average appliance power. This is a unit conversion of the measured energy, not a new high-rate electrical measurement. The trace cannot resolve mains voltage/current waveforms.','展示前七天从能量换算的区间平均家电功率。它是单位换算，不是新增高速电测量，不能解析电网电压/电流波形。','''part=frame.iloc[:7*144]
fig,ax=plt.subplots(figsize=(10,4));ax.plot(iso_datetimes(part.timestamp),part.appliance_average_power_W,lw=.8)
ax.set(xlabel="Source-local timestamp",ylabel="Interval-average appliance power (W)",title="Observed ten-minute energy converted to average power");plt.tight_layout();plt.show()''',cover=True),
 step('Compare diurnal distributions','比较日变化分布','Boxplots group observed interval energy by clock hour across the source period. They do not represent independent household replicates, and differences can mix behavior, weather and season. Keep the Wh/interval label distinct from the previous W plot.','按时钟小时分组展示区间能量分布。它们不是独立家庭重复；差异可能混合行为、天气和季节。保留 Wh/区间单位，与前图 W 区分。','''hour=np.array([value.hour for value in dates])
fig,ax=plt.subplots(figsize=(10,4));ax.boxplot([frame.loc[hour==h,"Appliances"] for h in range(24)],tick_labels=range(24),showfliers=False)
ax.set(xlabel="Source-local clock hour",ylabel="Energy (Wh per 10-minute interval)",title="Observed diurnal distributions; outlier markers hidden only in this drawing");plt.tight_layout();plt.show()'''),
 step('Read colocated environmental observations','解读环境观测','The kitchen temperature/humidity scatter is a measured association in one building. It does not calibrate the energy meter or identify a causal controller rule. Plot source humidity as percent, and temperature in degrees Celsius.','厨房温湿度散点描述单栋建筑中的测量关联，不能校准电能表，也不确定因果控制规则。湿度为百分比，温度为摄氏度。','''fig,ax=plt.subplots(figsize=(7,5));im=ax.scatter(frame.T1,frame.RH_1,c=frame.Appliances,s=5,alpha=.3,cmap="viridis")
ax.set(xlabel="Kitchen temperature (°C)",ylabel="Kitchen relative humidity (%)",title="Observed environmental association")
fig.colorbar(im,ax=ax,label="Appliance energy (Wh/interval)");plt.tight_layout();plt.show()'''),
 step('Reconcile energy totals and export the audit','核对能量总计并导出审计','Summing Wh observations gives energy over the observed intervals. Integrating interval-average W with the exact interval duration recovers the same total. Preserve timestamp cadence and original values in the export.','对 Wh 求和得到观测区间总能量。将平均 W 乘精确区间时长后求和，应恢复相同总量。导出保留时间间隔及原始值。','''total_Wh=float(frame.Appliances.sum());integrated_Wh=float((frame.appliance_average_power_W*(600/3600)).sum())
assert np.isclose(total_Wh,integrated_Wh)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
frame[["timestamp","Appliances","appliance_average_power_W","T1","RH_1"]].to_csv(OUTPUT_DIR/"observed-energy-audit.csv",index=False)
(OUTPUT_DIR/"units-and-cadence.json").write_text(json.dumps({"rows":len(frame),"interval_seconds":600,"original_energy_unit":"Wh per interval","derived_power_unit":"W interval average","total_observed_Wh":total_Wh,"timezone":"source unspecified; no conversion"},indent=2))
print("Energy reconciliation passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[1]['id']]=[
 step('Reserve a chronological test interval','保留按时间顺序的测试时段','Use the first 70% of timestamps for fitting and the final 30% for testing. A random row split would mix nearby and seasonally related observations. Target energy is Wh per interval, and this is conditional reconstruction using contemporaneous environmental variables.','前 70% 时间记录用于拟合，末 30% 用于测试。随机分行会混合临近及季节相关观测。目标为区间 Wh，并使用同时段环境变量进行条件回归。',ENERGY_LOAD+'''
split=int(.7*len(frame));train=np.arange(len(frame))<split;test=~train
frame["hour_sin"]=np.sin(2*np.pi*(np.array([value.hour+value.minute/60 for value in dates]))/24)
frame["hour_cos"]=np.cos(2*np.pi*(np.array([value.hour+value.minute/60 for value in dates]))/24)
features=["T1","RH_1","T_out","RH_out","hour_sin","hour_cos"]
assert frame.loc[train,"timestamp"].max()<frame.loc[test,"timestamp"].min()
print("Training/test rows:",int(train.sum()),int(test.sum()))'''),
 step('Fit training-only scaling and compare a baseline','仅用训练时段拟合缩放并比较基线','The random variables rv1/rv2 and other energy measurements are excluded. Ridge uses only training means/SDs. The mean baseline also uses the training target mean. Report held-out metrics even if the simple model performs poorly.','排除随机变量 rv1/rv2 及其他能量测量。岭回归缩放仅使用训练均值/标准差，均值基线也只用训练目标均值。简单模型即便表现较差，也应报告测试指标。','''model=ridge_fit_predict(frame.loc[train,features].to_numpy(),frame.loc[train,"Appliances"].to_numpy(),frame.loc[test,features].to_numpy(),penalty=10)
truth=frame.loc[test,"Appliances"].to_numpy(float);prediction=model["predictions"]
baseline=np.full(len(truth),frame.loc[train,"Appliances"].mean())
metrics=pd.DataFrame({"ridge":regression_metrics(truth,prediction),"training-mean":regression_metrics(truth,baseline)}).T;display(metrics)
fig,ax=plt.subplots(figsize=(7,5));ax.scatter(truth,prediction,s=5,alpha=.25)
limit=[min(truth.min(),prediction.min()),max(truth.max(),prediction.max())];ax.plot(limit,limit,"k--")
ax.set(xlabel="Observed Wh/interval",ylabel="Predicted Wh/interval",title="Chronological held-out conditional predictions");plt.tight_layout();plt.show()''',cover=True),
 step('Inspect time-dependent errors','检查时间相关误差','Plot a bounded first-week test interval; errors and target values share Wh/interval units. A limited feature set may miss occupancy and appliance events. The residual trace is not an independent-series confidence calculation.','展示测试期首周的有限窗口，误差和目标单位都是 Wh/区间。少量特征可能遗漏占用及设备事件；残差轨迹不是独立样本置信计算。','''timestamp=frame.loc[test,"timestamp"].to_numpy();residual=prediction-truth;count=min(7*144,len(truth))
fig,ax=plt.subplots(figsize=(10,4));ax.plot(iso_datetimes(timestamp[:count]),residual[:count],lw=.8)
ax.axhline(0,color="black",linestyle="--");ax.set(xlabel="Source-local test timestamp",ylabel="Prediction − observation (Wh/interval)",title="First test-week conditional errors");plt.tight_layout();plt.show()'''),
 step('Compare average errors by clock hour','按时钟小时比较平均误差','Group test absolute errors by source-local hour on the same dates for model and baseline. Error patterns can motivate a new prospective design, but do not retrospectively tune this held-out result and still call it untouched.','在相同测试日期按来源小时比较模型和基线绝对误差。模式可帮助设计新评估，不能在此测试结果上事后调参仍称其为未触碰测试。','''hours=np.array([value.hour for value in iso_datetimes(frame.loc[test,"timestamp"])])
hourly=pd.DataFrame({"hour":hours,"ridge":abs(residual),"training-mean":abs(baseline-truth)}).groupby("hour").mean()
fig,ax=plt.subplots(figsize=(9,4));hourly.plot(ax=ax,marker="o")
ax.set(xlabel="Source-local clock hour",ylabel="Held-out MAE (Wh/interval)",title="Common-date error stratification");plt.tight_layout();plt.show()'''),
 step('Reconcile predictors and export','核对预测信息边界并导出','Check training-only statistics and direct RMSE. Do not hide negative predictions by clipping. Export the time split, original target and both predictions, keeping the single-building observational limitation.','核对训练统计量及直接 RMSE，不以裁剪掩盖负预测。导出时间划分、原目标及两种预测，并保留单栋建筑的观测限制。','''assert np.allclose(model["mean"],frame.loc[train,features].mean())
assert np.isclose(metrics.loc["ridge","rmse"],np.sqrt(np.mean(residual**2)))
assert not {"Appliances","lights","rv1","rv2"}&set(features)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"timestamp":timestamp,"observed_Wh":truth,"ridge_Wh":prediction,"training_mean_Wh":baseline}).to_csv(OUTPUT_DIR/"held-out-energy.csv",index=False)
metrics.to_csv(OUTPUT_DIR/"metrics-Wh-per-interval.csv");hourly.to_csv(OUTPUT_DIR/"hourly-test-MAE.csv")
print("Prediction-boundary checks passed; negative model predictions:",int(np.sum(prediction<0)))''')]

SECTIONS[COURSES[2]['id']]=[
 step('Set the sampling scale in days','以日为单位设定采样尺度','Ten-minute observations give 144 samples/day and Nyquist 72 cycles/day. They cannot resolve 50/60 Hz mains waveforms. This workflow analyzes variation of interval-average energy/power on much slower time scales.','十分钟观测为每日 144 样本，Nyquist 为每日 72 周期，不能解析 50/60 Hz 电网波形。本课分析区间平均能量/功率的慢时间变化。',ENERGY_LOAD+'''
power=frame.appliance_average_power_W.to_numpy(float);sampling_per_day=144.0;cutoff_cycles_per_day=6.0
sos=butter(4,cutoff_cycles_per_day,btype="lowpass",fs=sampling_per_day,output="sos")
smoothed=sosfiltfilt(sos,power)
fig,ax=plt.subplots(figsize=(10,4));count=7*144
ax.plot(iso_datetimes(frame.timestamp.iloc[:count]),power[:count],label="Observed interval-average power",lw=.7,alpha=.7)
ax.plot(iso_datetimes(frame.timestamp.iloc[:count]),smoothed[:count],label="Acausal low-pass processing",lw=1.4)
ax.set(xlabel="Source-local time",ylabel="Average / processed power (W)",title="Measured source and offline processing");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Estimate the low-rate spectrum','估计低采样率频谱','With fs expressed as samples/day, Welch frequencies are cycles/day and density is W² per (cycles/day). A daily-pattern peak is a description of this source period, not evidence of high-rate electrical harmonics.','当 fs 采用样本/日，Welch 频率为周期/日，谱密度为 W² 每（周期/日）。日尺度峰描述此来源时段，不是高速电学谐波证据。','''frequency,psd=welch(power-power.mean(),fs=sampling_per_day,nperseg=7*144,noverlap=3*144)
positive=frequency>0
fig,ax=plt.subplots(figsize=(8,5));ax.loglog(frequency[positive],psd[positive])
ax.axvline(cutoff_cycles_per_day,color="red",linestyle="--",label="Declared cutoff")
ax.set(xlabel="Frequency (cycles/day)",ylabel="Power PSD (W² per cycles/day)",title="Welch density at the actual observation cadence");ax.legend();plt.tight_layout();plt.show()'''),
 step('Read the double-pass response','解读双次滤波响应','Forward/backward processing is acausal and squares the single-pass magnitude. It is useful for offline exploration, but cannot be deployed unchanged as a real-time controller filter. Boundaries and ringing can affect the processed series.','前后向处理非因果，幅度为单次响应幅度的平方。它可用于离线探索，但不能原样当作实时控制滤波器。边界及振铃可能影响处理结果。','''response_frequency,response=sosfreqz(sos,worN=2048,fs=sampling_per_day)
fig,ax=plt.subplots(figsize=(8,4));ax.plot(response_frequency,abs(response),label="Single pass")
ax.plot(response_frequency,abs(response)**2,label="Forward/backward magnitude")
ax.axvline(cutoff_cycles_per_day,color="gray",linestyle="--")
ax.set(xlabel="Frequency (cycles/day)",ylabel="Magnitude ratio",xlim=(0,20),title="Declared offline filter response");ax.legend();plt.tight_layout();plt.show()'''),
 step('Check FFT normalization and preserve original data','检查 FFT 归一化并保留原始数据','Use the full complex FFT for Parseval, avoiding an even/odd real-FFT endpoint mistake on 19735 observations. Keep measured and processed series separate and report any negative processed values without hiding them.','对 19735 个观测使用完整复数 FFT 核对 Parseval，避免实数 FFT 奇偶端点权重错误。分别保留测量与处理序列，并报告负处理值，不掩盖它们。','''centered=power-power.mean();transform=np.fft.fft(centered)
assert np.isclose(np.sum(abs(transform)**2)/len(power)**2,np.mean(centered**2),rtol=1e-12)
assert np.isfinite(smoothed).all() and np.all(psd>=0)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"timestamp":frame.timestamp,"observed_interval_average_W":power,"acausal_lowpass_W":smoothed}).to_csv(OUTPUT_DIR/"power-processing.csv",index=False)
pd.DataFrame({"cycles_per_day":frequency,"PSD_W_squared_per_cycles_per_day":psd}).to_csv(OUTPUT_DIR/"energy-spectrum.csv",index=False)
print("Cadence/FFT checks passed; negative processed values:",int(np.sum(smoothed<0)))''')]

SECTIONS[COURSES[3]['id']]=[
 step('Assemble material, geometry and boundary conditions','组装材料、几何及边界条件','Each Hermite beam node has transverse displacement (m) and rotation (rad). The clamp sets both root DOFs to zero. Nominal E and I are declared teaching parameters; the model assumes a slender, linear elastic beam and small displacement.','每个 Hermite 梁节点有横向位移 m 与转角 rad。固定端将根部两自由度置零。名义 E、I 为教学参数，模型假定细长线弹性梁及小挠度。','''p=snapshot("models")["beam"]
beam=cantilever_fem(10,p["length_m"],p["young_modulus_Pa"],p["second_moment_m4"],p["tip_force_N"])
dense=np.linspace(0,p["length_m"],501)
analytic=p["tip_force_N"]*dense**2*(3*p["length_m"]-dense)/(6*p["young_modulus_Pa"]*p["second_moment_m4"])
fig,ax=plt.subplots(figsize=(8,4));ax.plot(dense,1000*analytic,label="Closed tip-load solution")
ax.plot(beam["x"],1000*beam["displacement_m"],"o",label="Finite-element nodes")
ax.set(xlabel="Beam coordinate (m)",ylabel="Transverse deflection (mm)",title="Declared cantilever tip-load model");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Inspect the assembled connectivity','检查组装后的连接结构','The stiffness sparsity pattern reflects adjacent-element coupling before the clamp is removed. Because displacement and rotation DOFs have different units, a raw condition number depends on scaling and is not a material property.','固定端约束去除前的刚度稀疏模式反映相邻单元耦合。位移与转角自由度单位不同，原始条件数依赖缩放，不是材料性质。','''fig,ax=plt.subplots(figsize=(6,5));ax.spy(beam["stiffness"],markersize=3)
ax.set(xlabel="DOF column",ylabel="DOF row",title="Assembled beam stiffness connectivity");plt.tight_layout();plt.show()'''),
 step('Check meshes for this exactly represented load case','检查此可精确表示载荷的不同网格','The closed deflection is cubic, matching the Hermite basis, so nodal tip-load results are exact up to rounding even on a coarse mesh. This special case is a correctness benchmark, not proof that arbitrary loads, geometries or dynamic analyses need only one element.','闭式挠度为三次函数，匹配 Hermite 基，因此节点端载解即便粗网格也可在舍入精度内正确。这是特殊正确性基准，不能证明任意载荷、几何或动力问题只需一单元。','''records=[]
reference_tip=p["tip_force_N"]*p["length_m"]**3/(3*p["young_modulus_Pa"]*p["second_moment_m4"])
for count in [1,2,4,8,16]:
 trial=cantilever_fem(count,p["length_m"],p["young_modulus_Pa"],p["second_moment_m4"],p["tip_force_N"])
 records.append({"elements":count,"tip_deflection_m":trial["displacement_m"][-1],"reference_m":reference_tip,"relative_error":abs(trial["displacement_m"][-1]/reference_tip-1)})
mesh=pd.DataFrame(records);display(mesh)
fig,ax=plt.subplots(figsize=(7,4));ax.plot(mesh.elements,1000*mesh.tip_deflection_m,"o-")
ax.axhline(1000*reference_tip,color="gray",linestyle="--")
ax.set(xlabel="Elements",ylabel="Tip deflection (mm)",title="Special cubic benchmark across meshes");plt.tight_layout();plt.show()'''),
 step('Reconcile equilibrium reactions and export','核对平衡反力并导出','The root reaction force balances the tip force, and the root reaction moment balances F·L under the declared sign convention. Interior residuals should vanish. These are model-equilibrium checks, not load-test acceptance.','按声明符号约定，根部反力平衡端力，根部反力矩平衡 F·L，内部残差应为零。这是模型平衡检查，不是加载试验验收。','''assert np.allclose(beam["stiffness"],beam["stiffness"].T)
assert np.max(abs(beam["reaction"][2:]))<1e-6
assert np.isclose(beam["reaction"][0],-p["tip_force_N"],rtol=1e-8)
assert np.isclose(beam["reaction"][1],-p["tip_force_N"]*p["length_m"],rtol=1e-8)
assert mesh.relative_error.max()<1e-8
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"x_m":beam["x"],"deflection_m":beam["displacement_m"],"rotation_rad":beam["rotation_rad"]}).to_csv(OUTPUT_DIR/"beam-nodes.csv",index=False)
mesh.to_csv(OUTPUT_DIR/"cubic-benchmark-meshes.csv",index=False)
print("Assembly, reaction and closed-solution checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[4]['id']]=[
 step('Compare analytic and explicit transient responses','比较解析与显式暂态响应','Nominal tau=R·C in seconds. The explicit Euler step uses dt=tau/20, while the exact step response is Vin(1−exp(−t/tau)). These are model voltages, not oscilloscope measurements.','名义 tau=R·C，单位秒。显式 Euler 采用 dt=tau/20，解析阶跃为 Vin(1−exp(−t/tau))。这些是模型电压，不是示波器测量。','''models=snapshot("models");p=models["circuit"]
solution=rc_step_response(p["resistance_ohm"],p["capacitance_F"],p["input_voltage_V"])
fig,ax=plt.subplots(figsize=(8,4));ax.plot(solution["t"],solution["analytic_voltage"],label="Analytic")
ax.plot(solution["t"],solution["numerical_voltage"],"--",label="Explicit Euler")
ax.set(xlabel="Model time (s)",ylabel="Capacitor voltage (V)",title="RC step-response consistency");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Read gain and phase with Hz units','以 Hz 单位解读增益及相位','The transfer response is 1/(1+j2pi f RC); angular frequency is 2pi f. The cutoff has magnitude 1/sqrt(2), approximately −3.01 dB. Phase is displayed in degrees, and the source has no measured parasitic components.','传递响应为 1/(1+j2pi f RC)，角频率等于 2pi f。截止幅度为 1/sqrt(2)，约 −3.01 dB。相位使用度，模型未测量寄生元件。','''tau=solution["tau_s"];frequency=np.geomspace(.01,100,501);response=1/(1+1j*2*np.pi*frequency*tau)
cutoff=1/(2*np.pi*tau)
fig,axes=plt.subplots(1,2,figsize=(10,4));axes[0].semilogx(frequency,20*np.log10(abs(response)))
axes[0].axvline(cutoff,color="gray",linestyle="--");axes[0].set(xlabel="Frequency (Hz)",ylabel="Gain (dB)")
axes[1].semilogx(frequency,np.angle(response,deg=True));axes[1].set(xlabel="Frequency (Hz)",ylabel="Phase (degrees)")
plt.tight_layout();plt.show();print("Nominal tau (s):",tau,"; cutoff (Hz):",cutoff)'''),
 step('Keep tolerance bounds separate from probability assumptions','区分容差边界与概率假设','For this explicit Monte Carlo exercise, assume independent uniform ±5% distributions for R and C. Real tolerance specifications are bounds and do not prove such a distribution or independence. Plot the resulting simulated tau values, not measured batch statistics.','此 Monte Carlo 练习明确假设 R、C 独立均匀分布于 ±5%。真实容差规格是边界，不证明分布或独立性。图示模拟 tau，不是实测批次统计。','''rng=np.random.default_rng(models["seed"]);tolerance=p["tolerance_fraction"]
resistance=p["resistance_ohm"]*rng.uniform(1-tolerance,1+tolerance,5000)
capacitance=p["capacitance_F"]*rng.uniform(1-tolerance,1+tolerance,5000);drawn_tau=resistance*capacitance
fig,ax=plt.subplots(figsize=(8,4));ax.hist(drawn_tau,bins=35,edgecolor="white");ax.axvline(tau,color="black",linestyle="--")
ax.set(xlabel="Simulated time constant (s)",ylabel="Declared independent draws",title="Tolerance-propagation model");plt.tight_layout();plt.show()'''),
 step('Check limits and export units/assumptions','检查极限并导出单位和假设','Verify the one-time-constant analytic voltage, cutoff magnitude and tolerance bounds. Save all model inputs and the assumed distribution. Numerical error and simulated component variation remain different quantities.','核对一时间常数的解析电压、截止幅度及容差范围。保存全部输入和假定分布；数值误差与模拟元件变异是不同量。','''index=int(np.argmin(abs(solution["t"]-tau)))
assert np.isclose(solution["analytic_voltage"][index],p["input_voltage_V"]*(1-np.exp(-1)))
assert np.isclose(abs(1/(1+1j*2*np.pi*cutoff*tau)),1/np.sqrt(2))
assert drawn_tau.min()>=tau*(1-tolerance)**2 and drawn_tau.max()<=tau*(1+tolerance)**2
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"time_s":solution["t"],"analytic_voltage_V":solution["analytic_voltage"],"Euler_voltage_V":solution["numerical_voltage"]}).to_csv(OUTPUT_DIR/"rc-transient.csv",index=False)
pd.DataFrame({"frequency_Hz":frequency,"gain_dB":20*np.log10(abs(response)),"phase_degrees":np.angle(response,deg=True)}).to_csv(OUTPUT_DIR/"rc-frequency-response.csv",index=False)
(OUTPUT_DIR/"tolerance-assumptions.json").write_text(json.dumps({**p,"seed":models["seed"],"distribution":"independent uniform tolerance ranges; assumed, not inferred"},indent=2))
print("Circuit reference and bound checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[5]['id']]=[
 step('Declare the plant and controller units','声明对象及控制器单位','The assumed thermal plant relaxes toward ambient+gain·heater duty plus a declared disturbance. Heater duty is limited to 0–100%. Kp is %/°C, Ki %/(°C·s), Kd %·s/°C. Derivative is taken on the measured temperature, not on a step change of reference.','假定热对象向环境温度+增益·加热占空比+声明扰动松弛。加热限制在 0–100%。Kp 为 %/°C，Ki 为 %/(°C·s)，Kd 为 %·s/°C；微分作用于测量温度，不作用于参考阶跃。','''p=snapshot("models")["pid"]
arguments=dict(Kp=4,Ki=.2,Kd=6,tau_s=p["time_constant_s"],gain_degC_per_percent=p["plant_gain_degC_per_percent"],setpoint_degC=p["setpoint_degC"],ambient_degC=p["ambient_degC"],dt_s=p["step_s"],duration_s=p["duration_s"])
controlled=pid_thermal_simulation(**arguments,antiwindup=True)
unprotected=pid_thermal_simulation(**arguments,antiwindup=False)
fig,ax=plt.subplots(figsize=(9,4));ax.plot(controlled["t"],controlled["temperature_degC"],label="Conditional integration")
ax.plot(unprotected["t"],unprotected["temperature_degC"],label="No anti-windup")
ax.axhline(p["setpoint_degC"],color="black",linestyle="--",label="Declared setpoint");ax.axvline(300,color="gray",linestyle=":")
ax.set(xlabel="Model time (s)",ylabel="Model temperature (°C)",title="Bounded thermal control; equilibrium disturbance at 300 s");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Compare requested and applied control','比较请求与实际施加控制','The unclamped controller request can exceed actuator limits, while applied duty is bounded. This is an intentionally simulated actuator, not an instruction to control real hardware. Saturation is part of the declared model rather than a value to hide.','未限幅请求可超过执行器范围，而施加占空比有界。这是模拟执行器，不指令真实硬件。饱和属于声明模型，应展示而非隐藏。','''fig,ax=plt.subplots(figsize=(9,4));ax.plot(controlled["t"],controlled["unclamped_percent"],label="Requested duty")
ax.plot(controlled["t"],controlled["control_percent"],label="Applied duty")
ax.axhline(100,color="gray",linestyle="--");ax.axhline(0,color="gray",linestyle="--")
ax.set(xlabel="Model time (s)",ylabel="Heater duty (%)",title="Explicit actuator saturation");ax.legend();plt.tight_layout();plt.show()'''),
 step('Inspect the integral state','检查积分状态','Conditional integration holds the integrator when an already saturated request and error would push farther into saturation. The integral contribution is a controller state in duty units; it is not temperature or physical stored heat.','当已饱和请求和误差会继续加深饱和时，条件积分保持积分器状态。积分贡献单位为占空比，是控制器状态，不是温度或储存热量。','''fig,ax=plt.subplots(figsize=(9,4));ax.plot(controlled["t"],controlled["integral_percent"],label="Conditional integration")
ax.plot(unprotected["t"],unprotected["integral_percent"],label="No anti-windup")
ax.set(xlabel="Model time (s)",ylabel="Integral contribution (%)",title="Integrator behavior under the same plant model");ax.legend();plt.tight_layout();plt.show()'''),
 step('Reconcile bounded outputs and export a model audit','核对有界输出并导出模型审计','Check finite states and actuator bounds, then report integral absolute error in °C·s. Model gains, numerical step and disturbance must accompany the trace. Passing this simulation is not hardware validation or a universal controller tuning rule.','检查有限状态及执行器边界，并报告 °C·s 的绝对误差积分。模型增益、数值步长及扰动随轨迹保存。模拟通过不等于硬件验证，也不产生普适调参规则。','''assert np.isfinite(controlled["temperature_degC"]).all()
assert np.all((controlled["control_percent"]>=0)&(controlled["control_percent"]<=100))
error_integral=float(np.trapezoid(abs(controlled["error_degC"]),controlled["t"]))
assert np.max(controlled["unclamped_percent"])>100
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"time_s":controlled["t"],"temperature_degC":controlled["temperature_degC"],"applied_duty_percent":controlled["control_percent"],"requested_duty_percent":controlled["unclamped_percent"],"integral_percent":controlled["integral_percent"],"error_degC":controlled["error_degC"]}).to_csv(OUTPUT_DIR/"thermal-controller-simulation.csv",index=False)
(OUTPUT_DIR/"declared-control-model.json").write_text(json.dumps({**arguments,"antiwindup":"conditional integration","disturbance_start_s":300,"disturbance_equilibrium_offset_degC":-10,"integral_absolute_error_degC_s":error_integral,"hardware_validation":False},indent=2))
print("Bounded-control checks passed; simulated IAE (°C·s):",error_integral)''')]

EXERCISES={}
notes=[
 (['Convert 100 Wh per ten minutes to interval-average W.','Why are repeated time observations not independent buildings?','The average is 600 W. The record follows one building through time, so household generalization and observation independence require additional design evidence.','Using NumPy/Pandas/Matplotlib, add a daily observed-energy total with complete-interval counts.','With the same packages, compare kitchen and living-room temperatures without calling either an instrument calibration reference.','Cadence remains ten minutes, original Wh data is preserved and every derived power/energy unit is explicit.'],['将十分钟 100 Wh 换为区间平均 W。','为何连续观测不代表独立建筑？','区间平均为 600 W。记录跟踪同一栋建筑，家庭推广和观测独立性需要额外设计证据。','仅用 NumPy、Pandas、Matplotlib 增加日观测能量总计及完整区间数量。','使用同样的包比较厨房与客厅温度，不将任一方称为仪器校准参考。','间隔仍为十分钟，保留原 Wh 数据，派生功率/能量单位明确。']),
 (['Why prefer chronological over random-row holdout here?','Why distinguish conditional regression from forecasting?','Nearby seasonal observations can leak information across random splits. Contemporaneous environmental values are known for reconstruction, not necessarily for future predictions.','Using NumPy/Pandas/Matplotlib, add a training-only clock-hour mean baseline and evaluate on the same test timestamps.','With the same packages, report error separately for high and low observed energy while keeping the original fitted model unchanged.','No test values enter scaling or fitting; all methods share dates and Wh/interval units.'],['为何本例优先使用时间划分？','为何区分条件回归与预测？','临近季节观测可能在随机划分间泄漏信息。同时段环境值可供条件回归使用，但未来预测未必可知。','仅用 NumPy、Pandas、Matplotlib 增加仅训练数据的时钟小时均值基线，在同测试日期评估。','使用同样的包按观测高/低能耗分层报告误差，保持原拟合模型不变。','测试值不参与缩放或拟合，各方法使用同日期和 Wh/区间单位。']),
 (['What is the Nyquist limit in cycles/day?','Why square the single-pass magnitude?','It is 72 cycles/day at 144 samples/day. Forward/backward filtering composes two passes and is acausal; its magnitude is the square of the one-pass magnitude.','Using NumPy/SciPy/Matplotlib, compare 3 and 6 cycles/day cutoffs without changing cadence labels.','With the same packages, plot first/last-week boundary behavior and preserve processed versus measured values.','FFT normalization passes for the odd observation count, spectra have stated units and filtering is labelled offline/acausal.'],['以周期/日计的 Nyquist 上限是多少？','为何单次幅度需要平方？','每日 144 样本对应 72 周期/日。前后向处理叠加两次滤波且非因果，幅度为单次平方。','仅用 NumPy、SciPy、Matplotlib 比较每日三与六周期截止，保持采样尺度标签。','使用同样的包画首末周边界行为，分别保留测量与处理值。','奇数观测下 FFT 归一化通过，频谱单位明确，滤波标为离线/非因果。']),
 (['Why does the cubic tip-load benchmark look mesh-independent?','Why are displacement and rotation DOFs not interchangeable?','Hermite elements represent the cubic closed displacement for this special load case. Displacement is in m and rotation in rad; the stiffness couples different physical quantities.','Using NumPy/Matplotlib, add the analytical rotation curve and compare with all nodal rotations.','Using the same packages, vary E and I separately and check inverse-stiffness scaling while retaining force/moment equilibrium.','Clamped DOFs remain zero, reactions balance F and F·L and nodal references match within numerical tolerance.'],['为何三次端载基准看似不依赖网格？','位移与转角自由度为何不可互换？','该特殊载荷的闭式挠度为三次，Hermite 单元可表示。位移单位 m、转角 rad，刚度耦合不同物理量。','仅用 NumPy、Matplotlib 增加解析转角，并比较全部节点转角。','使用同样的包分别改变 E、I，检查逆刚度缩放，保留力/力矩平衡。','固定端自由度为零，反力平衡 F 与 F·L，节点参考在数值容差内一致。']),
 (['Explain units of RC and the cutoff.','Why is a tolerance bound not a probability distribution?','RC is seconds and 1/(2pi RC) is Hz. A manufacturing bound alone does not establish uniformity, independence or an empirical interval.','Using NumPy/Matplotlib, compare 10, 20 and 80 Euler steps per tau and show actual errors against the analytic response.','With the same packages, compare independent-uniform with a clearly labelled correlated tolerance simulation.','Analytic limits, −3 dB cutoff and units reconcile; all simulated distribution assumptions are saved.'],['解释 RC 及截止频率的单位。','为何容差边界不是概率分布？','RC 的单位为秒，1/(2pi RC) 为 Hz。制造边界本身不证明均匀性、独立性或经验区间。','仅用 NumPy、Matplotlib 比较每 tau 十、二十、八十步，画相对解析解的实际误差。','使用同样的包比较独立均匀与明确标记的相关容差模拟。','解析极限、−3 dB 截止及单位一致，保存所有模拟分布假设。']),
 (['Explain derivative-on-measurement units.','What does anti-windup prevent in this declared model?','The derivative term uses temperature rate and Kd to produce duty units. Conditional integration prevents an integral state from pushing farther into actuator saturation; it does not prove hardware suitability.','Using NumPy/Pandas/Matplotlib, compare two declared Ki values with identical plant and actuator limits.','With the same packages, reduce maximum duty and explain whether the disturbed setpoint is achievable under the model.','Applied duty stays within limits, states remain finite and plant/controller/time-step assumptions accompany every result.'],['解释测量微分项的单位。','抗积分饱和在此声明模型中防止什么？','温度变化率乘 Kd 得到占空比单位。条件积分防止积分状态继续推向执行器饱和，不证明硬件适用。','仅用 NumPy、Pandas、Matplotlib 在相同对象和限制下比较两个声明 Ki。','使用同样的包降低最大占空比，并解释扰动下设定值在模型中是否可达。','施加占空比有界，状态有限，每项结果随同对象/控制器/步长假设。'])]
for c,(en,zh) in zip(COURSES,notes):EXERCISES[c['id']]=exercises(en,zh)
