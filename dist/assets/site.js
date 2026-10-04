(() => {
  'use strict';
  const nav = document.querySelector('#navigation');
  const toggle = document.querySelector('#mobile-toggle');
  const closeMenus = () => document.querySelectorAll('.submenu-toggle').forEach(button => {
    button.setAttribute('aria-expanded', 'false');
    document.getElementById(button.getAttribute('aria-controls')).hidden = true;
  });
  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    if (!open) closeMenus();
  });
  document.querySelectorAll('.submenu-toggle').forEach(button => {
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') !== 'true';
      closeMenus();
      button.setAttribute('aria-expanded', String(open));
      document.getElementById(button.getAttribute('aria-controls')).hidden = !open;
    });
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.nav-group')) closeMenus();
    if (nav?.classList.contains('is-open') && !event.target.closest('.site-header')) {
      nav.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false');
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      const focused = document.activeElement.closest?.('.nav-group');
      if (focused && focused.querySelector('.submenu-toggle').getAttribute('aria-expanded') === 'true') {
        closeMenus(); focused.querySelector('.submenu-toggle').focus();
      } else if (nav?.classList.contains('is-open')) {
        closeMenus(); nav.classList.remove('is-open'); toggle.setAttribute('aria-expanded','false'); toggle.focus();
      } else closeMenus();
    }
  });
  const desktop = window.matchMedia('(min-width: 1281px)');
  desktop.addEventListener('change', () => { nav?.classList.remove('is-open'); toggle?.setAttribute('aria-expanded','false'); closeMenus(); });
  // The shipped pages work from disk and at a local HTTP preview. Pretty URLs
  // are applied only when served; the HTML itself retains portable links.
  if (location.protocol !== 'file:') {
    const ownRoute = document.body.dataset.route;
    document.querySelectorAll('.submenu a[data-route]').forEach(a=>{if(a.dataset.route===ownRoute)a.setAttribute('aria-current','page');});
    const currentPath = location.pathname.replace(/\/index\.html$/, '').replace(/\/$/, '');
    const base = ownRoute === '/' ? currentPath : currentPath.endsWith(ownRoute) ? currentPath.slice(0, -ownRoute.length) : '';
    document.querySelectorAll('a[data-route]').forEach(a => { a.href = base + a.dataset.route; });
  }
  document.querySelectorAll('[data-enquiry]').forEach(form => {
    const input = name => form.elements.namedItem(name);
    const interest = new URLSearchParams(location.search).get('interest');
    if (interest && input('interest')) {
      let selected = interest;
      if (form.dataset.enquiry === 'support' && ['livelihood','environment','human-rights','animal-welfare'].includes(interest)) selected = 'future';
      if ([...input('interest').options].some(option => option.value === selected)) input('interest').value = selected;
    }
    for (const field of form.querySelectorAll('input,select,textarea')) {
      if (field.id) field.setAttribute('aria-describedby', [document.getElementById(field.id+'-help') ? field.id+'-help' : '', document.getElementById(field.id+'-error') ? field.id+'-error' : ''].filter(Boolean).join(' '));
    }
    form.addEventListener('submit', async event => {
      event.preventDefault();
      const summary = form.querySelector('.error-summary');
      const result = form.querySelector('.form-result');
      summary.hidden = true; summary.replaceChildren(); result.textContent = '';
      form.querySelectorAll('.field-error').forEach(p => { p.textContent = ''; });
      form.querySelectorAll('[aria-invalid]').forEach(field => field.removeAttribute('aria-invalid'));
      const errors = [];
      const error = (name,message) => {
        if (errors.some(item => item.name === name)) return;
        const field=input(name); field?.setAttribute('aria-invalid','true');
        const el=document.getElementById(name+'-error'); if(el) el.textContent=message;
        errors.push({name,message});
      };
      form.querySelectorAll('[required]').forEach(field => {
        if (field.type==='checkbox' ? !field.checked : !field.value.trim()) {
          error(field.name, field.name==='consent' ? 'Please confirm your contact consent.' : 'Please complete '+(form.querySelector(`label[for="${field.id}"]`)?.textContent.replace('*','').trim().toLowerCase() || field.name)+'.');
        }
      });
      const email=input('email')?.value.trim() || '', phone=input('phone')?.value.trim() || '';
      if (!email && !phone) { error('email','Please provide an email address or phone number.'); error('phone','Please provide a phone number or email address.'); }
      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) error('email','Please enter a valid email address.');
      if (phone && (!/^[+()\d\s.-]+$/.test(phone) || phone.replace(/\D/g,'').length < 7 || phone.replace(/\D/g,'').length > 15)) error('phone','Please enter a phone number with 7–15 digits.');
      const age=input('age');
      if (age && age.value && (!Number.isInteger(Number(age.value)) || Number(age.value)<1 || Number(age.value)>120)) error('age','Please enter your age as a whole number from 1 to 120.');
      if (input('availability')?.value==='describe' && !input('message').value.trim()) error('message','Please describe your availability here.');
      if (errors.length) {
        const strong=document.createElement('strong'); strong.textContent='Please check your enquiry.';
        const list=document.createElement('ul');
        errors.forEach(({name,message}) => { const li=document.createElement('li'), a=document.createElement('a'); a.href='#'+name; a.textContent=message; a.addEventListener('click', () => input(name)?.focus()); li.append(a); list.append(li); });
        summary.append(strong,list); summary.hidden=false; summary.focus(); return;
      }
      const config=window.AASHRAY_CONFIG || {};
      if (!config.enquiryEndpoint || !config.formsApproved) {
        result.textContent='Preview check complete. Your enquiry has not been sent or stored. Form delivery and approved privacy arrangements are still required before submissions can be received.';
        result.focus(); return;
      }
      if(input('website').value) { result.textContent='Your enquiry could not be sent. Please check the fields and try again.'; return; }
      const button=form.querySelector('[type=submit]'); const label=button.textContent;
      button.disabled=true;button.textContent='Sending enquiry…';
      try {
        const response=await fetch(config.enquiryEndpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:form.dataset.enquiry,...Object.fromEntries(new FormData(form))}),signal:AbortSignal.timeout(15000)});
        const payload=await response.json();
        if (!response.ok || payload.received!==true) throw new Error('Receipt not confirmed');
        result.textContent='Thank you. Your enquiry has been received. Our team will respond using the contact details you provided.';
        form.reset();
      } catch {
        result.textContent='Your enquiry could not be confirmed as received. Your details remain in this form. Please try again or use the official contact details once available.';
      } finally {button.disabled=false;button.textContent=label;result.focus();}
    });
  });
  const storyCategories = {
    'All stories':[0,1], 'Community & Relief':[0,1], 'Roti Challenge Memories':[1],
    'Volunteer Stories':[], 'Health & Wellbeing':[], 'Education Updates':[]
  };
  const results = document.querySelector('[data-archive]');
  if(results) {
    const cards=[...results.querySelectorAll('.story-card')].map(card => card.cloneNode(true));
    document.querySelectorAll('.filter').forEach(button => button.addEventListener('click', () => {
      document.querySelectorAll('.filter').forEach(item=>{item.classList.toggle('active',item===button);item.setAttribute('aria-pressed',String(item===button));});
      if(results.dataset.archive==='news') {results.textContent='Updates in '+button.dataset.category+' will be shared as activities and program details are confirmed.';return;}
      results.replaceChildren();
      const indexes=storyCategories[button.dataset.category] || [];
      if(!indexes.length) {const empty=document.createElement('p');empty.className='empty-state';empty.textContent='Stories in this area will be shared as our archive grows.';results.append(empty);}
      else {const grid=document.createElement('div');grid.className='story-grid';indexes.forEach(index=>grid.append(cards[index].cloneNode(true)));results.append(grid);}
    }));
  }
})();
