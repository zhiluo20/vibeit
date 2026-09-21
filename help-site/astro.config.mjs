import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const groups = [
  ['Getting started','getting-started','开始使用'],
  ['Editing & running','notebooks','编辑与运行'],
  ['AI assistant','ai','AI 助手'],
  ['Models & environment','models','模型与环境'],
  ['Git & GitHub','git','Git 与 GitHub'],
  ['Remote development','remote','远程开发'],
  ['Shell & terminal','terminal','Shell 与终端'],
  ['Account & support','support','订阅与支持'],
];
const groupNames={
 fr:['Bien démarrer','Édition et exécution','Assistant IA','Modèles et environnement','Git et GitHub','Développement distant','Shell et terminal','Abonnement et assistance'],
 de:['Erste Schritte','Bearbeiten und Ausführen','KI-Assistent','Modelle und Umgebung','Git und GitHub','Remote-Entwicklung','Shell und Terminal','Abonnement und Hilfe'],
 th:['เริ่มต้นใช้งาน','แก้ไขและรัน','ผู้ช่วย AI','โมเดลและสภาพแวดล้อม','Git และ GitHub','พัฒนาบนเซิร์ฟเวอร์ระยะไกล','เชลล์และเทอร์มินัล','การสมัครสมาชิกและความช่วยเหลือ'],
 ja:['はじめに','編集と実行','AI アシスタント','モデルと環境','Git と GitHub','リモート開発','シェルとターミナル','サブスクリプションとサポート'],
 ko:['시작하기','편집과 실행','AI 도우미','모델과 환경','Git 및 GitHub','원격 개발','셸과 터미널','구독 및 지원'],
 es:['Primeros pasos','Edición y ejecución','Asistente de IA','Modelos y entorno','Git y GitHub','Desarrollo remoto','Shell y terminal','Suscripción y ayuda'],
 ar:['البدء','التحرير والتشغيل','مساعد الذكاء الاصطناعي','النماذج والبيئة','Git وGitHub','التطوير عن بُعد','الصدفة والطرفية','الاشتراك والدعم'],
 it:['Per iniziare','Modifica ed esecuzione','Assistente IA','Modelli e ambiente','Git e GitHub','Sviluppo remoto','Shell e terminale','Abbonamento e assistenza'],
 'zh-TW':['開始使用','編輯與執行','AI 助手','模型與環境','Git 與 GitHub','遠端開發','Shell 與終端機','訂閱與支援']
};
const langs = { root:{label:'English',lang:'en'},fr:{label:'Français'},de:{label:'Deutsch'},th:{label:'ไทย'},ja:{label:'日本語'},ko:{label:'한국어'},'zh-hans':{label:'简体中文',lang:'zh-CN'},'zh-hant':{label:'繁體中文',lang:'zh-TW'},es:{label:'Español'},ar:{label:'العربية',dir:'rtl'},it:{label:'Italiano'} };
export default defineConfig({
  site:'https://www.mecury.co.uk',
  base:'/vibeit/help',
  trailingSlash:'always',
  outDir:'../help',
  integrations:[starlight({
    title:{en:'Vibeit Help Center',fr:'Centre d’aide Vibeit',de:'Vibeit-Hilfe',th:'ศูนย์ช่วยเหลือ Vibeit',ja:'Vibeit ヘルプセンター',ko:'Vibeit 도움말 센터',es:'Centro de ayuda de Vibeit',ar:'مركز مساعدة Vibeit',it:'Centro assistenza Vibeit','zh-CN':'Vibeit 使用手册','zh-TW':'Vibeit 使用手冊'},
    description:'Learn to use Vibeit on iPad and iPhone, with real screenshots and guided steps.',
    locales:langs,
    defaultLocale:'root',
    customCss:['./src/styles/help.css'],
    head:[{tag:'meta',attrs:{name:'robots',content:process.env.HELP_RELEASE==='1'?'index,follow':'noindex,nofollow'}}],
    sidebar:groups.map(([label,directory,zh],i)=>({label,translations:{'zh-CN':zh,...Object.fromEntries(Object.entries(groupNames).map(([lang,names])=>[lang,names[i]]))},items:[{autogenerate:{directory}}]})),
    social:[{icon:'external',label:'Vibeit',href:'https://www.mecury.co.uk/vibeit/'}],
    editLink:{baseUrl:'https://github.com/zhiluo20/vibeit/edit/main/help-site/'},
    lastUpdated:false,
    pagination:true,
  })],
});
