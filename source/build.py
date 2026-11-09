from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import CMYKColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import subprocess
out=Path(__file__).resolve().parents[1]/'exports'
pdfmetrics.registerFont(TTFont('Sans','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
ink=CMYKColor(.71,.53,.44,.59)
paper=CMYKColor(.02,.04,.10,0)
orange=CMYKColor(0,.67,.94,0)
olive=CMYKColor(.51,.30,.75,.43)
black=CMYKColor(0,0,0,1)
spec=[
 ('wizytowka-przod',90,50,'KĄT NOŚNY','BUDOWA I REMONT',['Konstrukcja • Wykończenia'],False),
 ('wizytowka-tyl',90,50,'Porozmawiajmy','ZAPYTANIA O WYCENĘ',['kontakt@kat-nosny.example','Zakres, termin, lokalizacja'],False),
 ('rollup',850,2000,'KĄT NOŚNY','BUDOWA I REMONT',['Od fundamentów','po wykończenie.','Konstrukcje','Remonty','Prace wykończeniowe','kat-nosny.example'],False),
 ('ulotka-a5',148,210,'KĄT NOŚNY','USŁUGI BUDOWLANE',['Fundamenty i konstrukcje','Remonty mieszkań','Prace wykończeniowe','Zapytaj o zakres i termin','kontakt@kat-nosny.example'],False),
 ('menu-zewnetrzne',297,210,'Pora Talerza','MENU SEZONOWE',['Kuchnia sezonowa','Obiady • Desery • Napoje'],True),
 ('menu-wewnetrzne',297,210,'Na stole','MENU SEZONOWE',['Zupa dyniowa  24 zł','Pierogi z grzybami  38 zł','Pieczone buraki  32 zł','Ciasto śliwkowe  22 zł','Kompot jabłkowy  12 zł'],True)]
out.mkdir(exist_ok=True)
for key,wm,hm,title,subtitle,items,menu in spec:
 w,h=wm*mm,hm*mm; x=y=9*mm
 pdf=out/f'{key}.pdf'
 c=Canvas(str(pdf),pagesize=(w+18*mm,h+18*mm))
 c.setTrimBox((x,y,x+w,y+h)); c.setBleedBox((x-3*mm,y-3*mm,x+w+3*mm,y+h+3*mm))
 c.setTitle(title)
 bg,fg,accent=(paper,olive,olive) if menu else (ink,paper,orange)
 c.setFillColor(bg); c.rect(x-3*mm,y-3*mm,w+6*mm,h+6*mm,fill=1,stroke=0)
 c.setStrokeColor(accent); c.setLineWidth(w*.008)
 for j in range(4):
  a=w*(.67+j*.08)
  c.line(x+a,y,x+min(w+3*mm,a+w*.20),y+h*.41)
 if menu:
  c.setStrokeColor(olive); c.setLineWidth(.6); c.line(x+w/2,y+8*mm,x+w/2,y+h-8*mm)
 def text(px,py,size,value,color,font='Sans'):
  c.setFillColor(color); c.setFont(font,size); c.drawString(x+w*px,y+h*py,value)
 text(.075,.87,w*.035,subtitle,accent,'Bold')
 text(.075,.68,w*(.10 if not menu else .072),title,fg,'Bold')
 for j,item in enumerate(items):
  text(.075 if not menu or j<3 else .55,.51-(j if not menu or j<3 else j-3)*.072,w*(.039 if not menu else .028),item,fg)
 text(.075,.085,w*.017,'Projekt koncepcyjny – marka fikcyjna',fg)
 c.setStrokeColor(black);c.setLineWidth(.35)
 for a,sgn in [(x,-1),(x+w,1)]:
  for b,v in [(y,-1),(y+h,1)]:
   c.line(a+sgn*4*mm,b,a+sgn*8*mm,b); c.line(a,b+v*4*mm,a,b+v*8*mm)
 c.showPage();c.save()
 subprocess.run(['pdftoppm','-png','-scale-to','1200','-singlefile',str(pdf),str(out/key)],check=True)
