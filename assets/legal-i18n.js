(function () {
  "use strict";

  const LANGS = [
    { code: "en", label: "English", html: "en" },
    { code: "zh", label: "中文", html: "zh-Hans" },
    { code: "ja", label: "日本語", html: "ja" },
    { code: "ko", label: "한국어", html: "ko" },
    { code: "fr", label: "Français", html: "fr" },
    { code: "it", label: "Italiano", html: "it" },
    { code: "de", label: "Deutsch", html: "de" },
    { code: "ar", label: "العربية", html: "ar" },
    { code: "th", label: "ไทย", html: "th" }
  ];

  const SUPPORTED = new Set(LANGS.map((lang) => lang.code));
  const RTL = new Set(["ar"]);
  const STORAGE_KEY = "vibeit_lang";
  const GEO_ENDPOINT = "https://get.geojs.io/v1/ip/country.json";

  const COUNTRY_TO_LANG = {
    CN: "zh", HK: "zh", MO: "zh", TW: "zh",
    JP: "ja",
    KR: "ko", KP: "ko",
    FR: "fr", MC: "fr", BE: "fr", LU: "fr",
    IT: "it", SM: "it", VA: "it",
    DE: "de", AT: "de", CH: "de", LI: "de",
    SA: "ar", AE: "ar", EG: "ar", QA: "ar", KW: "ar", BH: "ar", OM: "ar", JO: "ar", IQ: "ar", LB: "ar",
    LY: "ar", DZ: "ar", MA: "ar", TN: "ar", YE: "ar", SD: "ar", SY: "ar", PS: "ar", MR: "ar",
    TH: "th"
  };

  const UI = {
    en: {
      home: "Home",
      privacy: "Privacy",
      terms: "Terms",
      support: "Support",
      languageLabel: "Language",
      footerTagline: "Vibeit - native Python IDE for iPadOS, iOS, and macOS.",
      autoNote: "Language is selected from your saved preference, country lookup, or browser language. You can change it here anytime.",
      translationNote: "This translation is provided for convenience. If it differs from the English version, the English version controls.",
      contact: "Contact",
      "c.feature": "Feature suggestion",
      "c.featureDesc": "Something Vibeit should do, or do better.",
      "c.bug": "Problem report",
      "c.bugDesc": "Something isn't working the way it should.",
      "c.title": "Title",
      "c.area": "Area",
      "c.a1": "Notebooks & editor",
      "c.a2": "AI assistant",
      "c.a3": "Remote & SSH",
      "c.a4": "Packages",
      "c.a5": "Lessons",
      "c.a6": "Pricing & account",
      "c.a7": "Other",
      "c.featWhat": "What would you like Vibeit to do?",
      "c.useCase": "Use case",
      "c.optional": "(optional)",
      "c.bugWhat": "What happened?",
      "c.steps": "Steps to reproduce",
      "c.device": "Device and OS version",
      "c.appver": "Vibeit version",
      "c.gh": "Open on GitHub",
      "c.ghHint": "GitHub opens with everything pre-filled — you just press Submit. No GitHub account? Use email.",
      "c.send": "Submit",
      "c.sending": "Submitting…",
      "c.sent": "Sent — thank you!",
      "c.view": "View the issue",
      "c.fail": "Couldn't submit — please try again, or email us below.",
      "c.tooMany": "Too many submissions — try again in a minute.",
      "c.doneBody": "We've received your feedback and will read it soon.",
      "c.close": "Done",
      "c.phTitle": "Brief one-line summary",
      "c.phFeat": "Describe the feature and how it should work…",
      "c.phBug": "What did you do, what did you expect, and what happened instead?"
    },
    zh: {
      home: "首页",
      privacy: "隐私政策",
      terms: "使用条款",
      support: "支持",
      languageLabel: "语言",
      footerTagline: "Vibeit - 适用于 iPadOS、iOS 和 macOS 的原生 Python IDE。",
      autoNote: "页面会优先使用你保存的语言，其次根据 IP 所在国家和浏览器语言自动选择。你可以随时在这里切换。",
      translationNote: "本译文仅为阅读便利提供。如与英文版本不一致，以英文版本为准。",
      contact: "联系我们",
      "c.feature": "功能建议",
      "c.featureDesc": "希望 Vibeit 增加或改进的功能。",
      "c.bug": "问题反馈",
      "c.bugDesc": "某个功能没有按预期工作。",
      "c.title": "标题",
      "c.area": "功能区",
      "c.a1": "笔记本与编辑器",
      "c.a2": "AI 助手",
      "c.a3": "远程与 SSH",
      "c.a4": "软件包",
      "c.a5": "课程",
      "c.a6": "订阅与账户",
      "c.a7": "其他",
      "c.featWhat": "你希望 Vibeit 做什么？",
      "c.useCase": "使用场景",
      "c.optional": "（选填）",
      "c.bugWhat": "发生了什么？",
      "c.steps": "复现步骤",
      "c.device": "设备与系统版本",
      "c.appver": "Vibeit 版本",
      "c.gh": "在 GitHub 打开",
      "c.ghHint": "GitHub 页面会自动填好全部内容，你只需点击提交。没有 GitHub 账号？用邮件。",
      "c.send": "提交",
      "c.sending": "正在提交…",
      "c.sent": "已提交，谢谢！",
      "c.view": "查看 issue",
      "c.fail": "提交失败——请稍后重试，或用下方邮件联系我们。",
      "c.tooMany": "提交太频繁——请一分钟后再试。",
      "c.doneBody": "我们已收到你的反馈，会尽快查看。",
      "c.close": "完成",
      "c.phTitle": "一句话简述",
      "c.phFeat": "描述这个功能以及它应该如何工作…",
      "c.phBug": "你做了什么、期望什么、实际发生了什么？"
    },
    ja: {
      home: "ホーム",
      privacy: "プライバシー",
      terms: "利用規約",
      support: "サポート",
      languageLabel: "言語",
      footerTagline: "Vibeit - iPadOS、iOS、macOS 向けのネイティブ Python IDE。",
      autoNote: "保存済みの設定、IP による国判定、ブラウザ言語の順で言語を選びます。ここでいつでも変更できます。",
      translationNote: "この翻訳は便宜のために提供されています。英語版と相違がある場合は英語版が優先されます。",
      contact: "お問い合わせ",
      "c.feature": "機能のご提案",
      "c.featureDesc": "Vibeit に欲しい機能や改善点。",
      "c.bug": "問題の報告",
      "c.bugDesc": "期待どおりに動かないことがある。",
      "c.title": "タイトル",
      "c.area": "機能エリア",
      "c.a1": "ノートブックとエディタ",
      "c.a2": "AI アシスタント",
      "c.a3": "リモートと SSH",
      "c.a4": "パッケージ",
      "c.a5": "レッスン",
      "c.a6": "料金とアカウント",
      "c.a7": "その他",
      "c.featWhat": "Vibeit に何をしてほしいですか？",
      "c.useCase": "ユースケース",
      "c.optional": "（任意）",
      "c.bugWhat": "何が起きましたか？",
      "c.steps": "再現手順",
      "c.device": "デバイスと OS バージョン",
      "c.appver": "Vibeit のバージョン",
      "c.gh": "GitHub で開く",
      "c.ghHint": "GitHub にすべて入力済みで開きます。送信を押すだけ。アカウントがなければメールで。",
      "c.send": "送信",
      "c.sending": "送信中…",
      "c.sent": "送信しました。ありがとうございます！",
      "c.view": "Issue を見る",
      "c.fail": "送信できませんでした。時間をおいて再試行するか、下のメールをご利用ください。",
      "c.tooMany": "送信が多すぎます。1分後にもう一度お試しください。",
      "c.doneBody": "フィードバックを受け取りました。近いうちに確認します。",
      "c.close": "完了",
      "c.phTitle": "一行での簡単な説明",
      "c.phFeat": "機能の内容と希望する動作を書いてください…",
      "c.phBug": "何をして、何を期待し、実際はどうなりましたか？"
    },
    ko: {
      home: "홈",
      privacy: "개인정보",
      terms: "이용 약관",
      support: "지원",
      languageLabel: "언어",
      footerTagline: "Vibeit - iPadOS, iOS, macOS용 네이티브 Python IDE.",
      autoNote: "저장된 설정, IP 기반 국가 조회, 브라우저 언어 순서로 언어를 선택합니다. 언제든 여기에서 바꿀 수 있습니다.",
      translationNote: "이 번역은 편의를 위해 제공됩니다. 영어 버전과 다를 경우 영어 버전이 우선합니다.",
      contact: "문의하기",
      "c.feature": "기능 제안",
      "c.featureDesc": "Vibeit에 바라는 기능이나 개선점.",
      "c.bug": "문제 신고",
      "c.bugDesc": "무언가 기대대로 작동하지 않아요.",
      "c.title": "제목",
      "c.area": "기능 영역",
      "c.a1": "노트북과 편집기",
      "c.a2": "AI 어시스턴트",
      "c.a3": "원격 및 SSH",
      "c.a4": "패키지",
      "c.a5": "레슨",
      "c.a6": "요금제 및 계정",
      "c.a7": "기타",
      "c.featWhat": "Vibeit이 무엇을 하길 바라나요?",
      "c.useCase": "사용 사례",
      "c.optional": "(선택)",
      "c.bugWhat": "무슨 일이 있었나요?",
      "c.steps": "재현 단계",
      "c.device": "기기 및 OS 버전",
      "c.appver": "Vibeit 버전",
      "c.gh": "GitHub에서 열기",
      "c.ghHint": "GitHub이 모든 내용이 채워진 채 열립니다. 제출만 누르면 돼요. 계정이 없다면 이메일로.",
      "c.send": "제출",
      "c.sending": "제출 중…",
      "c.sent": "제출되었습니다. 감사합니다!",
      "c.view": "Issue 보기",
      "c.fail": "제출하지 못했습니다. 잠시 후 다시 시도하거나 아래 이메일을 이용해 주세요.",
      "c.tooMany": "제출이 너무 잦습니다. 1분 후 다시 시도해 주세요.",
      "c.doneBody": "피드백을 받았습니다. 곧 확인하겠습니다.",
      "c.close": "완료",
      "c.phTitle": "한 줄 요약",
      "c.phFeat": "원하는 기능과 동작 방식을 설명해 주세요…",
      "c.phBug": "무엇을 했고, 무엇을 기대했고, 실제로는 어땠나요?"
    },
    fr: {
      home: "Accueil",
      privacy: "Confidentialité",
      terms: "Conditions",
      support: "Assistance",
      languageLabel: "Langue",
      footerTagline: "Vibeit - IDE Python natif pour iPadOS, iOS et macOS.",
      autoNote: "La langue est choisie selon votre préférence enregistrée, une détection du pays par IP, puis la langue du navigateur. Vous pouvez la changer ici.",
      translationNote: "Cette traduction est fournie pour votre confort. En cas de différence avec la version anglaise, la version anglaise prévaut.",
      contact: "Contact",
      "c.feature": "Suggestion de fonctionnalité",
      "c.featureDesc": "Ce que Vibeit devrait faire, ou faire mieux.",
      "c.bug": "Signaler un problème",
      "c.bugDesc": "Quelque chose ne fonctionne pas comme prévu.",
      "c.title": "Titre",
      "c.area": "Domaine",
      "c.a1": "Notebooks et éditeur",
      "c.a2": "Assistant IA",
      "c.a3": "Distant et SSH",
      "c.a4": "Paquets",
      "c.a5": "Leçons",
      "c.a6": "Tarifs et compte",
      "c.a7": "Autre",
      "c.featWhat": "Que voudriez-vous que Vibeit fasse ?",
      "c.useCase": "Cas d'usage",
      "c.optional": "(facultatif)",
      "c.bugWhat": "Que s'est-il passé ?",
      "c.steps": "Étapes pour reproduire",
      "c.device": "Appareil et version d'OS",
      "c.appver": "Version de Vibeit",
      "c.gh": "Ouvrir sur GitHub",
      "c.ghHint": "GitHub s'ouvre avec tout pré-rempli — il ne reste qu'à valider. Pas de compte GitHub ? Utilisez l'e-mail.",
      "c.send": "Envoyer",
      "c.sending": "Envoi…",
      "c.sent": "Envoyé — merci !",
      "c.view": "Voir l'issue",
      "c.fail": "Échec de l'envoi — réessayez ou utilisez l'e-mail ci-dessous.",
      "c.tooMany": "Trop d'envois — réessayez dans une minute.",
      "c.doneBody": "Nous avons bien reçu votre retour et le lirons bientôt.",
      "c.close": "OK",
      "c.phTitle": "Résumé en une ligne",
      "c.phFeat": "Décrivez la fonctionnalité et son fonctionnement…",
      "c.phBug": "Qu'avez-vous fait, qu'attendiez-vous, que s'est-il passé ?"
    },
    it: {
      home: "Home",
      privacy: "Privacy",
      terms: "Termini",
      support: "Assistenza",
      languageLabel: "Lingua",
      footerTagline: "Vibeit - IDE Python nativo per iPadOS, iOS e macOS.",
      autoNote: "La lingua viene scelta dalla preferenza salvata, dal paese rilevato tramite IP o dalla lingua del browser. Puoi cambiarla qui.",
      translationNote: "Questa traduzione è fornita per comodità. In caso di differenze, prevale la versione inglese.",
      contact: "Contatti",
      "c.feature": "Suggerimento di funzionalità",
      "c.featureDesc": "Qualcosa che Vibeit dovrebbe fare, o fare meglio.",
      "c.bug": "Segnala un problema",
      "c.bugDesc": "Qualcosa non funziona come dovrebbe.",
      "c.title": "Titolo",
      "c.area": "Area",
      "c.a1": "Notebook ed editor",
      "c.a2": "Assistente IA",
      "c.a3": "Remoto e SSH",
      "c.a4": "Pacchetti",
      "c.a5": "Lezioni",
      "c.a6": "Prezzi e account",
      "c.a7": "Altro",
      "c.featWhat": "Cosa vorresti che Vibeit facesse?",
      "c.useCase": "Caso d'uso",
      "c.optional": "(facoltativo)",
      "c.bugWhat": "Cosa è successo?",
      "c.steps": "Passaggi per riprodurre",
      "c.device": "Dispositivo e versione OS",
      "c.appver": "Versione di Vibeit",
      "c.gh": "Apri su GitHub",
      "c.ghHint": "GitHub si apre con tutto precompilato — basta premere Invia. Niente account GitHub? Usa l'e-mail.",
      "c.send": "Invia",
      "c.sending": "Invio…",
      "c.sent": "Inviato — grazie!",
      "c.view": "Vedi l'issue",
      "c.fail": "Invio non riuscito — riprova o usa l'e-mail qui sotto.",
      "c.tooMany": "Troppi invii — riprova tra un minuto.",
      "c.doneBody": "Abbiamo ricevuto il tuo feedback e lo leggeremo presto.",
      "c.close": "Fine",
      "c.phTitle": "Riassunto in una riga",
      "c.phFeat": "Descrivi la funzionalità e come dovrebbe funzionare…",
      "c.phBug": "Cosa hai fatto, cosa ti aspettavi e cosa è successo?"
    },
    de: {
      home: "Start",
      privacy: "Datenschutz",
      terms: "AGB",
      support: "Support",
      languageLabel: "Sprache",
      footerTagline: "Vibeit - native Python-IDE für iPadOS, iOS und macOS.",
      autoNote: "Die Sprache wird aus deiner gespeicherten Auswahl, einer IP-Länderabfrage oder der Browsersprache gewählt. Du kannst sie hier jederzeit ändern.",
      translationNote: "Diese Übersetzung dient nur der besseren Lesbarkeit. Bei Abweichungen gilt die englische Fassung.",
      contact: "Kontakt",
      "c.feature": "Funktionswunsch",
      "c.featureDesc": "Was Vibeit können sollte — oder besser machen sollte.",
      "c.bug": "Problem melden",
      "c.bugDesc": "Etwas funktioniert nicht wie erwartet.",
      "c.title": "Titel",
      "c.area": "Bereich",
      "c.a1": "Notebooks und Editor",
      "c.a2": "KI-Assistent",
      "c.a3": "Remote und SSH",
      "c.a4": "Pakete",
      "c.a5": "Lektionen",
      "c.a6": "Preise und Konto",
      "c.a7": "Sonstiges",
      "c.featWhat": "Was soll Vibeit können?",
      "c.useCase": "Anwendungsfall",
      "c.optional": "(optional)",
      "c.bugWhat": "Was ist passiert?",
      "c.steps": "Schritte zum Reproduzieren",
      "c.device": "Gerät und OS-Version",
      "c.appver": "Vibeit-Version",
      "c.gh": "Auf GitHub öffnen",
      "c.ghHint": "GitHub öffnet sich mit allem vorausgefüllt — nur noch absenden. Kein GitHub-Konto? Nimm die E-Mail.",
      "c.send": "Absenden",
      "c.sending": "Wird gesendet…",
      "c.sent": "Gesendet — danke!",
      "c.view": "Issue ansehen",
      "c.fail": "Senden fehlgeschlagen — versuch es erneut oder nutze die E-Mail unten.",
      "c.tooMany": "Zu viele Einsendungen — versuch es in einer Minute erneut.",
      "c.doneBody": "Wir haben dein Feedback erhalten und lesen es bald.",
      "c.close": "Fertig",
      "c.phTitle": "Kurze Zusammenfassung in einer Zeile",
      "c.phFeat": "Beschreibe die Funktion und wie sie arbeiten soll …",
      "c.phBug": "Was hast du getan, was hast du erwartet, was ist passiert?"
    },
    ar: {
      home: "الرئيسية",
      privacy: "الخصوصية",
      terms: "الشروط",
      support: "الدعم",
      languageLabel: "اللغة",
      footerTagline: "Vibeit - بيئة تطوير بايثون أصلية لـ iPadOS و iOS و macOS.",
      autoNote: "تُختار اللغة من تفضيلك المحفوظ، ثم من بلدك حسب عنوان IP، ثم من لغة المتصفح. يمكنك تغييرها من هنا في أي وقت.",
      translationNote: "هذه الترجمة مقدَّمة لتسهيل القراءة. إذا اختلفت عن النسخة الإنجليزية، فالنسخة الإنجليزية هي المُعتمَدة.",
      contact: "اتصل بنا",
      "c.feature": "اقتراح ميزة",
      "c.featureDesc": "شيء ينبغي لـ Vibeit أن يفعله، أو يفعله بشكل أفضل.",
      "c.bug": "الإبلاغ عن مشكلة",
      "c.bugDesc": "شيء لا يعمل كما ينبغي.",
      "c.title": "العنوان",
      "c.area": "المنطقة الوظيفية",
      "c.a1": "الدفاتر والمحرّر",
      "c.a2": "مساعد الذكاء الاصطناعي",
      "c.a3": "عن بُعد و SSH",
      "c.a4": "الحزم",
      "c.a5": "الدروس",
      "c.a6": "الأسعار والحساب",
      "c.a7": "أخرى",
      "c.featWhat": "ماذا تريد من Vibeit أن يفعل؟",
      "c.useCase": "حالة الاستخدام",
      "c.optional": "(اختياري)",
      "c.bugWhat": "ماذا حدث؟",
      "c.steps": "خطوات إعادة الإنتاج",
      "c.device": "الجهاز وإصدار النظام",
      "c.appver": "إصدار Vibeit",
      "c.gh": "افتح على GitHub",
      "c.ghHint": "يفتح GitHub وكل شيء معبّأ مسبقًا — يكفي الضغط على إرسال. لا تملك حساب GitHub؟ استخدم البريد.",
      "c.send": "إرسال",
      "c.sending": "جارٍ الإرسال…",
      "c.sent": "تم الإرسال — شكرًا لك!",
      "c.view": "عرض الـ issue",
      "c.fail": "تعذّر الإرسال — حاول مجددًا أو استخدم البريد أدناه.",
      "c.tooMany": "محاولات كثيرة — حاول مرة أخرى بعد دقيقة.",
      "c.doneBody": "لقد استلمنا ملاحظاتك وسنطّلع عليها قريبًا.",
      "c.close": "تم",
      "c.phTitle": "ملخّص من سطر واحد",
      "c.phFeat": "صِف الميزة وكيف ينبغي أن تعمل…",
      "c.phBug": "ماذا فعلت، وماذا توقّعت، وماذا حدث فعلًا؟"
    },
    th: {
      home: "หน้าแรก",
      privacy: "ความเป็นส่วนตัว",
      terms: "ข้อกำหนด",
      support: "ฝ่ายสนับสนุน",
      languageLabel: "ภาษา",
      footerTagline: "Vibeit - Python IDE แบบเนทีฟสำหรับ iPadOS, iOS และ macOS",
      autoNote: "ระบบเลือกภาษาจากค่าที่คุณบันทึกไว้ ถัดมาคือประเทศตามหมายเลข IP แล้วจึงเป็นภาษาของเบราว์เซอร์ คุณเปลี่ยนได้ที่นี่ทุกเมื่อ",
      translationNote: "คำแปลนี้จัดทำขึ้นเพื่อความสะดวกในการอ่าน หากข้อความใดต่างจากฉบับภาษาอังกฤษ ให้ยึดฉบับภาษาอังกฤษเป็นหลัก",
      contact: "ติดต่อเรา",
      "c.feature": "เสนอฟีเจอร์",
      "c.featureDesc": "สิ่งที่อยากให้ Vibeit ทำได้ หรือทำได้ดีขึ้น",
      "c.bug": "แจ้งปัญหา",
      "c.bugDesc": "มีบางอย่างทำงานไม่ถูกต้อง",
      "c.title": "หัวข้อ",
      "c.area": "ส่วนของแอป",
      "c.a1": "โน้ตบุ๊กและตัวแก้ไข",
      "c.a2": "ผู้ช่วย AI",
      "c.a3": "รีโมตและ SSH",
      "c.a4": "แพ็กเกจ",
      "c.a5": "บทเรียน",
      "c.a6": "ราคาและบัญชี",
      "c.a7": "อื่น ๆ",
      "c.featWhat": "อยากให้ Vibeit ทำอะไร?",
      "c.useCase": "กรณีการใช้งาน",
      "c.optional": "(ไม่บังคับ)",
      "c.bugWhat": "เกิดอะไรขึ้น?",
      "c.steps": "ขั้นตอนการทำซ้ำ",
      "c.device": "อุปกรณ์และเวอร์ชัน OS",
      "c.appver": "เวอร์ชัน Vibeit",
      "c.gh": "เปิดใน GitHub",
      "c.ghHint": "GitHub จะเปิดพร้อมข้อมูลที่กรอกให้แล้ว แค่กดส่ง ไม่มีบัญชี GitHub? ใช้อีเมลได้",
      "c.send": "ส่ง",
      "c.sending": "กำลังส่ง…",
      "c.sent": "ส่งแล้ว ขอบคุณ!",
      "c.view": "ดู issue",
      "c.fail": "ส่งไม่สำเร็จ ลองใหม่หรือใช้อีเมลด้านล่าง",
      "c.tooMany": "ส่งบ่อยเกินไป ลองใหม่ในอีกหนึ่งนาที",
      "c.doneBody": "เราได้รับความคิดเห็นของคุณแล้ว และจะอ่านโดยเร็ว",
      "c.close": "เสร็จสิ้น",
      "c.phTitle": "สรุปสั้น ๆ หนึ่งบรรทัด",
      "c.phFeat": "อธิบายฟีเจอร์และการทำงานที่ต้องการ…",
      "c.phBug": "คุณทำอะไร คาดหวังอะไร แล้วเกิดอะไรขึ้นแทน?"
    }
  };

  const PAGES = {
    en: {
      privacy: {
        title: "Privacy Policy",
        description: "Privacy Policy for Vibeit, the native Python IDE for iPadOS, iOS, and macOS.",
        body: `
          <h1>Privacy Policy</h1>
          <p class="updated">Last updated: July 6, 2026</p>
          <p>This Privacy Policy explains how <strong>Vibeit</strong> ("Vibeit", "the app", "we", "us") handles information when you use the Vibeit app on iPadOS, iOS, and macOS. Vibeit is a native Python notebook IDE designed to run on your device. We built it to be private by default: your code runs in an on-device Python kernel, and your files, credentials, and API keys stay on your device.</p>
          <div class="tldr"><strong>The short version.</strong> We do not operate analytics or advertising servers, and the app contains no third-party tracking or advertising SDKs. We do not sell your personal information. Data leaves your device only when <em>you</em> use a feature that requires it, such as calling an AI provider with your own key, connecting to a remote server you configured, or downloading a package.</div>

          <section class="legal-section"><h2>1. Information stored on your device</h2>
          <p>The following stay on your device, and in your own iCloud or Files storage if you choose to save there. We do not receive copies of them:</p>
          <ul>
            <li><strong>Notebooks, scripts, and workspace files</strong> you create or open.</li>
            <li><strong>Python execution</strong>: code runs in a local kernel; your code and output are not sent to us.</li>
            <li><strong>Credentials and secrets</strong>: API keys, SSH passwords, key passphrases, and Cloudflare Access tokens are stored in the device <strong>Keychain</strong> and are never written into notebooks, logs, or transmitted to us.</li>
            <li><strong>App settings</strong>, such as theme, language, and host profiles.</li>
          </ul></section>

          <section class="legal-section"><h2>2. Website language detection</h2>
          <p>These web pages may request a country lookup from GeoJS to choose the initial display language from your IP location. The lookup returns a country code and is used only in your browser for language selection. If it fails, the page falls back to your browser language and then English. You can change the language manually; your choice is stored in localStorage on this device.</p></section>

          <section class="legal-section"><h2>3. Features that send data to third parties</h2>
          <p>When you choose to use these features, data is sent to the relevant third party under <em>their</em> privacy policies. Vibeit acts only as the client.</p>
          <h3>AI assistance</h3><p>If you enable AI features and use a cloud AI provider, such as OpenAI or Anthropic, the prompts you send and the relevant code or context are transmitted to that provider using the API key or sign-in you supplied. Apple Intelligence or on-device foundation models, where used, run on your device. We do not receive your prompts or completions.</p>
          <h3>Remote connections</h3><p>If you configure a remote host, Vibeit connects directly to the server <em>you</em> specify to run commands, transfer files, or run Python. For hosts reached through Cloudflare Access, a sign-in window authenticates with your identity provider and stores the resulting access token in the Keychain. We do not operate these servers and do not receive your remote session contents.</p>
          <h3>Package downloads</h3><p>Managed packages are fetched over HTTPS from public package indexes, including this GitHub-hosted registry. As with any web request, the hosting provider may process your IP address and request metadata to deliver the files.</p></section>

          <section class="legal-section"><h2>4. Subscriptions and payments</h2>
          <p>Vibeit subscriptions are sold through <strong>Apple In-App Purchase</strong>. Apple processes your payment and manages your subscription; we never receive or store your payment card details. The app receives only your subscription or entitlement status from Apple via StoreKit to unlock features. Manage or cancel your subscription anytime in your Apple Account settings.</p></section>
          <section class="legal-section"><h2>5. Information we collect</h2><p>We do not maintain user accounts and do not run a backend that collects your personal information. The app does not include third-party analytics or advertising. If you contact us for support by email, we receive the information you choose to include in your message.</p></section>
          <section class="legal-section"><h2>6. Data security</h2><p>Secrets are stored using the operating system Keychain. Network connections use TLS or SSH encryption. No method of storage or transmission is 100% secure, but we rely on Apple platform protections and encrypted transport to safeguard your information.</p></section>
          <section class="legal-section"><h2>7. Data retention and deletion</h2><p>Because your data lives on your device, you control it. You can delete files, hosts, and credentials in the app, and removing the app deletes its local data and Keychain items associated with it. Data already sent to a third party is governed by that party's policies.</p></section>
          <section class="legal-section"><h2>8. Children's privacy</h2><p>Vibeit is a developer tool and is not directed to children under 13 or the equivalent minimum age in your jurisdiction. We do not knowingly collect personal information from children.</p></section>
          <section class="legal-section"><h2>9. International users and your rights</h2><p>Depending on where you live, for example under the EU GDPR or California CCPA/CPRA, you may have rights to access, correct, delete, or restrict processing of your personal information. Because we do not collect or store your personal information on our own servers, most requests are fulfilled directly on your device or with the relevant third-party provider. You can also contact us using the details below.</p></section>
          <section class="legal-section"><h2>10. Changes to this policy</h2><p>We may update this Privacy Policy from time to time. We will revise the "Last updated" date above and, for material changes, provide notice as appropriate. Continued use of the app after an update constitutes acceptance of the revised policy.</p></section>
          <section class="legal-section"><h2>11. Contact</h2><p>Questions about this policy or your privacy? Contact us at <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>.</p></section>`
      },
      support: {
        title: "Support",
        description: "Support and help for Vibeit, the native Python IDE for iPadOS, iOS, and macOS.",
        body: `
          <h1>Support</h1>
          <p class="updated">Vibeit - native Python IDE for iPadOS, iOS, and macOS.</p>
          <div class="tldr"><strong>Need a hand?</strong> Email us at <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> and we'll get back to you. We usually reply within 1-2 business days.</div>
          <p><a class="contact-btn" href="mailto:aroluo@icloud.com?subject=Vibeit%20Support">Contact Support</a></p>
          <section class="legal-section"><h2>Getting started</h2><p>Vibeit is a full Python IDE that runs on your device. Create a notebook or script, write Python, and press Run. Code executes in an on-device kernel with support for notebooks, matplotlib, NumPy, pandas, PyTorch, and more. No internet connection is required to run your code.</p></section>
          <section class="legal-section"><h2>Frequently asked questions</h2>
          <h3>What's included in the free version vs. a subscription?</h3><p>The core on-device Python IDE is available with the <strong>Standard</strong> plan. <strong>Pro</strong> adds remote SSH/SFTP servers and terminal, GitHub clone, push, pull and pull requests, and cloud AI providers. Every plan starts with a <strong>7-day free trial</strong>.</p>
          <h3>How do I start the free trial or subscribe?</h3><p>Open <strong>Settings -> Account</strong> in the app, choose a plan, and tap <strong>Start Free Trial</strong>. Payment is handled by Apple through your Apple Account.</p>
          <h3>How do I manage or cancel my subscription?</h3><p>Subscriptions are managed by Apple. On your device, open the <strong>Settings</strong> app, tap your name, open <strong>Subscriptions</strong>, then choose <strong>Vibeit</strong>. You can also <a href="https://apps.apple.com/account/subscriptions">manage subscriptions here</a>.</p>
          <h3>How do I restore a purchase?</h3><p>On a new device or after reinstalling, open <strong>Settings -> Account</strong> in Vibeit and tap <strong>Restore Purchases</strong>. Make sure you are signed in with the same Apple Account you used to subscribe.</p>
          <h3>How do I connect a remote server or GitHub?</h3><p>Go to <strong>Settings -> Remote</strong> to add an SSH/SFTP host, or <strong>Settings -> Source Control</strong> to connect GitHub. Credentials are stored in the device Keychain and are never sent to us.</p>
          <h3>How do I use my own AI provider?</h3><p>Open <strong>Settings -> AI</strong> and add your provider and API key. Your key stays on your device and is used only to talk directly to that provider.</p>
          <h3>Where can I install additional Python packages?</h3><p>Use the in-app package catalog to install supported pure-Python and prebuilt native packages. Availability depends on what can run on iOS and iPadOS.</p></section>
          <section class="legal-section"><h2>Privacy and data</h2><p>Vibeit is private by default: your code, files, and credentials stay on your device. See our <a href="privacy.html">Privacy Policy</a> for details.</p></section>
          <section class="legal-section"><h2>Contact</h2><p>Still stuck, found a bug, or have a feature request? Email <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> with your device model and iOS/iPadOS version and we'll help.</p></section>`
      },
      terms: {
        title: "Terms of Use",
        description: "Terms of Use for Vibeit, the native Python IDE for iPadOS, iOS, and macOS.",
        body: `
          <h1>Terms of Use</h1>
          <p class="updated">Last updated: July 6, 2026</p>
          <p>These Terms of Use ("Terms") are a legal agreement between you and the developer of <strong>Vibeit</strong> ("Vibeit", "the app", "we", "us", "our") governing your download and use of the Vibeit application on iPadOS, iOS, and macOS. By downloading, installing, or using Vibeit, you agree to these Terms. If you do not agree, do not use the app.</p>
          <div class="tldr"><strong>The short version.</strong> Vibeit is a developer tool that runs Python and optional AI and network features on your device and through services <em>you</em> connect. You are responsible for your own code, data, credentials, and for how you use those features. The app is provided "as is"; AI output and executed code can be wrong or insecure, so review before you rely on them.</div>
          <section class="legal-section"><h2>1. Eligibility and acceptance</h2><p>You must be at least 13 years old, or the minimum age of digital consent in your jurisdiction, and able to form a binding contract to use Vibeit. If you use the app on behalf of an organization, you represent that you are authorized to accept these Terms for it. Your use is also subject to Apple's <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Licensed Application End User License Agreement (EULA)</a>; where these Terms and Apple's EULA conflict, Apple's EULA controls with respect to your App Store license.</p></section>
          <section class="legal-section"><h2>2. What Vibeit is</h2><p>Vibeit is a native Python notebook and script IDE that executes code in an on-device Python runtime. Optional features include AI assistance through providers you configure, SSH/SFTP remote connections, Cloudflare Access, source control and GitHub integration, and Python package downloads. These services are operated by you or by third parties, not by us.</p></section>
          <section class="legal-section"><h2>3. License</h2><p>Subject to these Terms and Apple's EULA, we grant you a personal, limited, non-exclusive, non-transferable, revocable license to use Vibeit on Apple-branded devices that you own or control for lawful personal or internal business use. You may not copy, modify, reverse engineer, decompile, sublicense, sell, or distribute the app except as allowed by applicable law.</p></section>
          <section class="legal-section"><h2>4. Your responsibilities and acceptable use</h2><p>You are solely responsible for the code you write or run, the data you process, the credentials you enter, and the systems you connect to. You agree not to use Vibeit to violate laws, infringe rights, access systems without authorization, develop or distribute malware, conduct abusive activity, disclose data you are not allowed to disclose, or bypass security, usage, or rate limits. You are responsible for device security, API keys, SSH credentials, source control tokens, and backups.</p></section>
          <section class="legal-section"><h2>5. Third-party services</h2><p>When you enable a feature that connects to a third party, such as an AI provider, remote host, Cloudflare Access, GitHub, or package index, your use is governed by that party's terms and privacy policy. You are responsible for any fees they charge. We do not operate or control those services and are not responsible for their availability, content, security, actions, or charges.</p></section>
          <section class="legal-section"><h2>6. AI features and generated output</h2><p>AI features may produce code, explanations, or other content that is inaccurate, incomplete, insecure, biased, or unsuitable. AI output is not professional, legal, financial, medical, or security advice. You are responsible for reviewing, testing, and validating AI-generated or app-suggested content before relying on, executing, publishing, or shipping it.</p></section>
          <section class="legal-section"><h2>7. Code execution, remote commands, and data</h2><p>Vibeit runs code and shell commands that you or, at your direction, an AI agent provide. Executing code or remote commands can modify or delete files, consume resources, or affect systems you connect to. You accept these risks and are responsible for the outcomes. You retain ownership of your code, notebooks, and data.</p></section>
          <section class="legal-section"><h2>8. Security and data-loss disclaimer</h2><p>We design Vibeit to be private by default and use protections such as the Keychain and encrypted transport. However, no software, storage, or transmission method is completely secure, and we do not warrant that the app will be error-free, uninterrupted, free from vulnerabilities, or free from data loss or unauthorized access.</p></section>
          <section class="legal-section"><h2>9. Subscriptions and payments</h2><p>Some features may require a paid subscription sold through <strong>Apple In-App Purchase</strong>. Payment is charged to your Apple Account and subscriptions renew automatically unless canceled before the renewal deadline. You can manage or cancel your subscription in your Apple Account settings. Apple processes payments and refunds under Apple's terms.</p></section>
          <section class="legal-section"><h2 class="legal">10. Disclaimer of warranties</h2><p class="legal">The app is provided "as is" and "as available", without warranties of any kind, whether express, implied, or statutory, including implied warranties of merchantability, fitness for a particular purpose, title, accuracy, and non-infringement. Some jurisdictions do not allow the exclusion of certain warranties, so some exclusions may not apply to you.</p></section>
          <section class="legal-section"><h2 class="legal">11. Limitation of liability</h2><p class="legal">To the maximum extent permitted by law, we will not be liable for indirect, incidental, special, consequential, exemplary, or punitive damages, or for loss of profits, revenue, data, goodwill, or other intangible losses arising from your use of or inability to use the app, AI output, executed code or commands, data loss, security incidents, or third-party services. Our total liability for all claims relating to the app will not exceed the greater of the amount you paid us for the app in the twelve months before the claim or US$10.</p></section>
          <section class="legal-section"><h2>12. Indemnification</h2><p>To the extent permitted by law, you agree to indemnify and hold us harmless from claims, damages, liabilities, and expenses arising out of your misuse of the app, violation of these Terms or any law, your code, data, content, or your use of any connected third-party service or system.</p></section>
          <section class="legal-section"><h2>13. Termination</h2><p>You may stop using the app at any time by deleting it. We may suspend or terminate your license if you materially breach these Terms or use the app unlawfully. Sections that by their nature should survive termination will survive.</p></section>
          <section class="legal-section"><h2>14. Apple App Store terms</h2><p>These Terms are between you and us only, not with Apple. Apple is not responsible for the app or its content and has no obligation to provide maintenance or support. Apple and its subsidiaries are third-party beneficiaries of these Terms and may enforce them against you. You represent that you are not in a country subject to a U.S. Government embargo or on a U.S. Government restricted-party list.</p></section>
          <section class="legal-section"><h2>15. Governing law</h2><p>These Terms are governed by the laws of the jurisdiction in which the developer is established, except where mandatory consumer-protection laws of your place of residence provide otherwise. Nothing in these Terms limits non-waivable statutory rights you may have as a consumer.</p></section>
          <section class="legal-section"><h2>16. Changes to these Terms</h2><p>We may update these Terms from time to time. We will revise the "Last updated" date above and, for material changes, provide notice as appropriate. Continued use after an update constitutes acceptance of the revised Terms.</p></section>
          <section class="legal-section"><h2>17. Contact</h2><p>Questions about these Terms? Contact us at <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>.</p></section>`
      },
      contact: {
        title: "Contact",
        description: "Contact Vibeit: send a feature suggestion or report a problem.",
        body: `
          <h1>Contact us</h1>
          <p class="updated">Send a feature idea or report a problem — we read every message.</p>`
      }
    },

    zh: {
      privacy: {
        title: "隐私政策",
        description: "Vibeit 隐私政策，适用于 iPadOS、iOS 和 macOS 的原生 Python IDE。",
        body: `
          <h1>隐私政策</h1>
          <p class="updated">最后更新：2026 年 7 月 6 日</p>
          <p>本隐私政策说明 <strong>Vibeit</strong>（“Vibeit”“本 app”“我们”）在你使用 iPadOS、iOS 和 macOS 上的 Vibeit app 时如何处理信息。Vibeit 是在设备本地运行的原生 Python 笔记本 IDE。我们的默认设计是保护隐私：代码在设备端 Python 内核运行，文件、凭据和 API 密钥保留在你的设备上。</p>
          <div class="tldr"><strong>简短版。</strong>我们不运营分析或广告服务器，app 不包含第三方追踪或广告 SDK。我们不会出售你的个人信息。只有当你主动使用需要联网的功能时，数据才会离开设备，例如使用自己的密钥调用 AI 服务商、连接你配置的远程服务器，或下载软件包。</div>
          <section class="legal-section"><h2>1. 存储在你设备上的信息</h2><p>以下内容保留在你的设备上；如果你选择保存到 iCloud 或“文件”，也会进入你自己的存储空间。我们不会收到这些内容的副本：</p><ul><li><strong>你创建或打开的笔记本、脚本和工作区文件</strong>。</li><li><strong>Python 执行内容</strong>：代码在本地内核运行；代码和输出不会发送给我们。</li><li><strong>凭据和密钥</strong>：API 密钥、SSH 密码、密钥口令和 Cloudflare Access 令牌存储在设备<strong>钥匙串</strong>中，不会写入笔记本、日志，也不会传输给我们。</li><li><strong>App 设置</strong>，例如主题、语言和主机配置。</li></ul></section>
          <section class="legal-section"><h2>2. 网站语言自动选择</h2><p>这些网页可能会向 GeoJS 请求一次国家码查询，以便根据你的 IP 所在国家选择初始显示语言。该查询返回国家码，只在你的浏览器中用于语言选择。若查询失败，页面会回退到浏览器语言，再回退到英文。你可以手动切换语言；选择会保存在本设备的 localStorage 中。</p></section>
          <section class="legal-section"><h2>3. 会向第三方发送数据的功能</h2><p>当你主动使用以下功能时，相关数据会发送给对应第三方，并受其隐私政策约束。Vibeit 只是客户端。</p><h3>AI 辅助</h3><p>如果你启用 AI 功能并使用云端 AI 服务商，例如 OpenAI 或 Anthropic，你发送的提示词以及相关代码或上下文会使用你提供的 API 密钥或登录信息传输给该服务商。Apple Intelligence 或设备端基础模型（如使用）在设备本地运行。我们不会收到你的提示词或输出。</p><h3>远程连接</h3><p>如果你配置远程主机，Vibeit 会直接连接到你指定的服务器以运行命令、传输文件或运行 Python。通过 Cloudflare Access 访问的主机会在登录窗口中向你的身份提供商认证，并把访问令牌保存在钥匙串。我们不运营这些服务器，也不会收到远程会话内容。</p><h3>软件下载</h3><p>托管软件包会通过 HTTPS 从公共软件包索引下载，包括这个由 GitHub 托管的注册表。和任何网页请求一样，托管服务商可能会处理你的 IP 地址和请求元数据以交付文件。</p></section>
          <section class="legal-section"><h2>4. 订阅和付款</h2><p>Vibeit 订阅通过 <strong>Apple App 内购买</strong>销售。Apple 处理付款并管理订阅；我们不会接收或保存你的银行卡信息。App 只通过 StoreKit 从 Apple 接收订阅或权益状态，用于解锁功能。你可以随时在 Apple 账户设置中管理或取消订阅。</p></section>
          <section class="legal-section"><h2>5. 我们收集的信息</h2><p>我们不维护用户账户，也不运行收集个人信息的后端。App 不包含第三方分析或广告。如果你通过电子邮件联系我们寻求支持，我们会收到你选择写入邮件的信息。</p></section>
          <section class="legal-section"><h2>6. 数据安全</h2><p>密钥使用操作系统钥匙串保存。网络连接使用 TLS 或 SSH 加密。任何存储或传输方式都不可能 100% 安全，但我们依赖 Apple 平台保护和加密传输来保护你的信息。</p></section>
          <section class="legal-section"><h2>7. 数据保留和删除</h2><p>由于数据位于你的设备上，你可以控制它。你可以在 app 中删除文件、主机和凭据；删除 app 会移除其本地数据以及关联的钥匙串项目。已经发送给第三方的数据受该第三方政策约束。</p></section>
          <section class="legal-section"><h2>8. 儿童隐私</h2><p>Vibeit 是开发工具，并非面向 13 岁以下儿童或你所在地区规定的相应最低年龄儿童。我们不会有意收集儿童个人信息。</p></section>
          <section class="legal-section"><h2>9. 国际用户和你的权利</h2><p>根据你的居住地，例如欧盟 GDPR 或加州 CCPA/CPRA，你可能拥有访问、更正、删除或限制处理个人信息的权利。由于我们不在自己的服务器上收集或保存你的个人信息，大多数请求可直接在设备上或通过相关第三方服务商完成。你也可以使用下方联系方式联系我们。</p></section>
          <section class="legal-section"><h2>10. 本政策变更</h2><p>我们可能会不时更新本隐私政策。我们会修改上方“最后更新”日期；如有重大变更，会酌情提供通知。更新后继续使用 app 即表示接受修订后的政策。</p></section>
          <section class="legal-section"><h2>11. 联系方式</h2><p>如对本政策或隐私有疑问，请联系 <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>。</p></section>`
      },
      support: {
        title: "支持",
        description: "Vibeit 支持与帮助，适用于 iPadOS、iOS 和 macOS 的原生 Python IDE。",
        body: `
          <h1>支持</h1><p class="updated">Vibeit - 适用于 iPadOS、iOS 和 macOS 的原生 Python IDE。</p>
          <div class="tldr"><strong>需要帮助？</strong>请发送邮件到 <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>。我们通常会在 1-2 个工作日内回复。</div>
          <p><a class="contact-btn" href="mailto:aroluo@icloud.com?subject=Vibeit%20Support">联系支持</a></p>
          <section class="legal-section"><h2>快速开始</h2><p>Vibeit 是运行在你设备上的完整 Python IDE。创建笔记本或脚本，编写 Python，然后点击运行。代码会在设备端内核中执行，支持 notebooks、matplotlib、NumPy、pandas、PyTorch 等。运行代码不需要网络连接。</p></section>
          <section class="legal-section"><h2>常见问题</h2><h3>免费版本和订阅版包含哪些内容？</h3><p><strong>Standard</strong> 方案包含核心设备端 Python IDE。<strong>Pro</strong> 增加远程 SSH/SFTP 服务器与终端、GitHub 克隆/推送/拉取/拉取请求，以及云端 AI 服务商。每个方案都从 <strong>7 天免费试用</strong>开始。</p><h3>如何开始免费试用或订阅？</h3><p>在 app 中打开 <strong>设置 -> 账户</strong>，选择方案，然后点击 <strong>开始免费试用</strong>。付款由 Apple 通过你的 Apple 账户处理。</p><h3>如何管理或取消订阅？</h3><p>订阅由 Apple 管理。在设备上打开<strong>设置</strong> app，点击你的姓名，进入<strong>订阅</strong>，选择 <strong>Vibeit</strong>。你也可以<a href="https://apps.apple.com/account/subscriptions">在这里管理订阅</a>。</p><h3>如何恢复购买？</h3><p>在新设备或重新安装后，打开 Vibeit 的 <strong>设置 -> 账户</strong>，点击<strong>恢复购买</strong>。请确认使用的是订阅时的同一个 Apple 账户。</p><h3>如何连接远程服务器或 GitHub？</h3><p>进入 <strong>设置 -> 远程</strong> 添加 SSH/SFTP 主机，或进入 <strong>设置 -> 源代码管理</strong> 连接 GitHub。凭据会保存在设备钥匙串中，不会发送给我们。</p><h3>如何使用自己的 AI 服务商？</h3><p>打开 <strong>设置 -> AI</strong>，添加服务商和 API 密钥。你的密钥保留在设备上，只用于直接连接该服务商。</p><h3>在哪里安装额外 Python 包？</h3><p>使用 app 内置软件包目录安装受支持的纯 Python 包和预编译原生包。可用性取决于软件包是否能在 iOS 和 iPadOS 上运行。</p></section>
          <section class="legal-section"><h2>隐私和数据</h2><p>Vibeit 默认保护隐私：你的代码、文件和凭据保留在设备上。详情请参见<a href="privacy.html">隐私政策</a>。</p></section>
          <section class="legal-section"><h2>联系方式</h2><p>如果仍有问题、发现 bug 或想提出功能建议，请发送邮件到 <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>，并附上设备型号和 iOS/iPadOS 版本。</p></section>`
      },
      terms: {
        title: "使用条款",
        description: "Vibeit 使用条款，适用于 iPadOS、iOS 和 macOS 的原生 Python IDE。",
        body: `
          <h1>使用条款</h1><p class="updated">最后更新：2026 年 7 月 6 日</p>
          <p>本使用条款（“条款”）是你与 <strong>Vibeit</strong> 开发者之间关于下载和使用 iPadOS、iOS 和 macOS 上 Vibeit 应用程序的法律协议。下载、安装或使用 Vibeit 即表示你同意本条款。如不同意，请不要使用本 app。</p>
          <div class="tldr"><strong>简短版。</strong>Vibeit 是开发工具，在你的设备上运行 Python，并可通过你连接的服务使用可选 AI 和网络功能。你需要对自己的代码、数据、凭据以及这些功能的使用方式负责。App 按“现状”提供；AI 输出和执行的代码可能错误或不安全，因此依赖前请自行审查。</div>
          <section class="legal-section"><h2>1. 资格和接受</h2><p>你必须年满 13 岁或达到所在地区数字同意最低年龄，并具备订立有效合同的能力。如果你代表组织使用本 app，你声明你有权代表该组织接受本条款。你的使用还受 Apple <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">许可应用最终用户许可协议（EULA）</a>约束；如本条款与 Apple EULA 就 App Store 许可发生冲突，以 Apple EULA 为准。</p></section>
          <section class="legal-section"><h2>2. Vibeit 是什么</h2><p>Vibeit 是原生 Python 笔记本和脚本 IDE，在设备端 Python 运行时执行代码。可选功能包括你配置的 AI 服务商、SSH/SFTP 远程连接、Cloudflare Access、源代码管理和 GitHub 集成，以及 Python 包下载。这些服务由你或第三方运营，不由我们运营。</p></section>
          <section class="legal-section"><h2>3. 许可</h2><p>在遵守本条款和 Apple EULA 的前提下，我们授予你个人的、有限的、非独占、不可转让、可撤销许可，使你可在自己拥有或控制的 Apple 品牌设备上，为合法的个人或内部业务目的使用 Vibeit。除法律允许外，你不得复制、修改、反向工程、反编译、再许可、销售或分发本 app。</p></section>
          <section class="legal-section"><h2>4. 你的责任和可接受使用</h2><p>你需要对编写或运行的代码、处理的数据、输入的凭据以及连接的系统独自负责。你同意不使用 Vibeit 违法、侵权、未经授权访问系统、开发或传播恶意软件、进行滥用活动、披露无权披露的数据，或规避安全、使用量或速率限制。你负责保护设备、API 密钥、SSH 凭据、源代码管理令牌并备份自己的工作。</p></section>
          <section class="legal-section"><h2>5. 第三方服务</h2><p>当你启用连接第三方的功能，例如 AI 服务商、远程主机、Cloudflare Access、GitHub 或软件包索引时，你对该服务的使用受该第三方条款和隐私政策约束。你负责其可能收取的费用。我们不运营或控制这些服务，也不对其可用性、内容、安全、行为或收费负责。</p></section>
          <section class="legal-section"><h2>6. AI 功能和生成内容</h2><p>AI 功能可能生成不准确、不完整、不安全、有偏见或不适用的代码、解释或其他内容。AI 输出不构成专业、法律、财务、医疗或安全建议。在依赖、执行、发布或交付任何 AI 生成或 app 建议内容前，你负责审查、测试和验证。</p></section>
          <section class="legal-section"><h2>7. 代码执行、远程命令和数据</h2><p>Vibeit 会运行你提供的代码和 shell 命令，或在你的指示下运行 AI 智能体提供的代码和命令。执行代码或远程命令可能修改或删除文件、消耗资源，或影响你连接的系统。你接受这些风险并对结果负责。你保留对代码、笔记本和数据的所有权。</p></section>
          <section class="legal-section"><h2>8. 安全和数据丢失免责声明</h2><p>我们将 Vibeit 设计为默认保护隐私，并使用钥匙串和加密传输等保护措施。但任何软件、存储或传输方式都不可能完全安全；我们不保证 app 无错误、不中断、无漏洞，也不保证不会发生数据丢失或未经授权访问。</p></section>
          <section class="legal-section"><h2>9. 订阅和付款</h2><p>部分功能可能需要通过 <strong>Apple App 内购买</strong>销售的付费订阅。费用会记入你的 Apple 账户，订阅会自动续订，除非你在续订截止时间前取消。你可以在 Apple 账户设置中管理或取消订阅。Apple 根据其条款处理付款和退款。</p></section>
          <section class="legal-section"><h2 class="legal">10. 免责声明</h2><p class="legal">本 app 按“现状”和“可用状态”提供，不提供任何明示、默示或法定保证，包括适销性、特定用途适用性、所有权、准确性和不侵权的默示保证。部分司法辖区不允许排除某些保证，因此部分排除可能不适用于你。</p></section>
          <section class="legal-section"><h2 class="legal">11. 责任限制</h2><p class="legal">在法律允许的最大范围内，我们不对因使用或无法使用本 app、AI 输出、执行的代码或命令、数据丢失、安全事件或第三方服务引起的间接、附带、特殊、后果性、惩罚性损害，或利润、收入、数据、商誉及其他无形损失负责。与本 app 有关的全部索赔中，我们的总责任不超过你在索赔事件发生前十二个月内为本 app 向我们支付的金额或 10 美元两者中的较高者。</p></section>
          <section class="legal-section"><h2>12. 赔偿</h2><p>在法律允许范围内，你同意就你误用本 app、违反本条款或法律、你的代码、数据、内容，或你使用任何连接的第三方服务或系统所引起的索赔、损害、责任和费用，使我们免受损害。</p></section>
          <section class="legal-section"><h2>13. 终止</h2><p>你可以随时删除 app 停止使用。如果你实质性违反本条款或违法使用 app，我们可以暂停或终止你的许可。按性质应在终止后继续有效的条款将继续有效。</p></section>
          <section class="legal-section"><h2>14. Apple App Store 条款</h2><p>本条款仅在你与我们之间成立，并非与 Apple 成立。Apple 不负责 app 或其内容，也无义务提供维护或支持。Apple 及其子公司是本条款的第三方受益人，并可向你执行本条款。你声明你不位于受美国政府禁运的国家，也不在美国政府限制方名单上。</p></section>
          <section class="legal-section"><h2>15. 适用法律</h2><p>本条款受开发者所在地司法辖区法律管辖，但你居住地强制性消费者保护法律另有规定的除外。本条款不限制你作为消费者可能拥有的不可放弃法定权利。</p></section>
          <section class="legal-section"><h2>16. 条款变更</h2><p>我们可能不时更新本条款。我们会修改上方“最后更新”日期；如有重大变更，会酌情提供通知。更新后继续使用即表示接受修订后的条款。</p></section>
          <section class="legal-section"><h2>17. 联系方式</h2><p>如对本条款有疑问，请联系 <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>。</p></section>`
      },
      contact: {
        title: "联系我们",
        description: "联系 Vibeit：提交功能建议或反馈问题。",
        body: `
          <h1>联系我们</h1>
          <p class="updated">提交功能建议或反馈问题——每一条我们都会认真阅读。</p>`
      }
    },

    ja: {
      privacy: {
        title: "プライバシーポリシー",
        description: "iPadOS、iOS、macOS 向けネイティブ Python IDE、Vibeit のプライバシーポリシー。",
        body: `
          <h1>プライバシーポリシー</h1><p class="updated">最終更新日：2026年7月6日</p>
          <p>このポリシーは、iPadOS、iOS、macOS の Vibeit アプリを利用する際に <strong>Vibeit</strong>（「本アプリ」「当方」）が情報をどのように扱うかを説明します。Vibeit はデバイス上で動作するネイティブ Python ノートブック IDE です。コードはデバイス上の Python カーネルで実行され、ファイル、認証情報、API キーはあなたのデバイスに残ります。</p>
          <div class="tldr"><strong>要約。</strong>当方は分析サーバーや広告サーバーを運用せず、本アプリには第三者トラッキング SDK や広告 SDK は含まれません。個人情報を販売しません。データがデバイス外へ送信されるのは、あなたが自分のキーで AI プロバイダを呼び出す、設定したリモートサーバーへ接続する、パッケージをダウンロードするなど、必要な機能を使う場合だけです。</div>
          <section class="legal-section"><h2>1. デバイスに保存される情報</h2><p>作成または開いたノートブック、スクリプト、ワークスペースファイル、ローカル Python 実行のコードと出力、API キーや SSH 認証情報などの秘密情報、テーマや言語などの設定は、あなたのデバイスまたは選択した iCloud/Files ストレージに保存されます。当方はこれらのコピーを受け取りません。秘密情報は Keychain に保存され、ノートブックやログに書き込まれず、当方へ送信されません。</p></section>
          <section class="legal-section"><h2>2. ウェブサイトの言語判定</h2><p>これらのページは、IP 所在国から初期表示言語を選ぶため、GeoJS に国コードの問い合わせを行う場合があります。返される国コードはブラウザ内で言語選択にのみ使用されます。失敗した場合はブラウザ言語、次に英語へフォールバックします。手動で変更した言語は、このデバイスの localStorage に保存されます。</p></section>
          <section class="legal-section"><h2>3. 第三者へデータを送信する機能</h2><p>AI 支援、SSH/SFTP や Cloudflare Access によるリモート接続、パッケージダウンロードなどを利用すると、関連データは該当する第三者に送信され、その第三者のポリシーが適用されます。Vibeit はクライアントとして動作するだけです。当方は AI プロンプト、補完、リモートセッション内容を受け取りません。</p></section>
          <section class="legal-section"><h2>4. サブスクリプションと支払い</h2><p>Vibeit のサブスクリプションは <strong>Apple の App 内課金</strong>で販売されます。Apple が支払いと購読を処理し、当方はカード情報を受け取ったり保存したりしません。本アプリは機能解除のために StoreKit 経由で購読または権利状態のみを受け取ります。</p></section>
          <section class="legal-section"><h2>5. 当方が収集する情報</h2><p>当方はユーザーアカウントを運用せず、個人情報を収集するバックエンドも運用しません。第三者分析や広告も含まれていません。サポートメールを送った場合、メールに記載した情報を当方が受け取ります。</p></section>
          <section class="legal-section"><h2>6. データセキュリティ</h2><p>秘密情報は OS の Keychain に保存され、ネットワーク接続には TLS または SSH 暗号化を使用します。保存や送信の方法に 100% の安全はありませんが、Apple プラットフォームの保護と暗号化通信を利用します。</p></section>
          <section class="legal-section"><h2>7. 保持と削除</h2><p>データはあなたのデバイス上にあるため、あなたが管理できます。アプリ内でファイル、ホスト、認証情報を削除でき、アプリを削除するとローカルデータと関連 Keychain 項目が削除されます。第三者に送信済みのデータは、その第三者のポリシーに従います。</p></section>
          <section class="legal-section"><h2>8. 子どものプライバシー</h2><p>Vibeit は開発者向けツールであり、13 歳未満または地域の最低年齢未満の子どもを対象としていません。当方は子どもの個人情報を knowingly 収集しません。</p></section>
          <section class="legal-section"><h2>9. 国際ユーザーと権利</h2><p>居住地によっては、GDPR や CCPA/CPRA などに基づきアクセス、訂正、削除、処理制限の権利を持つ場合があります。当方は自社サーバーに個人情報を保存しないため、多くの請求はデバイス上または該当する第三者プロバイダで対応されます。</p></section>
          <section class="legal-section"><h2>10. 変更</h2><p>このポリシーは随時更新されることがあります。最終更新日を変更し、重要な変更については適切な通知を行います。</p></section>
          <section class="legal-section"><h2>11. 連絡先</h2><p>質問は <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> までご連絡ください。</p></section>`
      },
      support: {
        title: "サポート",
        description: "iPadOS、iOS、macOS 向けネイティブ Python IDE、Vibeit のサポート。",
        body: `
          <h1>サポート</h1><p class="updated">Vibeit - iPadOS、iOS、macOS 向けのネイティブ Python IDE。</p>
          <div class="tldr"><strong>お困りですか？</strong><a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> までメールしてください。通常 1〜2 営業日以内に返信します。</div>
          <p><a class="contact-btn" href="mailto:aroluo@icloud.com?subject=Vibeit%20Support">サポートに連絡</a></p>
          <section class="legal-section"><h2>はじめに</h2><p>Vibeit はデバイス上で動くフル Python IDE です。ノートブックまたはスクリプトを作成し、Python を書いて実行します。コードはデバイス上のカーネルで実行され、notebook、matplotlib、NumPy、pandas、PyTorch などに対応します。コード実行にインターネット接続は不要です。</p></section>
          <section class="legal-section"><h2>よくある質問</h2><h3>無料版とサブスクリプションの違いは？</h3><p><strong>Standard</strong> には基本的なオンデバイス Python IDE が含まれます。<strong>Pro</strong> では SSH/SFTP リモートサーバーとターミナル、GitHub の clone/push/pull/プルリクエスト、クラウド AI プロバイダが追加されます。各プランは <strong>7 日間無料トライアル</strong>から始まります。</p><h3>無料トライアルや購読を開始するには？</h3><p>アプリで <strong>Settings -> Account</strong> を開き、プランを選んで <strong>Start Free Trial</strong> をタップします。支払いは Apple アカウントを通じて処理されます。</p><h3>購読の管理や解約は？</h3><p>デバイスの <strong>設定</strong> アプリで名前をタップし、<strong>サブスクリプション</strong>から <strong>Vibeit</strong> を選びます。<a href="https://apps.apple.com/account/subscriptions">こちら</a>からも管理できます。</p><h3>購入を復元するには？</h3><p>新しいデバイスまたは再インストール後、Vibeit の <strong>Settings -> Account</strong> で <strong>Restore Purchases</strong> をタップします。購読に使った Apple アカウントでサインインしてください。</p><h3>リモートサーバーや GitHub に接続するには？</h3><p><strong>Settings -> Remote</strong> で SSH/SFTP ホストを追加し、<strong>Settings -> Source Control</strong> で GitHub に接続します。認証情報は Keychain に保存され、当方へ送信されません。</p><h3>自分の AI プロバイダを使うには？</h3><p><strong>Settings -> AI</strong> でプロバイダと API キーを追加します。キーはデバイス上に残り、そのプロバイダと直接通信するためだけに使用されます。</p><h3>追加パッケージはどこで入れられますか？</h3><p>アプリ内のパッケージカタログで、対応する pure-Python パッケージや事前ビルド済みネイティブパッケージをインストールできます。</p></section>
          <section class="legal-section"><h2>プライバシーとデータ</h2><p>Vibeit はデフォルトでプライベートです。詳細は <a href="privacy.html">プライバシーポリシー</a>をご覧ください。</p></section>
          <section class="legal-section"><h2>連絡先</h2><p>問題、バグ、機能要望がある場合は、デバイスモデルと iOS/iPadOS バージョンを添えて <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> までご連絡ください。</p></section>`
      },
      terms: {
        title: "利用規約",
        description: "iPadOS、iOS、macOS 向けネイティブ Python IDE、Vibeit の利用規約。",
        body: `
          <h1>利用規約</h1><p class="updated">最終更新日：2026年7月6日</p>
          <p>本利用規約（「本規約」）は、iPadOS、iOS、macOS 上の <strong>Vibeit</strong> アプリのダウンロードおよび使用に関する、あなたと開発者との法的合意です。Vibeit をダウンロード、インストール、使用することで本規約に同意したものとみなされます。同意しない場合は使用しないでください。</p>
          <div class="tldr"><strong>要約。</strong>Vibeit は Python、任意の AI 機能、ネットワーク機能を、あなたのデバイスおよびあなたが接続するサービスで動かす開発者向けツールです。コード、データ、認証情報、機能の使い方についてはあなたが責任を負います。本アプリは「現状有姿」で提供されます。</div>
          <section class="legal-section"><h2>1. 資格と同意</h2><p>あなたは 13 歳以上または地域のデジタル同意最低年齢以上で、有効な契約を結べる必要があります。組織を代表して利用する場合、その組織のために本規約を受け入れる権限があることを表明します。使用には Apple の <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Licensed Application End User License Agreement</a> も適用されます。</p></section>
          <section class="legal-section"><h2>2. Vibeit について</h2><p>Vibeit はデバイス上の Python ランタイムでコードを実行するネイティブ Python ノートブックおよびスクリプト IDE です。任意機能には AI プロバイダ、SSH/SFTP リモート接続、Cloudflare Access、GitHub 連携、Python パッケージダウンロードがあります。これらのサービスは当方ではなく、あなたまたは第三者が運営します。</p></section>
          <section class="legal-section"><h2>3. ライセンス</h2><p>本規約と Apple EULA に従い、当方はあなたが所有または管理する Apple ブランドデバイス上で、合法的な個人利用または社内業務利用のために Vibeit を使用する、個人的、限定的、非独占的、譲渡不可、取消可能なライセンスを付与します。</p></section>
          <section class="legal-section"><h2>4. あなたの責任と許容される利用</h2><p>あなたは、書くまたは実行するコード、処理するデータ、入力する認証情報、接続するシステムについて単独で責任を負います。違法行為、権利侵害、無許可アクセス、マルウェア、攻撃、無断データ開示、制限回避のために Vibeit を使用してはなりません。デバイス、キー、認証情報、トークン、バックアップの管理もあなたの責任です。</p></section>
          <section class="legal-section"><h2>5. 第三者サービス</h2><p>AI プロバイダ、リモートホスト、Cloudflare Access、GitHub、パッケージインデックスなどの第三者サービスの利用には、その第三者の規約とプライバシーポリシーが適用されます。当方はそれらのサービスを運営または管理せず、可用性、内容、セキュリティ、行為、料金について責任を負いません。</p></section>
          <section class="legal-section"><h2>6. AI 機能と生成出力</h2><p>AI 機能は不正確、不完全、安全でない、偏った、または不適切な内容を生成する場合があります。AI 出力は専門的、法的、金融、医療、セキュリティ上の助言ではありません。実行、公開、出荷、依拠する前に、あなたが確認、テスト、検証する責任を負います。</p></section>
          <section class="legal-section"><h2>7. コード実行、リモートコマンド、データ</h2><p>Vibeit はあなたまたはあなたの指示で AI エージェントが提供するコードやコマンドを実行します。実行によりファイルの変更や削除、リソース消費、接続先システムへの影響が生じる可能性があります。あなたはこれらのリスクを受け入れ、結果に責任を負います。</p></section>
          <section class="legal-section"><h2>8. セキュリティとデータ損失に関する免責</h2><p>当方は Keychain や暗号化通信などを利用しますが、どのソフトウェア、保存、送信方法も完全に安全ではありません。本アプリがエラーなく、中断なく、脆弱性やデータ損失、無許可アクセスなしに動作することを保証しません。</p></section>
          <section class="legal-section"><h2>9. 購読と支払い</h2><p>一部機能は Apple の App 内課金による有料サブスクリプションが必要な場合があります。支払いは Apple アカウントに請求され、期限までに解約しない限り自動更新されます。支払いと返金は Apple の規約に従って処理されます。</p></section>
          <section class="legal-section"><h2 class="legal">10. 保証の否認</h2><p class="legal">本アプリは「現状有姿」かつ「提供可能な範囲」で提供され、明示、黙示、法定を問わずいかなる保証もありません。商品性、特定目的適合性、権原、正確性、非侵害の黙示保証を含みます。</p></section>
          <section class="legal-section"><h2 class="legal">11. 責任の制限</h2><p class="legal">法律で認められる最大限の範囲で、当方は本アプリの利用または利用不能、AI 出力、実行されたコードやコマンド、データ損失、セキュリティ事故、第三者サービスに起因する間接、付随、特別、結果的、懲罰的損害または利益、収益、データ、信用その他無形損失について責任を負いません。総責任額は、請求原因発生前 12 か月にあなたが当方に支払った額または 10 米ドルのいずれか高い額を超えません。</p></section>
          <section class="legal-section"><h2>12. 補償</h2><p>法律で認められる範囲で、あなたは本アプリの誤用、本規約または法律違反、あなたのコード、データ、コンテンツ、第三者サービスまたはシステムの利用に起因する請求や費用から当方を保護することに同意します。</p></section>
          <section class="legal-section"><h2>13. 終了</h2><p>あなたはいつでもアプリを削除して使用を終了できます。当方は重大な違反または違法利用がある場合、ライセンスを停止または終了できます。性質上存続すべき条項は終了後も存続します。</p></section>
          <section class="legal-section"><h2>14. Apple App Store 条項</h2><p>本規約はあなたと当方の間のものであり、Apple とのものではありません。Apple は本アプリや内容について責任を負わず、保守やサポート義務もありません。Apple とその子会社は本規約の第三者受益者です。</p></section>
          <section class="legal-section"><h2>15. 準拠法</h2><p>本規約は開発者が設立された法域の法律に準拠します。ただし、居住地の強行的な消費者保護法が別途適用される場合を除きます。</p></section>
          <section class="legal-section"><h2>16. 規約変更</h2><p>当方は本規約を随時更新できます。最終更新日を変更し、重要な変更については適切に通知します。更新後の利用継続は改訂後規約への同意を意味します。</p></section>
          <section class="legal-section"><h2>17. 連絡先</h2><p>質問は <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> までご連絡ください。</p></section>`
      },
      contact: {
        title: "お問い合わせ",
        description: "Vibeit へのお問い合わせ：機能のご提案や問題のご報告。",
        body: `
          <h1>お問い合わせ</h1>
          <p class="updated">機能のご提案や問題のご報告をお送りください。すべて目を通します。</p>`
      }
    },

    ko: {
      privacy: {
        title: "개인정보 처리방침",
        description: "iPadOS, iOS, macOS용 네이티브 Python IDE Vibeit의 개인정보 처리방침.",
        body: `
          <h1>개인정보 처리방침</h1><p class="updated">최종 업데이트: 2026년 7월 6일</p>
          <p>이 방침은 iPadOS, iOS, macOS에서 <strong>Vibeit</strong> 앱을 사용할 때 Vibeit("앱", "당사")이 정보를 어떻게 처리하는지 설명합니다. Vibeit은 기기에서 실행되는 네이티브 Python 노트북 IDE입니다. 코드는 온디바이스 Python 커널에서 실행되고, 파일, 자격 증명, API 키는 사용자의 기기에 남도록 설계되었습니다.</p>
          <div class="tldr"><strong>요약.</strong> 당사는 분석 서버나 광고 서버를 운영하지 않으며, 앱에는 제3자 추적 또는 광고 SDK가 없습니다. 개인 정보를 판매하지 않습니다. 사용자가 직접 필요한 기능을 사용할 때만 데이터가 기기 밖으로 나갑니다. 예를 들면 본인 키로 AI 제공자를 호출하거나, 설정한 원격 서버에 연결하거나, 패키지를 다운로드하는 경우입니다.</div>
          <section class="legal-section"><h2>1. 기기에 저장되는 정보</h2><p>작성하거나 여는 노트북, 스크립트, 작업공간 파일, 로컬 Python 실행 코드와 출력, API 키와 SSH 자격 증명, 테마와 언어 같은 설정은 사용자의 기기 또는 사용자가 선택한 iCloud/Files 저장소에 저장됩니다. 당사는 사본을 받지 않습니다. 비밀 정보는 Keychain에 저장되며 노트북이나 로그에 기록되거나 당사로 전송되지 않습니다.</p></section>
          <section class="legal-section"><h2>2. 웹사이트 언어 감지</h2><p>이 페이지들은 IP 위치에 따른 초기 언어 선택을 위해 GeoJS에 국가 코드 조회를 요청할 수 있습니다. 반환된 국가 코드는 브라우저에서 언어 선택에만 사용됩니다. 실패하면 브라우저 언어, 그 다음 영어로 돌아갑니다. 수동으로 선택한 언어는 이 기기의 localStorage에 저장됩니다.</p></section>
          <section class="legal-section"><h2>3. 제3자에게 데이터가 전송되는 기능</h2><p>AI 지원, SSH/SFTP 또는 Cloudflare Access 원격 연결, 패키지 다운로드를 사용하면 관련 데이터가 해당 제3자에게 전송되고 그들의 정책이 적용됩니다. Vibeit은 클라이언트로만 동작합니다. 당사는 AI 프롬프트, 결과, 원격 세션 내용을 받지 않습니다.</p></section>
          <section class="legal-section"><h2>4. 구독과 결제</h2><p>Vibeit 구독은 <strong>Apple 앱 내 구입</strong>으로 판매됩니다. Apple이 결제와 구독을 처리하며, 당사는 카드 정보를 받거나 저장하지 않습니다. 앱은 기능 잠금 해제를 위해 StoreKit을 통해 구독 또는 권한 상태만 받습니다.</p></section>
          <section class="legal-section"><h2>5. 당사가 수집하는 정보</h2><p>당사는 사용자 계정을 운영하지 않고, 개인 정보를 수집하는 백엔드를 운영하지 않습니다. 앱에는 제3자 분석이나 광고가 없습니다. 지원 이메일을 보내면 사용자가 메일에 포함한 정보를 받습니다.</p></section>
          <section class="legal-section"><h2>6. 데이터 보안</h2><p>비밀 정보는 운영체제 Keychain에 저장되고 네트워크 연결은 TLS 또는 SSH 암호화를 사용합니다. 어떤 저장 또는 전송 방식도 100% 안전하지는 않지만, Apple 플랫폼 보호와 암호화 전송을 사용합니다.</p></section>
          <section class="legal-section"><h2>7. 보관과 삭제</h2><p>데이터는 사용자의 기기에 있으므로 사용자가 관리합니다. 앱에서 파일, 호스트, 자격 증명을 삭제할 수 있고, 앱을 제거하면 로컬 데이터와 관련 Keychain 항목이 삭제됩니다. 이미 제3자에게 보낸 데이터는 해당 제3자의 정책을 따릅니다.</p></section>
          <section class="legal-section"><h2>8. 아동 개인정보</h2><p>Vibeit은 개발자 도구이며 13세 미만 또는 지역의 최소 연령 미만 아동을 대상으로 하지 않습니다. 당사는 아동의 개인 정보를 고의로 수집하지 않습니다.</p></section>
          <section class="legal-section"><h2>9. 국제 사용자와 권리</h2><p>거주 지역에 따라 GDPR 또는 CCPA/CPRA 등에 따른 열람, 정정, 삭제, 처리 제한 권리가 있을 수 있습니다. 당사는 자체 서버에 개인 정보를 저장하지 않으므로 대부분의 요청은 기기 또는 관련 제3자 제공자에서 처리됩니다.</p></section>
          <section class="legal-section"><h2>10. 방침 변경</h2><p>이 방침은 때때로 업데이트될 수 있습니다. 최종 업데이트 날짜를 수정하고 중요한 변경에는 적절히 알립니다.</p></section>
          <section class="legal-section"><h2>11. 연락처</h2><p>문의는 <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> 으로 보내 주세요.</p></section>`
      },
      support: {
        title: "지원",
        description: "iPadOS, iOS, macOS용 네이티브 Python IDE Vibeit 지원.",
        body: `
          <h1>지원</h1><p class="updated">Vibeit - iPadOS, iOS, macOS용 네이티브 Python IDE.</p>
          <div class="tldr"><strong>도움이 필요하신가요?</strong> <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> 으로 이메일을 보내 주세요. 보통 영업일 기준 1-2일 안에 답장합니다.</div>
          <p><a class="contact-btn" href="mailto:aroluo@icloud.com?subject=Vibeit%20Support">지원 문의</a></p>
          <section class="legal-section"><h2>시작하기</h2><p>Vibeit은 기기에서 실행되는 완전한 Python IDE입니다. 노트북이나 스크립트를 만들고 Python을 작성한 뒤 실행하세요. 코드는 온디바이스 커널에서 실행되며 notebooks, matplotlib, NumPy, pandas, PyTorch 등을 지원합니다. 코드 실행에는 인터넷 연결이 필요하지 않습니다.</p></section>
          <section class="legal-section"><h2>자주 묻는 질문</h2><h3>무료 버전과 구독에는 무엇이 포함되나요?</h3><p><strong>Standard</strong> 플랜에는 핵심 온디바이스 Python IDE가 포함됩니다. <strong>Pro</strong>에는 SSH/SFTP 원격 서버와 터미널, GitHub clone/push/pull/PR, 클라우드 AI 제공자가 추가됩니다. 모든 플랜은 <strong>7일 무료 체험</strong>으로 시작합니다.</p><h3>무료 체험 또는 구독은 어떻게 시작하나요?</h3><p>앱에서 <strong>Settings -> Account</strong>를 열고 플랜을 선택한 뒤 <strong>Start Free Trial</strong>을 누르세요. 결제는 Apple 계정을 통해 처리됩니다.</p><h3>구독 관리 또는 취소는 어떻게 하나요?</h3><p>기기의 <strong>설정</strong> 앱에서 이름을 탭하고 <strong>구독</strong>으로 이동한 뒤 <strong>Vibeit</strong>을 선택하세요. <a href="https://apps.apple.com/account/subscriptions">여기</a>에서도 관리할 수 있습니다.</p><h3>구매 복원은 어떻게 하나요?</h3><p>새 기기나 재설치 후 Vibeit의 <strong>Settings -> Account</strong>에서 <strong>Restore Purchases</strong>를 누르세요. 구독에 사용한 Apple 계정으로 로그인해야 합니다.</p><h3>원격 서버나 GitHub 연결은?</h3><p><strong>Settings -> Remote</strong>에서 SSH/SFTP 호스트를 추가하거나 <strong>Settings -> Source Control</strong>에서 GitHub를 연결하세요. 자격 증명은 Keychain에 저장되고 당사로 전송되지 않습니다.</p><h3>내 AI 제공자는 어떻게 쓰나요?</h3><p><strong>Settings -> AI</strong>에서 제공자와 API 키를 추가하세요. 키는 기기에 남고 해당 제공자와 직접 통신하는 데만 사용됩니다.</p><h3>추가 Python 패키지는 어디서 설치하나요?</h3><p>앱 내 패키지 카탈로그에서 지원되는 pure-Python 및 사전 빌드 네이티브 패키지를 설치할 수 있습니다.</p></section>
          <section class="legal-section"><h2>개인정보와 데이터</h2><p>Vibeit은 기본적으로 비공개입니다. 자세한 내용은 <a href="privacy.html">개인정보 처리방침</a>을 확인하세요.</p></section>
          <section class="legal-section"><h2>연락처</h2><p>문제, 버그, 기능 요청이 있으면 기기 모델과 iOS/iPadOS 버전을 포함해 <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> 으로 보내 주세요.</p></section>`
      },
      terms: {
        title: "이용 약관",
        description: "iPadOS, iOS, macOS용 네이티브 Python IDE Vibeit 이용 약관.",
        body: `
          <h1>이용 약관</h1><p class="updated">최종 업데이트: 2026년 7월 6일</p>
          <p>본 이용 약관("약관")은 iPadOS, iOS, macOS용 <strong>Vibeit</strong> 앱의 다운로드 및 사용에 관한 사용자와 개발자 간의 법적 계약입니다. Vibeit을 다운로드, 설치 또는 사용하면 본 약관에 동의하는 것입니다. 동의하지 않으면 앱을 사용하지 마세요.</p>
          <div class="tldr"><strong>요약.</strong> Vibeit은 사용자의 기기와 사용자가 연결한 서비스에서 Python, 선택적 AI, 네트워크 기능을 실행하는 개발자 도구입니다. 사용자의 코드, 데이터, 자격 증명, 기능 사용 방식은 사용자 책임입니다. 앱은 "있는 그대로" 제공됩니다.</div>
          <section class="legal-section"><h2>1. 자격과 수락</h2><p>사용자는 13세 이상 또는 관할 지역의 디지털 동의 최소 연령 이상이어야 하며 유효한 계약을 체결할 수 있어야 합니다. 조직을 대신하여 사용하는 경우 해당 조직을 위해 약관을 수락할 권한이 있음을 진술합니다. 사용에는 Apple의 <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Licensed Application End User License Agreement</a>도 적용됩니다.</p></section>
          <section class="legal-section"><h2>2. Vibeit의 성격</h2><p>Vibeit은 온디바이스 Python 런타임에서 코드를 실행하는 네이티브 Python 노트북 및 스크립트 IDE입니다. 선택 기능에는 사용자가 설정한 AI 제공자, SSH/SFTP 원격 연결, Cloudflare Access, GitHub 통합, Python 패키지 다운로드가 포함됩니다. 이러한 서비스는 당사가 아닌 사용자 또는 제3자가 운영합니다.</p></section>
          <section class="legal-section"><h2>3. 라이선스</h2><p>본 약관과 Apple EULA에 따라, 당사는 사용자가 소유하거나 제어하는 Apple 브랜드 기기에서 합법적인 개인 또는 내부 업무 목적으로 Vibeit을 사용할 수 있는 개인적, 제한적, 비독점적, 양도 불가, 취소 가능한 라이선스를 부여합니다.</p></section>
          <section class="legal-section"><h2>4. 책임과 허용 사용</h2><p>사용자는 작성하거나 실행하는 코드, 처리하는 데이터, 입력하는 자격 증명, 연결하는 시스템에 대해 단독으로 책임집니다. 법률 위반, 권리 침해, 무단 접근, 악성코드, 공격, 허용되지 않은 데이터 공개, 보안/사용량/속도 제한 우회를 위해 Vibeit을 사용할 수 없습니다. 기기, 키, 자격 증명, 토큰, 백업 관리도 사용자 책임입니다.</p></section>
          <section class="legal-section"><h2>5. 제3자 서비스</h2><p>AI 제공자, 원격 호스트, Cloudflare Access, GitHub, 패키지 인덱스와 같은 제3자 서비스에는 해당 제3자의 약관과 개인정보 정책이 적용됩니다. 당사는 해당 서비스를 운영하거나 제어하지 않으며 가용성, 콘텐츠, 보안, 행위, 요금에 책임지지 않습니다.</p></section>
          <section class="legal-section"><h2>6. AI 기능과 생성 출력</h2><p>AI 기능은 부정확하거나 불완전하거나 안전하지 않거나 편향되거나 부적절한 내용을 생성할 수 있습니다. AI 출력은 전문, 법률, 금융, 의료, 보안 조언이 아닙니다. 사용, 실행, 게시, 배포 전에 사용자가 검토, 테스트, 검증해야 합니다.</p></section>
          <section class="legal-section"><h2>7. 코드 실행, 원격 명령, 데이터</h2><p>Vibeit은 사용자 또는 사용자의 지시에 따라 AI 에이전트가 제공한 코드와 명령을 실행합니다. 실행은 파일을 변경 또는 삭제하고, 리소스를 소비하고, 연결한 시스템에 영향을 줄 수 있습니다. 사용자는 이러한 위험과 결과를 부담합니다.</p></section>
          <section class="legal-section"><h2>8. 보안 및 데이터 손실 면책</h2><p>당사는 Keychain과 암호화 전송 같은 보호를 사용하지만, 어떤 소프트웨어, 저장, 전송 방식도 완전히 안전하지 않습니다. 앱이 오류 없이, 중단 없이, 취약점이나 데이터 손실 또는 무단 접근 없이 동작한다고 보증하지 않습니다.</p></section>
          <section class="legal-section"><h2>9. 구독과 결제</h2><p>일부 기능에는 Apple 앱 내 구입으로 판매되는 유료 구독이 필요할 수 있습니다. 결제는 Apple 계정에 청구되며, 갱신 기한 전에 취소하지 않으면 자동 갱신됩니다. 결제와 환불은 Apple 약관에 따라 처리됩니다.</p></section>
          <section class="legal-section"><h2 class="legal">10. 보증 부인</h2><p class="legal">앱은 "있는 그대로" 및 "사용 가능한 상태"로 제공되며, 상품성, 특정 목적 적합성, 권원, 정확성, 비침해를 포함한 명시적, 묵시적, 법정 보증 없이 제공됩니다.</p></section>
          <section class="legal-section"><h2 class="legal">11. 책임 제한</h2><p class="legal">법이 허용하는 최대 범위에서, 당사는 앱 사용 또는 사용 불능, AI 출력, 실행된 코드나 명령, 데이터 손실, 보안 사고, 제3자 서비스와 관련된 간접, 부수, 특별, 결과, 징벌적 손해 또는 이익, 수익, 데이터, 영업권 등 무형 손실에 책임지지 않습니다. 총 책임은 청구 발생 전 12개월 동안 사용자가 당사에 지불한 금액 또는 미화 10달러 중 큰 금액을 초과하지 않습니다.</p></section>
          <section class="legal-section"><h2>12. 면책</h2><p>법이 허용하는 범위에서, 사용자는 앱 오용, 약관 또는 법률 위반, 코드, 데이터, 콘텐츠, 연결된 제3자 서비스 또는 시스템 사용에서 발생한 청구와 비용으로부터 당사를 보호하는 데 동의합니다.</p></section>
          <section class="legal-section"><h2>13. 종료</h2><p>사용자는 언제든 앱을 삭제해 사용을 중단할 수 있습니다. 당사는 중대한 위반 또는 불법 사용이 있는 경우 라이선스를 정지하거나 종료할 수 있습니다. 성격상 존속해야 하는 조항은 종료 후에도 존속합니다.</p></section>
          <section class="legal-section"><h2>14. Apple App Store 조건</h2><p>본 약관은 사용자와 당사 사이의 것이며 Apple과의 계약이 아닙니다. Apple은 앱이나 콘텐츠에 책임지지 않고 유지보수 또는 지원 의무가 없습니다. Apple과 그 자회사는 본 약관의 제3자 수익자입니다.</p></section>
          <section class="legal-section"><h2>15. 준거법</h2><p>본 약관은 개발자가 설립된 관할권의 법률을 따릅니다. 단, 거주지의 강행 소비자 보호법이 달리 적용되는 경우는 제외합니다.</p></section>
          <section class="legal-section"><h2>16. 약관 변경</h2><p>당사는 약관을 때때로 업데이트할 수 있습니다. 최종 업데이트 날짜를 수정하고 중요한 변경에는 적절히 알립니다. 업데이트 후 계속 사용하면 개정 약관을 수락한 것으로 간주됩니다.</p></section>
          <section class="legal-section"><h2>17. 연락처</h2><p>문의는 <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> 으로 보내 주세요.</p></section>`
      },
      contact: {
        title: "문의하기",
        description: "Vibeit 문의: 기능 제안이나 문제 신고를 보내주세요.",
        body: `
          <h1>문의하기</h1>
          <p class="updated">기능 제안이나 문제를 보내주세요. 모두 꼼꼼히 읽습니다.</p>`
      }
    },

    fr: {
      privacy: {
        title: "Politique de Confidentialité",
        description: "Politique de confidentialité de Vibeit, IDE Python natif pour iPadOS, iOS et macOS.",
        body: `
          <h1>Politique de Confidentialité</h1><p class="updated">Dernière mise à jour : 6 juillet 2026</p>
          <p>Cette politique explique comment <strong>Vibeit</strong> ("l'app", "nous") traite les informations lorsque vous utilisez Vibeit sur iPadOS, iOS et macOS. Vibeit est un IDE Python natif conçu pour fonctionner sur votre appareil. Votre code s'exécute dans un noyau Python local, et vos fichiers, identifiants et clés API restent sur votre appareil.</p>
          <div class="tldr"><strong>En bref.</strong> Nous n'exploitons pas de serveurs d'analyse ou de publicité, et l'app ne contient aucun SDK tiers de suivi ou de publicité. Nous ne vendons pas vos informations personnelles. Des données quittent votre appareil uniquement lorsque vous utilisez une fonction qui l'exige, par exemple appeler un fournisseur d'IA avec votre propre clé, connecter un serveur distant ou télécharger un paquet.</div>
          <section class="legal-section"><h2>1. Informations stockées sur votre appareil</h2><p>Les notebooks, scripts, fichiers de travail, code et sorties Python locaux, clés API, identifiants SSH et paramètres de l'app restent sur votre appareil ou dans le stockage iCloud/Files que vous choisissez. Nous n'en recevons pas de copie. Les secrets sont stockés dans le Trousseau et ne sont pas écrits dans les notebooks ou journaux ni transmis à nous.</p></section>
          <section class="legal-section"><h2>2. Détection de langue du site</h2><p>Ces pages peuvent demander à GeoJS un code pays afin de choisir la langue initiale à partir de votre localisation IP. Le code pays est utilisé seulement dans votre navigateur pour choisir la langue. En cas d'échec, la page utilise la langue du navigateur puis l'anglais. Votre choix manuel est conservé dans localStorage sur cet appareil.</p></section>
          <section class="legal-section"><h2>3. Fonctions envoyant des données à des tiers</h2><p>Lorsque vous utilisez l'assistance IA, les connexions SSH/SFTP ou Cloudflare Access, ou les téléchargements de paquets, les données pertinentes sont envoyées au tiers concerné et soumises à ses politiques. Vibeit agit seulement comme client. Nous ne recevons pas vos prompts IA, réponses ou contenus de sessions distantes.</p></section>
          <section class="legal-section"><h2>4. Abonnements et paiements</h2><p>Les abonnements Vibeit sont vendus via <strong>Apple In-App Purchase</strong>. Apple traite le paiement et gère l'abonnement ; nous ne recevons ni ne stockons vos informations de carte. L'app reçoit seulement l'état d'abonnement ou de droit via StoreKit.</p></section>
          <section class="legal-section"><h2>5. Informations que nous collectons</h2><p>Nous ne maintenons pas de comptes utilisateur et n'exploitons pas de backend collectant vos informations personnelles. L'app n'inclut pas d'analyse ou de publicité tierce. Si vous nous contactez par e-mail, nous recevons les informations que vous choisissez d'inclure.</p></section>
          <section class="legal-section"><h2>6. Sécurité</h2><p>Les secrets sont stockés dans le Trousseau du système. Les connexions réseau utilisent TLS ou SSH. Aucune méthode n'est sûre à 100 %, mais nous utilisons les protections de la plateforme Apple et le transport chiffré.</p></section>
          <section class="legal-section"><h2>7. Conservation et suppression</h2><p>Vos données vivant sur votre appareil, vous les contrôlez. Vous pouvez supprimer fichiers, hôtes et identifiants dans l'app ; supprimer l'app supprime ses données locales et éléments Keychain associés. Les données déjà envoyées à un tiers relèvent des politiques de ce tiers.</p></section>
          <section class="legal-section"><h2>8. Vie privée des enfants</h2><p>Vibeit est un outil de développement et ne s'adresse pas aux enfants de moins de 13 ans ou à l'âge minimum équivalent de votre juridiction. Nous ne collectons pas sciemment d'informations personnelles d'enfants.</p></section>
          <section class="legal-section"><h2>9. Utilisateurs internationaux et droits</h2><p>Selon votre lieu de résidence, vous pouvez avoir des droits d'accès, de correction, de suppression ou de limitation du traitement. Comme nous ne stockons pas vos informations personnelles sur nos serveurs, la plupart des demandes se traitent sur votre appareil ou auprès du fournisseur tiers concerné.</p></section>
          <section class="legal-section"><h2>10. Modifications</h2><p>Nous pouvons mettre à jour cette politique. Nous changerons la date de mise à jour et fournirons un avis approprié pour les changements importants.</p></section>
          <section class="legal-section"><h2>11. Contact</h2><p>Questions : <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>.</p></section>`
      },
      support: {
        title: "Assistance",
        description: "Assistance et aide pour Vibeit, IDE Python natif pour iPadOS, iOS et macOS.",
        body: `
          <h1>Assistance</h1><p class="updated">Vibeit - IDE Python natif pour iPadOS, iOS et macOS.</p>
          <div class="tldr"><strong>Besoin d'aide ?</strong> Écrivez à <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>. Nous répondons généralement sous 1 à 2 jours ouvrés.</div>
          <p><a class="contact-btn" href="mailto:aroluo@icloud.com?subject=Vibeit%20Support">Contacter l'assistance</a></p>
          <section class="legal-section"><h2>Premiers pas</h2><p>Vibeit est un IDE Python complet qui s'exécute sur votre appareil. Créez un notebook ou un script, écrivez Python puis lancez l'exécution. Le code tourne dans un noyau local avec notebooks, matplotlib, NumPy, pandas, PyTorch et plus. Aucune connexion Internet n'est nécessaire pour exécuter votre code.</p></section>
          <section class="legal-section"><h2>Questions fréquentes</h2><h3>Que contient la version gratuite par rapport à l'abonnement ?</h3><p>Le plan <strong>Standard</strong> inclut l'IDE Python local principal. <strong>Pro</strong> ajoute les serveurs SSH/SFTP et terminal, GitHub clone/push/pull et pull requests, ainsi que les fournisseurs IA cloud. Chaque plan commence par un <strong>essai gratuit de 7 jours</strong>.</p><h3>Comment démarrer l'essai ou s'abonner ?</h3><p>Ouvrez <strong>Settings -> Account</strong>, choisissez un plan puis touchez <strong>Start Free Trial</strong>. Le paiement est traité par Apple via votre compte Apple.</p><h3>Comment gérer ou annuler l'abonnement ?</h3><p>Dans l'app <strong>Réglages</strong> de l'appareil, touchez votre nom, ouvrez <strong>Abonnements</strong>, puis <strong>Vibeit</strong>. Vous pouvez aussi <a href="https://apps.apple.com/account/subscriptions">gérer les abonnements ici</a>.</p><h3>Comment restaurer un achat ?</h3><p>Sur un nouvel appareil ou après réinstallation, ouvrez <strong>Settings -> Account</strong> dans Vibeit et touchez <strong>Restore Purchases</strong>. Utilisez le même compte Apple.</p><h3>Comment connecter un serveur distant ou GitHub ?</h3><p>Ajoutez un hôte SSH/SFTP dans <strong>Settings -> Remote</strong>, ou connectez GitHub dans <strong>Settings -> Source Control</strong>. Les identifiants restent dans le Trousseau.</p><h3>Comment utiliser mon propre fournisseur IA ?</h3><p>Dans <strong>Settings -> AI</strong>, ajoutez le fournisseur et la clé API. La clé reste sur votre appareil et sert uniquement à communiquer directement avec ce fournisseur.</p><h3>Où installer des paquets Python ?</h3><p>Utilisez le catalogue intégré pour installer les paquets pure-Python et natifs précompilés pris en charge.</p></section>
          <section class="legal-section"><h2>Confidentialité et données</h2><p>Vibeit est privé par défaut. Voir notre <a href="privacy.html">Politique de confidentialité</a>.</p></section>
          <section class="legal-section"><h2>Contact</h2><p>Pour un bug, une question ou une demande de fonction, écrivez à <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> avec le modèle de votre appareil et la version iOS/iPadOS.</p></section>`
      },
      terms: {
        title: "Conditions d'Utilisation",
        description: "Conditions d'utilisation de Vibeit, IDE Python natif pour iPadOS, iOS et macOS.",
        body: `
          <h1>Conditions d'Utilisation</h1><p class="updated">Dernière mise à jour : 6 juillet 2026</p>
          <p>Ces Conditions d'Utilisation ("Conditions") constituent un accord juridique entre vous et le développeur de <strong>Vibeit</strong> concernant le téléchargement et l'utilisation de l'application Vibeit sur iPadOS, iOS et macOS. En téléchargeant, installant ou utilisant Vibeit, vous acceptez ces Conditions.</p>
          <div class="tldr"><strong>En bref.</strong> Vibeit est un outil de développement qui exécute Python et des fonctions optionnelles d'IA et de réseau sur votre appareil et via les services que vous connectez. Vous êtes responsable de votre code, de vos données, de vos identifiants et de votre usage. L'app est fournie "telle quelle".</div>
          <section class="legal-section"><h2>1. Éligibilité et acceptation</h2><p>Vous devez avoir au moins 13 ans ou l'âge minimum applicable, et être capable de conclure un contrat. Si vous utilisez l'app pour une organisation, vous déclarez être autorisé à accepter ces Conditions. L'utilisation est aussi soumise au <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Licensed Application End User License Agreement</a> d'Apple.</p></section>
          <section class="legal-section"><h2>2. Ce qu'est Vibeit</h2><p>Vibeit est un IDE natif pour notebooks et scripts Python qui exécute le code dans un runtime Python local. Les fonctions optionnelles incluent fournisseurs IA configurés par vous, connexions SSH/SFTP, Cloudflare Access, GitHub et téléchargements de paquets Python. Ces services sont opérés par vous ou par des tiers.</p></section>
          <section class="legal-section"><h2>3. Licence</h2><p>Sous réserve de ces Conditions et de l'EULA Apple, nous vous accordons une licence personnelle, limitée, non exclusive, non transférable et révocable pour utiliser Vibeit sur les appareils Apple que vous possédez ou contrôlez, à des fins légales personnelles ou professionnelles internes.</p></section>
          <section class="legal-section"><h2>4. Vos responsabilités et usage acceptable</h2><p>Vous êtes seul responsable du code exécuté, des données traitées, des identifiants saisis et des systèmes connectés. Vous ne devez pas utiliser Vibeit pour violer la loi, porter atteinte à des droits, accéder sans autorisation, développer ou distribuer des logiciels malveillants, mener des attaques, divulguer des données non autorisées ou contourner des limites de sécurité ou d'usage. La sécurité de l'appareil, des clés, des identifiants, des jetons et des sauvegardes vous incombe.</p></section>
          <section class="legal-section"><h2>5. Services tiers</h2><p>L'utilisation de fournisseurs IA, hôtes distants, Cloudflare Access, GitHub ou index de paquets est régie par les conditions et politiques de ces tiers. Nous ne les opérons ni ne les contrôlons et ne sommes pas responsables de leur disponibilité, contenu, sécurité, actions ou frais.</p></section>
          <section class="legal-section"><h2>6. Fonctions IA et sorties générées</h2><p>Les fonctions IA peuvent produire du contenu inexact, incomplet, non sécurisé, biaisé ou inadapté. Les sorties IA ne sont pas des conseils professionnels, juridiques, financiers, médicaux ou de sécurité. Vous devez les vérifier, tester et valider avant de les utiliser, exécuter, publier ou livrer.</p></section>
          <section class="legal-section"><h2>7. Exécution de code, commandes distantes et données</h2><p>Vibeit exécute le code et les commandes que vous fournissez ou qu'un agent IA fournit à votre demande. Cela peut modifier ou supprimer des fichiers, consommer des ressources ou affecter les systèmes connectés. Vous acceptez ces risques et restez responsable des résultats.</p></section>
          <section class="legal-section"><h2>8. Sécurité et perte de données</h2><p>Nous utilisons le Trousseau et les transports chiffrés, mais aucun logiciel, stockage ou transport n'est entièrement sûr. Nous ne garantissons pas que l'app sera exempte d'erreurs, d'interruptions, de vulnérabilités, de pertes de données ou d'accès non autorisés.</p></section>
          <section class="legal-section"><h2>9. Abonnements et paiements</h2><p>Certaines fonctions peuvent nécessiter un abonnement payant via Apple In-App Purchase. Le paiement est facturé à votre compte Apple et se renouvelle automatiquement sauf annulation dans les délais. Apple traite paiements et remboursements selon ses conditions.</p></section>
          <section class="legal-section"><h2 class="legal">10. Exclusion de garanties</h2><p class="legal">L'app est fournie "telle quelle" et "selon disponibilité", sans garantie d'aucune sorte, expresse, implicite ou légale, y compris les garanties de qualité marchande, d'adéquation à un usage particulier, de titre, d'exactitude et de non-contrefaçon.</p></section>
          <section class="legal-section"><h2 class="legal">11. Limitation de responsabilité</h2><p class="legal">Dans toute la mesure permise par la loi, nous ne sommes pas responsables des dommages indirects, accessoires, spéciaux, consécutifs, exemplaires ou punitifs, ni des pertes de profits, revenus, données, clientèle ou autres pertes immatérielles liées à l'app, aux sorties IA, au code exécuté, aux pertes de données, incidents de sécurité ou services tiers. Notre responsabilité totale ne dépassera pas le plus élevé entre le montant payé au cours des douze mois précédant la réclamation et 10 USD.</p></section>
          <section class="legal-section"><h2>12. Indemnisation</h2><p>Dans la mesure permise par la loi, vous acceptez de nous indemniser pour les réclamations et frais découlant de votre mauvaise utilisation, violation des Conditions ou de la loi, code, données, contenu ou usage de services ou systèmes tiers.</p></section>
          <section class="legal-section"><h2>13. Résiliation</h2><p>Vous pouvez cesser d'utiliser l'app à tout moment en la supprimant. Nous pouvons suspendre ou résilier la licence en cas de violation substantielle ou d'usage illégal. Les clauses destinées à survivre continueront de s'appliquer.</p></section>
          <section class="legal-section"><h2>14. Conditions Apple App Store</h2><p>Ces Conditions sont conclues entre vous et nous, non avec Apple. Apple n'est pas responsable de l'app ou de son contenu et n'a aucune obligation de maintenance ou de support. Apple et ses filiales sont bénéficiaires tiers.</p></section>
          <section class="legal-section"><h2>15. Droit applicable</h2><p>Ces Conditions sont régies par les lois de la juridiction où le développeur est établi, sauf application obligatoire des lois de protection des consommateurs de votre résidence.</p></section>
          <section class="legal-section"><h2>16. Modifications</h2><p>Nous pouvons mettre à jour ces Conditions. Nous modifierons la date de mise à jour et fournirons un avis approprié pour les changements importants. L'utilisation continue vaut acceptation.</p></section>
          <section class="legal-section"><h2>17. Contact</h2><p>Questions : <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>.</p></section>`
      },
      contact: {
        title: "Contact",
        description: "Contacter Vibeit : suggérer une fonctionnalité ou signaler un problème.",
        body: `
          <h1>Nous contacter</h1>
          <p class="updated">Envoyez une idée ou signalez un problème — nous lisons chaque message.</p>`
      }
    },

    it: {
      privacy: {
        title: "Informativa sulla Privacy",
        description: "Informativa sulla privacy di Vibeit, IDE Python nativo per iPadOS, iOS e macOS.",
        body: `
          <h1>Informativa sulla Privacy</h1><p class="updated">Ultimo aggiornamento: 6 luglio 2026</p>
          <p>Questa informativa spiega come <strong>Vibeit</strong> ("l'app", "noi") gestisce le informazioni quando usi Vibeit su iPadOS, iOS e macOS. Vibeit è un IDE Python nativo progettato per funzionare sul tuo dispositivo. Il codice gira in un kernel Python locale e file, credenziali e chiavi API restano sul tuo dispositivo.</p>
          <div class="tldr"><strong>In breve.</strong> Non gestiamo server di analytics o pubblicità e l'app non contiene SDK di tracciamento o pubblicità di terze parti. Non vendiamo informazioni personali. I dati lasciano il dispositivo solo quando usi una funzione che lo richiede, per esempio chiamare un provider IA con la tua chiave, connettere un server remoto o scaricare un pacchetto.</div>
          <section class="legal-section"><h2>1. Informazioni salvate sul dispositivo</h2><p>Notebook, script, file di lavoro, codice e output Python locali, chiavi API, credenziali SSH e impostazioni dell'app restano sul dispositivo o nello storage iCloud/Files scelto. Non ne riceviamo copie. I segreti sono salvati nel Portachiavi e non vengono scritti in notebook o log né trasmessi a noi.</p></section>
          <section class="legal-section"><h2>2. Rilevamento lingua del sito</h2><p>Queste pagine possono chiedere a GeoJS un codice paese per scegliere la lingua iniziale in base alla posizione IP. Il codice paese viene usato solo nel browser per la scelta della lingua. Se non funziona, la pagina usa la lingua del browser e poi l'inglese. La scelta manuale viene salvata in localStorage su questo dispositivo.</p></section>
          <section class="legal-section"><h2>3. Funzioni che inviano dati a terzi</h2><p>Quando usi assistenza IA, connessioni SSH/SFTP o Cloudflare Access, o download di pacchetti, i dati pertinenti vengono inviati alla terza parte interessata e sono soggetti alle sue policy. Vibeit agisce solo come client. Non riceviamo prompt IA, risposte o contenuti delle sessioni remote.</p></section>
          <section class="legal-section"><h2>4. Abbonamenti e pagamenti</h2><p>Gli abbonamenti Vibeit sono venduti tramite <strong>Apple In-App Purchase</strong>. Apple gestisce pagamento e abbonamento; non riceviamo né conserviamo i dati della carta. L'app riceve solo lo stato di abbonamento o diritto tramite StoreKit.</p></section>
          <section class="legal-section"><h2>5. Informazioni che raccogliamo</h2><p>Non manteniamo account utente e non gestiamo backend che raccolgono informazioni personali. L'app non include analytics o pubblicità di terze parti. Se ci contatti via email, riceviamo le informazioni che decidi di includere.</p></section>
          <section class="legal-section"><h2>6. Sicurezza dei dati</h2><p>I segreti sono salvati nel Portachiavi del sistema. Le connessioni di rete usano TLS o SSH. Nessun metodo è sicuro al 100%, ma usiamo le protezioni della piattaforma Apple e trasporti cifrati.</p></section>
          <section class="legal-section"><h2>7. Conservazione ed eliminazione</h2><p>Poiché i dati vivono sul tuo dispositivo, li controlli tu. Puoi eliminare file, host e credenziali nell'app; rimuovere l'app elimina dati locali ed elementi Keychain associati. I dati già inviati a terzi seguono le loro policy.</p></section>
          <section class="legal-section"><h2>8. Privacy dei minori</h2><p>Vibeit è uno strumento per sviluppatori e non è rivolto a minori di 13 anni o all'età minima equivalente nella tua giurisdizione. Non raccogliamo consapevolmente informazioni personali da minori.</p></section>
          <section class="legal-section"><h2>9. Utenti internazionali e diritti</h2><p>A seconda del luogo in cui vivi, potresti avere diritti di accesso, correzione, eliminazione o limitazione del trattamento. Poiché non conserviamo dati personali sui nostri server, la maggior parte delle richieste si gestisce sul dispositivo o presso il provider terzo rilevante.</p></section>
          <section class="legal-section"><h2>10. Modifiche</h2><p>Possiamo aggiornare questa informativa. Modificheremo la data di ultimo aggiornamento e daremo avviso appropriato per cambiamenti importanti.</p></section>
          <section class="legal-section"><h2>11. Contatti</h2><p>Domande: <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>.</p></section>`
      },
      support: {
        title: "Assistenza",
        description: "Assistenza e aiuto per Vibeit, IDE Python nativo per iPadOS, iOS e macOS.",
        body: `
          <h1>Assistenza</h1><p class="updated">Vibeit - IDE Python nativo per iPadOS, iOS e macOS.</p>
          <div class="tldr"><strong>Serve aiuto?</strong> Scrivi a <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>. Di solito rispondiamo entro 1-2 giorni lavorativi.</div>
          <p><a class="contact-btn" href="mailto:aroluo@icloud.com?subject=Vibeit%20Support">Contatta assistenza</a></p>
          <section class="legal-section"><h2>Per iniziare</h2><p>Vibeit è un IDE Python completo che gira sul tuo dispositivo. Crea un notebook o script, scrivi Python e premi Run. Il codice viene eseguito in un kernel locale con notebooks, matplotlib, NumPy, pandas, PyTorch e altro. Non serve Internet per eseguire il codice.</p></section>
          <section class="legal-section"><h2>Domande frequenti</h2><h3>Cosa include la versione gratuita rispetto all'abbonamento?</h3><p>Il piano <strong>Standard</strong> include l'IDE Python locale principale. <strong>Pro</strong> aggiunge server SSH/SFTP e terminale, GitHub clone/push/pull e pull request, e provider IA cloud. Ogni piano inizia con una <strong>prova gratuita di 7 giorni</strong>.</p><h3>Come avvio la prova o mi abbono?</h3><p>Apri <strong>Settings -> Account</strong>, scegli un piano e tocca <strong>Start Free Trial</strong>. Il pagamento è gestito da Apple tramite il tuo account Apple.</p><h3>Come gestisco o annullo l'abbonamento?</h3><p>Nell'app <strong>Impostazioni</strong> del dispositivo, tocca il tuo nome, apri <strong>Abbonamenti</strong>, poi <strong>Vibeit</strong>. Puoi anche <a href="https://apps.apple.com/account/subscriptions">gestire gli abbonamenti qui</a>.</p><h3>Come ripristino un acquisto?</h3><p>Su un nuovo dispositivo o dopo reinstallazione, apri <strong>Settings -> Account</strong> in Vibeit e tocca <strong>Restore Purchases</strong>. Usa lo stesso account Apple.</p><h3>Come connetto un server remoto o GitHub?</h3><p>Aggiungi un host SSH/SFTP in <strong>Settings -> Remote</strong> oppure collega GitHub in <strong>Settings -> Source Control</strong>. Le credenziali restano nel Portachiavi.</p><h3>Come uso il mio provider IA?</h3><p>In <strong>Settings -> AI</strong>, aggiungi provider e chiave API. La chiave resta sul dispositivo e serve solo per comunicare direttamente con quel provider.</p><h3>Dove installo pacchetti Python aggiuntivi?</h3><p>Usa il catalogo integrato per installare pacchetti pure-Python e nativi precompilati supportati.</p></section>
          <section class="legal-section"><h2>Privacy e dati</h2><p>Vibeit è privato per impostazione predefinita. Vedi la nostra <a href="privacy.html">Informativa sulla Privacy</a>.</p></section>
          <section class="legal-section"><h2>Contatti</h2><p>Per bug, domande o richieste, scrivi a <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> con modello del dispositivo e versione iOS/iPadOS.</p></section>`
      },
      terms: {
        title: "Termini di Utilizzo",
        description: "Termini di utilizzo di Vibeit, IDE Python nativo per iPadOS, iOS e macOS.",
        body: `
          <h1>Termini di Utilizzo</h1><p class="updated">Ultimo aggiornamento: 6 luglio 2026</p>
          <p>Questi Termini di Utilizzo ("Termini") sono un accordo legale tra te e lo sviluppatore di <strong>Vibeit</strong> per il download e l'uso dell'app Vibeit su iPadOS, iOS e macOS. Scaricando, installando o usando Vibeit, accetti i Termini.</p>
          <div class="tldr"><strong>In breve.</strong> Vibeit è uno strumento per sviluppatori che esegue Python e funzioni opzionali di IA e rete sul tuo dispositivo e tramite i servizi che colleghi. Sei responsabile di codice, dati, credenziali e uso. L'app è fornita "così com'è".</div>
          <section class="legal-section"><h2>1. Idoneità e accettazione</h2><p>Devi avere almeno 13 anni o l'età minima applicabile e poter concludere un contratto. Se usi l'app per un'organizzazione, dichiari di essere autorizzato ad accettare i Termini per essa. Si applica anche il <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Licensed Application End User License Agreement</a> di Apple.</p></section>
          <section class="legal-section"><h2>2. Cos'è Vibeit</h2><p>Vibeit è un IDE nativo per notebook e script Python che esegue codice in un runtime Python locale. Le funzioni opzionali includono provider IA configurati da te, connessioni SSH/SFTP, Cloudflare Access, GitHub e download di pacchetti Python. Questi servizi sono gestiti da te o da terzi.</p></section>
          <section class="legal-section"><h2>3. Licenza</h2><p>Nel rispetto dei Termini e dell'EULA Apple, ti concediamo una licenza personale, limitata, non esclusiva, non trasferibile e revocabile per usare Vibeit su dispositivi Apple che possiedi o controlli, per uso personale o aziendale interno lecito.</p></section>
          <section class="legal-section"><h2>4. Responsabilità e uso accettabile</h2><p>Sei l'unico responsabile del codice eseguito, dei dati trattati, delle credenziali inserite e dei sistemi collegati. Non puoi usare Vibeit per violare leggi, diritti, accedere senza autorizzazione, sviluppare malware, condurre attacchi, divulgare dati non autorizzati o aggirare limiti di sicurezza o uso. Sei responsabile di dispositivo, chiavi, credenziali, token e backup.</p></section>
          <section class="legal-section"><h2>5. Servizi di terze parti</h2><p>Provider IA, host remoti, Cloudflare Access, GitHub e indici di pacchetti sono regolati dai termini e dalle policy delle rispettive terze parti. Non li gestiamo o controlliamo e non siamo responsabili di disponibilità, contenuti, sicurezza, azioni o costi.</p></section>
          <section class="legal-section"><h2>6. Funzioni IA e output generato</h2><p>Le funzioni IA possono produrre contenuti inaccurati, incompleti, insicuri, distorti o inadatti. L'output IA non è consulenza professionale, legale, finanziaria, medica o di sicurezza. Devi verificarlo, testarlo e validarlo prima di usarlo, eseguirlo, pubblicarlo o distribuirlo.</p></section>
          <section class="legal-section"><h2>7. Esecuzione di codice, comandi remoti e dati</h2><p>Vibeit esegue codice e comandi forniti da te o, su tua istruzione, da un agente IA. L'esecuzione può modificare o eliminare file, consumare risorse o influire sui sistemi collegati. Accetti questi rischi e sei responsabile dei risultati.</p></section>
          <section class="legal-section"><h2>8. Sicurezza e perdita dati</h2><p>Usiamo Portachiavi e trasporti cifrati, ma nessun software, storage o trasmissione è completamente sicuro. Non garantiamo che l'app sia priva di errori, interruzioni, vulnerabilità, perdita dati o accessi non autorizzati.</p></section>
          <section class="legal-section"><h2>9. Abbonamenti e pagamenti</h2><p>Alcune funzioni possono richiedere un abbonamento tramite Apple In-App Purchase. Il pagamento è addebitato all'account Apple e si rinnova automaticamente se non annullato nei tempi previsti. Apple gestisce pagamenti e rimborsi secondo i suoi termini.</p></section>
          <section class="legal-section"><h2 class="legal">10. Esclusione di garanzie</h2><p class="legal">L'app è fornita "così com'è" e "secondo disponibilità", senza garanzie di alcun tipo, espresse, implicite o legali, incluse garanzie di commerciabilità, idoneità a uno scopo particolare, titolo, accuratezza e non violazione.</p></section>
          <section class="legal-section"><h2 class="legal">11. Limitazione di responsabilità</h2><p class="legal">Nella misura massima consentita dalla legge, non saremo responsabili di danni indiretti, incidentali, speciali, consequenziali, esemplari o punitivi, né di perdita di profitti, ricavi, dati, avviamento o altre perdite immateriali collegate all'app, output IA, codice eseguito, perdita dati, incidenti di sicurezza o servizi terzi. La responsabilità totale non supererà l'importo pagato nei dodici mesi precedenti il reclamo o 10 USD, se maggiore.</p></section>
          <section class="legal-section"><h2>12. Manleva</h2><p>Nella misura consentita dalla legge, accetti di manlevarci da reclami e costi derivanti da uso improprio dell'app, violazione dei Termini o della legge, codice, dati, contenuti o uso di servizi o sistemi terzi.</p></section>
          <section class="legal-section"><h2>13. Risoluzione</h2><p>Puoi smettere di usare l'app in qualsiasi momento eliminandola. Possiamo sospendere o terminare la licenza in caso di violazione sostanziale o uso illecito. Le clausole destinate a sopravvivere continueranno ad applicarsi.</p></section>
          <section class="legal-section"><h2>14. Termini Apple App Store</h2><p>Questi Termini sono tra te e noi, non con Apple. Apple non è responsabile dell'app o del suo contenuto e non ha obbligo di manutenzione o supporto. Apple e le sue controllate sono beneficiari terzi.</p></section>
          <section class="legal-section"><h2>15. Legge applicabile</h2><p>I Termini sono regolati dalle leggi della giurisdizione in cui lo sviluppatore è stabilito, salvo applicazione obbligatoria delle leggi di tutela dei consumatori del tuo luogo di residenza.</p></section>
          <section class="legal-section"><h2>16. Modifiche</h2><p>Possiamo aggiornare i Termini. Cambieremo la data di aggiornamento e daremo avviso appropriato per modifiche importanti. L'uso continuato vale come accettazione.</p></section>
          <section class="legal-section"><h2>17. Contatti</h2><p>Domande: <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>.</p></section>`
      },
      contact: {
        title: "Contatti",
        description: "Contatta Vibeit: suggerisci una funzionalità o segnala un problema.",
        body: `
          <h1>Contattaci</h1>
          <p class="updated">Invia un'idea o segnala un problema — leggiamo ogni messaggio.</p>`
      }
    },

    de: {
      privacy: {
        title: "Datenschutzerklärung",
        description: "Datenschutzerklärung für Vibeit, die native Python-IDE für iPadOS, iOS und macOS.",
        body: `
          <h1>Datenschutzerklärung</h1><p class="updated">Zuletzt aktualisiert: 6. Juli 2026</p>
          <p>Diese Erklärung beschreibt, wie <strong>Vibeit</strong> ("die App", "wir") Informationen verarbeitet, wenn du Vibeit auf iPadOS, iOS und macOS nutzt. Vibeit ist eine native Python-IDE für dein Gerät. Code läuft in einem lokalen Python-Kernel, und Dateien, Zugangsdaten und API-Schlüssel bleiben auf deinem Gerät.</p>
          <div class="tldr"><strong>Kurzfassung.</strong> Wir betreiben keine Analyse- oder Werbeserver, und die App enthält keine Tracking- oder Werbe-SDKs Dritter. Wir verkaufen keine personenbezogenen Informationen. Daten verlassen dein Gerät nur, wenn du eine Funktion nutzt, die dies erfordert, etwa einen KI-Anbieter mit deinem eigenen Schlüssel, eine Remote-Verbindung oder einen Paketdownload.</div>
          <section class="legal-section"><h2>1. Informationen auf deinem Gerät</h2><p>Notebooks, Skripte, Arbeitsdateien, lokal ausgeführter Python-Code und Ausgaben, API-Schlüssel, SSH-Zugangsdaten und App-Einstellungen bleiben auf deinem Gerät oder in deinem gewählten iCloud/Files-Speicher. Wir erhalten keine Kopien. Geheimnisse werden im Schlüsselbund gespeichert und nicht in Notebooks oder Logs geschrieben oder an uns übertragen.</p></section>
          <section class="legal-section"><h2>2. Spracherkennung der Website</h2><p>Diese Seiten können bei GeoJS einen Ländercode abfragen, um anhand deiner IP-Region die anfängliche Sprache zu wählen. Der Ländercode wird nur im Browser zur Sprachauswahl verwendet. Wenn die Abfrage fehlschlägt, nutzt die Seite die Browsersprache und danach Englisch. Deine manuelle Auswahl wird auf diesem Gerät in localStorage gespeichert.</p></section>
          <section class="legal-section"><h2>3. Funktionen mit Datenübertragung an Dritte</h2><p>Wenn du KI-Unterstützung, SSH/SFTP oder Cloudflare Access, Remote-Verbindungen oder Paketdownloads nutzt, werden relevante Daten an den jeweiligen Dritten gesendet und unterliegen dessen Richtlinien. Vibeit handelt nur als Client. Wir erhalten keine KI-Prompts, Antworten oder Remote-Sitzungsinhalte.</p></section>
          <section class="legal-section"><h2>4. Abonnements und Zahlungen</h2><p>Vibeit-Abonnements werden über <strong>Apple In-App Purchase</strong> verkauft. Apple verarbeitet Zahlungen und verwaltet Abonnements; wir erhalten oder speichern keine Kartendaten. Die App erhält nur den Abo- oder Berechtigungsstatus über StoreKit.</p></section>
          <section class="legal-section"><h2>5. Von uns erfasste Informationen</h2><p>Wir führen keine Benutzerkonten und betreiben kein Backend, das personenbezogene Informationen sammelt. Die App enthält keine Analyse oder Werbung Dritter. Wenn du uns per E-Mail kontaktierst, erhalten wir die Informationen, die du freiwillig angibst.</p></section>
          <section class="legal-section"><h2>6. Datensicherheit</h2><p>Geheimnisse werden im System-Schlüsselbund gespeichert. Netzwerkverbindungen nutzen TLS oder SSH. Kein Verfahren ist zu 100 % sicher, aber wir verwenden Apple-Plattformschutz und verschlüsselte Übertragung.</p></section>
          <section class="legal-section"><h2>7. Aufbewahrung und Löschung</h2><p>Da deine Daten auf deinem Gerät liegen, kontrollierst du sie. Du kannst Dateien, Hosts und Zugangsdaten in der App löschen; das Entfernen der App löscht lokale Daten und zugehörige Schlüsselbund-Einträge. Bereits an Dritte gesendete Daten unterliegen deren Richtlinien.</p></section>
          <section class="legal-section"><h2>8. Datenschutz von Kindern</h2><p>Vibeit ist ein Entwicklerwerkzeug und richtet sich nicht an Kinder unter 13 Jahren oder dem entsprechenden Mindestalter in deiner Region. Wir erfassen nicht wissentlich personenbezogene Informationen von Kindern.</p></section>
          <section class="legal-section"><h2>9. Internationale Nutzer und Rechte</h2><p>Je nach Wohnort können dir Rechte auf Auskunft, Berichtigung, Löschung oder Einschränkung der Verarbeitung zustehen. Da wir keine personenbezogenen Informationen auf eigenen Servern speichern, werden die meisten Anfragen direkt auf deinem Gerät oder beim betreffenden Drittanbieter erfüllt.</p></section>
          <section class="legal-section"><h2>10. Änderungen</h2><p>Wir können diese Erklärung aktualisieren. Wir ändern das Datum und informieren bei wesentlichen Änderungen angemessen.</p></section>
          <section class="legal-section"><h2>11. Kontakt</h2><p>Fragen: <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>.</p></section>`
      },
      support: {
        title: "Support",
        description: "Support und Hilfe für Vibeit, die native Python-IDE für iPadOS, iOS und macOS.",
        body: `
          <h1>Support</h1><p class="updated">Vibeit - native Python-IDE für iPadOS, iOS und macOS.</p>
          <div class="tldr"><strong>Brauchst du Hilfe?</strong> Schreib an <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>. Wir antworten normalerweise innerhalb von 1-2 Werktagen.</div>
          <p><a class="contact-btn" href="mailto:aroluo@icloud.com?subject=Vibeit%20Support">Support kontaktieren</a></p>
          <section class="legal-section"><h2>Erste Schritte</h2><p>Vibeit ist eine vollständige Python-IDE, die auf deinem Gerät läuft. Erstelle ein Notebook oder Skript, schreibe Python und führe es aus. Der Code läuft in einem On-Device-Kernel mit Notebooks, matplotlib, NumPy, pandas, PyTorch und mehr. Zum Ausführen deines Codes ist keine Internetverbindung nötig.</p></section>
          <section class="legal-section"><h2>Häufige Fragen</h2><h3>Was ist in der kostenlosen Version und im Abo enthalten?</h3><p>Der <strong>Standard</strong>-Plan enthält die zentrale lokale Python-IDE. <strong>Pro</strong> ergänzt SSH/SFTP-Remote-Server und Terminal, GitHub clone/push/pull und Pull Requests sowie Cloud-KI-Anbieter. Jeder Plan startet mit einer <strong>7-tägigen kostenlosen Testphase</strong>.</p><h3>Wie starte ich die Testphase oder abonniere?</h3><p>Öffne <strong>Settings -> Account</strong>, wähle einen Plan und tippe <strong>Start Free Trial</strong>. Die Zahlung läuft über Apple und dein Apple-Konto.</p><h3>Wie verwalte oder kündige ich das Abo?</h3><p>Öffne die <strong>Einstellungen</strong>-App, tippe deinen Namen, öffne <strong>Abonnements</strong> und wähle <strong>Vibeit</strong>. Du kannst Abos auch <a href="https://apps.apple.com/account/subscriptions">hier verwalten</a>.</p><h3>Wie stelle ich einen Kauf wieder her?</h3><p>Auf einem neuen Gerät oder nach Neuinstallation öffne in Vibeit <strong>Settings -> Account</strong> und tippe <strong>Restore Purchases</strong>. Verwende dasselbe Apple-Konto.</p><h3>Wie verbinde ich Remote-Server oder GitHub?</h3><p>Füge unter <strong>Settings -> Remote</strong> einen SSH/SFTP-Host hinzu oder verbinde GitHub unter <strong>Settings -> Source Control</strong>. Zugangsdaten bleiben im Schlüsselbund.</p><h3>Wie nutze ich meinen eigenen KI-Anbieter?</h3><p>Unter <strong>Settings -> AI</strong> fügst du Anbieter und API-Schlüssel hinzu. Der Schlüssel bleibt auf deinem Gerät und wird nur zur direkten Kommunikation mit diesem Anbieter genutzt.</p><h3>Wo installiere ich zusätzliche Python-Pakete?</h3><p>Nutze den Paketkatalog in der App, um unterstützte pure-Python- und vorgefertigte native Pakete zu installieren.</p></section>
          <section class="legal-section"><h2>Datenschutz und Daten</h2><p>Vibeit ist standardmäßig privat. Siehe unsere <a href="privacy.html">Datenschutzerklärung</a>.</p></section>
          <section class="legal-section"><h2>Kontakt</h2><p>Für Fehler, Fragen oder Funktionswünsche schreibe mit Gerätemodell und iOS/iPadOS-Version an <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>.</p></section>`
      },
      terms: {
        title: "Nutzungsbedingungen",
        description: "Nutzungsbedingungen für Vibeit, die native Python-IDE für iPadOS, iOS und macOS.",
        body: `
          <h1>Nutzungsbedingungen</h1><p class="updated">Zuletzt aktualisiert: 6. Juli 2026</p>
          <p>Diese Nutzungsbedingungen ("Bedingungen") sind eine rechtliche Vereinbarung zwischen dir und dem Entwickler von <strong>Vibeit</strong> über Download und Nutzung der Vibeit-App auf iPadOS, iOS und macOS. Durch Download, Installation oder Nutzung stimmst du diesen Bedingungen zu.</p>
          <div class="tldr"><strong>Kurzfassung.</strong> Vibeit ist ein Entwicklerwerkzeug, das Python sowie optionale KI- und Netzwerkfunktionen auf deinem Gerät und über von dir verbundene Dienste ausführt. Du bist für Code, Daten, Zugangsdaten und Nutzung verantwortlich. Die App wird "wie besehen" bereitgestellt.</div>
          <section class="legal-section"><h2>1. Berechtigung und Annahme</h2><p>Du musst mindestens 13 Jahre alt oder im geltenden Mindestalter sein und einen wirksamen Vertrag schließen können. Wenn du die App für eine Organisation nutzt, bestätigst du deine Befugnis, diese Bedingungen für sie anzunehmen. Zusätzlich gilt Apples <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Licensed Application End User License Agreement</a>.</p></section>
          <section class="legal-section"><h2>2. Was Vibeit ist</h2><p>Vibeit ist eine native Python-Notebook- und Skript-IDE, die Code in einer lokalen Python-Laufzeit ausführt. Optionale Funktionen umfassen von dir konfigurierte KI-Anbieter, SSH/SFTP-Verbindungen, Cloudflare Access, GitHub und Python-Paketdownloads. Diese Dienste werden von dir oder Dritten betrieben.</p></section>
          <section class="legal-section"><h2>3. Lizenz</h2><p>Vorbehaltlich dieser Bedingungen und der Apple EULA gewähren wir dir eine persönliche, beschränkte, nicht exklusive, nicht übertragbare und widerrufliche Lizenz zur Nutzung von Vibeit auf Apple-Geräten, die du besitzt oder kontrollierst, für rechtmäßige persönliche oder interne geschäftliche Zwecke.</p></section>
          <section class="legal-section"><h2>4. Verantwortung und zulässige Nutzung</h2><p>Du bist allein verantwortlich für ausgeführten Code, verarbeitete Daten, eingegebene Zugangsdaten und verbundene Systeme. Du darfst Vibeit nicht nutzen, um Gesetze zu verletzen, Rechte zu verletzen, unbefugt zuzugreifen, Malware zu entwickeln, Angriffe durchzuführen, unerlaubt Daten offenzulegen oder Sicherheits- und Nutzungslimits zu umgehen. Geräte-, Schlüssel-, Zugangsdaten-, Token- und Backup-Sicherheit liegen bei dir.</p></section>
          <section class="legal-section"><h2>5. Dienste Dritter</h2><p>Für KI-Anbieter, Remote-Hosts, Cloudflare Access, GitHub und Paketindizes gelten die Bedingungen und Datenschutzrichtlinien der jeweiligen Dritten. Wir betreiben oder kontrollieren diese Dienste nicht und sind nicht verantwortlich für Verfügbarkeit, Inhalte, Sicherheit, Handlungen oder Kosten.</p></section>
          <section class="legal-section"><h2>6. KI-Funktionen und generierte Ausgaben</h2><p>KI-Funktionen können ungenaue, unvollständige, unsichere, voreingenommene oder ungeeignete Inhalte erzeugen. KI-Ausgaben sind keine professionelle, rechtliche, finanzielle, medizinische oder sicherheitsbezogene Beratung. Du musst sie prüfen, testen und validieren, bevor du dich darauf verlässt, sie ausführst, veröffentlichst oder auslieferst.</p></section>
          <section class="legal-section"><h2>7. Codeausführung, Remote-Befehle und Daten</h2><p>Vibeit führt Code und Befehle aus, die du oder auf deine Anweisung ein KI-Agent bereitstellen. Ausführung kann Dateien ändern oder löschen, Ressourcen verbrauchen oder verbundene Systeme beeinflussen. Du akzeptierst diese Risiken und bist für Ergebnisse verantwortlich.</p></section>
          <section class="legal-section"><h2>8. Sicherheit und Datenverlust</h2><p>Wir verwenden Schlüsselbund und verschlüsselte Übertragung, aber keine Software, Speicherung oder Übertragung ist vollständig sicher. Wir garantieren nicht, dass die App fehlerfrei, unterbrechungsfrei, frei von Schwachstellen, Datenverlust oder unbefugtem Zugriff ist.</p></section>
          <section class="legal-section"><h2>9. Abonnements und Zahlungen</h2><p>Einige Funktionen können ein kostenpflichtiges Abo über Apple In-App Purchase erfordern. Zahlungen werden deinem Apple-Konto belastet und verlängern sich automatisch, sofern sie nicht rechtzeitig gekündigt werden. Apple verarbeitet Zahlungen und Rückerstattungen nach seinen Bedingungen.</p></section>
          <section class="legal-section"><h2 class="legal">10. Gewährleistungsausschluss</h2><p class="legal">Die App wird "wie besehen" und "wie verfügbar" ohne Garantien jeglicher Art bereitgestellt, ausdrücklich, stillschweigend oder gesetzlich, einschließlich Garantien der Marktgängigkeit, Eignung für einen bestimmten Zweck, Rechtsinhaberschaft, Genauigkeit und Nichtverletzung.</p></section>
          <section class="legal-section"><h2 class="legal">11. Haftungsbeschränkung</h2><p class="legal">Soweit gesetzlich zulässig, haften wir nicht für indirekte, beiläufige, besondere, Folge-, exemplarische oder Strafschäden oder für Verluste von Gewinn, Umsatz, Daten, Goodwill oder anderen immateriellen Werten im Zusammenhang mit der App, KI-Ausgaben, ausgeführtem Code, Datenverlust, Sicherheitsvorfällen oder Drittanbietern. Unsere Gesamthaftung übersteigt nicht den höheren Betrag aus den in den zwölf Monaten vor dem Anspruch gezahlten Beträgen oder 10 USD.</p></section>
          <section class="legal-section"><h2>12. Freistellung</h2><p>Soweit gesetzlich zulässig, stellst du uns von Ansprüchen und Kosten frei, die aus Missbrauch der App, Verletzung dieser Bedingungen oder des Gesetzes, deinem Code, deinen Daten, Inhalten oder der Nutzung verbundener Dienste oder Systeme entstehen.</p></section>
          <section class="legal-section"><h2>13. Beendigung</h2><p>Du kannst die Nutzung jederzeit durch Löschen der App beenden. Wir können die Lizenz bei wesentlicher Verletzung oder rechtswidriger Nutzung aussetzen oder beenden. Bestimmungen, die ihrem Wesen nach fortgelten sollen, bleiben bestehen.</p></section>
          <section class="legal-section"><h2>14. Apple App Store Bedingungen</h2><p>Diese Bedingungen bestehen zwischen dir und uns, nicht mit Apple. Apple ist nicht für die App oder Inhalte verantwortlich und hat keine Wartungs- oder Supportpflicht. Apple und seine Tochtergesellschaften sind Drittbegünstigte.</p></section>
          <section class="legal-section"><h2>15. Anwendbares Recht</h2><p>Diese Bedingungen unterliegen dem Recht der Gerichtsbarkeit, in der der Entwickler ansässig ist, außer zwingende Verbraucherschutzgesetze deines Wohnorts gelten anderweitig.</p></section>
          <section class="legal-section"><h2>16. Änderungen</h2><p>Wir können diese Bedingungen aktualisieren. Wir ändern das Datum und informieren bei wesentlichen Änderungen angemessen. Fortgesetzte Nutzung gilt als Annahme.</p></section>
          <section class="legal-section"><h2>17. Kontakt</h2><p>Fragen: <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>.</p></section>`
      },
      contact: {
        title: "Kontakt",
        description: "Vibeit kontaktieren: Funktionswunsch senden oder Problem melden.",
        body: `
          <h1>Kontakt</h1>
          <p class="updated">Schick uns einen Funktionswunsch oder melde ein Problem — wir lesen jede Nachricht.</p>`
      }
    },
    ar: {
      privacy: {
        title: "سياسة الخصوصية",
        description: "سياسة الخصوصية لـ Vibeit، بيئة تطوير بايثون الأصلية لـ iPadOS و iOS و macOS.",
        body: `
          <h1>سياسة الخصوصية</h1>
          <p class="updated">آخر تحديث: 6 يوليو 2026</p>
          <p>توضّح سياسة الخصوصية هذه كيف يتعامل <strong>Vibeit</strong> ("Vibeit"، "التطبيق"، "نحن") مع المعلومات عند استخدامك تطبيق Vibeit على iPadOS و iOS و macOS. إن Vibeit بيئة تطوير أصلية لدفاتر بايثون صُمّمت لتعمل على جهازك. بنيناه ليكون خاصًا افتراضيًا: تعمل شيفرتك في نواة بايثون على الجهاز، وتبقى ملفاتك وبيانات اعتمادك ومفاتيح واجهات البرمجة على جهازك.</p>
          <div class="tldr"><strong>باختصار.</strong> لا نشغّل خوادم تحليلات أو إعلانات، ولا يحتوي التطبيق على أي حزم تتبّع أو إعلانات من طرف ثالث. لا نبيع معلوماتك الشخصية. ولا تغادر البيانات جهازك إلا عندما <em>تستخدم أنت</em> ميزة تتطلّب ذلك، مثل استدعاء مزوّد ذكاء اصطناعي بمفتاحك الخاص، أو الاتصال بخادم بعيد أعددته، أو تنزيل حزمة.</div>

          <section class="legal-section"><h2>1. المعلومات المخزّنة على جهازك</h2>
          <p>يبقى ما يلي على جهازك، وفي مساحة iCloud أو الملفات الخاصة بك إن اخترت الحفظ هناك. ولا نتلقّى نسخًا منه:</p>
          <ul>
            <li><strong>الدفاتر والنصوص البرمجية وملفات مساحة العمل</strong> التي تنشئها أو تفتحها.</li>
            <li><strong>تنفيذ بايثون</strong>: تعمل الشيفرة في نواة محلية؛ ولا تُرسل شيفرتك ولا مخرجاتها إلينا.</li>
            <li><strong>بيانات الاعتماد والأسرار</strong>: تُخزَّن مفاتيح واجهات البرمجة وكلمات مرور SSH وعبارات مرور المفاتيح ورموز Cloudflare Access في <strong>Keychain</strong> على الجهاز، ولا تُكتب أبدًا في الدفاتر أو السجلات ولا تُرسل إلينا.</li>
            <li><strong>إعدادات التطبيق</strong>، مثل السمة واللغة وملفات تعريف المضيفين.</li>
          </ul></section>

          <section class="legal-section"><h2>2. اكتشاف لغة الموقع</h2>
          <p>قد تطلب هذه الصفحات استعلامًا عن البلد من GeoJS لاختيار لغة العرض الأولية بناءً على موقع عنوان IP الخاص بك. يعيد الاستعلام رمز بلد، ويُستخدم داخل متصفحك فقط لاختيار اللغة. وإذا أخفق، تعود الصفحة إلى لغة متصفحك ثم إلى الإنجليزية. يمكنك تغيير اللغة يدويًا؛ ويُحفظ اختيارك في localStorage على هذا الجهاز.</p></section>

          <section class="legal-section"><h2>3. الميزات التي ترسل بيانات إلى أطراف ثالثة</h2>
          <p>عندما تختار استخدام هذه الميزات، تُرسل البيانات إلى الطرف الثالث المعني بموجب سياسات الخصوصية الخاصة <em>به</em>. ولا يعمل Vibeit إلا كعميل.</p>
          <h3>مساعدة الذكاء الاصطناعي</h3><p>إذا فعّلت ميزات الذكاء الاصطناعي واستخدمت مزوّدًا سحابيًا، مثل OpenAI أو Anthropic، فإن المطالبات التي ترسلها والشيفرة أو السياق ذا الصلة تُنقل إلى ذلك المزوّد باستخدام مفتاح واجهة البرمجة أو تسجيل الدخول الذي قدّمته. أما Apple Intelligence أو النماذج الأساسية العاملة على الجهاز، حيثما استُخدمت، فتعمل على جهازك. ولا نتلقّى مطالباتك ولا ردودها.</p>
          <h3>الاتصالات البعيدة</h3><p>إذا أعددت مضيفًا بعيدًا، يتصل Vibeit مباشرة بالخادم الذي <em>تحدّده أنت</em> لتشغيل الأوامر أو نقل الملفات أو تشغيل بايثون. وبالنسبة للمضيفين الذين يُوصل إليهم عبر Cloudflare Access، تُصادِق نافذة تسجيل دخول لدى مزوّد الهوية الخاص بك، ويُخزَّن رمز الوصول الناتج في Keychain. نحن لا نشغّل هذه الخوادم ولا نتلقّى محتويات جلساتك البعيدة.</p>
          <h3>تنزيل الحزم</h3><p>تُجلب الحزم المُدارة عبر HTTPS من فهارس حزم عامة، بما في ذلك هذا السجل المستضاف على GitHub. وكما في أي طلب ويب، قد يعالج مزوّد الاستضافة عنوان IP الخاص بك وبيانات الطلب الوصفية لتسليم الملفات.</p></section>

          <section class="legal-section"><h2>4. الاشتراكات والمدفوعات</h2>
          <p>تُباع اشتراكات Vibeit عبر <strong>الشراء داخل التطبيق من Apple</strong>. تعالج Apple دفعتك وتدير اشتراكك؛ ولا نتلقّى تفاصيل بطاقة الدفع أو نخزّنها أبدًا. ولا يتلقّى التطبيق من Apple عبر StoreKit سوى حالة اشتراكك أو استحقاقك لفتح الميزات. يمكنك إدارة اشتراكك أو إلغاؤه في أي وقت من إعدادات حساب Apple.</p></section>
          <section class="legal-section"><h2>5. المعلومات التي نجمعها</h2><p>لا نحتفظ بحسابات مستخدمين ولا نشغّل خادمًا خلفيًا يجمع معلوماتك الشخصية. ولا يتضمّن التطبيق تحليلات أو إعلانات من طرف ثالث. وإذا راسلتنا طلبًا للدعم عبر البريد الإلكتروني، فإننا نتلقّى المعلومات التي تختار تضمينها في رسالتك.</p></section>
          <section class="legal-section"><h2>6. أمن البيانات</h2><p>تُخزَّن الأسرار باستخدام Keychain في نظام التشغيل. وتستخدم اتصالات الشبكة تشفير TLS أو SSH. لا توجد طريقة تخزين أو نقل آمنة بنسبة 100 بالمئة، لكننا نعتمد على حماية منصة Apple والنقل المشفّر لصون معلوماتك.</p></section>
          <section class="legal-section"><h2>7. الاحتفاظ بالبيانات وحذفها</h2><p>لأن بياناتك تعيش على جهازك، فأنت من يتحكّم بها. يمكنك حذف الملفات والمضيفين وبيانات الاعتماد داخل التطبيق، وإزالة التطبيق تحذف بياناته المحلية وعناصر Keychain المرتبطة به. أما البيانات التي أُرسلت بالفعل إلى طرف ثالث فتخضع لسياسات ذلك الطرف.</p></section>
          <section class="legal-section"><h2>8. خصوصية الأطفال</h2><p>إن Vibeit أداة للمطوّرين وليست موجّهة إلى الأطفال دون سنّ 13 عامًا أو الحدّ الأدنى المكافئ للسنّ في ولايتك القضائية. ولا نجمع عن علم معلومات شخصية من الأطفال.</p></section>
          <section class="legal-section"><h2>9. المستخدمون الدوليون وحقوقك</h2><p>حسب مكان إقامتك، على سبيل المثال بموجب اللائحة العامة لحماية البيانات في الاتحاد الأوروبي أو قانوني CCPA و CPRA في كاليفورنيا، قد تكون لديك حقوق في الوصول إلى معلوماتك الشخصية أو تصحيحها أو حذفها أو تقييد معالجتها. ولأننا لا نجمع معلوماتك الشخصية ولا نخزّنها على خوادمنا، تُلبّى معظم الطلبات مباشرة على جهازك أو لدى المزوّد الخارجي المعني. ويمكنك أيضًا التواصل معنا عبر البيانات أدناه.</p></section>
          <section class="legal-section"><h2>10. التغييرات على هذه السياسة</h2><p>قد نحدّث سياسة الخصوصية هذه من حين لآخر. وسنراجع تاريخ "آخر تحديث" أعلاه، وسنقدّم إشعارًا مناسبًا عند التغييرات الجوهرية. ويشكّل استمرار استخدامك للتطبيق بعد التحديث قبولًا للسياسة المُعدَّلة.</p></section>
          <section class="legal-section"><h2>11. التواصل</h2><p>أسئلة حول هذه السياسة أو خصوصيتك؟ تواصل معنا عبر <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>.</p></section>`
      },
      support: {
        title: "الدعم",
        description: "الدعم والمساعدة لـ Vibeit، بيئة تطوير بايثون الأصلية لـ iPadOS و iOS و macOS.",
        body: `
          <h1>الدعم</h1>
          <p class="updated">Vibeit - بيئة تطوير بايثون أصلية لـ iPadOS و iOS و macOS.</p>
          <div class="tldr"><strong>تحتاج مساعدة؟</strong> راسلنا على <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> وسنعاود التواصل معك. عادةً نردّ خلال يوم إلى يومي عمل.</div>
          <p><a class="contact-btn" href="mailto:aroluo@icloud.com?subject=Vibeit%20Support">تواصل مع الدعم</a></p>
          <section class="legal-section"><h2>البداية</h2><p>إن Vibeit بيئة تطوير بايثون كاملة تعمل على جهازك. أنشئ دفترًا أو نصًّا برمجيًا، واكتب بايثون، ثم اضغط تشغيل. تُنفَّذ الشيفرة في نواة على الجهاز تدعم الدفاتر و matplotlib و NumPy و pandas و PyTorch وغيرها. ولا حاجة إلى اتصال بالإنترنت لتشغيل شيفرتك.</p></section>
          <section class="legal-section"><h2>الأسئلة الشائعة</h2>
          <h3>ما الفرق بين النسخة المجانية والاشتراك؟</h3><p>تتوفّر بيئة تطوير بايثون الأساسية على الجهاز ضمن الخطة <strong>العادية</strong>. وتضيف الخطة <strong>الاحترافية</strong> خوادم SSH و SFTP البعيدة والطرفية، واستنساخ GitHub والدفع والسحب وطلبات السحب، ومزوّدي الذكاء الاصطناعي السحابيين. وتبدأ كل خطة بـ <strong>تجربة مجانية لمدة 7 أيام</strong>.</p>
          <h3>كيف أبدأ التجربة المجانية أو أشترك؟</h3><p>افتح <strong>الإعدادات ثم الحساب</strong> داخل التطبيق، واختر خطة، ثم اضغط <strong>ابدأ التجربة المجانية</strong>. تتولّى Apple عملية الدفع عبر حساب Apple الخاص بك.</p>
          <h3>كيف أدير اشتراكي أو ألغيه؟</h3><p>تدير Apple الاشتراكات. على جهازك، افتح تطبيق <strong>الإعدادات</strong>، ثم اضغط على اسمك، ثم افتح <strong>الاشتراكات</strong>، ثم اختر <strong>Vibeit</strong>. ويمكنك أيضًا <a href="https://apps.apple.com/account/subscriptions">إدارة الاشتراكات من هنا</a>.</p>
          <h3>كيف أستعيد عملية شراء؟</h3><p>على جهاز جديد أو بعد إعادة التثبيت، افتح <strong>الإعدادات ثم الحساب</strong> في Vibeit واضغط <strong>استعادة المشتريات</strong>. وتأكّد من تسجيل الدخول بحساب Apple نفسه الذي اشتركت به.</p>
          <h3>كيف أتصل بخادم بعيد أو بـ GitHub؟</h3><p>اذهب إلى <strong>الإعدادات ثم عن بُعد</strong> لإضافة مضيف SSH أو SFTP، أو إلى <strong>الإعدادات ثم التحكّم بالمصدر</strong> لربط GitHub. تُخزَّن بيانات الاعتماد في Keychain على الجهاز ولا تُرسل إلينا أبدًا.</p>
          <h3>كيف أستخدم مزوّد الذكاء الاصطناعي الخاص بي؟</h3><p>افتح <strong>الإعدادات ثم الذكاء الاصطناعي</strong> وأضف مزوّدك ومفتاح واجهة البرمجة. يبقى مفتاحك على جهازك ويُستخدم للتحدّث مباشرة إلى ذلك المزوّد فقط.</p>
          <h3>أين يمكنني تثبيت حزم بايثون إضافية؟</h3><p>استخدم كتالوج الحزم داخل التطبيق لتثبيت الحزم المدعومة، سواء المكتوبة ببايثون الخالصة أو المبنية أصليًا مسبقًا. ويعتمد التوفّر على ما يمكن تشغيله على iOS و iPadOS.</p></section>
          <section class="legal-section"><h2>الخصوصية والبيانات</h2><p>إن Vibeit خاص افتراضيًا: تبقى شيفرتك وملفاتك وبيانات اعتمادك على جهازك. راجع <a href="privacy.html">سياسة الخصوصية</a> لمعرفة التفاصيل.</p></section>
          <section class="legal-section"><h2>التواصل</h2><p>ما زلت عالقًا، أو وجدت خللًا، أو لديك طلب ميزة؟ راسل <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> مع ذكر طراز جهازك وإصدار iOS أو iPadOS وسنساعدك.</p></section>`
      },
      terms: {
        title: "شروط الاستخدام",
        description: "شروط استخدام Vibeit، بيئة تطوير بايثون الأصلية لـ iPadOS و iOS و macOS.",
        body: `
          <h1>شروط الاستخدام</h1>
          <p class="updated">آخر تحديث: 6 يوليو 2026</p>
          <p>شروط الاستخدام هذه ("الشروط") اتفاقية قانونية بينك وبين مطوّر <strong>Vibeit</strong> ("Vibeit"، "التطبيق"، "نحن") تحكم تنزيلك تطبيق Vibeit واستخدامك إياه على iPadOS و iOS و macOS. وبتنزيل Vibeit أو تثبيته أو استخدامه، فإنك توافق على هذه الشروط. وإن لم توافق، فلا تستخدم التطبيق.</p>
          <div class="tldr"><strong>باختصار.</strong> إن Vibeit أداة للمطوّرين تشغّل بايثون وميزات اختيارية للذكاء الاصطناعي والشبكة على جهازك وعبر خدمات <em>تربطها أنت</em>. وأنت مسؤول عن شيفرتك وبياناتك وبيانات اعتمادك وعن طريقة استخدامك تلك الميزات. يُقدَّم التطبيق "كما هو"؛ وقد تكون مخرجات الذكاء الاصطناعي والشيفرة المنفَّذة خاطئة أو غير آمنة، فراجعها قبل الاعتماد عليها.</div>
          <section class="legal-section"><h2>1. الأهلية والقبول</h2><p>يجب ألّا يقلّ عمرك عن 13 عامًا، أو الحدّ الأدنى لسنّ الموافقة الرقمية في ولايتك القضائية، وأن تكون قادرًا على إبرام عقد ملزم لاستخدام Vibeit. وإذا استخدمت التطبيق نيابة عن مؤسسة، فإنك تقرّ بأنك مخوَّل بقبول هذه الشروط عنها. ويخضع استخدامك أيضًا لاتفاقية <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">ترخيص المستخدم النهائي للتطبيق المرخّص (EULA)</a> من Apple؛ وعند تعارض هذه الشروط مع اتفاقية Apple، تسود اتفاقية Apple فيما يتعلّق برخصتك من App Store.</p></section>
          <section class="legal-section"><h2>2. ما هو Vibeit</h2><p>إن Vibeit بيئة تطوير أصلية لدفاتر بايثون ونصوصها البرمجية، تنفّذ الشيفرة في بيئة تشغيل بايثون على الجهاز. وتشمل الميزات الاختيارية مساعدة الذكاء الاصطناعي عبر مزوّدين تعدّهم أنت، والاتصالات البعيدة عبر SSH و SFTP، و Cloudflare Access، والتحكّم بالمصدر وتكامل GitHub، وتنزيل حزم بايثون. وهذه الخدمات تشغّلها أنت أو أطراف ثالثة، لا نحن.</p></section>
          <section class="legal-section"><h2>3. الترخيص</h2><p>مع مراعاة هذه الشروط واتفاقية Apple، نمنحك ترخيصًا شخصيًا ومحدودًا وغير حصري وغير قابل للنقل وقابلًا للإلغاء لاستخدام Vibeit على أجهزة تحمل علامة Apple تملكها أو تتحكّم بها، لاستخدام شخصي أو تجاري داخلي مشروع. ولا يجوز لك نسخ التطبيق أو تعديله أو هندسته عكسيًا أو فكّ ترجمته أو ترخيصه من الباطن أو بيعه أو توزيعه إلا بما يسمح به القانون المعمول به.</p></section>
          <section class="legal-section"><h2>4. مسؤولياتك والاستخدام المقبول</h2><p>أنت وحدك المسؤول عن الشيفرة التي تكتبها أو تشغّلها، والبيانات التي تعالجها، وبيانات الاعتماد التي تدخلها، والأنظمة التي تتصل بها. وتوافق على ألّا تستخدم Vibeit لانتهاك القوانين، أو التعدّي على الحقوق، أو الوصول إلى أنظمة دون تصريح، أو تطوير برمجيات خبيثة أو توزيعها، أو ممارسة نشاط مسيء، أو إفشاء بيانات لا يُسمح لك بإفشائها، أو تجاوز حدود الأمان أو الاستخدام أو المعدّل. وأنت مسؤول عن أمن الجهاز، ومفاتيح واجهات البرمجة، وبيانات اعتماد SSH، ورموز التحكّم بالمصدر، والنسخ الاحتياطية.</p></section>
          <section class="legal-section"><h2>5. خدمات الأطراف الثالثة</h2><p>عندما تفعّل ميزة تتصل بطرف ثالث، مثل مزوّد ذكاء اصطناعي أو مضيف بعيد أو Cloudflare Access أو GitHub أو فهرس حزم، يخضع استخدامك لشروط ذلك الطرف وسياسة خصوصيته. وأنت مسؤول عن أي رسوم يفرضها. ونحن لا نشغّل تلك الخدمات ولا نتحكّم بها، ولسنا مسؤولين عن توفّرها أو محتواها أو أمنها أو تصرّفاتها أو رسومها.</p></section>
          <section class="legal-section"><h2>6. ميزات الذكاء الاصطناعي والمخرجات المولَّدة</h2><p>قد تنتج ميزات الذكاء الاصطناعي شيفرة أو شروحًا أو محتوى آخر غير دقيق أو ناقص أو غير آمن أو متحيّز أو غير مناسب. ومخرجات الذكاء الاصطناعي ليست مشورة مهنية أو قانونية أو مالية أو طبية أو أمنية. وأنت مسؤول عن مراجعة المحتوى المولَّد بالذكاء الاصطناعي أو المقترح من التطبيق واختباره والتحقّق منه قبل الاعتماد عليه أو تنفيذه أو نشره أو شحنه.</p></section>
          <section class="legal-section"><h2>7. تنفيذ الشيفرة والأوامر البعيدة والبيانات</h2><p>يشغّل Vibeit الشيفرة وأوامر الصدفة التي تقدّمها أنت، أو يقدّمها وكيل ذكاء اصطناعي بتوجيه منك. وقد يؤدّي تنفيذ الشيفرة أو الأوامر البعيدة إلى تعديل ملفات أو حذفها، أو استهلاك موارد، أو التأثير على الأنظمة التي تتصل بها. وأنت تقبل هذه المخاطر وتتحمّل مسؤولية النتائج. وتحتفظ بملكية شيفرتك ودفاترك وبياناتك.</p></section>
          <section class="legal-section"><h2>8. إخلاء المسؤولية عن الأمان وفقدان البيانات</h2><p>نصمّم Vibeit ليكون خاصًا افتراضيًا ونستخدم وسائل حماية مثل Keychain والنقل المشفّر. ومع ذلك، لا توجد برمجية أو طريقة تخزين أو نقل آمنة تمامًا، ولا نضمن أن يكون التطبيق خاليًا من الأخطاء أو متواصلًا دون انقطاع أو خاليًا من الثغرات أو من فقدان البيانات أو الوصول غير المصرّح به.</p></section>
          <section class="legal-section"><h2>9. الاشتراكات والمدفوعات</h2><p>قد تتطلّب بعض الميزات اشتراكًا مدفوعًا يُباع عبر <strong>الشراء داخل التطبيق من Apple</strong>. تُحمَّل الدفعة على حساب Apple الخاص بك وتتجدّد الاشتراكات تلقائيًا ما لم تُلغَ قبل الموعد النهائي للتجديد. ويمكنك إدارة اشتراكك أو إلغاؤه من إعدادات حساب Apple. وتعالج Apple المدفوعات والمبالغ المستردّة وفق شروطها.</p></section>
          <section class="legal-section"><h2 class="legal">10. إخلاء الضمانات</h2><p class="legal">يُقدَّم التطبيق "كما هو" و "حسب توفّره"، دون أي ضمانات من أي نوع، صريحة كانت أم ضمنية أم قانونية، بما في ذلك الضمانات الضمنية للرواج التجاري والملاءمة لغرض معيّن والملكية والدقة وعدم التعدّي. ولا تسمح بعض الولايات القضائية باستبعاد ضمانات معيّنة، لذا قد لا تنطبق عليك بعض الاستثناءات.</p></section>
          <section class="legal-section"><h2 class="legal">11. تحديد المسؤولية</h2><p class="legal">إلى أقصى حدّ يسمح به القانون، لن نكون مسؤولين عن أي أضرار غير مباشرة أو عرضية أو خاصة أو تبعية أو رادعة أو تأديبية، ولا عن خسارة الأرباح أو الإيرادات أو البيانات أو السمعة أو أي خسائر غير ملموسة أخرى ناشئة عن استخدامك التطبيق أو عجزك عن استخدامه، أو عن مخرجات الذكاء الاصطناعي، أو الشيفرة أو الأوامر المنفَّذة، أو فقدان البيانات، أو الحوادث الأمنية، أو خدمات الأطراف الثالثة. ولن تتجاوز مسؤوليتنا الإجمالية عن جميع المطالبات المتعلّقة بالتطبيق المبلغَ الأكبر من: ما دفعته لنا مقابل التطبيق خلال الاثني عشر شهرًا السابقة للمطالبة، أو 10 دولارات أمريكية.</p></section>
          <section class="legal-section"><h2>12. التعويض</h2><p>إلى الحدّ الذي يسمح به القانون، توافق على تعويضنا وإبراء ذمّتنا من المطالبات والأضرار والالتزامات والنفقات الناشئة عن إساءة استخدامك التطبيق، أو مخالفتك هذه الشروط أو أي قانون، أو عن شيفرتك أو بياناتك أو محتواك، أو عن استخدامك أي خدمة أو نظام متصل تابع لطرف ثالث.</p></section>
          <section class="legal-section"><h2>13. الإنهاء</h2><p>يمكنك التوقّف عن استخدام التطبيق في أي وقت بحذفه. ويجوز لنا تعليق ترخيصك أو إنهاؤه إذا خالفت هذه الشروط مخالفة جوهرية أو استخدمت التطبيق بصورة غير مشروعة. وتظلّ سارية تلك البنود التي يقتضي طبعها الاستمرار بعد الإنهاء.</p></section>
          <section class="legal-section"><h2>14. شروط Apple App Store</h2><p>هذه الشروط مبرمة بينك وبيننا فقط، لا مع Apple. وApple ليست مسؤولة عن التطبيق أو محتواه، ولا يقع عليها التزام بتقديم الصيانة أو الدعم. وApple وشركاتها التابعة مستفيدون من الغير بموجب هذه الشروط ويجوز لهم إنفاذها تجاهك. وتقرّ بأنك لست في بلد يخضع لحظر من حكومة الولايات المتحدة، ولست مدرجًا على أي قائمة أطراف مقيّدة لدى حكومة الولايات المتحدة.</p></section>
          <section class="legal-section"><h2>15. القانون الحاكم</h2><p>تخضع هذه الشروط لقوانين الولاية القضائية التي تأسّس فيها المطوّر، إلا حيث تنصّ قوانين حماية المستهلك الإلزامية في مكان إقامتك على خلاف ذلك. ولا يقيّد أيّ نصّ في هذه الشروط الحقوق القانونية غير القابلة للتنازل التي قد تتمتّع بها بصفتك مستهلكًا.</p></section>
          <section class="legal-section"><h2>16. التغييرات على هذه الشروط</h2><p>قد نحدّث هذه الشروط من حين لآخر. وسنراجع تاريخ "آخر تحديث" أعلاه، وسنقدّم إشعارًا مناسبًا عند التغييرات الجوهرية. ويشكّل استمرار استخدامك بعد التحديث قبولًا للشروط المُعدَّلة.</p></section>
          <section class="legal-section"><h2>17. التواصل</h2><p>أسئلة حول هذه الشروط؟ تواصل معنا عبر <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a>.</p></section>`
      },
      contact: {
        title: "اتصل بنا",
        description: "تواصل مع Vibeit: أرسل اقتراح ميزة أو أبلغ عن مشكلة.",
        body: `
          <h1>اتصل بنا</h1>
          <p class="updated">أرسل اقتراح ميزة أو أبلغ عن مشكلة — نقرأ كل رسالة.</p>`
      }
    },
    th: {
      privacy: {
        title: "นโยบายความเป็นส่วนตัว",
        description: "นโยบายความเป็นส่วนตัวของ Vibeit ซึ่งเป็น Python IDE แบบเนทีฟสำหรับ iPadOS, iOS และ macOS",
        body: `
          <h1>นโยบายความเป็นส่วนตัว</h1>
          <p class="updated">อัปเดตล่าสุด: 6 กรกฎาคม 2026</p>
          <p>นโยบายความเป็นส่วนตัวฉบับนี้อธิบายว่า <strong>Vibeit</strong> ("Vibeit", "แอป", "เรา") จัดการข้อมูลอย่างไรเมื่อคุณใช้แอป Vibeit บน iPadOS, iOS และ macOS โดย Vibeit เป็น Python notebook IDE แบบเนทีฟที่ออกแบบมาให้ทำงานบนเครื่องของคุณ เราสร้างให้มันเป็นส่วนตัวโดยค่าเริ่มต้น โค้ดของคุณรันในเคอร์เนล Python บนเครื่อง ส่วนไฟล์ ข้อมูลรับรอง และคีย์ API ของคุณยังคงอยู่บนเครื่องของคุณ</p>
          <div class="tldr"><strong>ฉบับย่อ</strong> เราไม่ได้เดินเซิร์ฟเวอร์วิเคราะห์ข้อมูลหรือโฆษณา และในแอปไม่มี SDK ติดตามหรือโฆษณาของบุคคลที่สาม เราไม่ขายข้อมูลส่วนบุคคลของคุณ ข้อมูลจะออกจากเครื่องของคุณก็ต่อเมื่อ<em>คุณ</em>ใช้ฟีเจอร์ที่จำเป็นต้องส่งเท่านั้น เช่น การเรียกผู้ให้บริการ AI ด้วยคีย์ของคุณเอง การเชื่อมต่อเซิร์ฟเวอร์ระยะไกลที่คุณตั้งค่าไว้ หรือการดาวน์โหลดแพ็กเกจ</div>

          <section class="legal-section"><h2>1. ข้อมูลที่เก็บอยู่บนเครื่องของคุณ</h2>
          <p>สิ่งต่อไปนี้อยู่บนเครื่องของคุณ และอยู่ใน iCloud หรือแอปไฟล์ของคุณเองหากคุณเลือกบันทึกไว้ที่นั่น เราไม่ได้รับสำเนาของสิ่งเหล่านี้</p>
          <ul>
            <li><strong>โน้ตบุ๊ก สคริปต์ และไฟล์ในพื้นที่ทำงาน</strong> ที่คุณสร้างหรือเปิด</li>
            <li><strong>การรัน Python</strong>: โค้ดทำงานในเคอร์เนลบนเครื่อง โค้ดและผลลัพธ์ของคุณไม่ถูกส่งมาให้เรา</li>
            <li><strong>ข้อมูลรับรองและความลับ</strong>: คีย์ API รหัสผ่าน SSH วลีรหัสผ่านของคีย์ และโทเคน Cloudflare Access ถูกเก็บใน <strong>Keychain</strong> ของเครื่อง และไม่ถูกเขียนลงในโน้ตบุ๊กหรือบันทึกล็อก และไม่ถูกส่งมาให้เรา</li>
            <li><strong>การตั้งค่าแอป</strong> เช่น ธีม ภาษา และโปรไฟล์โฮสต์</li>
          </ul></section>

          <section class="legal-section"><h2>2. การตรวจหาภาษาของเว็บไซต์</h2>
          <p>หน้าเว็บเหล่านี้อาจขอข้อมูลประเทศจาก GeoJS เพื่อเลือกภาษาที่จะแสดงในครั้งแรกจากตำแหน่งของหมายเลข IP ของคุณ คำขอนี้คืนค่าเป็นรหัสประเทศ และถูกใช้ในเบราว์เซอร์ของคุณเพื่อเลือกภาษาเท่านั้น หากล้มเหลว หน้าเว็บจะย้อนกลับไปใช้ภาษาของเบราว์เซอร์ แล้วจึงเป็นภาษาอังกฤษ คุณเปลี่ยนภาษาเองได้ และตัวเลือกของคุณจะถูกเก็บไว้ใน localStorage บนเครื่องนี้</p></section>

          <section class="legal-section"><h2>3. ฟีเจอร์ที่ส่งข้อมูลไปยังบุคคลที่สาม</h2>
          <p>เมื่อคุณเลือกใช้ฟีเจอร์เหล่านี้ ข้อมูลจะถูกส่งไปยังบุคคลที่สามที่เกี่ยวข้องภายใต้นโยบายความเป็นส่วนตัวของ<em>ฝ่ายนั้น</em> โดย Vibeit ทำหน้าที่เป็นเพียงไคลเอนต์</p>
          <h3>ผู้ช่วย AI</h3><p>หากคุณเปิดใช้ฟีเจอร์ AI และใช้ผู้ให้บริการ AI บนคลาวด์ เช่น OpenAI หรือ Anthropic พรอมป์ตที่คุณส่ง รวมถึงโค้ดหรือบริบทที่เกี่ยวข้อง จะถูกส่งไปยังผู้ให้บริการนั้นโดยใช้คีย์ API หรือการลงชื่อเข้าใช้ที่คุณให้ไว้ ส่วน Apple Intelligence หรือโมเดลพื้นฐานบนเครื่อง หากมีการใช้งาน จะทำงานบนเครื่องของคุณ เราไม่ได้รับพรอมป์ตหรือคำตอบของคุณ</p>
          <h3>การเชื่อมต่อระยะไกล</h3><p>หากคุณตั้งค่าโฮสต์ระยะไกล Vibeit จะเชื่อมต่อโดยตรงไปยังเซิร์ฟเวอร์ที่<em>คุณ</em>ระบุ เพื่อรันคำสั่ง โอนไฟล์ หรือรัน Python สำหรับโฮสต์ที่เข้าถึงผ่าน Cloudflare Access หน้าต่างลงชื่อเข้าใช้จะยืนยันตัวตนกับผู้ให้บริการข้อมูลประจำตัวของคุณ และเก็บโทเคนการเข้าถึงที่ได้ไว้ใน Keychain เราไม่ได้ดูแลเซิร์ฟเวอร์เหล่านี้ และไม่ได้รับเนื้อหาของเซสชันระยะไกลของคุณ</p>
          <h3>การดาวน์โหลดแพ็กเกจ</h3><p>แพ็กเกจที่จัดการให้ถูกดึงผ่าน HTTPS จากคลังแพ็กเกจสาธารณะ รวมถึงรีจิสทรีที่โฮสต์บน GitHub นี้ เช่นเดียวกับคำขอเว็บทั่วไป ผู้ให้บริการโฮสติงอาจประมวลผลหมายเลข IP และข้อมูลกำกับคำขอของคุณเพื่อส่งไฟล์ให้</p></section>

          <section class="legal-section"><h2>4. การสมัครสมาชิกและการชำระเงิน</h2>
          <p>การสมัครสมาชิก Vibeit ขายผ่าน <strong>Apple In-App Purchase</strong> โดย Apple เป็นผู้ดำเนินการชำระเงินและจัดการการสมัครสมาชิกของคุณ เราไม่เคยได้รับหรือเก็บรายละเอียดบัตรชำระเงินของคุณ แอปได้รับจาก Apple ผ่าน StoreKit เพียงสถานะการสมัครสมาชิกหรือสิทธิ์ของคุณ เพื่อปลดล็อกฟีเจอร์ คุณจัดการหรือยกเลิกการสมัครสมาชิกได้ทุกเมื่อในการตั้งค่าบัญชี Apple</p></section>
          <section class="legal-section"><h2>5. ข้อมูลที่เราเก็บรวบรวม</h2><p>เราไม่มีระบบบัญชีผู้ใช้ และไม่ได้เดินระบบหลังบ้านที่เก็บข้อมูลส่วนบุคคลของคุณ แอปไม่มีการวิเคราะห์ข้อมูลหรือโฆษณาของบุคคลที่สาม หากคุณติดต่อเราเพื่อขอความช่วยเหลือทางอีเมล เราจะได้รับข้อมูลเท่าที่คุณเลือกใส่มาในข้อความ</p></section>
          <section class="legal-section"><h2>6. ความปลอดภัยของข้อมูล</h2><p>ความลับถูกเก็บโดยใช้ Keychain ของระบบปฏิบัติการ การเชื่อมต่อเครือข่ายใช้การเข้ารหัส TLS หรือ SSH ไม่มีวิธีจัดเก็บหรือส่งข้อมูลใดปลอดภัย 100 เปอร์เซ็นต์ แต่เราอาศัยการป้องกันของแพลตฟอร์ม Apple และการรับส่งข้อมูลที่เข้ารหัสเพื่อปกป้องข้อมูลของคุณ</p></section>
          <section class="legal-section"><h2>7. การเก็บรักษาและการลบข้อมูล</h2><p>เนื่องจากข้อมูลของคุณอยู่บนเครื่องของคุณ คุณจึงเป็นผู้ควบคุมมัน คุณลบไฟล์ โฮสต์ และข้อมูลรับรองได้ในแอป และการลบแอปจะลบข้อมูลในเครื่องกับรายการ Keychain ที่เกี่ยวข้องไปด้วย ส่วนข้อมูลที่ถูกส่งไปยังบุคคลที่สามแล้วจะอยู่ภายใต้นโยบายของฝ่ายนั้น</p></section>
          <section class="legal-section"><h2>8. ความเป็นส่วนตัวของเด็ก</h2><p>Vibeit เป็นเครื่องมือสำหรับนักพัฒนา และไม่ได้มุ่งเป้าไปที่เด็กอายุต่ำกว่า 13 ปี หรือต่ำกว่าเกณฑ์อายุขั้นต่ำที่เทียบเท่าในเขตอำนาจศาลของคุณ เราไม่เก็บข้อมูลส่วนบุคคลจากเด็กโดยเจตนา</p></section>
          <section class="legal-section"><h2>9. ผู้ใช้ระหว่างประเทศและสิทธิของคุณ</h2><p>ขึ้นอยู่กับถิ่นที่อยู่ของคุณ เช่น ภายใต้ GDPR ของสหภาพยุโรป หรือ CCPA และ CPRA ของแคลิฟอร์เนีย คุณอาจมีสิทธิเข้าถึง แก้ไข ลบ หรือจำกัดการประมวลผลข้อมูลส่วนบุคคลของคุณ เนื่องจากเราไม่ได้เก็บรวบรวมหรือจัดเก็บข้อมูลส่วนบุคคลของคุณไว้บนเซิร์ฟเวอร์ของเราเอง คำขอส่วนใหญ่จึงทำได้โดยตรงบนเครื่องของคุณ หรือกับผู้ให้บริการภายนอกที่เกี่ยวข้อง คุณติดต่อเราได้ตามรายละเอียดด้านล่างเช่นกัน</p></section>
          <section class="legal-section"><h2>10. การเปลี่ยนแปลงนโยบายนี้</h2><p>เราอาจปรับปรุงนโยบายความเป็นส่วนตัวนี้เป็นครั้งคราว เราจะแก้ไขวันที่ "อัปเดตล่าสุด" ด้านบน และจะแจ้งให้ทราบตามสมควรหากมีการเปลี่ยนแปลงในสาระสำคัญ การใช้แอปต่อไปหลังการอัปเดตถือเป็นการยอมรับนโยบายฉบับแก้ไข</p></section>
          <section class="legal-section"><h2>11. ติดต่อเรา</h2><p>มีคำถามเกี่ยวกับนโยบายนี้หรือความเป็นส่วนตัวของคุณ? ติดต่อเราที่ <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a></p></section>`
      },
      support: {
        title: "ฝ่ายสนับสนุน",
        description: "ความช่วยเหลือและการสนับสนุนสำหรับ Vibeit ซึ่งเป็น Python IDE แบบเนทีฟสำหรับ iPadOS, iOS และ macOS",
        body: `
          <h1>ฝ่ายสนับสนุน</h1>
          <p class="updated">Vibeit - Python IDE แบบเนทีฟสำหรับ iPadOS, iOS และ macOS</p>
          <div class="tldr"><strong>ต้องการความช่วยเหลือ?</strong> อีเมลหาเราที่ <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> แล้วเราจะติดต่อกลับ โดยปกติเราตอบภายใน 1-2 วันทำการ</div>
          <p><a class="contact-btn" href="mailto:aroluo@icloud.com?subject=Vibeit%20Support">ติดต่อฝ่ายสนับสนุน</a></p>
          <section class="legal-section"><h2>เริ่มต้นใช้งาน</h2><p>Vibeit เป็น Python IDE เต็มรูปแบบที่ทำงานบนเครื่องของคุณ สร้างโน้ตบุ๊กหรือสคริปต์ เขียน Python แล้วกดรัน โค้ดจะทำงานในเคอร์เนลบนเครื่อง ซึ่งรองรับโน้ตบุ๊ก matplotlib, NumPy, pandas, PyTorch และอื่น ๆ ไม่จำเป็นต้องเชื่อมต่ออินเทอร์เน็ตเพื่อรันโค้ดของคุณ</p></section>
          <section class="legal-section"><h2>คำถามที่พบบ่อย</h2>
          <h3>เวอร์ชันฟรีกับแบบสมัครสมาชิกต่างกันอย่างไร?</h3><p>Python IDE บนเครื่องส่วนหลักใช้ได้ในแพ็กเกจ <strong>มาตรฐาน</strong> ส่วน <strong>โปร</strong> เพิ่มเซิร์ฟเวอร์ SSH/SFTP ระยะไกลและเทอร์มินัล การโคลน พุช พูล และ pull request ของ GitHub รวมถึงผู้ให้บริการ AI บนคลาวด์ ทุกแพ็กเกจเริ่มด้วย <strong>การทดลองใช้ฟรี 7 วัน</strong></p>
          <h3>จะเริ่มทดลองใช้ฟรีหรือสมัครสมาชิกได้อย่างไร?</h3><p>เปิด <strong>การตั้งค่า แล้วไปที่ บัญชี</strong> ในแอป เลือกแพ็กเกจ แล้วแตะ <strong>เริ่มทดลองใช้ฟรี</strong> การชำระเงินดำเนินการโดย Apple ผ่านบัญชี Apple ของคุณ</p>
          <h3>จะจัดการหรือยกเลิกการสมัครสมาชิกได้อย่างไร?</h3><p>Apple เป็นผู้จัดการการสมัครสมาชิก บนเครื่องของคุณ ให้เปิดแอป <strong>การตั้งค่า</strong> แตะชื่อของคุณ เปิด <strong>การสมัครใช้บริการ</strong> แล้วเลือก <strong>Vibeit</strong> หรือคุณจะ <a href="https://apps.apple.com/account/subscriptions">จัดการการสมัครสมาชิกที่นี่</a> ก็ได้</p>
          <h3>จะกู้คืนการซื้อได้อย่างไร?</h3><p>บนเครื่องใหม่หรือหลังติดตั้งใหม่ ให้เปิด <strong>การตั้งค่า แล้วไปที่ บัญชี</strong> ใน Vibeit แล้วแตะ <strong>กู้คืนการซื้อ</strong> ตรวจสอบว่าคุณลงชื่อเข้าใช้ด้วยบัญชี Apple เดียวกับที่ใช้สมัคร</p>
          <h3>จะเชื่อมต่อเซิร์ฟเวอร์ระยะไกลหรือ GitHub ได้อย่างไร?</h3><p>ไปที่ <strong>การตั้งค่า แล้วไปที่ รีโมต</strong> เพื่อเพิ่มโฮสต์ SSH/SFTP หรือ <strong>การตั้งค่า แล้วไปที่ ระบบควบคุมเวอร์ชัน</strong> เพื่อเชื่อมต่อ GitHub ข้อมูลรับรองถูกเก็บใน Keychain ของเครื่องและไม่ถูกส่งมาให้เรา</p>
          <h3>จะใช้ผู้ให้บริการ AI ของตัวเองได้อย่างไร?</h3><p>เปิด <strong>การตั้งค่า แล้วไปที่ AI</strong> แล้วเพิ่มผู้ให้บริการและคีย์ API ของคุณ คีย์ของคุณอยู่บนเครื่องของคุณ และถูกใช้เพื่อคุยกับผู้ให้บริการนั้นโดยตรงเท่านั้น</p>
          <h3>ติดตั้งแพ็กเกจ Python เพิ่มเติมได้ที่ไหน?</h3><p>ใช้แคตตาล็อกแพ็กเกจในแอปเพื่อติดตั้งแพ็กเกจที่รองรับ ทั้งแบบ pure-Python และแบบเนทีฟที่คอมไพล์มาแล้ว ความพร้อมใช้งานขึ้นอยู่กับว่าอะไรรันได้บน iOS และ iPadOS</p></section>
          <section class="legal-section"><h2>ความเป็นส่วนตัวและข้อมูล</h2><p>Vibeit เป็นส่วนตัวโดยค่าเริ่มต้น โค้ด ไฟล์ และข้อมูลรับรองของคุณอยู่บนเครื่องของคุณ ดูรายละเอียดได้ใน <a href="privacy.html">นโยบายความเป็นส่วนตัว</a> ของเรา</p></section>
          <section class="legal-section"><h2>ติดต่อเรา</h2><p>ยังติดขัด เจอบั๊ก หรืออยากขอฟีเจอร์ใหม่? อีเมลไปที่ <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a> พร้อมระบุรุ่นเครื่องและเวอร์ชัน iOS หรือ iPadOS แล้วเราจะช่วยเหลือ</p></section>`
      },
      terms: {
        title: "ข้อกำหนดการใช้งาน",
        description: "ข้อกำหนดการใช้งานของ Vibeit ซึ่งเป็น Python IDE แบบเนทีฟสำหรับ iPadOS, iOS และ macOS",
        body: `
          <h1>ข้อกำหนดการใช้งาน</h1>
          <p class="updated">อัปเดตล่าสุด: 6 กรกฎาคม 2026</p>
          <p>ข้อกำหนดการใช้งานฉบับนี้ ("ข้อกำหนด") เป็นข้อตกลงทางกฎหมายระหว่างคุณกับผู้พัฒนา <strong>Vibeit</strong> ("Vibeit", "แอป", "เรา") ซึ่งกำกับการดาวน์โหลดและการใช้งานแอป Vibeit บน iPadOS, iOS และ macOS การดาวน์โหลด ติดตั้ง หรือใช้ Vibeit ถือว่าคุณยอมรับข้อกำหนดเหล่านี้ หากคุณไม่ยอมรับ โปรดอย่าใช้แอป</p>
          <div class="tldr"><strong>ฉบับย่อ</strong> Vibeit เป็นเครื่องมือสำหรับนักพัฒนา ที่รัน Python และฟีเจอร์เสริมด้าน AI กับเครือข่ายบนเครื่องของคุณ และผ่านบริการที่<em>คุณ</em>เชื่อมต่อเอง คุณรับผิดชอบโค้ด ข้อมูล ข้อมูลรับรองของคุณเอง และวิธีที่คุณใช้ฟีเจอร์เหล่านั้น แอปนี้ให้บริการ "ตามสภาพ" ผลลัพธ์จาก AI และโค้ดที่ถูกรันอาจผิดพลาดหรือไม่ปลอดภัย โปรดตรวจสอบก่อนนำไปใช้จริง</div>
          <section class="legal-section"><h2>1. คุณสมบัติและการยอมรับ</h2><p>คุณต้องมีอายุอย่างน้อย 13 ปี หรือถึงเกณฑ์อายุขั้นต่ำของการให้ความยินยอมทางดิจิทัลในเขตอำนาจศาลของคุณ และสามารถทำสัญญาที่มีผลผูกพันเพื่อใช้ Vibeit ได้ หากคุณใช้แอปในนามขององค์กร คุณรับรองว่าคุณได้รับมอบอำนาจให้ยอมรับข้อกำหนดเหล่านี้แทนองค์กรนั้น การใช้งานของคุณยังอยู่ภายใต้ <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">ข้อตกลงอนุญาตให้ใช้สิทธิสำหรับผู้ใช้ปลายทาง (EULA)</a> ของ Apple ด้วย หากข้อกำหนดเหล่านี้ขัดกับ EULA ของ Apple ให้ยึด EULA ของ Apple เป็นหลักในส่วนที่เกี่ยวกับสิทธิ์การใช้งานจาก App Store ของคุณ</p></section>
          <section class="legal-section"><h2>2. Vibeit คืออะไร</h2><p>Vibeit เป็น IDE แบบเนทีฟสำหรับโน้ตบุ๊กและสคริปต์ Python ที่รันโค้ดในรันไทม์ Python บนเครื่อง ฟีเจอร์เสริมได้แก่ ผู้ช่วย AI ผ่านผู้ให้บริการที่คุณตั้งค่าเอง การเชื่อมต่อระยะไกลด้วย SSH/SFTP, Cloudflare Access, ระบบควบคุมเวอร์ชันและการผสานกับ GitHub รวมถึงการดาวน์โหลดแพ็กเกจ Python บริการเหล่านี้ดำเนินการโดยคุณหรือโดยบุคคลที่สาม ไม่ใช่โดยเรา</p></section>
          <section class="legal-section"><h2>3. สิทธิ์การใช้งาน</h2><p>ภายใต้ข้อกำหนดเหล่านี้และ EULA ของ Apple เราให้สิทธิ์แก่คุณแบบส่วนบุคคล จำกัด ไม่ผูกขาด โอนสิทธิ์ไม่ได้ และเพิกถอนได้ ในการใช้ Vibeit บนอุปกรณ์ยี่ห้อ Apple ที่คุณเป็นเจ้าของหรือควบคุม เพื่อการใช้งานส่วนตัวหรือการใช้งานภายในองค์กรที่ชอบด้วยกฎหมาย คุณต้องไม่คัดลอก ดัดแปลง ทำวิศวกรรมย้อนกลับ แยกส่วนโปรแกรม ให้สิทธิ์ช่วง ขาย หรือแจกจ่ายแอป เว้นแต่กฎหมายที่ใช้บังคับจะอนุญาต</p></section>
          <section class="legal-section"><h2>4. ความรับผิดชอบของคุณและการใช้งานที่ยอมรับได้</h2><p>คุณรับผิดชอบแต่เพียงผู้เดียวต่อโค้ดที่คุณเขียนหรือรัน ข้อมูลที่คุณประมวลผล ข้อมูลรับรองที่คุณกรอก และระบบที่คุณเชื่อมต่อ คุณตกลงจะไม่ใช้ Vibeit เพื่อละเมิดกฎหมาย ละเมิดสิทธิ เข้าถึงระบบโดยไม่ได้รับอนุญาต พัฒนาหรือแจกจ่ายมัลแวร์ กระทำการอันเป็นการล่วงละเมิด เปิดเผยข้อมูลที่คุณไม่มีสิทธิ์เปิดเผย หรือหลบเลี่ยงมาตรการความปลอดภัย ขีดจำกัดการใช้งาน หรือขีดจำกัดอัตราการเรียกใช้ คุณรับผิดชอบความปลอดภัยของเครื่อง คีย์ API ข้อมูลรับรอง SSH โทเคนของระบบควบคุมเวอร์ชัน และการสำรองข้อมูล</p></section>
          <section class="legal-section"><h2>5. บริการของบุคคลที่สาม</h2><p>เมื่อคุณเปิดใช้ฟีเจอร์ที่เชื่อมต่อกับบุคคลที่สาม เช่น ผู้ให้บริการ AI โฮสต์ระยะไกล Cloudflare Access, GitHub หรือคลังแพ็กเกจ การใช้งานของคุณจะอยู่ภายใต้ข้อกำหนดและนโยบายความเป็นส่วนตัวของฝ่ายนั้น คุณรับผิดชอบค่าธรรมเนียมใด ๆ ที่พวกเขาเรียกเก็บ เราไม่ได้ดำเนินการหรือควบคุมบริการเหล่านั้น และไม่รับผิดชอบต่อความพร้อมใช้งาน เนื้อหา ความปลอดภัย การกระทำ หรือค่าใช้จ่ายของบริการเหล่านั้น</p></section>
          <section class="legal-section"><h2>6. ฟีเจอร์ AI และผลลัพธ์ที่สร้างขึ้น</h2><p>ฟีเจอร์ AI อาจสร้างโค้ด คำอธิบาย หรือเนื้อหาอื่นที่ไม่ถูกต้อง ไม่ครบถ้วน ไม่ปลอดภัย มีอคติ หรือไม่เหมาะสม ผลลัพธ์จาก AI ไม่ใช่คำแนะนำทางวิชาชีพ กฎหมาย การเงิน การแพทย์ หรือความปลอดภัย คุณรับผิดชอบในการตรวจทาน ทดสอบ และตรวจสอบความถูกต้องของเนื้อหาที่ AI สร้างขึ้นหรือที่แอปแนะนำ ก่อนจะนำไปพึ่งพา รัน เผยแพร่ หรือส่งมอบ</p></section>
          <section class="legal-section"><h2>7. การรันโค้ด คำสั่งระยะไกล และข้อมูล</h2><p>Vibeit รันโค้ดและคำสั่งเชลล์ที่คุณเป็นผู้ให้ หรือที่เอเจนต์ AI ให้ตามคำสั่งของคุณ การรันโค้ดหรือคำสั่งระยะไกลอาจแก้ไขหรือลบไฟล์ ใช้ทรัพยากร หรือส่งผลกระทบต่อระบบที่คุณเชื่อมต่อ คุณยอมรับความเสี่ยงเหล่านี้และรับผิดชอบต่อผลลัพธ์ที่เกิดขึ้น คุณยังคงเป็นเจ้าของโค้ด โน้ตบุ๊ก และข้อมูลของคุณ</p></section>
          <section class="legal-section"><h2>8. ข้อจำกัดความรับผิดด้านความปลอดภัยและการสูญหายของข้อมูล</h2><p>เราออกแบบ Vibeit ให้เป็นส่วนตัวโดยค่าเริ่มต้น และใช้มาตรการป้องกัน เช่น Keychain และการรับส่งข้อมูลที่เข้ารหัส อย่างไรก็ตาม ไม่มีซอฟต์แวร์ วิธีจัดเก็บ หรือวิธีส่งข้อมูลใดปลอดภัยอย่างสมบูรณ์ และเราไม่รับประกันว่าแอปจะปราศจากข้อผิดพลาด ทำงานต่อเนื่องไม่สะดุด ปราศจากช่องโหว่ หรือปราศจากการสูญหายของข้อมูลหรือการเข้าถึงโดยไม่ได้รับอนุญาต</p></section>
          <section class="legal-section"><h2>9. การสมัครสมาชิกและการชำระเงิน</h2><p>บางฟีเจอร์อาจต้องสมัครสมาชิกแบบเสียเงินซึ่งขายผ่าน <strong>Apple In-App Purchase</strong> ค่าบริการจะถูกเรียกเก็บจากบัญชี Apple ของคุณ และการสมัครสมาชิกจะต่ออายุอัตโนมัติ เว้นแต่จะยกเลิกก่อนกำหนดเส้นตายของการต่ออายุ คุณจัดการหรือยกเลิกการสมัครสมาชิกได้ในการตั้งค่าบัญชี Apple โดย Apple เป็นผู้ดำเนินการชำระเงินและการคืนเงินตามข้อกำหนดของ Apple</p></section>
          <section class="legal-section"><h2 class="legal">10. การปฏิเสธการรับประกัน</h2><p class="legal">แอปนี้ให้บริการ "ตามสภาพ" และ "เท่าที่มีให้" โดยไม่มีการรับประกันใด ๆ ไม่ว่าโดยชัดแจ้ง โดยปริยาย หรือโดยบทบัญญัติของกฎหมาย รวมถึงการรับประกันโดยปริยายด้านความเหมาะสมในเชิงพาณิชย์ ความเหมาะสมต่อวัตถุประสงค์เฉพาะ กรรมสิทธิ์ ความถูกต้อง และการไม่ละเมิดสิทธิ บางเขตอำนาจศาลไม่อนุญาตให้ยกเว้นการรับประกันบางประการ ข้อยกเว้นบางข้อจึงอาจไม่ใช้กับคุณ</p></section>
          <section class="legal-section"><h2 class="legal">11. การจำกัดความรับผิด</h2><p class="legal">ภายในขอบเขตสูงสุดที่กฎหมายอนุญาต เราจะไม่รับผิดต่อความเสียหายทางอ้อม ความเสียหายโดยบังเอิญ ความเสียหายพิเศษ ความเสียหายอันเป็นผลสืบเนื่อง ความเสียหายเชิงลงโทษ หรือต่อการสูญเสียกำไร รายได้ ข้อมูล ชื่อเสียง หรือความสูญเสียที่จับต้องไม่ได้อื่น ๆ อันเกิดจากการที่คุณใช้หรือไม่สามารถใช้แอป ผลลัพธ์จาก AI โค้ดหรือคำสั่งที่ถูกรัน การสูญหายของข้อมูล เหตุการณ์ด้านความปลอดภัย หรือบริการของบุคคลที่สาม ความรับผิดรวมของเราสำหรับข้อเรียกร้องทั้งหมดที่เกี่ยวกับแอปจะไม่เกินจำนวนที่สูงกว่าระหว่าง จำนวนเงินที่คุณชำระให้เราสำหรับแอปในช่วงสิบสองเดือนก่อนเกิดข้อเรียกร้อง หรือ 10 ดอลลาร์สหรัฐ</p></section>
          <section class="legal-section"><h2>12. การชดใช้ค่าเสียหาย</h2><p>ภายในขอบเขตที่กฎหมายอนุญาต คุณตกลงจะชดใช้ค่าเสียหายและปกป้องเราจากข้อเรียกร้อง ความเสียหาย ความรับผิด และค่าใช้จ่ายที่เกิดจากการที่คุณใช้แอปในทางที่ผิด การละเมิดข้อกำหนดเหล่านี้หรือกฎหมายใด ๆ โค้ด ข้อมูล หรือเนื้อหาของคุณ หรือการที่คุณใช้บริการหรือระบบของบุคคลที่สามที่เชื่อมต่ออยู่</p></section>
          <section class="legal-section"><h2>13. การสิ้นสุด</h2><p>คุณหยุดใช้แอปเมื่อใดก็ได้ด้วยการลบแอปออก เราอาจระงับหรือยุติสิทธิ์การใช้งานของคุณ หากคุณละเมิดข้อกำหนดเหล่านี้ในสาระสำคัญ หรือใช้แอปโดยมิชอบด้วยกฎหมาย ข้อกำหนดที่โดยสภาพแล้วควรมีผลต่อไปหลังการสิ้นสุด จะยังคงมีผลบังคับ</p></section>
          <section class="legal-section"><h2>14. ข้อกำหนดของ Apple App Store</h2><p>ข้อกำหนดเหล่านี้เป็นข้อตกลงระหว่างคุณกับเราเท่านั้น ไม่ใช่กับ Apple โดย Apple ไม่รับผิดชอบต่อแอปหรือเนื้อหาในแอป และไม่มีภาระผูกพันในการให้บริการบำรุงรักษาหรือสนับสนุน Apple และบริษัทในเครือเป็นผู้รับประโยชน์ที่เป็นบุคคลภายนอกตามข้อกำหนดเหล่านี้ และอาจบังคับใช้ข้อกำหนดเหล่านี้กับคุณได้ คุณรับรองว่าคุณไม่ได้อยู่ในประเทศที่ถูกรัฐบาลสหรัฐฯ คว่ำบาตร และไม่ได้อยู่ในบัญชีรายชื่อบุคคลต้องห้ามของรัฐบาลสหรัฐฯ</p></section>
          <section class="legal-section"><h2>15. กฎหมายที่ใช้บังคับ</h2><p>ข้อกำหนดเหล่านี้อยู่ภายใต้กฎหมายของเขตอำนาจศาลที่ผู้พัฒนาจัดตั้งอยู่ เว้นแต่กฎหมายคุ้มครองผู้บริโภคซึ่งบังคับใช้เด็ดขาดในถิ่นที่อยู่ของคุณจะกำหนดไว้เป็นอย่างอื่น ไม่มีข้อความใดในข้อกำหนดเหล่านี้ที่จำกัดสิทธิตามกฎหมายที่คุณสละไม่ได้ในฐานะผู้บริโภค</p></section>
          <section class="legal-section"><h2>16. การเปลี่ยนแปลงข้อกำหนดเหล่านี้</h2><p>เราอาจปรับปรุงข้อกำหนดเหล่านี้เป็นครั้งคราว เราจะแก้ไขวันที่ "อัปเดตล่าสุด" ด้านบน และจะแจ้งให้ทราบตามสมควรหากมีการเปลี่ยนแปลงในสาระสำคัญ การใช้งานต่อไปหลังการอัปเดตถือเป็นการยอมรับข้อกำหนดฉบับแก้ไข</p></section>
          <section class="legal-section"><h2>17. ติดต่อเรา</h2><p>มีคำถามเกี่ยวกับข้อกำหนดเหล่านี้? ติดต่อเราที่ <a href="mailto:aroluo@icloud.com">aroluo@icloud.com</a></p></section>`
      },
      contact: {
        title: "ติดต่อเรา",
        description: "ติดต่อ Vibeit: เสนอฟีเจอร์หรือแจ้งปัญหา",
        body: `
          <h1>ติดต่อเรา</h1>
          <p class="updated">ส่งไอเดียฟีเจอร์หรือแจ้งปัญหา เราอ่านทุกข้อความ</p>`
      }
    }
  };

  function normalizedLang(value) {
    if (!value) return "";
    const lower = String(value).toLowerCase();
    if (lower.startsWith("zh")) return "zh";
    if (lower.startsWith("ja")) return "ja";
    if (lower.startsWith("ko")) return "ko";
    if (lower.startsWith("fr")) return "fr";
    if (lower.startsWith("it")) return "it";
    if (lower.startsWith("de")) return "de";
    if (lower.startsWith("ar")) return "ar";
    if (lower.startsWith("th")) return "th";
    return lower.startsWith("en") ? "en" : "";
  }

  function fallbackFromBrowser() {
    const choices = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language];
    for (const choice of choices) {
      const lang = normalizedLang(choice);
      if (SUPPORTED.has(lang)) return lang;
    }
    return "en";
  }

  function setMeta(selector, value) {
    const node = document.querySelector(selector);
    if (node && value) node.setAttribute("content", value);
  }

  function render(lang) {
    if (!SUPPORTED.has(lang)) lang = "en";
    const pageKey = document.body.dataset.legalPage || "privacy";
    const data = (PAGES[lang] && PAGES[lang][pageKey]) || PAGES.en[pageKey];
    const ui = UI[lang] || UI.en;
    const metaLang = LANGS.find((entry) => entry.code === lang) || LANGS[0];
    const content = document.getElementById("legalContent");
    if (!data || !content) return;

    document.documentElement.lang = metaLang.html;
    document.documentElement.dir = RTL.has(lang) ? "rtl" : "ltr";
    document.title = `${data.title} - Vibeit`;
    setMeta('meta[name="description"]', data.description);
    setMeta('meta[property="og:title"]', `Vibeit ${data.title}`);

    content.innerHTML = data.body;
    if (!document.body.hasAttribute("data-no-locale-note")) {
      const updated = content.querySelector(".updated");
      const note = document.createElement("p");
      note.className = "locale-note";
      note.textContent = lang === "en" ? ui.autoNote : ui.translationNote;
      if (updated) updated.insertAdjacentElement("afterend", note);
      else content.insertAdjacentElement("afterbegin", note);
    }

    document.querySelectorAll("[data-ui]").forEach((node) => {
      const key = node.getAttribute("data-ui");
      if (ui[key]) node.textContent = ui[key];
    });

    document.querySelectorAll("[data-ui-ph]").forEach((node) => {
      const key = node.getAttribute("data-ui-ph");
      if (ui[key]) node.setAttribute("placeholder", ui[key]);
    });

    const select = document.getElementById("languageSelect");
    if (select) {
      select.value = lang;
      select.setAttribute("aria-label", ui.languageLabel);
    }
  }

  function populateLanguageSelect() {
    const select = document.getElementById("languageSelect");
    if (!select) return;
    select.innerHTML = "";
    LANGS.forEach((lang) => {
      const option = document.createElement("option");
      option.value = lang.code;
      option.textContent = lang.label;
      select.appendChild(option);
    });
    select.addEventListener("change", () => {
      const lang = select.value;
      try {
        localStorage.setItem(STORAGE_KEY, lang);
      } catch (error) {
        /* localStorage can be unavailable in strict privacy modes. */
      }
      render(lang);
      try {
        window.dispatchEvent(new Event("vibeit:lang"));
      } catch (error) {
        /* Event dispatch is non-critical. */
      }
    });
  }

  function storedLanguage() {
    try {
      const value = localStorage.getItem(STORAGE_KEY);
      return SUPPORTED.has(value) ? value : "";
    } catch (error) {
      return "";
    }
  }

  function queryLanguage() {
    try {
      const value = new URLSearchParams(window.location.search).get("lang");
      const lang = normalizedLang(value);
      return SUPPORTED.has(lang) ? lang : "";
    } catch (error) {
      return "";
    }
  }

  async function geoLanguage() {
    if (!window.fetch || !window.AbortController) return "";
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 4000);
    try {
      const response = await fetch(GEO_ENDPOINT, {
        signal: controller.signal,
        cache: "no-store",
        referrerPolicy: "strict-origin-when-cross-origin"
      });
      if (!response.ok) return "";
      const data = await response.json();
      const country = String(data.country || "").toUpperCase();
      return COUNTRY_TO_LANG[country] || "";
    } catch (error) {
      return "";
    } finally {
      window.clearTimeout(timeout);
    }
  }

  async function chooseInitialLanguage() {
    const requested = queryLanguage();
    if (requested) {
      try {
        localStorage.setItem(STORAGE_KEY, requested);
      } catch (error) {
        /* Ignore storage failures. */
      }
      render(requested);
      return;
    }

    const saved = storedLanguage();
    if (saved) {
      render(saved);
      return;
    }

    const fromGeo = await geoLanguage();
    render(fromGeo || fallbackFromBrowser());
  }

  populateLanguageSelect();
  render("en");
  chooseInitialLanguage();
})();
