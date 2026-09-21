import {mkdir,writeFile} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {topics} from '../src/data/topics.mjs';
import {locales,ui,prerequisites,groupTroubleshooting} from '../src/data/ui.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const base='/vibeit/help/';
const route=(locale,id)=>base+(locale==='en'?'':locale+'/')+id+'/';
const publicLocales=locales.filter(l=>ui[l]&&topics.every(t=>t.title[l]&&t.goal[l]&&t.steps.every(s=>s.title[l]&&s.body[l])));
for(const locale of publicLocales){
 const labels=ui[locale];
 for(const t of topics){
  const dir=path.join(root,'src/content/docs',locale==='en'?'':locale,path.dirname(t.id));await mkdir(dir,{recursive:true});
  const out=path.join(dir,path.basename(t.id)+'.mdx');
  const requirements=t.requirements.map(key=>prerequisites[locale][key]).filter(Boolean);
  const steps=t.steps.map(s=>({...s,title:s.title[locale],body:s.body[locale],iphoneBody:s.iphoneBody?.[locale]}));
  const related=t.related.map(id=>topics.find(x=>x.id===id)).filter(Boolean);
  const relativeComponents=path.relative(dir,path.join(root,'src/components')).replaceAll('\\','/');
  const content=`---\ntitle: ${JSON.stringify(t.title[locale])}\ndescription: ${JSON.stringify(t.goal[locale])}\nsidebar:\n  order: ${t.order}\n---\n\nimport ArticleMeta from '${relativeComponents}/ArticleMeta.astro';\nimport TutorialSteps from '${relativeComponents}/TutorialSteps.astro';\n\n<ArticleMeta labels={${JSON.stringify(labels)}} requirement={${JSON.stringify(t.requirements.includes('pro')?'Pro':t.requirements.includes('subscription')?'Standard / Pro':null)}} shotLocale="${locale.startsWith('zh-')?'简体中文':'English'}" aliases={${JSON.stringify(t.aliases??[])}} />\n\n## ${labels.goal}\n\n${t.goal[locale]}\n\n## ${labels.before}\n\n${requirements.map(x=>'- '+x).join('\n')}\n\n[${labels.examples}](${base}downloads/vibeit-tutorials.zip)\n\n## ${labels.entry}\n\n<div className="entry-path">${t.entry.replaceAll('&','&amp;').replaceAll('<','&lt;')}</div>\n\n${t.note?.[locale]?`:::note[${labels.note}]\n${t.note[locale]}\n:::\n`:''}\n## ${labels.steps}\n\n<TutorialSteps id="${t.id.replaceAll('/','-')}" locale="${locale}" labels={${JSON.stringify(labels)}} steps={${JSON.stringify(steps)}} />\n\n## ${labels.expected}\n\n${t.expected?.[locale]??steps.at(-1).body}\n\n## ${labels.troubleshooting}\n\n${groupTroubleshooting[locale][t.group].map(x=>'- '+x).join('\n')}\n\n## ${labels.next}\n\n${related.map(r=>`- [${r.title[locale]}](${route(locale,r.id)})`).join('\n')}\n\n${t.links?.length?`## ${labels.references}\n\n${t.links.map(([label,url])=>`- [${label}](${url})`).join('\n')}\n`:''}\n[${labels.support}](https://www.mecury.co.uk/vibeit/contact.html)\n`;
  await writeFile(out,content);
 }
 const folder=path.join(root,'src/content/docs',locale==='en'?'':locale);await mkdir(folder,{recursive:true});
 const popular=['getting-started/first-run','ai/codex','ai/reasoning','models/hugging-face','git/clone','remote/ssh'];
 const links=popular.map(id=>topics.find(t=>t.id===id)).filter(Boolean);
 const index=`---\ntitle: ${JSON.stringify(labels.siteTitle)}\ndescription: ${JSON.stringify(labels.intro)}\n---\n\n${labels.intro}\n\n## ${labels.popular}\n\n${links.map(t=>`- [${t.title[locale]}](${route(locale,t.id)}) — ${t.goal[locale]}`).join('\n')}\n\n## ${labels.all}\n\n${topics.map(t=>`- [${t.title[locale]}](${route(locale,t.id)})`).join('\n')}\n\n[${labels.examples}](${base}downloads/vibeit-tutorials.zip)\n\n[${labels.support}](https://www.mecury.co.uk/vibeit/contact.html)\n`;
 await writeFile(path.join(folder,'index.mdx'),index);
}
console.log(`Generated ${topics.length} topics in ${publicLocales.length} completed source languages. Required languages: ${locales.length}.`);
