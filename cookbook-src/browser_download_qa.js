async page => {
  await page.goto('http://127.0.0.1:8764/vibeit/cookbook/');
  const courses=await page.evaluate(async()=>(await fetch('/vibeit/cookbook/manifest.json')).json());
  const paths=courses.flatMap(c=>Object.values(c.downloads));
  const disciplines=[...new Set(courses.map(c=>c.discipline))];
  paths.push('/vibeit/cookbook/downloads/vibeit-cookbook.zip');
  for(const id of disciplines) paths.push('/vibeit/cookbook/downloads/vibeit-'+id+'-cookbook.zip');
  const downloads=[];
  for(const path of paths){
    const owner=courses.find(c=>Object.values(c.downloads).includes(path));
    const locale=owner ? Object.keys(owner.downloads).find(k=>owner.downloads[k]===path) : 'en';
    const subject=disciplines.find(id=>path.endsWith('vibeit-'+id+'-cookbook.zip'));
    await page.goto('http://127.0.0.1:8764'+(owner ? owner.previews[locale] : subject ? '/vibeit/cookbook/'+subject+'/' : '/vibeit/cookbook/'));
    const promise=page.waitForEvent('download');
    await page.locator('a[download][href="'+path+'"]').first().click();
    const download=await promise;
    const filename=path.split('/').pop();
    await download.saveAs('/tmp/vibeit-browser-downloads/'+filename);
    if(await download.failure())throw new Error('Download failed: '+filename);
    downloads.push({filename,status:'downloaded via browser'});
  }
  return {origin:'http://127.0.0.1:8764',downloads};
}
