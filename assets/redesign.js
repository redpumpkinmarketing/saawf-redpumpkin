(() => {
 document.querySelectorAll('[data-select-slide]').forEach(button=>button.addEventListener('click',()=>{
  document.querySelectorAll('[data-slide]').forEach(slide=>{const active=slide.dataset.slide===button.dataset.selectSlide;slide.classList.toggle('is-current',active);slide.setAttribute('aria-hidden',String(!active));});
  document.querySelectorAll('[data-select-slide]').forEach(b=>{b.classList.toggle('active',b===button);b.setAttribute('aria-pressed',String(b===button));});
 }));
 const gallery=document.querySelector('.v2-gallery');
 if(gallery){
  const items=[...gallery.querySelectorAll('.gallery-photo')],more=document.querySelector('.gallery-more'),count=document.querySelector('.gallery-count');
  let category='All photographs',limit=18;
  const update=()=>{const matching=items.filter(i=>category==='All photographs'||i.dataset.group===category);items.forEach(i=>i.hidden=true);matching.slice(0,limit).forEach(i=>i.hidden=false);more.hidden=matching.length<=limit;count.textContent=`Showing ${Math.min(limit,matching.length)} of ${matching.length} photographs`;};
  document.querySelectorAll('[data-photo-category]').forEach(button=>button.addEventListener('click',()=>{category=button.dataset.photoCategory;limit=18;document.querySelectorAll('[data-photo-category]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));update();}));
  more.addEventListener('click',()=>{const firstNew=items.filter(i=>category==='All photographs'||i.dataset.group===category)[limit];limit+=18;update();firstNew?.focus({preventScroll:true});});update();
 }
})();
