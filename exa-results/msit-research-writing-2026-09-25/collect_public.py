"""Read only public sources listed in sources.json; retain local research evidence."""
import concurrent.futures
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request
from pypdf import PdfReader

BASE = Path(__file__).resolve().parent

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.skip += 1
        if tag in ('p','div','br','tr','li','h1','h2','h3','h4','dt','dd'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.skip: self.skip -= 1
        if tag in ('p','div','tr','li','td'): self.parts.append('\n')
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def fetch(row):
    out = BASE / 'evidence'
    out.mkdir(exist_ok=True)
    try:
        req = urllib.request.Request(row['url'], headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=40) as r: raw = r.read()
        if row['id'].startswith('P'):
            path = out / (row['id'] + '.pdf')
            path.write_bytes(raw)
            pdf = PdfReader(path)
            text = '\n\n'.join(f'--- PDF PAGE {i+1} ---\n'+(p.extract_text() or '') for i,p in enumerate(pdf.pages))
            pages = len(pdf.pages)
        else:
            parser = VisibleText()
            parser.feed(raw.decode('utf-8',errors='replace'))
            text = re.sub(r'\n[ \t]*\n+', '\n', ''.join(parser.parts))
            text = '\n'.join(x.strip() for x in text.splitlines() if x.strip())
            pages = None
        (out / (row['id']+'.txt')).write_text(text,encoding='utf-8')
        return {'id':row['id'],'ok':True,'chars':len(text),'pages':pages}
    except Exception as e:
        return {'id':row['id'],'ok':False,'error':str(e)}

if __name__ == '__main__':
    data = json.loads((BASE/'sources.json').read_text(encoding='utf-8'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch,data['cases']+data['pdfs']))
    (BASE/'retrieval_status.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    for r in results: print(json.dumps(r,ensure_ascii=False))
