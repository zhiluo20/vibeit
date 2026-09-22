import {readFile,writeFile,mkdir,readdir} from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import sharp from 'sharp';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const source=process.argv[2];
if(!source)throw Error('Provide a private xcresult attachment export directory. Review images before importing.');
const reviewed=new Set((process.argv.find(x=>x.startsWith('--reviewed='))??'').slice(11).split(','));
const records=JSON.parse(await readFile(path.join(source,'manifest.json')));
const manifestPath=path.join(root,'src/data/screenshots.json');
const manifest=JSON.parse(await readFile(manifestPath));
let imported=0;
for(const test of records){
 const attachments=test.attachments??[];
 for(const info of attachments.filter(x=>x.exportedFileName?.endsWith('.json'))){
  const record=JSON.parse(await readFile(path.join(source,info.exportedFileName)));
  if(!/^S\d{2}(?:-[a-z0-9]+)?$/.test(record.id??''))continue;
  const key=`${record.id}.${record.device}.${record.locale}`;
  if(!reviewed.has(key))continue;
  if(record.id==='S29'&&!record.redactions?.length)throw Error(`${key}: device authorization code needs redaction`);
  const picture=attachments.find(x=>x.exportedFileName?.endsWith('.png')&&x.suggestedHumanReadableName?.startsWith(`${record.id}.`));
  if(!picture)throw Error(`No PNG associated with ${key}`);
  const input=path.join(source,picture.exportedFileName);
  // Resolve UIImage orientation metadata into pixels. Do not redraw or alter App UI.
  let pipeline=sharp(input).rotate();
  const oriented=await pipeline.toBuffer();
  const overlays=(record.redactions??[]).map(r=>{
   const left=Math.max(0,Math.floor(r.x*record.width)-4),top=Math.max(0,Math.floor(r.y*record.height)-4);
   const width=Math.min(record.width-left,Math.ceil(r.w*record.width)+8),height=Math.min(record.height-top,Math.ceil(r.h*record.height)+8);
   if(width<=0||height<=0)throw Error(`${key}: invalid redaction`);
   return {input:Buffer.from(`<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#a8b2bf"/></svg>`),left,top};
  });
  let pixels=await sharp(oriented).composite(overlays).png().toBuffer();
  if(record.crop){
   const original={width:record.width,height:record.height};const c=record.crop;
   const left=Math.max(0,Math.floor(c.x*original.width)),top=Math.max(0,Math.floor(c.y*original.height));
   const width=Math.min(original.width,Math.ceil((c.x+c.w)*original.width))-left;
   const height=Math.min(original.height,Math.ceil((c.y+c.h)*original.height))-top;
   pixels=await sharp(pixels).extract({left,top,width,height}).png().toBuffer();
   record.originalDimensions=original;record.width=width;record.height=height;
   record.targets=Object.fromEntries(Object.entries(record.targets).map(([name,r])=>[name,{x:(r.x*original.width-left)/width,y:(r.y*original.height-top)/height,w:r.w*original.width/width,h:r.h*original.height/height}]));
  }
  const {data,info:geometry}=await sharp(pixels).webp({lossless:true}).toBuffer({resolveWithObject:true});
  if(geometry.width!==record.width||geometry.height!==record.height)throw Error(`${key}: capture dimensions do not match normalized image`);
  const file=`screenshots/${record.appVersion}/${record.device}/${record.locale}/${record.id}.webp`;
  await mkdir(path.dirname(path.join(root,'public',file)),{recursive:true});
  await writeFile(path.join(root,'public',file),data);
  manifest.assets[key]={...record,file,sha256:createHash('sha256').update(data).digest('hex'),reviewed:true,redacted:!!record.redactions?.length,reviewedAt:new Date().toISOString(),source:'XCUIScreen.main.screenshot'};
  imported++;
 }
}
manifest.capturedAt=new Date().toISOString();
await writeFile(manifestPath,JSON.stringify(manifest,null,2)+'\n');
console.log(`Imported ${imported} reviewed captures; ${Object.keys(manifest.assets).length} total.`);
