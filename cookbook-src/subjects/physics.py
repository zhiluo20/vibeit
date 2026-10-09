"""Physical models plus one genuine detector-data workflow, all explicitly labelled."""
from ._common import lesson,step,exercises,bilingual

BASE=['numpy','pandas','scipy','matplotlib','IPython']
COURSES=[
 lesson('ph01-pendulum',1,'nonlinear-pendulum','Compare nonlinear and small-angle pendulums','比较非线性与小角度单摆','Integrate a declared ideal model, estimate periods from crossings and audit energy conservation.','积分明确声明的理想模型，从过零点估计周期，并审计能量守恒。',['models','constants'],['pendulum_solution'],'mechanics','Mechanics','力学',discipline='physics',data_kind='model',icon='🕰️',setup_imports='from scipy.integrate import solve_ivp\n',packages=BASE),
 lesson('ph02-oscillator',2,'damping-resonance','Inspect damping and forced resonance','检查阻尼与受迫共振','Connect free decay, steady frequency response and time-domain integration with dimensional parameters.','通过有量纲参数连接自由衰减、稳态频率响应及时间积分。',['models'],['oscillator_solution'],'mechanics','Mechanics','力学',discipline='physics',data_kind='model',icon='〰️',setup_imports='from scipy.integrate import solve_ivp\n',packages=BASE),
 lesson('ph03-projectile',3,'projectile-drag','Integrate a projectile with quadratic drag','积分具有二次阻力的抛体','Stop at a ground event, compare a vacuum reference and reconcile mechanical-energy loss with drag work.','在落地事件处停止，与真空参考比较，并用阻力功核对机械能损失。',['models','constants'],['projectile_with_drag'],'mechanics','Mechanics','力学',discipline='physics',data_kind='model',icon='🏹',setup_imports='from scipy.integrate import solve_ivp\n',packages=BASE),
 lesson('ph04-heat',4,'heat-equation','Check a heat-diffusion solver','核对热扩散求解器','Enforce the explicit stability limit, compare a known sine-mode solution and measure grid convergence.','执行显式稳定性约束，与已知正弦模态解比较，并测量网格收敛。',['models'],['heat_diffusion_explicit'],'fields','Fields & transport','场与输运',discipline='physics',data_kind='model',icon='🌡️',packages=BASE),
 lesson('ph05-gw150914',5,'gw150914-signal','Inspect real GW150914 detector strain','检查真实 GW150914 探测器应变','Audit a frozen Hanford record, estimate a spectrum and inspect a declared zero-phase band-pass without claiming a new detection.','审计冻结的 Hanford 记录，估计频谱，并检查指定零相位带通，不将其作为新的探测结论。',['gw150914'],[],'signals','Signals & spectra','信号与频谱',discipline='physics',data_kind='measured',minutes=60,difficulty=3,icon='🌠',setup_imports='from scipy.signal import welch, butter, sosfiltfilt\n',packages=BASE),
 lesson('ph06-blackbody',6,'blackbody-radiation','Reconcile Planck, Wien and Stefan–Boltzmann laws','核对普朗克、维恩与斯忒藩—玻尔兹曼定律','Compute spectral radiance from frozen SI constants, locate wavelength peaks and verify integrated exitance.','从冻结 SI 常数计算光谱辐亮度，定位波长谱峰，并核对积分辐射出射度。',['constants'],['planck_radiance'],'signals','Signals & spectra','信号与频谱',discipline='physics',data_kind='reference',minutes=60,icon='☀️',setup_imports='from scipy.optimize import minimize_scalar\nfrom scipy.integrate import quad\n',packages=BASE),
]
for c in COURSES:
 c['online_url']='https://gwosc.org/eventapi/json/GWTC-1-confident/GW150914/v3/' if 'gw150914' in c['snapshots'] else 'https://physics.nist.gov/cuu/Constants/' if 'constants' in c['snapshots'] else 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html'
 c['data_note']=bilingual('Pendulum, oscillator, projectile and heat trajectories are declared numerical models, not laboratory measurements. The gravitational acceleration is the conventional standard g0 when used. GW150914 uses actual frozen detector strain and published event timing; a filtered curve is not an independent significance or source-parameter analysis. Blackbody curves assume an ideal emitter.','单摆、振子、抛体和温度轨迹是明确声明的数值模型，不是实验室测量。使用的 g0 为约定标准重力加速度。GW150914 使用真实冻结应变和已发表事件时间；滤波曲线不是独立的显著性或源参数分析。黑体曲线假定理想辐射体。')

SECTIONS={}
SECTIONS[COURSES[0]['id']]=[
 step('Set units and compare three initial angles','设定单位并比较三个初始角度','Use a one-metre pendulum and conventional g0. The solver state is angle in radians and angular velocity in rad/s. Small-angle motion uses sin(theta)≈theta; its period does not depend on initial amplitude.','取一米摆长及标准 g0。求解器状态为弧度角度和 rad/s 角速度。小角度近似使用 sin(theta)≈theta，其周期不依赖初始振幅。','''parameters=snapshot("models")["pendulum"];gravity=snapshot("constants")["constants"]["g_0"]["value"]
length=parameters["length_m"];angles=parameters["angles_deg"]
solutions={angle:pendulum_solution(length,gravity,angle,parameters["duration_s"]) for angle in angles}
linear_period=2*np.pi*np.sqrt(length/gravity)
print("Length (m):",length,"; standard g0 (m/s²):",gravity,"; small-angle period (s):",linear_period)
fig,ax=plt.subplots(figsize=(9,4));large=solutions[90]
ax.plot(large["t"],np.rad2deg(large["theta"]),label="Nonlinear 90° initial angle")
ax.plot(large["t"],90*np.cos(np.sqrt(gravity/length)*large["t"]),"--",label="Small-angle approximation")
ax.set(xlabel="Model time (s)",ylabel="Angle (degrees)",title="Amplitude changes the nonlinear timing");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Estimate periods from actual zero crossings','由实际过零点估计周期','Use repeated downward zero crossings with linear interpolation between saved samples. These period estimates have interpolation and solver error, and require enough simulated cycles. Their difference from the linear period concerns model approximation.','对保存样本之间的重复向下过零点做线性插值。周期估计包含插值与求解误差，也需要足够周期。与线性周期的差别描述模型近似误差。','''periods=np.array([solutions[a]["period_s"] for a in angles])
display(pd.DataFrame({"initial_angle_deg":angles,"nonlinear_period_s":periods,"small_angle_period_s":linear_period,"relative_difference":periods/linear_period-1}))
fig,ax=plt.subplots(figsize=(7,4));ax.plot(angles,periods,"o-",label="Zero-crossing estimate")
ax.axhline(linear_period,color="gray",linestyle="--",label="Small-angle prediction")
ax.set(xlabel="Initial angle magnitude (degrees)",ylabel="Period (s)",title="Nonlinear period depends on amplitude");ax.legend();plt.tight_layout();plt.show()'''),
 step('Audit conserved energy per unit mass','审计单位质量的守恒能量','Energy per unit mass is ½L²ω²+gL(1−cos(theta)) in J/kg. Plot relative drift from the initial value. Ideal-model energy is conserved; the plotted small nonzero changes quantify the numerical integration, not real friction.','单位质量能量为 ½L²ω²+gL(1−cos(theta))，单位 J/kg。图上展示相对初值的漂移。理想模型能量守恒，微小变化描述数值积分，而不是真实摩擦。','''fig,ax=plt.subplots(figsize=(9,4))
for angle,solution in solutions.items():
 energy=solution["energy_per_mass"];ax.plot(solution["t"],(energy-energy[0])/energy[0],label=f"{angle}°")
ax.set(xlabel="Model time (s)",ylabel="Relative energy drift",title="Numerical energy audit");ax.legend();plt.tight_layout();plt.show()'''),
 step('Check the limiting model and export','检查极限模型并导出','The five-degree solution should closely approach the small-angle period. Higher initial angles give longer periods in this ideal regime. Verify finite state values and tight energy drift before transferring the algorithm to a different physical system.','五度解应接近小角度周期。在此理想范围内，更大角度具有更长周期。转用于其他系统之前，检查有限状态值与能量漂移。','''assert abs(periods[0]/linear_period-1)<.002 and np.all(np.diff(periods)>0)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
for angle,solution in solutions.items():
 energy=solution["energy_per_mass"];assert np.max(np.abs((energy-energy[0])/energy[0]))<1e-6
 pd.DataFrame({"time_s":solution["t"],"angle_rad":solution["theta"],"angular_velocity_rad_per_s":solution["omega"],"energy_J_per_kg":energy}).to_csv(OUTPUT_DIR/f"pendulum-{angle}-degrees.csv",index=False)
print("Limiting-period and energy checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[1]['id']]=[
 step('Declare the linear oscillator','声明线性振子','The equation is m x″+c x′+k x=F cos(omega t). Mass is kg, stiffness N/m and damping N·s/m. First inspect free decay from a one-metre initial displacement; the example is a teaching model rather than a measured apparatus.','方程为 m x″+c x′+k x=F cos(omega t)。质量 kg、刚度 N/m、阻尼 N·s/m。先检查从一米初始位移开始的自由衰减；该例是教学模型，不是装置实测。','''p=snapshot("models")["oscillator"];mass=p["mass_kg"];stiffness=p["stiffness_N_per_m"];dampings=p["damping_N_s_per_m"]
natural=np.sqrt(stiffness/mass)
fig,ax=plt.subplots(figsize=(9,4))
for damping in dampings:
 solution=oscillator_solution(mass,stiffness,damping)
 ax.plot(solution["t"],solution["x"],label=f"c={damping} N·s/m")
ax.set(xlabel="Time (s)",ylabel="Displacement (m)",title="Free damped motion");ax.legend();plt.tight_layout();plt.show()'''),
 step('Read the steady frequency response','解读稳态频率响应','For positive damping, amplitude is F/sqrt((k−m omega²)²+(c omega)²). The horizontal coordinate is angular frequency in rad/s, not Hz. The damped amplitude maximum need not equal the undamped natural frequency.','正阻尼下振幅为 F/sqrt((k−m omega²)²+(c omega)²)。横轴为 rad/s 角频率，不是 Hz。阻尼后的振幅峰不一定等于无阻尼固有频率。','''frequencies=np.linspace(.1,8,501);force=p["force_N"]
fig,ax=plt.subplots(figsize=(8,4))
for damping in dampings:
 amplitude=force/np.sqrt((stiffness-mass*frequencies**2)**2+(damping*frequencies)**2)
 ax.plot(frequencies,amplitude,label=f"c={damping}")
ax.axvline(natural,color="gray",linestyle="--",label="Undamped natural omega")
ax.set(xlabel="Drive angular frequency (rad/s)",ylabel="Steady displacement amplitude (m)",title="Damping changes peak location and width");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Check one forced trajectory against the analytic response','将受迫轨迹与解析响应核对','Integrate zero initial state long enough for transients to decay. The late trajectory should match a sinusoid with the analytic amplitude and phase. Comparing the initial transient to a steady-state formula would be an invalid check.','从零初始状态积分足够长时间，使瞬态衰减。后期轨迹应与解析振幅和相位的正弦波匹配。不能将初期瞬态直接与稳态公式比较。','''damping=1.6;drive=natural
forced=oscillator_solution(mass,stiffness,damping,force,drive,duration_s=80,initial_displacement=0,samples=8001)
amplitude=force/np.sqrt((stiffness-mass*drive**2)**2+(damping*drive)**2)
phase=np.arctan2(damping*drive,stiffness-mass*drive**2)
expected=amplitude*np.cos(drive*forced["t"]-phase);late=forced["t"]>70
fig,ax=plt.subplots(figsize=(9,4));ax.plot(forced["t"][late],forced["x"][late],label="ODE integration")
ax.plot(forced["t"][late],expected[late],"--",label="Analytic steady state")
ax.set(xlabel="Late model time (s)",ylabel="Displacement (m)",title="Time/frequency-domain consistency");ax.legend();plt.tight_layout();plt.show()'''),
 step('Reconcile and export the declared model','核对并导出声明模型','Verify late-time amplitude/phase agreement with a separate closed expression. Keep natural angular frequency, damping units and solver tolerances with the exported trace. No fitted laboratory parameters are claimed.','使用独立闭式表达式核对后期振幅和相位。导出时保留固有角频率、阻尼单位及求解容差；本课不声称得到实验装置参数。','''assert np.max(np.abs(forced["x"][late]-expected[late]))<1e-6
assert np.isclose(natural,4.0)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"time_s":forced["t"],"ODE_displacement_m":forced["x"],"steady_displacement_m":expected}).to_csv(OUTPUT_DIR/"forced-oscillation.csv",index=False)
(OUTPUT_DIR/"parameters.json").write_text(json.dumps({"mass_kg":mass,"stiffness_N_per_m":stiffness,"damping_N_s_per_m":damping,"force_N":force,"drive_rad_per_s":drive,"natural_rad_per_s":natural},indent=2))
print("Steady-state cross-check passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[2]['id']]=[
 step('Specify the force model and ground event','设定力模型及落地事件','Use constant air density and drag coefficient for a spherical cross-section. This omits wind, spin and speed-dependent coefficients. The event stops at the descending z=0 crossing; integration beyond impact would not describe flight.','使用恒定空气密度、阻力系数及球形迎风截面，省略风、旋转及速度相关系数。事件在下降的 z=0 过零处停止，撞击后的积分不再属于飞行轨迹。','''p=snapshot("models")["projectile"];gravity=snapshot("constants")["constants"]["g_0"]["value"]
arguments=dict(mass=p["mass_kg"],diameter=p["diameter_m"],air_density=p["air_density_kg_per_m3"],speed=p["speed_m_per_s"],angle_deg=p["angle_deg"],gravity=gravity,height_m=1.5)
drag=projectile_with_drag(**arguments,drag_coefficient=p["drag_coefficient"])
vacuum=projectile_with_drag(**arguments,drag_coefficient=0)
fig,ax=plt.subplots(figsize=(8,4));ax.plot(drag["state"][0],drag["state"][1],label="Quadratic drag")
ax.plot(vacuum["state"][0],vacuum["state"][1],"--",label="Vacuum")
ax.set(xlabel="Horizontal displacement (m)",ylabel="Height (m)",title="Declared flight model until first descending impact");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Inspect flight speed and timing','检查速度与飞行时间','Speed is sqrt(vx²+vz²) in m/s. The two traces end at their own impact times; do not align them by pretending their durations are equal. Drag changes both the trajectory and the time of flight in this example.','速率为 sqrt(vx²+vz²)，单位 m/s。两条曲线在各自撞击时间结束，不能假定持续时间相等而强行对齐。此例中的阻力同时影响轨迹和飞行时间。','''fig,ax=plt.subplots(figsize=(8,4))
for name,solution in [("Drag",drag),("Vacuum",vacuum)]:ax.plot(solution["t"],np.hypot(solution["state"][2],solution["state"][3]),label=name)
ax.set(xlabel="Flight time (s)",ylabel="Speed (m/s)",title="Speed before impact");ax.legend();plt.tight_layout();plt.show()
display(pd.DataFrame({"model":["drag","vacuum"],"flight_s":[drag["flight_s"],vacuum["flight_s"]],"range_m":[drag["range_m"],vacuum["range_m"]]}))'''),
 step('Reconcile drag work with mechanical-energy loss','用阻力功核对机械能损失','Mechanical energy is ½mv²+mgz in joules. Drag power is negative and measured in watts. Integrating that power over time should recover the energy change to discretization accuracy. This is a conservation audit within the declared model, not an experimental drag measurement.','机械能为 ½mv²+mgz，单位焦耳。阻力功率为负，单位瓦。对功率做时间积分，应在离散精度内恢复能量变化。这是声明模型中的守恒审计，不是阻力实测。','''energy_change=drag["energy_J"]-drag["energy_J"][0]
widths=np.diff(drag["t"]);power=drag["drag_power_W"]
work=np.r_[0,np.cumsum(widths*(power[:-1]+power[1:])/2)]
fig,ax=plt.subplots(figsize=(8,4));ax.plot(drag["t"],energy_change,label="Mechanical-energy change")
ax.plot(drag["t"],work,"--",label="Integrated drag work")
ax.set(xlabel="Flight time (s)",ylabel="Energy change / work (J)",title="Energy balance of the dissipative model");ax.legend();plt.tight_layout();plt.show()'''),
 step('Check the vacuum limit and export','检查真空极限并导出','The zero-drag reference has an analytic flight time and range, including the nonzero launch height. Check the final ground height and energy balance before interpreting drag differences.','零阻力参考具有解析飞行时间和射程，应包含非零发射高度。解释阻力差异之前，检查最终落地高度和能量平衡。','''angle=np.deg2rad(arguments["angle_deg"]);vx=arguments["speed"]*np.cos(angle);vz=arguments["speed"]*np.sin(angle)
expected_time=(vz+np.sqrt(vz*vz+2*gravity*arguments["height_m"]))/gravity
assert np.isclose(vacuum["flight_s"],expected_time,rtol=1e-8)
assert np.isclose(vacuum["range_m"],vx*expected_time,rtol=1e-8)
assert abs(drag["state"][1,-1])<1e-8 and np.all(np.diff(drag["energy_J"])<=1e-5)
assert np.isclose(energy_change[-1],work[-1],rtol=.002)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"time_s":drag["t"],"x_m":drag["state"][0],"z_m":drag["state"][1],"vx_m_per_s":drag["state"][2],"vz_m_per_s":drag["state"][3],"mechanical_energy_J":drag["energy_J"],"drag_power_W":power}).to_csv(OUTPUT_DIR/"drag-flight.csv",index=False)
print("Ground event, analytic vacuum and work checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[3]['id']]=[
 step('Respect the explicit stability limit','遵守显式稳定性上限','For FTCS, r=alpha·dt/dx² must not exceed 0.5 in one dimension. End temperatures are fixed at the ambient value. The initial sine profile has a closed solution and provides a meaningful solver reference.','一维 FTCS 的 r=alpha·dt/dx² 不得超过 0.5。两端温度固定为环境温度。初始正弦分布具有闭式解，可作为求解器的有效参考。','''p=snapshot("models")["heat"]
solution=heat_diffusion_explicit(51,p["length_m"],p["diffusivity_m2_per_s"],600,.4,p["ambient_degC"],p["amplitude_degC"])
print("Actual dx (m):",solution["spacing_m"],"; dt (s):",solution["step_s"],"; r:",solution["ratio"])
fig,ax=plt.subplots(figsize=(8,4))
for time in [0,150,300,600]:
 index=int(np.argmin(abs(solution["t"]-time)));ax.plot(solution["x"],solution["temperature"][index],label=f"t={solution['t'][index]:.1f} s")
ax.set(xlabel="Position (m)",ylabel="Model temperature (°C)",title="Fixed-temperature ends and diffusing sine profile");ax.legend();plt.tight_layout();plt.show()'''),
 step('View the computed temperature field','观察计算温度场','Color is temperature in °C; the horizontal coordinate is metres and vertical coordinate is seconds. Cooling occurs because fixed end reservoirs remove heat. An isolated-system energy-conservation claim would use different boundary conditions.','颜色表示 °C 温度，横轴为米，纵轴为秒。冷却来自固定端点热库带走热量；孤立系统的能量守恒需要不同边界条件。','''fig,ax=plt.subplots(figsize=(8,5));im=ax.pcolormesh(solution["x"],solution["t"],solution["temperature"],shading="auto",cmap="inferno")
ax.set(xlabel="Position (m)",ylabel="Model time (s)",title="Explicit heat-equation solution");fig.colorbar(im,ax=ax,label="Temperature (°C)");plt.tight_layout();plt.show()''',cover=True),
 step('Measure joint space/time grid convergence','测量时空网格联合收敛','Keep r fixed while refining x, which also refines dt. Compare the final profile with T0+A sin(pi x/L) exp(−alpha(pi/L)²t). This controlled model benchmark measures numerical error, not material-property uncertainty.','保持 r 不变细化 x，dt 也随之细化。将末时分布与 T0+A sin(pi x/L) exp(−alpha(pi/L)²t) 比较。这是受控模型数值误差基准，不是材料参数不确定性。','''nodes=[21,41,81,161];records=[]
for count in nodes:
 trial=heat_diffusion_explicit(count,p["length_m"],p["diffusivity_m2_per_s"],600,.4,p["ambient_degC"],p["amplitude_degC"])
 exact=p["ambient_degC"]+p["amplitude_degC"]*np.sin(np.pi*trial["x"]/p["length_m"])*np.exp(-p["diffusivity_m2_per_s"]*(np.pi/p["length_m"])**2*600)
 records.append({"nodes":count,"dx_m":trial["spacing_m"],"dt_s":trial["step_s"],"max_error_degC":float(np.max(abs(trial["temperature"][-1]-exact)))})
convergence=pd.DataFrame(records)
fig,ax=plt.subplots(figsize=(7,4));ax.loglog(convergence.dx_m,convergence.max_error_degC,"o-")
ax.set(xlabel="Spatial spacing (m)",ylabel="Maximum final error (°C)",title="Known-solution grid audit");plt.tight_layout();plt.show()'''),
 step('Test invalid stability settings and export','测试非法稳定性设置并导出','The implementation rejects r>0.5. Check fixed ends, bounded temperatures and decreasing refinement error. Record both requested r and actual dt so rounding the number of steps does not hide the actual scheme.','实现拒绝 r>0.5。检查固定端点、温度范围及递减的网格误差。记录请求 r 与实际 dt，避免步数取整遮盖真实格式。','''try:heat_diffusion_explicit(ratio=.7)
except ValueError:print("Unstable FTCS ratio rejected")
else:raise AssertionError("Unstable ratio accepted")
assert np.allclose(solution["temperature"][:,[0,-1]],p["ambient_degC"])
assert solution["temperature"].min()>=p["ambient_degC"]-1e-9
assert np.all(np.diff(convergence.max_error_degC)<0)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame(solution["temperature"],index=solution["t"],columns=solution["x"]).to_csv(OUTPUT_DIR/"temperature-field.csv")
convergence.to_csv(OUTPUT_DIR/"grid-convergence.csv",index=False)
print("Boundary, stability and refinement checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[4]['id']]=[
 step('Audit actual strain samples and event timing','审计真实应变样本及事件时间','The embedded GWOSC snapshot is H1, 4096 samples/s, 32 seconds. Strain is dimensionless. Plot time relative to the published event GPS; the event label comes from the catalog, not from thresholding this plot.','内嵌 GWOSC 快照为 H1、4096 样本/秒、32 秒，应变无量纲。时间相对于已发表事件 GPS；事件标签来自目录，不由此图阈值判断。','''gw=snapshot("gw150914");strain=np.asarray(gw["strain"],float);fs=gw["sample_rate"]
assert len(strain)==fs*gw["duration"] and np.isfinite(strain).all()
relative_time=gw["gps_start"]+np.arange(len(strain))/fs-gw["event_gps"]
centered=strain-strain.mean()
print("Release:",gw["version"],"; detector:",gw["detector"],"; samples:",len(strain),"; rate:",fs,"Hz")
fig,ax=plt.subplots(figsize=(9,4));ax.plot(relative_time,centered,lw=.5)
ax.axvline(0,color="red",linestyle="--",label="Catalogued event time")
ax.set(xlabel="Time relative to catalogued event (s)",ylabel="H1 strain (dimensionless)",title="Frozen detector measurements");ax.legend();plt.tight_layout();plt.show()'''),
 step('Estimate amplitude spectral density','估计振幅谱密度','Welch averages overlapping tapered segments. sqrt(PSD) has units strain/sqrt(Hz); it is not the same quantity as a raw FFT amplitude. Source data is downsampled, so avoid interpreting near-Nyquist details as an independently calibrated high-frequency result.','Welch 对重叠加窗片段进行平均。sqrt(PSD) 的单位为应变/sqrt(Hz)，不同于原始 FFT 振幅。来源已降采样，不能将近 Nyquist 细节当成独立校准的高频结果。','''frequency,psd=welch(centered,fs=fs,nperseg=fs*4,noverlap=fs*2,scaling="density")
positive=frequency>0
fig,ax=plt.subplots(figsize=(8,5));ax.loglog(frequency[positive],np.sqrt(psd[positive]))
ax.axvspan(35,350,color="orange",alpha=.12,label="Declared display band")
ax.set(xlim=(10,1500),xlabel="Frequency (Hz)",ylabel="ASD (strain / sqrt(Hz))",title="Welch spectrum of the frozen record");ax.legend();plt.tight_layout();plt.show()'''),
 step('Apply a declared acausal display filter','应用声明过的非因果显示滤波器','The fourth-order Butterworth 35–350 Hz band-pass is applied forward and backward. This is zero-phase offline display processing and uses future samples within the record. A single detector’s filtered trace does not establish false-alarm probability or reproduce the published detection pipeline.','四阶 Butterworth 35–350 Hz 带通前向、反向各应用一次。这是离线零相位显示处理，会使用记录内未来样本。单探测器滤波轨迹不提供虚警概率，也不复现正式探测流程。','''sos=butter(4,[35,350],btype="bandpass",fs=fs,output="sos")
filtered=sosfiltfilt(sos,centered)
window=(relative_time>=-.25)&(relative_time<=.15)
fig,ax=plt.subplots(figsize=(9,4));ax.plot(relative_time[window],1e21*filtered[window],lw=1)
ax.axvline(0,color="gray",linestyle="--")
ax.set(xlabel="Time relative to catalogued event (s)",ylabel="Filtered strain (10⁻²¹)",title="Declared band-pass; interpretation requires the published analysis");plt.tight_layout();plt.show()''',cover=True),
 step('Audit spectral normalization and export','审计频谱归一化并导出','Use Parseval’s identity for the full-record real FFT as a separate normalization check. That identity is distinct from the averaged Welch PSD. Export the filter band and event metadata with every derived series.','使用整段实数 FFT 的 Parseval 恒等式做独立归一化检查；它不同于平均 Welch PSD。每个派生序列随同滤波频带及事件 metadata 导出。','''transform=np.fft.rfft(centered);squared=np.abs(transform)**2
fft_variance=(squared[0]+squared[-1]+2*squared[1:-1].sum())/len(centered)**2
assert np.isclose(fft_variance,np.mean(centered**2),rtol=1e-12,atol=0)
assert np.isfinite(filtered).all() and np.all(psd>=0)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"relative_time_s":relative_time,"centered_strain":centered,"filtered_strain":filtered}).to_csv(OUTPUT_DIR/"strain-display.csv",index=False)
pd.DataFrame({"frequency_Hz":frequency,"PSD_strain_squared_per_Hz":psd}).to_csv(OUTPUT_DIR/"welch-spectrum.csv",index=False)
(OUTPUT_DIR/"processing.json").write_text(json.dumps({"detector":gw["detector"],"release":gw["version"],"event_GPS":gw["event_gps"],"sample_rate_Hz":fs,"band_Hz":[35,350],"filter":"4th-order Butterworth SOS, forward/backward","inference":"display processing; no independent detection significance"},indent=2))
print("Parseval check passed; source credit: GWOSC, LIGO, Virgo and KAGRA. Exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[5]['id']]=[
 step('Compute wavelength spectral radiance in SI units','以 SI 单位计算波长谱辐亮度','Use frozen h, c and k_B. B_lambda is per metre of wavelength; multiplying by 10⁻⁹ expresses it per nm. The wavelength and frequency versions require a Jacobian and have different peak coordinates.','使用冻结的 h、c、k_B。B_lambda 按每米波长计，乘 10⁻⁹ 才换为每 nm。波长形式与频率形式需要 Jacobian，谱峰坐标不同。','''constants=snapshot("constants")["constants"]
h=constants["h"]["value"];c=constants["c"]["value"];k_B=constants["k_B"]["value"]
temperatures=[3000,5000,8000];wavelength=np.linspace(100e-9,3000e-9,1001)
fig,ax=plt.subplots(figsize=(9,4))
for temperature in temperatures:ax.plot(1e9*wavelength,1e-9*planck_radiance(wavelength,temperature,h,c,k_B),label=f"{temperature} K")
ax.set(xlabel="Wavelength (nm)",ylabel="Radiance (W m⁻² sr⁻¹ nm⁻¹)",title="Ideal blackbody wavelength spectra");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Locate continuous wavelength maxima','定位连续波长极大值','A bounded scalar optimizer searches wavelengths in metres. Its tolerance is a numerical setting. Confirm lambda_peak·T against the wavelength Wien constant; simply taking the highest sampled grid point adds grid-location error.','有界标量优化器以米为单位搜索波长，容差属于数值设置。用波长形式的维恩常数核对 lambda_peak·T；仅选网格最高点会增加位置离散误差。','''peaks=[]
for temperature in temperatures:
 optimum=minimize_scalar(lambda wave:-planck_radiance(np.array([wave]),temperature,h,c,k_B)[0],bounds=(50e-9,3000e-9),method="bounded",options={"xatol":1e-15})
 assert optimum.success
 peaks.append(optimum.x)
peaks=np.array(peaks)
fig,ax=plt.subplots(figsize=(7,4));ax.plot(temperatures,1e9*peaks,"o-",label="Continuous spectral maximum")
ax.plot(temperatures,1e9*2.897771955e-3/np.asarray(temperatures),"--",label="Wavelength Wien reference")
ax.set(xlabel="Model temperature (K)",ylabel="Peak wavelength (nm)",title="Peak-coordinate cross-check");ax.legend();plt.tight_layout();plt.show()'''),
 step('Integrate radiance into exitance','将辐亮度积分为出射度','For an ideal isotropic surface, exitance is pi times wavelength-integrated radiance. A dimensionless change of variable yields the integral of x³/(exp(x)−1), equal to pi⁴/15. This avoids a poorly scaled wavelength quadrature over an infinite interval.','理想各向同性表面的出射度为波长积分辐亮度乘 pi。无量纲变量转换给出 x³/(exp(x)−1) 的积分，等于 pi⁴/15，可避免无限波长区间的尺度问题。','''integral,estimated_error=quad(lambda x:x**3/np.expm1(x),0,100,epsabs=1e-10)
sigma=2*np.pi**5*k_B**4/(15*h**3*c**2)
grid_temperature=np.linspace(1000,10000,101)
numeric_exitance=2*np.pi*k_B**4*grid_temperature**4/(h**3*c**2)*integral
reference_exitance=sigma*grid_temperature**4
fig,ax=plt.subplots(figsize=(7,4));ax.loglog(grid_temperature,numeric_exitance,label="Dimensionless quadrature")
ax.loglog(grid_temperature,reference_exitance,"--",label="Derived sigma T⁴")
ax.set(xlabel="Model temperature (K)",ylabel="Exitance (W/m²)",title="Integrated spectral law and T⁴ scaling");ax.legend();plt.tight_layout();plt.show()
print("Derived sigma (W m⁻² K⁻⁴):",sigma,"; dimensionless integral:",integral)'''),
 step('Reconcile positivity, peaks and integrated units','核对正值、谱峰和积分单位','Verify the independent integral identity and T⁴ exponent. These comparisons concern ideal laws and numerical implementation; they do not validate emissivity, temperature or detector calibration for a real material.','核对独立积分恒等式及 T⁴ 指数。这些比较验证理想定律和数值实现，不会替真实材料验证发射率、温度或探测器校准。','''assert np.isclose(integral,np.pi**4/15,rtol=1e-10)
assert np.allclose(peaks*np.asarray(temperatures),2.897771955e-3,rtol=1e-5)
assert np.allclose(numeric_exitance,reference_exitance,rtol=1e-10)
assert np.isclose(np.polyfit(np.log(grid_temperature),np.log(numeric_exitance),1)[0],4)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"wavelength_nm":wavelength*1e9,**{f"radiance_per_nm_{t}K":1e-9*planck_radiance(wavelength,t,h,c,k_B) for t in temperatures}}).to_csv(OUTPUT_DIR/"blackbody-spectra.csv",index=False)
pd.DataFrame({"temperature_K":temperatures,"peak_wavelength_nm":peaks*1e9}).to_csv(OUTPUT_DIR/"spectral-peaks.csv",index=False)
print("Integral, wavelength-peak and scaling checks passed; exports:",OUTPUT_DIR)''')]

EXERCISES={}
notes=[
 (['Explain why the 90-degree period differs from the small-angle period.','Interpret the relative energy-drift curve.','The nonlinear restoring acceleration uses sin(theta), so large-angle timing differs. Relative drift is a numerical audit of an ideal conservative model, not measured friction.','Using NumPy/SciPy/Matplotlib, add 60 degrees and retain all zero-crossing and energy checks.','With the same packages, halve solver tolerances and compare energy drift without altering physical parameters.','Periods are finite, small-angle agreement remains and relative energy drift is bounded.'],['解释九十度周期为何不同于小角度周期。','解释相对能量漂移曲线。','非线性回复加速度使用 sin(theta)，大角度计时因此不同。相对漂移是理想守恒模型的数值审计，不是实测摩擦。','仅用 NumPy、SciPy、Matplotlib 加入六十度，保留过零点和能量校验。','使用同样的包缩小求解容差，比较能量漂移，不改物理参数。','周期有限，小角度仍接近线性值，相对能量漂移受限。']),
 (['Distinguish rad/s from Hz.','Why compare steady response only after transient decay?','Angular frequency is 2pi times cycles/s. A steady sinusoid omits the transient determined by initial conditions.','Using NumPy/SciPy/Matplotlib, add damping=8 N·s/m and inspect free-decay versus frequency-response behavior.','With the same packages, export the analytical phase curve using atan2 and clear radian units.','Dimensional parameters are retained; late-time amplitude/phase checks pass for positive damping.'],['区分 rad/s 与 Hz。','为何稳态响应只应在瞬态衰减后比较？','角频率等于每秒周期数乘 2pi。稳态正弦未包含由初始条件决定的瞬态。','仅用 NumPy、SciPy、Matplotlib 加入阻尼 8 N·s/m，检查自由衰减及频响。','使用同样的包，用 atan2 导出解析相位曲线并说明弧度单位。','保留有量纲参数；正阻尼下后期振幅/相位核对通过。']),
 (['Explain the sign of drag power.','Why include launch height in the vacuum reference?','Drag opposes velocity, so its dot product with velocity is nonpositive. Nonzero launch height changes flight time and range.','Using NumPy/SciPy/Matplotlib, compare initial angles 30, 45 and 60 degrees under the same declared drag model.','With the same packages, vary constant air density and export trajectories plus energy/work errors.','Stop at descending ground events; zero-drag checks and dimensional energy balances pass.'],['说明阻力功率的符号。','为何真空参考要包含发射高度？','阻力反向于速度，其与速度的内积非正。非零高度会改变飞行时间与射程。','仅用 NumPy、SciPy、Matplotlib 在同一阻力模型下比较三十、四十五、六十度。','使用同样的包改变恒定空气密度，导出轨迹及能量/功误差。','在下降落地事件停止，零阻力核对及有量纲能量平衡通过。']),
 (['Explain the dependence of allowable dt on dx.','Why does integrated thermal excess decrease with these boundaries?','The stable dt scales with dx²/alpha. Fixed-temperature endpoints exchange heat with reservoirs, so the system is not isolated.','Using NumPy/Pandas/Matplotlib, compare r=.2 and .4 at the same spatial grid, recording actual dt.','With the same packages, add final analytic and numerical profiles plus an error subplot.','Reject r>.5, preserve fixed ends and verify refinement against the sine-mode solution.'],['解释允许 dt 如何依赖 dx。','为何此边界下的总超温积分会下降？','稳定 dt 按 dx²/alpha 缩放。固定温度端点与热库交换热量，系统不是孤立的。','仅用 NumPy、Pandas、Matplotlib 在同一空间网格比较 r=.2、.4，记录实际 dt。','使用同样的包增加末时解析/数值分布及误差子图。','拒绝 r>.5，保持固定端点，按正弦模态解核对网格收敛。']),
 (['Distinguish PSD, ASD and FFT amplitude units.','Why is forward/backward filtering not real-time processing?','ASD is sqrt(PSD), with strain/sqrt(Hz) units. Acausal filtering reads future record samples; a displayed waveform alone is not a significance calculation.','Using NumPy/SciPy/Matplotlib, compare 30–300 and 35–350 Hz bands while preserving the same original strain and declared settings.','With the same packages, add a filter-magnitude response and mark the selected band; retain the FFT Parseval check.','Preserve all 131072 samples, source timing and credit, finite outputs and explicit acausal/display interpretation.'],['区分 PSD、ASD 与 FFT 振幅的单位。','为何前后向滤波不是实时处理？','ASD 为 PSD 的平方根，单位为应变/sqrt(Hz)。非因果滤波读取未来样本；显示波形本身不是显著性计算。','仅用 NumPy、SciPy、Matplotlib 比较 30–300 与 35–350 Hz，保留原始应变及明确设置。','使用同样的包增加滤波幅频响应并标频带，保留 FFT Parseval 校验。','保留 131072 个样本、来源时间及署名，输出有限，明确非因果显示性质。']),
 (['Why convert per-metre radiance to per-nm before plotting?','Why do wavelength and frequency representations peak differently?','Spectral density transforms with the coordinate differential. The wavelength/frequency Jacobian changes density and maximum coordinates.','Using NumPy/SciPy/Matplotlib, add an ideal 6500 K spectrum and peak without changing the frozen constants.','With the same packages, implement frequency-domain Planck radiance with explicit W m^-2 sr^-1 Hz^-1 units and explain the peak difference.','Spectra remain positive, unit conversions are stated, the integral identity and sigma T^4 checks pass.'],['为何绘图前要把每米辐亮度换为每 nm？','为何波长和频率表示的谱峰不同？','谱密度随坐标微分转换，波长/频率 Jacobian 改变密度及极大值位置。','仅用 NumPy、SciPy、Matplotlib 加入理想 6500 K 光谱及谱峰，不改变冻结常数。','使用同样的包实现频率形式普朗克辐亮度，注明 W m^-2 sr^-1 Hz^-1 并解释谱峰差别。','光谱为正，单位换算明确，积分恒等式及 sigma T^4 校验通过。'])]
for c,(en,zh) in zip(COURSES,notes):EXERCISES[c['id']]=exercises(en,zh)
