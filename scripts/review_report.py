"""Audit report geometry and render contact sheets for visual review."""
from pathlib import Path
import subprocess
import pdfplumber
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'reports/Entrega_2_Vallenato_2027_APA.pdf'
DEST=ROOT/'tmp/pdf-review'
DEST.mkdir(parents=True,exist_ok=True)
with pdfplumber.open(PDF) as doc:
    assert all((p.width,p.height)==(612,792) for p in doc.pages)
    assert 'DEIVYS MORALES URIBE' in doc.pages[0].extract_text()
    outside=[i+1 for i,p in enumerate(doc.pages) if any(c['x0']<70 or c['x1']>542 for c in p.chars)]
    assert not outside,outside
    count=len(doc.pages)
    print('APA report:',count,'pages; Letter; no text outside horizontal margins.')
poppler=Path('/Users/esteban.villada/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm')
subprocess.run([str(poppler),'-scale-to','1600','-png',str(PDF),str(DEST/'page')],check=True)
files=sorted(DEST.glob('page-*.png'))[:count]
for start in range(0,count,6):
    sheet=Image.new('RGB',(1230,1100),'#ddd')
    draw=ImageDraw.Draw(sheet)
    for i,f in enumerate(files[start:start+6]):
        picture=Image.open(f).convert('RGB');picture.thumbnail((390,510))
        x,y=(i%3)*410+10,(i//3)*550+25
        sheet.paste(picture,(x,y));draw.text((x,y-20),str(start+i+1),fill='black')
    sheet.save(DEST/f'contact-{start//6+1}.png')
print(DEST)
