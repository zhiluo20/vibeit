const search=document.querySelector('#recipe-search');
const category=document.querySelector('#recipe-category');
const cards=[...document.querySelectorAll('[data-recipe]')];
function filterRecipes(){
  const query=(search?.value??'').normalize('NFKC').trim().toLocaleLowerCase();
  const selected=category?.value??'all';
  let count=0;
  for(const card of cards){
    const matches=(selected==='all'||card.dataset.category===selected)&&card.dataset.search.toLocaleLowerCase().includes(query);
    card.hidden=!matches;if(matches)count++;
  }
  const status=document.querySelector('#result-count');
  if(status)status.textContent=document.documentElement.lang==='zh-CN'?`显示 ${count} 个教程，共 ${cards.length} 个`:`Showing ${count} of ${cards.length} recipes`;
  const empty=document.querySelector('#empty-state');if(empty)empty.hidden=count>0;
}
search?.addEventListener('input',filterRecipes);category?.addEventListener('change',filterRecipes);
if(cards.length)filterRecipes();

// Product navigation behavior, with two available lesson languages.
const nav=document.querySelector('.site-header nav');
const navToggle=document.querySelector('#navToggle');
const navCollapse=document.querySelector('#navCollapse');
const langButton=document.querySelector('#langBtn');
const langMenu=document.querySelector('#langMenu');
const languageItems=[...(langMenu?.querySelectorAll('[role="menuitem"]')??[])];
function setNavigation(open){
  nav?.classList.toggle('open',open);
  navToggle?.setAttribute('aria-expanded',String(open));
  if(!open)setLanguageMenu(false);
}
function setLanguageMenu(open){
  langMenu?.classList.toggle('open',open);
  langButton?.setAttribute('aria-expanded',String(open));
}
navToggle?.addEventListener('click',()=>setNavigation(!nav.classList.contains('open')));
navCollapse?.querySelectorAll('.nav-links a,.nav-cta').forEach(link=>link.addEventListener('click',()=>setNavigation(false)));
langButton?.addEventListener('click',()=>{
  const open=!langMenu.classList.contains('open');
  setLanguageMenu(open);
  if(open)languageItems[0]?.focus();
});
langButton?.addEventListener('keydown',event=>{
  if(event.key==='ArrowDown'){event.preventDefault();setLanguageMenu(true);languageItems[0]?.focus();}
});
languageItems.forEach(link=>link.addEventListener('click',()=>{
  try{localStorage.setItem('vibeit_lang',link.dataset.code==='zh-hans'?'zh':'en');}catch(error){}
}));
langMenu?.addEventListener('keydown',event=>{
  const index=languageItems.indexOf(document.activeElement);
  const target={ArrowDown:(index+1)%languageItems.length,ArrowUp:(index+languageItems.length-1)%languageItems.length,Home:0,End:languageItems.length-1}[event.key];
  if(target!==undefined){event.preventDefault();languageItems[target]?.focus();}
});
document.addEventListener('click',event=>{
  if(nav&&!nav.contains(event.target))setNavigation(false);
  if(langButton&&!langButton.contains(event.target)&&!langMenu.contains(event.target))setLanguageMenu(false);
});
document.addEventListener('keydown',event=>{
  if(event.key!=='Escape')return;
  if(langMenu?.classList.contains('open')){setLanguageMenu(false);langButton.focus();}
  else if(nav?.classList.contains('open')){setNavigation(false);navToggle.focus();}
});
