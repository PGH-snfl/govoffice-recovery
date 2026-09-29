"""Render additional report pages; selection is not a claim of exhaustive review."""
import json
from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
CHOICES = {'S06':[50,100,200,300,400,500], 'I36':[12,40,80,140,200,300],
           'I06':[20,60,100,150,250,350], 'I04':[50,100,150,200,250,300],
           'I18':[50,80,120,160,200,240], 'S02':[34,37,43,48,52,62],
           'S23':[12,20,28,36,44,50], 'S29':[20,40,80,100,120,140]}

def main():
    result = {}
    for rid, requested in CHOICES.items():
        doc = pdfium.PdfDocument(str(BASE/'pdfs'/(rid+'.pdf')))
        chosen = sorted({min(len(doc),p) for p in requested})
        result[rid] = chosen
        sheet = Image.new('RGB',(1560,1580),'#e5e7eb')
        draw = ImageDraw.Draw(sheet)
        font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',20)
        for i,n in enumerate(chosen):
            p = doc[n-1]
            bmp = p.render(scale=508/p.get_width())
            im = bmp.to_pil().convert('RGB')
            im.thumbnail((508,742))
            x,y=(i%3)*520+6,(i//3)*790+38
            sheet.paste(im,(x,y))
            draw.text((x,y-32),f'{rid} PDF p.{n}',font=font,fill='black')
            bmp.close()
            p.close()
        sheet.save(BASE/'review_sheets'/(rid+'-extra.jpg'),quality=90)
        doc.close()
    (BASE/'additional_selection.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(result)

if __name__ == '__main__':
    main()
