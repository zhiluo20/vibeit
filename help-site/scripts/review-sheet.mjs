import {readFile,writeFile} from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
const folder=process.argv[2],output=process.argv[3];
const records=JSON.parse(await readFile(path.join(folder,'manifest.json')));const images=[];
for(const test of records)for(const f of test.attachments??[]){
 if(!f.exportedFileName.endsWith('.json'))continue;
 const m=JSON.parse(await readFile(path.join(folder,f.exportedFileName)));
 if(!m.id?.startsWith('S'))continue;
 const png=test.attachments.find(a=>a.exportedFileName.endsWith('.png')&&a.suggestedHumanReadableName.startsWith(m.id+'.'));
 if(png)images.push({id:`${m.id}.${m.device}.${m.locale}`,path:path.join(folder,png.exportedFileName),targets:Object.keys(m.targets??{}),record:m});
}
images.sort((a,b)=>a.id.localeCompare(b.id));
const width=440,height=365,columns=4;const rows=Math.ceil(images.length/columns);const pieces=[];
for(const [i,item]of images.entries()){
 const x=(i%columns)*width,y=Math.floor(i/columns)*height;
 let pixels=await sharp(item.path).rotate().png().toBuffer();
 const meta=item.record;
 const masks=(meta.redactions??[]).map(r=>{const left=Math.max(0,Math.floor(r.x*meta.width)-4),top=Math.max(0,Math.floor(r.y*meta.height)-4),w=Math.min(meta.width-left,Math.ceil(r.w*meta.width)+8),h=Math.min(meta.height-top,Math.ceil(r.h*meta.height)+8);return {input:Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><rect width="100%" height="100%" fill="#a8b2bf"/></svg>`),left,top};});
 pixels=await sharp(pixels).composite(masks).png().toBuffer();
 if(meta.crop){const c=meta.crop;const left=Math.max(0,Math.floor(c.x*meta.width)),top=Math.max(0,Math.floor(c.y*meta.height));pixels=await sharp(pixels).extract({left,top,width:Math.min(meta.width-left,Math.ceil(c.w*meta.width)),height:Math.min(meta.height-top,Math.ceil(c.h*meta.height))}).png().toBuffer();}
 pieces.push({input:await sharp(pixels).resize(width,height-30,{fit:'contain',background:'#fff'}).png().toBuffer(),left:x,top:y+30});
 pieces.push({input:Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="440" height="30"><rect width="440" height="30" fill="#e5eaf0"/><text x="8" y="21" font-family="Arial" font-size="16">${item.id}</text></svg>`),left:x,top:y});
}
await sharp({create:{width:width*columns,height:height*rows,channels:3,background:'#fff'}}).composite(pieces).png().toFile(output);
await writeFile(output+'.json',JSON.stringify(images,null,2));console.log(`Review sheet: ${images.length} actual captures`);
