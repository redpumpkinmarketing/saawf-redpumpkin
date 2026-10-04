"""Local-only preview server. No form storage, email or payment processing."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit
import argparse

ROOT=Path(__file__).parent/'dist'
class PreviewHandler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
    def end_headers(self):
        self.send_header('X-Robots-Tag','noindex, nofollow')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','strict-origin-when-cross-origin')
        self.send_header('Cache-Control','no-store')
        super().end_headers()
    def do_GET(self):
        path=urlsplit(self.path).path
        resolved=(ROOT/path.lstrip('/')).resolve()
        if ROOT.resolve() not in (resolved,*resolved.parents):
            self.send_error(403); return
        if resolved.is_dir() and (resolved/'index.html').exists():
            self.path=path.rstrip('/')+'/index.html'
        super().do_GET()
    def do_POST(self): self.send_error(503,'Preview only: enquiry delivery is not configured.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765)
    args=parser.parse_args()
    print(f'Local preview: http://127.0.0.1:{args.port}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),PreviewHandler).serve_forever()
