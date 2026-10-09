"""Bilingual teaching narrative and shared executable cells. Source of truth for both media."""

COURSES = [
 dict(id="01-fasta-to-protein",slug="fasta-to-protein",category="sequences",minutes=45,difficulty=1,
      title={"en":"From FASTA to a gene and its protein","zh-hans":"从 FASTA 到基因与蛋白质"},
      summary={"en":"Trace real HBB and HBD transcripts through their annotated coding regions, then verify translation against RefSeq.","zh-hans":"沿着真实 HBB 与 HBD 转录本提取编码区，将翻译结果与 RefSeq 注释逐字核对。"},
      snapshots=["sequences"],functions=["parse_fasta","translate_cds","gc_fraction"],packages=["numpy","pandas","matplotlib","IPython"]),
 dict(id="02-affine-sequence-alignment",slug="sequence-alignment",category="sequences",minutes=60,difficulty=2,
      title={"en":"Align the beta- and delta-globin genes","zh-hans":"比对 β 与 δ 珠蛋白基因"},
      summary={"en":"Build affine-gap global and local alignment, follow the traceback, and explain exactly what identity and coverage measure.","zh-hans":"实现仿射缺口全局与局部比对，跟随回溯路径，准确理解一致性、覆盖率及评分。"},
      snapshots=["sequences"],functions=["affine_align","alignment_summary"],packages=["numpy","pandas","matplotlib","IPython"]),
 dict(id="03-airway-expression",slug="rnaseq-expression",category="expression",minutes=60,difficulty=2,
      title={"en":"Explore a paired RNA-seq experiment","zh-hans":"探索真实的配对 RNA-seq 实验"},
      summary={"en":"Inspect 63,677 genes across eight airway samples; normalize depth, distinguish donor from treatment, and inspect paired responses.","zh-hans":"检查 63,677 个基因与 8 个 airway 样本，归一化测序深度，区分供体与处理效应并查看配对变化。"},
      snapshots=["airway"],functions=["validate_counts","normalize_counts","paired_response"],packages=["numpy","pandas","matplotlib","IPython"]),
 dict(id="04-reactome-enrichment",slug="pathway-enrichment",category="expression",minutes=60,difficulty=3,
      title={"en":"Test pathway overrepresentation","zh-hans":"检验响应候选基因的通路富集"},
      summary={"en":"Define a measured gene universe, test real Reactome pathways with a hypergeometric model, and correct the entire test family.","zh-hans":"定义实际测量的背景集合，用超几何模型检验真实 Reactome 通路，并对完整检验族校正。"},
      snapshots=["airway","reactome"],functions=["validate_counts","normalize_counts","paired_response","bh_adjust","overrepresentation"],packages=["numpy","pandas","scipy","matplotlib","networkx","IPython"]),
 dict(id="05-string-physical-network",slug="protein-interactions",category="networks",minutes=50,difficulty=2,
      title={"en":"Read a protein interaction network","zh-hans":"解读蛋白质物理互作网络"},
      summary={"en":"Map 12 DNA-damage response proteins to STRING, retain isolates, compare confidence thresholds, and inspect evidence channels.","zh-hans":"将 12 个 DNA 损伤响应蛋白映射到 STRING，保留孤立节点，比较阈值并查看证据来源。"},
      snapshots=["network"],functions=["physical_graph"],packages=["numpy","pandas","matplotlib","networkx","IPython"]),
 dict(id="06-hemoglobin-structure",slug="protein-structure",category="structure",minutes=60,difficulty=2,
      title={"en":"Inspect hemoglobin in three dimensions","zh-hans":"在三维空间中分析血红蛋白"},
      summary={"en":"Rotate real 1A3N coordinates, inspect heme and its neighbors, and connect chain numbering to a RefSeq protein sequence.","zh-hans":"旋转真实 1A3N 坐标，观察血红素与邻近残基，将结构链编号与 RefSeq 蛋白序列联系起来。"},
      snapshots=["structure","sequences"],functions=["parse_pdb"],packages=["numpy","pandas","scipy","matplotlib","py3Dmol","IPython"]),
]

def section(en_title, zh_title, en, zh, code=None, tag=None):
    return dict(title={"en":en_title,"zh-hans":zh_title},text={"en":en,"zh-hans":zh},code=code,tag=tag)

AIRWAY_LOAD = '''airway = snapshot("airway")
counts = pd.DataFrame(airway["counts"], index=airway["genes"], columns=airway["samples"])
metadata = pd.DataFrame(airway["metadata"]).set_index("sample").loc[counts.columns]
validate_counts(counts, metadata)
print("Complete count matrix:", counts.shape)
def display_scroll_table(frame):
    # Keep identifiers and numeric values intact on narrow device screens.
    table = frame.to_html(border=0, classes="vibeit-scroll-table")
    style = """<style>
    table.vibeit-scroll-table {table-layout:auto !important;width:max-content !important;max-width:none !important;}
    table.vibeit-scroll-table th, table.vibeit-scroll-table td {
      white-space:nowrap !important;word-break:normal !important;padding:6px 8px;}
    </style>"""
    display(HTML(style+'<div style="max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch">'+table+'</div>'))
display_scroll_table(metadata)
display_scroll_table(counts.iloc[:6])'''

NORMALIZE = '''MIN_COUNT, MIN_SAMPLES = 10, 4
filtered, size_factors, normalized = normalize_counts(counts, MIN_COUNT, MIN_SAMPLES)
log_counts = np.log2(normalized + 1)
print("Retained genes:", len(filtered), "of", len(counts))
print("Genes positive in every sample:", int((filtered > 0).all(axis=1).sum()))
display(size_factors.to_frame())'''

SECTIONS = {}
SECTIONS["01-fasta-to-protein"] = [
 section("Read the record before reading the bases","先读记录，再读碱基",
 "HBB and HBD are human paralogs, not two patients. RefSeq NM_000518.5 and NM_000519.4 describe mRNA. Their sequences include untranslated regions (UTRs). The annotated CDS is 51..494 in both records. GenBank uses **1-based inclusive** coordinates; Python slicing is **0-based, end-exclusive**. Therefore the correct slice is `[start-1:end]`. Keep the accession version: a sequence without its version is harder to reproduce.",
 "HBB 与 HBD 是人类旁系同源基因，不是两个患者的样本。RefSeq NM_000518.5 和 NM_000519.4 描述的是 mRNA，序列包含非翻译区（UTR）。两份记录的 CDS 均为 51..494。GenBank 采用**从 1 开始、包含终点**的坐标；Python 切片**从 0 开始、不包含终点**，因此应使用 `[start-1:end]`。保留 accession 的版本号，才能明确复现的是哪一条序列。",
 '''records = snapshot("sequences")["records"]
fasta = "\\n".join(">"+r["accession"]+" "+r["gene"]+"\\n"+r["sequence"] for r in records)
parsed = parse_fasta(fasta)
display(pd.DataFrame([dict(gene=r["gene"], accession=r["accession"],
    mrna_bases=len(r["sequence"]), cds=f'{r["cds_start"]}..{r["cds_end"]}',
    protein=r["protein_id"]) for r in records]))
print(fasta[:180] + "…")'''),
 section("Draw the transcript map","绘制转录本结构",
 "A transcript diagram checks our coordinates before translation. Each rectangle spans annotated bases; the green region is the CDS and the gray regions are UTRs. The x-axis is the mRNA coordinate, not the chromosome coordinate. This drawing comes from the downloaded record, not a hand-drawn gene model.",
 "转录本示意图让我们在翻译前检查坐标。绿色矩形表示 CDS，灰色区域表示 UTR；横轴是 mRNA 坐标，不是染色体坐标。图形直接来自下载记录中的注释，不能据此推断基因的内含子结构。",
 '''fig, ax = plt.subplots(figsize=(8,3))
for i, r in enumerate(records):
    start, end, length = r["cds_start"], r["cds_end"], len(r["sequence"])
    ax.broken_barh([(1,start-1),(end+1,length-end)],(i-.22,.44),facecolors="#d9dedb")
    ax.broken_barh([(start,end-start+1)],(i-.22,.44),facecolors="#18785f")
    ax.text(start,i+.3,f"CDS {start}–{end}",fontsize=10)
ax.set(yticks=range(len(records)),yticklabels=[r["gene"] for r in records],
       xlabel="mRNA position (1-based)",title="Annotated coding regions and untranslated regions")
ax.spines[["top","right","left"]].set_visible(False)
plt.tight_layout(); plt.show()''',"cover"),
 section("Inspect composition and ambiguous bases","检查碱基组成与模糊碱基",
 "GC content is a descriptive sequence statistic. Count only A/C/G/T in its denominator and report ambiguous bases separately. A GC difference between these two transcripts does not establish expression, stability or evolutionary selection. Change the window later to see how smoothing changes the display.",
 "GC 含量是描述序列组成的统计量。分母只计入 A/C/G/T，模糊碱基另行报告。两条转录本的 GC 差异不能直接证明表达量、稳定性或进化选择。后面的窗口参数可以修改，用来观察平滑程度如何改变图形。",
 '''from collections import Counter
composition = pd.DataFrame({r["gene"]:Counter(r["sequence"]) for r in records}).reindex(list("ACGT")).fillna(0)
composition.plot.bar(figsize=(7,3),color=["#18785f","#416aa6"],rot=0)
plt.ylabel("Base count"); plt.title("Composition of the complete mRNA sequences")
plt.tight_layout(); plt.show()
display(pd.DataFrame([dict(gene=r["gene"],gc_fraction=gc_fraction(r["sequence"]),
    ambiguous_bases=sum(b not in "ACGT" for b in r["sequence"])) for r in records]))'''),
 section("Compare local GC content","比较局部 GC 含量",
 "Each point uses an 80-base window and a 20-base step. The position is the window midpoint; terminal partial windows are omitted. A short transcript supports only a few windows, so avoid treating this curve as a genome-wide pattern.",
 "每个点使用 80 个碱基的窗口，步长为 20 个碱基，位置表示窗口中点；末端不足一个窗口的片段被省略。短转录本只支持少量窗口，不应将曲线视作全基因组规律。",
 '''WINDOW, STEP = 80, 20
fig, ax = plt.subplots(figsize=(8,3))
for r in records:
    starts = range(0,len(r["sequence"])-WINDOW+1,STEP)
    ax.plot([s+(WINDOW+1)/2 for s in starts],
            [100*gc_fraction(r["sequence"][s:s+WINDOW]) for s in starts],marker="o",label=r["gene"])
ax.set(xlabel="Window midpoint (mRNA coordinate)",ylabel="GC (%)",title=f"Local GC: {WINDOW}-base windows")
ax.legend(); plt.tight_layout(); plt.show()'''),
 section("Translate the annotated coding sequence","翻译注释中的编码序列",
 "Use the standard genetic code, not a search for the first ATG in the whole transcript. A complete CDS includes its terminal stop codon; the RefSeq protein does not. Here 444 coding bases correspond to 147 amino acids plus the terminal stop. The first methionine is present in the translated precursor. Mature hemoglobin chain numbering may remove that methionine.",
 "使用标准遗传密码表，不能简单地从整条转录本的第一个 ATG 开始翻译。完整 CDS 包含末端终止密码子，RefSeq 蛋白序列不包含该终止符。本例 444 个编码碱基对应 147 个氨基酸及一个终止密码子。翻译产物包含起始甲硫氨酸，而成熟血红蛋白链的编号可能不包含它。",
 '''proteins, cds_records = {}, {}
for r in records:
    cds = r["sequence"][r["cds_start"]-1:r["cds_end"]]
    protein = translate_cds(cds)
    assert protein == r["translation"], "Translation differs from RefSeq"
    proteins[r["gene"]], cds_records[r["gene"]] = protein, cds
    print(r["gene"], "CDS:",len(cds), "bases; protein:",len(protein),"aa; RefSeq match: True")
    print(protein)'''),
 section("Check and export the result","校验并导出",
 "Assertions make coordinate or translation mistakes visible. Export both nucleotide and protein sequences so the analysis can move to another tool. The output directory is created next to the notebook. Re-running replaces this lesson's generated files, not your input notebook.",
 "断言可以使坐标或翻译错误立即显现。分别导出核酸和蛋白序列，方便在其他工具中继续分析。输出目录创建在 notebook 所在文件夹，重复运行只会更新本课生成的结果文件。",
 '''assert len(parsed) == 2
assert all(len(cds) == 444 for cds in cds_records.values())
assert all(len(p) == 147 for p in proteins.values())
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
(OUTPUT_DIR/"transcripts.fasta").write_text(fasta+"\\n")
(OUTPUT_DIR/"proteins.fasta").write_text("".join(f">{g}\\n{p}\\n" for g,p in proteins.items()))
pd.DataFrame([dict(gene=g,cds_bases=len(cds_records[g]),protein_aa=len(p),gc=gc_fraction(cds_records[g]))
              for g,p in proteins.items()]).to_csv(OUTPUT_DIR/"sequence-summary.csv",index=False)
print("Checks passed. Exported:",[p.name for p in OUTPUT_DIR.iterdir()])'''),
]

SECTIONS["02-affine-sequence-alignment"] = [
 section("Choose the sequence and scoring system","选择序列与评分",
 "Align annotated coding sequences rather than mixing UTRs with CDS. Global alignment accounts for every base; local alignment selects a high-scoring segment. Match +2, mismatch −1, gap-open −3 and gap-extension −1 are transparent teaching parameters, not an inferred evolutionary model. A gap of length k costs open + (k−1)×extension. Both end gaps are penalized in our global model.",
 "先比对注释中的编码区，避免将 UTR 与 CDS 混合解释。全局比对处理每一个碱基，局部比对寻找高分片段。match +2、mismatch −1、gap-open −3、gap-extension −1 是透明的教学参数，不能视作推断出的进化模型。长度 k 的缺口得分为 open + (k−1)×extension；本课全局模型也惩罚两端缺口。",
 '''records = {r["gene"]:r for r in snapshot("sequences")["records"]}
sequences = {g:r["sequence"][r["cds_start"]-1:r["cds_end"]] for g,r in records.items()}
a,b = sequences["HBB"],sequences["HBD"]
SCORING = dict(match=2,mismatch=-1,gap_open=-3,gap_extend=-1)
print("HBB / HBD CDS lengths:",len(a),len(b)); print("Scoring:",SCORING)'''),
 section("Run the three-state dynamic program","运行三状态动态规划",
 "The function above keeps three states: M ends in a paired column, X ends in a gap in sequence b, and Y ends in a gap in sequence a. Extending a gap stays in the same gap state; opening one moves from M. Traceback follows stored parent states. Local alignment can restart at zero. Its coordinates refer to the original CDS, not the cropped output. Inspect the function before asking an AI assistant to modify it.",
 "上方函数保留三个状态：M 以成对碱基结束，X 表示 b 序列中的缺口，Y 表示 a 序列中的缺口。延伸缺口保持在同一个缺口状态，打开缺口则从 M 转入。回溯沿着记录的父状态恢复比对。局部比对允许从零重新开始，其坐标仍指向原 CDS，不是截短后输出的坐标。使用 AI 修改前先查看函数。",
 '''global_result = affine_align(a,b,**SCORING)
local_result = affine_align(a,b,local=True,**SCORING)
summary = pd.DataFrame([alignment_summary(r,len(a),len(b)) for r in (global_result,local_result)],
                       index=["global","local"])
display(summary)
print("Local 0-based intervals:",local_result["start"],local_result["end"])'''),
 section("Read a colored alignment","阅读着色比对",
 "Green columns match; orange columns contain substitutions; gray indicates a gap. Print manageable 60-column blocks rather than one unreadable line. A visually similar alignment is not a gene annotation or a statistical homology test. Identity over all columns and identity over nongap paired columns answer different questions.",
 "绿色列表示一致，橙色列表示替换，灰色表示缺口。每块显示 60 列，避免输出一条难以阅读的长序列。比对看起来相似不等同于基因注释，也不是统计上的同源性检验。包含所有比对列的一致性与只包含成对非缺口列的一致性采用不同分母。",
 '''import html
blocks=[]
for start in range(0,len(global_result["a"]),60):
    x,y=global_result["a"][start:start+60],global_result["b"][start:start+60]
    colors=["#daf0e6" if p==q else "#eee" if "-" in (p,q) else "#ffe3cb" for p,q in zip(x,y)]
    rows=["".join(f'<span style="background:{c};padding:1px">{html.escape(base)}</span>'
                  for base,c in zip(seq,colors)) for seq in (x,y)]
    blocks.append(f'<p>Columns {start+1}–{start+len(x)}</p><div>HBB {rows[0]}</div><div>HBD {rows[1]}</div>')
display(HTML('<div style="font:12px/1.8 monospace;overflow-x:auto">'+"".join(blocks)+'</div>'))'''),
 section("Draw a sequence dot plot","绘制序列点阵图",
 "Each dot marks an exact matching 9-mer. Coordinates are 0-based CDS starts. Repeated motifs can create off-diagonal points. This is a separate visualization of sequence similarity; it does not reuse the dynamic-programming traceback.",
 "每个点表示一段完全一致的 9-mer，坐标为从 0 开始的 CDS 片段起点。重复片段可能产生非对角线上的点。这幅图是对序列相似性的独立可视化，没有复用动态规划的回溯结果。",
 '''KMER=9
locations={}
for j in range(len(b)-KMER+1): locations.setdefault(b[j:j+KMER],[]).append(j)
dots=[(i,j) for i in range(len(a)-KMER+1) for j in locations.get(a[i:i+KMER],[])]
fig,ax=plt.subplots(figsize=(5,5))
if dots:
    xy=np.array(dots); ax.scatter(xy[:,0],xy[:,1],s=8,color="#18785f",alpha=.6)
ax.set(xlabel="HBB CDS start (0-based)",ylabel="HBD CDS start (0-based)",title="Exact 9-mer matches")
plt.tight_layout();plt.show();print("Matching k-mer pairs:",len(dots))''',"cover"),
 section("Follow the traceback through the matrix","跟随矩阵中的回溯路径",
 "The heatmap is the maximum of M/X/Y at each cell. The blue path is a complete traceback from the global terminal state. It is not necessarily the only optimal path: ties follow a documented deterministic preference. Compare its shape with the dot plot, then change one scoring parameter at a time.",
 "热图展示每个位置的 M/X/Y 最大得分，蓝色路径是从全局终点恢复出的完整回溯路径。该路径不一定是唯一最优解；同分情况遵循函数中规定的确定性优先顺序。将它与点阵图比较，再一次只修改一个评分参数。",
 '''fig,ax=plt.subplots(figsize=(6,5))
matrix=global_result["matrix"].copy();matrix[~np.isfinite(matrix)]=np.nan
im=ax.imshow(matrix,origin="lower",aspect="auto",cmap="YlGn")
path=np.array(global_result["path"])
ax.plot(path[:,1],path[:,0],color="#3565af",lw=1.3)
ax.set(xlabel="HBD bases consumed",ylabel="HBB bases consumed",title="Global affine alignment and traceback")
fig.colorbar(im,ax=ax,label="Best state score");plt.tight_layout();plt.show()'''),
    section("Compare scoring sensitivity","比较评分敏感性",
 "Change the mismatch cost while keeping the input sequences and gap penalties fixed. Compare scores, gaps and all-column identity. These results answer a parameter-sensitivity question, not a hypothesis test for homology. Different scoring systems cannot be compared as though their raw scores used one common scale.",
 "保持输入序列及缺口参数不变，只修改替换罚分，比较得分、缺口数及全列一致性。这是在研究参数敏感性，不是在进行同源性假设检验。不同评分体系的原始得分不能当成同一尺度上的证据直接比较。",
 '''sensitivity=pd.DataFrame([dict(mismatch=penalty,**alignment_summary(affine_align(a,b,match=2,mismatch=penalty,gap_open=-3,gap_extend=-1),len(a),len(b))) for penalty in [-1,-2,-3]])
fig,axes=plt.subplots(1,2,figsize=(8,3))
axes[0].bar(sensitivity.mismatch.astype(str),sensitivity.identity_all_columns,color="#18785f")
axes[0].set(xlabel="Mismatch penalty",ylabel="Identity / all columns",ylim=(0,1),title="Identity under alternative costs")
axes[1].bar(sensitivity.mismatch.astype(str),sensitivity.gap_characters,color="#416aa6")
axes[1].set(xlabel="Mismatch penalty",ylabel="Gap characters",title="Gap sensitivity")
plt.tight_layout();plt.show();display(sensitivity[["mismatch","score","gap_characters"]])'''),
    section("Check coverage and export differences","检查覆盖率并导出差异",
 "Removing gaps must recover the original sequence for a global alignment. Differences are indexed by alignment column, not chromosome position. Gaps make those coordinates diverge. Keep the score parameters and accessions beside the output; an alignment without them cannot be reproduced reliably.",
 "对全局比对去除缺口后，应恢复原始序列。差异表采用比对列坐标，不是染色体坐标；存在缺口时，这些坐标不再一致。输出中同时保留评分参数及 accession，才能可靠地复现结果。",
 '''assert global_result["a"].replace("-","")==a
assert global_result["b"].replace("-","")==b
assert summary.loc["global","coverage_a"]==1 and summary.loc["global","coverage_b"]==1
differences=pd.DataFrame([dict(alignment_column=i+1,HBB=x,HBD=y)
    for i,(x,y) in enumerate(zip(global_result["a"],global_result["b"])) if x!=y])
display(differences.head(12))
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
summary.to_csv(OUTPUT_DIR/"alignment-summary.csv")
differences.to_csv(OUTPUT_DIR/"alignment-differences.csv",index=False)
(OUTPUT_DIR/"alignment.txt").write_text(str(SCORING)+"\\nHBB " +global_result["a"]+"\\nHBD "+global_result["b"]+"\\n")
print("Checks passed; differing columns:",len(differences))'''),
]

SECTIONS["03-airway-expression"] = [
 section("Audit the experimental design","核对实验设计",
 "Four primary human airway smooth-muscle cell lines were measured under control and dexamethasone conditions. The **biological unit is the donor**, and the eight columns are not eight independent donors. The snapshot retains all 63,677 rows of the official airway count object. Sample labels must be matched by identifier, not sorted independently or inferred from column order.",
 "实验包含 4 个原代人气道平滑肌细胞供体，每个供体分别测量对照与地塞米松处理条件。**生物学单位是供体**，8 列并不代表 8 个独立供体。快照保留官方 airway counts 对象的全部 63,677 行。必须用样本标识符匹配注释，不能分别排序或只根据列的位置推断处理组。",AIRWAY_LOAD),
 section("Inspect library sizes before normalization","归一化前检查文库大小",
 "Total mapped gene counts describe how many reads were assigned to this count matrix. They are not the total sequencing yield or a complete quality report. Large depth differences can dominate raw-count comparisons. Here every library has reads; a zero-total library is rejected rather than divided by zero.",
 "基因 counts 的列总和表示被计入该矩阵的 reads 数，不是总测序产出，也不是完整的测序质控报告。较大的深度差异会影响原始 counts 的比较。每个文库必须有 reads；零总数的文库应报错，而不是继续进行除零计算。",
 '''library_sizes=counts.sum(axis=0)
fig,ax=plt.subplots(figsize=(8,3))
ax.bar(range(len(counts.columns)),library_sizes/1e6,color=["#416aa6" if c=="control" else "#18785f" for c in metadata.condition])
ax.set(xticks=range(8),xticklabels=counts.columns, ylabel="Assigned gene counts (millions)",title="Sequencing depth differs between samples")
ax.tick_params(axis="x",rotation=45);plt.tight_layout();plt.show()
assert library_sizes.astype(int).tolist()==airway["library_totals"]
print("Original library totals verified")'''),
 section("Filter and estimate median-ratio size factors","过滤并估计 median-ratio size factors",
 "Keep genes with at least 10 counts in at least four samples. For genes positive in every sample, calculate the geometric mean across samples, divide each count by that reference, and take the per-sample median. Rescale factors to geometric mean one. The method assumes most genes do not undergo a large shared directional change. This depth adjustment is not TPM and does not correct gene length.",
 "保留至少 4 个样本 counts ≥10 的基因。对所有样本均为正的基因，先计算跨样本几何均值，再求 counts 与该参考值的比值，最后取每个样本的中位数。将 factors 调整至几何均值为 1。该方法假定多数基因不会产生大幅同方向变化；它不是 TPM，也不校正基因长度。",NORMALIZE),
 section("Measure similarity after a transparent log transform","透明地进行 log 变换并比较样本",
 "We use `log2(normalized counts + 1)` for teaching-scale exploration. It is **not DESeq2 VST or rlog**. Correlation uses the same retained genes for every sample pair. Closely related samples may share donor biology as well as treatment. Do not call a sample an outlier from this picture alone; check metadata and upstream quality evidence.",
 "本课使用 `log2(normalized counts + 1)` 进行探索，**不是 DESeq2 的 VST 或 rlog**。所有样本对都使用同一组保留基因计算相关性。样本相近可能来自相同供体，也可能与处理有关。不能只凭这幅图认定异常样本，需要结合样本注释及上游质量证据。",
 '''correlation=log_counts.corr()
fig,ax=plt.subplots(figsize=(6,5))
im=ax.imshow(correlation,vmin=.9,vmax=1,cmap="YlGnBu")
labels=[f"{r.donor} / {r.condition}" for r in metadata.itertuples()]
ax.set(xticks=range(8),yticks=range(8),xticklabels=labels,yticklabels=labels,title="Sample correlation after depth adjustment")
plt.setp(ax.get_xticklabels(),rotation=60,ha="right")
fig.colorbar(im,ax=ax,label="Pearson r");plt.tight_layout();plt.show()'''),
 section("Separate donor and treatment in PCA","在 PCA 中区分供体与处理",
 "Select at most 2,000 high-variance genes, transpose to samples × genes, and center each gene before SVD. No gene-wise unit-variance scaling is applied. Color indicates treatment; the connecting lines identify a donor pair. PCA signs may flip across numerical libraries without changing the geometry. PCA does not prove that treatment caused every visible axis.",
 "选择最多 2,000 个高变基因，转置为样本 × 基因矩阵，对每个基因中心化后进行 SVD；不进行基因方差标准化。颜色表示处理条件，连线表示同一供体的样本对。不同数值库可能翻转主成分的符号，但不会改变样本间几何关系。PCA 不能证明每个可见坐标轴都由处理造成。",
 '''variable_genes=log_counts.var(axis=1).nlargest(min(2000,len(log_counts))).index
matrix=log_counts.loc[variable_genes].T.to_numpy()
matrix=matrix-matrix.mean(axis=0)
u,s,vt=np.linalg.svd(matrix,full_matrices=False)
coordinates=u[:,:2]*s[:2];explained=s**2/np.sum(s**2)
fig,ax=plt.subplots(figsize=(7,5))
for donor,rows in metadata.groupby("donor"):
    indices=[metadata.index.get_loc(sample) for sample in rows.index]
    ax.plot(coordinates[indices,0],coordinates[indices,1],color="#bac6bf",lw=1)
for i,row in enumerate(metadata.itertuples()):
    ax.scatter(*coordinates[i],s=85,color="#416aa6" if row.condition=="control" else "#18785f")
    ax.annotate(row.donor+(" C" if row.condition=="control" else " T"),coordinates[i],xytext=(5,4),textcoords="offset points",fontsize=9)
ax.set(xlabel=f"PC1 ({explained[0]:.1%})",ylabel=f"PC2 ({explained[1]:.1%})",title="Donor pairs: blue control → green treated")
plt.tight_layout();plt.show()
print("PCA uses",len(variable_genes),"genes; explained variance:",explained[:2])''',"cover"),
 section("Inspect paired effects, without assigning DEG p-values","查看配对效应，不赋予 DEG p 值",
 "Subtract each donor's control log-counts from its treated log-counts. The mean of four differences measures a descriptive treatment-associated change. Because we added one before taking logs, this is not a fitted negative-binomial log fold change. Select response candidates using effect size and direction consistency; formal differential expression requires a suitable count model with donor in its design.",
 "将每个供体的处理组 log-counts 减去其对照组，再计算 4 个差值的平均值。这是描述性的处理相关变化。由于取 log 前加了 1，它不是负二项模型拟合出的 log fold change。本课按效应大小与方向一致性筛选响应候选；正式差异表达分析需要适当的 count 模型，并在设计中考虑供体。",
 '''paired_changes,response=paired_response(log_counts,metadata,min_effect=1,min_consistent=3)
display(response.direction.value_counts().rename("genes").to_frame())
top=response.mean_log2_change.abs().nlargest(16).index
heat=log_counts.loc[top];heat=heat.sub(heat.mean(axis=1),axis=0)
fig,ax=plt.subplots(figsize=(8,6))
im=ax.imshow(heat,aspect="auto",cmap="RdBu_r",vmin=-3,vmax=3)
ax.set(xticks=range(8),xticklabels=labels,yticks=range(len(top)),yticklabels=top,
       title="Largest observed paired changes: row-centered log counts")
plt.setp(ax.get_xticklabels(),rotation=60,ha="right");fig.colorbar(im,ax=ax,label="Centered log2 normalized counts")
plt.tight_layout();plt.show()'''),
 section("Follow one measured gene across all donors","在所有供体中追踪一个实测基因",
 "The original airway experiment investigated CRISPLD2 (ENSG00000103196). Check that the gene is in the measured, filtered matrix before plotting. The line endpoints represent normalized counts, not protein abundance. All four donors stay visible; showing only their average would hide heterogeneity.",
 "原始 airway 研究关注 CRISPLD2（ENSG00000103196）。绘图前检查该基因是否实际测量且通过过滤。连线端点表示归一化 counts，不是蛋白质丰度。保留全部 4 个供体，避免平均值掩盖个体差异。",
 '''GENE="ENSG00000103196"
assert GENE in normalized.index
fig,ax=plt.subplots(figsize=(5,4))
for donor,rows in metadata.groupby("donor"):
    ordered=rows.set_index("condition").loc[["control","treated"],:]
    values=[normalized.loc[GENE,rows.index[rows.condition==condition][0]] for condition in ["control","treated"]]
    ax.plot([0,1],values,marker="o",label=donor)
ax.set(xticks=[0,1],xticklabels=["Control","Treated"],ylabel="Normalized counts",title="CRISPLD2: paired donor measurements")
ax.legend(title="Donor",fontsize=8);plt.tight_layout();plt.show()'''),
 section("Check and export the audit trail","校验并导出分析轨迹",
 "Keep full results in files while showing small tables in the notebook. Counts remain integers before normalization; factors are positive; PCA explained fractions sum to one. The response table records its screening rule and includes every retained gene, including those that were not candidates.",
 "完整结果写入文件，notebook 中只显示小表格。归一化前 counts 为整数，factors 为正，PCA 的解释比例总和为 1。响应表保留每个通过过滤的基因，包括未被选为候选的基因，并明确注明筛选规则。",
 '''assert np.isclose(np.exp(np.log(size_factors).mean()),1)
assert np.isclose(explained.sum(),1)
assert np.isfinite(log_counts.to_numpy()).all()
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
metadata.to_csv(OUTPUT_DIR/"samples.csv")
size_factors.to_csv(OUTPUT_DIR/"size-factors.csv")
response.to_csv(OUTPUT_DIR/"response-candidates.csv")
paired_changes.to_csv(OUTPUT_DIR/"paired-log2-changes.csv")
pd.DataFrame(coordinates,index=metadata.index,columns=["PC1","PC2"]).to_csv(OUTPUT_DIR/"pca.csv")
print("Checks passed. No differential-expression p-values were estimated.")'''),
]

SECTIONS["04-reactome-enrichment"] = [
 section("Rebuild a self-contained candidate analysis","独立重建候选基因分析",
 "This notebook contains the complete airway matrix and runs without lesson 03 or its output files. The original experiment and donor pairing are unchanged. Start by auditing the eight sample identifiers. An input gene list without its selection rule and measured universe is not enough for a defensible enrichment analysis.",
 "本 notebook 包含完整 airway 矩阵，无需先运行第 03 课或读取其输出。实验来源与供体配对关系保持一致，先核对 8 个样本标识符。只有基因列表、没有筛选规则及实际测量背景，不能支持可靠的富集分析。",AIRWAY_LOAD),
 section("Normalize before selecting candidates","筛选候选前进行归一化",
 "Apply the same count filter and median-ratio method as lesson 03. Candidate selection must be based on the measurements, before looking at the pathways. Selecting genes because they belong to a pathway and then testing that same pathway creates circular evidence.",
 "采用第 03 课相同的过滤及 median-ratio 方法。候选应从测量结果中筛选，而不是看过通路结果之后再选择。先挑出某通路的基因，再检验该通路是否富集，会产生循环论证。",NORMALIZE),
 section("Make the screening rule explicit","明确写出筛选规则",
 "Up candidates have a mean paired log2 change ≥1 and at least three positive donor differences; down candidates have a mean ≤−1 and at least three negative differences. These are effect-based response candidates, not statistically tested DEGs. The scatter plot shows both retained and unselected genes so the threshold stays visible.",
 "上调候选要求平均配对 log2 变化 ≥1，且至少 3 个供体差值为正；下调候选要求平均值 ≤−1，且至少 3 个供体差值为负。这是按效应筛选的响应候选，不是经过统计检验的 DEG。散点图同时展示选中与未选中的基因，使阈值保持可见。",
 '''paired_changes,response=paired_response(log_counts,metadata,min_effect=1,min_consistent=3)
up=set(response.index[response.direction=="up"])
down=set(response.index[response.direction=="down"])
fig,ax=plt.subplots(figsize=(7,4))
for direction,color in [("other","#bdc5c0"),("up","#bc6541"),("down","#416aa6")]:
    selected=response.direction==direction
    ax.scatter(normalized.mean(axis=1)[selected],response.mean_log2_change[selected],s=8,alpha=.45,color=color,label=direction)
ax.set_xscale("log");ax.axhline(1,color="#888",ls="--",lw=.7);ax.axhline(-1,color="#888",ls="--",lw=.7)
ax.set(xlabel="Mean normalized count",ylabel="Mean paired log2 change",title="Effect screening before pathway testing")
ax.legend();plt.tight_layout();plt.show()
print("Up / down / retained:",len(up),len(down),len(filtered))'''),
 section("Define the gene universe from actual measurements","用实际测量定义背景集合",
 "The frozen Reactome mapping contains human Ensembl genes and lowest-level pathway memberships. Intersect measured, filtered genes with genes covered by these annotations. Report unmapped candidates. Do not use every human gene as the background for a filtered experiment. Our term-size rule is 10–500 members within this background, chosen before viewing results.",
 "冻结的 Reactome 映射包含人类 Ensembl 基因与底层通路归属。背景定义为通过表达过滤且被这些注释覆盖的基因，未映射候选需要报告。不能将所有人类基因作为已过滤实验的背景。通路大小规则为在该背景内有 10–500 个成员，该规则在查看结果前确定。",
 '''reactome=snapshot("reactome")
pathways=reactome["pathways"]
annotated=set().union(*(set(term["genes"]) for term in pathways))
background=set(filtered.index)&annotated
print("Reactome version:",reactome["version"])
audit=pd.DataFrame([dict(stage="Measured",genes=len(counts)),dict(stage="Expression filter",genes=len(filtered)),
 dict(stage="Annotated background",genes=len(background)),dict(stage="Up candidates mapped",genes=len(up&background)),
 dict(stage="Down candidates mapped",genes=len(down&background))])
display(audit)
print("Unmapped up / down candidates:",len(up-background),len(down-background))'''),
 section("Test every eligible term and correct the complete family","检验全部合格通路并校正完整检验族",
 "For N background genes, K term members, n candidates and k overlapping genes, the one-sided p-value is P(X≥k) = `hypergeom.sf(k−1,N,K,n)`. Include terms with zero overlap (p=1), then apply BH across **both directions together**. A q-value is not the probability that a pathway is active. Expression-based selection and related pathway memberships also constrain biological interpretation.",
 "若背景有 N 个基因、通路有 K 个成员、候选有 n 个基因、重叠有 k 个基因，则单侧 p 值为 P(X≥k)，使用 `hypergeom.sf(k−1,N,K,n)`。零重叠通路也纳入检验（p=1），再对**两个方向的全部检验共同**进行 BH 校正。q 值不是通路被激活的概率；表达筛选与通路之间的相关性也限制了结果解释。",
 '''background,enrichment=overrepresentation(up,down,filtered.index,pathways,min_size=10,max_size=500)
print("Complete test family:",len(enrichment))
print("Terms with q < 0.05:",int((enrichment.qvalue<.05).sum()) if len(enrichment) else 0)
display(enrichment.drop(columns="genes").head(12))'''),
 section("Read the enrichment bubble plot","阅读富集气泡图",
 "Show at most twelve nonzero-overlap terms, ordered by q then p. Bubble area encodes overlap count; x is overlap/query size; color is −log10(q). Labels remain descriptive even if no q-value meets 0.05. A ranked plot always has a top row, so ranking alone is not significance.",
 "最多展示 12 个非零重叠通路，按 q 值及 p 值排序。气泡面积表示重叠基因数，横轴为 overlap/query size，颜色为 −log10(q)。即使没有 q 值达到 0.05，也保留描述性标签。排序图总会有第一行，排名靠前本身不等同于显著。",
 '''plot_terms=enrichment.loc[enrichment.overlap>0].head(12).copy() if len(enrichment) else enrichment.copy()
fig,ax=plt.subplots(figsize=(9,5))
if len(plot_terms):
    colors=-np.log10(plot_terms.qvalue.clip(lower=1e-300))
    dots=ax.scatter(plot_terms.overlap/plot_terms.query_size,np.arange(len(plot_terms)),
        s=30+18*plot_terms.overlap,c=colors,cmap="YlGnBu")
    names=[r.direction+": "+r.name[:62] for r in plot_terms.itertuples()]
    ax.set(yticks=range(len(names)),yticklabels=names);ax.invert_yaxis()
    fig.colorbar(dots,ax=ax,label="−log10(BH q)")
else:
    ax.text(.5,.5,"No eligible terms with overlapping candidates",ha="center",va="center",transform=ax.transAxes)
ax.set(xlabel="Overlap / mapped candidate count",title="Reactome overrepresentation: effect-screened candidates")
plt.tight_layout();plt.show()''',"cover"),
 section("Inspect redundant pathways through shared genes","通过共享基因观察通路冗余",
 "Related pathways can share much of their evidence. Use the twelve displayed terms to compute candidate-overlap Jaccard similarity: intersection/union. This graph describes redundancy in the displayed results, not protein interactions. Edges require Jaccard ≥0.2; node color identifies the direction of the candidate set.",
 "相关通路可能共享大部分证据。对展示的 12 个通路计算候选重叠集合的 Jaccard 相似度，即交集/并集。这幅网络描述结果的冗余，不代表蛋白互作。Jaccard ≥0.2 才连边，节点颜色表示候选集合方向。",
 '''term_graph=nx.Graph()
sets={}
for r in plot_terms.itertuples():
    key=r.direction+":"+r.pathway;sets[key]=set(r.genes.split(";"))
    term_graph.add_node(key,label=r.name[:28],direction=r.direction)
keys=list(sets)
for i,x in enumerate(keys):
    for y in keys[i+1:]:
        similarity=len(sets[x]&sets[y])/len(sets[x]|sets[y]) if sets[x]|sets[y] else 0
        if similarity>=.2:term_graph.add_edge(x,y,jaccard=similarity)
fig,ax=plt.subplots(figsize=(8,5))
if term_graph:
    pos=nx.spring_layout(term_graph,seed=42)
    nx.draw_networkx(term_graph,pos,ax=ax,labels=nx.get_node_attributes(term_graph,"label"),
        node_color=["#bde3d1" if term_graph.nodes[k]["direction"]=="up" else "#c5d6ee" for k in term_graph],
        node_size=650,font_size=8,edge_color="#a4b4ac")
else:ax.text(.5,.5,"No terms to compare",ha="center",transform=ax.transAxes)
ax.set_title("Shared candidate genes between displayed pathways");ax.axis("off")
plt.tight_layout();plt.show()'''),
 section("Export all tests, including unremarkable results","导出全部检验，包括不显著结果",
 "The export contains all eligible terms in both directions, not only the plotted or significant rows. Include background identifiers and candidate-selection measurements. If the candidate set is empty, every tested p-value is one; an empty universe or missing annotation is an analysis limitation to report, not an invitation to change the background until a desired result appears.",
 "导出保留两个方向的所有合格通路，不仅保留展示或显著的行。同时导出背景标识符及候选筛选的测量值。候选为空时，检验 p 值均为 1；空背景或缺失注释是需要报告的分析限制，不能为了得到预期结果而反复修改背景。",
 '''if len(enrichment):
    assert enrichment.qvalue.between(0,1).all()
    assert (enrichment.qvalue+1e-15>=enrichment.pvalue).all()
    assert (enrichment.overlap<=enrichment.term_size).all()
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
enrichment.to_csv(OUTPUT_DIR/"reactome-all-tests.csv",index=False)
response.to_csv(OUTPUT_DIR/"response-screen.csv")
pd.Series(sorted(background),name="ensembl_gene").to_csv(OUTPUT_DIR/"background.csv",index=False)
audit.to_csv(OUTPUT_DIR/"universe-audit.csv",index=False)
print("Checks passed; full background and test family exported")'''),
]

SECTIONS["05-string-physical-network"] = [
 section("Read the query, mapping and network type","阅读查询、映射及网络类型",
 "The query contains twelve human DNA-damage response proteins. STRING identifiers refer to proteins; a gene symbol is resolved before graph construction. The API was queried with `network_type=physical`, species 9606 and no added neighbors. The frozen edge set starts at API score 400, enabling comparisons at 0.4 or above. STRING's physical network can include predicted evidence; it does not mean every edge was directly measured in one experiment.",
 "查询包含 12 个人类 DNA 损伤响应相关蛋白。STRING 标识符指向蛋白，构图前需要解析基因符号。本快照采用 `network_type=physical`、物种 9606，不额外添加邻居；冻结边集从 API score 400 开始，因此可比较 ≥0.4 的阈值。STRING 物理网络可以包含预测证据，并不意味着每条边都在某个实验中被直接测量。",
 '''network=snapshot("network")
mapping=pd.DataFrame(network["mapping"])
display(mapping[[c for c in ["queryItem","queryIndex","stringId","preferredName","ncbiTaxonId"] if c in mapping]])
print("Query:",network["query"])
print("Snapshot API threshold:",network["request"]["required_score"],"; added nodes:",network["request"]["add_nodes"])
print("Version:",network["version"])'''),
 section("Build a graph that retains all queried proteins","构图并保留所有查询蛋白",
 "Create nodes from the mapping first, then add qualifying edges. A protein with no edge at this threshold stays in the graph. Such an isolate may reflect limited evidence or the chosen query; it is not proof that the protein has no partners. Self-loops are excluded and repeated undirected edges retain their largest combined score.",
 "先根据映射创建节点，再添加通过阈值的边。没有边的查询蛋白仍保留在图中。孤立节点可能反映证据不足或查询范围限制，不能证明该蛋白没有互作伙伴。排除自环，对重复无向边保留最大的综合得分。",
 '''THRESHOLD=.7
graph=physical_graph(network,THRESHOLD)
print("Nodes / edges / isolates:",graph.number_of_nodes(),graph.number_of_edges(),list(nx.isolates(graph)))
positions=nx.spring_layout(graph,seed=42,weight="score")
fig,ax=plt.subplots(figsize=(8,6))
nx.draw_networkx_edges(graph,positions,ax=ax,alpha=.5,width=[1+2*graph[a][b]["score"] for a,b in graph.edges],edge_color="#829b8f")
nx.draw_networkx_nodes(graph,positions,ax=ax,node_size=[450+80*graph.degree(n) for n in graph],
    node_color=["#18785f" if n=="TP53" else "#c4ded3" for n in graph],edgecolors="white",linewidths=1.5)
nx.draw_networkx_labels(graph,positions,ax=ax,font_size=10)
ax.set_title("STRING physical network: human query, confidence ≥0.7");ax.axis("off")
plt.tight_layout();plt.show()''',"cover"),
 section("Inspect evidence channels","查看证据来源",
 "Combined score is a confidence measure, not binding affinity or interaction strength. `escore` describes experimental evidence, `dscore` curated database evidence, and `tscore` text-mining evidence. These channels are not independent probabilities to add together. Inspect them separately to see whether a high combined score rests on the evidence appropriate to your question.",
 "综合得分表示置信度，不是结合亲和力或互作强度。`escore` 表示实验证据，`dscore` 表示数据库证据，`tscore` 表示文本挖掘证据。不能将这些字段当成独立概率直接相加；分别查看它们，才能判断高综合得分是否具有与你的问题相符的证据。",
 '''edge_table=pd.DataFrame([dict(protein_a=a,protein_b=b,**attrs) for a,b,attrs in graph.edges(data=True)],
    columns=["protein_a","protein_b","score","escore","dscore","tscore"])
evidence=edge_table.sort_values("score",ascending=False).head(15)
fig,ax=plt.subplots(figsize=(7,5))
if len(evidence):
    im=ax.imshow(evidence[["score","escore","dscore","tscore"]],vmin=0,vmax=1,cmap="YlGnBu",aspect="auto")
    ax.set(xticks=range(4),xticklabels=["Combined","Experiments","Database","Text mining"],
           yticks=range(len(evidence)),yticklabels=evidence.protein_a+" — "+evidence.protein_b)
    fig.colorbar(im,ax=ax,label="Channel score")
else:ax.text(.5,.5,"No edges at this threshold",ha="center",transform=ax.transAxes)
ax.set_title("Evidence channels for the highest-score edges");plt.tight_layout();plt.show()
display(edge_table.head(10))'''),
 section("Compare thresholds using one frozen edge set","用同一个冻结边集比较阈值",
 "Change only the threshold. All twelve nodes remain, so the isolate count is comparable. A denser network is not necessarily better evidence. Scores below 0.4 were not retrieved: lowering the local threshold further cannot recover edges absent from the snapshot. Refresh the data explicitly for that new question.",
 "比较时只修改阈值，始终保留 12 个节点，因此孤立节点数可以直接比较。网络更稠密并不一定意味着证据更好。快照未获取 <0.4 的边，在本地继续降低阈值无法恢复不存在于快照中的边；若要研究该范围，需要明确重新获取数据。",
 '''thresholds=[.4,.7,.9,.95,.99]
sensitivity=pd.DataFrame([dict(threshold=t,edges=g.number_of_edges(),isolates=len(list(nx.isolates(g))),
    components=nx.number_connected_components(g)) for t in thresholds for g in [physical_graph(network,t)]])
fig,ax=plt.subplots(figsize=(7,3))
ax.plot(sensitivity.threshold,sensitivity.edges,"o-",label="Edges")
ax.plot(sensitivity.threshold,sensitivity.isolates,"s-",label="Isolates")
ax.set(xlabel="Minimum combined confidence",ylabel="Count",title="Network sensitivity to the confidence threshold")
ax.legend();plt.tight_layout();plt.show();display(sensitivity)'''),
 section("Compute topology and describe its limits","计算拓扑并解释局限",
 "Degree counts neighbors within the selected query. Unweighted betweenness counts shortest-path mediation without pretending confidence is a physical distance. Communities use confidence as a graph weight, with a fixed seed. Neither centrality nor a community label proves essentiality, causality or a biological module; the query itself already focuses on a pathway.",
 "度数统计查询范围内的邻居。无权介数统计最短路径中介作用，避免把置信度伪装成物理距离。社区检测使用置信度权重及固定随机种子。中心性或社区标签不能证明必需性、因果作用或功能模块；查询本身已经偏向特定通路。",
 '''centrality=nx.betweenness_centrality(graph,weight=None)
communities=nx.community.louvain_communities(graph,weight="score",seed=42) if graph.number_of_edges() else [{n} for n in graph]
membership={n:i+1 for i,nodes in enumerate(communities) for n in nodes}
node_table=pd.DataFrame([dict(protein=n,degree=graph.degree(n),betweenness=centrality[n],community=membership[n],
    string_id=graph.nodes[n]["string_id"]) for n in graph]).sort_values(["degree","protein"],ascending=[False,True])
display(node_table)'''),
 section("Check and export a portable network","校验并导出可移植网络",
 "The GraphML file preserves node identifiers and selected confidence channels. The source snapshot inside the notebook preserves the full returned evidence fields, including those not displayed here. Export the threshold audit too, so a reader can reproduce the graph rather than merely view its picture.",
 "GraphML 保留节点标识符与本课展示的置信度字段。notebook 内部原始快照保留完整返回字段，包括未展示的证据。阈值审计表也应导出，让读者能够复现网络，而不只是查看一张图片。",
 '''assert graph.number_of_nodes()==12
assert nx.number_of_selfloops(graph)==0
assert all(attrs["score"]>=THRESHOLD for _,_,attrs in graph.edges(data=True))
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
edge_table.to_csv(OUTPUT_DIR/"physical-edges.csv",index=False)
node_table.to_csv(OUTPUT_DIR/"proteins.csv",index=False)
sensitivity.to_csv(OUTPUT_DIR/"threshold-audit.csv",index=False)
nx.write_graphml(graph,OUTPUT_DIR/"physical-network.graphml")
print("Checks passed; GraphML, nodes, edges and threshold audit exported")'''),
]

SECTIONS["06-hemoglobin-structure"] = [
 section("Read structure metadata before viewing the model","查看模型前先读结构信息",
 "1A3N is an experimental X-ray structure of human deoxyhemoglobin. The model contains alpha and beta protein chains and heme ligands. Resolution describes the experiment, not a uniform atom-position error bar. Inspect experimental method, resolution and accession before rotating a convincing-looking picture. No structure prediction runs in this lesson.",
 "1A3N 是人类脱氧血红蛋白的 X 射线实验结构，包含 α、β 蛋白链及血红素配体。分辨率描述实验，不能直接当成每个原子坐标的统一误差范围。旋转模型前先检查实验方法、分辨率及结构编号。本课不执行结构预测。",
 '''structure=snapshot("structure")
pdb_text=structure["pdb"];entry=structure["entry"]
print("PDB:",structure["pdb_id"])
print("Method:",[item["method"] for item in entry["exptl"]])
print("Resolution (Å):",entry["rcsb_entry_info"].get("resolution_combined"))
print("Title:",entry["struct"]["title"])
print("Coordinate file:",len(pdb_text),"characters")'''),
 section("Parse chains, insertion codes and alternate conformations","解析链、插入码及替代构象",
 "Our small parser reads fixed PDB columns for ATOM/HETATM records. It selects the first model and one alternative per atom by occupancy, with deterministic tie-breaking. Residue identity includes chain, residue number and insertion code. Keep occupancy-zero atoms in the audit, then exclude them from coordinate-based analyses. The parser is for this documented format; arbitrary mmCIF files require a different parser.",
 "本课小型解析器按 PDB 固定列读取 ATOM/HETATM。选择第一个模型，按 occupancy 为每个原子选取替代构象，同分时使用确定性规则。残基标识同时包含链、残基编号和插入码。审计保留 occupancy 为零的原子，坐标分析则排除它们。本解析器针对 PDB 格式，不适用于任意 mmCIF 文件。",
 '''atoms=parse_pdb(pdb_text)
usable=atoms.loc[atoms.occupancy>0].copy()
protein=usable.loc[usable.record=="ATOM"]
ca=protein.loc[protein.atom=="CA"].sort_values(["chain","resnum","icode"])
chain_summary=ca.groupby("chain").agg(observed_ca=("atom","size"),first_residue=("resnum","min"),last_residue=("resnum","max"))
display(chain_summary)
display(usable.loc[usable.record=="HETATM"].groupby("residue").size().rename("atoms").to_frame())
print("Parsed atoms:",len(atoms),"; zero occupancy:",int((atoms.occupancy==0).sum()))'''),
 section("Rotate the model and inspect heme","旋转模型并观察血红素",
 "The viewer uses the embedded coordinate text and the app's bundled 3Dmol library. Drag to rotate and pinch to zoom. Cartoon follows the protein backbone; sticks highlight heme. Water is hidden to reduce clutter. Change STYLE between `cartoon` and `stick` (the API key is singular) and rerun the cell. Labels and color choices aid inspection; they are not experimental evidence.",
 "预览使用内嵌坐标与应用随附的 3Dmol 库。拖动旋转，双指缩放。cartoon 展示蛋白骨架，sticks 突出血红素；隐藏水分子以减少遮挡。可以将 STYLE 在 `cartoon` 与 `stick`（API 使用单数）之间切换并重新运行。颜色和标签用于辅助观察，不构成实验证据。",
 '''import py3Dmol
STYLE="cartoon"
view=py3Dmol.view(width="100%",height=420)
view.addModel(pdb_text,"pdb")
view.setStyle({"hetflag":False},{STYLE:{"colorscheme":"chain"}})
view.setStyle({"resn":"HEM"},{"stick":{"colorscheme":"orangeCarbon","radius":.18}})
view.setStyle({"resn":"HOH"},{})
view.setBackgroundColor("#f8faf8");view.zoomTo()
display(HTML(view._make_html()))
print("Interactive 1A3N view: drag to rotate; pinch/scroll to zoom")'''),
 section("Project the observed backbone into coordinates","将观测骨架投影到坐标空间",
 "This static view uses one Cα atom per observed residue, colored by chain. It remains readable without WebGL and provides a coordinate-level companion to the interactive viewer. Lines connect sequential observed residues only when consecutive residue numbers have no gap; a missing residue must not be bridged as if it were observed.",
 "静态图使用每个观测残基的一个 Cα 原子，按链着色。它无需 WebGL，能与交互模型互相核对。只连接残基编号连续的观测点；缺失残基不能被连成已经观测到的骨架。",
 '''fig=plt.figure(figsize=(7,5));ax=fig.add_subplot(111,projection="3d")
for chain,rows in ca.groupby("chain"):
    coords=rows[["x","y","z"]].to_numpy();ax.scatter(*coords.T,s=8,label=chain)
    numbers=rows.resnum.to_numpy()
    for i in range(len(rows)-1):
        if numbers[i+1]-numbers[i]==1:ax.plot(*coords[i:i+2].T,color="#afbdb5",lw=.5,alpha=.5)
ax.set(xlabel="x (Å)",ylabel="y (Å)",zlabel="z (Å)",title="Observed Cα atoms in the deposited coordinates")
ax.legend(title="Chain");plt.tight_layout();plt.show()''',"cover"),
 section("Connect sequence numbering to the observed chain","连接序列编号与观测链",
 "RefSeq HBB translates to a 147-aa sequence including initiating methionine. The mature beta chain convention omits that methionine. Use the deposited SEQRES record for the expected chain sequence, then compare it with ATOM residues. Missing coordinates do not mean a residue is absent from the protein. This distinction matters when mapping a variant to a structure.",
 "RefSeq HBB 翻译得到含起始甲硫氨酸的 147 aa 序列，成熟 β 链惯用编号通常省略它。先读取沉积文件的 SEQRES 预期链序列，再与 ATOM 中的残基比较。缺少坐标并不表示蛋白中不存在该残基；将变异映射到结构时必须区分这两种情况。",
 '''seqres={}
for line in pdb_text.splitlines():
    if line.startswith("SEQRES"):
        seqres.setdefault(line[11],[]).extend(line[19:70].split())
hbb=next(r for r in snapshot("sequences")["records"] if r["gene"]=="HBB")
print("RefSeq HBB amino acids:",len(hbb["translation"]),"; without starting methionine:",len(hbb["translation"][1:]))
for chain,rows in ca.groupby("chain"):
    expected=len(seqres.get(chain,[]));observed=len(rows)
    print("Chain",chain,"SEQRES:",expected,"; usable Cα:",observed,"; difference:",expected-observed)
display(ca.loc[ca.chain=="B",["chain","resnum","icode","residue"]].head(10))'''),
 section("Measure distances and define a contact map","测量距离并定义接触图",
 "For chain B, Euclidean Cα distance is computed in ångströms. A contact is distance <8 Å, excluding self-pairs and residues within two sequence positions. The threshold and atom choice define a descriptive contact map. They are not a universal biochemical interaction definition. The diagonal of the distance matrix must be zero and the matrix symmetric.",
 "对 B 链计算以 Å 为单位的 Cα 欧氏距离。接触定义为距离 <8 Å，并排除自身及序列位置相隔不超过 2 的残基。阈值和原子选择共同定义这幅描述性接触图，不能当成通用生化互作标准。距离矩阵必须对称，对角线必须为零。",
 '''from scipy.spatial.distance import cdist
chain_b=ca.loc[ca.chain=="B"].copy()
xyz=chain_b[["x","y","z"]].to_numpy()
distances=cdist(xyz,xyz)
separation=np.abs(chain_b.resnum.to_numpy()[:,None]-chain_b.resnum.to_numpy()[None,:])
contacts=(distances<8)&(separation>2)
fig,axes=plt.subplots(1,2,figsize=(10,4))
im=axes[0].imshow(distances,cmap="viridis");fig.colorbar(im,ax=axes[0],label="Cα distance (Å)")
axes[1].imshow(contacts,cmap="Greys",vmin=0,vmax=1)
for ax,title in zip(axes,["Chain B pairwise distances","Contacts <8 Å, sequence separation >2"]):
    ax.set(xlabel="Observed residue index",ylabel="Observed residue index",title=title)
plt.tight_layout();plt.show()
assert np.allclose(distances,distances.T) and np.allclose(np.diag(distances),0)
print("Unique contact pairs:",int(np.triu(contacts,1).sum()))'''),
 section("Find residues near one heme ligand","寻找一个血红素附近的残基",
 "Select chain B's heme and calculate each protein residue's minimum non-hydrogen atom distance to that ligand. Retain residues within 4 Å, including residues from another chain if they satisfy that condition. Proximity identifies inspection targets; it does not calculate affinity or prove catalysis. The B-factor plot describes model displacement parameters and must not be read as AlphaFold pLDDT.",
 "选择 B 链血红素，计算每个蛋白残基的非氢原子到该配体的最小距离。保留 4 Å 内的残基，满足条件的其他链残基也保留。邻近关系可用于选择观察目标，但不能计算亲和力或证明催化作用。B-factor 图表示模型位移参数，不能当成 AlphaFold pLDDT。",
 '''heavy=usable.loc[~usable.element.isin(["H","D"])]
heme=heavy.loc[(heavy.residue=="HEM")&(heavy.chain=="B")]
assert not heme.empty
near=[]
for key,rows in heavy.loc[heavy.record=="ATOM"].groupby(["chain","resnum","icode","residue"]):
    minimum=float(cdist(rows[["x","y","z"]],heme[["x","y","z"]]).min())
    if minimum<=4:near.append(dict(chain=key[0],resnum=key[1],icode=key[2],residue=key[3],minimum_distance_A=minimum))
neighbors=pd.DataFrame(near).sort_values("minimum_distance_A")
display(neighbors)
fig,ax=plt.subplots(figsize=(8,3))
ax.plot(chain_b.resnum,chain_b.bfactor,color="#416aa6")
ax.set(xlabel="Deposited chain B residue number",ylabel="Cα B-factor (Å²)",title="Experimental model displacement parameters")
plt.tight_layout();plt.show()'''),
 section("Export coordinates, tables and measurements","导出坐标、表格与测量结果",
 "Keep the original coordinate file alongside the derived summary so another viewer can reproduce the scene. Label distance units and chain selection. The export contains observed atoms and residue identities; it does not fill missing residues or predict their coordinates.",
 "保留原始坐标文件及派生摘要，方便在其他预览器中复现。距离注明单位及链选择。导出的是观测原子及残基标识，不会补齐缺失残基或预测其坐标。",
 '''assert set(ca.chain)=={"A","B","C","D"}
assert len(heme)>0 and len(chain_b)>100
assert np.isfinite(distances).all()
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
(OUTPUT_DIR/"1A3N.pdb").write_text(pdb_text)
chain_summary.to_csv(OUTPUT_DIR/"chains.csv")
neighbors.to_csv(OUTPUT_DIR/"heme-neighbors.csv",index=False)
pd.DataFrame(distances,index=chain_b.resnum,columns=chain_b.resnum).to_csv(OUTPUT_DIR/"chain-B-distances-A.csv")
atoms.to_csv(OUTPUT_DIR/"selected-first-model-atoms.csv",index=False)
print("Checks passed; original PDB and derived measurements exported")'''),
]
