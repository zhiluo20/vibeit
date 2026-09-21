const pair=(en,zh)=>({en,'zh-hans':zh});
const step=(shot,target,title,body,zhTitle,zhBody,extra={})=>({shot,target,title:pair(title,zhTitle),body:pair(body,zhBody),...extra});
const topic=(id,group,order,title,zhTitle,goal,zhGoal,entry,requirements,steps,related,extra={})=>({id,group,order,title:pair(title,zhTitle),goal:pair(goal,zhGoal),entry,requirements,steps,related,...extra});
export const topics=[
 topic('getting-started/workspace','getting-started',1,'Find your way around Vibeit','认识 Vibeit 工作区','Recognize the file browser, editor, output area, settings and AI entry points.','认识文件浏览器、编辑区、结果区、设置和 AI 助手入口。','Vibeit → Local Workspace',['subscription'],[
 step('S01','primary','Open the workspace menu','Tap the ellipsis button in the file browser. It contains Settings, Example Gallery, Coding Agent and other workspace tools.','打开工作区菜单','点击文件浏览器中的省略号按钮。设置、示例库、编码助手等入口都在这个菜单里。'),
 step('S02','primary','Locate the create and import menu','Tap + to create a notebook or script, import files, or open a folder as a project.','找到新建与导入菜单','点击 +，可以新建笔记本或脚本、导入文件，或把文件夹作为项目打开。'),
 step('S01','file','Choose a file','Select a notebook or Python script to open its editor. On iPhone, return to the file browser before selecting another file.','选择文件','点选笔记本或 Python 脚本即可打开编辑器。iPhone 上可先返回文件列表，再选择其他文件。'),
 step('S13','primary','Find settings by task','Open Settings and choose the relevant section: AI for providers, Environment for HF_TOKEN, Source Control for GitHub, or Remote for hosts.','按任务寻找设置','打开设置后，AI 服务在“AI”，HF_TOKEN 在“环境”，GitHub 在“源代码管理”，服务器在“远程”。')
 ],['getting-started/first-run','ai/choose-provider']),
 topic('getting-started/first-run','getting-started',2,'Run your first Python code','第一次运行 Python','Run a notebook cell and a Python script, and recognize their output.','运行一个笔记本单元和一个 Python 脚本，并找到输出结果。','File browser → + → Notebook',['subscription'],[
 step('S02','primary','Create a notebook','Open + and choose Notebook. A notebook opens in the editor.','创建笔记本','打开 + 菜单，选择 Notebook（笔记本），新笔记本会在编辑器中打开。'),
 step('S03','editor','Enter a small program','Tap inside the code cell and enter the example. Keep the quotation marks around the text.','输入一段小程序','点击代码单元，输入示例。文字两侧的引号需要保留。',{action:'input',code:'print("Hello, Vibeit!")\nprint("2 + 3 =", 2 + 3)'}),
 step('S03','primary','Run the cell','Tap the cell’s Run control. With a hardware keyboard, Command–Return runs the current cell.','运行单元','点击单元的运行按钮。使用外接键盘时，可以按 Command–Return 运行当前单元。'),
 step('S04','primary','Check the result','The output should contain Hello, Vibeit! and 2 + 3 = 5. Create a Script from + to run the same code as a .py file.','核对结果','输出应包含 Hello, Vibeit! 和 2 + 3 = 5。也可以从 + 新建 Script，把同样的代码保存为 .py 脚本运行。')
 ],['notebooks/cells','getting-started/files'],{expected:pair('Both lines appear in the result area without a traceback.','结果区出现两行文字，没有错误回溯。')}),
 topic('getting-started/files','getting-started',3,'Import, organize and export files','导入、管理与导出文件','Keep a notebook and its data together, and save copies outside Vibeit.','把笔记本和数据放在同一项目中，并将文件副本保存到 Vibeit 之外。','File browser → +',['subscription'],[
 step('S06','import','Import a file or folder','Choose Import from Files for individual files, or Open Folder as Project for a project directory. Grant access to the selected location.','导入文件或文件夹','单个文件选择“从文件导入”；项目文件夹选择“将文件夹作为项目打开”，并允许访问所选位置。'),
 step('S01','file','Keep relative paths intact','Place quickstart.ipynb beside the data folder. Do not move samples.csv out of data unless you also update the code path.','保留相对路径','把 quickstart.ipynb 与 data 文件夹放在同一级。移动 samples.csv 后，需要同步修改代码中的路径。'),
 step('S06','primary','Open file actions','Long-press a file to see its available actions. Read the confirmation before deleting or moving a file.','打开文件操作菜单','长按文件查看可用操作。删除或移动前，先确认目标文件和位置。',{action:'longPress'}),
 step('S06','export','Export a copy','Use the notebook’s share/export control and choose the required format and destination in the system sheet. Reopen the exported file to check it.','导出副本','使用笔记本的分享或导出入口，在系统面板中选择格式和保存位置，然后重新打开导出的文件进行核对。')
 ],['getting-started/gallery','git/clone']),
 topic('getting-started/gallery','getting-started',4,'Learn with the example gallery','使用内置示例库','Open a guided example as a working notebook and run it in order.','把内置示例打开为可操作的笔记本，并按顺序运行。','File browser → … → Example Gallery',['subscription'],[
 step('S05','primary','Open Example Gallery','Open the workspace menu and select Example Gallery. Choose an example that matches what you want to learn.','打开示例库','在工作区菜单中选择 Example Gallery（示例库），再选择你想学习的项目。'),
 step('S05','example','Check its requirements','Read the example’s network and package notes before opening it. Some examples fetch data or models on their first run.','查看运行条件','打开前阅读网络和依赖说明。有些示例首次运行时需要下载数据或模型。'),
 step('S03','primary','Run cells in order','Start at the first code cell. Later cells may use variables or files created earlier in the notebook.','按顺序运行','从第一个代码单元开始。后面的单元可能依赖前面创建的变量或文件。'),
 step('S04','primary','Try a small change','Change one value, rerun the relevant cells, and compare the output. Keep a copy before making larger changes.','尝试小改动','修改一个数值，重新运行相关单元并比较结果。进行较大修改前先保留副本。')
 ],['notebooks/kernel','models/packages']),
 topic('notebooks/cells','notebooks',1,'Use code, Markdown and HTML cells','使用代码、Markdown 与 HTML 单元','Choose the right cell type and switch between reading and editing rich content.','选择合适的单元类型，在阅读和编辑富文本内容之间切换。','Open a notebook → cell controls',['subscription'],[
 step('S07','primary','Choose the cell type','Use a code cell for Python, Markdown for explanations, and an HTML cell for HTML content.','选择单元类型','Python 放在代码单元中，说明文字使用 Markdown，HTML 内容使用 HTML 单元。'),
 step('S03','editor','Edit Python in a code cell','Tap the source area and enter code. Code cells run through the notebook’s Python kernel.','编辑 Python 代码','点击代码区域输入内容。代码单元由当前笔记本的 Python 内核运行。',{action:'input'}),
 step('S07','edit','Edit rich content','Non-empty Markdown and HTML cells open in rendered form. Tap the cell’s edit control to reveal its source.','编辑富文本内容','非空 Markdown 和 HTML 单元默认显示渲染结果。点击单元的编辑按钮查看源码。'),
 step('S10','primary','Finish editing','Use the finish-editing control to return to the rendered result. Your source remains available whenever you edit again.','完成编辑','点击完成编辑，返回渲染结果。下次进入编辑时仍能查看和修改源码。')
 ],['notebooks/results','notebooks/kernel']),
 topic('notebooks/kernel','notebooks',2,'Run, interrupt and restart the kernel','运行、停止与重启内核','Understand execution order, stop a long task, and start with a fresh Python state.','理解执行顺序、停止耗时任务，并重建干净的 Python 状态。','Open a notebook → execution controls',['subscription'],[
 step('S03','primary','Run the current cell','Run a cell when it is ready. If it depends on variables from earlier cells, run those cells first.','运行当前单元','代码准备好后运行当前单元。若依赖前面的变量，先运行创建这些变量的单元。'),
 step('S09','interrupt','Interrupt a long-running task','Use Stop/Interrupt while a task is running. Wait for the kernel to return to an idle state before starting another run.','中断耗时任务','任务运行时使用停止或中断按钮，等待内核回到空闲状态后再开始下一次运行。'),
 step('S09','primary','Restart when you need a fresh state','Restart the kernel to clear in-memory variables or apply changed environment variables. Saved notebook source is retained.','需要干净状态时重启','重启内核可以清除内存变量，并应用更新后的环境变量。已保存的笔记本源码会保留。'),
 step('S04','primary','Run the notebook again from the top','After a restart, recreate variables by running the notebook in order. A NameError often means an earlier defining cell has not run.','从头重新运行','重启后按顺序运行笔记本以重建变量。NameError 往往表示定义变量的前置单元尚未运行。')
 ],['models/environment','notebooks/results']),
 topic('notebooks/results','notebooks',3,'Read tables, plots and interactive results','查看表格、图表与交互结果','Find output where the code ran and interact with supported notebook results.','在代码运行的位置查看输出，并操作受支持的交互结果。','Notebook → run a result-producing cell',['subscription'],[
 step('S04','primary','Start with a small table or plot','Run the tutorial notebook’s CSV and plot cells. The result appears below the cell that produced it.','先运行简单表格或图表','运行示例笔记本中的 CSV 和绘图单元，结果会出现在产生它的单元下方。'),
 step('S10','primary','Interact with supported output','Use the controls inside interactive output. A molecular view supports drag to rotate and pinch to zoom.','操作交互结果','使用交互结果中的控件。分子视图可以拖动旋转、双指缩放。'),
 step('S10','output','Check where the code is running','Local output is produced by the local kernel; a remote notebook uses the selected server. Package and hardware availability can differ.','确认运行位置','本地结果来自本地内核，远程笔记本使用所选服务器。两者可用的包和硬件能力可能不同。'),
 step('S06','export','Save a result you want to keep','Export the notebook or write an output file from Python, then confirm the file appears in the project.','保存需要保留的结果','导出笔记本，或通过 Python 写入结果文件，然后确认文件已经出现在项目中。')
 ],['getting-started/files','models/packages']),
 topic('ai/choose-provider','ai',1,'Choose an AI provider','选择 AI 服务','Choose between Apple Intelligence and a connected AI service, and activate the provider you configured.','选择 Apple Intelligence 或联网 AI 服务，并启用已经配置好的服务。','Settings → AI → Model Providers',['subscription'],[
 step('S13','primary','Open Model Providers','Open Settings → AI. The provider list shows which services are configured and which provider is active.','打开模型服务列表','进入“设置 → AI”。列表会显示服务是否已配置，以及当前启用的服务。'),
 step('S14','primary','Check Apple Intelligence requirements','Apple Intelligence needs supported hardware and a ready system model. It does not use your Claude or Codex account.','查看 Apple Intelligence 条件','Apple Intelligence 需要兼容硬件和已准备好的系统模型，不使用 Claude 或 Codex 账号。'),
 step('S13','codex','Choose a cloud service if needed','Cloud providers require Pro, an internet connection and the provider’s own account or API access. Available options may depend on your storefront.','按需选择联网服务','云端服务需要 Pro、网络，以及对应服务商的账号或 API 权限。可见选项也可能受商店地区影响。'),
 step('S13','active','Activate the configured provider','Open its detail page, complete configuration and select Use This Provider. Saving settings and making a provider active are separate actions.','启用已配置的服务','打开详情页并完成配置，再选择 Use This Provider。保存设置与将服务设为当前启用是两个不同动作。')
 ],['ai/apple-intelligence','ai/codex','ai/claude']),
 topic('ai/apple-intelligence','ai',2,'Set up Apple Intelligence','配置 Apple Intelligence','Find the on-device provider and understand its availability requirements.','找到设备端 AI 服务，并理解它的可用条件。','Settings → AI → Apple Intelligence',['subscription','appleIntelligence'],[
 step('S14','primary','Check device and system support','Use a supported device with iOS or iPadOS 26 or later. Enable Apple Intelligence in the system Settings app and let its model finish preparing.','确认设备与系统支持','使用兼容设备及 iOS 或 iPadOS 26 及以上版本。在系统设置中启用 Apple Intelligence，并等待系统模型准备完成。'),
 step('S13','apple','Open the Apple Intelligence provider','In Vibeit, open Settings → AI and select Apple Intelligence.','打开 Apple Intelligence 服务','在 Vibeit 中进入“设置 → AI”，点选 Apple Intelligence。'),
 step('S14','status','Read the availability message','If the provider is unavailable, follow the stated reason: unsupported device, disabled Apple Intelligence, or a model that is not ready.','阅读可用性提示','若显示不可用，按具体原因处理：设备不支持、Apple Intelligence 未开启，或系统模型尚未准备好。'),
 step('S14','activate','Choose Use This Provider','Once available, activate the provider and try a short request. Simulator availability is not evidence of whether your physical device supports it.','选择启用此服务','服务可用后将其启用，并尝试一条简短请求。模拟器中的状态不能代表你的实体设备是否支持这项能力。')
 ],['ai/choose-provider','ai/agent'],{hardwareOnly:true}),
 topic('ai/codex','ai',3,'Sign in to Codex and load models','登录 Codex 并加载模型','Connect a Codex account and choose from the models available to that account.','连接 Codex 账号，并从该账号实际可用的模型中进行选择。','Settings → AI → Codex',['pro','network','codex'],[
 step('S15','primary','Start the official sign-in flow','Open the Codex provider and tap Sign in with OpenAI Codex. Complete the sign-in and authorization in the browser that opens.','开始官方登录流程','打开 Codex 服务详情，点击 Sign in with OpenAI Codex，在打开的浏览器中完成登录与授权。'),
 step('S16','status','Return to Vibeit','Return after authorization. Confirm that the provider shows a signed-in account and that model discovery finishes.','返回 Vibeit','授权后返回 App，确认显示已登录账号，并等待可用模型加载完成。'),
 step('S16','primary','Choose Automatic or an available model','Automatic lets Vibeit use the available catalog. An explicit selection keeps your preferred model while it remains available. The list can change over time.','选择 Automatic 或可用模型','Automatic 根据当前可用列表选择模型；也可以明确选择偏好的型号。模型列表会随账号权限和服务更新而变化。'),
 step('S16','refresh','Refresh and activate','Use Refresh Models if the list needs updating. Save the settings, then use Use This Provider when you want Codex to power the agent.','刷新并启用','需要更新列表时使用 Refresh Models。保存设置；希望由 Codex 驱动助手时，选择 Use This Provider。')
 ],['ai/reasoning','ai/agent'],{aliases:['Codex','ChatGPT','OpenAI','Automatic','模型列表']}),
 topic('ai/claude','ai',4,'Configure Claude with an API key','使用 API Key 配置 Claude','Store an Anthropic API key and choose a Claude model.','保存 Anthropic API Key，并选择 Claude 模型。','Settings → AI → Claude',['pro','network','claude'],[
 step('S17','primary','Get the correct kind of key','Use an Anthropic API key from the provider console. A Claude app subscription or Claude Code OAuth token is not the API key this form expects.','准备正确类型的密钥','使用服务商控制台提供的 Anthropic API Key。Claude 应用订阅或 Claude Code OAuth Token 不是此表单所需的 API Key。'),
 step('S17','key','Enter the key in the secure field','Paste the key into Anthropic API Key. Do not paste keys into notebook cells or chat messages.','在安全字段中输入','把密钥粘贴到 Anthropic API Key 字段，不要放进笔记本单元或聊天消息。',{action:'input'}),
 step('S17','models','Refresh the model list','Tap Refresh Claude Models and select a model available to your API account.','刷新模型列表','点击 Refresh Claude Models，选择 API 账号可用的模型。'),
 step('S17','activate','Save and make it active','Save the configuration and choose Use This Provider. If a test reports Invalid key, replace the key and test again.','保存并启用','保存配置并选择 Use This Provider。若测试提示 Invalid key，请更换密钥后重试。')
 ],['ai/choose-provider','ai/custom-provider']),
 topic('ai/custom-provider','ai',5,'Add an OpenAI-compatible provider','添加 OpenAI 兼容服务','Configure an endpoint, model ID and API key for a supported compatible service.','为兼容服务设置接口地址、模型 ID 和 API Key。','Settings → AI → Add a Model Provider',['pro','network'],[
 step('S18','primary','Add a model provider','Choose Add a Model Provider. Select an appropriate template or the custom compatible option.','添加模型服务','选择 Add a Model Provider，使用合适的模板或自定义兼容服务选项。'),
 step('S18','endpoint','Use the endpoint supplied by the provider','Enter the full endpoint expected by that service. A website home page is not necessarily an API endpoint.','填写服务商提供的接口地址','输入服务商要求的完整接口地址。网站首页地址不一定是 API 接口地址。',{action:'input'}),
 step('S18','model','Enter an exact model ID and key','Use the provider’s documented model ID. Enter its API key in the secure field.','填写准确模型 ID 与密钥','使用服务商文档中的模型 ID，并把 API Key 填入安全字段。',{action:'input'}),
 step('S18','save','Save, activate and test','Save and activate the provider, then try a short request. Agent tools also require the endpoint to support the tool-calling protocol.','保存、启用并测试','保存并启用服务，再发一条简短请求。助手工具还要求接口支持相应的工具调用协议。')
 ],['ai/choose-provider','ai/reasoning']),
 topic('ai/reasoning','ai',6,'Choose a model and reasoning effort','选择模型与推理强度','Choose an effort level for the task without confusing it with the app theme.','根据任务选择推理强度，并理解它与界面主题无关。','Agent panel → bottom model and reasoning controls',['subscription'],[
 step('S19','primary','Open the agent for your task','Open a notebook or script and open Coding Agent. Confirm the active provider and the file you want the agent to work with.','打开当前任务的助手','打开笔记本或脚本，再打开 Coding Agent，确认当前服务和要处理的文件。'),
 step('S20','primary','Open the Reasoning menu','Tap the effort control at the bottom of the panel. The menu offers Light, Medium, High and Extra High.','打开推理强度菜单','点击面板底部的强度控件，菜单提供 Light、Medium、High 和 Extra High。'),
 step('S20','medium','Start with Medium','Use Medium for everyday tasks. Light favors a quicker, narrower pass; High and Extra High ask for more investigation and verification.','先从 Medium 开始','日常任务可从 Medium 开始。Light 偏向更快、更聚焦的处理；High 和 Extra High 要求更多检查与验证。'),
 step('S20','high','Adjust to the actual provider','Codex maps the choice to the model’s supported efforts and can fall back to its supported default. Other providers do not necessarily expose the same native parameter.','结合实际服务理解选项','Codex 会按模型支持的强度进行映射，必要时回退到受支持的默认值；其他服务不一定提供同样的原生参数。')
 ],['ai/codex','ai/agent'],{aliases:['Reasoning','思考强度','推理强度','Light','Medium','High','Extra High'],note:pair('In the current Chinese catalog, Light may appear as 浅色 because the label is shared with the theme. Here it means light reasoning, not a color setting.','当前中文词条中 Light 可能显示为“浅色”，因为该词与主题共用了翻译。这里表示轻量推理，不是颜色设置。')}),
 topic('ai/agent','ai',7,'Work with context, tools, memory and skills','使用上下文、工具、记忆与技能','Give the agent useful context and review the actions it proposes.','向助手提供合适的上下文，并检查它提出的操作。','File browser → … → Coding Agent',['subscription'],[
 step('S19','primary','Start with a specific task','Ask a small, concrete question about the open tutorial file, such as explaining its CSV-reading code.','从具体任务开始','围绕打开的示例文件提出一个小而明确的问题，例如解释读取 CSV 的代码。',{action:'input'}),
 step('S21','primary','Control file context','Review Attach Open File to Model in Settings → AI. It controls whether the current file is supplied to the active provider as context.','控制文件上下文','在“设置 → AI”中查看 Attach Open File to Model，决定是否把当前文件作为上下文提供给正在使用的服务。'),
 step('S19','approval','Read proposed actions','Check code changes and any confirmation request before applying or running them. A suggestion is not proof that code has executed successfully.','检查建议的操作','应用或运行前检查代码改动和确认请求。助手给出建议，并不等于代码已经成功运行。'),
 step('S22','primary','Review memory','Open Manage Memory in Settings → AI to review, pin, disable or delete stored memories.','查看记忆','在“设置 → AI”的 Manage Memory 中查看、固定、停用或删除记忆。'),
 step('S23','primary','Enable skills intentionally','Open Manage Skills and enable only the reusable instructions you want offered to the agent.','按需启用技能','打开 Manage Skills，只启用你希望提供给助手的可复用指令。')
 ],['ai/reasoning','support/troubleshooting']),
 topic('models/hugging-face','models',1,'Configure a Hugging Face token','配置 Hugging Face Token','Store a Hugging Face token and apply it to a newly started Python kernel.','保存 Hugging Face Token，并使它在新启动的 Python 内核中生效。','Settings → Environment → Hugging Face Token',['subscription','network','huggingface'],[
 step('S24','primary','Open the Environment page','Open Settings → Environment. The Hugging Face field is here, not in the AI provider list.','打开环境页面','进入“设置 → 环境”。Hugging Face 字段位于这里，不在 AI 服务列表中。'),
 step('S24','primary','Enter your access token','Use a token with access to the resources you need. Restricted models may also require approval of their access conditions on Hugging Face.','输入访问 Token','使用具有所需资源访问权限的 Token。受限模型还可能要求先在 Hugging Face 上获得访问许可。',{action:'input'}),
 step('S09','primary','Restart the Python kernel','The token is applied as HF_TOKEN when the kernel starts. Restart an already-running kernel after adding or changing the token.','重启 Python 内核','Token 会在内核启动时以 HF_TOKEN 的形式应用。添加或修改后，需要重启已经运行的内核。'),
 step('S25','primary','Check without printing the token','Run a presence check. True confirms the variable is present, not that a particular model has granted access. Never print the token itself.','验证时不要输出 Token','运行存在性检查。True 表示变量存在，不代表已经获得某个模型的访问权限。不要输出 Token 本身。',{code:'import os\nprint("HF token configured:", bool(os.environ.get("HF_TOKEN")))'})
 ],['models/downloads','models/environment'],{aliases:['HF','HF_TOKEN','Hugging Face','huggingface','hugginface','抱抱脸'],links:[['Hugging Face access tokens','https://huggingface.co/docs/hub/security-tokens']]}),
 topic('models/downloads','models',2,'Download and manage model files','下载与管理模型文件','Verify a small Hugging Face download before trying a large model.','先验证小型 Hugging Face 文件下载，再尝试大型模型。','Notebook → huggingface_hub',['subscription','network'],[
 step('S24','primary','Check access requirements first','Public files may not require a token. Private or gated resources need the correct account permissions in addition to a stored token.','先确认访问条件','公开文件可能不需要 Token。私有或受限资源除了保存 Token，还需要账号具有相应权限。'),
 step('S26','primary','Download a small configuration file','Start with a configuration file instead of full weights. Run the example in a notebook cell.','先下载小型配置文件','先下载配置文件，不要一开始就下载完整权重。在笔记本单元中运行示例。',{code:'from huggingface_hub import hf_hub_download\npath = hf_hub_download("bert-base-uncased", "config.json")\nprint("Configuration downloaded:", path.endswith("config.json"))'}),
 step('S26','files','Find the cache and downloaded files','Vibeit places its default Hugging Face cache in the Models directory. A custom HF_HOME environment value can change that location.','找到缓存和下载文件','默认 Hugging Face 缓存位于 Models 目录。自定义 HF_HOME 环境变量可以改变这个位置。'),
 step('S27','primary','Check compatibility before loading weights','A successful download does not guarantee the model can run. Check the required package, model format, available memory and device backend.','加载权重前检查兼容性','下载成功不代表模型一定能运行。还需要检查依赖包、模型格式、可用内存和设备后端。')
 ],['models/hugging-face','models/packages']),
 topic('models/environment','models',3,'Set environment variables','设置环境变量','Pass project configuration to a fresh Python kernel and terminal.','把项目配置传入新启动的 Python 内核和终端。','Settings → Environment → Environment Variables',['subscription'],[
 step('S24','newKey','Enter a name and value','For a harmless example, enter VIBEIT_DEMO as the key and tutorial as the value. Names are case-sensitive.','填写名称和值','用一个无敏感信息的例子：名称填 VIBEIT_DEMO，值填 tutorial。变量名称区分大小写。',{action:'input'}),
 step('S24','add','Add the variable','Tap Add Variable and check that the name appears in the list. Names containing TOKEN, KEY, SECRET or PASSWORD use secure storage.','添加变量','点击 Add Variable，确认名称出现在列表中。包含 TOKEN、KEY、SECRET 或 PASSWORD 的名称会使用安全存储。'),
 step('S09','primary','Start a new kernel session','Restart the notebook kernel after changing a variable. An existing Python session keeps its previous environment until restarted.','重建内核会话','修改变量后重启笔记本内核；已启动的 Python 会话不会立即采用新环境。'),
 step('S25','primary','Check the harmless value','Run the example and check for tutorial. Use presence checks instead of printing secret values.','核对演示值','运行示例，预期得到 tutorial。检查秘密变量时只检查是否存在，不输出实际内容。',{code:'import os\nprint(os.environ.get("VIBEIT_DEMO"))'})
 ],['models/hugging-face','terminal/basics'],{expected:pair('The new kernel prints tutorial.','新内核输出 tutorial。')}),
 topic('models/packages','models',4,'Find and install compatible Python packages','查看和安装兼容的 Python 包','Find bundled libraries and install a compatible additional package.','查看内置库，并安装兼容的扩展包。','File browser → … → Packages',['subscription','network'],[
 step('S27','primary','Open the package catalog','Browse installed and available packages, or search by the package name. Bundled native libraries are already part of Vibeit.','打开包目录','浏览已安装和可用的包，或按名称搜索。内置原生库已经随 Vibeit 提供。'),
 step('S27','search','Check the package details','Read the available versions and compatibility result. The iPad runtime cannot install every desktop native extension.','查看包详情','检查可选版本和兼容性结果。iPad 运行时不能安装所有桌面原生扩展。'),
 step('S27','install','Install an eligible version','Choose an installable version, review its dependencies and tap Install. Wait for completion before importing it.','安装兼容版本','选择可安装版本，检查依赖并点击 Install。等待安装完成后再导入。'),
 step('S25','primary','Test the import','Run a small import in the same runtime where you installed the package. Remote packages belong to the selected server interpreter.','测试导入','在安装该包的同一个运行环境中测试导入。远程包属于所选服务器解释器。',{code:'import importlib.util\nprint("pandas available:", importlib.util.find_spec("pandas") is not None)'})
 ],['models/downloads','remote/python']),
 topic('git/github','git',1,'Sign in to GitHub','登录 GitHub','Authorize Vibeit to access the GitHub repositories your account permits.','授权 Vibeit 访问账号有权使用的 GitHub 仓库。','Settings → Source Control → GitHub',['pro','network'],[
 step('S28','primary','Open GitHub sign-in','Open Settings → Source Control and choose Sign in with GitHub.','打开 GitHub 登录','进入“设置 → 源代码管理”，选择 Sign in with GitHub。'),
 step('S29','primary','Open the verification page','Use the verification button to open GitHub’s official device authorization page.','打开验证页面','点击验证按钮，打开 GitHub 官方设备授权页面。'),
 step('S29','code','Authorize this device','Enter the current device code on GitHub and review the requested access. Complete any organization authorization your repository needs.','授权当前设备','在 GitHub 中填写当前设备验证码，检查访问权限；组织仓库可能还需要组织授权。'),
 step('S28','status','Return and check the account','Return to Vibeit and confirm that GitHub shows the intended signed-in account.','返回并核对账号','返回 Vibeit，确认 GitHub 显示的是你打算使用的已登录账号。')
 ],['git/clone','git/commit'],{aliases:['GitHub','login','登录']}),
 topic('git/clone','git',2,'Clone and open a repository','克隆并打开仓库','Create a local working copy of a GitHub repository.','把 GitHub 仓库克隆为本地可编辑的工作副本。','File browser → + → Clone from GitHub',['pro','network'],[
 step('S30','primary','Start a clone','Choose Clone from GitHub from the file browser’s + menu. Sign in first if the repository requires it.','开始克隆','在文件浏览器的 + 菜单中选择 Clone from GitHub。需要认证的仓库应先登录。'),
 step('S30','repository','Choose the repository','Select the repository you intend to edit. For practice, fork the tutorial repository into your own account first.','选择仓库','选择准备编辑的仓库。练习时先把教程仓库 fork 到你自己的账号。'),
 step('S30','clone','Wait for the clone to finish','Keep the connection available until cloning completes. Open the resulting project folder.','等待克隆完成','保持网络连接，等待克隆结束，再打开生成的项目文件夹。'),
 step('S31','primary','Confirm the working copy','Open Source Control from Files. Check the repository’s branch and history before editing a file.','确认工作副本','从 Files 区域打开源代码管理，检查分支和历史，再开始编辑文件。')
 ],['git/commit','git/sync'],{links:[['Tutorial repository','https://github.com/zhiluo20/vibeit-tutorials']]}),
 topic('git/commit','git',3,'Review, stage and commit changes','查看差异、暂存与提交','Save a reviewed change in your repository’s local history.','把检查过的改动保存到仓库的本地历史中。','File browser → Files → Source Control',['pro','git'],[
 step('S31','primary','Review the changed file','Edit and save hello.py, then open Source Control. Tap the changed file to read its diff.','检查改动文件','编辑并保存 hello.py，再打开源代码管理。点击变更文件查看差异。'),
 step('S31','stage','Stage only the intended changes','Swipe a change row to reveal Stage, or use Stage All after reviewing every file. Unstage removes a file from the next commit without deleting the edit.','暂存准备提交的改动','滑动变更行显示 Stage，或检查全部文件后使用 Stage All。Unstage 只取消暂存，不会删除编辑内容。',{action:'swipe'}),
 step('S32','message','Describe the change','Enter a short message such as Explain the greeting example. The commit button needs a message and at least one staged file.','填写提交说明','例如填写 Explain the greeting example。提交按钮需要非空说明和至少一个暂存文件。',{action:'input'}),
 step('S32','commit','Commit and check History','Tap Commit. Confirm the new message appears in History. This records local history; it has not yet sent the commit to GitHub.','提交并检查历史','点击 Commit，确认新说明出现在 History 中。这一步记录本地历史，还没有把提交发送到 GitHub。')
 ],['git/sync','git/pull-requests'],{aliases:['commit','stage','diff','提交','暂存','差异']}),
 topic('git/sync','git',4,'Pull and push repository changes','拉取与推送仓库改动','Bring remote commits into a working copy and send your own commits back.','把远程提交取回工作副本，并把自己的提交发送到远程。','Source Control → Pull / Push',['pro','network','git'],[
 step('S32','primary','Check the repository and account','Confirm the project has an origin remote and that your GitHub account can access it. A new local repository needs a remote configured before it can sync.','检查仓库与账号','确认项目有 origin 远程地址，且 GitHub 账号具有访问权限。新建本地仓库需要先配置远程地址才能同步。'),
 step('S32','pull','Pull before continuing work','Save and review your current changes, then tap Pull. Read any rejection before making further edits.','继续工作前拉取','先保存并检查当前改动，再点击 Pull。若被拒绝，先阅读原因，再继续修改。'),
 step('S32','push','Push completed commits','After committing locally, tap Push. Uploading saved files without a commit is not the same operation.','推送已经完成的提交','本地 Commit 后点击 Push。只保存文件，还没有形成可以推送的提交。'),
 step('S32','status','Verify on GitHub','Open the matching branch on GitHub and check the new commit message and file content. For remote workspaces, Git runs on the server and uses that server’s Git credentials.','在 GitHub 核对','打开 GitHub 对应分支，检查新提交说明和文件内容。远程工作区的 Git 在服务器上运行，使用服务器的 Git 凭据。')
 ],['git/pull-requests','remote/files'],{aliases:['push','pull','推送','拉取']}),
 topic('git/pull-requests','git',5,'Open a pull request and resolve sync problems','创建 PR 并处理同步问题','Propose changes from a pushed branch and identify common synchronization failures.','从已推送的分支发起改动提案，并识别常见同步失败原因。','Source Control → Create Pull Request',['pro','network','git'],[
 step('S32','primary','Prepare a separate branch','Prepare the working branch with a Git tool or a remote terminal, then push it. The current App panel shows the branch but does not offer a branch-creation button.','准备独立分支','使用 Git 工具或远程终端准备工作分支并推送。当前 App 面板显示分支，但没有创建分支按钮。'),
 step('S33','primary','Open Create Pull Request','Use the pull-request control when origin points to GitHub. Confirm that the head branch differs from the branch you want to merge into.','打开创建 PR','origin 指向 GitHub 时使用创建 PR 控件。确认当前分支与希望合入的目标分支不同。'),
 step('S33','title','Describe and submit the proposal','Enter the title, explanation and base branch. Submit after reviewing the proposed destination.','填写并提交提案','填写标题、说明和目标分支；检查目标后提交。',{action:'input'}),
 step('S33','result','Follow the returned GitHub link','Open the resulting PR to review its changes. If sync is rejected or histories have diverged, resolve the repository with a suitable Git tool or server terminal before retrying.','打开返回的 GitHub 链接','进入生成的 PR 检查改动。同步被拒绝或历史分叉时，先用合适的 Git 工具或服务器终端处理，再重试。')
 ],['git/sync','terminal/basics'],{note:pair('There is no dedicated merge-conflict editor in this version. Do not discard files or force-push simply to clear an error.','本版本没有专门的合并冲突编辑器。不要为了清除错误而直接丢弃文件或强制推送。')}),
 topic('remote/ssh','remote',1,'Connect to an SSH server with a password','使用密码连接 SSH 服务器','Save a server profile, verify its host key and open its remote files.','保存服务器配置、核验主机密钥并打开远程文件。','Locations → + → Add Remote Host',['pro','network','ssh'],[
 step('S34','primary','Add a remote host','Choose Add Remote Host from Locations. Keep the server address and SSH username ready.','添加远程主机','从 Locations 添加远程主机，准备好服务器地址和 SSH 用户名。'),
 step('S35','host','Enter the connection details','Choose Direct (TCP), then enter the host, port and username. Use the actual server port; 22 is the usual SSH default.','填写连接信息','选择 Direct（TCP），填写主机地址、端口和用户名。端口以服务器配置为准，SSH 常用默认端口为 22。',{action:'input'}),
 step('S35','password','Select password authentication','Choose Password and enter the SSH password. Save the profile. Saving the form does not prove that the server is reachable.','选择密码认证','选择 Password 并输入 SSH 密码，然后保存配置。保存成功不代表服务器已经连接成功。',{action:'input'}),
 step('S37','primary','Verify the host key','Choose Verify Host Key. Compare the displayed fingerprint with one obtained from the server administrator or another trusted channel before trusting it.','核验主机密钥','选择 Verify Host Key，将显示的指纹与管理员或可信渠道提供的指纹核对，确认后再信任。'),
 step('S38','primary','Open the remote directory','Connect to the saved host and confirm that the remote file list loads. Open a small file to verify read access.','打开远程目录','连接已保存主机，确认远程文件列表加载，并打开一个小文件验证读取权限。')
 ],['remote/keys','remote/files'],{aliases:['SSH','password','host','远程连接','服务器']}),
 topic('remote/keys','remote',2,'Connect with an SSH private key','使用 SSH 私钥连接','Configure a private key that matches a public key authorized on the server.','配置与服务器已授权公钥对应的私钥。','Add or Edit Remote Host → Authentication',['pro','network','ssh'],[
 step('S36','primary','Select SSH Key','Edit or add a host and choose SSH Key. The server must already authorize the matching public key for this user.','选择 SSH Key','添加或编辑主机时选择 SSH Key。服务器需要已为该用户授权对应公钥。'),
 step('S36','key','Enter the local private-key file path','Import the private-key file into the local workspace. Copy the workspace folder path from Settings → Workspace, append the key filename, and enter that full path in Private key path. This field takes a file path, not the key contents or the server path.','填写本地私钥文件路径','把私钥文件导入本地工作区。在“设置 → 工作区”复制工作区文件夹路径，追加私钥文件名，再填入 Private key path。这里填写文件路径，不是密钥正文，也不是服务器上的路径。',{action:'input'}),
 step('S36','passphrase','Enter the key passphrase if needed','For an encrypted key, use its passphrase. This is not necessarily the server account password. Save the profile.','按需填写私钥口令','加密私钥需要填写对应口令；它不一定等于服务器账号密码，然后保存配置。',{action:'input'}),
 step('S37','primary','Verify and connect','Verify the host fingerprint, then connect and open the remote directory. If rejected, check the username and matching authorized public key.','核验后连接','核验主机指纹后连接并打开远程目录。若被拒绝，检查用户名和服务器上授权的公钥是否匹配。')
 ],['remote/ssh','remote/files'],{note:pair('Keep private-key files out of Git repositories and shared exports. Use a separate unshared local folder and an SSH key format supported by Vibeit (Ed25519 or RSA).','私钥文件应放在独立且不共享的本地文件夹中，避免进入 Git 仓库或共享导出。使用 Vibeit 支持的 Ed25519 或 RSA 私钥格式。')}),
 topic('remote/files','remote',3,'Manage remote files with SFTP','通过 SFTP 管理远程文件','Browse and edit files in the selected server directory.','浏览和编辑所选服务器目录中的文件。','Locations → saved host → remote file browser',['pro','network','ssh'],[
 step('S38','primary','Choose the connected host','Select the verified host and wait for its file list. Confirm the remote path before editing.','选择已连接主机','点选已核验主机，等待文件列表，并在编辑前确认远程路径。'),
 step('S38','folder','Open the project directory','Enter the project folder and select a notebook or script. Remote work uses server paths and permissions.','进入项目目录','打开项目文件夹并选择笔记本或脚本。远程操作使用服务器路径和权限。'),
 step('S38','file','Edit and save a small file','Make a small change and use the editor’s save action. Wait for the upload to finish before closing the connection.','编辑并保存小文件','做一处小修改并保存，等待上传完成后再关闭连接。'),
 step('S38','status','Reopen to verify the saved content','Refresh or reopen the file to confirm the server has the saved version. Resolve any external-change warning before overwriting another edit.','重新打开核对内容','刷新或重新打开文件，确认服务器保存了新版本。遇到外部修改提醒时，先核对再覆盖。')
 ],['remote/python','git/sync']),
 topic('remote/python','remote',4,'Choose a remote Python environment','选择远程 Python 环境','Select a server interpreter and verify where a script runs.','选择服务器解释器，并验证脚本实际运行的位置。','Connected host → Packages → Environment',['pro','network','ssh'],[
 step('S40','discover','Discover server environments','Open the remote Packages panel and refresh environment discovery. Python and the required packages must be installed on the server.','发现服务器环境','打开远程 Packages 面板并刷新环境发现。服务器需要已安装 Python 和所需依赖。'),
 step('S40','primary','Select the interpreter','Choose the Python environment and check its path. Use the intended virtual environment instead of assuming every python3 is identical.','选择解释器','选择 Python 环境并检查路径。明确选择所需虚拟环境，不要假定所有 python3 都相同。'),
 step('S40','packages','Check its packages','The installed-package list belongs to the selected interpreter. Install missing packages there when you have permission.','检查对应依赖','已安装包列表属于所选解释器。有权限时，可在这里安装缺失依赖。'),
 step('S39','primary','Run a small verification','Run the example remotely and check the interpreter path and operating system. A remote result uses server hardware, not the iPad GPU.','运行小型验证','远程运行示例，核对解释器路径和操作系统。远程结果使用服务器硬件，不使用 iPad GPU。',{code:'import sys, platform\nprint(sys.executable)\nprint(platform.system())'})
 ],['remote/files','models/packages']),
 topic('remote/cloudflare','remote',5,'Configure Cloudflare Access','配置 Cloudflare Access','Use an existing Cloudflare Access SSH application from Vibeit.','在 Vibeit 中连接已经配置好的 Cloudflare Access SSH 应用。','Add Remote Host → Connection → Cloudflare Access',['pro','network','ssh'],[
 step('S41','primary','Confirm the server-side setup','Ask the administrator for the Access hostname, team domain and SSH user. The tunnel and Access policy must already be configured.','确认服务器端准备','向管理员取得 Access 主机域名、团队域名和 SSH 用户名。隧道和 Access 策略需要已配置。'),
 step('S41','host','Select Cloudflare Access','Choose Cloudflare Access and enter its hostname and team domain. This transport uses the Access hostname rather than a direct SSH port.','选择 Cloudflare Access','选择该连接方式，填写主机域名和团队域名。它使用 Access 主机域名，不填写直连 SSH 端口。',{action:'input'}),
 step('S41','login','Complete Access sign-in','Tap Sign in with Cloudflare Access and complete the identity-provider flow. Configure the SSH password or key separately.','完成 Access 登录','点击 Sign in with Cloudflare Access，完成身份提供商认证。SSH 密码或私钥仍需单独配置。'),
 step('S37','primary','Save, verify and connect','Keep the default connection concurrency unless your setup supports more. Save, verify the host key and confirm a real file connection.','保存、核验并连接','除非服务配置支持更多并发，否则保留默认并发数。保存、核验主机密钥，并实际连接文件目录。')
 ],['remote/ssh','remote/python'],{note:pair('Access authorization and SSH authentication are separate checks. Renew Access sign-in when its session expires.','Access 授权与 SSH 认证是两项独立检查。Access 会话过期后需要重新登录。')}),
 topic('terminal/basics','terminal',1,'Type, copy and paste in the terminal','在终端中输入、复制与粘贴','Use the terminal directly and distinguish local and remote commands.','直接操作终端，并区分本地与远程命令环境。','Editor → bottom panel → Terminal / Shell',['subscription'],[
 step('S11','primary','Focus the terminal window','Open the terminal and tap inside its surface. Type at the blinking cursor; there is no separate command-send box in this terminal.','使终端获得焦点','打开终端并点击窗口内部，在闪烁光标处输入。这种终端直接接收键盘输入。',{action:'input'}),
 step('S11','cursor','Run a harmless command','Enter pwd and press Return to see the current directory. Check the active location before running commands.','运行无害命令','输入 pwd 并回车查看当前目录。执行命令前确认当前使用的位置。',{action:'input',code:'pwd'}),
 step('S12','primary','Use the system editing menu','Long-press terminal text to select it, adjust the selection handles and choose Copy. Focus the terminal and long-press for Paste when the system menu offers it.','使用系统编辑菜单','长按终端文字进行选择，调整选择范围并点击复制。使终端获得焦点后，长按并使用系统菜单中的粘贴。',{action:'longPress'}),
 step('S11','keys','Use keyboard shortcuts carefully','With a hardware keyboard, use Command–C and Command–V for copy/paste when text selection is active. Control–C interrupts the foreground command; it is not the copy shortcut.','正确使用快捷键','连接外接键盘时，选中文字后使用 Command–C 与 Command–V 复制粘贴。Control–C 用于中断前台命令，不是复制快捷键。'),
 step('S39','primary','Check the remote alternative','A remote terminal sends commands to the server. Local iPad commands and available packages differ from a desktop or Linux shell.','理解远程终端','远程终端把命令发送到服务器。iPad 本地终端的命令和依赖与桌面或 Linux Shell 不完全相同。')
 ],['models/environment','remote/ssh']),
 topic('support/plans','support',1,'Understand Standard, Pro and trials','了解 Standard、Pro 与试用','Find your current entitlement and the available subscription options.','查看当前权益和可选择的订阅方案。','Settings → Account',['network'],[
 step('S42','primary','Open your account page','Open Settings → Account and read the current subscription status. Trial eligibility and offers are shown by the App Store.','打开账户页面','进入“设置 → 账户”查看当前订阅状态。试用资格和优惠以 App Store 显示为准。'),
 step('S42','plans','Compare available plans','Standard covers local coding. Pro adds supported cloud AI and remote workflows. Read the current feature list on the purchase screen before choosing.','比较可用方案','Standard 支持本地编程；Pro 增加受支持的云端 AI 和远程工作流程。选择前阅读购买页面的当前功能说明。'),
 step('S42','purchase','Choose a plan and review Apple’s confirmation','Select an offered subscription and review the price, billing period and renewal terms in Apple’s purchase confirmation.','选择方案并检查确认信息','选择可用订阅，在 Apple 购买确认中检查价格、计费周期和续订条款。'),
 step('S42','status','Confirm the updated entitlement','After a successful purchase, return to the app and check the active plan. If a trial has ended, choose an available plan or restore a previous valid purchase.','确认权益更新','购买成功后返回 App 检查有效方案。试用结束时，可选择可用方案，或恢复之前仍有效的购买。')
 ],['support/restore','support/troubleshooting'],{note:pair('Third-party AI accounts, API usage and server costs are separate from Vibeit subscriptions.','第三方 AI 账号、API 用量和服务器费用不包含在 Vibeit 订阅中。')}),
 topic('support/restore','support',2,'Restore a previous purchase','恢复之前的购买','Ask the App Store to refresh an existing subscription entitlement.','向 App Store 刷新已有订阅权益。','Settings → Account → Restore Purchases',['network'],[
 step('S42','restore','Use the purchasing Apple Account','Confirm the device’s Media & Purchases account is the one that purchased Vibeit.','使用原购买账号','确认设备“媒体与购买项目”使用的是当初购买 Vibeit 的 Apple 账号。'),
 step('S42','restore','Restore purchases','Tap Restore Purchases and complete any Apple authentication request. Wait for the result.','恢复购买','点击 Restore Purchases，完成可能出现的 Apple 验证，然后等待结果。'),
 step('S43','primary','Read the outcome','A valid restored subscription should update the active plan. An expired or absent subscription cannot create new access.','查看恢复结果','恢复有效订阅后，当前方案应更新。已到期或不存在的订阅不能生成新的使用权益。'),
 step('S42','plans','Choose a next step','If no active purchase is found, inspect the offered plans. If Apple shows an active subscription but Vibeit does not, send a report with the version and error message.','选择下一步','没有找到有效购买时，查看可选方案。如果 Apple 显示订阅有效而 App 未识别，请附版本和错误信息反馈。')
 ],['support/plans','support/troubleshooting']),
 topic('support/troubleshooting','support',3,'Troubleshoot and report a problem','排查并报告问题','Collect useful evidence and send a bug report from Settings.','收集有用信息，并从设置中发送问题报告。','Settings → Report an Issue',['network'],[
 step('S01','primary','Identify the affected workflow','Record whether the problem affects local Python, a provider, Git, a remote host or a purchase. Note the first error message and what you expected.','确定发生问题的流程','记录问题发生在本地 Python、AI 服务、Git、远程主机还是购买流程，保存第一条错误信息和预期结果。'),
 step('S44','primary','Open Report an Issue','Open Settings and choose Report an Issue. Give the report a specific title.','打开问题反馈','打开设置并选择 Report an Issue，为问题填写明确标题。'),
 step('S44','details','Describe a reproducible example','Describe what happened, the steps to reproduce, App version and device. Remove tokens, passwords, private host details and unrelated private data.','描述可复现的例子','说明现象、复现步骤、App 版本和设备，去除 Token、密码、私人主机信息及无关私人数据。',{action:'input'}),
 step('S44','submit','Submit and read the result','Use Submit Report when the required fields are complete. Confirm the result; if sending fails, use the support contact link below.','提交并检查结果','填完必填字段后点击 Submit Report，检查提交结果。发送失败时，使用下方支持联系入口。')
 ],['models/packages','ai/choose-provider','git/sync','remote/ssh','support/restore'],{aliases:['bug','error','report','问题反馈','排错','报错']})
];

import hfExamples from './hf-examples.json' with {type:'json'};
const hfTopic=topics.find(t=>t.id==='models/hugging-face');
hfTopic.steps[3].title=pair('Check presence and authorization','验证变量与授权');
hfTopic.steps[3].body=pair('Run the example. HF_TOKEN present: True confirms the kernel has the token; Hugging Face authorization: OK confirms the service accepts it. Approval for a gated model remains a separate requirement.','运行示例。HF_TOKEN present: True 表示内核已读取 Token；Hugging Face authorization: OK 表示服务已接受授权。受限模型的访问许可仍需单独获得。');
hfTopic.steps[3].code=hfExamples['hf-auth'];
hfTopic.steps[3].action='observe';
const downloadTopic=topics.find(t=>t.id==='models/downloads');
downloadTopic.requirements.push('huggingface');
downloadTopic.steps[0].body=pair('This exercise uses your saved token to verify an authenticated download. Public resources may also allow anonymous access; private or gated resources need account permissions as well as a valid token.','本练习使用保存的 Token 验证带授权的下载。公开资源也可能允许匿名访问；私有或受限资源除了有效 Token，还需要账号具有相应权限。');
downloadTopic.steps[1].code=hfExamples['hf-download'];
downloadTopic.steps[1].action='observe';
downloadTopic.expected=pair('Configuration downloaded: True confirms that the small configuration file was downloaded and parsed. It does not verify model inference or access to other models.','Configuration downloaded: True 表示小型配置文件已下载且能正确解析，不代表模型推理或其他模型的访问权限已验证。');

for(const t of topics)for(const s of t.steps)if(s.shot==='S04')s.action='observe';
// Distinct outputs need their own captures; do not reuse an unrelated success screen.
const environmentCheck=topics.find(t=>t.id==='models/environment').steps[3];environmentCheck.shot='S25-environment';environmentCheck.action='observe';
const importCheck=topics.find(t=>t.id==='models/packages').steps[3];importCheck.shot='S27-import';importCheck.action='observe';importCheck.code='import pandas\nprint("pandas available:", pandas.__version__ is not None)';
const tableResult=topics.find(t=>t.id==='notebooks/results').steps[0];tableResult.shot='S10-table';tableResult.action='observe';

// Use the exact screen for each action, including sheets reached from an earlier screen.
topics.find(t=>t.id==='getting-started/workspace').steps[3].target='section';
const fileSteps=topics.find(t=>t.id==='getting-started/files').steps;
fileSteps[0].shot='S02';fileSteps[0].target='import';fileSteps[2].shot='S01';fileSteps[2].target='file';fileSteps[3].target='primary';
topics.find(t=>t.id==='notebooks/results').steps[3].target='primary';
topics.find(t=>t.id==='ai/choose-provider').steps[3].shot='S14';topics.find(t=>t.id==='ai/choose-provider').steps[3].target='activate';
topics.find(t=>t.id==='ai/claude').steps[3].shot='S17-activate';topics.find(t=>t.id==='ai/claude').steps[3].target='primary';
Object.assign(topics.find(t=>t.id==='ai/agent').steps[2],{shot:'S19-approval',target:'primary',action:'observe'});
for (const t of topics) for (const s of t.steps) {
 if (s.shot==='S01' && s.target==='file') s.iphoneShot='S01-file';
 if (s.shot==='S13' && s.target==='section') s.iphoneShot='S13-section';
}
topics.find(t=>t.id==='support/plans').steps[1].shot='S42-plans';topics.find(t=>t.id==='support/plans').steps[1].target='primary';topics.find(t=>t.id==='support/plans').steps[2].shot='S42-plans';
topics.find(t=>t.id==='notebooks/cells').steps[3].shot='S07-editing';

// 1.0.1 keeps its interpreter alive on Restart; re-open the app to apply environment changes.
const restartNote=pair('On iOS/iPadOS 1.0.1, completely close and reopen Vibeit after changing Environment settings. Restart Kernel clears the Python session but does not reload these saved settings.','在 iOS/iPadOS 1.0.1 中，更改“环境”设置后，需要完全关闭并重新打开 Vibeit。Restart Kernel 会重置 Python 会话，但不会重新加载这些设置。');
for(const id of ['models/hugging-face','models/environment']){
 const t=topics.find(t=>t.id===id);t.note=restartNote;
 t.steps[2].shot='S09-relaunch';t.steps[2].action='tap';
 t.steps[2].title=pair('Close and reopen Vibeit','完全关闭并重新打开 Vibeit');
 t.steps[2].body=pair('Save your work. Open the system app switcher, swipe Vibeit’s card upward to close it, then tap the Vibeit icon to open it again. Returning to the Home Screen alone does not restart the app.','先保存文件。打开系统多任务视图，上划 Vibeit 的卡片关闭 App，再点击 Vibeit 图标重新打开。仅返回主屏幕不会重新启动 App。');
 t.links??=[];t.links.push(['Apple: quit and reopen an app','https://support.apple.com/en-ae/guide/ipad/ipad79518d15/ipados']);
}
const kernelTopic=topics.find(t=>t.id==='notebooks/kernel');kernelTopic.note=restartNote;
kernelTopic.steps[2].body=pair('Restart the kernel to clear in-memory variables. Saved source and existing rendered outputs are retained. Reopen the app when you need changed Environment settings to take effect.','重启内核会清除内存变量，并保留已保存的源码和已有输出。修改“环境”设置后，则需要重新打开 App 才会生效。');
const cloneTopic=topics.find(t=>t.id==='git/clone');cloneTopic.steps[1].title=pair('Enter the repository address','输入仓库地址');cloneTopic.steps[1].body=pair('Enter owner/repo or a full GitHub HTTPS URL. For editing practice, fork the tutorial repository into your own account and enter your fork’s address.','填写 owner/repo 或完整 GitHub HTTPS 地址。练习编辑时，先将教程仓库 fork 到自己的账号，再填写你的 fork 地址。');
topics.find(t=>t.id==='ai/codex').steps[2].shot='S16-models';
topics.find(t=>t.id==='git/github').steps[3].shot='S28-connected';topics.find(t=>t.id==='git/github').steps[3].target='primary';
topics.find(t=>t.id==='git/clone').steps[3].shot='S31-clean';
Object.assign(topics.find(t=>t.id==='git/pull-requests').steps[3],{shot:'S33-result',target:'primary',action:'observe'});
topics.find(t=>t.id==='models/packages').steps[2].shot='S27-install';topics.find(t=>t.id==='models/packages').steps[2].target='primary';
topics.find(t=>t.id==='support/plans').steps[2].shot='S42-purchase';topics.find(t=>t.id==='support/plans').steps[2].target='primary';
const reportStep=topics.find(t=>t.id==='support/troubleshooting').steps[3];reportStep.shot='S44-submit';reportStep.target='primary';reportStep.body=pair('Complete the required fields and any Human verification prompt, then use Submit Report. Read the result; if sending fails, use the support contact link below.','完成必填字段和页面要求的人机验证后，点击 Submit Report。检查提交结果；发送失败时使用下方支持联系入口。');
// On iPhone, kernel controls are nested in the ellipsis menu.
for(const t of topics)for(const s of t.steps)if(s.shot==='S09')s.iphoneBody=pair('On iPhone, open the notebook’s ellipsis menu. Choose Restart Kernel to retain existing outputs, or Interrupt to stop the current task. Restart and Clear Outputs also removes the displayed outputs.','iPhone 上先打开笔记本的省略号菜单。选择 Restart Kernel（重启内核）可保留已有输出；Interrupt 用于中断当前任务。Restart and Clear Outputs 还会清除已显示的输出。');

// Chinese variants share the same operational content and Simplified Chinese screenshots.
import {traditional} from './traditional.mjs';
for(const t of topics){
 for(const field of ['title','goal','note','expected'])if(t[field]?.['zh-hans'])t[field]['zh-hant']=traditional(t[field]['zh-hans']);
 for(const s of t.steps)for(const field of ['title','body','iphoneBody'])if(s[field]?.['zh-hans'])s[field]['zh-hant']=traditional(s[field]['zh-hans']);
}
import {applyTopicLocalizations} from './localizations.mjs';
applyTopicLocalizations(topics);
