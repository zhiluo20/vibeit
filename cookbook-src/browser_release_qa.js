async page => {
  const origin = 'http://127.0.0.1:8764';
  await page.setViewportSize({width:1440,height:1000});
  const errors = [];
  await page.route('https://**/*',route=>route.abort());
  page.on('pageerror', error => errors.push(String(error)));
  await page.goto(origin + '/vibeit/cookbook/');
  const courses = await page.evaluate(async () => (await fetch('/vibeit/cookbook/manifest.json')).json());
  if (courses.length !== 50) throw new Error('Expected all 50 courses');
  const results = [];
  for (const locale of ['en','zh-hans']) {
    const root = '/vibeit/cookbook/' + (locale==='en' ? '' : 'zh-hans/');
    await page.goto(origin+root);
    if (await page.locator('.discipline-card').count() !== 8) throw new Error('Missing discipline');
    for (const discipline of [...new Set(courses.map(c=>c.discipline))]) {
      await page.goto(origin+root+discipline+'/');
      const cards = page.locator('.recipe-card');
      const expected = courses.filter(c=>c.discipline===discipline).length;
      if (await cards.count() !== expected) throw new Error('Missing lessons: '+discipline);
      await page.locator('#recipe-search').fill('no such recipe 987654');
      if (await cards.filter({visible:true}).count() !== 0 || !await page.locator('#empty-state').isVisible()) throw new Error('Empty search');
      await page.locator('#recipe-search').fill('');
      const categories=await page.locator('#recipe-category option').evaluateAll(options=>options.map(o=>o.value));
      await page.locator('#recipe-category').selectOption(categories[1]);
      if (await cards.filter({visible:true}).count() === 0) throw new Error('Category filter');
      await page.locator('#recipe-category').selectOption('all');
      if (await cards.filter({visible:true}).count() !== expected) throw new Error('Reset filter');
    }
    for (const course of courses) {
      await page.goto(origin+course.previews[locale],{waitUntil:'load'});
      const row=await page.evaluate(()=>({
        width:innerWidth,documentWidth:document.documentElement.scrollWidth,
        code:document.querySelectorAll('.source-code').length,
        tokens:document.querySelectorAll('.source-code span').length,
        callouts:document.querySelectorAll('.callout').length,
        images:document.querySelectorAll('.output img').length,
        intro:!!document.querySelector('.lesson-intro'),
        download:!!document.querySelector('a[download][href$=".ipynb"]'),
        schema:JSON.parse(document.querySelector('script[type="application/ld+json"]').textContent)['@type']
      }));
      if (row.documentWidth>row.width || !row.intro || !row.download || row.code<6 || row.tokens<100 || row.images<3 || row.callouts<4 || row.schema!=='LearningResource') throw new Error(course.id+': '+JSON.stringify(row));
      results.push({id:course.id,locale,viewport:'desktop',...row});
    }
  }
  await page.setViewportSize({width:390,height:844});
  for (const course of courses) {
    await page.goto(origin+course.previews['zh-hans'],{waitUntil:'load'});
    const width=await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth}));
    if(width.documentWidth>390)throw new Error('Mobile overflow: '+course.id);
    results.push({id:course.id,locale:'zh-hans',viewport:'mobile',...width});
  }
  await page.route('https://**/*',route=>route.abort());
  await page.goto(origin+'/vibeit/cookbook/chemistry/caffeine-geometry/');
  await page.locator('canvas').first().waitFor();
  const atoms=await page.evaluate(()=>Object.values(window).filter(v=>v && typeof v.selectedAtoms==='function').map(v=>v.selectedAtoms({}).length));
  if(!atoms.includes(24))throw new Error('Caffeine should have 24 atoms: '+JSON.stringify(atoms));
  if(errors.length)throw new Error('Browser errors: '+errors.join('; '));
  return {courses:50,reader_checks:results,disciplines:8,languages:2,search_and_categories:'passed',caffeine_offline_atoms:atoms,page_errors:errors};
}
