import {readFile,stat,access,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {topics} from '../src/data/topics.mjs';
import {locales,ui,prerequisites,groupTroubleshooting} from '../src/data/ui.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const release=process.argv.includes('--release');
const errors=[],pending=[];const require=(condition,message)=>{if(!condition)errors.push(message)};
const manifest=JSON.parse(await readFile(path.join(root,'src/data/screenshots.json')));
const capturePlan=JSON.parse(await readFile(path.join(root,'src/data/capture-plan.json')));
const requiredCaptureKeys=['ipad','iphone'].flatMap(device=>capturePlan[device].flatMap(id=>capturePlan.locales.map(locale=>`${id}.${device}.${locale}`)));
const completedBaseCaptures=requiredCaptureKeys.filter(key=>manifest.assets[key]?.reviewed).length;
for(const device of ['ipad','iphone'])for(const id of capturePlan[device])for(const locale of capturePlan.locales){const key=`${id}.${device}.${locale}`;if(!manifest.assets[key])pending.push(`${key}: required capture missing`);}
require(topics.length===32,`Expected 32 topics; got ${topics.length}`);
require(new Set(topics.map(t=>t.id)).size===topics.length,'Duplicate tutorial route');
const complete=[];
for(const locale of locales){
 const missing=[];
 if(!ui[locale])missing.push('interface labels');
 else for(const key of Object.keys(ui.en))if(!ui[locale][key])missing.push(`interface.${key}`);
 if(!prerequisites[locale])missing.push('prerequisites');
 if(!groupTroubleshooting[locale])missing.push('troubleshooting');
 for(const t of topics){
  for(const key of ['title','goal'])if(!t[key]?.[locale])missing.push(`${t.id}.${key}`);
  if(t.note&&!t.note[locale])missing.push(`${t.id}.note`);
  if(t.expected&&!t.expected[locale])missing.push(`${t.id}.expected`);
  t.steps.forEach((s,i)=>{if(!s.title?.[locale]||!s.body?.[locale])missing.push(`${t.id}.step${i+1}`);if(s.iphoneBody&&!s.iphoneBody[locale])missing.push(`${t.id}.step${i+1}.iphoneBody`)});
  for(const key of t.requirements)if(!prerequisites[locale]?.[key])missing.push(`${t.id}.requirement.${key}`);
  if(!groupTroubleshooting[locale]?.[t.group])missing.push(`${t.id}.troubleshooting`);
 }
 if(missing.length)pending.push(`${locale}: ${missing.length} missing translation fields`);else complete.push(locale);
}
for(const t of topics){
 require(t.entry&&t.requirements.length&&t.steps.length>=3,`${t.id}: missing tutorial structure`);
 for(const related of t.related)require(topics.some(x=>x.id===related),`${t.id}: unknown related route ${related}`);
 for(const step of t.steps){
  require(/^S\d{2}(?:-[a-z0-9]+)?$/.test(step.shot),`${t.id}: invalid shot ID`);
  require(!!step.target,`${t.id}: missing target name`);
  require(!step.action||['tap','longPress','swipe','input','observe'].includes(step.action),`${t.id}: invalid action`);
  for(const device of ['ipad','iphone'])for(const lang of ['en','zh-Hans']){
   const shot=device==='iphone'?(step.iphoneShot??step.shot):step.shot;
   const key=`${shot}.${device}.${lang}`,asset=manifest.assets[key];
   // iPhone shares the iPad figure only for explicitly shared states.
   if(!asset){if(device==='ipad')pending.push(`${key}: missing screenshot`);continue;}
   if(!asset.targets?.[step.target])pending.push(`${key}: missing target ${step.target}`);
  }
 }
}
for(const [key,a] of Object.entries(manifest.assets)){
 require(key===`${a.id}.${a.device}.${a.locale}`,`${key}: inconsistent identity`);
 require(a.appVersion==='1.0.1'&&a.build==='7',`${key}: wrong release baseline`);
 require(!a.file.startsWith('/')&&!a.file.includes('..'),`${key}: unsafe asset path`);
 require(a.width>0&&a.height>0,`${key}: invalid dimensions`);
 if(!a.reviewed)pending.push(`${key}: visual/privacy review pending`);
 for(const [name,r] of Object.entries(a.targets??{}))require([r.x,r.y,r.w,r.h].every(Number.isFinite)&&r.x>=0&&r.y>=0&&r.w>0&&r.h>0&&r.x+r.w<=1.001&&r.y+r.h<=1.001,`${key}.${name}: rectangle outside screenshot`);
 try {const data=await readFile(path.join(root,'public',a.file));require(createHash('sha256').update(data).digest('hex')===a.sha256,`${key}: file hash mismatch`)}catch{errors.push(`${key}: missing image file`)}
}
if(completedBaseCaptures<requiredCaptureKeys.length)pending.push(`Base screenshots: ${completedBaseCaptures}/${requiredCaptureKeys.length}`);
const gatesPath=path.join(root,'qa/acceptance.json');
const gates=JSON.parse(await readFile(gatesPath));
for(const [name,g]of Object.entries(gates.checks))if(g.status!=='passed')pending.push(`Acceptance: ${name} (${g.status})`);
await access(path.join(root,'public/downloads/vibeit-tutorials.zip')).catch(()=>errors.push('Missing sample project download'));
const uniquePending=[...new Set(pending)];
const screenshotCoverage=topics.map(topic=>({
 id:topic.id,
 title:topic.title.en,
 steps:topic.steps.map((step,index)=>({number:index+1,shot:step.shot,target:step.target,
  captures:Object.fromEntries(['ipad','iphone'].flatMap(device=>['en','zh-Hans'].map(locale=>{
   const asset=manifest.assets[`${device==='iphone'?(step.iphoneShot??step.shot):step.shot}.${device}.${locale}`];
   return [`${device}.${locale}`,!asset?'missing':!asset.targets?.[step.target]?'target-missing':asset.reviewed?'reviewed':'unreviewed'];
  })))
 }))
}));
const report={checkedAt:new Date().toISOString(),topics:topics.length,requiredLocales:locales.length,completedLocales:complete,screenshots:Object.keys(manifest.assets).length,baseScreenshots:{completed:completedBaseCaptures,required:requiredCaptureKeys.length},supplementaryScreenshots:Object.keys(manifest.assets).filter(key=>!requiredCaptureKeys.includes(key)).length,errors,pending:uniquePending,publishable:!errors.length&&!uniquePending.length};
await mkdir(path.join(root,'qa'),{recursive:true});await writeFile(path.join(root,'qa/readiness.json'),JSON.stringify(report,null,2)+'\n');
await writeFile(path.join(root,'qa/screenshot-coverage.json'),JSON.stringify(screenshotCoverage,null,2)+'\n');
console.log(`${topics.length} topics; ${complete.length}/${locales.length} complete languages; ${completedBaseCaptures}/${requiredCaptureKeys.length} base screenshots; ${report.supplementaryScreenshots} supplementary screenshots`);
console.log(`${errors.length} structural errors; ${uniquePending.length} outstanding release checks`);
errors.slice(0,20).forEach(x=>console.error(x));
if(release&&!report.publishable){console.error('Release blocked. See qa/readiness.json.');process.exitCode=1}else if(errors.length)process.exitCode=1;
