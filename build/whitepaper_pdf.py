# -*- coding: utf-8 -*-
"""Render the white paper PDF from content_whitepaper.WP (same source as the web page).

Usage: python3 whitepaper_pdf.py FONT_DIR
FONT_DIR holds TTF copies of the site fonts (InstrumentSerif.ttf, Manrope-Regular.ttf, Manrope-Bold.ttf, JetBrainsMono.ttf),
converted from assets/fonts/*.woff2 with fontTools (variable Manrope instanced at wght 400 / 700).
Glyphs missing from the site subsets (≥ ≤ Δ) fall back to DejaVu Sans.
"""
import os, sys, re
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether, NextPageTemplate, Image)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_whitepaper import WP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = sys.argv[1]
for n in ['InstrumentSerif', 'Manrope-Regular', 'Manrope-Bold', 'JetBrainsMono']:
    pdfmetrics.registerFont(TTFont(n, os.path.join(FD, n + '.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))

INK = colors.HexColor('#121416'); INK2 = colors.HexColor('#3a3e43'); MUTED = colors.HexColor('#6b7076')
RED = colors.HexColor('#c8231a'); LINE = colors.HexColor('#d8dbdd'); PAPER2 = colors.HexColor('#eef0f1'); BLUE = colors.HexColor('#125894')


def T(s):
    """escape text and route glyphs missing from the site font subsets to DejaVu"""
    s = escape(s)
    return re.sub(r'([≥≤Δ→])', r'<font name="DejaVu">\1</font>', s)


body = ParagraphStyle('b', fontName='Manrope-Regular', fontSize=9.6, leading=14.6, textColor=INK2, spaceAfter=7)
small = ParagraphStyle('s', parent=body, fontSize=8.2, leading=11.8, textColor=MUTED)
cell = ParagraphStyle('c', parent=body, fontSize=8.1, leading=11.2, spaceAfter=0)
cellb = ParagraphStyle('cb', parent=cell, fontName='Manrope-Bold', textColor=INK)
head = ParagraphStyle('th', parent=cell, fontName='JetBrainsMono', fontSize=7, leading=9.5, textColor=colors.white)
h2 = ParagraphStyle('h2', fontName='InstrumentSerif', fontSize=21, leading=24, textColor=INK, spaceBefore=4, spaceAfter=9)
num = ParagraphStyle('n', fontName='JetBrainsMono', fontSize=7.5, leading=10, textColor=RED, spaceBefore=14, spaceAfter=3)
eyebrow = ParagraphStyle('e', fontName='JetBrainsMono', fontSize=7.5, leading=10, textColor=RED, spaceAfter=6)
bullet = ParagraphStyle('bl', parent=body, leftIndent=12, bulletIndent=0, spaceAfter=4)
note = ParagraphStyle('nt', parent=small, borderPadding=0, spaceBefore=4, spaceAfter=8)

W, H = A4
M = 20 * mm


def logo(c, x, y, h):
    try:
        d = svg2rlg(os.path.join(ROOT, 'assets/img/logo-mark.svg'))
        s = h / d.height; d.width *= s; d.height *= s; d.scale(s, s)
        renderPDF.draw(d, c, x, y)
    except Exception:
        pass


def cover(c, doc):
    c.saveState()
    c.setFillColor(INK); c.rect(0, 0, W, H, fill=1, stroke=0)
    img = os.path.join(ROOT, 'assets/img/home/sample-kit.webp')
    try:
        from PIL import Image as PI
        tmp = os.path.join(FD, 'cover.jpg')
        PI.open(img).convert('RGB').save(tmp, quality=86)
        iw = W; ih = iw * 1024 / 1536
        c.drawImage(tmp, 0, 0, iw, ih, mask=None)
        c.setFillColor(colors.Color(0.07, 0.08, 0.09, alpha=0.35)); c.rect(0, 0, W, ih, fill=1, stroke=0)
    except Exception:
        pass
    logo(c, M, H - M - 9 * mm, 9 * mm)
    c.setFillColor(colors.white); c.setFont('Manrope-Bold', 11); c.drawString(M + 12 * mm, H - M - 6 * mm, 'POLYMER')
    c.setFillColor(colors.HexColor('#9ca1a7')); c.setFont('JetBrainsMono', 7.5); c.drawString(M + 12 * mm, H - M - 9.6 * mm, 'POWDER COATINGS')
    c.setFillColor(colors.HexColor('#f0584d')); c.setFont('JetBrainsMono', 8)
    c.drawString(M, H - 70 * mm, 'TECHNICAL WHITE PAPER  ·  ' + WP['edition'].upper().replace('·', ' · '))
    p = Paragraph(T(WP['title']), ParagraphStyle('ct', fontName='InstrumentSerif', fontSize=38, leading=40, textColor=colors.white))
    w, hh = p.wrap(W - 2 * M - 20 * mm, 200 * mm); p.drawOn(c, M, H - 76 * mm - hh)
    q = Paragraph(T(WP['subtitle']), ParagraphStyle('cs', fontName='Manrope-Regular', fontSize=11.5, leading=16.5, textColor=colors.HexColor('#d4d7da')))
    w2, h3 = q.wrap(W - 2 * M - 40 * mm, 100 * mm); q.drawOn(c, M, H - 84 * mm - hh - h3)
    c.setFillColor(colors.white); c.setFont('Manrope-Regular', 8.5)
    c.drawString(M, 14 * mm, 'Fujian Polymer Industry & Trade Co., Ltd.  ·  polymerpaints.com  ·  sales@polymerpaints.com')
    c.restoreState()


def page(c, doc):
    c.saveState()
    c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(M, H - 13 * mm, W - M, H - 13 * mm); c.line(M, 13 * mm, W - M, 13 * mm)
    c.setFont('JetBrainsMono', 6.8); c.setFillColor(MUTED)
    c.drawString(M, H - 10.5 * mm, 'POLYMER POWDER COATINGS  ·  ' + WP['short'].upper())
    c.drawRightString(W - M, H - 10.5 * mm, WP['edition'].upper())
    c.drawString(M, 8.5 * mm, 'polymerpaints.com' + '/white-paper/' + WP['slug'] + '/')
    c.drawRightString(W - M, 8.5 * mm, str(doc.page - 1))
    c.restoreState()


def table(rows, first_bold=True):
    n = len(rows[0]); avail = W - 2 * M
    widths = [avail * 0.22] + [avail * 0.78 / (n - 1)] * (n - 1) if n > 2 else [avail * 0.38, avail * 0.62]
    data = [[Paragraph(T(x).upper() if x else '', head) for x in rows[0]]]
    for r in rows[1:]:
        data.append([Paragraph(T(x), cellb if (j == 0 and first_bold) else cell) for j, x in enumerate(r)])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), INK), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('LINEBELOW', (0, 1), (-1, -1), 0.4, LINE), ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                           ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5)]))
    return t


def boxed(flow, bg=PAPER2):
    t = Table([[flow]], colWidths=[W - 2 * M])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), bg), ('LINEBEFORE', (0, 0), (0, -1), 2.2, RED),
                           ('LEFTPADDING', (0, 0), (-1, -1), 12), ('RIGHTPADDING', (0, 0), (-1, -1), 12), ('TOPPADDING', (0, 0), (-1, -1), 10), ('BOTTOMPADDING', (0, 0), (-1, -1), 10)]))
    return t


story = [NextPageTemplate('body'), PageBreak()]
# page 2: takeaways, audience, contents
story += [Paragraph('KEY TAKEAWAYS', eyebrow)]
story += [boxed([Paragraph(T(x), bullet, bulletText=f'{i + 1}.') for i, x in enumerate(WP['summary'])])]
story += [Spacer(1, 12), Paragraph('WRITTEN FOR', eyebrow), Paragraph(T(' · '.join(WP['audience'])), body), Spacer(1, 10), Paragraph('CONTENTS', eyebrow)]
for k, sec in enumerate(WP['sections']):
    story.append(Paragraph(f'<font name="JetBrainsMono" color="#c8231a">{k + 1:02d}</font>&nbsp;&nbsp;&nbsp;{T(sec["title"])}', ParagraphStyle('toc', parent=body, spaceAfter=3)))
story.append(Paragraph(f'<font name="JetBrainsMono" color="#c8231a">{len(WP["sections"]) + 1:02d}</font>&nbsp;&nbsp;&nbsp;About POLYMER', ParagraphStyle('toc2', parent=body, spaceAfter=3)))

for k, sec in enumerate(WP['sections']):
    blk = [Paragraph(f'{k + 1:02d}', num), Paragraph(T(sec['title']), h2)]
    paras = [Paragraph(T(x), body) for x in sec.get('paras', [])]
    story.append(KeepTogether(blk + paras[:1])); story += paras[1:]
    if sec.get('table'): story += [Spacer(1, 4), KeepTogether([table(sec['table'])]), Spacer(1, 6)]
    if sec.get('steps'):
        story += [KeepTogether([table([('Stage', 'What happens')] + [(f'{i + 1}. {a}', b) for i, (a, b) in enumerate(sec['steps'])])]), Spacer(1, 6)]
    if sec.get('bullets'): story += [Paragraph(T(x), bullet, bulletText='–') for x in sec['bullets']]
    if sec.get('note'): story += [boxed(Paragraph(T(sec['note']), ParagraphStyle('bn', parent=small, textColor=INK2)), PAPER2), Spacer(1, 4)]

story += [KeepTogether([Paragraph(f'{len(WP["sections"]) + 1:02d}', num), Paragraph('About POLYMER', h2), Paragraph(T(WP['about'][0]), body)])] + [Paragraph(T(x), body) for x in WP['about'][1:]]
story += [Spacer(1, 6), Paragraph('<b>Contact</b> &nbsp; sales@polymerpaints.com · +86 596 2600611 · WhatsApp +86 158 2472 9376 / +86 188 5021 3808 · No. 2 Zhuli Road, Xiangcheng District, Zhangzhou, Fujian 363005, China', body)]
story += [Spacer(1, 10), Paragraph(T(WP['disclaimer']), small),
          Paragraph(T(f'Cite as: POLYMER Powder Coatings, {WP["title"]}, {WP["edition"].split(" · ")[1]}. Online: https://polymerpaints.com/white-paper/{WP["slug"]}/'), small)]

out = os.path.join(ROOT, WP['pdf'].lstrip('/'))
os.makedirs(os.path.dirname(out), exist_ok=True)
doc = BaseDocTemplate(out, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=20 * mm, bottomMargin=20 * mm,
                      title=WP['title'], author='POLYMER Powder Coatings (Fujian Polymer Industry & Trade Co., Ltd.)',
                      subject=WP['subtitle'], keywords='powder coating specification, polyester, epoxy, hybrid, Qualicoat', creator='polymerpaints.com')
fr = Frame(M, 20 * mm, W - 2 * M, H - 40 * mm, id='f')
doc.addPageTemplates([PageTemplate('cover', [Frame(0, 0, W, H, id='c')], onPage=cover), PageTemplate('body', [fr], onPage=page)])
doc.build(story)
print(out, os.path.getsize(out))
