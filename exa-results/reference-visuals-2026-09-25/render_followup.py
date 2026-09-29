"""Render uncertain-location and sparse-text pages for actual review."""
import json
import sys
import re
from pathlib import Path
from collections import defaultdict
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

BASE=Path(__file__).resolve().parent
OUT=BASE/'followup-2026-09-26'

def main():
    missing_mode='--missing' in sys.argv
    rows=json.loads((BASE/'page_visual_index.json').read_text(encoding='utf-8'))
    memory=json.loads((BASE.parent.parent/'docs/authoring_visual_reference_memory.json').read_text(encoding='utf-8'))
    viewed={r['id']:set(r['visually_reviewed_pdf_pages']) for r in memory['records']}
    queue=defaultdict(set)
    for r in rows:
        if missing_mode:
            if r['images']:
                continue
            pages=json.loads((OUT/'pages'/(r['id']+'.json')).read_text(encoding='utf-8'))
            chosen=set()
            for pattern in ['흐름|절차|구조|구성|프로세스','데이터|평가|성능|시험|비교','추진|일정|계획|연차|목표','화면|사진|결과|분석|개념']:
                matches=[p for p in pages if p['pdf_page'] not in viewed[r['id']]|chosen and any(re.search(pattern,c['text']) for c in p['caption_candidates']) and not any('부록' in h for h in p['heading_candidates'])]
                if matches:
                    chosen.add(matches[0]['pdf_page'])
            if not chosen:
                chosen=set(p['pdf_page'] for p in pages if p['pdf_page']>7 and p['image_regions'] and p['pdf_page'] not in viewed[r['id']])
                chosen=set(sorted(chosen)[:4])
            for p in chosen:
                queue[(r['id'],p)].add('public_list_missing_followup')
            continue
        for v in r['images']:
            if v['location_evidence']!='caption_text_match':
                queue[(r['id'],v['filename_page_hint'])].add('caption_location_unconfirmed')
        for p in json.loads((OUT/'pages'/(r['id']+'.json')).read_text(encoding='utf-8')):
            if p['needs_image_or_ocr_check']:
                queue[(r['id'],p['pdf_page'])].add('sparse_text')
    items=[{'id':rid,'pdf_page':p,'reason':sorted(reason),'previous_page_overview':p in viewed[rid]} for (rid,p),reason in sorted(queue.items())]
    for start in range(0,len(items),6):
        sheet=Image.new('RGB',(1560,1580),'#e5e7eb')
        draw=ImageDraw.Draw(sheet)
        font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',18)
        for i,item in enumerate(items[start:start+6]):
            doc=pdfium.PdfDocument(str(BASE/'pdfs'/(item['id']+'.pdf')))
            p=doc[item['pdf_page']-1]
            bitmap=p.render(scale=508/p.get_width())
            im=bitmap.to_pil().convert('RGB')
            im.thumbnail((508,742))
            x,y=(i%3)*520+6,(i//3)*790+38
            sheet.paste(im,(x,y))
            draw.text((x,y-32),f'{item["id"]} PDF p.{item["pdf_page"]}',font=font,fill='black')
            bitmap.close(); p.close(); doc.close()
            item['sheet']=f'sheets/{"missing" if missing_mode else "check"}-{start//6+1:03}.jpg'
        sheet.save(OUT/'sheets'/f'{"missing" if missing_mode else "check"}-{start//6+1:03}.jpg',quality=90)
    (OUT/('missing_review_queue.json' if missing_mode else 'review_queue.json')).write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(items)} pages, {(len(items)+5)//6} sheets; not yet viewed')

if __name__=='__main__': main()
