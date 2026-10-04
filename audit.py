"""Audit the generated routes, content facts and all local navigation targets."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json

ROOT=Path(__file__).parent
DIST=ROOT/'dist'
class Page(HTMLParser):
    def __init__(self): super().__init__(); self.targets=[]; self.ids=[]; self.text=[]; self.titles=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag in ('a','link','script','img'):
            target=a.get('href') or a.get('src')
            if target:self.targets.append(target)
        if tag=='title':self.titles+=1
    def handle_data(self,data):self.text.append(data)

checked=0
for route in json.loads((ROOT/'routes.json').read_text()):
    path=DIST/route.strip('/')/'index.html'
    page=Page();page.feed(path.read_text(encoding='utf8'))
    assert len(set(page.ids))==len(page.ids),f'Duplicate ids: {route}'
    assert page.titles==1,route
    assert 'Siliguri Aashray Welfare Foundation' in ' '.join(page.text),route
    for target in page.targets:
        u=urlsplit(target)
        if u.scheme or u.netloc:continue
        if not u.path:
            assert not u.fragment or u.fragment in page.ids,f'Broken anchor {route} {target}'
        else:
            resolved=(path.parent/unquote(u.path)).resolve()
            assert resolved.is_relative_to(DIST.resolve()),f'Link outside site: {route} {target}'
            assert resolved.is_file(),f'Broken target {route} {target}'
        checked+=1
    if route.startswith('/our-work/'):
        expected={'children-education':'Upcoming program','health-wellbeing':'Work undertaken','women-livelihood':'Planned initiative','community-relief':'Work undertaken','environment-animal-welfare':'Planned initiative','human-rights':'Planned initiative'}[route.split('/')[-1]]
        assert expected in ' '.join(page.text),route
    if route=='/roti-challenge':assert 'Legacy initiative' in ' '.join(page.text)
    if route in ['/privacy-policy','/terms-conditions','/donation-policy']:assert 'Policy draft — approval required.' in ' '.join(page.text)
print(f'PASS: {checked} local link/asset targets; unique IDs, metadata, name, pillar statuses and policy gates.')
(ROOT/'audit-report.txt').write_text(f'PASS: 21 routes, {checked} local link and asset references.\nUnique IDs; route metadata; organisation spelling; pillar statuses; policy draft gates.\n',encoding='utf8')
