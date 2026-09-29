"""Build page contact sheets and a separate unverified caption-candidate index."""
import concurrent.futures
import json
import re
from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
FONT = 'C:/Windows/Fonts/malgun.ttf'

def one(row):
    rid = row['id']
    pages = json.loads((BASE/'page_text'/(rid+'.json')).read_text(encoding='utf-8'))
    candidates = []
    for page in pages:
        for line in page['text'].splitlines():
            line = line.strip()
            if re.match(r'^[<〈\[【(]?(?:그림|표|Figure|Table)\s*[\dIVX]+', line, re.I):
                candidates.append({'pdf_page':page['pdf_page'], 'text':line, 'verification':'pdf_text_candidate_not_visual_review'})
    (BASE/'caption_candidates'/(rid+'.json')).write_text(json.dumps(candidates,ensure_ascii=False,indent=2),encoding='utf-8')
    items = [{'pdf_page':v.get('pdf_page') or v.get('filename_page_hint'), 'caption':v['caption']} for v in row['images']]
    if not items:
        items = [{'pdf_page':c['pdf_page'], 'caption':c['text']} for c in candidates if '...' not in c['text'] and '···' not in c['text']]
    # Select diverse evidence types for a report overview, NOT exhaustive visual inspection.
    selected = []
    patterns = [r'구성|개념|구조|모델|시스템|architecture',r'절차|흐름|방법|알고리즘|과정|설계',
                r'사진|시제품|구축|구현|실험 환경|화면|장치|제작',r'비교|성능|정확|측정|평가|결과',r'목표|추진|일정|역할|계획|달성|지표',r'.']
    for pattern in patterns:
        options = [v for v in items if v['pdf_page'] and v['pdf_page']<=len(pages) and v['pdf_page'] not in [s['pdf_page'] for s in selected] and re.search(pattern,v['caption'],re.I)]
        if options:
            selected.append(options[0] if pattern != r'.' else options[len(options)//2])
    if not selected:
        selected = [{'pdf_page':min(len(pages),p),'caption':'목록 없는 문서: 배치 탐색 표본'} for p in (7,10,15,20,25,30)]
        selected = list({v['pdf_page']:v for v in selected}.values())
    doc = pdfium.PdfDocument(str(BASE/'pdfs'/(rid+'.pdf')))
    cellw, cellh = 520, 790
    sheet = Image.new('RGB',(cellw*3,cellh*2),'#e5e7eb')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(FONT,16)
    for i,item in enumerate(selected[:6]):
        page = doc[item['pdf_page']-1]
        bmp = page.render(scale=(cellw-12)/page.get_width())
        im = bmp.to_pil().convert('RGB')
        im.thumbnail((cellw-12,cellh-48))
        x,y = (i%3)*cellw+6,(i//3)*cellh+38
        sheet.paste(im,(x,y))
        draw.text((x,y-32),f"{rid} PDF p.{item['pdf_page']} | {item['caption'][:24]}",font=font,fill='black')
        bmp.close()
        page.close()
    doc.close()
    sheet.save(BASE/'review_sheets'/(rid+'.jpg'),quality=88)
    return {'id':rid,'title':row['title'],'selected_pages':selected[:6], 'caption_candidate_count':len(candidates),'review_status':'not_yet_viewed'}

if __name__=='__main__':
    for folder in ('caption_candidates','review_sheets'):
        (BASE/folder).mkdir(exist_ok=True)
    rows = json.loads((BASE/'page_visual_index.json').read_text(encoding='utf-8'))
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(one,rows))
    (BASE/'review_selection.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'reports':len(results),'selected_pages':sum(len(r['selected_pages']) for r in results), 'caption_candidates':sum(r['caption_candidate_count'] for r in results)}))
