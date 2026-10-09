# Cookbook 验证记录

日期：2026-10-09。当前扩展包含 **8 学科 × 每科 6 课 × 2 种语言，共 48 个工作流、96 份 notebook**。七个新学科新增 42 课、84 份 notebook。生物信息学首版已由 PR #27 发布；本次扩展的发布状态以独立 PR 和 GitHub Pages 公共复检为准。

## 交付与离线执行

- 96 份标准 `.ipynb`、116 个静态页面、8 个学科 ZIP 及一个 96 份合集。
- 全部 notebook 清空状态后按顺序执行，作者验证禁用 Python socket 连接；共保存 **292 张实际生成的 PNG 图表**。3D HTML 输出另行保存，不冒充静态图。
- nbformat、允许包导入、每个数据快照的 SHA-256、双语计算代码相同及已执行输出检查通过。
- `validate_release.py` 固定核对 8×6×2 的用户范围，核对生成源与交付计算代码、快照及来源 metadata 一致，防止只验证已登记子集。
- 所有 96 份在独立临时文件夹中重命名、移动、JSON 保存后重新读取，使用本 notebook 的真实加载函数读取全部内嵌数据，无旁侧文件。
- 第一单元统一为 Gallery 风格 `raw` / `text/html` 介绍卡片；实际图表来自执行，不是示意输出。

证据：`qa/notebook-execution.json`、`qa/artifact-validation.json`、`qa/release-validation.json`。

## 科学方法与真实来源

`test_methods.py` 的 6 组和 `test_science_methods.py` 的 12 组独立数值/异常检查通过。包括 RefSeq 翻译、仿射比对穷举及回溯、归一化、ORA/BH、PDB 替代构象；以及 PCA 协方差参考、kNN 距离、k-means 已知最小值、岭回归正规方程、数值积分/求根、重采样与排列、物理解析极限、化学平衡、有限元/RC/PID 参考、精确尾部风险及显式 TF-IDF 矩阵。

新增日期实现使用标准库，核对闰年日期、星期及精确十分钟间隔。原生 Pandas 日期 dtype 的崩溃记录及规避见 `qa/native-compatibility-issues.json`。更换解析方式后 8 个受影响课程的 16 份版本重新执行；共享单车测试 MAE 1245.3946847、RMSE 1479.9941754、R² 0.3134869094 与此前相同，顺序回测仍为 366 个预测。

44 份原始/参考/模型文件均归档并与来源清单核对 SHA-256。UCI 数据保留原观测与来源单位说明；未使用发现额外使用限制的 Air Quality 数据。ECB 采用官方 SDMX 响应，拒绝过时/异常的旧 CSV。World Bank 保留缺失值、定义与观测年份。全文语料内嵌完整来源和许可，章节筛选是可见计算。PubChem 计算属性、参考公式、建模参数及模拟校准明确标记，未当作实测数据。

证据：`data/sources.json`、`data/raw-manifest.json`、`qa/source-quality.json`、`EXPANSION_PLAN.md` 及两份方法检查脚本。

## 实际应用运行与覆盖边界

应用 **VibeIt 1.0.2 (8)**，iPadOS 27.0 Simulator；实际环境 Python **3.13.14**、NumPy **2.5.0**、Pandas **3.0.3**。

- 已发布的生物信息学 12 份有逐份编辑器 Run All 的历史记录，152 个代码单元。历史 iPhone 结构、长表、导出/重新导入证据保留。
- 新增 **84 份**在实际应用内核中通过作者 QA notebook 批量执行。每份隔离工作目录与变量空间，执行交付文件的原样代码，禁用 Python 网络，记录真实图表/表格及增量报告；**782 个代码单元、252 张 PNG 全部通过**。报告的每份源 SHA-256 与交付文件一致。
- 该批量记录证明真实应用内核兼容性，不等同于逐份人工完成所有编辑器导入、滚动、保存和导出流程。
- 中文共享单车回归另外从清空输出的副本在编辑器点击 Run All，12 个代码单元、3 张 PNG、实际 Python 3.13.14 输出及保存文件核对通过，原样代码/快照与浏览器下载一致。中文介绍卡片实际显示正常。
- 新建独立 Cookbook Expansion QA iPad，使用应用现有 debug open-file 启动参数检查英文咖啡因介绍卡片。标题、数据类型、包标签及换行实际显示；该展示检查不作为重新执行证据。
- 通过实际外部文件 URL 打开浏览器下载的完整咖啡因 notebook，应用执行导入并以新名称保存。源码、解释、全部快照、3 张已保存 PNG 和 HTML 单元类型保留；保存文件哈希另记。此项是实际文件导入，未冒充手动文件选择器流程或此次导入后的重新执行。见 `qa/expansion-app-import.json`。
- 尚未逐一人工验收新增 84 份的完整导入/导出 UI，也未完成全部新增工作流的 iPhone 原生交互复检。共享模拟器窗口正被其他操作使用时，未继续操作其认证或编辑流程。
- 未使用真实 iPad/iPhone，不将模拟器证据描述为实机验收。应用源码、Gallery 示例库和 App Store 发行版未随网站扩展修改。

证据：`qa/expansion-native-kernel.json`、`qa/expansion-editor-ui.json`、`qa/native-compatibility-issues.json`，以及历史 `qa/ipad-execution.json`、`qa/iphone-execution.json`、`qa/app-export.json`。

## 网页、下载与交互

- 96 个双语阅读页在 1440px 桌面检查实际代码高亮、HTML 卡片、至少 3 张图、5 张提示 callout、下载链接、课程 schema 和无页面水平溢出。
- 48 个中文阅读页在 390px 手机尺寸检查无页面水平溢出；来源页的中英文版本也为 390px。
- 8 学科的双语目录各有 6 张完整课程卡片；搜索、空结果、主题筛选及重置通过。1440/900/390px 对应 3/2/1 列。
- 实际点击验证同学科语言切换和键盘 Escape 关闭菜单。产品配色、导航和 Lessons 入口保持共享，Python 高亮无 CDN 依赖。
- 咖啡因与血红蛋白网页 3D 阅读版阻断外部 HTTPS 后分别显示 **24 / 4993 个原子**。移动容器与 canvas 同为 358px，摄像机随列宽重新拟合并留边距，避免固定 640px 画面裁切。
- 浏览器从真实页面下载按钮下载全部 **96 份单课与 9 个 ZIP，共 105 个文件**，全部与交付文件逐字节及 SHA-256 一致。
- 116 页 canonical、双语 hreflang、sitemap 和 3146 个本地链接/资源目标检查通过；各学科及总 ZIP 的成员与单课字节一致。

证据：`qa/expansion-browser-validation.json`、`qa/expansion-browser-downloads.json`、`qa/artifact-validation.json` 和 `qa/evidence/`。

## 发布状态

本地地址为 `http://127.0.0.1:8764/vibeit/cookbook/`，中文在 `zh-hans/`。本次扩展提交独立网站 PR 供审阅；公开上线须由合并、GitHub Pages 部署和公共文件哈希共同确认。当前验证报告明确区分交付完成、内核执行、编辑器覆盖和实机/发布证据。
