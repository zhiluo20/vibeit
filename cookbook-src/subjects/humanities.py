"""Five computational-text workflows and one real social-indicator exploration."""
from ._common import lesson,step,exercises,bilingual

TEXT_FUNCTIONS=['strip_ebook_wrapper','split_novel_chapters','tokenize_words']
TEXT_IMPORTS='import re\nfrom collections import Counter\n'
COURSES=[
 lesson('hu01-corpus-audit',1,'historical-corpus-audit','Audit a historical text corpus','审计历史文本语料','Preserve source ebooks and licenses, inspect chapter boundaries and make tokenization decisions visible.','保留来源电子书和许可，检查章节边界并公开分词决策。',['novels'],TEXT_FUNCTIONS,'text','Text methods','文本方法',discipline='humanities',data_kind='text',difficulty=1,icon='📚',setup_imports=TEXT_IMPORTS),
 lesson('hu02-lexical-diversity',2,'length-controlled-diversity','Compare length-controlled lexical diversity','比较控制长度后的词汇多样性','Separate whole-corpus token/type counts from matched-window vocabulary ratios and inspect length effects.','区分整部语料词/词型数量与相同窗口词汇比例，并检查长度影响。',['novels'],TEXT_FUNCTIONS,'text','Text methods','文本方法',discipline='humanities',data_kind='text',icon='🔤',setup_imports=TEXT_IMPORTS),
 lesson('hu03-keyword-context',3,'keyword-in-context','Read keyword frequencies in context','在语境中解读关键词频率','Retrieve every exact-token match with context, inspect chapter-normalized counts and return to the source passages.','为每个完整词匹配提取语境，检查章节归一化数量，并回到来源段落。',['novels'],TEXT_FUNCTIONS+['keyword_contexts'],'text','Text methods','文本方法',discipline='humanities',data_kind='text',icon='🔎',setup_imports=TEXT_IMPORTS),
 lesson('hu04-mention-network',4,'name-mention-network','Audit a name-mention cooccurrence graph','审计名称提及共现图','Declare surface-pattern aliases, count paragraph cooccurrences and inspect threshold-sensitive graph summaries.','声明表面名称模式，计数段落共现，并检查阈值敏感的图摘要。',['novels'],TEXT_FUNCTIONS+['mention_cooccurrence'],'networks','Networks & representations','网络与表示',discipline='humanities',data_kind='text',minutes=60,icon='🕸️',setup_imports=TEXT_IMPORTS,packages=['numpy','pandas','matplotlib','networkx','IPython']),
 lesson('hu05-text-projection',5,'tfidf-svd-chapters','Inspect TF-IDF and signed chapter projections','检查 TF-IDF 与有符号章节投影','Build a declared chapter vocabulary, compute normalized TF-IDF and interpret an uncentered SVD without treating axes as topic probabilities.','构造声明的章节词汇，计算归一化 TF-IDF，并解读未中心化 SVD，不将轴当作主题概率。',['novels'],TEXT_FUNCTIONS+['tfidf_svd'],'networks','Networks & representations','网络与表示',discipline='humanities',data_kind='text',minutes=60,difficulty=3,icon='🧭',setup_imports=TEXT_IMPORTS),
 lesson('hu06-social-indicators',6,'social-indicator-exploration','Explore dated social indicators with explicit scope','按明确范围探索社会指标','Join economy-level income, population and life-expectancy observations, audit missingness and distinguish association from individual or causal inference.','合并经济体收入、人口及预期寿命观测，审计缺失，并区分关联与个人/因果推断。',['worldbank'],['worldbank_panel'],'social','Social indicators','社会指标',discipline='humanities',minutes=60,icon='🌍',setup_imports='from scipy.stats import spearmanr\n',packages=['numpy','pandas','scipy','matplotlib','IPython']),
]
for c in COURSES:
 if 'novels' in c['snapshots']:
  c['online_url']='https://www.gutenberg.org/ebooks/1342'
  c['data_note']=bilingual('The snapshot retains complete unmodified source ebooks, including their original licenses. Chapter-based analysis uses 61 Pride and Prejudice chapters and 24 Frankenstein chapters; front matter and Frankenstein framing letters are outside this declared scope. English-letter tokenization is a method choice, not a language-neutral definition. Word frequencies, surface-pattern cooccurrence and SVD axes do not independently establish authorial intent, character relationships or sentiment.','快照保留完整未修改来源电子书及原许可。章节分析使用《傲慢与偏见》61 章及《弗兰肯斯坦》24 章；前言和后者书信框架不在本次声明范围。英文字母分词是方法选择，不是语言无关定义。词频、表面模式共现和 SVD 轴不能独立证明作者意图、人物关系或情感。')
 else:
  c['online_url']='https://api.worldbank.org/v2/indicator/SP.DYN.LE00.IN?format=json'
  c['data_note']=bilingual('Use a declared 2023 economy-level cross-section. Life expectancy at birth is a period indicator based on mortality conditions, not a personal life prediction. Current frozen income-group metadata is not reconstructed historical classification. Complete-case selection and macro-level association cannot establish individual or causal effects.','使用声明的 2023 经济体截面。出生时预期寿命是基于死亡条件的时期指标，不是个人寿命预测。冻结的当前收入组 metadata 不等于重建历史分类。完整案例选择和宏观关联不能确定个人或因果效应。')

CORPUS_LOAD='''novels=snapshot("novels");corpus={};chapter_rows=[]
for book in novels["books"]:
 chapters=split_novel_chapters(strip_ebook_wrapper(book["raw_text"]))
 tokens=tokenize_words(" ".join(chapter["text"] for chapter in chapters))
 corpus[book["id"]]={"title":book["title"],"author":book["author"],"chapters":chapters,"tokens":tokens}
 for chapter in chapters:chapter_rows.append({"book_id":book["id"],"book":book["title"],"chapter":chapter["order"],"source_label":chapter["label"],"characters":len(chapter["text"]),"tokens":len(tokenize_words(chapter["text"])),"text":chapter["text"]})
chapter_table=pd.DataFrame(chapter_rows)
assert len(corpus[1342]["chapters"])==61 and len(corpus[84]["chapters"])==24
print(novels["source_notice"])
print("Declared chapter counts:",{b:len(corpus[b]["chapters"]) for b in corpus})
display(chapter_table.drop(columns="text").head(8))'''
STOPWORDS=set('a an and are as at be been being but by can could did do does for from had has have he her hers him his i if in is it its me more most my no not of on one or our she so some than that the their them then there these they this those to too was we were what when where which who why will with would you your'.split())
SECTIONS={}
SECTIONS[COURSES[0]['id']]=[
 step('Preserve source and inspect boundaries','保留来源并检查边界','The complete original ebooks and licenses remain in metadata. Analysis removes only wrappers and declared chapter-layout elements in memory. Repeated chapter labels resolve to the last heading for these two snapshots, excluding Frankenstein’s table-of-contents duplicates. This is not a universal book parser.','原电子书及许可完整留在 metadata。分析仅在内存删除包装和声明排版元素；对两份快照，重复章节标签保留末次标题，排除《弗兰肯斯坦》目录重复。这不是通用书籍解析器。',CORPUS_LOAD),
 step('Read chapter sizes','解读章节规模','Bars count tokens under the explicit English-letter rule. The number is a computational measure of the processed chapter, not a count of sentences, ideas or narrative importance.','柱计数声明英文字母规则下的词，不是句子、思想或叙事重要性的数量。','''fig,ax=plt.subplots(figsize=(10,4))
for book_id,part in chapter_table.groupby("book_id"):ax.plot(part.chapter,part.tokens,"o-",ms=3,label=corpus[book_id]["title"])
ax.set(xlabel="Declared chapter order",ylabel="Processed word tokens",title="Chapter boundaries and unequal text lengths");ax.legend(fontsize=8);plt.tight_layout();plt.show()''',cover=True),
 step('Compare transparent count definitions','比较透明的数量定义','Count characters, tokens and distinct normalized types separately. These are not interchangeable denominators. Lowercasing merges case variants; apostrophe handling and illustration removal are visible implementation choices.','字符、词和归一化词型分别计数，不可互换分母。小写合并大小写变体，撇号处理和插图删除为可见方法选择。','''summary=pd.DataFrame([{ "book":entry["title"],"chapters":len(entry["chapters"]),"word_tokens":len(entry["tokens"]),"word_types":len(set(entry["tokens"]))} for entry in corpus.values()]).set_index("book")
display(summary)
fig,ax=plt.subplots(figsize=(9,4));summary[["word_tokens","word_types"]].plot.bar(ax=ax)
ax.set(ylabel="Processed count",title="Tokens versus distinct types");plt.xticks(rotation=15);plt.tight_layout();plt.show()'''),
 step('Inspect frequent words before interpretation','解释前检查高频词','These are source chapter counts under a simple tokenizer, including function words. Display the ten most common tokens in deterministic count/alphabetical order. High frequency alone is not a theme or sentiment label.','这些是简单分词的来源章节计数，包括功能词。按数量/字母确定顺序显示前十词，高频本身不是主题或情感标签。','''fig,axes=plt.subplots(1,2,figsize=(11,4))
for ax,entry in zip(axes,corpus.values()):
 counts=Counter(entry["tokens"]);top=sorted(counts.items(),key=lambda item:(-item[1],item[0]))[:10]
 ax.barh([w for w,n in top][::-1],[n for w,n in top][::-1]);ax.set(xlabel="Chapter-corpus token count",title=entry["title"])
plt.tight_layout();plt.show()'''),
 step('Reconcile declared scope and export','核对声明范围并导出','Verify chapter totals and all count definitions directly. Export boundary labels and processed counts rather than replacing the original ebook. The raw source remains independently recoverable from the embedded snapshot.','直接核对章节数及计数定义，导出边界标签和处理计数，不覆盖原电子书；内嵌快照可独立恢复原来源。','''assert len(chapter_table)==85 and chapter_table.tokens.gt(0).all()
for book_id,entry in corpus.items():assert chapter_table.loc[chapter_table.book_id.eq(book_id),"tokens"].sum()==len(entry["tokens"])
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);chapter_table.drop(columns="text").to_csv(OUTPUT_DIR/"chapter-boundary-audit.csv",index=False)
summary.to_csv(OUTPUT_DIR/"processed-corpus-summary.csv")
(OUTPUT_DIR/"tokenization.json").write_text(json.dumps({"rule":"lowercase English letters; internal apostrophes retained","illustration_markup":"removed in analysis only","corpus_scope":"substantive numbered chapters only","chapter_counts":{"1342":61,"84":24}},indent=2))
print("Boundary and count checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[1]['id']]=[
 step('Separate raw TTR from text length','区分原始 TTR 与文本长度','Type-token ratio is distinct normalized types divided by tokens. Whole-book TTR depends strongly on length, so do not rank authors by the two raw numbers. We use the same declared chapter scope.','TTR 为不同归一化词型数除以词数，整部 TTR 强烈受长度影响，不能按两个原始数值排名作者。使用同一声明章节范围。',CORPUS_LOAD+'''
summary=pd.DataFrame([{ "book":entry["title"],"tokens":len(entry["tokens"]),"types":len(set(entry["tokens"])),"whole_TTR":len(set(entry["tokens"]))/len(entry["tokens"])} for entry in corpus.values()])
display(summary)
fig,axes=plt.subplots(1,2,figsize=(10,4));axes[0].bar(summary.book,summary.tokens);axes[0].set(ylabel="Processed tokens",title="Unequal corpus lengths")
axes[1].bar(summary.book,summary.whole_TTR);axes[1].set(ylabel="Whole-corpus TTR",title="Length-dependent ratio")
for ax in axes:ax.tick_params(axis="x",rotation=15)
plt.tight_layout();plt.show()'''),
 step('Match contiguous sampling-window lengths','匹配连续采样窗口长度','For each length, draw 30 seeded contiguous windows from each processed book. Mean and SD describe window variation in this corpus, not independent author experiments. Identical window lengths make the comparison more interpretable.','每个长度从各处理语料固定种子抽取 30 个连续窗口，均值/标准差描述该语料窗口变化，不是独立作者实验。相同长度改善可比性。','''rng=np.random.default_rng(42);lengths=[100,500,1000,2000,5000];records=[]
for book_id,entry in corpus.items():
 tokens=entry["tokens"]
 for length in lengths:
  for repeat in range(30):
   start=int(rng.integers(0,len(tokens)-length+1));window=tokens[start:start+length]
   records.append({"book":entry["title"],"window_tokens":length,"start_token":start,"TTR":len(set(window))/length})
windows=pd.DataFrame(records)
fig,ax=plt.subplots(figsize=(8,5))
for book,part in windows.groupby("book"):
 grouped=part.groupby("window_tokens").TTR.agg(["mean","std"]);ax.errorbar(grouped.index,grouped["mean"],yerr=grouped["std"],fmt="o-",label=book)
ax.set(xscale="log",xlabel="Contiguous window tokens",ylabel="TTR; bars = window SD",title="Length-controlled corpus comparison");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Read normalized frequency-rank curves','解读归一化词频—秩曲线','Rank words by count and divide by each corpus token total. Log axes expose the descriptive heavy-tailed shape. A curve here does not prove a universal language law or literary quality.','按数量排名并除以各语料总词数，对数坐标展示描述性的长尾形状，不证明普遍语言定律或文学质量。','''fig,ax=plt.subplots(figsize=(8,5))
for entry in corpus.values():
 frequency=np.array(sorted(Counter(entry["tokens"]).values(),reverse=True));ax.loglog(np.arange(1,len(frequency)+1),frequency/len(entry["tokens"]),label=entry["title"])
ax.set(xlabel="Within-corpus frequency rank",ylabel="Relative token frequency",title="Descriptive normalized rank-frequency curves");ax.legend();plt.tight_layout();plt.show()'''),
 step('Reconcile windows and export all draws','核对窗口并导出全部抽取','Each TTR must lie in (0,1], window starts stay within corpus bounds and every book gets equal replication at each length. Save all starts, not only windows supporting a preferred interpretation.','TTR 位于 (0,1]，起点在语料范围，各长度两书重复数量相同。保存所有起点，不能只保留支持偏好解释的窗口。','''assert windows.TTR.between(0,1,inclusive="right").all()
assert windows.groupby(["book","window_tokens"]).size().eq(30).all()
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);windows.to_csv(OUTPUT_DIR/"all-matched-windows.csv",index=False)
summary.to_csv(OUTPUT_DIR/"length-dependent-corpus-counts.csv",index=False)
print("Matched-window checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[2]['id']]=[
 step('Declare exact-token queries and context width','声明完整词查询和上下文宽度','Query pride in Pride and Prejudice and creature in Frankenstein. These are predeclared examples, not automatic thematic labels. Contexts use seven normalized tokens on each side and retain source chapter/order identifiers.','对两书预先声明查询 pride 和 creature，不是自动主题标签。两侧各七个归一化词，保留来源章节及位置标识。',CORPUS_LOAD+'''
queries={1342:"pride",84:"creature"};hits=[];counts=[]
for book_id,entry in corpus.items():
 for chapter in entry["chapters"]:
  tokens=tokenize_words(chapter["text"]);contexts=keyword_contexts(tokens,queries[book_id],7)
  for row in contexts:hits.append({"book_id":book_id,"book":entry["title"],"chapter":chapter["order"],**row})
  counts.append({"book_id":book_id,"book":entry["title"],"chapter":chapter["order"],"query":queries[book_id],"hits":len(contexts),"tokens":len(tokens),"per_1000_tokens":1000*len(contexts)/len(tokens)})
kwic=pd.DataFrame(hits);chapter_counts=pd.DataFrame(counts)
display(kwic[["book","chapter","before","keyword","after"]].head(10))'''),
 step('Normalize chapter frequencies','归一化章节频率','The vertical axis is query occurrences per 1000 chapter tokens, not raw count or sentiment intensity. Zero means no exact query match under this tokenizer, not no relevant theme in the passage.','纵轴为每千章节词的查询次数，不是原数量或情感强度。零仅表示此分词下无完整查询匹配，不代表段落没有相关主题。','''fig,ax=plt.subplots(figsize=(10,4))
for book_id,part in chapter_counts.groupby("book_id"):ax.plot(part.chapter,part.per_1000_tokens,"o-",ms=3,label=part.book.iloc[0]+": "+queries[book_id])
ax.set(xlabel="Declared chapter order",ylabel="Query hits per 1000 tokens",title="Length-normalized exact-token occurrences");ax.legend(fontsize=8);plt.tight_layout();plt.show()''',cover=True),
 step('Inspect corpus-position dispersion','检查语料位置分散','Locations are relative to the processed numbered-chapter token sequence. The display ignores excluded front matter and framing letters. Dispersion shows where the query occurs; it does not determine how the narrator uses the word.','位置相对处理后的编号章节词序列，不包括已排除前言/框架书信。分散图说明查询出现位置，不确定叙述者如何使用该词。','''fig,axes=plt.subplots(2,1,figsize=(10,4))
for ax,(book_id,entry) in zip(axes,corpus.items()):
 indices=[i for i,w in enumerate(entry["tokens"]) if w==queries[book_id]]
 ax.scatter(np.asarray(indices)/len(entry["tokens"]),np.zeros(len(indices)),marker="|",s=100)
 ax.set(xlim=(0,1),yticks=[],xlabel="Relative processed-corpus position",title=entry["title"]+": "+queries[book_id])
plt.tight_layout();plt.show()'''),
 step('Read context neighbors rather than automatic sentiment','阅读语境邻词而非自动情感','Count words in retrieved context windows after a declared short stop list. Overlapping windows may count a neighbor more than once. The bars motivate close reading, not a sentiment classifier or an author-intent conclusion.','按声明短停词表统计提取窗口邻词。窗口重叠可能重复计邻词。柱图用于促成细读，不是情感分类器或作者意图结论。','''stop=set("the a an and to of in i he she it was is that with for".split())
fig,axes=plt.subplots(1,2,figsize=(11,4))
for ax,book_id in zip(axes,corpus):
 subset=kwic[kwic.book_id.eq(book_id)];neighbor=Counter()
 for row in subset.itertuples():neighbor.update(w for w in (row.before+" "+row.after).split() if w not in stop and w!=queries[book_id])
 top=neighbor.most_common(10);ax.barh([w for w,n in top][::-1],[n for w,n in top][::-1]);ax.set(xlabel="Counts in retrieved windows",title=corpus[book_id]["title"])
plt.tight_layout();plt.show()'''),
 step('Reconcile exact matches and export all contexts','核对完整匹配并导出所有语境','Compare per-chapter totals with direct query counts. Export all matches in source order so students can examine counterexamples and return to the full original ebook, not only a selected excerpt.','将章节总数与直接查询计数对照，按来源顺序导出全部匹配，方便检视反例并回到完整原书，而非只看挑选片段。','''assert chapter_counts.hits.sum()==len(kwic)
for book_id,entry in corpus.items():assert kwic.book_id.eq(book_id).sum()==entry["tokens"].count(queries[book_id])
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);kwic.to_csv(OUTPUT_DIR/"all-keyword-contexts.csv",index=False)
chapter_counts.to_csv(OUTPUT_DIR/"normalized-chapter-query-counts.csv",index=False)
print("Exact match totals reconciled; all contexts exported:",len(kwic))''')]

SECTIONS[COURSES[3]['id']]=[
 step('Declare alias patterns and paragraph unit','声明别名模式及段落单位','Use surface patterns in Pride and Prejudice. Darcy is labelled as a surname rule and may refer to discussion or family mentions; rules do not establish unique character identity. Cooccurrence means both patterns occur in the same processed paragraph.','在《傲慢与偏见》中使用表面模式。Darcy 标为姓氏规则，可能出现讨论或家族提及，不确定唯一人物身份。共现指同一处理段落中两模式均出现。',CORPUS_LOAD+r'''
patterns={"Elizabeth / Lizzy":r"\b(?:elizabeth|lizzy|eliza)\b","Jane":r"\bjane\b","Darcy surname":r"\bdarcy\b","Bingley surname":r"\bbingley\b","Mr Bennet":r"\bmr\.?\s+bennet\b","Mrs Bennet":r"\bmrs\.?\s+bennet\b","Lydia":r"\blydia\b","Wickham":r"\bwickham\b"}
paragraphs=[part for chapter in corpus[1342]["chapters"] for part in re.split(r"\n\s*\n",chapter["text"]) if part.strip()]
MINIMUM=3;network=mention_cooccurrence(paragraphs,patterns,MINIMUM);graph=network["graph"]
print("Processed paragraphs:",len(paragraphs),"; declared entities:",len(patterns),"; minimum shared paragraphs:",MINIMUM)
display(pd.DataFrame({"pattern":list(patterns),"regex":list(patterns.values()),"paragraph_presence":network["paragraph_presence"]}))'''),
 step('Read a thresholded cooccurrence graph','解读阈值共现图','Edges count shared paragraphs under the declared rules. Layout is seeded; edge width encodes count. This graph is not a verified social relationship network or proof that two characters met. All declared nodes survive even with no edges.','边计声明规则下的共享段落，布局固定种子，边宽编码数量。此图不是已核实社会关系网，也不证明人物相遇。即便无边，保留全部声明节点。','''position=nx.spring_layout(graph,seed=42,weight="paragraph_count")
fig,ax=plt.subplots(figsize=(9,6));width=[1+np.log1p(graph[a][b]["paragraph_count"]) for a,b in graph.edges()]
nx.draw_networkx(graph,pos=position,ax=ax,node_size=1500,font_size=8,width=width,node_color="#b4d4ed")
ax.set_title("Surface-pattern cooccurrence; threshold = 3 shared paragraphs");ax.axis("off");plt.tight_layout();plt.show()''',cover=True),
 step('Inspect the underlying count matrix','检查底层计数矩阵','Matrix entries are shared-paragraph counts with an intentionally zero diagonal. The figure separates counted evidence from a drawn graph. A high count can reflect frequent mentions, not interpersonal importance.','矩阵为共享段落数量，对角线明确设零。图把计数依据与绘制网络分开；高数量可能来自高提及率，不是人际重要性。','''fig,ax=plt.subplots(figsize=(8,6));im=ax.imshow(network["matrix"],cmap="Blues")
ax.set_xticks(range(8),network["labels"],rotation=55,ha="right",fontsize=8);ax.set_yticks(range(8),network["labels"],fontsize=8)
fig.colorbar(im,ax=ax,label="Shared processed paragraphs");ax.set_title("Declared alias-rule counts");plt.tight_layout();plt.show()'''),
 step('Compare thresholds without dropping declared nodes','比较阈值并保留声明节点','Rebuild at 1, 3, 5 and 10 shared paragraphs. Thresholds change retained edges; the declared node set stays fixed. Centrality is a graph summary conditional on these choices, not a narrative truth.','按共享段落一、三、五、十重建。阈值改变边，节点集固定。中心性依赖这些选择，不是叙事事实。','''sensitivity=[]
for minimum in [1,3,5,10]:
 trial=mention_cooccurrence(paragraphs,patterns,minimum)["graph"]
 sensitivity.append({"minimum_shared_paragraphs":minimum,"nodes":trial.number_of_nodes(),"edges":trial.number_of_edges(),"isolates":len(list(nx.isolates(trial)))})
sensitivity=pd.DataFrame(sensitivity)
fig,ax=plt.subplots(figsize=(7,4));ax.plot(sensitivity.minimum_shared_paragraphs,sensitivity.edges,"o-")
ax.set(xlabel="Minimum shared paragraphs",ylabel="Retained edges",title="Threshold-sensitive cooccurrence representation");plt.tight_layout();plt.show()'''),
 step('Reconcile counts and export inspectable rules','核对数量并导出可检视规则','Check symmetric counts, all nodes and monotonic retained edges. Export patterns, counts and GraphML. Preserve isolated nodes and explain that surname ambiguity must be examined in context.','检查对称计数、完整节点及保留边单调性。导出模式、数量和 GraphML，保留孤立点，并说明姓氏歧义需回到语境核查。','''assert graph.number_of_edges()>0 and network["paragraph_presence"].sum()>0
assert np.array_equal(network["matrix"],network["matrix"].T) and np.all(np.diag(network["matrix"])==0)
assert set(graph)==set(patterns) and sensitivity.nodes.eq(8).all() and np.all(np.diff(sensitivity.edges)<=0)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);nx.write_graphml(graph,OUTPUT_DIR/"surface-mention-cooccurrence.graphml")
pd.DataFrame(network["matrix"],index=network["labels"],columns=network["labels"]).to_csv(OUTPUT_DIR/"shared-paragraph-counts.csv")
sensitivity.to_csv(OUTPUT_DIR/"threshold-sensitivity.csv",index=False)
(OUTPUT_DIR/"alias-rules.json").write_text(json.dumps(patterns,indent=2))
print("Count/node checks passed; interpretation remains conditional on alias rules")''')]

SECTIONS[COURSES[4]['id']]=[
 step('Define chapters and vocabulary rules','定义章节及词汇规则','Use 85 numbered chapters as exploratory documents. A declared short stop list, document-frequency limits and a 500-term cap define the representation. This analysis uses the full corpus and is not a held-out classifier.','使用 85 编号章节作为探索文档。声明短停词表、文档频率范围及 500 词上限，定义表示方式。使用整部语料，不是测试分类器。',CORPUS_LOAD+'''
stopwords=set("a an and are as at be been being but by can could did do does for from had has have he her hers him his i if in is it its me more most my no not of on one or our she so some than that the their them then there these they this those to too was we were what when where which who why will with would you your".split())
documents=chapter_table.text.tolist();model=tfidf_svd(documents,stopwords,min_df=3,max_df_fraction=.9,max_terms=500,components=3)
print("Documents:",len(documents),"; retained terms:",len(model["terms"]),"; TF-IDF row normalization: L2")'''),
 step('Read signed word directions','解读有符号词方向','TF-IDF uses smoothed idf=log((1+n)/(1+df))+1 and L2 document normalization. SVD is uncentered. Each component has signed coefficients with an arbitrary global sign; it is not a probability distribution of topics.','TF-IDF 使用平滑 idf=log((1+n)/(1+df))+1 及文档 L2 归一化。SVD 未中心化，成分有符号系数且整体符号任意，不是主题概率分布。','''component=1;loading=model["components"][component]
selected=np.argsort(abs(loading))[-15:];selected=selected[np.argsort(loading[selected])]
fig,ax=plt.subplots(figsize=(8,5));ax.barh([model["terms"][j] for j in selected],loading[selected])
ax.axvline(0,color="black",lw=1);ax.set(xlabel="Signed SVD coefficient",title="Second uncentered text direction; not topic probabilities");plt.tight_layout();plt.show()'''),
 step('Inspect chapter projection geometry','检查章节投影几何','Points are chapter documents; colors show source book identity. Geometry depends on vocabulary, normalization and truncation. Source-book separation does not establish author intention or a validated genre classifier.','点为章节文档，颜色为来源书籍。几何依赖词汇、归一化及截断，书籍分离不证明作者意图或有效体裁分类器。','''fig,ax=plt.subplots(figsize=(8,5))
for book_id in corpus:
 mask=chapter_table.book_id.eq(book_id).to_numpy();ax.scatter(model["scores"][mask,0],model["scores"][mask,1],label=corpus[book_id]["title"],s=25)
ax.set(xlabel="SVD1 score (uncentered)",ylabel="SVD2 score",title="Exploratory chapter geometry");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Read cosine similarity in the original TF-IDF space','解读原 TF-IDF 空间余弦相似度','Because rows are L2 normalized, their dot product gives original-space cosine similarity. This matrix concerns a declared bag-of-words representation, not identity of meaning, events or characters.','行经 L2 归一化，内积给出原空间余弦相似度。矩阵仅描述声明词袋表示，不等于意义、事件或人物身份相同。','''similarity=model["tfidf"]@model["tfidf"].T
fig,ax=plt.subplots(figsize=(7,6));im=ax.imshow(similarity,vmin=0,vmax=1,cmap="viridis")
ax.set(xlabel="Source chapter-document order",ylabel="Source chapter-document order",title="TF-IDF cosine similarity");fig.colorbar(im,ax=ax,label="Cosine similarity");plt.tight_layout();plt.show()'''),
 step('Reconcile normalization and export representation','核对归一化并导出表示','Check unit row norms, symmetric similarity and orthonormal retained directions. Export vocabulary and signed weights so a student can inspect influential terms and return to the original passages.','检查行单位范数、相似矩阵对称及保留方向正交。导出词汇与有符号权重，方便检视重要词并回到原段落。','''assert np.allclose(np.linalg.norm(model["tfidf"],axis=1),1)
assert np.allclose(similarity,similarity.T) and np.allclose(np.diag(similarity),1)
assert np.allclose(model["components"]@model["components"].T,np.eye(3))
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame(model["scores"],columns=["SVD1","SVD2","SVD3"]).assign(book=chapter_table.book,chapter=chapter_table.chapter).to_csv(OUTPUT_DIR/"chapter-projections.csv",index=False)
pd.DataFrame(model["components"].T,index=model["terms"],columns=["SVD1","SVD2","SVD3"]).to_csv(OUTPUT_DIR/"signed-term-directions.csv")
print("Normalization and orthogonality checked; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[5]['id']]=[
 step('Join a common dated cross-section','合并同年截面','Use 2023 economy-level GDP per capita in constant 2015 USD, population and life expectancy. Official metadata excludes aggregates. Keep missingness counts and current source income-group labels explicit.','使用 2023 经济体不变价人均 GDP、人口及预期寿命，按官方 metadata 排除汇总。明确缺失数量和来源当前收入组标签。','''wb=snapshot("worldbank");panel,economies,observations=worldbank_panel(wb)
year=2023;columns=["NY.GDP.PCAP.KD","SP.POP.TOTL","SP.DYN.LE00.IN"]
cross=panel.xs(year,level="year")[columns].rename(columns={columns[0]:"GDP_pc_constant_2015_USD",columns[1]:"population",columns[2]:"life_expectancy_years"})
coverage=cross.notna().sum();usable=cross.dropna().join(economies[["name","income_group"]])
assert usable.GDP_pc_constant_2015_USD.gt(0).all() and usable.population.gt(0).all()
assert usable.life_expectancy_years.between(0,110).all()
print("Year:",year,"; complete economies:",len(usable),"of",len(cross));display(coverage.to_frame("observed_economies"))
display(usable.head(8))'''),
 step('Read an economy-level association','解读经济体层面关联','The x axis is log-scaled constant-price GDP per capita and y is period life expectancy at birth. Each marker is one economy, not an individual. This does not estimate what raising an individual’s income would do to their lifespan.','横轴对数显示不变价人均 GDP，纵轴为时期出生预期寿命。每点是一经济体，不是个人，不估计提高个人收入会怎样改变寿命。','''fig,ax=plt.subplots(figsize=(8,5))
for group,part in usable.groupby("income_group"):ax.scatter(part.GDP_pc_constant_2015_USD,part.life_expectancy_years,label=group,s=20,alpha=.7)
ax.set(xscale="log",xlabel="GDP per capita (constant 2015 USD)",ylabel="Period life expectancy at birth (years)",title="2023 complete-economy cross-section");ax.legend(fontsize=8);plt.tight_layout();plt.show()''',cover=True),
 step('Inspect group distributions with a dated classification caveat','带分类年份说明检查组分布','Boxplots use current frozen source income-group metadata applied to 2023 observations. They do not reconstruct past group classification. Country values are not population-weighted household observations.','箱图把当前冻结收入组 metadata 应用于 2023 观测，不重建历史组分类。经济体数值不是按人口加权的家庭观测。','''groups=sorted(usable.income_group.unique())
fig,ax=plt.subplots(figsize=(9,4));ax.boxplot([usable.loc[usable.income_group.eq(g),"life_expectancy_years"] for g in groups],tick_labels=groups)
ax.set(ylabel="Period life expectancy (years)",title="Source current income-group metadata applied to 2023");plt.xticks(rotation=15);plt.tight_layout();plt.show()'''),
 step('Compare association measures and transformations','比较关联度量与变换','Pearson on log GDP and Spearman on raw GDP answer related but different descriptive questions. Bar coefficients are not causal effects or probability of a personal outcome. Report sample size and complete-case selection.','对数 GDP Pearson 与原 GDP Spearman 回答相关但不同的描述问题。条形系数不是因果效应或个人结果概率，须报告样本数及完整案例选择。','''pearson=float(np.corrcoef(np.log(usable.GDP_pc_constant_2015_USD),usable.life_expectancy_years)[0,1])
spearman=float(spearmanr(usable.GDP_pc_constant_2015_USD,usable.life_expectancy_years).statistic)
fig,ax=plt.subplots(figsize=(7,4));ax.bar(["Pearson: log GDP","Spearman: raw GDP"],[pearson,spearman])
ax.set(ylim=(-1,1),ylabel="Economy-level correlation",title=f"Descriptive association, n={len(usable)} complete economies");plt.tight_layout();plt.show()'''),
 step('Audit selection and export definitions','审计选择并导出定义','Confirm IDs belong to official nonaggregate economy metadata and correlation lies in [−1,1]. Save the complete-case rows and missingness, not just the scatter. A cross-section cannot resolve individual or causal questions.','核对 ID 来自官方非汇总 metadata，相关在 [−1,1]。保存完整案例与缺失情况，而不只保存散点；截面不能解决个人或因果问题。','''assert set(usable.index)<=set(economies.index) and -1<=pearson<=1 and -1<=spearman<=1
assert len(usable)==int(cross.notna().all(axis=1).sum())
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);usable.to_csv(OUTPUT_DIR/"2023-complete-economies.csv")
cross.to_csv(OUTPUT_DIR/"2023-source-with-missingness.csv")
(OUTPUT_DIR/"scope.json").write_text(json.dumps({"year":year,"units":{"GDP_pc":"constant 2015 USD","population":"persons","life_expectancy":"period years at birth"},"n_complete_economies":len(usable),"classification":"current frozen income-group metadata, not historical reconstruction","association":{"pearson_log_GDP":pearson,"spearman_GDP":spearman},"inference":"economy-level descriptive; no individual or causal claim"},indent=2))
print("Economy IDs, dated selection and units checked; exports:",OUTPUT_DIR)''')]

EXERCISES={}
notes=[
 (['Why exclude the duplicate TOC headings?','How would apostrophe/case decisions change counts?','The snapshots contain repeated headings in front matter. Token rules change the computational unit; original sources remain intact for verification.','Using re/Counter/NumPy/Pandas/Matplotlib, compare two documented token rules on the same declared chapters.','With the same packages, export all chapter labels and flag unsupported layouts rather than silently dropping text.','Chapter totals remain 61 and 24, token sums reconcile and full original/license text stays embedded.'],['为何排除重复目录标题？','撇号/大小写决策怎样影响数量？','前置目录含重复标题；分词规则改变计算单位，原来源完整保留用于核验。','仅用 re、Counter、NumPy、Pandas、Matplotlib 在同章节比较两种记录的分词规则。','同包导出全部标签，标不支持排版，不静默丢文本。','章节为 61、24，总词数一致，原文/许可完整内嵌。']),
 (['Why not rank authors by whole-book TTR?','Why keep matched windows and all starts?','TTR depends on length. Equal windows and recorded starts expose corpus variability without selecting favorable passages or inventing independent author samples.','Using re/Counter/NumPy/Pandas/Matplotlib, add 3000-token windows with the same replication and recorded seed.','With the same packages, compare nonoverlapping windows and report their dependence/scope.','All ratios stay in (0,1], sample lengths and starts are valid and observations are not new books.'],['为何不按整书 TTR 排作者？','为何保留匹配窗口及全部起点？','TTR 依赖长度。等长与起点公开变异，不挑有利段落或编造独立作者样本。','仅用 re、Counter、NumPy、Pandas、Matplotlib 加 3000 词等重复窗口及种子。','同包比较非重叠窗口并说明依赖/范围。','比例在 (0,1]，长度/起点合法，不当作新增书。']),
 (['Can query frequency determine sentiment?','What do overlapping context windows imply?','Meaning needs close reading. Overlap can count neighbor words repeatedly, so neighbor bars are window counts rather than independent utterances.','Using re/Counter/NumPy/Pandas/Matplotlib, add a declared exact-word query and export every match.','With the same packages, compare context widths 5 and 10 without retokenizing the source silently.','Direct/query totals agree, zero hits are handled and every displayed context has source chapter/order.'],['查询频率能确定情感吗？','窗口重叠意味着什么？','意义需细读，重叠可重复邻词，柱为窗口计数非独立语句。','仅用 re、Counter、NumPy、Pandas、Matplotlib 加一完整词查询并导出全部。','同包比较两侧五/十词，不暗改分词。','总数一致，处理零匹配，展示语境有来源章节/顺序。']),
 (['Does surname cooccurrence identify a social relationship?','Why preserve isolated declared nodes?','Surface aliases can conflate family/discussion mentions. Isolates document declared scope; centrality depends on pattern, paragraph and threshold choices.','Using re/NumPy/Pandas/Matplotlib/NetworkX, compare thresholds 1, 3 and 10 with fixed nodes/layout.','With the same packages, inspect ambiguous Darcy/Bingley contexts and export revised rules separately from the original.','Counts stay symmetric, nodes remain eight, self edges are excluded and relationship/intent is not inferred automatically.'],['姓氏共现确定社会关系吗？','为何保留声明孤立点？','表面别名可能混家族/讨论。孤立点记录范围，中心性依赖模式、段落和阈值。','仅用 re、NumPy、Pandas、Matplotlib、NetworkX 比较阈值一、三、十，固定节点/布局。','同包检查 Darcy/Bingley 歧义语境，修订规则另存。','对称计数、八节点、无自身边，不自动推关系/意图。']),
 (['Why are signed SVD directions not topic probabilities?','How do vocabulary/normalization decisions change geometry?','SVD components are signed linear directions with arbitrary global sign. Selected terms and weighting define the representation, not a universal semantic model.','Using re/Counter/NumPy/Pandas/Matplotlib, compare 300 and 500 retained terms and preserve representation parameters.','With the same packages, export both positive and negative influential terms and inspect their source chapters.','Rows have unit L2 norm, components are orthonormal, similarity is symmetric and no topic-probability claim is made.'],['为何有符号 SVD 不是主题概率？','词汇/归一化如何改几何？','SVD 为有符号线性方向且整体符号任意，选词及权重定义表示，不是普遍语义模型。','仅用 re、Counter、NumPy、Pandas、Matplotlib 比较三百/五百词并保存参数。','同包导出正负重要词并细读来源章节。','行 L2 范数一，方向正交、相似对称，不称主题概率。']),
 (['Why is this an ecological rather than individual association?','What does current metadata applied to 2023 mean?','The unit is an economy, not a person. Frozen current income-group labels do not reconstruct historical classification; missing selection and confounding remain.','Using NumPy/SciPy/Pandas/Matplotlib, repeat a declared common-year comparison and report changing sample coverage.','With the same packages, export complete-case and missing rows separately and label all units/current classifications.','Aggregates stay excluded, dates match, IDs/coverage reconcile and no individual or causal effect is inferred.'],['为何是生态层面而非个人关联？','当前 metadata 应用于 2023 意味什么？','单位为经济体，不是人；当前标签不重建历史分类，缺失选择和混杂仍存在。','仅用 NumPy、SciPy、Pandas、Matplotlib 重复声明同年比较并报告覆盖变化。','同包分别导完整/缺失行，注明单位/当前分类。','排除汇总、年份匹配、ID/覆盖一致，不推个人/因果效应。'])]
for c,(en,zh) in zip(COURSES,notes):EXERCISES[c['id']]=exercises(en,zh)
