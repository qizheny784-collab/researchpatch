"""Build the English submission brief from the maintained project text."""
from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader

root=Path(__file__).resolve().parents[1]
out=root/'output/pdf/ResearchPatch-Project-Brief-EN.pdf'
out.parent.mkdir(parents=True,exist_ok=True)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='RPTitle',fontName='Helvetica-Bold',fontSize=26,leading=30,textColor=colors.HexColor('#172d3b'),spaceAfter=16))
styles.add(ParagraphStyle(name='RPHeading',fontName='Helvetica-Bold',fontSize=12,leading=15,textColor=colors.HexColor('#17695a'),spaceBefore=12,spaceAfter=6,keepWithNext=True))
styles.add(ParagraphStyle(name='RPBody',fontName='Helvetica',fontSize=9.5,leading=13.5,spaceAfter=8,alignment=TA_LEFT))
story=[]
for block in (root/'docs/PROJECT-EN.md').read_text(encoding='utf-8').split('\n\n'):
    block=block.strip()
    if not block:continue
    block=block.replace('\u2014','-').replace('\u2013','-')
    style='RPTitle' if block.startswith('# ') else 'RPHeading' if block.startswith('## ') else 'RPBody'
    story.append(Paragraph(escape(block.lstrip('# ').replace('\n',' ')),styles[style]))
def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#dce5e8'));canvas.line(48,43,A4[0]-48,43)
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#54656e'))
    canvas.drawString(48,29,'ResearchPatch | SciencePal hackathon | 1 November 2026')
    canvas.drawRightString(A4[0]-48,29,str(doc.page))
SimpleDocTemplate(str(out),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=46,bottomMargin=57,title='ResearchPatch - Project Brief',author='ResearchPatch contributors').build(story,onFirstPage=footer,onLaterPages=footer)
reader=PdfReader(out)
assert 1<=len(reader.pages)<=5
assert all(len(p.extract_text())>50 for p in reader.pages)
print(f'{out}: {len(reader.pages)} pages')

