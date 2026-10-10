async page => {
  const origin='http://127.0.0.1:8764';
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.route('https://**/*',r=>new URL(r.request().url()).origin===origin?r.continue():r.abort());
  const rows=[];
  for(const locale of ['en','zh-hans']){
    for(const slug of ['imatinib-binding-pocket','antibody-target-interface']){
      await page.setViewportSize({width:1280,height:900});
      await page.goto(origin+'/vibeit/cookbook/'+(locale==='en'?'':'zh-hans/')+'bioinformatics/'+slug+'/');
      await page.waitForFunction(()=>[...document.querySelectorAll('[id^="3dmolviewer_"]')].every(e=>window[e.id.replace('3dmolviewer_','viewer_')]?.selectedAtoms({}).length>0));
      await page.waitForFunction(()=>[...document.querySelectorAll('.principle-sketch img')].every(i=>i.complete&&i.naturalWidth>0));
      const row=await page.evaluate(()=>({
        notes:document.querySelectorAll('.advanced-note').length,
        noteParagraphs:document.querySelectorAll('.advanced-note p').length,
        endnotes:document.querySelectorAll('.reading-footnotes p[id^="reading-note-"]').length,
        notesAtEnd:document.querySelector('.notebook').lastElementChild?.classList.contains('reading-footnotes'),
        noteFontSize:parseFloat(getComputedStyle(document.querySelector('.reading-footnotes p')).fontSize),
        code:document.querySelectorAll('.code-disclosure').length,
        open:document.querySelectorAll('.code-disclosure[open]').length,
        figures:document.querySelectorAll('.output>img').length,
        callouts:document.querySelectorAll('.callout').length,
        width:innerWidth,documentWidth:document.documentElement.scrollWidth,
        sketches:[...document.querySelectorAll('.principle-sketch img')].map(i=>({
          width:i.naturalWidth,height:i.naturalHeight,
          embedded:i.src.startsWith('data:image/'),visibleOutsideTechnicalNotes:!i.closest('details'),alt:!!i.alt})),
        modelAtoms:[...document.querySelectorAll('[id^="3dmolviewer_"]')].map(e=>window[e.id.replace('3dmolviewer_','viewer_')].selectedAtoms({}).length)
      }));
      const antibody=slug==='antibody-target-interface';
      if(row.notes!==0||row.endnotes!==4||!row.notesAtEnd||row.noteFontSize!==12||row.code!==14||row.open!==0||row.figures!==(antibody?5:4)||row.callouts!==5||row.width!==row.documentWidth)throw Error(JSON.stringify(row));
      if(row.sketches.length!==(antibody?2:1)||row.sketches.some(i=>!i.embedded||!i.visibleOutsideTechnicalNotes||!i.alt))throw Error('Missing accessible embedded sketches');
      if(JSON.stringify(row.modelAtoms)!==JSON.stringify(antibody?[7778]:[37,2266,208]))throw Error('Changed molecular models');
      if(antibody){
        const edges=await page.evaluate(()=>{
          const i=[...document.querySelectorAll('.principle-sketch img')].find(i=>i.src.startsWith('data:image/svg+xml'));
          return new DOMParser().parseFromString(atob(i.src.split(',')[1]),'image/svg+xml').querySelectorAll('.greeting-pair').length;
        });
        if(edges!==6)throw Error('Counting sketch must show exactly six greeting pairs');
        row.countingPairs=edges;
      }
      await page.locator('.code-disclosure summary').first().focus();await page.keyboard.press('Enter');
      if(await page.locator('.code-disclosure[open]').count()!==1)throw Error('Keyboard could not open code');
      await page.locator('.code-disclosure summary').first().click();
      await page.locator('.note-ref-link').first().click();
      await page.waitForFunction(()=>location.hash==='#reading-note-1');
      if(!await page.locator('#reading-note-1').isVisible())throw Error('Footnote link failed');
      const reading=await page.locator('.notebook').innerText();
      if(reading.includes('原理简笔画，不是实验结构')||reading.includes('Teaching sketch, not an experimental structure'))throw Error('Repeated clarification caption');
      await page.setViewportSize({width:390,height:844});
      await page.waitForFunction(()=>document.documentElement.scrollWidth<=innerWidth);
      await page.waitForFunction(()=>getComputedStyle(document.querySelector('#navCollapse')).opacity==='0'&&getComputedStyle(document.querySelector('#navCollapse')).visibility==='hidden');
      await page.screenshot({path:'/tmp/vibeit-plain-'+slug+'-'+locale+'.png'});
      const figure=page.locator('.principle-sketch').first();
      await figure.evaluate(e=>e.scrollIntoView({block:'center'}));
      await page.screenshot({path:'/tmp/vibeit-plain-sketch-'+slug+'-'+locale+'.png'});
      rows.push({locale,slug,...row,mobileOverflow:false,keyboardCodeToggle:'passed',endnoteReference:'passed'});
    }
  }
  if(errors.length)throw Error(errors.join(';'));
  return {scope:'plain-language reading, embedded sketches, preserved real outputs, keyboard code disclosure, endnotes and phone layout',rows,page_errors:errors};
}
