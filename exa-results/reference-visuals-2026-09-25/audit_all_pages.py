"""All-page mechanical audit; never substitutes for visual/semantic verification."""
import concurrent.futures
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
import pypdfium2 as pdfium

BASE = Path(__file__).resolve().parent
OUT = BASE/'followup-2026-09-26'

def norm(s):
    return re.sub(r'[^a-z0-9가-힣]','',unicodedata.normalize('NFKC',s).lower())

CAPTION = re.compile(r'^\s*[<〈\[【(]?(?:그림|표|Figure|Table)\s*([\dIVX]+(?:[-.－–]\d+)*)\s*[>〉\]】).:\-]?\s*(.*)',re.I)
HEADING = re.compile(r'^(?:제\s*\d+\s*[장절]|\d+(?:[-.]\d+)*[.)]?\s+|[가나다라마바사아자차카타파하][.)]\s*|[□■▶]\s*)')
SECTION_WORDS = re.compile(r'개요|필요성|배경|동향|목표|추진|수행|연구|개발|방법|내용|성과|평가|결과|활용|효과|계획|실증|검증|부록|참고문헌')

def dump(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def one(row):
    rid=row['id']
    cached=OUT/'pages'/(rid+'.json')
    if cached.exists() and all(p.get('audit_version')==2 and not p.get('object_scan_error') for p in json.loads(cached.read_text(encoding='utf-8'))):
        pages=json.loads(cached.read_text(encoding='utf-8'))
    else:
        texts=json.loads((BASE/'page_text'/(rid+'.json')).read_text(encoding='utf-8'))
        doc=pdfium.PdfDocument(str(BASE/'pdfs'/(rid+'.pdf')))
        pages=[]
        last_heading=None
        for pi,raw in enumerate(texts):
            page=doc[pi]
            area=page.get_width()*page.get_height()
            counts=Counter()
            images=[]
            object_error=None
            try:
                for obj in page.get_objects(max_depth=8):
                    counts[str(obj.type)]+=1
                    if obj.type==3:
                        box=obj.get_bounds()
                        fraction=abs((box[2]-box[0])*(box[3]-box[1]))/area
                        if fraction>=0.008:
                            images.append({'bbox_pdf_points_bottom_origin':[round(v,2) for v in box],
                                           'page_area_fraction':round(fraction,4)})
            except Exception as e:
                object_error=type(e).__name__+': '+str(e)
            lines=[l.strip() for l in raw['text'].splitlines() if l.strip()]
            headings=[l for l in lines if len(l)<95 and HEADING.search(l) and SECTION_WORDS.search(l) and not CAPTION.search(l)]
            captions=[]
            for li,line in enumerate(lines):
                match=CAPTION.match(line)
                if match:
                    toc=bool(re.search(r'\.{3,}|·{3,}|…{2,}',line))
                    captions.append({'text':line,'line_index':li,'toc_like':toc,
                                     'before':'\n'.join(lines[max(0,li-4):li]),
                                     'after':'\n'.join(lines[li+1:li+5]),
                                     'verification':'text_candidate_may_be_caption_or_body_reference'})
                else:
                    # Several reports use unnumbered <captions> or [captions].
                    # Keep these as candidates, not a fabricated unique-figure count.
                    for bracket in re.findall(r'[<〈\[【]([^>〉\]】]{8,180})[>〉\]】]',line):
                        if len(re.findall(r'[가-힣]',bracket))>=3:
                            captions.append({'text':bracket,'line_index':li,'toc_like':False,
                                             'before':'\n'.join(lines[max(0,li-4):li]),
                                             'after':'\n'.join(lines[li+1:li+5]),
                                             'verification':'unnumbered_bracket_candidate_may_be_heading_or_caption'})
            section= headings[0] if headings else (last_heading['text'] if last_heading else None)
            prior=last_heading
            if headings:
                last_heading={'text':headings[-1],'pdf_page':pi+1}
            pages.append({'audit_version':2,'pdf_page':pi+1,'text_characters':len(raw['text']),
                          'heading_candidates':headings,'section_context_candidate':section,
                          'prior_heading_candidate':prior,'section_inference_verified':False,
                          'caption_candidates':captions,'pdf_object_counts':dict(counts),
                          'image_regions':images,'object_scan_error':object_error,
                          'needs_image_or_ocr_check':len(raw['text'].strip())<80,
                          'visual_content_confirmed_by_human':False})
            page.close()
        doc.close()
        dump(cached,pages)
    texts=json.loads((BASE/'page_text'/(rid+'.json')).read_text(encoding='utf-8'))
    contexts=[]
    for v in row['images']:
        hint=v.get('pdf_page') or v.get('filename_page_hint')
        if not hint or hint>len(pages):
            contexts.append({'visual_id':v['visual_id'],'error':'no_valid_page'})
            continue
        raw=texts[hint-1]['text']
        lines=[l.strip() for l in raw.splitlines() if l.strip()]
        ncap=norm(v['caption'])
        # Full captions can wrap. A prefix is a search lead, not a confirmed match.
        best=None
        for i,line in enumerate(lines):
            joined=norm(''.join(lines[i:i+4]))
            if ncap and ncap in joined:
                best=i; break
        prefix=False
        if best is None and len(ncap)>=12:
            for i,line in enumerate(lines):
                if ncap[:min(24,len(ncap))] in norm(''.join(lines[i:i+4])):
                    best=i; prefix=True; break
        p=pages[hint-1]
        contexts.append({'visual_id':v['visual_id'],'caption':v['caption'],'pdf_page_candidate':hint,
                         'location_evidence':v['location_evidence'],
                         'caption_line_index':best,'prefix_match_only':prefix,
                         'text_before': '\n'.join(lines[max(0,best-7):best]) if best is not None else '',
                         'caption_and_following_text':'\n'.join(lines[best:best+10]) if best is not None else '',
                         'section_context_candidate':p['section_context_candidate'],
                         'heading_candidates':p['heading_candidates'],
                         'image_regions':p['image_regions'],
                         'association_verified':False,
                         'evidence_scope':'whole_page_mechanical_scan_and_nearby_text_not_individual_visual_interpretation'})
    dump(OUT/'contexts'/(rid+'.json'),contexts)
    result={'id':rid,'title':row['title'],'pages':len(pages),
            'public_listed_visuals':len(row['images']),
            'pages_with_caption_candidates':sum(bool(p['caption_candidates']) for p in pages),
            'pages_with_large_image_objects':sum(bool(p['image_regions']) for p in pages),
            'large_image_objects':sum(len(p['image_regions']) for p in pages),
            'caption_candidates':sum(len(p['caption_candidates']) for p in pages),
            'sparse_text_pages':[p['pdf_page'] for p in pages if p['needs_image_or_ocr_check']],
            'object_scan_errors':sum(p['object_scan_error'] is not None for p in pages)}
    print(f'{rid}: {len(pages)} pages audited',flush=True)
    return result

if __name__=='__main__':
    for d in ['pages','contexts','sheets']:
        (OUT/d).mkdir(parents=True,exist_ok=True)
    rows=json.loads((BASE/'page_visual_index.json').read_text(encoding='utf-8'))
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(one,rows))
    dump(OUT/'all_page_audit.json',{'date':'2026-09-26','method':'PDF object and text scan of every page; not visual inspection',
                                 'records':results,'total_pages':sum(r['pages'] for r in results),
                                 'all_visual_elements_verified':False})
