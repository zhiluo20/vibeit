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
