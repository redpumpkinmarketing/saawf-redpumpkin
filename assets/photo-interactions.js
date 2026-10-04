(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const header = document.querySelector('.site-header');
  let ticking = false;
  const update = () => { header?.classList.toggle('is-scrolled', scrollY > 20); ticking = false; };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive:true });
  update();
  // Progressive enhancement: content never depends on animation to be visible.
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(({target,isIntersecting}) => {
        if (!isIntersecting) return;
        if (!reduced.matches && target.getBoundingClientRect().top > 40) {
          target.animate([{opacity:.3,transform:'translateY(22px)'},{opacity:1,transform:'translateY(0)'}], {duration:650,easing:'cubic-bezier(.2,.65,.25,1)'});
        }
        observer.unobserve(target);
      });
    }, {threshold:.12});
    document.querySelectorAll('.section-heading,.pillar-card,.field-photo,.editorial-block,.content-section,.v2-section-intro,.v2-pillar,.v2-photo-tile,.v2-participation-grid article').forEach(el=>observer.observe(el));
  }
  reduced.addEventListener('change',()=>{if(reduced.matches)document.getAnimations().forEach(a=>a.finish());});
  const viewer=document.querySelector('#photo-viewer');
  if(viewer){
    let trigger;
    document.querySelectorAll('[data-photo]').forEach(button=>button.addEventListener('click',()=>{
      trigger=button;
      const image=viewer.querySelector('img');image.src=button.dataset.photo;image.alt=button.dataset.alt;
      viewer.querySelector('p').textContent=button.dataset.caption;
      viewer.showModal();document.body.style.overflow='hidden';viewer.querySelector('button').focus();
    }));
    viewer.querySelector('.viewer-close').addEventListener('click',()=>viewer.close());
    viewer.addEventListener('click',event=>{if(event.target===viewer){const rect=viewer.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)viewer.close();}});
    viewer.addEventListener('close',()=>{document.body.style.overflow='';trigger?.focus();});
  }
})();
