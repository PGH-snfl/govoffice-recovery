"""Extract page-aware text using PDFium; label machine matches, not visual review."""
import concurrent.futures
import json
import re
from pathlib import Path
import pypdfium2 as pdfium

BASE = Path(__file__).resolve().parent

def norm(text):
    return re.sub(r'[^0-9A-Za-z가-힣]', '', text).lower()

def one(row):
    file = BASE/'pdfs'/(row['id']+'.pdf')
    result = dict(row)
    result.pop('scripts', None)
    result['pdf_page_count'] = None
    if not file.exists():
        return result
    cached = BASE/'page_text'/(row['id']+'.json')
    if cached.exists():
        pages = json.loads(cached.read_text(encoding='utf-8'))
    else:
        pages = []
        doc = pdfium.PdfDocument(str(file))
        for i in range(len(doc)):
            page = doc[i]
            tp = page.get_textpage()
            content = tp.get_text_range()
            pages.append({'pdf_page':i+1, 'width':page.get_width(), 'height':page.get_height(), 'text':content})
            tp.close()
            page.close()
        doc.close()
        cached.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
    result['pdf_page_count'] = len(pages)
    normal = [norm(p['text']) for p in pages]
    for index, visual in enumerate(result['images']):
        visual['visual_id'] = f"{row['id']}-V{index+1:04}"
        filename = visual['url'].split('/')[-1]
        match = re.search(r'_(\d+)_(image|table)_', filename)
        hint = int(match[1]) if match else None
        visual['filename_page_hint'] = hint
        visual['source_kind'] = match[2] if match else None
        caption = norm(visual['caption'])
        matches = [i+1 for i,t in enumerate(normal) if caption and caption in t]
        visual['caption_matching_pdf_pages'] = matches
        visual['pdf_page'] = hint if hint in matches else (matches[0] if len(matches)==1 else None)
        visual['location_evidence'] = 'caption_text_match' if visual['pdf_page'] else 'filename_hint_only'
        visual['visual_review'] = 'not_yet_reviewed'
        # Keep enough page context to support analysis without pretending automated categories are facts.
        candidate = visual['pdf_page'] or hint
        if candidate and candidate <= len(pages):
            visual['page_context_path'] = f"page_text/{row['id']}.json"
            text = pages[candidate-1]['text']
            # Section candidates are deliberately not treated as validated report section names.
            visual['nearby_heading_candidates'] = [l.strip() for l in text.splitlines() if re.match(r'^\s*(?:제\s*\d+\s*[장절]|\d+[.)]|[가나다라마바사아자차카타파하][.)])\s*[^\d]', l)][:15]
    (BASE/'page_text'/(row['id']+'.txt')).write_text('\n\n'.join(f"===== PDF PAGE {p['pdf_page']} =====\n{p['text']}" for p in pages), encoding='utf-8')
    print(f"{row['id']} {len(pages)} pages {len(row['images'])} visuals", flush=True)
    return result

if __name__ == '__main__':
    (BASE/'page_text').mkdir(exist_ok=True)
    rows = json.loads((BASE/'visual_catalog.json').read_text(encoding='utf-8'))
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(one, rows))
    (BASE/'page_visual_index.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'pdfs':sum(bool(r['pdf_page_count']) for r in results), 'pages':sum(r['pdf_page_count'] or 0 for r in results),
                      'visuals':sum(len(r['images']) for r in results),
                      'caption_matches':sum(bool(v.get('pdf_page')) for r in results for v in r['images'])}))
