"""Collect public reference pages and their explicitly linked visual evidence."""
import concurrent.futures
import html
import json
import re
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = {}
        self.scripts = []
        self.text = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style'):
            self.skip += 1
        if tag == 'script' and a.get('src'):
            self.scripts.append(a['src'])
        if tag == 'img' and 'bitextimages' in a.get('src', ''):
            self.images[a['src']] = {'url': a['src'], 'caption': a.get('title', a.get('alt', ''))}
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
    def handle_data(self, data):
        if not self.skip and data.strip():
            self.text.append(data.strip())

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()

def one(row):
    target = BASE / 'pages' / (row['id'] + '.html')
    result = {k: row[k] for k in ('id', 'title', 'source', 'task_type')}
    try:
        if target.exists():
            data = target.read_bytes()
        else:
            data = fetch(row['source'])
            target.write_bytes(data)
        source = data.decode('utf-8', errors='replace')
        parser = Page()
        parser.feed(source)
        visible = '\n'.join(parser.text)
        (BASE / 'pages' / (row['id'] + '.txt')).write_text(visible, encoding='utf-8')
        count = re.search(r'표/그림\s*\(\s*(\d+)\s*\)', visible)
        result.update(status='page_fetched', listed_count=int(count[1]) if count else None,
                      images=list(parser.images.values()), scripts=parser.scripts,
                      verification='captions_and_public_image_links_only')
    except Exception as exc:
        result.update(status='fetch_failed', error=str(exc), images=[])
    return result

def main():
    (BASE / 'pages').mkdir(parents=True, exist_ok=True)
    rows = json.loads((ROOT / 'docs' / 'authoring_reference_memory.json').read_text(encoding='utf-8-sig'))['records']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(one, rows))
    (BASE / 'visual_catalog.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'references': len(results), 'fetched': sum(r['status']=='page_fetched' for r in results),
                      'linked_images':sum(len(r['images']) for r in results),
                      'listed_visuals':sum(r.get('listed_count') or 0 for r in results),
                      'failures':[r for r in results if r['status']=='fetch_failed']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
