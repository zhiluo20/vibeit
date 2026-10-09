# Cookbook 验证记录

日期：2026-10-09。交付状态：本地完整实现及验证完成，待发布 PR；官网尚未部署。

## 可运行成果

- 6 个真实生物信息学工作流、12 份中英文 `.ipynb`、32 个静态页面及一个课程合集 ZIP。
- 所有 notebook 按顺序执行通过，Python socket 连接在作者端验证过程中被禁用；每课保存 3–5 幅实际计算图表。
- 12 份 notebook 通过 nbformat 校验、内嵌数据 SHA-256 校验、支持包导入检查及中英文计算代码一致性检查。
- 重命名、移动及 JSON 保存/重新读取后，12 份 notebook 均能独立定位和读取自己的 metadata 数据，不需要旁侧数据文件。

详见 `qa/notebook-execution.json`、`qa/artifact-validation.json`、`qa/portability.json`。

## 实际 VibeIt 验证

- 应用版本 **1.0.2 (8)**，iPad Simulator / iPadOS 27.0。
- 嵌入环境实际输出 **Python 3.13.14、NumPy 2.5.0、Pandas 3.0.3**。
- 在应用中逐课执行全部 12 份 notebook，共 152 个代码单元，无 Python 错误；更新后的表达、富集和结构版本已再次执行核对。
- iPhone Simulator / iOS 27.0 验证了中文长教程、表达工作流、真实样本表以及英文结构工作流；1A3N 模型可显示并用拖动旋转。
- 手机宽表预览使用内嵌 HTML/CSS 保留完整标识符及数值，避免拆成多行；相同表格在 390px 浏览器中验证横向滚动，页面宽度保持 390px。
- 通过应用导出 `.ipynb` 后，两份内嵌结构/序列快照和全部代码执行结果均保留；通过 **+ → Import from Files** 实际重新导入，复制文件与导出文件字节一致。

详见 `qa/ipad-execution.json`、`qa/iphone-execution.json`、`qa/iphone-ui.json`、`qa/app-export.json`。未使用实机，因此不将模拟器观察称为实机验收。

## 数值与来源

独立检查覆盖全局/局部仿射比对的短序列穷举最优分数、回溯重新评分、RefSeq 翻译、median-ratio size factors、超几何尾概率、BH 校正、网络孤立节点及阈值单调性，以及 PDB 多模型/替代构象/插入码。异常输入与空结果按课程的方法边界处理。

原始快照的可核对结果为 **63,677 × 8** counts、4 个供体；默认过滤保留 **16,139** 个基因。效应筛选得到 527 个上调候选与 529 个下调候选；Reactome 实测注释背景为 7,980 个基因，检验族包含 2,086 项，其中 5 项 q <0.05。这里的候选未经过正式差异表达统计检验，富集不直接表示通路激活。

7 份原始数据库响应已压缩归档并与来源清单中的完整 SHA-256 一致。学生快照的转换和筛选规则在生成脚本与 notebook 中公开。

详见 `test_methods.py`、`data/sources.json`、`data/raw-manifest.json`、`qa/reference-results.json`。

## 网页与下载

- 英文与中文页面、8 个学科卡片、占位页、搜索、空结果状态、主题筛选、语言切换和官网/帮助中心入口均验证通过。
- 浏览器实际下载全部 12 个文件，逐个与交付文件核对字节和 SHA-256；合集 ZIP 的文件也与单份下载一致。
- 桌面 1440×1000 与手机 390×844 验证，手机首页和阅读页均没有页面水平溢出。
- Cookbook 背景、表面、文字、弱化文字及蓝青 accent 的浏览器计算值与产品页完全一致；品牌色从产品 CSS 自动生成。
- Python 代码使用 Pygments 静态高亮，具备实际 token span 和独立色彩；高亮与结构阅读版均不依赖外部 CDN。
- 结构页面在阻断所有外部 HTTPS 的测试中显示 4,993 个原子、一个 WebGL canvas，未产生页面异常或外部请求。
- 所有 32 个页面的 canonical、双语 hreflang、sitemap 和 698 个本地链接/资源目标检查通过。

详见 `qa/browser-validation.json`、`qa/browser-downloads.json` 及 `qa/evidence/`。

## 发布边界

本地预览和模拟器验证不等于公开站点部署或 App Store 发布。合并及部署之后，应对公共地址重新执行下载哈希与应用导入检查。现有应用示例库与发行版本没有随本次网站改动修改。
