"""Six public-indicator and historical currency-risk teaching workflows."""
from ._common import lesson,step,exercises,bilingual

COURSES=[
 lesson('ec01-real-growth',1,'real-growth-indicators','Compare real economic growth indicators','比较实际经济增长指标','Audit economy/year records and separate constant-price levels, rebased growth and a common-year comparison.','审计经济体/年度记录，区分不变价水平、重定指数增长及同年比较。',['worldbank'],['worldbank_panel'],'indicators','Economic indicators','经济指标',discipline='economics',difficulty=1,icon='🌍'),
 lesson('ec02-inflation',2,'inflation-real-values','Distinguish CPI, inflation and real values','区分 CPI、通胀与实值','Rebase an observed price index, reconcile annual changes and deflate a stated hypothetical nominal amount.','重定观测价格指数，核对年度变化，并对声明的假设名义金额做实值换算。',['worldbank'],['worldbank_panel'],'indicators','Economic indicators','经济指标',discipline='economics',icon='🧾'),
 lesson('ec03-inequality',3,'inequality-observation-years','Audit inequality observations and their years','审计不平等观测及其年份','Preserve absent years and compare dated Gini observations without manufacturing a synchronized ranking.','保留缺失年份，比较带年份的 Gini 观测，不制造同步排名。',['worldbank'],['worldbank_panel'],'indicators','Economic indicators','经济指标',discipline='economics',icon='⚖️'),
 lesson('ec04-fx-returns',4,'currency-return-units','Compute currency returns with explicit quote units','按明确报价单位计算汇率收益','Invert ECB foreign-units-per-euro quotes before calculating euro-valued price returns and historical associations.','先将 ECB 外国单位/欧元报价取倒数，再计算欧元计价价格收益和历史关联。',['ecb'],[],'risk','Historical risk analysis','历史风险分析',discipline='economics',icon='💱'),
 lesson('ec05-portfolio-variance',5,'currency-portfolio-variance','Evaluate constrained historical variance','评估受约束的历史方差','Fit a long-only covariance model on training years and evaluate fixed hypothetical weights against an equal-weight baseline.','用训练年份拟合多头协方差模型，以固定假设权重和等权基线比较测试行为。',['ecb'],['minimum_variance_weights'],'risk','Historical risk analysis','历史风险分析',discipline='economics',minutes=60,difficulty=3,icon='📊',setup_imports='from scipy.optimize import minimize\n',packages=['numpy','pandas','scipy','matplotlib','IPython']),
 lesson('ec06-tail-risk',6,'empirical-tail-risk','Reconcile empirical tail risk and block resampling','核对经验尾部风险与分块重采样','Define inverse-CDF VaR and fractional-tail ES for a hypothetical currency basket, then inspect conditional resampling variability.','为假设货币篮子定义逆 CDF VaR 和分数尾部 ES，再检查条件重采样变异。',['ecb'],['empirical_tail_risk','circular_block_resample'],'risk','Historical risk analysis','历史风险分析',discipline='economics',minutes=60,difficulty=3,icon='📉'),
]
for c in COURSES:
 if 'worldbank' in c['snapshots']:
  c['online_url']='https://api.worldbank.org/v2/indicator/NY.GDP.PCAP.KD?format=json'
  c['data_note']=bilingual('World Bank records retain definitions, missing observations and reference years. The six economies are declared examples, not a random global sample. Country averages, price-basket conversions and Gini indices describe different quantities; survey concepts and coverage can differ.','World Bank 记录保留定义、缺失观测及参考年。六个经济体为声明例子，不是全球随机样本。国家均值、价格篮子换算和 Gini 指数描述不同量，调查概念及覆盖可能不同。')
 else:
  c['online_url']='https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?startPeriod=2024-01-01&endPeriod=2024-12-31&format=csvdata'
  c['data_note']=bilingual('Historical price-only currency examples use hypothetical daily rebalancing, excluding interest/carry, fees, execution costs and tax. They do not establish future performance or an investment recommendation. Source: ECB; original reference rates are available free of charge at the ECB. Inversions, returns and risk statistics are derived course calculations, not ECB statistics.','历史价格型货币例子假设每日再平衡，不含利息/套息、费用、成交成本和税，不确定未来表现或构成投资建议。来源：ECB，原始参考汇率可在 ECB 免费取得。倒数、收益和风险统计为课程派生计算，不是 ECB 统计。')

WB_LOAD='''wb=snapshot("worldbank");panel,economies,observations=worldbank_panel(wb)
countries=["CHN","USA","DEU","BRA","IND","ZAF"]
assert set(countries)<=set(economies.index)
print("Economy/year records:",len(panel),"; official aggregates excluded; missing values preserved")
display(economies.loc[countries,["name","region","income_group"]])'''
for c in COURSES[3:]:
 c['functions'].append('iso_datetimes');c['setup_imports']=c.get('setup_imports','')+'from datetime import datetime\n'

FX_LOAD='''ecb=snapshot("ecb");rates=pd.DataFrame(ecb["rows"])
rates["date"]=rates["Date"].astype(str);rates=rates.set_index("date").sort_index()
currencies=ecb["currency_order"];original_dates=len(rates);rates=rates[currencies].dropna()
assert rates.index.is_unique and rates.index.is_monotonic_increasing and (rates>0).all().all()
prices=1/rates;returns=prices.pct_change(fill_method=None).iloc[1:]
print(ecb["source_notice"])
print("Quote:",ecb["quote"],"; common complete dates:",len(rates),"of",original_dates)
display(rates.head(6))'''
SECTIONS={}
SECTIONS[COURSES[0]['id']]=[
 step('Audit economy and indicator definitions','审计经济体及指标定义','NY.GDP.PCAP.KD is GDP per capita in constant 2015 US dollars. Use official economy metadata to exclude aggregates. The selection is a worked example, not a population survey.','NY.GDP.PCAP.KD 为 2015 不变价美元人均 GDP。用官方经济体 metadata 排除汇总地区；此选择是案例，不是总体调查。',WB_LOAD+'''
indicator="NY.GDP.PCAP.KD";levels=panel[indicator].unstack("iso3").reindex(columns=countries)
print("Indicator:",wb["indicators"][indicator]["name"])
assert levels.dropna().gt(0).all().all()'''),
 step('Compare observed constant-price levels','比较观测不变价水平','Missing years remain gaps. A higher absolute level does not imply a higher growth rate. Source national-accounting and conversion conventions matter for cross-economy interpretation.','缺失年保留空缺。绝对水平较高不意味着增长率较高，跨经济体解释须考虑来源核算及换算约定。','''fig,ax=plt.subplots(figsize=(9,5))
for code in countries:ax.plot(levels.index,levels[code],marker="o",ms=3,label=economies.loc[code,"name"])
ax.set(xlabel="Indicator year",ylabel="Real GDP per capita (constant 2015 USD)",title="Frozen source levels; missing observations remain missing");ax.legend(fontsize=8);plt.tight_layout();plt.show()'''),
 step('Separate rebased growth from size','区分重定增长与规模','Set each observed 2010 level to 100. The chart compares relative change, not economy size or household wealth. Missing or zero baseline values require explicit handling.','把各自有效 2010 值定为 100。该图比较相对变化，不代表经济体规模或家庭财富；缺失/零基值须明确处理。','''base=levels.loc[2010];assert base.notna().all() and base.gt(0).all();indexed=100*levels/base
fig,ax=plt.subplots(figsize=(9,5))
for code in countries:ax.plot(indexed.index,indexed[code],label=economies.loc[code,"name"])
ax.set(xlabel="Indicator year",ylabel="Real GDP-per-capita index (2010=100)",title="Relative growth under a common baseline");ax.legend(fontsize=8);plt.tight_layout();plt.show()''',cover=True),
 step('Use a common dated cross-section','使用同年截面','Use 2023 for every declared economy. Mixing the latest available years changes the comparison. Economy-level averages do not give the complete distribution of individual incomes.','声明经济体统一使用 2023。混合最近可得年份会改变比较；经济体均值不提供个人收入完整分布。','''cross=levels.loc[2023];display(cross.rename("constant_2015_USD").to_frame())
fig,ax=plt.subplots(figsize=(8,4));ax.barh([economies.loc[c,"name"] for c in countries],cross)
ax.set(xlabel="Real GDP per capita (constant 2015 USD)",title="Common reference year: 2023");plt.tight_layout();plt.show()'''),
 step('Reconcile and export levels and changes','核对并导出水平及变化','Use fill_method=None in percent changes, avoiding invented zero changes at missing observations. Export original levels separately from rebased indices and calculated rates.','变化率使用 fill_method=None，避免缺失观测变成虚构零变化。原水平、重定指数和计算变化率分别导出。','''growth=100*levels.pct_change(fill_method=None)
assert np.allclose(indexed.loc[2010],100) and growth.loc[2010].isna().all()
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);levels.to_csv(OUTPUT_DIR/"real-GDP-per-capita.csv")
indexed.to_csv(OUTPUT_DIR/"2010-base-index.csv");growth.to_csv(OUTPUT_DIR/"annual-percent-change.csv")
print("Baseline and missing-year checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[1]['id']]=[
 step('Declare the price index and hypothetical amount','声明价格指数和假设金额','Use US CPI and rebase its observed 2010 value. The constant nominal 1000 USD is a teaching input, not invented wage or household-income data.','使用美国 CPI 并重定有效 2010 基值。不变名义 1000 美元为教学输入，不是编造工资/家庭收入数据。',WB_LOAD+'''
cpi=panel.loc["USA","FP.CPI.TOTL"].reindex(range(2010,2025))
reported=panel.loc["USA","FP.CPI.TOTL.ZG"].reindex(cpi.index)
assert cpi.loc[2010]>0
rebased=100*cpi/cpi.loc[2010];nominal=1000.0
fig,ax=plt.subplots(figsize=(8,4));ax.plot(rebased.index,rebased,"o-")
ax.set(xlabel="Indicator year",ylabel="Rebased CPI (2010=100)",title="Price-index level, not a rate");plt.tight_layout();plt.show()'''),
 step('Reconcile calculated and published rates','核对计算及已发布变化率','Use adjacent observed years. Differences can reflect source revision and rounding; expose them rather than force agreement. Differences of rates are percentage points.','使用相邻有效年。来源修订/舍入可能产生差异，应公开而非强制一致；变化率之差为百分点。','''computed=100*cpi.pct_change(fill_method=None)
fig,ax=plt.subplots(figsize=(8,4));ax.plot(computed.index,computed,"o-",label="From frozen CPI")
ax.plot(reported.index,reported,"x--",label="Published inflation")
ax.set(xlabel="Indicator year",ylabel="Annual change (%)",title="Rates and source reconciliation");ax.legend();plt.tight_layout();plt.show()
comparison=pd.DataFrame({"computed_percent":computed,"reported_percent":reported,"difference_percentage_points":computed-reported})
display(comparison.tail(7))'''),
 step('Convert to a CPI-based real amount','换算 CPI 实值金额','Divide nominal USD by rebased CPI/100. The result uses a broad source price basket, not personalized living costs or investment profits.','名义美元除以重定 CPI/100。结果使用广义来源价格篮子，不是个人生活成本或投资盈利。','''real=nominal*100/rebased
fig,ax=plt.subplots(figsize=(8,4));ax.plot(cpi.index,np.full(len(cpi),nominal),label="Hypothetical nominal USD")
ax.plot(real.index,real,"o-",label="CPI-based 2010-price amount")
ax.set(xlabel="Indicator year",ylabel="USD / 2010-price USD",title="Stated hypothetical purchasing-power example");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Check rebasing and export assumptions','检查重定并导出假设','Nominal and real values match at the base year. Preserve original CPI and its derived index; the fixed nominal example does not measure income change.','基年名义/实值一致。保留原 CPI 及派生指数；固定名义例子不测量收入变化。','''assert np.isclose(rebased.loc[2010],100) and np.isclose(real.loc[2010],nominal) and pd.isna(computed.loc[2010])
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"source_CPI":cpi,"rebased_2010_100":rebased,"hypothetical_nominal_USD":nominal,"CPI_based_2010_price_USD":real}).to_csv(OUTPUT_DIR/"price-and-real-amount.csv")
comparison.to_csv(OUTPUT_DIR/"inflation-reconciliation.csv")
print("Rebasing checked; maximum discrepancy (percentage points):",float(comparison.difference_percentage_points.abs().max()))''')]

SECTIONS[COURSES[2]['id']]=[
 step('Preserve the observation year','保留观测年份','SI.POV.GINI is an index on 0–100. Indicator-reference years, income/consumption concepts and population coverage differ. Missing observations must remain missing.','SI.POV.GINI 为 0–100 指数。指标参考年、收入/消费概念及覆盖人群可能不同，缺失观测保持缺失。',WB_LOAD+'''
gini=panel["SI.POV.GINI"].unstack("iso3").reindex(index=range(2010,2025),columns=countries)
observed=gini.stack().dropna().rename("Gini_index").reset_index()
assert observed.Gini_index.between(0,100).all();display(observed.head(8))'''),
 step('Display actual reported values','展示实际报告值','Markers represent observations. An absent year is not zero or unchanged inequality. We avoid interpolation-like connecting lines.','标记代表观测。缺失年不是零或不变不平等，避免暗示插值的连线。','''fig,ax=plt.subplots(figsize=(9,5))
for code in countries:ax.plot(gini.index,gini[code],"o",label=economies.loc[code,"name"])
ax.set(xlabel="Indicator-reference year",ylabel="Gini index (0–100)",title="Reported values without imputation");ax.legend(fontsize=8);plt.tight_layout();plt.show()'''),
 step('Date the last available values','为最近可得值标日期','A fixed economy order with explicit years shows availability. Different vintages are not a synchronized global ranking. Economies lacking observations stay empty.','固定经济体顺序与年份展示可得性。不同年份不是同步全球排名，无观测者保持空。','''latest=observed.sort_values("year").groupby("iso3").tail(1).set_index("iso3").reindex(countries)
display(latest)
labels=[economies.loc[c,"name"]+" ("+(str(int(latest.loc[c,"year"])) if pd.notna(latest.loc[c,"year"]) else "no observation")+")" for c in countries]
fig,ax=plt.subplots(figsize=(9,4));ax.barh(labels,latest.Gini_index)
ax.set(xlabel="Reported Gini index (0–100)",title="Last available 2010–2024 values; dates differ");plt.tight_layout();plt.show()''',cover=True),
 step('Audit the availability matrix','审计可得性矩阵','Binary color says whether a source observation exists, not what the absent value would be. Common-year and latest-value selections answer different questions.','二值颜色表示是否有来源观测，不猜缺失值。同年和最近值选择回答不同问题。','''fig,ax=plt.subplots(figsize=(9,4));im=ax.imshow(gini.notna().T,aspect="auto",cmap="Blues",vmin=0,vmax=1)
ax.set_xticks(range(15),range(2010,2025),rotation=45);ax.set_yticks(range(6),[economies.loc[c,"name"] for c in countries])
ax.set(xlabel="Indicator year",title="Coverage: 1=reported, 0=missing");fig.colorbar(im,ax=ax,ticks=[0,1]);plt.tight_layout();plt.show()'''),
 step('Reconcile dates and export complete coverage','核对日期并导出完整覆盖','Count observed cells directly and check the chosen years against source availability. Empty selections are explicit; no years are artificially synchronized.','直接计数有效格，并按来源可得性核对选择年。明确空选择，不人为同步年份。','''assert len(observed)==int(gini.notna().to_numpy().sum())
for code in countries:
 available=gini[code].dropna()
 if not available.empty:assert latest.loc[code,"year"]==available.index.max()
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);gini.to_csv(OUTPUT_DIR/"Gini-with-missing-years.csv")
latest.to_csv(OUTPUT_DIR/"dated-last-observations.csv")
print("Source count/year selection reconciled:",len(observed),"observations")''')]

SECTIONS[COURSES[3]['id']]=[
 step('State quotation direction first','先声明报价方向','A quote gives foreign units per EUR. The euro value of one foreign unit is its inverse. Rebase those calculated prices to 100 for display.','报价为外国单位/欧元，一外国单位的欧元价值为其倒数。显示时将计算价格重定为 100。',FX_LOAD+'''
indices=100*prices/prices.iloc[0]
fig,ax=plt.subplots(figsize=(9,5))
for code in currencies:ax.plot(iso_datetimes(indices.index),indices[code],label=code)
ax.legend()
ax.set(xlabel="ECB reference date",ylabel="EUR-valued foreign-unit index (first date=100)",title="Explicit inverted quotation direction");plt.tight_layout();plt.show()''',cover=True),
 step('Inspect reference-date return distributions','检查参考日收益分布','Simple changes are percent on common observed dates. Do not add zero returns for absent calendar days. These are price changes, excluding interest/carry, fees and executable quotes.','在共同观测日期用百分比表示简单变化，不将缺失日插成零收益。这是价格变化，不含利息/套息、费用及可成交报价。','''fig,ax=plt.subplots(figsize=(8,5))
for code in currencies:ax.hist(100*returns[code],bins=60,alpha=.35,label=code)
ax.set(xlabel="Reference-date price return (%)",ylabel="Intervals",title="Frozen historical return distributions");ax.legend();plt.tight_layout();plt.show()'''),
 step('Read historical log-return associations','解读历史对数收益关联','Correlation describes this frozen period on common dates. It is dimensionless and does not establish a stable future hedge.','相关描述共同日期的冻结时段，无量纲，不确定稳定的未来对冲关系。','''log_returns=np.log(prices/prices.shift(1)).iloc[1:];correlation=log_returns.corr()
fig,ax=plt.subplots(figsize=(6,5));im=ax.imshow(correlation,cmap="coolwarm",vmin=-1,vmax=1)
ax.set_xticks(range(4),currencies);ax.set_yticks(range(4),currencies)
for i in range(4):
 for j in range(4):ax.text(j,i,f"{correlation.iloc[i,j]:.2f}",ha="center",va="center")
fig.colorbar(im,ax=ax,label="Historical log-return correlation");plt.tight_layout();plt.show()'''),
 step('Reconcile inversion and export denominations','核对倒数并导出计价','Inverted-price log changes are the negative original-quote log changes. Preserve both raw quotes and derived prices so this unit convention is reproducible.','倒数价格对数变化为原报价对数变化的反号。保留原报价与派生价格，使单位约定可复现。','''assert np.allclose(log_returns,-np.log(rates/rates.shift(1)).iloc[1:])
assert np.allclose(returns,np.expm1(log_returns)) and np.allclose(correlation,correlation.T)
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);rates.to_csv(OUTPUT_DIR/"foreign-units-per-EUR.csv")
prices.to_csv(OUTPUT_DIR/"EUR-per-foreign-unit.csv");returns.to_csv(OUTPUT_DIR/"EUR-price-returns.csv")
print("Quotation identity and common dates verified; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[4]['id']]=[
 step('Reserve held-out years and estimate weights','保留测试年并估计权重','Estimate covariance from 2019–2022, reserving 2023–2024. Weights are long-only and sum to one. Annualization uses a declared 252-observation convention.','2019–2022 估计协方差，2023–2024 测试。权重仅多头且和为一，年化采用声明的 252 观测约定。',FX_LOAD+'''
training=np.array([value.year<=2022 for value in iso_datetimes(returns.index)]);test=~training
assert returns.index[training].max()<returns.index[test].min()
covariance=returns.loc[training].cov().to_numpy();weights=minimum_variance_weights(covariance)
equal=np.full(4,.25);annualization=252
display(pd.DataFrame({"currency":currencies,"minimum_variance_weight":weights,"equal_weight":equal}))
fig,ax=plt.subplots(figsize=(7,4));positions=np.arange(4)
ax.bar(positions-.18,100*weights,width=.36,label="Training minimum variance");ax.bar(positions+.18,100*equal,width=.36,label="Equal")
ax.set_xticks(positions,currencies);ax.set(ylabel="Hypothetical weight (%)",title="Training-only constrained weights");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('Compare historical train/test volatility','比较历史训练/测试波动','Fixed training weights apply in both periods. Daily sample SD times sqrt(252) is a convention, not an exact calendar-year count. A training optimum need not remain best out of sample.','两时段固定训练权重，日样本标准差乘 sqrt(252) 为约定，不是确切自然年数量。训练最优不一定在测试最佳。','''series=pd.DataFrame({"minimum_variance":returns.to_numpy()@weights,"equal_weight":returns.to_numpy()@equal},index=returns.index)
volatility=pd.DataFrame({"training":[100*series.loc[training,c].std(ddof=1)*np.sqrt(annualization) for c in series],"held_out":[100*series.loc[test,c].std(ddof=1)*np.sqrt(annualization) for c in series]},index=series.columns)
fig,ax=plt.subplots(figsize=(8,4));volatility.plot.bar(ax=ax)
ax.set(ylabel="Annualized historical volatility (%)",xlabel="Fixed-weight strategy",title="Train/test historical comparison");plt.xticks(rotation=0);plt.tight_layout();plt.show()'''),
 step('Read hypothetical price-only growth','解读假设价格增长','Cumprod(1+r) gives a frictionless daily-rebalanced index from 100. It omits interest/carry, taxes and execution costs; this is not realized investor profit.','cumprod(1+r) 构造从 100 开始的无摩擦日再平衡指数，不含利息/套息、税与成交成本，不是真实投资盈利。','''growth=100*(1+series.loc[test]).cumprod()
fig,ax=plt.subplots(figsize=(9,4))
for code in growth:ax.plot(iso_datetimes(growth.index),growth[code],label=code)
ax.legend()
ax.set(xlabel="Held-out reference date",ylabel="Hypothetical price-only index (start=100)",title="Fixed training weights in held-out years");plt.tight_layout();plt.show()'''),
 step('Check constraints and the feasible baseline','检查约束及可行基线','Weight bounds/sum and covariance symmetry must pass. The optimized training variance cannot exceed the equal-weight feasible objective beyond tolerance. This is not future suitability evidence.','权重范围/和及协方差对称须通过，训练优化方差不应超过等权可行目标的容差，不据此证明未来适用。','''assert np.isclose(weights.sum(),1) and np.all(weights>=-1e-8) and np.all(weights<=1+1e-8)
assert np.allclose(covariance,covariance.T)
assert weights@covariance@weights<=equal@covariance@equal+1e-10
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
pd.DataFrame({"currency":currencies,"weight":weights}).to_csv(OUTPUT_DIR/"training-only-weights.csv",index=False)
series.to_csv(OUTPUT_DIR/"hypothetical-price-returns.csv");volatility.to_csv(OUTPUT_DIR/"historical-volatility.csv")
(OUTPUT_DIR/"assumptions.json").write_text(json.dumps({"training_years":[2019,2022],"held_out_years":[2023,2024],"denomination":"EUR","interest_and_carry_included":False,"costs_and_tax_included":False,"rebalancing":"daily fixed weights","annualization_observations":252},indent=2))
print("Constraint and training-objective checks passed; exports:",OUTPUT_DIR)''')]

SECTIONS[COURSES[5]['id']]=[
 step('Declare a hypothetical loss sequence','声明假设损失序列','Loss is minus the equal-weight simple return of inverted currency prices. Negative loss represents a gain. The price-only basket does not include actual trades, interest/carry, fees or tax.','损失是倒数货币价格等权简单收益的相反数，负损失代表收益；价格篮子不含实际交易、利息/套息、费用或税。',FX_LOAD+'''
losses=-(returns.to_numpy()@np.full(4,.25));risk=empirical_tail_risk(losses,.95)
fig,ax=plt.subplots(figsize=(8,5));ax.hist(100*losses,bins=60,edgecolor="white")
ax.axvline(100*risk["VaR"],color="red",label="Empirical 95% VaR");ax.axvline(100*risk["expected_shortfall"],color="orange",label="Fractional-tail ES")
ax.set(xlabel="Hypothetical price-return loss (%)",ylabel="Intervals",title="Frozen-period empirical tail");ax.legend();plt.tight_layout();plt.show()''',cover=True),
 step('State the finite-sample conventions','声明有限样本约定','VaR uses the inverse empirical-CDF order statistic. ES averages the worst (1−alpha)n sample mass, including a fractional next observation. A mean above an interpolated quantile can implement a different convention.','VaR 使用经验逆 CDF 次序统计量；ES 平均最差 (1−alpha)n 样本质量，包含必要的下一观测分数质量。插值分位数以上均值可能采用不同约定。','''confidence=[.90,.95,.99]
risk_table=pd.DataFrame([{"confidence":level,**empirical_tail_risk(losses,level)} for level in confidence]);display(risk_table)
fig,ax=plt.subplots(figsize=(8,4));positions=np.arange(3)
ax.bar(positions-.18,100*risk_table.VaR,width=.36,label="VaR");ax.bar(positions+.18,100*risk_table.expected_shortfall,width=.36,label="Fractional-tail ES")
ax.set_xticks(positions,[f"{q:.0%}" for q in confidence]);ax.set(xlabel="Confidence level",ylabel="Historical loss (%)",title="Declared empirical tail conventions");ax.legend();plt.tight_layout();plt.show()'''),
 step('Inspect conditional circular-block variation','检查条件循环分块变异','Five-observation circular blocks retain within-block order but assume stationary resampling. Wrapping the boundary is artificial, not a true adjacent date. The interval describes conditional historical variability, not a tomorrow-loss guarantee.','五观测循环块保留块内次序，假定平稳重采样；首尾连接为人工构造，不是真实相邻日期。区间描述条件历史变异，不保证明日损失。','''draws=[]
for seed in range(1000):
 sampled=circular_block_resample(losses,block_length=5,seed=seed);value=empirical_tail_risk(sampled,.95)
 draws.append([value["VaR"],value["expected_shortfall"]])
draws=np.asarray(draws);interval=np.quantile(draws[:,1],[.025,.975])
fig,ax=plt.subplots(figsize=(8,4));ax.hist(100*draws[:,1],bins=40,edgecolor="white")
ax.axvspan(*(100*interval),color="orange",alpha=.2,label="Conditional percentile range");ax.axvline(100*risk["expected_shortfall"],color="black",linestyle="--",label="Original ES")
ax.set(xlabel="Resampled historical ES (%)",ylabel="Block resamples",title="Conditional variability, not a future bound");ax.legend();plt.tight_layout();plt.show()'''),
 step('Check a hand-calculated fractional tail','检查手算分数尾部','For [0,1,2,3], alpha=.625 gives tail mass 1.5 and ES=(3+0.5·2)/1.5. Verify this convention, ES≥VaR and rejected confidence endpoints, then export full assumptions.','[0,1,2,3]、alpha=.625 的尾质量为 1.5，ES=(3+0.5·2)/1.5。核对约定、ES≥VaR 及非法端点，再导出完整假设。','''fixture=empirical_tail_risk(np.array([0,1,2,3]),.625)
assert np.isclose(fixture["expected_shortfall"],(3+.5*2)/1.5)
assert np.all(risk_table.expected_shortfall>=risk_table.VaR-1e-15)
try:empirical_tail_risk(losses,1)
except ValueError:print("Empty-tail confidence endpoint rejected")
else:raise AssertionError("Invalid confidence accepted")
OUTPUT_DIR.mkdir(parents=True,exist_ok=True);risk_table.to_csv(OUTPUT_DIR/"empirical-tail-risk.csv",index=False)
pd.DataFrame(draws,columns=["VaR","fractional_ES"]).to_csv(OUTPUT_DIR/"conditional-block-risk.csv",index=False)
pd.DataFrame({"date":returns.index,"hypothetical_loss":losses}).to_csv(OUTPUT_DIR/"hypothetical-loss-sequence.csv",index=False)
print("Hand-calculated tail check passed; conditional ES range:",interval)''')]

EXERCISES={}
notes=[
 (['Distinguish constant-price level and indexed growth.','Why use a common dated cross-section?','Rebasing removes original level differences. Common dates avoid mixed vintages; economy averages do not determine individual income distributions.','Using NumPy/Pandas/Matplotlib, add annual changes with missing years preserved.','With the same packages, change to another observed positive common base year while retaining original levels.','Base indices equal 100, units remain constant 2015 USD and aggregates are excluded.'],['区分不变价水平与指数增长。','为何使用同年截面？','重定消除原水平差。同年避免混合年份；经济体均值不确定个人分布。','仅用 NumPy、Pandas、Matplotlib 加年度变化并保留缺失。','同包更改有效共同基年，保留原水平。','基期为 100，单位保持 2015 不变价美元，排除汇总。']),
 (['Distinguish an index and an inflation rate.','Why is the money amount hypothetical?','A rate compares adjacent levels; the money amount is a stated input, not observed income.','Using NumPy/Pandas/Matplotlib, rebase to 2020 and relabel the real-value unit.','With the same packages, compare one additional declared economy with its own observed CPI.','No missing values are filled, differences use percentage points and base real/nominal values match.'],['区分指数与通胀率。','金额为何是假设？','率比较相邻水平；金额为声明输入，不是收入观测。','仅用 NumPy、Pandas、Matplotlib 重定至 2020 并重标实值单位。','同包增加另一声明经济体的观测 CPI。','不填缺失，率差用百分点，基年金额一致。']),
 (['Why show each last-value year?','Can one Gini reconstruct a full distribution?','Years and concepts differ. One Gini does not uniquely identify a Lorenz curve or income/consumption distribution.','Using NumPy/Pandas/Matplotlib, restrict to a common observed year and report exclusions.','With the same packages, count available/missing years without imputation.','Retain original reference years and 0–100 index units; explicitly report empty selections.'],['为何显示各最近值年份？','单个 Gini 能否重建完整分布？','年份/概念不同；单个 Gini 不能唯一确定 Lorenz 曲线或分布。','仅用 NumPy、Pandas、Matplotlib 限定共同有效年并报告排除。','同包统计有效/缺失年，不填补。','保留原参考年和 0–100 单位，明确空选择。']),
 (['Why invert the quote?','What do missing calendar days mean?','The inverse is EUR per foreign unit. Common observed intervals, not inserted calendar-day zeros, define returns.','Using NumPy/Pandas/Matplotlib, compare original and inverted log changes and annotate opposite signs.','With the same packages, export a dated price-only cumulative index without interest claims.','Inversion identities pass; original quotes, denominations and free ECB source attribution remain explicit.'],['为何取报价倒数？','缺失自然日意味着什么？','倒数为欧元/外国单位；共同观测区间定义收益，不插自然日零值。','仅用 NumPy、Pandas、Matplotlib 比较原/倒数对数变化并标反号。','同包导出有日期的价格累计指数，不声称含利息。','恒等式通过，原报价、计价及免费 ECB 署名明确。']),
 (['Why can a training optimum fail later?','Which costs/returns are excluded?','Covariance can change. The hypothetical price-only model omits interest/carry, tax and execution costs.','Using NumPy/SciPy/Pandas/Matplotlib, compare training windows with fixed weights on the same holdout.','With the same packages, add a stated maximum currency weight and verify feasibility.','Weights sum to one and respect bounds; covariance is training-only, with no future suitability claim.'],['训练最优为何可能随后失效？','排除哪些成本/收益？','协方差会变化；假设价格模型省略利息/套息、税及成交成本。','仅用 NumPy、SciPy、Pandas、Matplotlib 比较训练窗口，在同测试期固定权重。','同包增加声明的权重上限并核对可行。','权重和为一且有界，只用训练协方差，不宣称未来适用。']),
 (['Why state quantile and tail-mass conventions?','Which assumptions support circular blocks?','Empirical interpolation and inverse-CDF tail integration differ. Circular blocks assume stationarity and make an artificial boundary; intervals are conditional.','Using NumPy/Pandas/Matplotlib, compare block lengths 1, 5, 10 with recorded seeds.','With the same packages, export 90%, 95%, 99% risk with the exact empirical convention.','Hand examples pass, ES≥VaR, endpoint confidence fails and no future-loss guarantee is claimed.'],['为何声明分位和尾质量约定？','循环块依赖哪些假设？','经验插值和逆 CDF 尾积分不同。循环块假定平稳且人工连接首尾，区间为条件性。','仅用 NumPy、Pandas、Matplotlib 比较块长一、五、十并记录种子。','同包按确切经验约定导出 90%、95%、99% 风险。','手算通过、ES≥VaR、拒绝置信端点，不保证未来损失。'])]
for c,(en,zh) in zip(COURSES,notes):EXERCISES[c['id']]=exercises(en,zh)
