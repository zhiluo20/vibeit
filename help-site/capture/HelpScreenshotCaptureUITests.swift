import XCTest
import StoreKitTest
import UIKit

/// Actual production screens, reached through the ordinary application UI.
/// No --pydev-ui-test fixture views or fake service results are used here.
final class HelpScreenshotCaptureUITests: XCTestCase {
    var app: XCUIApplication!
    var store: SKTestSession!
    var locale: String { ProcessInfo.processInfo.environment["HELP_CAPTURE_LOCALE"] ?? "en" }
    var device: String { UIDevice.current.userInterfaceIdiom == .pad ? "ipad" : "iphone" }

    override func setUp() {
        super.setUp()
        continueAfterFailure = false
    }

    @MainActor
    func launch() async throws {
        let url = try XCTUnwrap(Bundle(for: Self.self).url(forResource: "PyDev", withExtension: "storekit"))
        store = try SKTestSession(contentsOf: url)
        store.resetToDefaultState()
        store.clearTransactions()
        store.disableDialogs = true
        _ = try await store.buyProduct(identifier: "dev.pydev.pro.yearly")
        XCUIDevice.shared.orientation = device == "ipad" ? .landscapeLeft : .portrait
        app = XCUIApplication()
        app.launchArguments = ["--help-capture", "-AppleLanguages", "(\(locale))", "-AppleLocale", locale == "en" ? "en_US" : "zh_CN",
                               "-PyDevHasSeenWelcomeWalkthrough", "YES", "-PyDevHasSeenInteractiveGuide", "YES",
                               "-PyDevColorSchemePreset", "appleLight", "-PyDevThemePreference", "light"]
        app.launch()
        XCTAssertTrue(element("documentBrowser.more").waitForExistence(timeout: 30))
        if element("documentBrowser.workspace.local").exists { tap("documentBrowser.workspace.local") }
        if element("ide.console.mode").exists && element("ide.toggleBottomPanel").exists { tap("ide.toggleBottomPanel") }
    }

    @MainActor
    func element(_ id: String) -> XCUIElement { app.descendants(matching: .any)[id].firstMatch }

    @MainActor
    func tap(_ id: String) {
        let target = element(id)
        if !target.waitForExistence(timeout: 2) { reveal(id, sidebar: id.hasPrefix("documentBrowser.file.") || id.hasPrefix("settings.section.")) }
        XCTAssertTrue(target.waitForExistence(timeout: 15), "Missing capture target: \(id)")
        target.tap()
        if id.hasPrefix("documentBrowser.file."),element("ide.console.mode").exists {
            let toggle=element("ide.toggleBottomPanel")
            if toggle.exists && toggle.isHittable {toggle.tap()}
        }
    }

    @MainActor
    func openSettings(_ section: String? = nil) {
        tap("documentBrowser.more")
        tap("documentBrowser.settings")
        if let section { reveal("settings.section.\(section)", sidebar: true); tap("settings.section.\(section)") }
    }

    @MainActor
    func capture(_ id: String, targets: [String: XCUIElement], evidence: String = "configuration", systemScreen: Bool = false) throws {
        // Accessibility can report the destination before its transition has rendered.
        // Leave time for the actual on-screen frame, then reject obstructing onboarding.
        Thread.sleep(forTimeInterval: 1.2)
        let keyboardTip = app.staticTexts.matching(NSPredicate(format: "label CONTAINS %@", "Speed up your typing")).firstMatch
        if !systemScreen && keyboardTip.exists {
            let proceed = app.buttons["Continue"].firstMatch
            if proceed.exists { proceed.tap(); Thread.sleep(forTimeInterval: 0.6) }
        }
        if !systemScreen { XCTAssertFalse(keyboardTip.exists, "Dismiss the system keyboard tutorial before capturing public material.") }
        let shot = XCUIScreen.main.screenshot()
        let image = shot.image

        let bounds = systemScreen ? CGRect(origin:.zero,size:image.size) : app.frame
        XCTAssertLessThan(abs(bounds.width / bounds.height - image.size.width / image.size.height), 0.08, "Full-screen capture required")
        let pixelWidth = Int(image.size.width * image.scale)
        let pixelHeight = Int(image.size.height * image.scale)
        var rectangles: [String: [String: Double]] = [:]
        for (name, item) in targets where item.exists {
            let originalFrame=item.frame
            guard !originalFrame.isEmpty && (item.isHittable || !item.isEnabled) else {continue}
            let frame = originalFrame.intersection(bounds)
            guard bounds.contains(CGPoint(x: frame.midX, y: frame.midY)) else { continue }
            rectangles[name] = ["x": Double(frame.minX / bounds.maxX), "y": Double(frame.minY / bounds.maxY),
                                "w": Double(frame.width / bounds.width), "h": Double(frame.height / bounds.height)]
        }
        XCTAssertFalse(rectangles.isEmpty, "The expected screen must have at least one visible target.")
        let privateFields: [XCUIElement] = systemScreen ? [] : ["settings.provider.codexAccount", "github.deviceCode"].map { element($0) }.filter { $0.exists && !$0.frame.isEmpty && bounds.intersects($0.frame) }
        let redactions = privateFields.map { item -> [String:Double] in
            let f=item.frame.intersection(bounds)
            return ["x":Double(f.minX/bounds.width),"y":Double(f.minY/bounds.height),"w":Double(f.width/bounds.width),"h":Double(f.height/bounds.height)]
        }
        var metadata: [String: Any] = ["id":id,"device":device,"locale":locale,"appVersion":"1.0.1","build":"7",
                                      "width":pixelWidth,"height":pixelHeight,"targets":rectangles,"evidence":evidence,
                                      "capturedAt":ISO8601DateFormatter().string(from: Date()),
                                      "osVersion":UIDevice.current.systemVersion,"redactions":redactions]
        if id == "S16-models" {
            let options=app.buttons.allElementsBoundByIndex.filter { item in
                item.isHittable && (item.label.hasPrefix("GPT") || item.label.contains("Automatic (recommended)") || item.label.contains("自动（推荐）"))
            }
            let menu=options.reduce(CGRect.null) { $0.union($1.frame) }.insetBy(dx:-3,dy:-3).intersection(bounds)
            if !menu.isNull && !menu.isEmpty {
                metadata["crop"]=["x":Double(menu.minX/bounds.width),"y":Double(menu.minY/bounds.height),"w":Double(menu.width/bounds.width),"h":Double(menu.height/bounds.height)]
                // This crop contains only the open menu, which covers the underlying account row.
                metadata["redactions"]=[] as [[String:Double]]
            }
        }
        if id == "S09-relaunch", let icon=targets["primary"] {
            let crop=icon.frame.insetBy(dx:-8,dy:-8).intersection(bounds)
            metadata["crop"]=["x":Double(crop.minX/bounds.width),"y":Double(crop.minY/bounds.height),"w":Double(crop.width/bounds.width),"h":Double(crop.height/bounds.height)]
        }
        let base = "\(id).\(device).\(locale)"
        let format = UIGraphicsImageRendererFormat(); format.scale = image.scale
        let normalized = UIGraphicsImageRenderer(size: image.size, format: format).image { _ in
            image.draw(in: CGRect(origin: .zero, size: image.size))
        }
        let picture = XCTAttachment(image: normalized); picture.name = base; picture.lifetime = .keepAlways; add(picture)
        let record = XCTAttachment(data: try JSONSerialization.data(withJSONObject: metadata, options: [.sortedKeys]),
                                   uniformTypeIdentifier: "public.json")
        record.name = base + ".json"; record.lifetime = .keepAlways; add(record)
    }

    @MainActor
    func testCaptureWorkspaceAndSettings() async throws {
        try await launch()
        try capture("S01", targets:["primary":element("documentBrowser.more"),"create":element("documentBrowser.create"),"file":element("documentBrowser.file.hello.py")])
        if device == "iphone" { reveal("documentBrowser.file.hello.py",sidebar:true);try capture("S01-file",targets:["file":element("documentBrowser.file.hello.py")]) }
        tap("documentBrowser.create")
        try capture("S02", targets:["primary":element("documentBrowser.createNotebook"),"import":element("documentBrowser.importFiles"),"clone":element("documentBrowser.cloneGitHub")])
        app.coordinate(withNormalizedOffset:CGVector(dx:0.1,dy:0.15)).tap()
        openSettings()
        if device == "iphone" { try capture("S13-section",targets:["section":element("settings.section.intelligence")]) }
        tap("settings.section.intelligence")
        XCTAssertTrue(element("settings.provider.builtin-apple-intelligence").waitForExistence(timeout: 10))
        try capture("S13", targets:["primary":element("settings.provider.builtin-apple-intelligence"),"apple":element("settings.provider.builtin-apple-intelligence"),"codex":element("settings.provider.builtin-codex"),"section":element("settings.section.intelligence")])
    }

    @MainActor
    func testCaptureEnvironment() async throws {
        try await launch()
        openSettings("environment")
        XCTAssertTrue(element("settings.env.hfToken").waitForExistence(timeout: 12))
        try capture("S24", targets:["primary":element("settings.env.hfToken"),"newKey":element("settings.env.newKey"),"add":element("settings.env.add")])
    }


    @MainActor
    func reveal(_ id: String, sidebar: Bool = false) {
        let target = element(id)
        for attempt in 0..<12 {
            if target.exists && target.isHittable && app.frame.insetBy(dx: 4, dy: 6).contains(CGPoint(x: target.frame.midX, y: target.frame.midY)) { return }
            let scroll = app.scrollViews.containing(.any, identifier: id).firstMatch
            let list = app.collectionViews.containing(.any, identifier: id).firstMatch
            let viewport=scroll.exists ? scroll.frame : (list.exists ? list.frame : app.frame)
            let above=target.exists && !target.frame.isEmpty && target.frame.maxY < viewport.minY + 20
            let down=above || (!target.exists && attempt >= 5)
            var region=viewport.intersection(app.frame)
            if !scroll.exists && !list.exists, let form=app.collectionViews.allElementsBoundByIndex.last(where:{$0.isHittable && $0.frame.height > 200}) {region=form.frame.intersection(app.frame)}
            if let keyboard=app.keyboards.allElementsBoundByIndex.first,keyboard.frame.height>100 {
                region.size.height=max(0,min(region.maxY,keyboard.frame.minY-12)-region.minY)
            }
            guard region.height>80 else {hideKeyboard();continue}
            let x=sidebar && app.frame.width>700 ? app.frame.width*0.15 : region.midX
            let top=region.minY+min(50,region.height*0.2),bottom=region.maxY-min(35,region.height*0.15)
            let start=app.coordinate(withNormalizedOffset:CGVector(dx:x/app.frame.width,dy:(down ? top:bottom)/app.frame.height))
            let end=app.coordinate(withNormalizedOffset:CGVector(dx:x/app.frame.width,dy:(down ? bottom:top)/app.frame.height))
            start.press(forDuration:0.05,thenDragTo:end)
        }
    }

    @MainActor
    func cancelSheet() {
        let button = app.buttons[locale == "en" ? "Cancel" : "取消"].firstMatch
        XCTAssertTrue(button.waitForExistence(timeout: 5)); button.tap()
    }

    @MainActor
    func testCaptureProviderConfiguration() async throws {
        try await launch()
        openSettings("intelligence")
        let apple = "settings.provider.builtin-apple-intelligence"
        try capture("S13", targets:["primary":element(apple),"apple":element(apple),"codex":element("settings.provider.builtin-codex"),"section":element("settings.section.intelligence")])
        tap(apple)
        try capture("S14", targets:["primary":element("settings.useProvider"),"activate":element("settings.useProvider"),"status":app.staticTexts[ui("Status")].firstMatch], evidence:"hardware-configuration-only")
        cancelSheet()
        tap("settings.provider.builtin-codex")
        reveal("settings.provider.codexOAuthSignIn")
        try capture("S15", targets:["primary":element("settings.provider.codexOAuthSignIn")])
        cancelSheet()
        tap("settings.provider.builtin-claude")
        reveal("settings.provider.claudeAPIKey")
        try capture("S17", targets:["primary":element("settings.provider.claudeAPIKey"),"key":element("settings.provider.claudeAPIKey"),"models":element("settings.provider.claudeRefreshModels")])
        reveal("settings.useProvider")
        try capture("S17-activate", targets:["primary":element("settings.useProvider")])
        cancelSheet()
        reveal("settings.addModelProvider"); tap("settings.addModelProvider")
        tap("settings.addProvider.kind.custom")
        try capture("S18", targets:["primary":element("settings.addProvider.name"),"endpoint":element("settings.addProvider.url"),"model":element("settings.addProvider.model"),"save":element("settings.addProvider.confirm")])
    }

    @MainActor
    func testCaptureNotebookResult() async throws {
        try await launch()
        tap("documentBrowser.file.quickstart.ipynb")
        let editor = element("editor.codeTextView")
        XCTAssertTrue(editor.waitForExistence(timeout: 15))
        let run = app.buttons.matching(NSPredicate(format: "identifier BEGINSWITH 'cell.' AND identifier ENDSWITH '.run'")).firstMatch
        try capture("S03", targets:["primary":run,"editor":editor])
        run.tap()
        let output = app.staticTexts.matching(NSPredicate(format: "label CONTAINS %@", "Hello, Vibeit!")).firstMatch
        XCTAssertTrue(output.waitForExistence(timeout: 60), "The actual Python execution must produce the expected output.")
        try capture("S04", targets:["primary":output], evidence:"python-execution")
        if device == "iphone" { tap("notebook.more") }
        let restart = device == "iphone" ? app.buttons[locale == "en" ? "Restart Kernel" : "重启内核"].firstMatch : element("notebook.restart")
        try capture("S09", targets:["primary":restart,"interrupt":element("notebook.interrupt")])
    }

    @MainActor
    func testValidateHuggingFaceAuthorization() async throws {
        try await launch()
        tap("documentBrowser.file.hf-auth.ipynb")
        XCTAssertTrue(element("notebook.restart").waitForExistence(timeout: 15))
        try capture("S09", targets:["primary":element("notebook.restart"),"interrupt":element("notebook.interrupt")])
        tap("notebook.restart")
        XCTAssertTrue(element("kernel.status.idle").waitForExistence(timeout: 20))
        tap("notebook.runAll")
        let presence = app.staticTexts.matching(NSPredicate(format: "label CONTAINS %@", "HF_TOKEN present: True")).firstMatch
        let authorized = app.staticTexts.matching(NSPredicate(format: "label CONTAINS %@", "Hugging Face authorization: OK")).firstMatch
        let downloaded = app.staticTexts.matching(NSPredicate(format: "label CONTAINS %@", "Configuration downloaded: True")).firstMatch
        XCTAssertTrue(presence.waitForExistence(timeout: 60), "Saved token must reach the restarted Python kernel.")
        XCTAssertTrue(authorized.waitForExistence(timeout: 120), "Hugging Face must accept the token; never infer authorization from local presence.")
        try capture("S25", targets:["primary":authorized], evidence:"real-account-authorization")
        tap("documentBrowser.file.hf-download.ipynb")
        tap("notebook.runAll")
        XCTAssertTrue(downloaded.waitForExistence(timeout: 120), "The configuration download must return valid model JSON.")
        try capture("S26", targets:["primary":downloaded], evidence:"authenticated-config-download")
    }

    @MainActor
    func testPrepareTokenEntry() async throws {
        try await launch()
        openSettings("environment")
        XCTAssertTrue(element("settings.env.hfToken").waitForExistence(timeout: 12))
        print("HELP_TOKEN_ENTRY_READY")
        // Keep the real settings page available for manual secure input.
        try await Task.sleep(for: .seconds(1200))
    }

    @MainActor
    func testCaptureFeedback() async throws {
        try await launch()
        openSettings()
        reveal("settings.reportIssue", sidebar: true)
        tap("settings.reportIssue")
        try capture("S44", targets:["primary":element("issueReport.title"),"details":element("issueReport.whatHappened")])
        hideKeyboard();reveal("issueReport.submit")
        try capture("S44-submit",targets:["primary":element("issueReport.submit")])
    }

    @MainActor func ui(_ text: String) -> String { locale == "en" ? text : (Self.captureLabels[text] ?? text) }
    static let captureLabels: [String:String] = [
        "Done": "完成",
        "Cancel": "取消",
        "Status": "状态",
        "Settings": "设置",
        "Medium": "中",
        "High": "高",
        "Shell": "Shell",
        "Search memories": "搜索记忆",
        "Agent Memory": "Agent 记忆",
        "Agent Skills": "智能体技能",
        "Restart Kernel": "重启内核",
        "Password": "密码",
        "SSH Key": "SSH 密钥",
        "Cloudflare Access": "Cloudflare Access",
        "Direct (TCP)": "Direct (TCP)",
        "Copy": "拷贝",
        "Paste": "Paste",
        "Continue": "继续",
        "Name (optional)": "名称(可选)",
        "Username": "用户名",
        "Port": "端口",
        "Private key path": "私钥路径",
        "Key passphrase (if any)": "密钥口令(如有)",
        "Remote path": "远程路径",
        "Python interpreter": "Python 解释器",
        "Host (e.g. 192.168.1.10 or example.com)": "主机(如 192.168.1.10 或 example.com)",
        "Hostname (e.g. ssh.example.com)": "主机名(如 ssh.example.com)",
        "Sign in with Cloudflare Access": "使用 Cloudflare Access 登录",
        "Notebook": "笔记本",
        "Python Script": "Python Script",
        "HTML": "HTML",
        "PDF": "PDF",
        "Add Code Cell Below": "在下方添加代码 cell",
        "Convert to Code": "转为代码",
        "Export": "导出",
        "Save": "保存",
        "Update": "更新",
        "Close": "关闭",
        "Automatic (recommended)": "自动（推荐）",
        "Loaded %d OpenAI Codex models.": "已加载 %d 个 OpenAI Codex 模型。",
        "Pin Host Key": "固定主机密钥",
        "Search packages": "Search packages",
        "Stage All": "全部暂存",
        "Pull": "拉取",
        "Push": "推送"
    ]
    @MainActor func done() {
        let buttons = app.buttons.matching(NSPredicate(format: "label == %@ OR label == %@", ui("Done"), "Done")).allElementsBoundByIndex
        guard let button = buttons.last(where: { $0.isHittable }) else { XCTFail("Visible Done button required"); return }
        button.tap()
    }
    @MainActor func testCaptureMemorySkillsAndContext() async throws {
        try await launch(); openSettings("intelligence")
        reveal("settings.attachOpenFile")
        try capture("S21", targets:["primary":element("settings.attachOpenFile")])
        reveal("settings.manageMemory");tap("settings.manageMemory")
        XCTAssertTrue(app.searchFields.firstMatch.waitForExistence(timeout: 10))
        try capture("S22", targets:["primary":app.searchFields.firstMatch])
        done()
        reveal("settings.manageSkills");tap("settings.manageSkills")
        XCTAssertTrue(element("skills.add").waitForExistence(timeout: 10))
        let toggle=app.switches.matching(NSPredicate(format:"identifier BEGINSWITH 'skills.toggle.'")).firstMatch
        try capture("S23", targets:["primary":toggle,"add":element("skills.add")])
    }
    @MainActor func testCaptureAccountAndRestore() async throws {
        try await launch();openSettings("account")
        XCTAssertTrue(element("settings.viewPlans").waitForExistence(timeout: 20))
        try capture("S42", targets:["primary":element("settings.subscriptionHeading"),"status":element("settings.subscriptionHeading"),"plans":element("settings.viewPlans"),"restore":element("settings.restorePurchases")],evidence:"storekit-test-purchase")
        tap("settings.restorePurchases")
        XCTAssertTrue(element("settings.purchaseMessage").waitForExistence(timeout: 30))
        try capture("S43", targets:["primary":element("settings.purchaseMessage")],evidence:"storekit-test-restore")
        tap("settings.viewPlans")
        XCTAssertTrue(element("paywall.subscribe").waitForExistence(timeout: 20))
        try capture("S42-plans", targets:["primary":element("paywall.tierPicker")],evidence:"storekit-test-products")
        tap("paywall.tier.standard");reveal("paywall.subscribe")
        try capture("S42-purchase",targets:["primary":element("paywall.subscribe")],evidence:"storekit-test-products")
    }
    @MainActor func testCaptureAgentReasoning() async throws {
        try await launch()
        tap("documentBrowser.file.hello.py")
        if device == "iphone" {tap("BackButton");tap("documentBrowser.more");tap("documentBrowser.agent")}
        else {tap("ide.toggleAgent")}
        XCTAssertTrue(element("agent.input").waitForExistence(timeout: 20))
        try capture("S19", targets:["primary":element("agent.input")])
        tap("agent.reasoningMenu")
        let medium=app.buttons.matching(NSPredicate(format:"label CONTAINS %@",ui("Medium"))).allElementsBoundByIndex.first(where: { $0.isHittable }) ?? element("agent.reasoning.medium")
        let high=app.buttons.matching(NSPredicate(format:"label == %@",ui("High"))).firstMatch
        try capture("S20", targets:["primary":medium,"medium":medium,"high":high])
    }
    @MainActor func testCaptureGallery() async throws {
        try await launch();tap("documentBrowser.more");tap("documentBrowser.gallery")
        XCTAssertTrue(element("gallery.done").waitForExistence(timeout: 15))
        let card=app.buttons.matching(NSPredicate(format:"identifier BEGINSWITH 'gallery.card.'")).firstMatch
        try capture("S05", targets:["primary":card,"example":card])
    }
    @MainActor func testCaptureCloneForm() async throws {
        try await launch();tap("documentBrowser.create");tap("documentBrowser.cloneGitHub")
        tap("githubClone.input");element("githubClone.input").typeText("zhiluo20/vibeit-tutorials")
        try capture("S30", targets:["primary":element("githubClone.input"),"repository":element("githubClone.input"),"clone":element("githubClone.clone")])
    }


    @MainActor func fill(_ field: XCUIElement, _ value: String) {
        XCTAssertTrue(field.waitForExistence(timeout:10));
        if !field.isHittable && !field.identifier.isEmpty { reveal(field.identifier) }
        field.tap();Thread.sleep(forTimeInterval:0.35);field.tap()
        if let old=field.value as? String, old != field.placeholderValue, !old.isEmpty {field.typeText(String(repeating:XCUIKeyboardKey.delete.rawValue,count:old.count))}
        if field.identifier == "remoteHostForm.port" {
            for digit in value {field.typeText(String(digit));Thread.sleep(forTimeInterval:0.1)}
        } else {field.typeText(value)}
        if field.elementType == .textField { XCTAssertEqual(field.value as? String,value,"Capture input must match the intended demonstration value") }
    }
    @MainActor func hideKeyboard() {
        let hide=app.buttons.matching(NSPredicate(format:"label == 'Hide keyboard' OR label == '隐藏键盘' OR label == '收起键盘'")).firstMatch
        if hide.waitForExistence(timeout:3) && hide.isHittable {hide.tap()}
    }
    @MainActor func testCaptureShell() async throws {
        try await launch();tap("documentBrowser.file.quickstart.ipynb");if !element("ide.console.mode").exists {tap("ide.toggleBottomPanel")}
        let shell=app.segmentedControls["ide.console.mode"].buttons["Shell"]
        XCTAssertTrue(shell.waitForExistence(timeout:10));shell.tap()
        let input=element("sandbox.terminal.input");XCTAssertTrue(input.waitForExistence(timeout:10));input.tap();input.typeText("echo Vibeit terminal\n")
        let line=app.staticTexts["Vibeit terminal"].firstMatch
        XCTAssertTrue(line.waitForExistence(timeout:20))
        try capture("S11", targets:["primary":input,"cursor":input,"keys":input])
        line.press(forDuration:1.3)
        let copy=app.descendants(matching:.any).matching(NSPredicate(format:"label == 'Copy' OR label == '复制' OR label == '拷贝'")).firstMatch
        XCTAssertTrue(copy.waitForExistence(timeout:10))
        try capture("S12", targets:["primary":copy])
    }
    @MainActor func testCaptureRichCells() async throws {
        try await launch();tap("documentBrowser.file.rich-content.ipynb")
        let edit=app.buttons.matching(NSPredicate(format:"identifier ENDSWITH '.htmlToggle'")).firstMatch
        XCTAssertTrue(edit.waitForExistence(timeout:15))
        XCTAssertTrue(app.webViews.buttons["Add one"].firstMatch.waitForExistence(timeout:25))
        try capture("S07",targets:["primary":edit,"edit":edit])
        edit.tap()
        try capture("S07-editing",targets:["primary":edit])
        edit.tap()
        let button=app.webViews.buttons["Add one"].firstMatch
        XCTAssertTrue(button.waitForExistence(timeout:20));button.tap()
        XCTAssertTrue(app.webViews.staticTexts["Count: 1"].firstMatch.waitForExistence(timeout:10))
        try capture("S10",targets:["primary":button,"output":app.webViews.firstMatch],evidence:"inline-html-interaction")
    }
    @MainActor func testCapturePackageImportAndTable() async throws {
        try await launch();tap("documentBrowser.file.package-check.ipynb");tap("notebook.runAll")
        let result=app.staticTexts.matching(NSPredicate(format:"label CONTAINS %@","pandas available: True")).firstMatch
        XCTAssertTrue(result.waitForExistence(timeout:40))
        try capture("S27-import",targets:["primary":result],evidence:"python-package-availability")
        tap("documentBrowser.file.table-view.ipynb");tap("notebook.runAll")
        let table=app.webViews.firstMatch
        XCTAssertTrue(table.waitForExistence(timeout:45))
        try capture("S10-table",targets:["primary":table],evidence:"pandas-table-rendering")
    }
    @MainActor func testCaptureEnvironmentVariable() async throws {
        try await launch();openSettings("environment")
        fill(element("settings.env.newKey"),"VIBEIT_DEMO");fill(element("settings.env.newValue"),"tutorial");tap("settings.env.add");done()
        app.terminate();app.launch()
        XCTAssertTrue(element("documentBrowser.more").waitForExistence(timeout:30))
        tap("documentBrowser.file.environment-check.ipynb");tap("notebook.restart");tap("notebook.runAll")
        let result=app.staticTexts.matching(NSPredicate(format:"label CONTAINS %@","VIBEIT_DEMO = tutorial")).firstMatch
        XCTAssertTrue(result.waitForExistence(timeout:40))
        try capture("S25-environment",targets:["primary":result],evidence:"environment-after-kernel-restart")
    }
    @MainActor func testCaptureRemoteForms() async throws {
        try await launch()
        try capture("S34",targets:["primary":element("documentBrowser.addRemoteHost")])
        addHostForm()
        let host=element("remoteHostForm.host")
        fill(element("remoteHostForm.name"),"Tutorial SSH")
        fill(host,"127.0.0.1");fill(element("remoteHostForm.username"),"student")
        fill(element("remoteHostForm.port"),"2222")
        app.segmentedControls.buttons[ui("Cloudflare Access")].firstMatch.tap()
        app.segmentedControls.buttons.matching(NSPredicate(format:"label == %@ OR label == %@",ui("Direct (TCP)"),"Direct (TCP)")).firstMatch.tap()
        try capture("S35",targets:["host":host,"password":element("remoteHostForm.password")])
        tap("remoteHostForm.authMethod");app.buttons[ui("SSH Key")].firstMatch.tap()
        try capture("S36",targets:["primary":element("remoteHostForm.keyPath"),"key":element("remoteHostForm.keyPath"),"passphrase":element("remoteHostForm.passphrase")])
        app.segmentedControls.buttons[ui("Cloudflare Access")].firstMatch.tap()
        // Keep the demonstration hostname already present; no external sign-in is performed.
        reveal("remoteHostForm.cloudflareLogin")
        try capture("S41",targets:["primary":host,"host":host,"login":element("remoteHostForm.cloudflareLogin")])
    }

    @MainActor func testCaptureRelaunchApp() async throws {
        try await launch()
        app.terminate()
        XCUIDevice.shared.press(.home)
        let springboard=XCUIApplication(bundleIdentifier:"com.apple.springboard")
        let icon=springboard.descendants(matching:.any).matching(NSPredicate(format:"label == 'Vibeit'")).firstMatch
        if !icon.waitForExistence(timeout:3) { springboard.swipeLeft() }
        XCTAssertTrue(icon.waitForExistence(timeout:15))
        try capture("S09-relaunch",targets:["primary":icon],evidence:"system-home-reopen",systemScreen:true)
    }
    @MainActor func testCaptureGitHubSignIn() async throws {
        try await launch();openSettings("sourceControl")
        XCTAssertTrue(element("github.signIn").waitForExistence(timeout:15))
        try capture("S28",targets:["primary":element("github.signIn")])
        tap("github.signIn")
        XCTAssertTrue(element("github.openVerification").waitForExistence(timeout:40))
        try capture("S29",targets:["primary":element("github.openVerification"),"code":element("github.deviceCode")])
    }

    @MainActor func addHostForm() {
        if element("documentBrowser.addRemoteHost.empty").exists {tap("documentBrowser.addRemoteHost.empty")}
        else {tap("documentBrowser.addRemoteHost");tap("documentBrowser.addRemoteHost.menuItem")}
    }
    @MainActor func testCaptureSSHPasswordAndKey() async throws {
        try await launch();addHostForm()
        fill(element("remoteHostForm.name"),"Tutorial SSH " + locale)
        fill(element("remoteHostForm.host"),"127.0.0.1")
        fill(element("remoteHostForm.username"),"student")
        fill(element("remoteHostForm.path"),"/home/student/tutorials")
        let password=try XCTUnwrap(ProcessInfo.processInfo.environment["HELP_SSH_PASSWORD"])
        element("remoteHostForm.password").tap();element("remoteHostForm.password").typeText(password)
        fill(element("remoteHostForm.port"),"2222")
        hideKeyboard();app.segmentedControls.buttons[ui("Cloudflare Access")].firstMatch.tap();app.segmentedControls.buttons.matching(NSPredicate(format:"label == %@ OR label == %@",ui("Direct (TCP)"),"Direct (TCP)")).firstMatch.tap()
        tap("remoteHostForm.save");tap("documentBrowser.remoteVerifyHostKey")
        let alert=app.alerts.firstMatch
        XCTAssertTrue(alert.waitForExistence(timeout:40))
        let message=alert.staticTexts.allElementsBoundByIndex.map(\.label).joined(separator:" ")
        let trusted=(ProcessInfo.processInfo.environment["HELP_SSH_FINGERPRINTS"] ?? "").split(separator:"|")
        XCTAssertTrue(trusted.contains { message.contains(String($0)) },"Host key must match the isolated server's actual public key")
        try capture("S37",targets:["primary":element("documentBrowser.pinHostKey")],evidence:"verified-local-server-fingerprint")
        tap("documentBrowser.pinHostKey")
        XCTAssertTrue(element("documentBrowser.remoteEntry.hello.py").waitForExistence(timeout:40))
        try capture("S38",targets:["primary":element("documentBrowser.remoteEntry.hello.py"),"file":element("documentBrowser.remoteEntry.hello.py"),"folder":element("documentBrowser.remoteEntry.data"),"status":element("documentBrowser.remoteEntry.hello.py")],evidence:"authenticated-sftp-listing")
        tap("documentBrowser.remotePackages")
        XCTAssertTrue(element("remotePackages.environment").waitForExistence(timeout:30))
        let environmentReady=expectation(for:NSPredicate(format:"enabled == true"),evaluatedWith:element("remotePackages.environment"))
        await fulfillment(of:[environmentReady],timeout:45)
        try capture("S40",targets:["primary":element("remotePackages.environment"),"discover":element("remotePackages.discover"),"packages":element("remotePackages.interpreter")],evidence:"server-environment-discovery")
        done();tap("documentBrowser.remoteConsole")
        let terminal=element("terminal.inputSurface")
        XCTAssertTrue(terminal.waitForExistence(timeout:30))
        let terminalReady=expectation(for:NSPredicate(format:"enabled == true"),evaluatedWith:element("remote.shell.interrupt"))
        await fulfillment(of:[terminalReady],timeout:30)
        terminal.tap();terminal.typeText("python3 -c 'import sys,platform; print(sys.executable); print(platform.system())'\n")
        let linux=app.descendants(matching:.any).matching(NSPredicate(format:"label CONTAINS 'Linux'")).firstMatch
        XCTAssertTrue(linux.waitForExistence(timeout:40))
        try capture("S39",targets:["primary":terminal],evidence:"remote-python-execution")
        addHostForm()
        fill(element("remoteHostForm.name"),"Tutorial SSH Key " + locale)
        fill(element("remoteHostForm.host"),"127.0.0.1");fill(element("remoteHostForm.username"),"student")
        fill(element("remoteHostForm.path"),"/home/student/tutorials");fill(element("remoteHostForm.port"),"2222")
        hideKeyboard();app.segmentedControls.buttons[ui("Cloudflare Access")].firstMatch.tap();app.segmentedControls.buttons.matching(NSPredicate(format:"label == %@ OR label == %@",ui("Direct (TCP)"),"Direct (TCP)")).firstMatch.tap()
        tap("remoteHostForm.authMethod");app.buttons[ui("SSH Key")].firstMatch.tap()
        fill(element("remoteHostForm.keyPath"),"~/Documents/.ssh/id_ed25519");hideKeyboard()
        tap("remoteHostForm.save");tap("documentBrowser.remoteVerifyHostKey")
        XCTAssertTrue(alert.waitForExistence(timeout:40))
        let keyMessage=alert.staticTexts.allElementsBoundByIndex.map(\.label).joined(separator:" ")
        XCTAssertTrue(trusted.contains{keyMessage.contains(String($0))})
        tap("documentBrowser.pinHostKey")
        XCTAssertTrue(element("documentBrowser.remoteEntry.hello.py").waitForExistence(timeout:40))
        try capture("S38-key",targets:["primary":element("documentBrowser.remoteEntry.hello.py")],evidence:"ed25519-authenticated-sftp")
    }
    @MainActor func testCaptureExportMenu() async throws {
        try await launch();tap("documentBrowser.file.quickstart.ipynb")
        let export=app.buttons.matching(NSPredicate(format:"label BEGINSWITH 'Export ' OR label BEGINSWITH '导出 '")).firstMatch
        XCTAssertTrue(export.waitForExistence(timeout:15));export.tap()
        let notebook=app.buttons.matching(NSPredicate(format:"label == %@ OR label == %@",ui("Notebook"),"Notebook")).firstMatch
        XCTAssertTrue(notebook.waitForExistence(timeout:10))
        try capture("S06",targets:["primary":notebook,"export":notebook])
    }
    @MainActor func testCapturePackageCatalog() async throws {
        try await launch();tap("documentBrowser.more");tap("documentBrowser.packages")
        XCTAssertTrue(element("packages.search").waitForExistence(timeout:20))
        try capture("S27",targets:["primary":element("packages.search"),"search":element("packages.search")])
    }
    @MainActor func testCaptureCodexCatalog() async throws {
        try await launch();openSettings("intelligence");tap("settings.provider.builtin-codex")
        XCTAssertTrue(element("settings.provider.codexRefreshModels").waitForExistence(timeout:15))
        tap("settings.provider.codexRefreshModels")
        let prefix=ui("Loaded %d OpenAI Codex models.").components(separatedBy:"%").first ?? "Loaded"
        reveal("settings.provider.codexStatus")
        let status=element("settings.provider.codexStatus")
        let loaded=NSPredicate(format:"label BEGINSWITH %@",prefix)
        let ready=expectation(for:loaded,evaluatedWith:status)
        await fulfillment(of:[ready],timeout:60)
        try capture("S16",targets:["primary":element("settings.provider.codexModel"),"status":status,"refresh":element("settings.provider.codexRefreshModels")],evidence:"live-account-model-discovery")
        app.collectionViews.allElementsBoundByIndex.last?.swipeDown()
        tap("settings.provider.codexModel")
        let automatic=app.buttons.matching(NSPredicate(format:"label CONTAINS %@",ui("Automatic (recommended)"))).allElementsBoundByIndex.first(where: { $0.isHittable }) ?? element("settings.provider.codexModel")
        try capture("S16-models",targets:["primary":automatic],evidence:"live-account-model-catalog")
    }

    @MainActor func testCaptureActualClone() async throws {
        try await launch();tap("documentBrowser.create");tap("documentBrowser.cloneGitHub")
        fill(element("githubClone.input"),"zhiluo20/vibeit-tutorials")
        tap("githubClone.clone")
        let repo=app.descendants(matching:.any).matching(NSPredicate(format:"identifier BEGINSWITH 'documentBrowser.github.'")).firstMatch
        XCTAssertTrue(repo.waitForExistence(timeout:60));repo.tap()
        tap("documentBrowser.localGit")
        XCTAssertTrue(element("gitPanel.branch").waitForExistence(timeout:30))
        try capture("S31-clean",targets:["primary":element("gitPanel.branch")],evidence:"native-github-clone")
    }
    @MainActor func testCaptureGitCommitPushAndPR() async throws {
        try await launch()
        let repo=app.descendants(matching:.any).matching(NSPredicate(format:"identifier BEGINSWITH 'documentBrowser.github.'")).firstMatch
        XCTAssertTrue(repo.waitForExistence(timeout:15));repo.tap()
        tap("documentBrowser.file.hello.py")
        let editor=element("editor.codeTextView");XCTAssertTrue(editor.waitForExistence(timeout:15))
        editor.tap();editor.typeText("\n# A greeting example edited in Vibeit.\n")
        if device == "iphone" {tap("BackButton")}
        tap("documentBrowser.localGit")
        XCTAssertTrue(element("gitPanel.change.hello.py").waitForExistence(timeout:30))
        try capture("S31",targets:["primary":element("gitPanel.change.hello.py"),"stage":element("gitPanel.change.hello.py")],evidence:"native-working-copy-diff")
        let changeRow=element("gitPanel.change.hello.py")
        changeRow.coordinate(withNormalizedOffset:CGVector(dx:0.1,dy:0.5)).press(forDuration:0.05,thenDragTo:changeRow.coordinate(withNormalizedOffset:CGVector(dx:0.55,dy:0.5)))
        let stage=app.buttons.matching(NSPredicate(format:"label == 'Stage' OR label == '暂存'")).firstMatch
        XCTAssertTrue(stage.waitForExistence(timeout:10));stage.tap()
        fill(element("gitPanel.message"),"Explain the greeting example");hideKeyboard()
        let staged=expectation(for:NSPredicate(format:"enabled == true"),evaluatedWith:element("gitPanel.commit"))
        await fulfillment(of:[staged],timeout:20)
        try capture("S32",targets:["primary":element("gitPanel.branch"),"message":element("gitPanel.message"),"commit":element("gitPanel.commit"),"pull":element("gitPanel.pull"),"push":element("gitPanel.push"),"status":element("gitPanel.branch")])
        tap("gitPanel.commit")
        try await Task.sleep(for: .seconds(1))
        if let message=element("gitPanel.message").value as? String,message=="Explain the greeting example",element("gitPanel.commit").isEnabled {
            element("gitPanel.commit").coordinate(withNormalizedOffset:CGVector(dx:0.5,dy:0.5)).tap()
        }
        let history=app.staticTexts["Explain the greeting example"].firstMatch
        XCTAssertTrue(history.waitForExistence(timeout:30))
        tap("gitPanel.push")
        let pushReady=expectation(for:NSPredicate(format:"enabled == true"),evaluatedWith:element("gitPanel.push"))
        await fulfillment(of:[pushReady],timeout:60)
        try capture("S32-success",targets:["primary":history],evidence:"native-commit-history")
        tap("gitPanel.createPR")
        fill(element("githubPR.title"),"Tutorial: explain the greeting example")
        hideKeyboard();reveal("githubPR.create")
        try capture("S33",targets:["primary":element("githubPR.create"),"title":element("githubPR.title")])
        if ProcessInfo.processInfo.environment["HELP_CREATE_PR"] == "1" {
            fill(element("githubPR.description"),"Demonstration pull request created from Vibeit for the official help center. Adds a comment to the tutorial greeting example.")
            hideKeyboard();tap("githubPR.create")
            XCTAssertTrue(element("githubPR.view").waitForExistence(timeout:60))
            try capture("S33-result",targets:["primary":element("githubPR.view")],evidence:"native-github-pull-request")
        }
    }

    @MainActor func testCaptureEditingTools() async throws {
        try await launch();tap("documentBrowser.file.quickstart.ipynb");tap("notebook.more");tap("notebook.find")
        let search=app.textFields.firstMatch
        XCTAssertTrue(search.waitForExistence(timeout:15))
        try capture("S08",targets:["primary":search])
    }
    @MainActor func testCaptureCompatiblePackageInstall() async throws {
        try await launch();tap("documentBrowser.more");tap("documentBrowser.packages")
        fill(element("packages.search"),"pyfiglet");hideKeyboard();tap("packages.lookupPyPI")
        let install=element("packages.pypiInstall.pyfiglet")
        XCTAssertTrue(install.waitForExistence(timeout:40))
        let ready=expectation(for:NSPredicate(format:"enabled == true"),evaluatedWith:install)
        await fulfillment(of:[ready],timeout:45)
        hideKeyboard();reveal("packages.pypiInstall.pyfiglet")
        try capture("S27-install",targets:["primary":install])
        install.tap()
        let installed=expectation(for:NSPredicate(format:"label CONTAINS 'Reinstall' OR label CONTAINS '重新安装'"),evaluatedWith:install)
        await fulfillment(of:[installed],timeout:90)
        try capture("S27-installed",targets:["primary":install],evidence:"compatible-pypi-package-install")
    }

    @MainActor func testCaptureConnectedGitHub() async throws {
        try await launch();openSettings("sourceControl")
        let status=app.staticTexts.matching(NSPredicate(format:"label CONTAINS 'Signed in.' OR label CONTAINS '已登录'")).firstMatch
        XCTAssertTrue(status.waitForExistence(timeout:15))
        try capture("S28-connected",targets:["primary":status],evidence:"existing-authorized-github-account")
    }
    @MainActor func testCaptureDownloadLocation() async throws {
        try await launch();tap("documentBrowser.file.hf-download.ipynb")
        let result=app.staticTexts.matching(NSPredicate(format:"label CONTAINS 'Configuration downloaded: True'")).firstMatch
        XCTAssertTrue(result.waitForExistence(timeout:15));reveal("documentBrowser.file.Models",sidebar:true)
        try capture("S26",targets:["primary":result,"files":element("documentBrowser.file.Models")],evidence:"previously-verified-authenticated-download")
    }

    @MainActor func testCaptureAgentConfirmation() async throws {
        try await launch();openSettings("intelligence");tap("settings.provider.builtin-codex")
        reveal("settings.useProvider");tap("settings.useProvider")
        if element("settings.section.intelligence").exists {done()}
        tap("documentBrowser.more");tap("documentBrowser.agent")
        let prompt=locale == "en" ? "Use ask_user to ask whether to explain hello.py or add comments. Offer Explain the code and Add comments. Wait for my choice before doing anything else." : "请使用 ask_user 询问我想解释 hello.py 还是添加注释，提供解释代码和添加注释两个选项，等待我的选择后再继续。"
        fill(element("agent.input"),prompt);hideKeyboard();XCTAssertTrue(element("agent.send").isEnabled);tap("agent.send")
        try await Task.sleep(for: .seconds(1))
        if element("agent.send").exists,element("agent.input").value as? String==prompt {
            element("agent.send").coordinate(withNormalizedOffset:CGVector(dx:0.5,dy:0.5)).tap()
        }
        let confirmation=element("agent.confirmationTitle")
        XCTAssertTrue(confirmation.waitForExistence(timeout:120))
        try capture("S19-approval",targets:["primary":confirmation],evidence:"live-codex-tool-confirmation")
        if element("agent.interrupt").exists {tap("agent.interrupt")}
    }
    @MainActor func testCaptureGitOverview() async throws {
        try await launch()
        let repo=app.descendants(matching:.any).matching(NSPredicate(format:"identifier BEGINSWITH 'documentBrowser.github.'")).firstMatch
        XCTAssertTrue(repo.waitForExistence(timeout:15));repo.tap();tap("documentBrowser.localGit")
        XCTAssertTrue(element("gitPanel.branch").waitForExistence(timeout:30))
        try capture("S31-clean",targets:["primary":element("gitPanel.branch")],evidence:"native-github-working-copy")
    }

}
