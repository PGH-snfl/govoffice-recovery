from pathlib import Path
import sys
import json
import pypdfium2 as pdfium
from pypdf import PdfReader
from PIL import Image, ImageDraw

path = Path(sys.argv[1])
doc = pdfium.PdfDocument(str(path))
for page_number in sys.argv[2:]:
    page_index = int(page_number)-1
    doc[page_index].render(scale=1.5).to_pil().save(path.parent/f'page_{page_index+1}.png')
reader = PdfReader(path)
summary=[]
for i,p in enumerate(reader.pages):
    text = p.extract_text() or ''
    summary.append({'page':i+1,'characters':len(text),'start':text[:150]})
    if i%20==0:
        sheet=Image.new('RGB',(1200,1740),'#dddddd')
    img=doc[i].render(scale=.48).to_pil().convert('RGB')
    img.thumbnail((290,400))
    x=(i%4)*300;y=((i%20)//4)*348
    img.thumbnail((290,322))
    sheet.paste(img,(x,y+22))
    ImageDraw.Draw(sheet).text((x+8,y+4),f'PAGE {i+1}',fill='black')
    if i%20==19 or i==len(doc)-1:
        sheet.save(path.parent/f'contact_{i//20+1}.png')
(path.parent/'pages.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
