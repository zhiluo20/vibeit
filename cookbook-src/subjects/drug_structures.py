"""Paired experimental examples: a chemical drug pocket and an antibody interface."""
from ._common import lesson, step, exercises, bilingual

PACKAGES = ['numpy','pandas','scipy','matplotlib','py3Dmol','IPython']
METHODS = ['parse_pdb','residue_minimum_distances','residue_labels','pdb_atom_text']
IMPORTS = 'import py3Dmol\nfrom scipy.spatial.distance import cdist\n'
COURSES = [
    lesson('07-imatinib-pocket',7,'imatinib-binding-pocket',
        'How imatinib occupies an ABL kinase pocket','伊马替尼如何占据 ABL 激酶口袋',
        'Inspect an experimentally observed drug pose in 1IEP, measure its pocket, and separate geometric contacts from affinity and efficacy.',
        '观察 1IEP 中实验测定的药物姿态，测量结合口袋，区分几何接触、亲和力与药效。',
        ['imatinib'],METHODS,'drug-binding','Drug–protein binding','药物与蛋白结合',
        discipline='bioinformatics',minutes=60,packages=PACKAGES,setup_imports=IMPORTS,
        data_kind='measured',interactive_3d=True,scroll_tables=True,icon='💊',data_version='snapshot-2026-10-10',
        keywords='imatinib 伊马替尼 ABL kinase 激酶 药物 结合口袋 小分子 ATP STI 1IEP'),
    lesson('08-trastuzumab-interface',8,'antibody-target-interface',
        'How a trastuzumab Fab recognizes HER2','曲妥珠单抗 Fab 如何识别 HER2',
        'Read the antibody–target complex 1N8Z, locate its protein interface, and compare surface recognition with small-molecule pocket binding.',
        '解读抗体与靶蛋白复合物 1N8Z，定位蛋白界面，与小分子的口袋结合进行比较。',
        ['trastuzumab'],METHODS,'drug-binding','Drug–protein binding','药物与蛋白结合',
        discipline='bioinformatics',minutes=60,packages=PACKAGES,setup_imports=IMPORTS,
        data_kind='measured',interactive_3d=True,scroll_tables=True,icon='🧩',data_version='snapshot-2026-10-10',
        keywords='trastuzumab 曲妥珠单抗 Herceptin HER2 抗体 生物药 Fab 表位 界面 1N8Z'),
]

COURSES[0]['online_url']='https://data.rcsb.org/rest/v1/core/entry/1IEP'
COURSES[1]['online_url']='https://data.rcsb.org/rest/v1/core/entry/1N8Z'
COURSES[0]['data_note']=bilingual(
    '1IEP is an X-ray structure (2.10 Å) of **mouse c-Abl kinase domain**, not a complete human BCR–ABL fusion. STI is imatinib. The asymmetric unit contains two kinase copies; use author chain A and its own STI, not an inferred A/B dimer. The coordinates and RCSB identity metadata are frozen. This is analysis of an observed complex, not docking. No hydrogens, solvent energetics, affinity or clinical response are reconstructed.',
    '1IEP 是 **鼠源 c-Abl 激酶结构域**的 X 射线结构（2.10 Å），不是完整的人 BCR–ABL 融合蛋白。STI 是伊马替尼。不对称单元含两个激酶副本；本课选作者链 A 及其自身的 STI，不把 A/B 自动解释为二聚体。坐标及 RCSB 身份注释均已冻结。本课分析已观测的复合物，不进行对接，也不重建氢原子、溶剂能量、亲和力或临床反应。')
COURSES[1]['data_note']=bilingual(
    '1N8Z is an X-ray complex (2.52 Å): author chain A is the trastuzumab Fab light chain, B the Fab heavy chain, and C the human HER2 extracellular construct. This is **one Fab, not a complete IgG**; neither Fc nor the membrane/intracellular kinase domain is present. Trastuzumab is a [humanized IgG1 antibody](https://www.gene.com/download/pdf/herceptin_prescribing.pdf). RCSB labels these mixed-source entities chimeric; that database flag should not be substituted for the therapeutic antibody classification. NAG is a sugar component, not the antibody drug. Use deposited author residue numbers including insertion codes; do not invent CDR or clinical numbering assignments.',
    '1N8Z 是 X 射线复合物（2.52 Å）：作者链 A 是曲妥珠单抗 Fab 轻链，B 是 Fab 重链，C 是人 HER2 胞外区构建体。这是**一个 Fab，不是完整 IgG**；没有 Fc、细胞膜或胞内激酶结构域。曲妥珠单抗是[人源化 IgG1 抗体](https://www.gene.com/download/pdf/herceptin_prescribing.pdf)。RCSB 对鼠/人多来源实体使用 chimeric 标记，这个数据库标记不能替代治疗抗体的分类。NAG 是糖组分，不是抗体药物。保留作者残基编号和插入码，不自行推定 CDR 或临床编号对应关系。')

AUDIT = '''data = snapshot(KEY)
atoms = parse_pdb(data["pdb"])
heavy = atoms[(atoms.occupancy > 0) & ~atoms.element.isin(["H", "D"])].copy()
assert heavy.serial.is_unique
ca = heavy[(heavy.record == "ATOM") & (heavy.atom == "CA")]
identity = []
for entity in data["entities"]:
    for chain in entity["entity_poly"]["pdbx_strand_id"].split(","):
        identity.append(dict(chain=chain, molecule=entity["rcsb_polymer_entity"]["pdbx_description"],
            deposited_sequence_length=entity["entity_poly"]["rcsb_sample_sequence_length"],
            observed_CA_residues=int((ca.chain == chain).sum())))
display(pd.DataFrame(identity))
print("PDB:", data["pdb_id"], "; resolution (Å):", data["entry"]["rcsb_entry_info"]["resolution_combined"])
print("Revision:", data["entry"]["rcsb_accession_info"]["revision_date"])
print("Selected atom rows:", len(atoms), "; usable heavy atoms:", len(heavy),
      "; zero occupancy:", int((atoms.occupancy == 0).sum()))
print("Non-polymer components:", sorted(atoms.loc[atoms.record == "HETATM", "residue"].unique()))'''

CHECKS = '''# Independent atom-pair calculation for the closest residue pair.
i, j = np.unravel_index(np.argmin(distances), distances.shape)
def residue_atoms(frame, row):
    return frame[(frame.chain == row.chain) & (frame.resnum == row.resnum) &
                 (frame.icode == row.icode) & (frame.residue == row.residue)]
left_test = residue_atoms(drug, left_residues.iloc[i])
right_test = residue_atoms(target, right_residues.iloc[j])
manual_minimum = min(float(np.linalg.norm(a-b))
    for a in left_test[["x","y","z"]].to_numpy() for b in right_test[["x","y","z"]].to_numpy())
assert np.isclose(manual_minimum, distances[i,j], atol=1e-12)
# A common rigid translation cannot change any distance.
shifted_drug = drug.copy(); shifted_target = target.copy()
shifted_drug[["x","y","z"]] += np.array([10., -7., 3.])
shifted_target[["x","y","z"]] += np.array([10., -7., 3.])
_, _, shifted_distances = residue_minimum_distances(shifted_drug, shifted_target)
assert np.allclose(distances, shifted_distances, atol=1e-12)
# Empty selections fail explicitly; a zero-contact threshold is a valid result.
try:
    residue_minimum_distances(drug.iloc[:0], target)
except ValueError:
    print("Empty selection: reported correctly")
else:
    raise AssertionError("Empty selection was accepted")
assert not (distances <= 0.01).any()
assert np.isfinite(distances).all() and (distances >= 0).all()
print("PASS: independent atom minimum, rigid translation, finite distances, empty selections and empty contacts")'''

EXPORT = '''OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
target_profile.to_csv(OUTPUT_DIR / "target-residue-distances.csv", index=False)
threshold_table.to_csv(OUTPUT_DIR / "threshold-sensitivity.csv", index=False)
pd.DataFrame(distances, index=residue_labels(left_residues), columns=residue_labels(right_residues)).to_csv(
    OUTPUT_DIR / "residue-minimum-distances.csv")
(OUTPUT_DIR / "selected-complex.pdb").write_text(pdb_atom_text(pd.concat([target, drug])), encoding="ascii")
summary = dict(pdb_id=data["pdb_id"], cutoff_angstrom=CUTOFF,
    atom_selection="positive occupancy heavy atoms; parser selects one altloc per atom",
    target_chains=sorted(target.chain.unique()), drug_chains=sorted(drug.chain.unique()),
    target_residues_within_cutoff=int((target_profile.min_distance_A <= CUTOFF).sum()),
    contacting_residue_pairs=int((distances <= CUTOFF).sum()),
    method="minimum atom distance, not affinity, interaction energy or buried surface area")
(OUTPUT_DIR / "analysis-summary.json").write_text(json.dumps(summary, indent=2)+"\\n")
print("Exported:", sorted(p.name for p in OUTPUT_DIR.iterdir()))'''

SECTIONS = {}
SECTIONS['07-imatinib-pocket'] = [
    step('Why analyze this drug complex?','为什么分析这个药物复合物？',
        'Start with a classroom question: **how can a small molecule alter the action of a much larger protein?** Think of a machine with an ATP slot: imatinib occupies the kinase pocket and stabilizes an inactive conformation. The analogy explains location, but proteins and drugs are flexible and water matters. The mechanistic interpretation comes from the [primary study](https://pubmed.ncbi.nlm.nih.gov/12154025/) and [PDB-101](https://pdb101.rcsb.org/motm/283); our calculations locate the observed pose and nearby residues. Heme is a natural cofactor; imatinib is an externally supplied inhibitor. Spatial analysis is shared, biological purpose differs. Learning goals: verify the drug/construct, rotate its bound pose, define a heavy-atom pocket, inspect contact thresholds, and state what evidence is still needed for inhibition and affinity.',
        '先提出课堂问题：**一个小分子，怎样改变大蛋白的工作？** 可以把激酶比作带有 ATP 插槽的机器：伊马替尼占据口袋，并稳定一种非活性构象。这个类比帮助理解位置，但蛋白和药物会运动，水也参与结合。机制解释来自[原始研究](https://pubmed.ncbi.nlm.nih.gov/12154025/)与 [PDB-101](https://pdb101.rcsb.org/motm/283)；我们的计算定位实验姿态和邻近残基。血红素是天然辅因子，伊马替尼是外源抑制剂；两者共享空间分析方法，生物学目的不同。学习目标：核验药物与构建体、旋转结合姿态、定义重原子口袋、检查阈值，以及说明还需要哪些证据才能讨论抑制作用和亲和力。'),
    step('Verify protein, drug and experimental coordinates','核验蛋白、药物与实验坐标',
        'Use the deposited metadata rather than inferring species from a familiar drug name. The table separates sequence length from observed Cα residues: unresolved atoms/residues are not zeros and missing coordinates cannot be analyzed. Choose the first model and highest-occupancy alternate atom (the parser documents its tie rule); exclude zero-occupancy rows and H/D. This atom-wise altloc rule is a teaching approximation, not a full joint conformer reconstruction. All coordinates are in the same experimentally refined reference frame.',
        '不要根据熟悉的药名推断物种，先读提交记录。表格将序列长度与已建模 Cα 残基数分开：未解析的原子或残基不能填成零，也不能计算不存在的坐标。选择第一个模型、每个原子占有率最高的替代构象（平局规则见解析函数），排除零占有率与 H/D。逐原子选替代构象是教学近似，不能视作完整联合构象重建。所有坐标来自同一个实验精修坐标系。',
        'KEY = "imatinib"\n'+AUDIT+'''
compound = data["compound"]["chem_comp"]
display(pd.DataFrame([dict(component=compound["id"], formula=compound["formula"],
    formula_weight_Da=compound["formula_weight"], formal_charge=compound["pdbx_formal_charge"])]))
drug = heavy[(heavy.chain == "A") & (heavy.residue == "STI")].copy()
target = heavy[(heavy.chain == "A") & (heavy.record == "ATOM")].copy()
assert len(drug) == 37 and not target.empty
print("Bound drug heavy atoms:", len(drug), "; protein heavy atoms:", len(target))'''),
    step('Rotate the drug alone, then inside the protein','先看药物，再看药物位于蛋白中的位置',
        'The first view shows **the drug coordinates extracted from the complex**: it is the observed bound pose, not a free-solution conformer or a docking prediction. The second view shows green ABL cartoon and orange drug sticks. Hover atom labels to connect atom names to the distance matrix later. py3Dmol may infer bonds for rendering; no inferred bond is used as an interaction-energy calculation. Hydrogens are absent in this coordinate selection; the CCD formula includes them.',
        '第一幅三维图展示**从复合物中提取的药物坐标**：它是实验观察到的结合姿态，不是游离溶液构象，也不是对接预测。第二幅显示绿色 ABL cartoon 与橙色药物 sticks。悬停查看原子名，随后对应距离矩阵。py3Dmol 会为绘图推定部分键连接；这些绘图连接不参与相互作用能计算。选取坐标没有氢，CCD 化学式仍包含氢。',
        '''drug_view = py3Dmol.view(width="100%", height=350)
drug_view.addModel(pdb_atom_text(drug), "pdb")
drug_view.setStyle({}, {"stick":{"colorscheme":"orangeCarbon"}})
drug_view.setHoverable({}, True, "function(a,v){if(!a.label)a.label=v.addLabel(a.atom,{position:a,backgroundColor:'white',fontColor:'black'});}",
    "function(a,v){if(a.label){v.removeLabel(a.label);delete a.label;}}")
drug_view.setBackgroundColor("white"); drug_view.zoomTo(); drug_view.zoom(.7)
display(HTML(drug_view._make_html()))
complex_view = py3Dmol.view(width="100%", height=440)
complex_view.addModel(pdb_atom_text(pd.concat([target, drug])), "pdb")
complex_view.setStyle({"chain":"A"}, {"cartoon":{"color":"#18785f"}})
complex_view.setStyle({"resn":"STI"}, {"stick":{"colorscheme":"orangeCarbon"}})
complex_view.setBackgroundColor("white"); complex_view.zoomTo(); complex_view.zoom(.7)
display(HTML(complex_view._make_html()))'''),
    step('Define and measure the pocket','定义并测量口袋',
        'For residue r and drug L, calculate **d(r,L) = min ||xᵢ − xⱼ||**, over all selected heavy-atom pairs. Report residues at **≤4.0 Å**; 1 Å = 0.1 nm. This is a declared geometric cutoff, not a universal bond boundary. A Cα distance is unsuitable for this pocket: a side chain can approach the drug while its Cα stays farther away. The bar chart uses one minimum per residue, in Å; the dashed line is the chosen cutoff. It identifies the local environment, not energetic contribution.',
        '对残基 r 与药物 L，计算 **d(r,L) = min ||xᵢ − xⱼ||**，遍历选定的重原子对。报告 **≤4.0 Å** 的残基；1 Å = 0.1 nm。这是明确的几何阈值，不是通用成键边界。口袋分析不宜只用 Cα 距离：侧链可能靠近药物，而 Cα 更远。柱形图每个残基一个最短距离，单位 Å，虚线表示阈值。它描述局部环境，不能衡量每个残基的能量贡献。',
        '''CUTOFF = 4.0
left_residues, right_residues, distances = residue_minimum_distances(drug, target)
target_profile = right_residues.copy()
target_profile["label"] = residue_labels(right_residues)
target_profile["min_distance_A"] = distances.min(axis=0)
pocket = target_profile[target_profile.min_distance_A <= CUTOFF].sort_values("min_distance_A", kind="stable")
print("Pocket residues:", len(pocket))
display(pocket.head(12))
fig, ax = plt.subplots(figsize=(8,5))
if len(pocket):
    ax.barh(pocket.label.iloc[::-1], pocket.min_distance_A.iloc[::-1], color="#18785f")
else:
    ax.text(.5,.5,"No residues within cutoff",ha="center",transform=ax.transAxes)
ax.axvline(CUTOFF, color="#bc6541", linestyle="--", label=f"Cutoff {CUTOFF:g} Å")
ax.set(xlabel="Minimum heavy-atom distance (Å)", title="1IEP: ABL residues near imatinib")
ax.legend(); plt.tight_layout(); plt.show()''',cover=True),
    step('Which drug atoms approach which residues?','哪些药物原子靠近哪些残基？',
        'The heatmap retains drug atom names and author residue IDs. Each cell is the minimum distance from one drug atom to all heavy atoms of one pocket residue. Darker cells are closer, with the displayed scale capped at 8 Å. There can be many nearby pairs for one residue: pair counts and residue counts have different denominators. A short N/O distance is only a candidate polar contact. Protonation, donor/acceptor chemistry, angles, missing hydrogens and water must be considered before assigning a hydrogen bond. Do not label every N/O atom a hydrogen-bond donor.',
        '热图保留药物原子名和作者残基编号。每格是一个药物原子到一个口袋残基全部重原子的最短距离。颜色越深距离越近，色阶显示上限为 8 Å。一个残基可以对应多个邻近原子对，原子对数与残基数的分母不同。短的 N/O 距离只能提示候选极性接触；判断氢键还需考虑质子化、供受体性质、角度、缺失的氢与水，不能把所有 N/O 原子都标为氢键供体。',
        '''atom_to_target = cdist(drug[["x","y","z"]].to_numpy(), target[["x","y","z"]].to_numpy())
groups = list(target.reset_index(drop=True).groupby(["chain","resnum","icode","residue"], sort=False).indices.values())
atom_residue = np.column_stack([atom_to_target[:,indices].min(axis=1) for indices in groups])
assert np.allclose(atom_residue.min(axis=0), target_profile.min_distance_A)
selected = np.flatnonzero(target_profile.min_distance_A.to_numpy() <= CUTOFF)
fig, ax = plt.subplots(figsize=(10,7))
if len(selected):
    image = ax.imshow(atom_residue[:,selected], aspect="auto", cmap="viridis_r", vmin=2, vmax=8)
    ax.set(xticks=range(len(selected)), xticklabels=target_profile.label.iloc[selected],
           yticks=range(len(drug)), yticklabels=drug.atom)
    plt.setp(ax.get_xticklabels(), rotation=70, ha="right")
    fig.colorbar(image, ax=ax, label="Minimum atom-to-residue distance (Å; scale capped at 8)")
else:
    ax.text(.5,.5,"Empty pocket at this cutoff",ha="center",transform=ax.transAxes)
ax.set(xlabel="ABL author residue ID", ylabel="STI drug atom name", title="Observed drug–pocket geometry")
plt.tight_layout(); plt.show()'''),
    step('Show the pocket in space','在空间中标出口袋',
        'Green points are protein Cα positions; orange points are imatinib heavy atoms. Purple points mark Cα of the residues selected by the **heavy-atom** cutoff. The axes use deposited coordinates in Å; the viewing direction has no physiological meaning. The additional close-up shows the selected pocket atoms in purple and drug in orange, labelling the four closest residues without moving their coordinates. Residues separated along the sequence can meet around the same drug in the folded structure.',
        '绿色点是蛋白 Cα，橙色点是药物重原子，紫色点是通过**重原子**阈值选出口袋残基的 Cα。坐标轴为提交的 Å 坐标，观察方向没有生理含义。新增的局部放大视图以紫色显示所选口袋原子、橙色显示药物，标注最近的四个残基，不改变坐标。序列上相隔很远的残基，可以在折叠后共同围绕同一个药物。',
        '''target_ca = target[target.atom == "CA"].copy()
target_ca["label"] = residue_labels(target_ca)
pocket_ca = target_ca[target_ca.label.isin(pocket.label)]
fig = plt.figure(figsize=(8,5)); ax = fig.add_subplot(111, projection="3d")
ax.scatter(target_ca.x,target_ca.y,target_ca.z,s=8,c="#18785f",alpha=.25,label="ABL Cα")
ax.scatter(drug.x,drug.y,drug.z,s=25,c="#bc6541",label="Imatinib heavy atoms")
ax.scatter(pocket_ca.x,pocket_ca.y,pocket_ca.z,s=30,c="#9974a5",label="Pocket residue Cα")
ax.set(xlabel="x (Å)",ylabel="y (Å)",zlabel="z (Å)",title="Sequence-distant residues form a drug pocket")
xyz=target[["x","y","z"]].to_numpy(); ax.set_box_aspect(np.ptp(xyz,axis=0))
ax.legend(loc="upper left"); plt.tight_layout(); plt.show()
target_labels = pd.Series(residue_labels(target), index=target.index)
pocket_atoms = target[target_labels.isin(pocket.label)]
pocket_view = py3Dmol.view(width="100%", height=440)
pocket_view.addModel(pdb_atom_text(pd.concat([pocket_atoms, drug])), "pdb")
pocket_view.setStyle({}, {"stick":{"color":"#9974a5","radius":.14}})
pocket_view.setStyle({"resn":"STI"}, {"stick":{"colorscheme":"orangeCarbon","radius":.2}})
for row in pocket.iloc[:4].itertuples():
    position = pocket_ca[pocket_ca.label == row.label]
    if len(position):
        r = position.iloc[0]
        pocket_view.addLabel(row.label, {"position":{"x":float(r.x),"y":float(r.y),"z":float(r.z)},
            "backgroundColor":"white","fontColor":"black","fontSize":12,"backgroundOpacity":.8})
pocket_view.setBackgroundColor("white"); pocket_view.zoomTo(); pocket_view.zoom(.7)
display(HTML(pocket_view._make_html()))
print("Close-up atoms:", len(pocket_atoms)+len(drug))'''),
    step('Check sensitivity and interpretation','检查阈值敏感性与结果解释',
        'At a fixed experimental pose, increasing the cutoff can only add residues. The curve therefore measures how our definition changes; it is not a drug dose–response curve. Ask students: what can we conclude? “The observed imatinib pose is surrounded by these ABL residues under this selection.” What else is needed? Binding assays for affinity, kinase assays for inhibition, and cellular/selectivity evidence for biological action. This structure alone does not establish potency, resistance or patient benefit. Author numbering is retained; a clinical mutation requires an explicit species/isoform sequence map first.',
        '固定实验姿态下，增加阈值只能增加所选残基；曲线表示定义如何变化，**不是药物剂量反应曲线**。问学生：能得出什么结论？“在当前选择规则下，实验中的伊马替尼姿态被这些 ABL 残基包围。”还需要什么？亲和力需结合实验，抑制作用需激酶实验，生物效应需细胞与选择性证据。单个结构不能证明效力、耐药或患者获益。这里保留作者编号；讲临床突变前必须建立物种与异构体的序列编号映射。',
        '''threshold_table = pd.DataFrame([dict(cutoff_A=t,
    target_residues=int((target_profile.min_distance_A <= t).sum())) for t in [0.01,3.,3.5,4.,4.5,5.,6.]])
assert np.all(np.diff(threshold_table.target_residues) >= 0)
display(threshold_table)
fig,ax=plt.subplots(figsize=(7,3))
ax.plot(threshold_table.cutoff_A,threshold_table.target_residues,"o-",color="#416aa6")
ax.axvline(CUTOFF,ls="--",color="#bc6541")
ax.set(xlabel="Geometric cutoff (Å)",ylabel="Unique ABL residues",title="Definition sensitivity; not dose–response")
plt.tight_layout(); plt.show()'''),
    step('Validate and export','校验并导出',
        'Independently recompute the closest atom pair and translate the whole complex: distances must agree. Export the selected complex, complete residue distances, cutoff curve and summary. The CSV units are Å. Failed selections report errors; valid zero-contact results remain empty rather than being replaced with invented contacts. Keep the immutable snapshot and record parameter changes.',
        '独立重算最近的原子对，再整体平移复合物：距离应一致。导出所选复合物、完整残基距离、阈值曲线与摘要；CSV 距离单位为 Å。错误选择会报错；有效的零接触结果保持为空，不补入虚构接触。保留冻结快照并记录参数修改。',CHECKS+'\n'+EXPORT),
]

SECTIONS['08-trastuzumab-interface'] = [
    step('Why compare an antibody with a chemical drug?','为什么把抗体和化学药物放在一起比较？',
        'A small-molecule drug can enter a protein pocket; an antibody Fab recognizes a **surface patch** using a protein interface. Think of a shaped connector meeting a matching surface rather than a tiny object entering a slot. Both cases ask where components meet in 3D, but their size, chemistry and biological mechanisms differ. Here locate the binding surface observed in 1N8Z and determine whether light chain, heavy chain or both contribute geometric contacts. The [primary study](https://doi.org/10.1038/nature01392) places Herceptin binding near the membrane-proximal region of HER2. The structure does not depict a membrane or all mechanisms of a full therapeutic antibody.',
        '小分子药物可以进入蛋白口袋；抗体 Fab 通过蛋白界面识别**表面区域**。可以把它比作形状互补的接头贴合表面，帮助学生联想“插槽”和“表面识别”的区别。两种分析都问组分在三维空间哪里相遇，但大小、化学性质与生物机制不同。本课定位 1N8Z 中的结合表面，检查轻链、重链是否都贡献几何接触。[原始研究](https://doi.org/10.1038/nature01392)将 Herceptin 结合位置定位于 HER2 靠近膜的区域；这个结构没有画出细胞膜，也不能展示完整治疗抗体的全部机制。'),
    step('Read chain identity before coloring the model','先核验链身份，再给模型上色',
        'A/B are the Fab light/heavy chains and C is human HER2. The therapeutic component is therefore in **ATOM polymer chains**, not in the list of small HETATM ligands. NAG is a sugar; calling it the drug would invert the biological question. Deposited sequences include unresolved residues; the antibody author numbering also contains insertion codes. Use chain + residue number + insertion code as the identifier. Cα counts and deposited sequence lengths audit coordinate coverage but do not automatically enumerate every missing side-chain atom.',
        'A/B 为 Fab 轻链/重链，C 为人 HER2。这里的药物组分位于 **ATOM 聚合物链**中，而不在小分子 HETATM 清单里。NAG 是糖，将它叫作药物会误读研究问题。提交序列含未建模残基；抗体作者编号还含插入码。采用“链 + 残基编号 + 插入码”作为标识。Cα 数与提交序列长度用于检查坐标覆盖，不等于列出了全部缺失侧链原子。',
        'KEY = "trastuzumab"\n'+AUDIT+'''
drug = heavy[(heavy.record == "ATOM") & heavy.chain.isin(["A","B"])].copy()
target = heavy[(heavy.record == "ATOM") & (heavy.chain == "C")].copy()
assert set(drug.chain) == {"A","B"} and not target.empty
print("Fab heavy atoms:", len(drug), "; HER2 heavy atoms:", len(target))
print("Residues carrying insertion codes:",
      len(drug.loc[drug.icode != "", ["chain","resnum","icode"]].drop_duplicates()))'''),
    step('Rotate the experimentally observed complex','旋转实验观察到的复合物',
        'Green is HER2, orange the Fab light chain and blue the Fab heavy chain. This view uses only selected positive-occupancy protein heavy atoms; sugars and waters are omitted from this protein-interface analysis. Omission is an analysis choice, not evidence that they are biologically irrelevant. The two antibody chains approach a limited region of HER2. One Fab is an antigen-binding fragment; the Fc-mediated effects of a complete antibody cannot be analyzed from this fragment.',
        '绿色为 HER2，橙色为 Fab 轻链，蓝色为 Fab 重链。视图只使用选定的正占有率蛋白重原子；本次蛋白界面分析省略糖和水。省略是分析范围的选择，不能说明它们在生物学上无关。两条抗体链靠近 HER2 的局部区域。一个 Fab 是抗原结合片段，不能用这个片段分析完整抗体的 Fc 介导效应。',
        '''viewer = py3Dmol.view(width="100%",height=480)
viewer.addModel(pdb_atom_text(pd.concat([target,drug])),"pdb")
for chain,color in [("C","#18785f"),("A","#bc6541"),("B","#416aa6")]:
    viewer.setStyle({"chain":chain},{"cartoon":{"color":color}})
viewer.setBackgroundColor("white");viewer.zoomTo();viewer.zoom(.7)
display(HTML(viewer._make_html()))
fig=plt.figure(figsize=(8,5));ax=fig.add_subplot(111,projection="3d")
for chain,color,label in [("C","#18785f","HER2 C"),("A","#bc6541","Fab light A"),("B","#416aa6","Fab heavy B")]:
    frame=ca[ca.chain==chain]
    ax.scatter(frame.x,frame.y,frame.z,s=10,c=color,alpha=.6,label=label)
ax.set(xlabel="x (Å)",ylabel="y (Å)",zlabel="z (Å)",title="1N8Z: an antibody meets a target surface")
ax.set_box_aspect(np.ptp(pd.concat([target,drug])[["x","y","z"]].to_numpy(),axis=0))
ax.legend(loc="upper left");plt.tight_layout();plt.show()''',cover=True),
    step('Calculate a protein–protein interface','计算蛋白与蛋白的接触界面',
        'For each Fab/HER2 residue pair, take the minimum over all selected heavy-atom distances. A pair at **≤4 Å** is called a geometric contact in this lesson. The block-wise helper avoids allocating a full atoms × atoms × coordinates array on a phone. The table counts unique interface residues separately from residue-pair edges. One residue can touch several residues across the interface, so an edge count cannot be called an epitope size. This threshold-derived HER2 set is a geometric interface candidate, not a complete experimentally validated epitope.',
        '对每一对 Fab/HER2 残基，取全部选定重原子距离的最小值；本课将 **≤4 Å** 的残基对称为几何接触。分块函数避免在手机上创建巨大的“原子 × 原子 × 三坐标”数组。表格分别统计独立界面残基与残基对边数。一个残基可接触对面的多个残基，因此边数不能叫作表位大小。这个阈值定义的 HER2 集合是几何界面候选，不是完整且经过实验验证的表位。',
        '''CUTOFF=4.0
left_residues,right_residues,distances=residue_minimum_distances(drug,target)
left_profile=left_residues.copy();left_profile["label"]=residue_labels(left_residues)
left_profile["min_distance_A"]=distances.min(axis=1)
target_profile=right_residues.copy();target_profile["label"]=residue_labels(right_residues)
target_profile["min_distance_A"]=distances.min(axis=0)
contact_mask=distances<=CUTOFF
contributions=pd.DataFrame([dict(Fab_chain=chain,
    unique_Fab_residues=int(((left_profile.chain==chain)&(left_profile.min_distance_A<=CUTOFF)).sum()),
    residue_pair_edges=int(contact_mask[left_profile.chain.to_numpy()==chain].sum())) for chain in ["A","B"]])
display(contributions)
print("Unique HER2 interface residues:",int((target_profile.min_distance_A<=CUTOFF).sum()),
      "; residue-pair edges:",int(contact_mask.sum()))
display(target_profile[target_profile.min_distance_A<=CUTOFF].sort_values("min_distance_A").head(12))
fig,ax=plt.subplots(figsize=(6,3))
ax.bar(["Fab light A","Fab heavy B"],contributions.unique_Fab_residues,color=["#bc6541","#416aa6"])
ax.set(ylabel="Unique Fab residues within cutoff",title="Geometric contribution of each Fab chain (≤4 Å)")
plt.tight_layout();plt.show()'''),
    step('Inspect the interface contact matrix','查看界面接触矩阵',
        'Rows are Fab residues and columns are HER2 residues, retaining insertion letters. Show only residues that have at least one ≤4 Å partner. The color scale is minimum distance in Å, capped at 8 Å. A dark cell is spatial proximity, not a hydrogen bond, salt bridge or binding-energy contribution. Contacts near the interface can come from residues distant along either sequence. CDR assignments require a stated antibody numbering method and sequence annotation; this lesson preserves author IDs instead.',
        '行是 Fab 残基，列是 HER2 残基，保留插入字母。只显示至少存在一个 ≤4 Å 对侧伙伴的残基。色阶为最短距离 Å，上限显示为 8 Å。深色格子表示空间接近，不直接表示氢键、盐桥或结合能贡献。界面附近的残基可能在各自序列上相隔很远。划定 CDR 需要明确的抗体编号方法与序列注释；本课保留作者编号。',
        '''left_indices=np.flatnonzero(contact_mask.any(axis=1))
right_indices=np.flatnonzero(contact_mask.any(axis=0))
fig,ax=plt.subplots(figsize=(10,7))
if len(left_indices) and len(right_indices):
    image=ax.imshow(distances[np.ix_(left_indices,right_indices)],aspect="auto",cmap="viridis_r",vmin=2,vmax=8)
    ax.set(xticks=range(len(right_indices)),xticklabels=target_profile.label.iloc[right_indices],
        yticks=range(len(left_indices)),yticklabels=left_profile.label.iloc[left_indices])
    plt.setp(ax.get_xticklabels(),rotation=70,ha="right")
    fig.colorbar(image,ax=ax,label="Minimum heavy-atom distance (Å; scale capped at 8)")
else:
    ax.text(.5,.5,"No interface at this cutoff",ha="center",transform=ax.transAxes)
ax.set(xlabel="HER2 author residue ID",ylabel="Fab author residue ID",title="Antibody–target geometry; not interaction energy")
plt.tight_layout();plt.show()'''),
    step('Locate contact residues along HER2','沿 HER2 序列定位接触残基',
        'Every point is an observed HER2 residue, x = deposited author number and y = its minimum distance to any Fab heavy atom. Purple points meet the ≤4 Å definition. The cluster near the C-terminal part of this extracellular construct is consistent with the published membrane-proximal binding site. The membrane itself is absent, so use the publication for topology rather than claiming that the coordinate axis locates a membrane. Gaps in modeled residues are not bridged with a fitted curve.',
        '每点为一个已建模 HER2 残基：横轴是提交的作者编号，纵轴为到 Fab 任一重原子的最短距离；紫点满足 ≤4 Å 定义。靠近这个胞外构建体 C 端的接触簇，与文献报道的近膜结合位置相符。结构本身没有细胞膜，膜拓扑来自文献，不能宣称坐标轴确定了膜的位置。缺失的建模残基不通过拟合曲线补齐。',
        '''fig,ax=plt.subplots(figsize=(9,3))
ax.scatter(target_profile.resnum,target_profile.min_distance_A,s=9,c="#18785f",alpha=.6,label="Observed HER2 residues")
interface=target_profile[target_profile.min_distance_A<=CUTOFF]
ax.scatter(interface.resnum,interface.min_distance_A,s=28,c="#9974a5",label="Within cutoff")
ax.axhline(CUTOFF,ls="--",c="#bc6541")
ax.set(xlabel="HER2 deposited author residue number",ylabel="Minimum distance to Fab (Å)",title="A localized protein surface is recognized")
ax.legend();plt.tight_layout();plt.show()'''),
    step('Compare definitions, then compare mechanisms','比较接触定义，再比较机制',
        'Count Fab residues, HER2 residues and residue-pair edges at each cutoff. All counts must be nondecreasing, but absolute counts cannot compare the affinity of an antibody and a small molecule: their sizes and contact opportunities differ. The result supports a localized Fab/HER2 interface in this experimental structure. It does not establish which residue is an energetic hotspot, a dissociation constant, an Fc mechanism or clinical efficacy. Alanine scanning, SPR/BLI or other binding assays, and functional experiments answer different follow-up questions.',
        '分别统计各阈值下 Fab 残基、HER2 残基与残基对边数。它们应单调不减，但不能用绝对接触数量比较抗体与小分子的亲和力：两者尺寸及潜在接触机会不同。结果支持“这个实验结构存在局部 Fab/HER2 界面”。它不能确定能量热点、解离常数、Fc 机制或临床疗效。丙氨酸扫描、SPR/BLI 等结合实验，以及功能实验分别回答不同的后续问题。',
        '''threshold_table=pd.DataFrame([dict(cutoff_A=t,Fab_residues=int((distances.min(axis=1)<=t).sum()),
    HER2_residues=int((distances.min(axis=0)<=t).sum()),residue_pair_edges=int((distances<=t).sum()))
    for t in [0.01,3.,3.5,4.,4.5,5.,6.]])
assert np.all(np.diff(threshold_table[["Fab_residues","HER2_residues","residue_pair_edges"]],axis=0)>=0)
display(threshold_table)
fig,ax=plt.subplots(figsize=(7,3))
for column in ["Fab_residues","HER2_residues","residue_pair_edges"]:
    ax.plot(threshold_table.cutoff_A,threshold_table[column],"o-",label=column)
ax.axvline(CUTOFF,ls="--",c="#bc6541")
ax.set(xlabel="Geometric cutoff (Å)",ylabel="Count (denominator shown in legend)",title="Interface definition sensitivity")
ax.legend();plt.tight_layout();plt.show()'''),
    step('Validate, export and teach the analogy','校验、导出与课堂类比',
        'Repeat independent atom-pair and rigid-translation checks. Export complete distances and the coordinate subset. End the lesson by asking students to explain: heme is a cofactor within hemoglobin, imatinib is a small-molecule inhibitor in a kinase pocket, and a trastuzumab Fab is a protein drug fragment at a target surface. The common computational step is measuring geometry; causal mechanisms and affinity require separate evidence.',
        '重复独立原子对与整体平移校验，导出完整距离及坐标子集。课堂结束时请学生解释：血红素是血红蛋白的辅因子，伊马替尼是激酶口袋中的小分子抑制剂，曲妥珠单抗 Fab 是在靶蛋白表面结合的蛋白药物片段。共同计算步骤是测量几何关系；因果机制与亲和力需要另外的证据。',
        CHECKS+'\n'+EXPORT+'''
left_profile.to_csv(OUTPUT_DIR / "Fab-residue-distances.csv",index=False)
rows,cols=np.nonzero(contact_mask)
contact_edges=pd.DataFrame(dict(Fab_residue=np.array(residue_labels(left_residues))[rows],
    HER2_residue=np.array(residue_labels(right_residues))[cols],distance_A=distances[rows,cols]))
contact_edges.to_csv(OUTPUT_DIR / "interface-residue-pairs.csv",index=False)
print("Exported Fab profile and",len(contact_edges),"geometric interface edges")'''),
]

EXERCISES = {
    '07-imatinib-pocket':exercises([
        'Compare 3.5, 4.0 and 5.0 Å pockets. Why can membership change without a drug pose change?',
        'Recompute the closest pocket residue using Cα only. Why can it leave the heavy-atom pocket?',
        'Increasing a cutoff enlarges the geometric selection without changing chemistry. Cα is a backbone reference point, while side-chain atoms can make the nearest approach. More contacts do not imply better affinity.',
        'Using only the listed NumPy/Pandas/SciPy/Matplotlib/py3Dmol packages and standard library, add a CUTOFF control at 3.5/4/5 Å and recolor pocket atoms in the 3D complex. Preserve the data and author IDs; do not perform docking or report binding energies.',
        'Add a table of the nearest protein atom to each drug N/O atom using the selected experimental coordinates. Call entries candidate polar proximities, not proven hydrogen bonds. Keep atom names, residue IDs and Å units; use only the listed packages.',
        'Run all affected cells manually. Pocket counts must be nondecreasing; 3D atom selections must agree with the table. Recompute one N/O distance with np.linalg.norm and retain the existing snapshot and translation checks.'
    ],[
        '比较 3.5、4.0、5.0 Å 的口袋。为什么药物姿态不变，成员仍会改变？',
        '只使用 Cα，重算距离药物最近的口袋残基。为什么它可能不再满足重原子口袋定义？',
        '增加阈值改变几何选择，不改变化学。Cα 是骨架参考点，侧链原子可以更靠近药物。更多接触不能推出更高亲和力。',
        '只用本课列出的 NumPy/Pandas/SciPy/Matplotlib/py3Dmol 与标准库，增加 3.5/4/5 Å 的 CUTOFF 控制，并在三维复合物中给口袋原子重新上色。保留数据与作者编号，不进行对接、不报告结合能。',
        '利用所选实验坐标，给每个药物 N/O 原子列出最近的蛋白原子，称为候选极性邻近关系，不叫已证实氢键。保留原子名、残基编号与 Å 单位；只用已列包。',
        '手动运行全部受影响单元。口袋数量须单调不减，三维原子选择须与表格一致；用 np.linalg.norm 复算一项 N/O 距离，保留原有快照与平移校验。'
    ]),
    '08-trastuzumab-interface':exercises([
        'Compare unique HER2 residues with residue-pair edges. Why are these counts different?',
        'Set the contact cutoff to 0.01 Å. What should the table, graph and export report?',
        'A residue may have several partners; edges and unique residues have different denominators. At 0.01 Å the valid result is an empty interface with zero counts, explicit empty-state figures and header-only edge CSV, not invented contacts.',
        'Using only listed packages, highlight HER2 interface residues in the 3D model at 3.5/4/5 Å. Preserve author insertion codes and compare with the exported target profile. Do not label the result a validated epitope.',
        'Add separate minimum-distance profiles from HER2 to Fab light chain A and heavy chain B. Retain positive-occupancy heavy atoms and a zero-contact case. Use only NumPy/Pandas/SciPy/Matplotlib/py3Dmol and standard library; do not predict affinity.',
        'Manually rerun code. At each HER2 residue the combined minimum must equal the minimum of the A-only and B-only values. Unique contact counts must not decrease as the cutoff rises; preserve insertion codes in CSV and empty-interface reporting.'
    ],[
        '比较独立 HER2 残基数与残基对边数。为什么这两个计数不同？',
        '把阈值设为 0.01 Å。表格、图形与导出应怎样呈现？',
        '一个残基可能有多个伙伴，边数和独立残基数的分母不同。0.01 Å 的有效结果是空界面、零计数、明确的空状态图，以及仅含表头的边表，不能虚构接触。',
        '只用已列包，在三维视图中分别标出 3.5/4/5 Å 下 HER2 界面残基。保留作者插入码，与导出的靶蛋白表核对，不将结果标为已验证表位。',
        '分别增加 HER2 到 Fab 轻链 A、重链 B 的最短距离曲线。保留正占有率重原子选择与零接触场景，只用 NumPy/Pandas/SciPy/Matplotlib/py3Dmol 和标准库，不预测亲和力。',
        '手动重新运行。每个 HER2 残基的整体最短距离须等于 A 单链与 B 单链结果的较小值；增加阈值后接触数量不能下降，CSV 保留插入码和空界面报告。'
    ])
}
