"""Reusable future detail layouts. No records or URLs are published by default."""
from html import escape
from datetime import date

def render_detail(record,kind):
    """Return a semantic HTML body; wrap with the site's shared shell in build.py.

    A publication workflow must verify factual content, permissions and dates
    before calling this renderer and generating an actual detail route.
    """
    if kind not in ('story','news','program'): raise ValueError('Unknown detail type')
    required={'story':['title','introduction','period','location','pillar','account'],
              'news':['title','date','category','summary','account'],
              'program':['title','status','purpose','participants','location','eligibility','schedule','cost','registration']}[kind]
    for key in required:
        if not record.get(key): raise ValueError(f'Missing verified field: {key}')
    if record.get('approved') is not True: raise ValueError('Publication approval is required')
    if kind=='news': date.fromisoformat(record['date'])
    if kind=='program' and record['status'] not in ('Work undertaken','Upcoming program','Planned initiative','Legacy initiative'):
        raise ValueError('Use an approved program status')
    e=lambda x:escape(str(x),quote=True)
    out=f'<article class="container page-content"><div class="content-sections"><header><p class="eyebrow">{e(kind)}</p><h1>{e(record["title"])}</h1></header>'
    for key in required[1:]:
        out+=f'<section class="content-section"><h2>{e(key.replace("_"," ").title())}</h2><p>{e(record[key])}</p></section>'
    if record.get('quote') and record.get('quote_permission'):
        out+='<blockquote>'+e(record['quote'])+'</blockquote>'
    if record.get('image') and record.get('image_permission') and record.get('image_description') and record.get('caption'):
        out+=f'<figure><img src="{e(record["image"])}" alt="{e(record["image_description"])}" loading="lazy"><figcaption>{e(record["caption"])}</figcaption></figure>'
    if record.get('outcome') and record.get('outcome_verified'):
        out+='<section><h2>Outcome</h2><p>'+e(record['outcome'])+'</p></section>'
    out+='</div></article>'
    return out
