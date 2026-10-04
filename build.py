"""Build dependency-free pages from the approved, editable content master."""
import json, re, shutil, html
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
NAME = 'Siliguri Aashray Welfare Foundation'
PAGES = json.loads((ROOT / 'content.json').read_text(encoding='utf8'))
BY_ROUTE = {p['route']: p for p in PAGES}
PHOTOS = json.loads((ROOT / 'photos.json').read_text(encoding='utf8'))
PILLARS = [
 ('Children & Education','children-education','Upcoming program','education','Practical digital skills. New possibilities.'),
 ('Health & Wellbeing','health-wellbeing','Work undertaken','health','Community care, grounded in experience.'),
 ('Women & Livelihood','women-livelihood','Planned initiative','livelihood','Skills, confidence and opportunity.'),
 ('Community & Relief','community-relief','Work undertaken','relief','Practical support. Shared responsibility.'),
 ('Environment & Animal Welfare','environment-animal-welfare','Planned initiative','environment','Care for the world we share.'),
 ('Human Rights','human-rights','Planned initiative','human-rights','Dignity, awareness and inclusion.')]
MAIN = [('Home','/'),('About Us','/about-us'),('Our Work','/our-work'),('Roti Challenge','/roti-challenge'),('Impact & Stories','/impact-stories'),('Get Involved','/get-involved'),('Transparency','/transparency'),('Contact','/contact')]
POLICIES = ['/privacy-policy','/terms-conditions','/donation-policy']
CURRENT = '/'

def esc(t): return html.escape(str(t), quote=True)
def prefix(): return '../' * len(CURRENT.strip('/').split('/')) if CURRENT != '/' else './'
def href(route):
    if route.startswith('https://'): return route
    u = urlsplit(route)
    return prefix() + (u.path.strip('/')+'/' if u.path != '/' else '') + 'index.html' + ('?'+u.query if u.query else '')
def link(label, route, cls='text-link'):
    return f'<a class="{cls}" data-route="{esc(route)}" href="{esc(href(route))}">{esc(label)}</a>'
def buttons(lines):
    links=[]
    for t in lines:
        if t.startswith('Button  ') and '→' in t:
            label, route = t.removeprefix('Button  ').split('→',1)
            if route.strip().startswith('/'):
                links.append(link(label.strip(),route.strip(),'button '+('secondary' if links else 'primary')))
    return '<div class="actions">'+''.join(links)+'</div>' if links else ''
def badge(status): return f'<span class="status {"undertaken" if status=="Work undertaken" else "legacy" if status=="Legacy initiative" else "planned"}">{esc(status)}</span>'
def status_for(route):
    if route == '/roti-challenge': return 'Legacy initiative'
    return next((s for _,slug,s,_,_ in PILLARS if route=='/our-work/'+slug),'')
def section(page, heading): return next((s for s in page['sections'] if s['heading']==heading), {'heading':heading,'lines':[]})
def paragraphs(lines):
    out=[]
    for t in lines:
        if t.startswith(('Button  ','Success message:','Error message:','Validation:','Consent checkbox:','Form help:')): continue
        if t in ['Work undertaken','Upcoming program','Planned initiative','Legacy initiative']: continue
        if t.startswith('Browse:'): continue
        if '[' in t:
            out.append('<p class="confirmation-note"><span>Preview · confirmation needed</span>'+esc(t)+'</p>')
        elif t.startswith(('Empty category text:','Empty report list:','Empty state:')):
            out.append('<div class="empty-state">'+esc(t.split(':',1)[1].strip())+'</div>')
        else: out.append('<p>'+esc(t)+'</p>')
    return ''.join(out)
def cards():
    summaries=section(BY_ROUTE['/'],'Our six impact areas')['lines'][1:]
    out=''
    for i,(name,slug,status,_,short) in enumerate(PILLARS):
        summary=next((x.split(' — ',1)[1] for x in summaries if x.startswith(name+' — ')),short)
        out+=f'<a class="pillar-card" data-route="/our-work/{slug}" href="{href("/our-work/"+slug)}"><div class="card-top"><span class="number">0{i+1}</span>{badge(status)}</div><h3>{esc(name)}</h3><p>{esc(summary)}</p><span class="card-link">Explore this area</span></a>'
    return '<div class="pillar-grid">'+out+'</div>'
def photo(slug, cls='', eager=False, caption=True):
    item=PHOTOS[slug]; versions=item['variants']; full=versions[-1]['file']
    srcset=', '.join(prefix()+'assets/'+v['file']+' '+str(v['width'])+'w' for v in versions)
    sizes='(max-width: 800px) calc(100vw - 36px), (max-width: 1280px) 48vw, 620px'
    img=f'<img src="{prefix()}assets/{full}" srcset="{srcset}" sizes="{sizes}" width="{item["width"]}" height="{item["height"]}" alt="{esc(item["alt"])}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'
    return f'<figure class="field-photo {cls}"><div class="photo-frame">{img}</div>'+('<figcaption>'+esc(item['caption'])+'</figcaption>' if caption else '')+'</figure>'

def photo_gallery():
    keys=['meal-packing','roti-contribution','community-together','shared-kitchen','community-outreach','packed-meals','food-preparation','volunteers-together','sharing-refreshments']
    items=''
    for key in keys:
        item=PHOTOS[key]
        items+=f'<button class="gallery-photo" type="button" data-photo="{prefix()}assets/{item["variants"][-1]["file"]}" data-caption="{esc(item["caption"])}" data-alt="{esc(item["alt"])}" aria-label="Enlarge photograph: {esc(item["alt"])}">'+photo(key,caption=False).replace('<figure','<span').replace('</figure>','</span>').replace('<div','<span').replace('</div>','</span>')+'<span>'+esc(item['caption'])+'</span><span class="enlarge-label">View photograph</span></button>'
    return '<section class="photo-archive"><p class="eyebrow">THE ORGANISATION PHOTO COLLECTION</p><h2>Care, in everyday moments.</h2><p>Food preparation, community participation and the people who make it possible. These photographs come from the organisation’s own collection. Activity dates and locations are being documented.</p><div class="photo-gallery">'+items+'</div><dialog id="photo-viewer" aria-label="Enlarged organisation photograph"><button type="button" class="viewer-close" aria-label="Close enlarged photograph">Close ×</button><img alt=""><p></p></dialog></section>'

def story_cards():
    items=[('OUR ORIGIN · SILIGURI','From Bharosa to Aashray','A lockdown food response became the beginning of a wider community mission.','Read Our Story','/about-us','community-together'),('LEGACY INITIATIVE · 2020','The Roti Challenge','Families contributed rotis weekly. Volunteers collected, packed and distributed the food.','Read the Roti Challenge Story','/roti-challenge','roti-contribution')]
    return '<div class="story-grid">'+''.join('<article class="story-card">'+photo(slug,'story-photo',caption=False)+'<div class="story-card-copy"><span class="eyebrow">'+tag+'</span><h3>'+title+'</h3><p>'+text+'</p>'+link(label,url)+'<p class="photo-context">Photo from the wider organisation collection; not a dated record of the 2020 initiative.</p></div></article>' for tag,title,text,label,url,slug in items)+'</div>'

def photo_slot(label='Genuine field photograph',detail='Approved photograph and factual caption to be added.'):
    return f'<figure class="photo-slot"><div class="photo-label"><span class="eyebrow">PHOTO SPACE · PREVIEW</span><strong>{esc(label)}</strong><p>{esc(detail)}</p></div><figcaption>Awaiting an approved field photograph</figcaption></figure>'
def header():
    nav=''
    for label,url in MAIN:
        active=' aria-current="page"' if CURRENT==url else ''
        anchor=f'<a data-route="{url}" href="{href(url)}"{active}>{label}</a>'
        if url in ['/our-work','/get-involved']:
            entries=[('Overview',url)]+([(n,'/our-work/'+slug) for n,slug,_,_,_ in PILLARS] if url=='/our-work' else [('Volunteer','/volunteer'),('Partner With Us','/partner-with-us'),('Support Our Work','/support-our-work')])
            nav+=f'<div class="nav-group" data-active="{str(CURRENT.startswith(url+'/') or (url=='/get-involved' and CURRENT in ['/volunteer','/partner-with-us','/support-our-work'])).lower()}">{anchor}<button class="submenu-toggle" aria-expanded="false" aria-controls="menu-{url[1:]}" aria-label="Open {label} menu"><span aria-hidden="true">⌄</span></button><div class="submenu" id="menu-{url[1:]}" hidden>'+''.join(link(n,u,'') for n,u in entries)+'</div></div>'
        else: nav+=anchor
    identity=f'<img src="{prefix()}assets/Siliguri-Aashray-Logo.png" width="1090" height="350" alt="{NAME}">'
    return f'<a class="skip-link" href="#main">Skip to content</a><div class="preview-bar">Website preview <span>·</span> Forms are not connected. Policy drafts await approval.</div><header class="site-header"><div class="header-inner"><a class="brand" data-route="/" href="{href("/")}" aria-label="{NAME} home">{identity}</a><button id="mobile-toggle" class="mobile-toggle" aria-controls="navigation" aria-expanded="false">Menu <span aria-hidden="true">☰</span></button><nav id="navigation" aria-label="Main navigation">{nav}</nav>{link("Support Our Work","/support-our-work","button header-cta")}</div></header>'
def footer():
    groups=[('Explore',[('About Us','/about-us'),('Our Work','/our-work'),('Roti Challenge','/roti-challenge'),('Impact & Stories','/impact-stories'),('News & Updates','/news')]),('Participate',[('Get Involved','/get-involved'),('Volunteer','/volunteer'),('Partner With Us','/partner-with-us'),('Support Our Work','/support-our-work')]),('Trust & information',[('Transparency','/transparency'),('Contact','/contact'),('Privacy Policy','/privacy-policy'),('Terms & Conditions','/terms-conditions'),('Donation and Refund Policy','/donation-policy')])]
    return '<footer><div class="container footer-grid"><div class="footer-about"><p class="eyebrow">ROOTED IN SILIGURI</p><h2>Siliguri Aashray<br>Welfare Foundation</h2><p>Born from community care during the 2020 lockdown, Aashray brings people together to support dignity, wellbeing and opportunity.</p><p class="footer-confirmation">Preview: official contact details and verified social profiles await confirmation.</p></div>'+''.join('<div><h3>'+n+'</h3>'+''.join(link(label,url,'footer-link') for label,url in entries)+'</div>' for n,entries in groups)+'</div><div class="container footer-bottom"><p>© 2026 Siliguri Aashray Welfare Foundation. All rights reserved.</p><p>Crafted &amp; Maintained by <a href="https://redpumpkin.in" target="_blank" rel="noopener noreferrer">Red Pumpkin Marketing</a></p></div></footer>'
def hero_media(route):
    mapping={'/about-us':'community-together','/our-work':'meal-packing','/our-work/community-relief':'community-outreach','/roti-challenge':'roti-contribution','/impact-stories':'volunteers-together','/get-involved':'community-together','/volunteer':'shared-kitchen','/partner-with-us':'team-conversation','/support-our-work':'food-parcels','/contact':'volunteers-together'}
    slug=mapping.get(route)
    return photo(slug,'inner-hero-photo',eager=True) if slug else ''

def hero(page):
    lines=section(page,'Hero')['lines']
    title=lines[0] if lines else page['name']
    rest=[x for x in lines[1:] if not x.startswith('Button  ')]
    status=status_for(page['route'])
    return f'<section class="page-hero"><div class="container"><div class="breadcrumb">{link("Home","/","")}<span>/</span><span>{esc(page["name"].replace(" and "," & "))}</span></div><div class="inner-hero-grid {"has-photo" if hero_media(page["route"]) else ""}"><div class="hero-copy"><span class="eyebrow">{esc(page["name"].replace(" and "," & "))}</span>{badge(status) if status else ""}<h1>{esc(title)}</h1>{paragraphs(rest)}{buttons(lines)}</div>{hero_media(page["route"])}</div></div></section>'
def home():
    p=BY_ROUTE['/']
    out=f'<section class="home-hero"><div class="container hero-grid"><div><p class="eyebrow">SILIGURI ROOTS. A SHARED FUTURE.</p><h1>Aashray for <em>Hope.</em><br>Aashray for <em>Dignity.</em><br>Aashray for <em>Everyone.</em></h1>{paragraphs(section(p,"Hero")["lines"][1:])}{buttons(section(p,"Hero")["lines"])}</div><div class="hero-photography">{photo("meal-packing", "hero-field-photo", eager=True)}<div class="hero-photo-note"><span>ROOTED IN COMMUNITY</span><strong>Care becomes meaningful when we act together.</strong></div></div></div></section>'
    s=section(p,'Our story began in 2020')
    out+=f'<section class="section origin-section"><div class="container split"><div class="origin-year" aria-hidden="true">20<br>20<span>BHAROSA GROUP<br>SILIGURI</span></div><div><p class="eyebrow">OUR STORY BEGAN IN 2020</p><h2>{esc(s["lines"][0])}</h2>{paragraphs(s["lines"][1:])}{buttons(s["lines"])}</div></div></section>'
    out+='<section class="section"><div class="container"><div class="section-heading"><p class="eyebrow">OUR SIX IMPACT AREAS</p><h2>Immediate care.<br>Longer-term opportunity.</h2><p>'+esc(section(p,'Our six impact areas')['lines'][0])+'</p></div>'+cards()+'</div></section>'
    s=section(p,'Our work and next steps')
    out+='<section class="section navy"><div class="container split"><div><p class="eyebrow">OUR WORK AND NEXT STEPS</p><h2>Every step has<br>its own beginning.</h2></div><div>'+paragraphs(s['lines'])+buttons(s['lines'])+'<div class="stage-row">'+badge('Work undertaken')+badge('Upcoming program')+badge('Planned initiative')+'</div></div></div></section>'
    s=section(p,'Roti Challenge')
    out+='<section class="section roti-section"><div class="container split"><div><p class="eyebrow">THE ROTI CHALLENGE · 2020</p>'+badge('Legacy initiative')+'<h2>'+esc(s['lines'][0])+'</h2>'+paragraphs(s['lines'][1:])+buttons(s['lines'])+'</div><div class="roti-process"><p class="eyebrow">A WEEKLY COMMUNITY EFFORT</p><ol>'+''.join('<li><span>'+n+'</span><strong>'+t+'</strong></li>' for n,t in [('01','Families prepared rotis at home'),('02','Volunteers collected from homes'),('03','Food was packed at the work location'),('04','Meals went out for distribution')])+'</ol>'+photo('packed-meals','roti-detail-photo')+'</div></div></section>'
    s=section(p,'Impact and stories')
    out+='<section class="section archive-section"><div class="container split"><div><p class="eyebrow">THE IMPACT ARCHIVE</p><h2>'+esc(s['lines'][0])+'</h2>'+paragraphs(s['lines'][1:])+buttons(s['lines'])+'</div>'+photo('community-outreach','archive-field-photo')+'</div></section>'
    out+='<section class="section"><div class="container"><p class="eyebrow">STORIES FROM THE COMMUNITY</p><h2>The people behind<br>the beginning.</h2>'+story_cards()+'</div></section>'
    s=section(p,'Get involved')
    out+='<section class="section involvement"><div class="container split"><div>'+photo('volunteers-together','participation-photo')+'<p class="eyebrow">GET INVOLVED</p><h2>'+esc(s['lines'][0])+'</h2></div><div>'+paragraphs(s['lines'][1:])+buttons(s['lines'])+'</div></div></section>'
    out+='<section class="section"><div class="container two-columns">'
    for heading,title in [('Working together','Good work grows together.'),('Transparency and trust','Trust grows through honest communication.')]:
        s=section(p,heading)
        texts=s['lines'][1:] if heading=='Transparency and trust' else s['lines']
        out+='<article class="editorial-block"><p class="eyebrow">'+esc(heading.upper())+'</p><h2>'+title+'</h2>'+paragraphs(texts)+buttons(s['lines'])+'</article>'
    out+='</div></section>'
    s=section(p,'Closing invitation')
    return out+'<section class="section closing"><div class="container"><p class="eyebrow">A SHARED FUTURE</p><h2>'+esc(s['lines'][0])+'</h2>'+paragraphs(s['lines'][1:])+buttons(s['lines'])+'</div></section>'

BASE_INTERESTS=[('education','Education'),('health','Health'),('relief','Community Relief'),('livelihood','Women & Livelihood'),('environment','Environment'),('animal-welfare','Animal Welfare'),('human-rights','Human Rights Awareness')]
def field(name,label,kind='text',required=False,options=None,help=''):
    req=' required' if required else ''
    label=label+(' <span aria-hidden="true">*</span>' if required else ' <span class="optional">(optional)</span>')
    if options is not None:
        control=f'<select id="{name}" name="{name}"{req}><option value="">Choose an option</option>'+''.join(f'<option value="{esc(v)}">{esc(l)}</option>' for v,l in options)+'</select>'
    elif kind=='textarea': control=f'<textarea id="{name}" name="{name}" rows="4" maxlength="3000"{req}></textarea>'
    else:
        attrs={'name':' autocomplete="name"','email':' autocomplete="email"','phone':' autocomplete="tel"','location':' autocomplete="address-level2"','organisation':' autocomplete="organization"'}.get(name,'')
        if kind=='tel': attrs+=' inputmode="tel"'
        if kind=='email': attrs+=' autocapitalize="none" spellcheck="false"'
        if kind=='number': attrs+=' min="1" max="120" step="1"'
        control=f'<input type="{kind}" id="{name}" name="{name}" maxlength="200"{attrs}{req}>'
    return f'<div class="field {"wide" if kind=="textarea" else ""}"><label for="{name}">{label}</label>{control}<p class="field-help" id="{name}-help">{esc(help)}</p><p class="field-error" id="{name}-error"></p></div>'
def form(kind):
    f=''; b=BY_ROUTE[CURRENT]
    if kind=='partnership': f+=field('organisation','Organisation name',required=True)+field('name','Contact person',required=True)
    else: f+=field('name','Full name' if kind=='volunteer' else 'Name',required=True)
    if kind=='volunteer': f+=field('age','Age','number',True,help='Participation and guardian arrangements will be confirmed before activities.')
    f+=field('email','Email','email',help='Provide email or phone; at least one is required.')+field('phone','Phone','tel',help='Provide phone or email; at least one is required.')
    if kind=='volunteer':
        f+=field('location','City or locality',required=True)
        f+=field('interest','Area of interest',required=True,options=BASE_INTERESTS+[('skills','Share my skills'),('media','Photography/Media'),('events','Event Support'),('other','Other')])
        f+=field('availability','Availability',required=True,options=[('weekdays','Weekdays'),('weekends','Weekends'),('occasional','Occasional'),('describe','Other — describe below')])
        f+=field('skills','Skills or profession')+field('message','Why would you like to volunteer?','textarea')
        consent=f'I agree that {NAME} may use the information I provide to review my volunteer enquiry and contact me about it.'
        label='Apply to Volunteer'
    elif kind=='partnership':
        f+=field('organisation-type','Organisation type',options=[('business','Business'),('education','Educational Institution'),('health','Health Institution'),('ngo','NGO/Community Group'),('professional','Individual Professional'),('other','Other')])
        f+=field('interest','Area of interest',options=[(k,v.replace('Education','Children & Education').replace('Health','Health & Wellbeing')) for k,v in BASE_INTERESTS if k!='animal-welfare']+[('general','General Partnership'),('material','Material Support'),('other','Other')])
        f+=field('location','Location')+field('message','Proposed contribution or collaboration','textarea',True)
        consent='I agree that Aashray may use these details to review and respond to my partnership enquiry.'
        label='Send Partnership Enquiry'
    elif kind=='support':
        f+=field('support-type','Type of support',options=[('financial','Financial'),('material','Material'),('professional','Professional'),('program','Program Sponsorship'),('other','Other')])
        f+=field('interest','Area of interest',options=[('relief','Community & Relief'),('health','Health & Wellbeing'),('education','Upcoming Computer Training'),('future','Future Initiatives'),('needed','Where Support Is Needed')])
        f+=field('message','Message','textarea',True)
        consent='I agree that Aashray may use these details to respond to my support enquiry.'
        label='Enquire About Supporting Aashray'
    else:
        f+=field('interest','I am interested in',options=[('volunteer','Volunteer'),('support','Support/Donation Enquiry'),('partnership','Partnership'),('education','Education'),('health','Health'),('relief','Community Relief'),('other','Other'),('livelihood','Women & Livelihood'),('human-rights','Human Rights'),('transparency','Transparency')])
        f+=field('message','Message','textarea',True)
        consent=f'I agree that {NAME} may use my details to respond to this enquiry.'
        label='Send Message'
    return f'<div class="form-card"><div class="form-intro"><span class="eyebrow">{kind.upper()} ENQUIRY</span><h2>Start with a conversation.</h2><p class="preview-note"><strong>Form preview — not connected.</strong> You can check the fields and validation. No enquiry is sent or stored. Delivery and approved privacy practices must be configured before the form opens.</p><p>Fields marked * are required. Please provide at least one contact method. Do not share identification documents or sensitive personal information.</p></div><form data-enquiry="{kind}" novalidate><div class="error-summary" role="alert" tabindex="-1" hidden></div><div class="form-grid">{f}</div><div class="consent-field"><label class="consent"><input id="consent" name="consent" type="checkbox" required><span>{esc(consent)} I have read the {link("Privacy Policy","/privacy-policy","")} (draft for review).</span></label><p class="field-error" id="consent-error"></p></div><div class="honeypot" aria-hidden="true"><label>Leave this field empty<input name="website" tabindex="-1" autocomplete="off"></label></div><button class="button primary" type="submit">{label}</button><p class="form-result" role="status" aria-live="polite" tabindex="-1"></p></form></div>'

def filters(kind):
    opts=['All stories','Community & Relief','Roti Challenge Memories','Volunteer Stories','Health & Wellbeing','Education Updates'] if kind=='stories' else ['All Updates','Foundation Updates','Community Activities','Upcoming Programs','Announcements','Press & Media']
    return '<div class="archive-filters" role="group" aria-label="'+('Story' if kind=='stories' else 'News')+' categories">'+''.join(f'<button class="filter {"active" if i==0 else ""}" type="button" data-category="{esc(x)}" aria-pressed="{"true" if i==0 else "false"}">{esc(x)}</button>' for i,x in enumerate(opts))+'</div>'
def generic(page):
    route=page['route']; out=hero(page)
    if route=='/our-work': return out+'<section class="section"><div class="container">'+cards()+'<div class="editorial-block">'+paragraphs(section(page,'Help shape what comes next')['lines'])+buttons(section(page,'Help shape what comes next')['lines'])+'</div></div></section>'
    out+='<div class="container page-content">'
    if route.startswith('/our-work/') or route=='/roti-challenge': out+='<aside class="page-aside"><p class="eyebrow">ON THIS PAGE</p>'+''.join(f'<a href="#section-{i}">{esc(s["heading"])}</a>' for i,s in enumerate(page['sections']) if s['heading'] not in ['Hero','Search preview'])+link('Our Work','/our-work','aside-back')+'</aside>'
    out+='<div class="content-sections">'
    for i,s in enumerate(page['sections']):
        heading=s['heading']; lines=s['lines']
        if heading in ['Hero','Search preview','Content for a later approved payment flow']: continue
        if heading in ['Volunteer form','Partnership enquiry form','Support enquiry form','Contact form']:
            kind={'/volunteer':'volunteer','/partner-with-us':'partnership','/support-our-work':'support','/contact':'contact'}[route]
            out+=f'<section id="section-{i}">'+form(kind)+'</section>'; continue
        if heading=='Explore our archive':
            out+='<section><h2>Explore our archive</h2>'+filters('stories')+'<div class="archive-results" aria-live="polite" data-archive="stories">'+story_cards()+'</div></section>';continue
        if route=='/impact-stories' and heading in ['Featured story one','Featured story two']:continue
        if heading=='Browse updates':
            out+='<section><h2>Browse updates</h2>'+filters('news')+'<div class="archive-results empty-state" aria-live="polite" data-archive="news">Updates will be shared here as activities and program details are confirmed.</div></section>';continue
        if heading=='Launch announcement copy':
            out+='<section class="draft-callout"><span class="eyebrow">PREVIEW · ANNOUNCEMENT DRAFT · NOT PUBLISHED</span><h2>'+esc(lines[0])+'</h2>'+paragraphs([x for x in lines[1:] if not x.startswith('Empty state:')])+buttons(lines)+'<p class="confirmation-note">Publication date and approval are still to be confirmed.</p></section>';continue
        if heading=='Reach our team':
            out+='<section><h2>Reach our team</h2><div class="contact-pending"><span class="eyebrow">PREVIEW · DETAILS TO CONFIRM</span><p>Official phone, email, public address, WhatsApp and verified social profiles have not been confirmed. These will be added before public launch.</p></div></section>';continue
        if heading=='How it worked':
            out+=f'<section id="section-{i}"><h2>{heading}</h2><ol class="steps">'+''.join('<li>'+esc(re.sub(r'^\d\. ','',x))+'</li>' for x in lines)+'</ol></section>';continue
        if heading=='Choose an area of interest':
            out+=f'<section id="section-{i}"><h2>{heading}</h2>'+paragraphs(lines)+'<div class="interest-links">'+''.join(link(v,'/support-our-work?interest='+k,'interest-link') for k,v in [('relief','Community & Relief'),('health','Health & Wellbeing'),('education','Upcoming Computer Training'),('future','Future Initiatives'),('needed','Where Support Is Needed')])+'</div></section>';continue
        if route in POLICIES and heading in ['Privacy Policy','Terms and Conditions','Donation and Refund Policy']:
            lines=[x for x in lines if not x.startswith('Effective date:')]
        if route=='/transparency' and heading=='Organisation details':
            lines=[x for x in lines if '[' not in x]+['Preview: legal entity, registration details and public office information require verified records before publication.']
        if route=='/transparency' and heading in ['Governance','Registrations and documents']: lines=[x for x in lines if '[' not in x]
        out+=f'<section class="content-section" id="section-{i}"><p class="eyebrow">{i:02d} / {esc(page["name"].replace(" and "," & "))}</p><h2>{esc(heading)}</h2>'+paragraphs(lines)+buttons(lines)
        if heading=='Memories from 2020': out+='<p class="photo-context">Photographs specifically verified as records of the 2020 initiative will be added here. The photographs elsewhere on this page are from the wider organisation collection.</p>'
        if route=='/about-us' and heading=='The people behind Aashray': out+=photo('volunteers-together')
        if route=='/our-work/community-relief' and heading=='Food support': out+=photo('food-preparation')
        if route=='/roti-challenge' and heading=='It was never just about roti': out+=photo('meal-packing')
        if route=='/volunteer' and heading=='Ways you may contribute': out+=photo('community-together')
        if route=='/support-our-work' and heading=='Ways to support': out+=photo('food-supplies')
        if route=='/get-involved' and heading=='Share your skills': out+=photo('preparing-a-meal')
        if heading=='Our impact archive': out+='<div class="empty-state">Activity records and verified reporting are being prepared. No unverified totals are displayed.</div>'
        out+='</section>'
    if route=='/impact-stories': out+=photo_gallery()
    return out+'</div></div>'
def policy(page):
    page=dict(page); page['sections']=[{'heading':'Hero','lines':[page['name'],'Draft for foundation review. This policy is not approved for public use.']},*page['sections']]
    return '<div class="policy-banner"><div class="container"><strong>Policy draft — approval required.</strong> Effective date, contact details and applicable arrangements are unconfirmed. This preview must not be published as an approved policy.</div></div>'+generic(page)
def shell(page,body):
    title=page['title'] or page['name']+' | '+NAME
    desc=page['description'] or ('Draft '+page['name']+' for review by '+NAME+'.')
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#122b38"><link rel="icon" href="{prefix()}assets/favicon-32.png" type="image/png" sizes="32x32"><link rel="icon" href="{prefix()}assets/Siliguri-Aashray-Favicon.png" type="image/png" sizes="512x512"><link rel="apple-touch-icon" href="{prefix()}assets/Siliguri-Aashray-Favicon.png"><link rel="stylesheet" href="{prefix()}assets/styles.css"><link rel="stylesheet" href="{prefix()}assets/photo-design.css"><link rel="stylesheet" href="{prefix()}assets/redesign.css"><link rel="stylesheet" href="{prefix()}assets/editorial.css"><link rel="stylesheet" href="{prefix()}assets/polish.css"><script defer src="{prefix()}assets/config.js"></script><script defer src="{prefix()}assets/site.js"></script><script defer src="{prefix()}assets/photo-interactions.js"></script><script defer src="{prefix()}assets/redesign.js"></script></head><body data-route="{CURRENT}">{header()}<main id="main">{body}</main>{footer()}</body></html>'
def build():
    global CURRENT
    DIST.mkdir(exist_ok=True)
    (DIST/'assets').mkdir(exist_ok=True)
    for asset in (ROOT/'assets').iterdir():
        if asset.is_file() and asset.suffix in ['.css','.js','.svg','.webp','.jpg','.jpeg','.png','.woff2']: shutil.copyfile(asset,DIST/'assets'/asset.name)
    routes=[]
    for page in PAGES:
        CURRENT=page['route']; body=home() if CURRENT=='/' else policy(page) if CURRENT in POLICIES else generic(page)
        target=DIST/CURRENT.strip('/'); target.mkdir(parents=True,exist_ok=True)
        (target/'index.html').write_text(shell(page,body),encoding='utf8'); routes.append(CURRENT)
    CURRENT='/404'
    fake={'name':'Page not found','title':'Page not found | '+NAME,'description':'Return to Aashray’s website.'}
    (DIST/'404.html').write_text(shell(fake,'<section class="section"><div class="container"><h1>This page could not be found.</h1><p>The story or update may not have been published yet.</p>'+link('Return Home','/','button primary')+'</div></section>'),encoding='utf8')
    (DIST/'robots.txt').write_text('User-agent: *\nDisallow: /\n',encoding='utf8')
    (ROOT/'routes.json').write_text(json.dumps(routes,indent=2),encoding='utf8')
    print(f'Built {len(routes)} complete pages in {DIST}')
if __name__=='__main__':
    from design_v2 import install
    install(globals())
    build()
