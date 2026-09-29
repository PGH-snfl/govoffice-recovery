"""Follow the public original-view route observed on ScienceON report pages."""
import concurrent.futures
import html
import json
import re
import urllib.parse
from pathlib import Path
from collect_visuals import BASE, fetch

def one(row):
    result = {'id':row['id'], 'source':row['source']}
    try:
        cn = urllib.parse.parse_qs(urllib.parse.urlsplit(row['source']).query)['cn'][0]
        viewer_url = 'https://scienceon.kisti.re.kr/commons/util/originalView.do?' + urllib.parse.urlencode({'cn':cn,'dbt':'TRKO','rn':''})
        target = BASE/'viewers'/(row['id']+'.html')
        if not target.exists():
            target.write_bytes(fetch(viewer_url))
        source = target.read_text(encoding='utf-8', errors='replace')
        match = re.search(r"var docurl\s*=\s*'([^']+)'", source)
        result['viewer_url'] = viewer_url
        if not match:
            result['status'] = 'no_public_pdf_link'
            return result
        url = urllib.parse.urljoin(viewer_url, html.unescape(match[1]).split('#')[0])
        url = urllib.parse.quote(url, safe=':/?=&%')
        result['pdf_url'] = url
        pdf = BASE/'pdfs'/(row['id']+'.pdf')
        if not pdf.exists():
            data = fetch(url)
            if not data.startswith(b'%PDF'):
                result.update(status='non_pdf_response', response_start=data[:150].decode('utf-8', errors='replace'))
                return result
            pdf.write_bytes(data)
        result.update(status='pdf_downloaded', bytes=pdf.stat().st_size)
    except Exception as exc:
        result.update(status='failed', error=str(exc))
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return result

if __name__ == '__main__':
    for sub in ('viewers','pdfs'):
        (BASE/sub).mkdir(exist_ok=True)
    rows = json.loads((BASE/'visual_catalog.json').read_text(encoding='utf-8'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(one, rows))
    (BASE/'pdf_manifest.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
