"""Six chemistry workflows, distinguishing database calculations, reference laws and simulations."""
from ._common import lesson,step,exercises,bilingual

COURSES=[
 lesson('ch01-molecular-formulas',1,'molecular-formulas','Reconcile molecular formulas and calculated properties','核对分子式与计算性质','Parse eight PubChem formulas, reconstruct approximate molar masses and compare elemental mass fractions and reported descriptors.','解析八个 PubChem 分子式，重建近似摩尔质量，并比较元素质量分数与计算描述符。',['molecules'],['parse_simple_formula'],'molecules','Molecules & structures','分子与结构',discipline='chemistry',data_kind='computed',difficulty=1,icon='⚗️',setup_imports='import re\n'),
 lesson('ch02-molecular-graphs',2,'molecular-graphs','Read standardized molecules as graphs','将标准化分子读为图','Parse real V2000 records, preserve formal charges, compare connected components and cycles, and export inspectable graphs.','解析真实 V2000 记录，保留形式电荷，比较连通分量与环，并导出可检查的图。',['molecules'],['parse_molfile','molecular_graph'],'molecules','Molecules & structures','分子与结构',discipline='chemistry',data_kind='computed',icon='🕸️',packages=['numpy','pandas','matplotlib','networkx','IPython']),
 lesson('ch03-caffeine-geometry',3,'caffeine-geometry','Inspect a calculated caffeine conformer','检查计算的咖啡因构象','Preview the PubChem 3D conformer offline, compare bond lengths and audit heavy-atom distance geometry.','离线预览 PubChem 三维构象，比较键长并审计重原子距离几何。',['molecules'],['parse_molfile'],'molecules','Molecules & structures','分子与结构',discipline='chemistry',data_kind='computed',icon='🧊',interactive_3d=True,setup_imports='import py3Dmol\nfrom scipy.spatial.distance import cdist\n',packages=['numpy','pandas','scipy','matplotlib','py3Dmol','IPython']),
 lesson('ch04-titration',4,'acid-base-titration','Solve an ideal weak-acid titration','求解理想弱酸滴定','Use mass and charge balance across a strong-base titration, compare the buffer approximation and inspect species fractions.','在强碱滴定过程中使用质量与电荷平衡，对照缓冲近似并检查物种分数。',['models'],['weak_acid_titration'],'equilibria','Equilibria & thermodynamics','平衡与热力学',discipline='chemistry',data_kind='model',icon='🧪',setup_imports='from scipy.optimize import brentq\n',packages=['numpy','pandas','scipy','matplotlib','IPython']),
 lesson('ch05-vapor-pressure',5,'water-vapor-pressure','Evaluate a reference vapor-pressure correlation','计算参考饱和蒸气压关联式','Reproduce IAPWS reference pressure in its valid range, check reference points and examine a Clausius–Clapeyron approximation.','在有效范围内复现 IAPWS 参考压力、检查参考点，并考察 Clausius–Clapeyron 近似。',['models','constants'],['water_saturation_pressure'],'equilibria','Equilibria & thermodynamics','平衡与热力学',discipline='chemistry',data_kind='reference',icon='💧'),
 lesson('ch06-calibration',6,'spectroscopic-calibration','Audit a simulated absorbance calibration','审计模拟吸光度校准','Generate declared Beer–Lambert teaching observations, fit a calibration, inspect residuals and propagate uncertainty to an unknown.','生成明确声明的 Beer–Lambert 教学观测，拟合校准、检查残差，并向未知量传播不确定性。',['models'],['linear_calibration'],'measurement','Measurement models','测量模型',discipline='chemistry',data_kind='simulation',minutes=60,icon='🔬'),
]
for c in COURSES:
 c['online_url']='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2519/property/MolecularFormula/JSON' if 'molecules' in c['snapshots'] else 'https://iapws.org/technical-guidance/release/Supp-sat' if 'vapor' in c['id'] else 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html'
 c['data_note']=bilingual('PubChem properties and conformers are calculated database fields, not new experimental measurements. V2000 parsing here is intentionally limited to atoms, reported bonds and formal charges. Titration and calibration use stated ideal/simulated teaching assumptions. Water pressure uses the attributed IAPWS reference correlation. Descriptors, distances and visual proximity do not establish biological activity or binding strength.','PubChem 性质与构象是数据库计算字段，不是新实验测量。本课 V2000 解析范围明确限定为原子、来源键型与形式电荷。滴定及校准使用已声明的理想/模拟教学假设；水蒸气压使用署名的 IAPWS 参考关联式。描述符、距离和视觉邻近不能证明生物活性或结合强度。')

MOLECULE_LOAD='''molecules=snapshot("molecules")
properties=pd.DataFrame(molecules["properties"]).set_index("CID")
assert len(properties)==8 and properties.index.is_unique
display(properties[["name","MolecularFormula","MolecularWeight","TPSA","Charge"]])'''
SECTIONS={}
SECTIONS[COURSES[0]['id']]=[
 step('Load calculated fields and define the parser boundary','加载计算字段并声明解析边界','The source provides molecular formula, calculated molecular weight and descriptors for eight declared CIDs. The readable parser accepts ordinary element/count formulas, and rejects parentheses, isotope and charge notation rather than silently changing their meaning.','来源给出八个声明 CID 的分子式、计算分子量和描述符。可读解析器接受普通元素/数量分子式，拒绝括号、同位素和电荷写法，不静默改义。',MOLECULE_LOAD+'''
atomic_weights={"H":1.008,"C":12.011,"N":14.007,"O":15.999}
counts={int(cid):parse_simple_formula(row.MolecularFormula) for cid,row in properties.iterrows()}
assert all(set(count)<=set(atomic_weights) for count in counts.values())'''),
 step('Reconstruct approximate molar masses','重建近似摩尔质量','Use explicitly rounded average atomic weights in g/mol. This is not a monoisotopic mass calculation. Small differences from PubChem arise from declared rounding and representation; keep both original and reconstructed values.','使用明确舍入的平均原子量，单位 g/mol；这不是单同位素质量计算。与 PubChem 的微小差异来自舍入及表示方式，应保留原值与重建值。','''calculated=np.array([sum(atomic_weights[element]*count for element,count in counts[int(cid)].items()) for cid in properties.index])
comparison=properties[["name","MolecularWeight"]].copy();comparison["reconstructed_g_per_mol"]=calculated
comparison["difference_g_per_mol"]=calculated-properties.MolecularWeight
fig,ax=plt.subplots(figsize=(8,4));ax.barh(properties.name,properties.MolecularWeight,label="PubChem")
ax.plot(calculated,np.arange(8),"kx",label="Rounded atomic-weight reconstruction")
ax.set(xlabel="Molar mass (g/mol)",title="Formula-based reconstruction of calculated source masses");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Read elemental mass fractions','解读元素质量分数','Stacked bars give percent mass attributed to C, H, N and O under the same rounded-weight convention. A mass fraction is different from an atom-count fraction; hydrogen’s many atoms need not dominate total mass.','叠加柱表示在同一舍入原子量约定下 C、H、N、O 的质量百分比。质量分数不同于原子数量分数，氢原子较多不代表总质量占比最高。','''fraction=pd.DataFrame({element:[atomic_weights[element]*counts[int(cid)].get(element,0)/calculated[j] for j,cid in enumerate(properties.index)] for element in atomic_weights},index=properties.name)
fig,ax=plt.subplots(figsize=(9,4));(100*fraction).plot.bar(stacked=True,ax=ax)
ax.set(ylabel="Elemental mass (%)",xlabel="Declared compound",title="Mass fractions under the stated atomic-weight convention");plt.xticks(rotation=25,ha="right");plt.tight_layout();plt.show()'''),
 step('Compare a second calculated descriptor','比较第二个计算描述符','TPSA is topological polar surface area in square ångströms, a computed descriptor. Its scatter against molar mass describes these eight molecules only, and does not estimate permeability, toxicity or drug efficacy.','TPSA 是计算的拓扑极性表面积，单位平方埃。与摩尔质量的散点仅描述这八个分子，不估计通透性、毒性或药效。','''fig,ax=plt.subplots(figsize=(8,5));ax.scatter(properties.MolecularWeight,properties.TPSA,s=40)
for row in properties.itertuples():ax.annotate(row.name,(row.MolecularWeight,row.TPSA),fontsize=8,xytext=(4,4),textcoords="offset points")
ax.set(xlabel="Calculated molar mass (g/mol)",ylabel="Calculated TPSA (Å²)",title="Reported descriptors, not a biological assay");plt.tight_layout();plt.show()'''),
 step('Check conservation and unsupported syntax','检查分数守恒及不支持的语法','Fractions sum to one and reconstructed masses agree with the reported rounded masses within 0.03 g/mol. Verify that a grouped formula is rejected, then export calculations with the weight convention.','分数应和为一，重建质量与舍入来源值相差不超过 0.03 g/mol。检查含分组分子式会报错，再随原子量约定导出计算。','''assert np.allclose(fraction.sum(axis=1),1)
assert np.max(abs(comparison.difference_g_per_mol))<.03
try:parse_simple_formula("Mg(OH)2")
except ValueError:print("Grouped formula rejected by the declared simple parser")
else:raise AssertionError("Unsupported syntax silently accepted")
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);comparison.to_csv(OUTPUT_DIR/"molar-mass-reconciliation.csv")
fraction.to_csv(OUTPUT_DIR/"elemental-mass-fractions.csv")
(OUTPUT_DIR/"atomic-weights.json").write_text(json.dumps(atomic_weights,indent=2))
print("Mass and fraction checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[1]['id']]=[
 step('Read atom, bond and charge records','读取原子、键与电荷记录','The V2000 counts line defines record boundaries. Atom IDs are converted to zero-based Python indices; bond endpoints are validated and duplicate/self edges rejected. Keep formal charges instead of inferring them from drawing color.','V2000 数量行定义记录边界。原子 ID 转为 Python 零基索引，检查键端点，拒绝重复/自身边。保留形式电荷，不根据颜色猜测。',MOLECULE_LOAD+'''
parsed={int(cid):parse_molfile(molecules["sdf_2d"][str(cid)]) for cid in properties.index}
graphs={};summaries=[]
for cid,record in parsed.items():
 graph,summary=molecular_graph(record);graphs[cid]=graph
 summaries.append({"CID":cid,"name":properties.loc[cid,"name"],**summary,"formal_charge":sum(a["formal_charge"] for a in record["atoms"])})
summary=pd.DataFrame(summaries).set_index("CID");display(summary)'''),
 step('Display one reported molecular graph','展示来源分子图','Use benzene’s two-dimensional SDF layout for a drawing. These layout coordinates are not experimental bond lengths. Node colors mark elements, and edge labels are reported bond-type codes; they are not force constants or interaction energies.','用苯的二维 SDF 排布绘图，这些排布坐标不是实验键长。节点颜色区分元素，边标签为来源键型代码，不是力常数或相互作用能。','''cid=241;record=parsed[cid];graph=graphs[cid]
positions={a["index"]:a["position"][:2] for a in record["atoms"]}
labels={a["index"]:a["element"]+str(a["index"]) for a in record["atoms"]}
fig,ax=plt.subplots(figsize=(7,6));nx.draw_networkx(graph,pos=positions,labels=labels,node_size=600,node_color=["#b4d4ed" if graph.nodes[j]["element"]=="C" else "#eeeeee" for j in graph],ax=ax,font_size=9)
nx.draw_networkx_edge_labels(graph,positions,edge_labels=nx.get_edge_attributes(graph,"reported_bond_type"),ax=ax,font_size=8)
ax.set_title("Benzene: reported 2D molecular graph");ax.axis("off");plt.tight_layout();plt.show()''',cover=True),
 step('Compare cyclomatic counts','比较独立环数量','For an undirected graph, cycle rank is edges−nodes+connected components. It counts independent graph cycles, not aromaticity or stereochemical rings. Explicit hydrogen nodes change degree counts but not this topological identity.','无向图的环秩为边数−节点数+连通分量，计数独立图环，不判断芳香性或立体化学环。显式氢节点影响度数，但不改变该拓扑恒等式。','''fig,ax=plt.subplots(figsize=(8,4));ax.barh(summary.name,summary.cycle_rank)
ax.set(xlabel="Independent cycle rank",title="Topology from reported atom/bond records");plt.tight_layout();plt.show()'''),
 step('Inspect node degrees','检查节点度数','The histogram uses all atom nodes in the eight declared records, including explicit hydrogens. Graph degree counts neighbors; it differs from bond-order sum and chemical valence. This teaching parser does not implement a full chemistry toolkit.','直方图使用八个记录中的全部原子，包括显式氢。图度数计邻居，与键级和、化学价不同。本解析器不承担完整化学工具库的功能。','''degrees=np.concatenate([np.array([degree for node,degree in graph.degree()]) for graph in graphs.values()])
fig,ax=plt.subplots(figsize=(7,4));ax.hist(degrees,bins=np.arange(-.5,6.6,1),edgecolor="white")
ax.set(xlabel="Reported atom-neighbor degree",ylabel="Atoms",title="Degree counts across declared structures");plt.tight_layout();plt.show()'''),
 step('Reconcile counts and export graph records','核对数量并导出图记录','Check atom/bond counts against every source header and compare total formal charge with the property endpoint. Export one graph and the complete summary. Validation uses record identity; a visual drawing alone cannot establish parsing correctness.','将各图原子/键数与来源头逐个核对，并将总形式电荷与性质接口比较。导出一个图及完整摘要。校验依靠记录身份，不能只看图形。','''for cid,record in parsed.items():
 assert graphs[cid].number_of_nodes()==record["atom_count"] and graphs[cid].number_of_edges()==record["bond_count"]
 assert summary.loc[cid,"formal_charge"]==properties.loc[cid,"Charge"]
assert summary.loc[241,"cycle_rank"]==1
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);summary.to_csv(OUTPUT_DIR/"molecular-graph-summary.csv")
nx.write_graphml(graphs[241],OUTPUT_DIR/"benzene.graphml")
print("Header, graph and charge checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[2]['id']]=[
 step('Distinguish computed conformation from experiment','区分计算构象与实验结构','The source is a PubChem calculated caffeine conformer. Coordinates are in ångströms and include explicit hydrogens. This is neither a solved protein structure nor a solvent-dependent ensemble; source bond connectivity remains separate from geometric proximity.','来源是 PubChem 计算的咖啡因构象，坐标单位为埃并包含显式氢。它不是实验解析蛋白结构，也不是溶剂中的构象集合；来源键连接与几何邻近应分别处理。','''molecules=snapshot("molecules");sdf=molecules["caffeine_3d_sdf"];record=parse_molfile(sdf)
positions=np.array([a["position"] for a in record["atoms"]]);elements=np.array([a["element"] for a in record["atoms"]])
heavy=elements!="H";print("Atoms:",len(positions),"; heavy atoms:",int(heavy.sum()),"; coordinate unit: Å; computed conformer")
viewer=py3Dmol.view(width=640,height=420)
viewer.addModel(sdf,"sdf");viewer.setStyle({"stick":{"radius":.15},"sphere":{"scale":.25}});viewer.setBackgroundColor("white");viewer.zoomTo()
display(HTML(viewer._make_html()))'''),
 step('Build a static geometry cross-check','构造静态几何核对图','The static figure uses the same coordinates and source bonds. Axes are ångströms. It provides an offline non-WebGL view, and does not infer a bond by simply drawing every short interatomic distance.','静态图使用同一组坐标及来源键，轴单位为埃。它提供无需 WebGL 的离线视图，也不靠画出所有短距离推断键。','''colors={"C":"gray","H":"lightgray","N":"royalblue","O":"red"}
fig=plt.figure(figsize=(7,6));ax=fig.add_subplot(projection="3d")
for element in sorted(set(elements)):
 mask=elements==element;ax.scatter(*positions[mask].T,color=colors.get(element,"green"),s=35 if element!="H" else 12,label=element)
for bond in record["bonds"]:
 pair=positions[[bond["a"],bond["b"]]];ax.plot(*pair.T,color="black",lw=1)
ax.set(xlabel="x (Å)",ylabel="y (Å)",zlabel="z (Å)",title="Calculated caffeine conformer; source bonds");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Measure source-bond lengths','测量来源键长','Measure Euclidean distances only for declared bond endpoints. The histogram uses the calculated conformer’s geometry. Bond lengths are not bond energies, force constants or evidence of biological binding.','仅对声明的键端点计算欧氏距离。直方图来自计算构象的几何，不将键长当成键能、力常数或生物结合证据。','''bond_lengths=np.array([np.linalg.norm(positions[b["a"]]-positions[b["b"]]) for b in record["bonds"]])
fig,ax=plt.subplots(figsize=(7,4));ax.hist(bond_lengths,bins=15,edgecolor="white")
ax.set(xlabel="Calculated source-bond length (Å)",ylabel="Bonds",title="Geometric lengths, not interaction energies");plt.tight_layout();plt.show()'''),
 step('Audit the heavy-atom distance matrix','审计重原子距离矩阵','The matrix includes all heavy-atom pairs and has a zero diagonal. A distance matrix encodes geometry but not bond type, stereochemical identity or a binding assay. Use it alongside the declared structure record.','矩阵包含全部重原子对，对角线为零。距离矩阵描述几何，不编码键型、立体身份或结合实验，应结合声明结构记录解读。','''heavy_positions=positions[heavy];distance=cdist(heavy_positions,heavy_positions)
fig,ax=plt.subplots(figsize=(6,5));im=ax.imshow(distance,cmap="viridis")
ax.set(xlabel="Heavy-atom order",ylabel="Heavy-atom order",title="Calculated heavy-atom distances");fig.colorbar(im,ax=ax,label="Distance (Å)");plt.tight_layout();plt.show()'''),
 step('Reconcile geometry and export the conformer','核对几何并导出构象','Check symmetry and one manually recomputed distance; check positivity of all reported bond lengths. Preserve the original SDF with derived tables so geometric results can be traced to the exact calculated conformer.','检查对称性及一个手工重算距离，并检查来源键长均为正。随派生表保留原始 SDF，便于追溯确切计算构象。','''assert np.allclose(distance,distance.T) and np.allclose(np.diag(distance),0)
assert np.isclose(distance[0,1],np.sqrt(np.sum((heavy_positions[0]-heavy_positions[1])**2)))
assert np.all(bond_lengths>0) and heavy.sum()==14
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);(OUTPUT_DIR/"caffeine-computed-conformer.sdf").write_text(sdf)
pd.DataFrame(distance).to_csv(OUTPUT_DIR/"heavy-atom-distances-Angstrom.csv",index=False)
pd.DataFrame({"a":[b["a"] for b in record["bonds"]],"b":[b["b"] for b in record["bonds"]],"reported_type":[b["order"] for b in record["bonds"]],"length_Angstrom":bond_lengths}).to_csv(OUTPUT_DIR/"reported-bond-lengths.csv",index=False)
print("Geometry checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[3]['id']]=[
 step('Solve charge balance over the full titration','在完整滴定范围求解电荷平衡','For a monoprotic weak acid plus strong base, solve H+[Na+]−Kw/H−[A−]=0 with [A−]=Ct Ka/(Ka+H). This is an ideal concentration model at the declared temperature; activity corrections and real instrument response are excluded.','单质子弱酸与强碱采用 H+[Na+]−Kw/H−[A−]=0，其中 [A−]=Ct Ka/(Ka+H)。这是声明温度下的理想浓度模型，未包含活度修正及真实仪器响应。','''p=snapshot("models")["titration"]
added=np.linspace(0,.05,501)
result=weak_acid_titration(p["acid_initial_mol_per_L"],p["acid_volume_L"],p["base_mol_per_L"],added,p["pKa"],p["Kw"])
equivalence=p["acid_initial_mol_per_L"]*p["acid_volume_L"]/p["base_mol_per_L"]
fig,ax=plt.subplots(figsize=(8,4));ax.plot(1000*added,result["pH"])
ax.axvline(1000*equivalence,color="gray",linestyle="--",label="Stoichiometric equivalence")
ax.set(xlabel="Added base (mL)",ylabel="Ideal concentration-model pH",title="Weak-acid/strong-base titration");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Read species fractions','解读物种分数','Plot fractions of total acid present as HA and A−. These fractions sum to one by mass balance. Large changes near the equivalence volume describe the ideal equilibrium calculation rather than direct concentration measurements.','绘制总酸以 HA 和 A− 存在的分数，其和因质量平衡等于一。当量体积附近的变化描述理想平衡计算，不是直接浓度测量。','''fraction=result["anion_fraction"]
fig,ax=plt.subplots(figsize=(8,4));ax.plot(1000*added,1-fraction,label="HA fraction");ax.plot(1000*added,fraction,label="A− fraction")
ax.set(xlabel="Added base (mL)",ylabel="Fraction of total acid",ylim=(0,1.05),title="Ideal speciation fractions");ax.legend();plt.tight_layout();plt.show()'''),
 step('Compare the buffer approximation in its intended interval','在适用区间比较缓冲近似','The Henderson–Hasselbalch comparison uses stoichiometric buffer amounts for 0<V<Veq. It is undefined at zero addition and equivalence in this form. Plot its difference from the full charge-balance solution instead of applying it across the whole curve.','Henderson–Hasselbalch 对照在 0<V<Veq 使用化学计量缓冲量，此形式在零添加量和当量处未定义。应画与完整电荷平衡的差，而不是跨整条曲线套用。','''mask=(added>.002)&(added<equivalence-.002)
acid_moles=p["acid_initial_mol_per_L"]*p["acid_volume_L"];base_moles=p["base_mol_per_L"]*added[mask]
approximation=p["pKa"]+np.log10(base_moles/(acid_moles-base_moles))
fig,ax=plt.subplots(figsize=(8,4));ax.plot(1000*added[mask],approximation-result["pH"][mask])
ax.axhline(0,color="black",lw=1);ax.set(xlabel="Added base (mL), buffer interval",ylabel="Approximation − charge-balance pH",title="Approximation error is not electrode uncertainty");plt.tight_layout();plt.show()'''),
 step('Check electroneutrality and export assumptions','检查电中性并导出假设','Verify the molar charge residual, monotonic titration response and near-pKa behavior at half-equivalence. pKa=4.76 and Kw are declared teaching inputs. None of these numerical checks substitutes for an experimental titration or activity model.','核对摩尔电荷残差、滴定曲线单调性及半当量附近 pKa 行为。pKa=4.76 和 Kw 是教学输入；数值检查不能替代真实滴定或活度模型。','''assert np.max(abs(result["charge_residual_mol_per_L"]))<1e-10
assert np.all(np.diff(result["pH"])>=-1e-9) and np.all((fraction>=0)&(fraction<=1))
half=weak_acid_titration(p["acid_initial_mol_per_L"],p["acid_volume_L"],p["base_mol_per_L"],np.array([equivalence/2]),p["pKa"],p["Kw"])
assert abs(half["pH"][0]-p["pKa"])<.01
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"base_volume_mL":added*1000,"ideal_pH":result["pH"],"anion_fraction":fraction,"charge_residual_mol_per_L":result["charge_residual_mol_per_L"]}).to_csv(OUTPUT_DIR/"ideal-titration.csv",index=False)
(OUTPUT_DIR/"assumptions.json").write_text(json.dumps(p,indent=2))
print("Mass/charge and half-equivalence checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[4]['id']]=[
 step('Respect the reference correlation range','遵守参考关联式范围','IAPWS SR1-86(1992) defines saturation pressure between the triple and critical temperatures. The correlation returns absolute pressure in Pa. Coefficients and critical values are transcribed from the official release, whose cover permits unrestricted publication.','IAPWS SR1-86(1992) 定义三相点至临界温度间的饱和压力，关联式返回绝对压力 Pa。系数及临界值来自官方发布文件，其封面允许不受限制地出版。','''p=snapshot("models")["water_saturation"];R=snapshot("constants")["constants"]["R"]["value"]
temperature=np.linspace(273.16,400,501);pressure=water_saturation_pressure(temperature,p)
fig,ax=plt.subplots(figsize=(8,4));ax.semilogy(temperature-273.15,pressure/1000)
ax.set(xlabel="Reference temperature (°C)",ylabel="Absolute saturation pressure (kPa)",title="IAPWS reference saturation-pressure correlation");plt.tight_layout();plt.show()''',cover=True),
 step('Inspect a Clausius–Clapeyron linear approximation','检查 Clausius–Clapeyron 线性近似','In an ideal-vapor, negligible-liquid-volume, constant-enthalpy approximation, ln(P) is linear in 1/T. Fit a declared 280–370 K reference interval and show residuals separately. These are calculated reference pressures, not independent experimental observations.','在理想蒸气、液体体积可忽略和恒定焓近似下，ln(P) 对 1/T 线性。对声明的 280–370 K 参考区间拟合，并单独检查残差；这些是参考计算压力，不是独立实验观测。','''fit_temperature=np.linspace(280,370,101);fit_pressure=water_saturation_pressure(fit_temperature,p)
coefficient=np.polyfit(1/fit_temperature,np.log(fit_pressure),1);predicted=np.polyval(coefficient,1/fit_temperature)
apparent_enthalpy=-R*coefficient[0]
fig,axes=plt.subplots(1,2,figsize=(10,4));axes[0].plot(1/fit_temperature,np.log(fit_pressure),label="Reference correlation")
axes[0].plot(1/fit_temperature,predicted,"--",label="Linear approximation");axes[0].set(xlabel="1/T (1/K)",ylabel="ln(P / 1 Pa)");axes[0].legend(fontsize=8)
axes[1].plot(fit_temperature,np.log(fit_pressure)-predicted);axes[1].set(xlabel="T (K)",ylabel="Log-pressure residual")
plt.tight_layout();plt.show();print("Apparent interval enthalpy under ideal-vapor approximation (kJ/mol):",apparent_enthalpy/1000)'''),
 step('Inspect local apparent enthalpy','检查局部表观焓','R T² dln(P)/dT gives an apparent molar vaporization enthalpy only under the same volume/ideal-vapor approximation. Its change over temperature exposes the constant-enthalpy simplification. Do not extend this estimate to critical conditions as an exact latent heat.','R T² dln(P)/dT 只有在相同体积和理想蒸气近似下才给出表观摩尔汽化焓。随温度变化提示恒定焓简化；不能在临界条件下将其当作精确潜热。','''local=R*fit_temperature**2*np.gradient(np.log(fit_pressure),fit_temperature,edge_order=2)
fig,ax=plt.subplots(figsize=(8,4));ax.plot(fit_temperature,local/1000)
ax.axhline(apparent_enthalpy/1000,color="gray",linestyle="--",label="Interval linear-fit value")
ax.set(xlabel="Reference temperature (K)",ylabel="Apparent ideal-vapor enthalpy (kJ/mol)",title="Temperature-dependent reference slope");ax.legend();plt.tight_layout();plt.show()'''),
 step('Check pressure benchmarks and rejected extrapolation','检查压力基准及拒绝外推','Reproduce the critical pressure and the triple-point reference to stated rounding precision. Below-triple-point input is rejected because this correlation is not a general ice-vapor equation. Export absolute units and the reference release.','在声明舍入精度下复现临界压力和三相点参考。拒绝三相点以下输入，因为该式不是一般冰—蒸气方程。导出绝对单位及参考发布号。','''assert np.isclose(water_saturation_pressure(np.array([647.096]),p)[0],22.064e6,rtol=1e-12)
assert np.isclose(water_saturation_pressure(np.array([273.16]),p)[0],611.657,rtol=5e-6)
assert np.all(np.diff(pressure)>0)
try:water_saturation_pressure(np.array([250]),p)
except ValueError:print("Below-range extrapolation rejected")
else:raise AssertionError("Unsupported temperature accepted")
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"temperature_K":temperature,"reference_pressure_Pa":pressure}).to_csv(OUTPUT_DIR/"reference-saturation-pressure.csv",index=False)
pd.DataFrame({"temperature_K":fit_temperature,"apparent_enthalpy_J_per_mol":local,"linear_log_pressure_residual":np.log(fit_pressure)-predicted}).to_csv(OUTPUT_DIR/"reference-approximation-audit.csv",index=False)
print("Reference-point and range checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[5]['id']]=[
 step('Generate explicitly simulated calibration observations','生成明确标记的模拟校准观测','The model is A=blank+epsilon·l·c plus declared Gaussian noise. There are three simulated replicates at each of nine concentration levels. These are a method benchmark, not laboratory data. Concentration is displayed in micromol/L; absorbance is dimensionless.','模型为 A=blank+epsilon·l·c，再加声明的高斯噪声。九个浓度水平各有三次模拟重复。这是方法基准，不是实验室数据。浓度显示为 μmol/L，吸光度无量纲。','''models=snapshot("models");p=models["calibration"];rng=np.random.default_rng(models["seed"])
concentration=np.repeat(np.linspace(0,80,9),3)
truth=p["blank_absorbance"]+p["absorptivity_L_per_mol_cm"]*p["path_length_cm"]*concentration*1e-6
absorbance=truth+rng.normal(0,p["noise_sd_absorbance"],len(truth))
fitted=linear_calibration(concentration,absorbance);intercept,slope=fitted["coefficients"]
fig,ax=plt.subplots(figsize=(8,4));ax.scatter(concentration,absorbance,label="Simulated observations")
grid=np.linspace(0,80,101);ax.plot(grid,intercept+slope*grid,label="OLS calibration")
ax.set(xlabel="Declared concentration (µmol/L)",ylabel="Simulated absorbance",title="Beer–Lambert teaching calibration");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Inspect residuals before inversion','反算前检查残差','Residuals are observed minus fitted absorbance. The declared noise model is constant-variance Gaussian noise; the plot can reveal deviations if you change the simulation. Residual SD is not automatically a traceable instrument uncertainty.','残差为观测减去拟合吸光度。声明的噪声为恒方差高斯噪声；修改模拟后，可用图检查偏离。残差标准差不自动等于可追溯仪器不确定性。','''fig,ax=plt.subplots(figsize=(8,4));ax.scatter(fitted["fitted"],fitted["residual"])
ax.axhline(0,color="black",linestyle="--");ax.set(xlabel="Fitted absorbance",ylabel="Observed − fitted absorbance",title="Simulated calibration residual audit");plt.tight_layout();plt.show()
print("Fitted absorptivity (L/mol/cm):",slope*1e6/p["path_length_cm"],"; fitted blank:",intercept)'''),
 step('Propagate calibration and unknown-measurement variation','传播校准及未知测量的变异','Simulate three unknown absorbance replicates. Draw the calibration coefficients from their estimated covariance and unknown mean from its conditional Gaussian model. This produces a model-based interval, conditional on the calibration and noise assumptions, not a universal assay guarantee.','模拟三次未知样本吸光度。按估计协方差抽取校准系数，并按条件高斯模型抽取未知均值。所得区间依赖校准及噪声假设，不构成普遍实验保证。','''unknown_truth=p["unknown_concentration_mol_per_L"]*1e6
unknown_replicates=p["blank_absorbance"]+p["absorptivity_L_per_mol_cm"]*p["path_length_cm"]*unknown_truth*1e-6+rng.normal(0,p["noise_sd_absorbance"],3)
unknown_mean=float(unknown_replicates.mean());point=(unknown_mean-intercept)/slope
coefficient_draws=rng.multivariate_normal(fitted["coefficients"],fitted["covariance"],size=5000)
measurement_draws=rng.normal(unknown_mean,np.sqrt(fitted["variance"]/3),5000)
valid=coefficient_draws[:,1]>0
concentration_draws=(measurement_draws[valid]-coefficient_draws[valid,0])/coefficient_draws[valid,1]
interval=np.quantile(concentration_draws,[.025,.975])
fig,ax=plt.subplots(figsize=(8,4));ax.hist(concentration_draws,bins=40,edgecolor="white")
ax.axvspan(*interval,color="orange",alpha=.2,label="Conditional 95% range");ax.axvline(unknown_truth,color="black",linestyle="--",label="Known simulation truth")
ax.set(xlabel="Inverted concentration (µmol/L)",ylabel="Propagation draws",title="Conditional calibration uncertainty");ax.legend();plt.tight_layout();plt.show()
print("Unknown estimate (µmol/L):",point,"; conditional interval:",interval,"; rejected nonpositive slopes:",int((~valid).sum()))'''),
 step('Reconcile the fit and export all assumptions','核对拟合并导出全部假设','Check residual orthogonality and agreement of the slope with a direct centred formula. Do not silently clip negative concentration draws or force the interval to contain the known simulated truth. Save the seed, noise, units and full coefficient covariance.','检查残差正交性，并用直接中心化公式核对斜率。不静默裁剪负浓度抽样，也不强制区间包含已知模拟真值。保存种子、噪声、单位及完整系数协方差。','''direct_slope=np.sum((concentration-concentration.mean())*(absorbance-absorbance.mean()))/np.sum((concentration-concentration.mean())**2)
assert np.isclose(slope,direct_slope)
assert np.linalg.norm(np.column_stack([np.ones(len(concentration)),concentration]).T@fitted["residual"])<1e-9
assert np.isfinite(concentration_draws).all() and interval[0]<=interval[1]
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"concentration_micromol_per_L":concentration,"simulated_absorbance":absorbance,"fitted_absorbance":fitted["fitted"],"residual":fitted["residual"]}).to_csv(OUTPUT_DIR/"simulated-calibration.csv",index=False)
pd.DataFrame({"concentration_draw_micromol_per_L":concentration_draws}).to_csv(OUTPUT_DIR/"conditional-propagation.csv",index=False)
(OUTPUT_DIR/"calibration-model.json").write_text(json.dumps({"seed":models["seed"],"declared_simulation":p,"coefficient_units":["absorbance","absorbance per micromol/L"],"coefficients":fitted["coefficients"].tolist(),"covariance":fitted["covariance"].tolist(),"unknown_point_micromol_per_L":point,"conditional_95_micromol_per_L":interval.tolist()},indent=2))
print("Calibration checks passed; exports:",OUTPUT_DIR)''')]

EXERCISES={}
notes=[
 (['Compare atom fraction and mass fraction for ethanol.','Explain why this is not monoisotopic mass.','Mass fractions weight each element count by the declared average atomic weight. The table uses rounded average weights, not individual isotope masses.','Using standard-library re plus NumPy/Pandas/Matplotlib, add a clear atom-fraction chart for the same eight CIDs.','Using the same packages, annotate mass reconstruction differences and list unsupported formula syntax explicitly.','Mass fractions sum to one, reconstruction uses the saved weight table and unsupported grouped/charged formulas raise errors.'],['比较乙醇的原子分数与质量分数。','解释为何这不是单同位素质量。','质量分数按声明的平均原子量加权元素数量。本表用舍入平均量，不是特定同位素质量。','仅用标准库 re、NumPy、Pandas、Matplotlib，为同八个 CID 增加原子分数图。','使用同样的包标注质量重建差，并明确列出不支持的分子式语法。','质量分数和为一，使用保存的原子量表，分组/电荷语法报错。']),
 (['Distinguish degree, bond-type code and valence.','Explain cycle rank of benzene.','Degree counts neighbors. A reported bond type is a source code, not an energy. A connected benzene graph has one independent topological cycle.','Using NumPy/Pandas/Matplotlib/NetworkX, draw another declared CID and retain source atom IDs and formal charges.','Using the same packages, export every declared graph to GraphML with only scalar attributes.','Header counts, total charge and graph invariants reconcile; duplicate and self bonds are rejected.'],['区分图度数、键型代码与价。','解释苯的环秩。','度数计邻居，来源键型代码不是能量。连通的苯图有一个独立拓扑环。','仅用 NumPy、Pandas、Matplotlib、NetworkX 绘制另一个声明 CID，保留原子 ID 与形式电荷。','使用同样的包将各声明图导出为 GraphML，仅使用标量属性。','头数量、总电荷和图不变量一致，重复/自身键报错。']),
 (['Why separate source bonds from close geometric pairs?','Why does one calculated conformer not represent solution dynamics?','Short distance alone is not a declared bond. The snapshot is a computed model and omits an environmental ensemble, dynamics and experiment.','Using NumPy/SciPy/Matplotlib/py3Dmol, color atoms by element and label source atom indices without implying biological binding.','Using the same packages, compare H-containing versus heavy-only bond-length distributions.','Distances are symmetric with zero diagonal, source SDF is preserved and units remain ångströms.'],['为何区分来源键与几何短距离对？','为何单一计算构象不代表溶液动态？','短距离本身不是声明的键。快照是计算模型，没有环境构象集合、动力学或实验。','仅用 NumPy、SciPy、Matplotlib、py3Dmol 按元素着色并标原子索引，不暗示生物结合。','使用同样的包比较含氢和仅重原子的键长分布。','距离对称、对角为零，保留来源 SDF，单位保持埃。']),
 (['Explain the half-equivalence comparison.','Where does the stoichiometric buffer approximation fail?','Half-neutralized ideal weak acid has similar HA/A− amounts, so pH is near pKa. Initial/equivalence conditions cannot use the simple stoichiometric ratio expression.','Using NumPy/SciPy/Matplotlib, compare pKa=4.0, 4.76 and 5.5 with the same acid/base amounts.','Using the same packages, add a charge-residual panel without clipping the pH curve.','Mass fractions stay in [0,1], charge balance passes and all volumes/concentrations are declared.'],['解释半当量比较。','化学计量缓冲近似在哪些区域失效？','理想弱酸半中和时 HA/A− 数量相近，pH 接近 pKa。起始/当量条件不能使用简单化学计量比值式。','仅用 NumPy、SciPy、Matplotlib 比较 pKa=4.0、4.76、5.5，保持相同酸碱量。','使用同样的包增加电荷残差图，不裁剪 pH 曲线。','分数在 [0,1]，电荷平衡通过，声明全部体积与浓度。']),
 (['Distinguish reference-correlated pressure from a new measurement.','What assumptions support the apparent enthalpy slope?','IAPWS is an attributed reference correlation. The slope interpretation assumes ideal vapor, negligible liquid volume and an enthalpy approximation; it is not exact near critical conditions.','Using NumPy/Pandas/Matplotlib, compare linear-fit intervals 280–320 and 320–370 K within the valid correlation range.','Using the same packages, add a normal-pressure boiling root using SciPy brentq and explicit Pa/K units.','Reference benchmarks and range guards pass, pressure is absolute and derived quantities retain approximation labels.'],['区分参考关联压力与新测量。','表观焓斜率依赖哪些假设？','IAPWS 是署名的参考关联式。斜率解释假定理想蒸气、忽略液体体积及焓近似，临界附近并不精确。','仅用 NumPy、Pandas、Matplotlib 在有效范围比较 280–320 与 320–370 K 的线性拟合。','使用同样的包并允许 SciPy brentq，增加标准绝对压力下的沸点求根，注明 Pa/K。','参考点和范围约束通过，压力为绝对量，派生量保留近似标签。']),
 (['Why keep an intercept in the calibration?','Why is the propagated interval conditional?','The blank/background contributes an intercept. The interval depends on the specified linear/noise model and estimated coefficient covariance; it does not guarantee every real assay.','Using NumPy/Pandas/Matplotlib, compare two stated noise levels with the same concentration design and independent recorded seeds.','Using the same packages, export unknown replicates and separate measurement-only from calibration-plus-measurement propagation.','Keep explicit simulated-data labels, concentration/absorbance units, original seeds and the full covariance; do not force coverage of truth.'],['为何校准需要保留截距？','为何传播区间具有条件性？','空白/背景贡献截距。区间依赖线性/噪声模型及估计系数协方差，不保证每次真实实验。','仅用 NumPy、Pandas、Matplotlib，在相同浓度设计下比较两个声明噪声水平，记录独立种子。','使用同样的包导出未知重复，分别做仅测量与校准加测量的传播。','明确模拟数据、浓度/吸光度单位、种子及完整协方差，不强制覆盖真值。'])]
for c,(en,zh) in zip(COURSES,notes):EXERCISES[c['id']]=exercises(en,zh)
