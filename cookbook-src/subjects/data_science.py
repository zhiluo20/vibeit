"""Six full data-science lessons; fitting code is shared between language editions."""
from ._common import lesson,step,exercises,bilingual

COURSES=[
 lesson('ds01-iris-audit',1,'iris-data-audit','Audit a real measurement table','审计真实的 Iris 测量表','Trace 150 UCI Iris observations, inspect repeat measurements and units, and build an honest exploratory report.','追溯 150 条 UCI Iris 观测，检查重复测量和单位，并形成可核验的探索报告。',['iris'],['audit_numeric_table'],'audit','Data audit','数据审计',difficulty=1,icon='🔎'),
 lesson('ds02-iris-pca',2,'iris-pca','Understand standardized PCA','理解标准化 PCA','Use all four Iris measurements to inspect scaling, singular values, component directions and reconstruction error.','用 Iris 四个测量特征检查缩放、奇异值、主成分方向和重建误差。',['iris'],['audit_numeric_table','standardized_pca'],'dimensions','Dimension reduction','降维',icon='📊'),
 lesson('ds03-iris-knn',3,'iris-knn-validation','Train and evaluate a classifier without leakage','避免信息泄漏地训练和评估分类器','Reserve a stratified test set, select k inside training-only folds, then report held-out confusion and macro-F1.','先保留分层测试集，在训练集内选择 k，再报告测试混淆矩阵与宏平均 F1。',['iris'],['audit_numeric_table','stratified_holdout','stratified_folds','knn_predict','classification_metrics'],'prediction','Prediction & validation','预测与验证',minutes=60,icon='🎯'),
 lesson('ds04-wine-clusters',4,'wine-clustering','Inspect clusters in chemical measurements','检查 Wine 化学测量的聚类','Standardize 13 real Wine features, run reproducible k-means, and compare anonymous clusters with source cultivar codes.','标准化 13 个真实 Wine 特征，执行可复现的 k-means，并对照来源中的品种代码。',['wine'],['audit_numeric_table','standardized_pca','kmeans'],'dimensions','Dimension reduction','降维',minutes=60,icon='🍇'),
 lesson('ds05-bike-regression',5,'bike-regression','Build an interpretable rental-count regression','构建可解释的共享单车回归','Fit on 2011 and evaluate on 2012, distinguish conditional weather reconstruction from forecasting, and inspect error and drift.','用 2011 年拟合、2012 年评估，区分同日天气条件回归与预测，并检查误差与分布变化。',['bike'],['audit_numeric_table','ridge_fit_predict','regression_metrics'],'prediction','Prediction & validation','预测与验证',minutes=60,icon='🚲'),
 lesson('ds06-bike-backtesting',6,'bike-backtesting','Backtest one-day-ahead demand forecasts','回测一步向前的需求预测','Construct past-only lag features, refit expanding windows and compare ridge with two transparent persistence baselines.','构造仅使用过去观测的滞后特征，扩展窗口重新拟合，并与两种朴素基线比较。',['bike'],['ridge_fit_predict','regression_metrics'],'prediction','Prediction & validation','预测与验证',minutes=60,difficulty=3,icon='📅'),
]
for c in COURSES:
 if 'bike' in c['snapshots']:
  c['functions'].append('iso_datetimes');c['setup_imports']='from datetime import datetime\n'
 c['online_url']='https://archive.ics.uci.edu/dataset/'+('275' if 'bike' in c['id'] else '109' if 'wine' in c['id'] else '53')
 if 'iris' in c['snapshots']:
  c['data_note']=bilingual('These are frozen public measurements, not a new random population sample. The original UCI iris.data is retained, including its two source-documented transcription discrepancies. Repeated rounded feature values do not by themselves establish that two rows are the same plant.','这些是冻结的公开实测数据，不是新的总体随机样本。保留原始 UCI iris.data，包括来源说明的两处转录差异。舍入后的重复特征值本身不能证明两行属于同一株植物。')
 elif 'wine' in c['snapshots']:
  c['data_note']=bilingual('The public Wine table contains chemical measurements and cultivar codes. Original units are not completely specified, so standardized analyses use dimensionless coordinates and never invent concentration units. Codes are excluded from unsupervised fitting.','公开 Wine 表包含化学测量及品种代码。来源未完整声明单位，因此标准化分析使用无量纲坐标，不编造浓度单位。品种代码不参与无监督拟合。')
 else:
  c['data_note']=bilingual('The source contains one daily rental count per date in 2011–2012. These are rental events, not unique people. Casual and registered counts sum to the response and are excluded from predictors. Source-normalized daily weather fields are not silently relabelled as degrees Celsius.','来源记录 2011–2012 年每天的租赁次数，不是独立人数。casual 与 registered 之和是目标，因此不能作为预测变量。来源归一化的日天气字段不会被静默改写为摄氏度。')

IRIS_LOAD='''iris=snapshot("iris")
frame=pd.DataFrame(iris["rows"],columns=iris["columns"])
features=list(frame.columns[:4])
audit=audit_numeric_table(frame,features)
assert len(frame)==150 and frame["species"].nunique()==3
assert (frame[features]>0).all().all()
print("Audit:",audit,"; measurement unit: cm")
print("Source variant:",iris["variant"])
display(frame.head(8))'''
BIKE_LOAD='''bike=snapshot("bike")
frame=pd.DataFrame(bike["rows"],columns=bike["columns"])
frame["date"]=frame["dteday"].astype(str)
frame=frame.sort_values("date").reset_index(drop=True)
assert len(frame)==731 and frame["date"].is_unique
dates=iso_datetimes(frame.date)
assert all((b-a).total_seconds()==86400 for a,b in zip(dates,dates[1:]))
assert (frame["casual"]+frame["registered"]).eq(frame["cnt"]).all()
assert frame["cnt"].ge(0).all()
print("Complete daily observations:",len(frame),"; target: rentals/day")
display(frame[["date","cnt","temp","hum","windspeed"]].head(7))'''

SECTIONS={}
SECTIONS[COURSES[0]['id']]=[
 step('Load and audit the original records','加载并审计原始记录','Use row IDs, not feature values, as observation identity. Repeated feature vectors can occur at the reported measurement precision. Keep them visible; deleting them silently changes the data. The audit rejects non-finite numeric values and duplicate row IDs.','使用记录行 ID 识别观测。来源测量精度下可能出现相同特征向量；应展示这些记录，不能静默删除。审计会拒绝非有限数值及重复的行 ID。',IRIS_LOAD),
 step('Compare the class counts and feature distributions','比较类别数量与特征分布','Each box summarizes a measurement in centimetres: median, quartiles and conventional 1.5-IQR whiskers. Source class balance is a property of this dataset; it is not the prevalence of these species in nature.','箱线图以厘米为单位显示中位数、四分位数和 1.5 IQR 范围。来源中的类别平衡属于该数据集，不能当作自然界物种的比例。','''display(frame.groupby("species").size().rename("observations").to_frame())
fig,ax=plt.subplots(figsize=(8,4))
ax.boxplot([frame[c] for c in features],tick_labels=features)
ax.set_ylabel("Measurement (cm)");ax.tick_params(axis="x",rotation=20)
ax.set_title("Four observed Iris measurements");plt.tight_layout();plt.show()'''),
 step('Look at a pair of measurements','观察两个测量特征','Color identifies the source species code, not a learned cluster. The horizontal and vertical axes are petal length and width in centimetres. Separation in this projection motivates later modelling; it does not measure test-set accuracy.','颜色表示来源物种代码，不是拟合的聚类。横、纵轴分别为花瓣长度和宽度，单位为厘米。二维分离可以帮助提出建模问题，但不能作为测试准确率。','''fig,ax=plt.subplots(figsize=(7,5))
for label,part in frame.groupby("species"):
 ax.scatter(part[features[2]],part[features[3]],label=label,s=28,alpha=.75)
ax.set(xlabel="Petal length (cm)",ylabel="Petal width (cm)",title="Observed petal measurements")
ax.legend(fontsize=8);plt.tight_layout();plt.show()''',cover=True),
 step('Inspect pairwise association','检查成对关联','Pearson correlation is dimensionless and ranges from −1 to +1. It summarizes pooled linear association. Because the three groups have different locations, pooled correlation need not describe an association within each species.','Pearson 相关系数无量纲，范围为 −1 至 +1。它概括合并样本的线性关联；三组均值不同，因此合并相关性不一定描述组内关联。','''correlation=frame[features].corr()
fig,ax=plt.subplots(figsize=(6,5));im=ax.imshow(correlation,vmin=-1,vmax=1,cmap="coolwarm")
ax.set_xticks(range(4),features,rotation=30,ha="right");ax.set_yticks(range(4),features)
for i in range(4):
 for j in range(4):ax.text(j,i,f"{correlation.iloc[i,j]:.2f}",ha="center",va="center",fontsize=9)
fig.colorbar(im,ax=ax,label="Pearson correlation");plt.tight_layout();plt.show()'''),
 step('Reconcile and export the report','核对并导出报告','Confirm that category counts recover every row and correlation is symmetric. Export observed records separately from summaries so later students can reproduce the distinction.','确认类别数量能恢复全部记录，相关矩阵对称。分别导出观测记录与摘要，便于后续复现两者的区别。','''assert frame.groupby("species").size().sum()==len(frame)
assert np.allclose(correlation,correlation.T) and np.allclose(np.diag(correlation),1)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
frame.to_csv(OUTPUT_DIR/"iris-observations.csv",index=False)
frame.groupby("species")[features].agg(["mean","std","min","max"]).to_csv(OUTPUT_DIR/"measurement-summary.csv")
correlation.to_csv(OUTPUT_DIR/"correlation.csv")
(OUTPUT_DIR/"audit.json").write_text(json.dumps(audit,indent=2))
print("Checked",len(frame),"observations; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[1]['id']]=[
 step('Audit the PCA input','审计 PCA 输入','PCA uses a rows × features matrix. Species labels are retained only for reading the final figure. This is a descriptive analysis of all measurements, so it does not create an independent predictive evaluation.','PCA 使用记录 × 特征矩阵，物种标签只用于解读图表。这里分析全部测量值，属于描述性分析，没有形成独立的预测评估。',IRIS_LOAD),
 step('Standardize and decompose','标准化并分解','Subtract each feature mean and divide by its population SD (ddof=0). SVD then determines orthogonal directions of variation. The variance denominator is n−1; its common factor cancels in explained-variance ratios.','减去各特征均值，并除以总体标准差（ddof=0）。随后使用 SVD 求正交变化方向。方差分母为 n−1，共同因子在解释方差比例中抵消。','''values=frame[features].to_numpy(float)
pca=standardized_pca(values,components=2)
display(pd.DataFrame({"feature":features,"mean_cm":pca["mean"],"SD_cm":pca["scale"]}))
fig,ax=plt.subplots(figsize=(7,4));ax.bar(np.arange(1,5),100*pca["explained_ratio"])
ax.set(xlabel="Principal component",ylabel="Explained variance (%)",title="Variance after feature standardization",xticks=[1,2,3,4]);plt.tight_layout();plt.show()'''),
 step('Read the component scores','解读主成分得分','Points are observations and colors are source labels. Scores are dimensionless. The axes report the percentage of standardized variation; visible grouping is not a held-out classification result.','点代表观测，颜色代表来源标签，得分无量纲。坐标轴给出标准化后变化的解释比例；可见分组不等于独立测试集的分类结果。','''fig,ax=plt.subplots(figsize=(7,5))
for label in sorted(frame.species.unique()):
 mask=frame.species.eq(label).to_numpy();ax.scatter(*pca["scores"][mask].T,label=label,s=26)
ax.set(xlabel=f"PC1 ({pca['explained_ratio'][0]:.1%})",ylabel=f"PC2 ({pca['explained_ratio'][1]:.1%})",title="Standardized Iris PCA")
ax.legend(fontsize=8);plt.tight_layout();plt.show()''',cover=True),
 step('Connect directions to input features','将方向与输入特征联系起来','The signed loading heatmap shows coefficients of standardized features. Reversing an entire component changes neither distances nor variance. Coefficients describe this decomposition, not a causal feature effect.','载荷热图显示标准化特征的有符号系数。将整个主成分反号不会改变距离或方差。这些系数描述分解方向，不是因果效应。','''loadings=pd.DataFrame(pca["loadings"].T,index=features,columns=["PC1","PC2"])
fig,ax=plt.subplots(figsize=(5,5));im=ax.imshow(loadings,cmap="coolwarm",vmin=-1,vmax=1)
ax.set_xticks([0,1],["PC1","PC2"]);ax.set_yticks(range(4),features)
for i in range(4):
 for j in range(2):ax.text(j,i,f"{loadings.iloc[i,j]:.3f}",ha="center",va="center")
fig.colorbar(im,ax=ax,label="Signed coefficient");plt.tight_layout();plt.show()'''),
 step('Check an independent decomposition and export','用独立分解核对并导出','Compare SVD ratios with eigenvalues of the covariance matrix. Recover the original measurements with all four components; compare that exact reconstruction with the lossy two-component reconstruction.','用协方差矩阵特征值核对 SVD 的解释比例。四个主成分应恢复原始测量，再与有损的双主成分重建比较。','''eigenvalues=np.linalg.eigvalsh(np.cov(pca["standardized"],rowvar=False))[::-1]
assert np.allclose(pca["explained_ratio"],eigenvalues/eigenvalues.sum())
assert np.allclose(pca["loadings"]@pca["loadings"].T,np.eye(2))
full=standardized_pca(values,4)
reconstructed=(full["scores"]@full["loadings"])*full["scale"]+full["mean"]
assert np.allclose(reconstructed,values)
two=(pca["scores"]@pca["loadings"])*pca["scale"]+pca["mean"]
print("Two-component RMSE (cm):",float(np.sqrt(np.mean((values-two)**2))))
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame(pca["scores"],columns=["PC1","PC2"]).assign(species=frame.species).to_csv(OUTPUT_DIR/"pca-scores.csv",index=False)
loadings.to_csv(OUTPUT_DIR/"pca-loadings.csv")
pd.DataFrame({"PC":np.arange(1,5),"explained_ratio":pca["explained_ratio"]}).to_csv(OUTPUT_DIR/"variance.csv",index=False)
print("Independent checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[2]['id']]=[
 step('Reserve the test set first','先保留测试集','Use a reproducible 30% class-stratified holdout. Do not use its feature distribution to compute means/SDs, select k or rewrite the algorithm after seeing test errors. Duplicate rounded feature vectors remain documented rather than silently removed.','固定随机种子，按类别保留 30% 测试记录。不能用测试特征计算均值/标准差、选择 k，或看到测试错误后再改算法。保留并说明重复的舍入测量向量。',IRIS_LOAD+'''
values=frame[features].to_numpy(float);labels=frame.species.to_numpy()
train_indices,test_indices=stratified_holdout(labels,test_fraction=.3,seed=42)
assert not set(train_indices)&set(test_indices)
assert len(train_indices)+len(test_indices)==150
print("Training/test observations:",len(train_indices),len(test_indices))'''),
 step('Select k using training-only folds','只用训练集内交叉验证选择 k','Each fold fits its own scaler using the fold training rows. Validation indices are relative to the reserved training subset. Error bars show between-fold SD, not a confidence interval from independent experiments.','每折只用折内训练记录拟合缩放器。验证索引相对于保留的训练子集。误差条表示折间标准差，不是独立实验的置信区间。','''candidates=[1,3,5,7,9];folds=stratified_folds(labels[train_indices],5,seed=7)
cv=[]
for k in candidates:
 scores=[]
 for validation in folds:
  fitting=np.setdiff1d(np.arange(len(train_indices)),validation)
  x=values[train_indices[fitting]];mean=x.mean(axis=0);scale=x.std(axis=0)
  prediction=knn_predict((x-mean)/scale,labels[train_indices[fitting]],(values[train_indices[validation]]-mean)/scale,k)
  scores.append(np.mean(prediction==labels[train_indices[validation]]))
 cv.append(scores)
cv=np.asarray(cv);chosen_k=candidates[int(np.argmax(cv.mean(axis=1)))]
print("Training-only selected k:",chosen_k,"; ties choose the smallest candidate")
fig,ax=plt.subplots(figsize=(7,4));ax.errorbar(candidates,cv.mean(axis=1),yerr=cv.std(axis=1,ddof=1),fmt="o-")
ax.set(xlabel="k",ylabel="Fold accuracy",ylim=(0,1.05),title="Training-only stratified CV; bars = fold SD");plt.tight_layout();plt.show()'''),
 step('Evaluate the held-out predictions','评估保留测试集','Now fit one scaler on all training rows and predict the untouched holdout. The confusion matrix uses true classes as rows and predicted classes as columns; entries are observation counts. Macro-F1 gives each class equal weight.','现在仅用全部训练记录拟合一个缩放器，并预测保留测试集。混淆矩阵行是真实类别、列是预测类别，数值为记录数。宏平均 F1 对各类别赋予相同权重。','''mean=values[train_indices].mean(axis=0);scale=values[train_indices].std(axis=0)
prediction=knn_predict((values[train_indices]-mean)/scale,labels[train_indices],(values[test_indices]-mean)/scale,chosen_k)
classes=np.unique(labels);metrics=classification_metrics(labels[test_indices],prediction,classes)
print("Held-out accuracy:",metrics["accuracy"],"; macro-F1:",metrics["macro_f1"])
fig,ax=plt.subplots(figsize=(6,5));im=ax.imshow(metrics["confusion"],cmap="Blues")
short=[v.replace("Iris-","") for v in classes];ax.set_xticks(range(3),short,rotation=25);ax.set_yticks(range(3),short)
for i in range(3):
 for j in range(3):ax.text(j,i,str(metrics["confusion"][i,j]),ha="center",va="center")
ax.set(xlabel="Predicted class",ylabel="True class",title="Untouched test set");fig.colorbar(im,ax=ax,label="Observations");plt.tight_layout();plt.show()''',cover=True),
 step('Locate test errors without retuning','定位测试错误并保持评估边界','This projection uses two original measurements in cm. Crosses mark incorrect predictions; their positions help explain errors but are not permission to tune on the holdout. Document what a genuinely new evaluation dataset would require.','投影使用两个原始测量，单位为厘米。叉号标记错误预测，可以辅助解释错误，但不能据此对测试集调参。说明新的独立评估数据需要哪些条件。','''fig,ax=plt.subplots(figsize=(7,5))
for label in classes:
 mask=labels[test_indices]==label;ax.scatter(values[test_indices][mask,2],values[test_indices][mask,3],label=label,s=35)
wrong=prediction!=labels[test_indices]
ax.scatter(values[test_indices][wrong,2],values[test_indices][wrong,3],marker="x",color="black",s=90,label="Incorrect prediction")
ax.set(xlabel="Petal length (cm)",ylabel="Petal width (cm)",title="Test errors in an observed feature plane");ax.legend(fontsize=8);plt.tight_layout();plt.show()'''),
 step('Reconcile metrics and export predictions','核对指标并导出预测','Check the matrix total and diagonal accuracy with direct counting. Export the fixed split and every test prediction; retain the scaler and selected k so the calculation is inspectable.','用直接计数核对矩阵总数及对角线准确率。导出固定划分与全部测试预测，并保留缩放器和选择的 k。','''assert metrics["confusion"].sum()==len(test_indices)
assert np.isclose(np.trace(metrics["confusion"])/len(test_indices),np.mean(prediction==labels[test_indices]))
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"source_row":test_indices,"true":labels[test_indices],"predicted":prediction}).to_csv(OUTPUT_DIR/"test-predictions.csv",index=False)
pd.DataFrame(cv,index=candidates).to_csv(OUTPUT_DIR/"training-cv.csv")
(OUTPUT_DIR/"model.json").write_text(json.dumps({"k":chosen_k,"seed":42,"train_indices":train_indices.tolist(),"test_indices":test_indices.tolist(),"training_mean":mean.tolist(),"training_SD":scale.tolist()},indent=2))
print("Metric reconciliation passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[3]['id']]=[
 step('Separate features from source codes','将特征与来源类别代码分开','Wine contains 178 observations and 13 chemical features. Units are not fully specified by the source, so keep the original feature names and make no invented concentration claims. Cultivar codes are excluded from clustering inputs.','Wine 包含 178 条观测及 13 个化学特征。来源未完整声明单位，应保留原始特征名，不能编造浓度单位。品种代码不作为聚类输入。','''wine=snapshot("wine");frame=pd.DataFrame(wine["rows"],columns=wine["columns"])
features=list(frame.columns[1:]);audit=audit_numeric_table(frame,features)
assert len(frame)==178 and len(features)==13
values=frame[features].to_numpy(float);standardized=(values-values.mean(axis=0))/values.std(axis=0)
print("Audit:",audit,"; standardized features are dimensionless")
display(frame.head(6))'''),
 step('Compare objective values across k','比较不同 k 的目标函数','Run ten k-means++ restarts at each k from 1 to 6. Inertia is the sum of squared standardized Euclidean distances to assigned centres; it usually falls as k grows. We inspect k=3 as a declared teaching choice, not as proof of an optimal biological taxonomy.','在 k=1 至 6 下各执行十次 k-means++ 初始化。惯量是到所属中心的标准化欧氏距离平方和，随 k 增加通常下降。本课预先选择 k=3 检查，不把它作为最优分类的证明。','''solutions={k:kmeans(standardized,k,seed=42,restarts=10) for k in range(1,7)}
solution=solutions[3]
fig,ax=plt.subplots(figsize=(7,4));ax.plot(list(solutions),[solutions[k]["inertia"] for k in solutions],"o-")
ax.axvline(3,color="gray",linestyle="--");ax.set(xlabel="k",ylabel="Standardized squared-distance sum",title="Inertia is an objective, not classification accuracy");plt.tight_layout();plt.show()'''),
 step('Project anonymous clusters','投影匿名聚类','PCA only creates the display coordinates; k-means fitted all 13 standardized features. Cluster numbers and colors are arbitrary identifiers. Similar-looking clusters in two PCs may overlap in discarded directions.','PCA 仅提供显示坐标，k-means 使用全部 13 个标准化特征。聚类编号和颜色是任意标识。两个主成分中的可见分组可能在被舍弃的方向上不同。','''pca=standardized_pca(values,2)
fig,ax=plt.subplots(figsize=(7,5))
for cluster in range(3):
 mask=solution["labels"]==cluster;ax.scatter(*pca["scores"][mask].T,label=f"Cluster {cluster}",s=25)
ax.set(xlabel="PC1 score",ylabel="PC2 score",title="Wine clusters; fitted in 13 dimensions");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Compare with withheld cultivar codes','对照未参与拟合的品种代码','The contingency table is a descriptive comparison after fitting. Rows use source cultivar codes and columns use anonymous cluster IDs. Do not compute accuracy by directly equating these unrelated label numbers.','拟合完成后使用列联表进行描述性比较。行是来源品种代码，列是匿名聚类 ID，不能直接将这两套无关编号相等当作准确率。','''table=pd.crosstab(frame.cultivar,pd.Series(solution["labels"],name="cluster"))
display(table)
fig,ax=plt.subplots(figsize=(6,4));im=ax.imshow(table,cmap="Blues")
ax.set_xticks(range(3),table.columns);ax.set_yticks(range(3),table.index)
for i in range(3):
 for j in range(3):ax.text(j,i,str(table.iloc[i,j]),ha="center",va="center")
ax.set(xlabel="Anonymous cluster",ylabel="Source cultivar code",title="Post-fit contingency counts");fig.colorbar(im,ax=ax,label="Observations");plt.tight_layout();plt.show()'''),
 step('Check the objective and export assignments','核对目标函数并导出分配','Recompute the final objective directly from points and centres. The stored update history must not increase. Export the standardized centres with assignments and objective values; zero clusters or non-finite input should fail instead of yielding a plausible-looking plot.','用观测和中心直接重新计算目标函数。更新历史不应增加。导出标准化中心、分配结果及目标值；非法聚类数或非有限输入应报错。','''assert table.to_numpy().sum()==178
assert np.isclose(solution["inertia"],np.sum((standardized-solution["centers"][solution["labels"]])**2))
assert np.all(np.diff(solution["history"])<=1e-8)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
frame.assign(cluster=solution["labels"]).to_csv(OUTPUT_DIR/"wine-clusters.csv",index=False)
pd.DataFrame(solution["centers"],columns=features).to_csv(OUTPUT_DIR/"standardized-centres.csv",index=False)
pd.DataFrame({"k":list(solutions),"inertia":[solutions[k]["inertia"] for k in solutions]}).to_csv(OUTPUT_DIR/"inertia.csv",index=False)
print("Objective and count checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[4]['id']]=[
 step('Audit dates, targets and source normalization','审计日期、目标与来源归一化','Daily observations span 2011 and 2012. The target is rentals per day, not unique people. Temperature, humidity and wind fields retain source normalization; the daily temperature conversion is not inferred from an hourly-only source note.','日数据覆盖 2011 与 2012 年，目标是每日租赁次数，不是独立人数。温度、湿度和风速保留来源归一化方式，不根据仅适用于小时数据的说明推断日数据温度换算。',BIKE_LOAD),
 step('Declare the split and permitted predictors','声明划分与允许的预测变量','Train on 2011 and test on 2012. Predictors include source-normalized weather, a working-day flag and elapsed time. Casual/registered counts are excluded because they sum to the target. Same-day observed weather makes this conditional regression, not a future-weather forecast.','2011 年用于训练，2012 年用于测试。特征包括来源归一化天气、工作日标记及已过去天数。casual/registered 与目标相加关系明确，因此排除。同日实测天气使本课属于条件回归，而非未来天气预测。','''frame["elapsed_days"]=[(value-dates[0]).days for value in dates]
features=["temp","hum","windspeed","workingday","elapsed_days"]
audit_numeric_table(frame,features+["cnt"])
train=np.array([value.year==2011 for value in dates]);test=~train
assert train.sum()==365 and test.sum()==366
fig,ax=plt.subplots(figsize=(9,4));ax.plot(dates,frame.cnt,color="gray",lw=1)
ax.axvline(datetime(2012,1,1),color="red",linestyle="--",label="2011 fit / 2012 test")
ax.set(xlabel="Date",ylabel="Rentals/day",title="Chronological split and observed demand");ax.legend();plt.tight_layout();plt.show()'''),
 step('Fit with training-only scale estimates','只用训练集拟合缩放与系数','Ridge minimizes squared error plus a penalty on standardized feature coefficients; the intercept is unpenalized. Solve an augmented least-squares system rather than explicitly inverting a matrix. Penalty=1 is declared before examining test outcomes.','岭回归最小化平方误差并惩罚标准化特征系数，截距不惩罚。使用增广最小二乘求解，避免显式求逆。penalty=1 在检查测试结果前声明。','''model=ridge_fit_predict(frame.loc[train,features].to_numpy(),frame.loc[train,"cnt"].to_numpy(),frame.loc[test,features].to_numpy(),penalty=1.0)
prediction=model["predictions"];truth=frame.loc[test,"cnt"].to_numpy(float)
metrics=regression_metrics(truth,prediction)
print("2012 held-out metrics:",metrics)
print("Negative predictions (not silently clipped):",int(np.sum(prediction<0)))
display(pd.DataFrame({"term":["intercept"]+features,"coefficient":model["coefficients"]}))
fig,ax=plt.subplots(figsize=(6,5));ax.scatter(truth,prediction,s=13,alpha=.5)
limit=[min(truth.min(),prediction.min()),max(truth.max(),prediction.max())];ax.plot(limit,limit,"k--")
ax.set(xlabel="Observed rentals/day",ylabel="Predicted rentals/day",title="2012 conditional predictions");plt.tight_layout();plt.show()''',cover=True),
 step('Inspect time-dependent errors','检查随时间变化的误差','Residuals are predicted minus observed rentals/day. A long run of errors in one direction can indicate dataset shift or missing predictors. R² is a held-out descriptive score and can be negative; it is not proof of causal effects or deployment accuracy.','残差为预测减去观测，单位为租赁次数/日。连续同方向误差可能提示分布变化或遗漏特征。测试 R² 可以为负，也不证明因果关系或部署准确性。','''residual=prediction-truth
fig,ax=plt.subplots(figsize=(9,4));ax.plot(iso_datetimes(frame.loc[test,"date"]),residual,lw=1)
ax.axhline(0,color="black",linestyle="--");ax.set(xlabel="Date in 2012",ylabel="Prediction − observation (rentals/day)",title="Chronological regression errors");plt.tight_layout();plt.show()'''),
 step('Reconcile errors and export the model report','核对误差并导出模型报告','Check RMSE and the fitted training mean directly. Export every held-out row and the training-only scaler. A student who adds leaked target components should expect artificially improved errors, then reject that model for the intended workflow.','直接核对 RMSE 与训练均值。导出全部测试记录和训练缩放器。若加入目标组成字段，会人为改善误差，但该模型不满足本课的预测信息边界。','''assert np.isclose(metrics["rmse"],np.linalg.norm(prediction-truth)/np.sqrt(len(truth)))
assert np.allclose(model["mean"],frame.loc[train,features].mean())
assert not {"casual","registered","cnt"}&set(features)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"date":frame.loc[test,"date"],"observed_rentals":truth,"predicted_rentals":prediction,"error":residual}).to_csv(OUTPUT_DIR/"2012-predictions.csv",index=False)
(OUTPUT_DIR/"model.json").write_text(json.dumps({"features":features,"penalty":1.0,"training_year":2011,"test_year":2012,"mean":model["mean"].tolist(),"scale":model["scale"].tolist(),"coefficients":model["coefficients"].tolist(),"metrics":metrics},indent=2))
print("Training-only scale and metric checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[5]['id']]=[
 step('Make strictly past-only features','构造严格使用过去的特征','Shift counts before creating the seven-day average. Each row predicts its own day using previous observations and known calendar information. This is sequential one-day-ahead forecasting; observed test outcomes become legitimate inputs for later days, not for their own prediction.','先移位计数，再计算过去七日均值。每一行使用此前观测及已知日历信息预测当日。这是顺序的一步预测：已经观测的测试结果可供后续日期使用，不能用于预测其自身。',BIKE_LOAD+'''
frame["lag1"]=frame.cnt.shift(1);frame["lag7"]=frame.cnt.shift(7)
frame["past7_mean"]=frame.cnt.shift(1).rolling(7).mean()
frame["weekday_sin"]=np.sin(2*np.pi*np.array([value.weekday() for value in dates])/7)
frame["weekday_cos"]=np.cos(2*np.pi*np.array([value.weekday() for value in dates])/7)
model_frame=frame.dropna(subset=["lag1","lag7","past7_mean"]).reset_index(drop=True)
features=["lag1","lag7","past7_mean","weekday_sin","weekday_cos"]
assert np.isclose(model_frame.iloc[0].past7_mean,frame.cnt.iloc[:7].mean())
display(model_frame[["date","cnt"]+features].head(6))'''),
 step('Refit expanding training windows','用扩展训练窗口重新拟合','For each 2012 day, fit only rows with earlier dates. Penalty=10 is fixed for this exercise. Persistence uses yesterday’s demand; seasonal persistence uses demand seven days earlier. Neither baseline nor model can read the same-day target.','对每个 2012 年日期，仅用更早记录拟合。penalty=10 为预设参数。两种朴素基线分别使用昨日和七日前需求；模型与基线均不能读取同日目标。','''start=int(np.flatnonzero(np.array([value.year==2012 for value in iso_datetimes(model_frame.date)]))[0])
forecasts=[]
for position in range(start,len(model_frame)):
 history=model_frame.iloc[:position];current=model_frame.iloc[position:position+1]
 fitted=ridge_fit_predict(history[features].to_numpy(),history.cnt.to_numpy(),current[features].to_numpy(),penalty=10.0)
 forecasts.append({"date":current.date.iloc[0],"training_end":history.date.iloc[-1],"observed":float(current.cnt.iloc[0]),"ridge":float(fitted["predictions"][0]),"yesterday":float(current.lag1.iloc[0]),"last_week":float(current.lag7.iloc[0])})
result=pd.DataFrame(forecasts)
assert result.training_end.lt(result.date).all()
scores=pd.DataFrame({name:regression_metrics(result.observed,result[name]) for name in ["ridge","yesterday","last_week"]}).T
display(scores)
print("Expanding-window predictions:",len(result),"; all training dates precede forecast dates")'''),
 step('Read a held-out forecast interval','阅读测试期间预测轨迹','The first 90 test days show observed rentals and three forecasts in rentals/day. Adjacent points belong to a time series, so errors are not automatically independent. A historical winner in this interval is not guaranteed to remain best.','展示测试期前 90 天的观测及三种预测，单位为租赁次数/日。相邻记录属于时间序列，误差不自动独立。某方法在此历史区间领先，不保证以后仍然最佳。','''fig,ax=plt.subplots(figsize=(9,4));part=result.iloc[:90]
ax.plot(iso_datetimes(part.date),part.observed,color="black",label="Observed",lw=1.5)
for name in ["ridge","yesterday","last_week"]:ax.plot(iso_datetimes(part.date),part[name],label=name,alpha=.75,lw=1)
ax.set(xlabel="Forecast date",ylabel="Rentals/day",title="One-day-ahead forecasts; first 90 test days");ax.legend(ncol=2);plt.tight_layout();plt.show()''',cover=True),
 step('Compare errors by month','按月份比较误差','Monthly MAE is the mean absolute daily error within each month. Every method is evaluated on the same dates. Separate months expose seasonal changes that an overall average can hide; this retrospective breakdown is not a new training rule.','月 MAE 是月内每日绝对误差的均值，各方法使用同一批日期。月份分层有助于发现总均值遮盖的季节变化，但这种事后比较不是新的调参规则。','''monthly=pd.DataFrame({name:(result[name]-result.observed).abs().groupby([value.month for value in iso_datetimes(result.date)]).mean() for name in ["ridge","yesterday","last_week"]})
fig,ax=plt.subplots(figsize=(9,4));monthly.plot.bar(ax=ax)
ax.set(xlabel="Test month in 2012",ylabel="MAE (rentals/day)",title="Forecast errors on common dates");plt.tight_layout();plt.show()'''),
 step('Inspect residual dependence','检查残差依赖','Lag correlations compare paired residuals separated by 1–30 days. They are descriptive coefficients, not significance tests. Serial dependence motivates time-respecting validation and block-based uncertainty methods rather than a random row split.','滞后相关比较相隔 1–30 天的成对残差，是描述性系数而非显著性检验。时间依赖提示需要尊重日期顺序的验证与分块不确定性方法。','''residual=(result.ridge-result.observed).to_numpy()
lags=np.arange(1,31);autocorrelation=np.array([np.corrcoef(residual[:-lag],residual[lag:])[0,1] for lag in lags])
fig,ax=plt.subplots(figsize=(8,4));ax.stem(lags,autocorrelation)
ax.set(xlabel="Lag (days)",ylabel="Residual correlation",ylim=(-1,1),title="Descriptive dependence of held-out errors");plt.tight_layout();plt.show()'''),
 step('Audit information time and export the backtest','审计信息时间并导出回测','Reconcile baseline predictions with shifted original observations, check every training cutoff and export the full backtest. Resetting saved outputs before rerunning must reproduce the same predictions within numerical precision.','用移位后的原始观测核对基线，检查全部训练截止时间，并导出完整回测。清空输出后重新运行应在数值精度内复现预测。','''assert len(result)==366 and result.date.is_unique
assert np.allclose(result.yesterday,model_frame.iloc[start:].lag1)
assert np.allclose(result.last_week,model_frame.iloc[start:].lag7)
assert np.isclose(scores.loc["ridge","mae"],np.mean(np.abs(residual)))
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
result.to_csv(OUTPUT_DIR/"one-day-backtest.csv",index=False);scores.to_csv(OUTPUT_DIR/"forecast-metrics.csv")
monthly.to_csv(OUTPUT_DIR/"monthly-mae.csv")
(OUTPUT_DIR/"protocol.json").write_text(json.dumps({"horizon_days":1,"features":features,"penalty":10.0,"training":"all earlier dates","test_year":2012,"observed_test_outcomes":"available only for subsequent forecast days"},indent=2))
print("Information-time checks passed; exports:",OUTPUT_DIR)''')]

EXERCISES={}
contents=[
(['How many source observations belong to each species?','Compare pooled correlation with within-species correlation.','There are 50 observations per source class. Grouped correlations can differ because pooling combines within-group variation and between-group mean differences.','Using only NumPy, Pandas and Matplotlib, add separate within-species correlation heatmaps without deleting repeated measurement vectors.','Using the same allowed packages, flag duplicate rounded measurement vectors and list their row IDs; do not remove them automatically.','Check totals remain 150, every original row ID survives and each grouped matrix is symmetric.'],
 ['各来源物种有多少条观测？','比较合并相关矩阵与组内相关矩阵。','每类各 50 条。合并相关性同时混合组内变化和组间均值差异，因此与组内相关性可能不同。','仅用 NumPy、Pandas、Matplotlib 增加各物种的组内相关热图，不删除重复测量向量。','使用同样允许的包，标记重复的舍入测量向量并列出行 ID，不自动删除。','确认记录仍为 150 条，原始行 ID 全部保留，各组矩阵对称。']),
(['Reconstruct measurements using one, two and four components.','Repeat PCA without variance scaling; explain why the geometry changes.','Four components recover the finite input matrix. Fewer components generally increase reconstruction error; centering alone weights features according to their original spread.','Using NumPy/Pandas/Matplotlib, add a reconstruction-error curve for 1–4 components, keeping the original decomposition checks.','Using the same packages, compare centered-only and standardized PCA with clear axis/unit captions.','Full reconstruction must match the input; explained ratios sum to one and every loading basis is orthonormal.'],
 ['用一个、两个和四个主成分重建测量。','不进行方差缩放再做 PCA，解释几何变化。','四个主成分恢复有限输入矩阵。较少成分一般增加重建误差；仅中心化会按原始特征分散程度加权。','仅用 NumPy、Pandas、Matplotlib 增加 1–4 个成分的重建误差曲线，保留原分解校验。','使用同样的包比较仅中心化与标准化 PCA，并说明坐标和单位。','完整重建与输入一致，解释比例之和为一，载荷基正交归一。']),
(['Explain why a fold needs its own feature scaler.','Compare accuracy and macro-F1 using the saved confusion matrix.','A validation fold cannot influence fitting of the preprocessing step. Accuracy weights observations; macro-F1 weights class F1 values equally. Both may coincide on some balanced predictions.','With only NumPy/Pandas/Matplotlib, add k=11 and k=13 to the training-only CV candidates and retain the untouched test split.','With the same packages, report per-class precision and recall from the saved holdout confusion matrix.','Verify no train/test overlap; each fold scaler uses only fitting rows; confusion totals equal 45 and accuracy matches direct counting.'],
 ['解释为何每个交叉验证折需要自己的缩放器。','用保存的混淆矩阵比较准确率和宏平均 F1。','验证折不能参与预处理拟合。准确率按观测加权，宏平均 F1 对类别 F1 等权；某些平衡预测下两者可能相同。','仅用 NumPy、Pandas、Matplotlib 在训练集 CV 中加入 k=11、13，保留固定测试划分。','使用同样的包，从测试混淆矩阵报告每类精确率和召回率。','确认训练/测试无重叠，每折缩放只用拟合记录，混淆矩阵总数 45，准确率与直接计数一致。']),
(['Explain why cluster IDs cannot be equated with cultivar codes.','Repeat ten-restart clustering with seed=7 and compare objective values.','Cluster IDs are arbitrary and can be permuted without changing membership. Different initializations can reach different local minima; source-code comparison is descriptive and occurs after fitting.','Using NumPy/Pandas/Matplotlib, add a labelled standardized-centre heatmap without including cultivar codes in the distance calculation.','Using the same packages, compare one and ten restarts at k=3 and show both objective histories.','Recomputed inertia must match, histories must not increase, assignment counts sum to 178 and all centres are finite.'],
 ['说明聚类 ID 为何不能直接等同于品种代码。','将十次初始化的随机种子改为 7，比较目标值。','聚类 ID 可任意置换而不改变成员关系。不同初始化可能进入不同局部最优；与来源代码的比较属于拟合后的描述分析。','仅用 NumPy、Pandas、Matplotlib 增加标准化中心热图，不将品种代码加入距离计算。','使用同样的包，在 k=3 时比较一次与十次初始化，展示各自目标更新历史。','重算惯量一致，历史不增加，分配数量为 178，全部中心有限。']),
(['Why would casual and registered create target leakage?','Would observed same-day weather be available for a real next-day prediction?','Their sum equals the response. Same-day measured weather makes this a conditional regression; a next-day system would need genuine weather forecasts or past-only features.','Using NumPy/Pandas/Matplotlib, compare penalties 0, 1 and 10 on training-only chronological folds, then evaluate one final choice on 2012.','Using the same packages, add monthly test-error summaries and counts of negative predictions without silently clipping them.','The test year stays excluded from fitting and tuning, scaler statistics match training rows and error units remain rentals/day.'],
 ['为何 casual 与 registered 会形成目标泄漏？','真实下一日预测是否能使用同日实测天气？','两者之和就是目标。同日实测天气使本课成为条件回归；下一日系统需要真实天气预报或仅过去的特征。','仅用 NumPy、Pandas、Matplotlib 在训练集时间折中比较惩罚 0、1、10，最终只选择一次方法评估 2012 年。','使用同样的包增加月度测试误差和负预测数量，不静默裁剪。','测试年不参与拟合或调参，缩放统计量来自训练行，误差单位为租赁次数/日。']),
(['Explain why rolling(7).mean() must follow shift(1).','Explain how a sequential one-day forecast differs from a fixed multi-day forecast.','Without the shift, the current target enters its own feature. Sequential evaluation can use newly observed outcomes for subsequent days; a fixed multi-day forecast cannot use future realized counts.','Using NumPy/Pandas/Matplotlib, add a past-14-day mean and retain strict earlier-date training cutoffs.','Using the same packages, compare expanding windows with a 180-day rolling training window, keeping the same test dates and declared penalties.','Each training_end precedes its forecast date, lag means equal explicit past slices, 366 common forecasts are exported and no same-day target enters a predictor.'],
 ['解释为何 rolling(7).mean() 前需要 shift(1)。','说明顺序一步预测与固定多日预测有何差别。','不移位会把当前目标混入特征。顺序评估可将新观测供后续日期使用；固定多日预测不能读取未来真实计数。','仅用 NumPy、Pandas、Matplotlib 增加过去 14 日均值，保留更早日期的训练截止约束。','使用同样的包比较扩展窗口与 180 日滚动训练窗口，保持相同测试日期及预设惩罚。','每个 training_end 早于预测日期，滞后均值等于显式过去切片，导出 366 个共同预测，不将同日目标放入特征。'])]
for course,(en,zh) in zip(COURSES,contents):EXERCISES[course['id']]=exercises(en,zh)
