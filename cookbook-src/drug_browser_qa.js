async page => {
  const origin='http://127.0.0.1:8764';
  const errors=[];page.on('pageerror',error=>errors.push(String(error)));
  await page.route('https://**/*',route=>route.abort());
  const checks=[];
  await page.setViewportSize({width:1440,height:1000});
  await page.goto(origin+'/vibeit/cookbook/');
  const manifest=await page.evaluate(async()=>await(await fetch('/vibeit/cookbook/manifest.json')).json());
  if(manifest.length!==50)throw Error('Expected 50 workflows');
  const newCourses=manifest.filter(c=>c.number>6);
  for(const locale of ['en','zh-hans']){
    const root='/vibeit/cookbook/'+(locale==='en'?'':'zh-hans/');
    await page.goto(origin+root);
    if(await page.locator('.discipline-card').count()!==8)throw Error('Missing disciplines');
    if(!(await page.locator('.discipline-card').first().textContent()).includes('8'))throw Error('Bioinformatics count');
    await page.goto(origin+root+'bioinformatics/');
    if(await page.locator('.recipe-card').count()!==8)throw Error('Missing bioinformatics lessons');
    await page.locator('#recipe-category').selectOption('drug-binding');
    if(await page.locator('.recipe-card:visible').count()!==2)throw Error('Drug category');
    await page.locator('#recipe-search').fill('HER2');
    if(await page.locator('.recipe-card:visible').count()!==1)throw Error('Drug search');
    await page.locator('#recipe-search').fill('no such recipe 987654');
    if(!await page.locator('#empty-state').isVisible())throw Error('Empty search');
    await page.locator('#recipe-search').fill('');
    await page.locator('#recipe-category').selectOption('all');
    if(await page.locator('.recipe-card:visible').count()!==8)throw Error('Reset filter');
    for(const course of newCourses){
      await page.goto(origin+course.previews[locale]);
      await page.waitForFunction(()=>{
        const holders=[...document.querySelectorAll('[id^="3dmolviewer_"]')];
        return holders.length>0&&holders.every(e=>window[e.id.replace('3dmolviewer_','viewer_')]?.selectedAtoms({}).length>0);
      });
      const row=await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth,
        images:document.querySelectorAll('.output img').length,tokens:document.querySelectorAll('.source-code span').length,
        callouts:document.querySelectorAll('.callout').length,
        viewers:[...document.querySelectorAll('[id^="3dmolviewer_"]')].map(e=>({
          atoms:window[e.id.replace('3dmolviewer_','viewer_')].selectedAtoms({}).length,
          width:e.getBoundingClientRect().width,canvas:!!e.querySelector('canvas')}))}));
      const expected=course.number===7?[37,2266,208]:[7778];
      if(JSON.stringify(row.viewers.map(v=>v.atoms))!==JSON.stringify(expected))throw Error('Model atom counts: '+JSON.stringify(row));
      if(row.documentWidth>row.width||row.images<3||row.tokens<100||row.callouts<4||row.viewers.some(v=>!v.canvas))throw Error('Reader layout');
      const downloadPromise=page.waitForEvent('download');
      await page.locator('a[download][href$=".ipynb"]').first().click();
      const download=await downloadPromise;
      await download.saveAs('/tmp/vibeit-drug-browser-downloads/'+download.suggestedFilename());
      checks.push({id:course.id,locale,viewport:'desktop',download:download.suggestedFilename(),...row});
      for(const viewport of [{width:768,height:1024},{width:390,height:844}]){
        await page.setViewportSize(viewport);
        await page.waitForFunction(()=>document.documentElement.scrollWidth<=innerWidth);
        const mobile=await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth,
          viewerWidths:[...document.querySelectorAll('[id^="3dmolviewer_"]')].map(e=>e.getBoundingClientRect().width)}));
        if(mobile.viewerWidths.some(v=>v>mobile.width))throw Error('3D overflow');
        checks.push({id:course.id,locale,viewport:viewport.width===390?'phone':'tablet',...mobile});
      }
      await page.screenshot({path:'/tmp/vibeit-drug-'+course.number+'-'+locale+'-mobile.png'});
      await page.setViewportSize({width:1440,height:1000});
      const canvas=page.locator('[id^="3dmolviewer_"]').last();
      await canvas.evaluate(e=>e.scrollIntoView({block:"center"}));
      const box=await canvas.boundingBox();
      await page.mouse.move(box.x+box.width*.5,box.y+box.height*.5);
      await page.mouse.down();await page.mouse.move(box.x+box.width*.65,box.y+box.height*.55,{steps:12});await page.mouse.up();
      await page.screenshot({path:'/tmp/vibeit-drug-'+course.number+'-'+locale+'-3d.png'});
    }
  }
  if(errors.length)throw Error(errors.join(';'));
  return {scope:'new drug lessons plus catalog/filter regression',checks,external_https_blocked:true,page_errors:errors};
}
