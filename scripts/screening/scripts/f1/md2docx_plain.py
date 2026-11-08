"""Markdown -> docx, deliberately plain (Google-Docs-like defaults): Arial 12 body,
default heading styles in Arial/black, 'Table Grid' tables, built-in list styles.
Fenced code blocks are rendered as dark-background PNG images (Consolas) and inserted."""
import io, re, sys, os, textwrap
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image, ImageDraw, ImageFont

src, dst, imgdir = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(imgdir, exist_ok=True)
lines = io.open(src, encoding='utf-8').read().split('\n')

doc = Document()
for sec in doc.sections:
    sec.top_margin = sec.bottom_margin = Cm(2.54)
    sec.left_margin = sec.right_margin = Cm(2.54)

def set_font(style, name='Arial', size=None, bold=None, color=RGBColor(0, 0, 0)):
    style.font.name = name
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts')
    if rfonts is None:
        from docx.oxml import OxmlElement
        rfonts = OxmlElement('w:rFonts'); rpr.append(rfonts)
    for k in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rfonts.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}' + k.split(':')[1], name)
    if size: style.font.size = Pt(size)
    if bold is not None: style.font.bold = bold
    style.font.color.rgb = color

set_font(doc.styles['Normal'], size=12)
doc.styles['Normal'].paragraph_format.space_after = Pt(6)
set_font(doc.styles['Title'], size=26, bold=True)
set_font(doc.styles['Heading 1'], size=20, bold=True)
set_font(doc.styles['Heading 2'], size=16, bold=True)
set_font(doc.styles['Heading 3'], size=14, bold=True)
for st in ('List Bullet', 'List Number'):
    set_font(doc.styles[st], size=12)

INLINE = re.compile(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)')
def add_runs(par, text):
    for chunk in INLINE.split(text):
        if not chunk: continue
        if chunk.startswith('**'): par.add_run(chunk[2:-2]).bold = True
        elif chunk.startswith('*'): par.add_run(chunk[1:-1]).italic = True
        elif chunk.startswith('`'): par.add_run(chunk[1:-1])
        else: par.add_run(chunk)

img_counter = [0]
def code_image(code_lines):
    img_counter[0] += 1
    font = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 22)
    wrapped = []
    for ln in code_lines:
        wrapped += textwrap.wrap(ln, width=95, subsequent_indent='    ') or ['']
    pad, lh = 24, 30
    w = 95 * 12 + 2 * pad
    h = lh * len(wrapped) + 2 * pad
    im = Image.new('RGB', (w, h), (30, 30, 30))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(wrapped):
        d.text((pad, pad + i * lh), ln, font=font, fill=(230, 230, 230))
    path = os.path.join(imgdir, f'code{img_counter[0]}.png')
    im.save(path)
    return path

buf = []
def flush(style=None):
    global buf
    if not buf: return
    p = doc.add_paragraph(style=style)
    add_runs(p, ' '.join(x.strip() for x in buf))
    buf = []

table = []
def flush_table():
    global table
    if not table: return
    rows = [r for r in table if not re.match(r'^\|[\s\-:|]+\|$', r)]
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    ncol = max(len(r) for r in cells)
    t = doc.add_table(rows=len(cells), cols=ncol)
    t.style = 'Table Grid'
    for i, row in enumerate(cells):
        for j in range(ncol):
            c = row[j] if j < len(row) else ''
            cell = t.cell(i, j); cell.text = ''
            par = cell.paragraphs[0]
            add_runs(par, c)
            for r in par.runs:
                r.font.size = Pt(10)
                if i == 0: r.bold = True
    doc.add_paragraph()
    table = []

in_code, code = False, []
last_list_style = None
i = 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith('```'):
        if in_code:
            flush()
            doc.add_picture(code_image(code), width=Cm(16))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.LEFT
            in_code, code = False, []
        else:
            flush(); flush_table(); in_code = True
        i += 1; continue
    if in_code:
        code.append(ln); i += 1; continue
    if ln.startswith('|'):
        flush(); table.append(ln); i += 1; continue
    flush_table()
    m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$', ln)
    if m:
        flush(); doc.add_picture(os.path.join(os.path.dirname(os.path.abspath(src)), m.group(2)), width=Cm(16))
        if m.group(1):
            cap = doc.add_paragraph(); r = cap.add_run(m.group(1)); r.italic = True; r.font.size = Pt(10)
        i += 1; continue
    if ln.startswith('# '):
        flush(); doc.add_paragraph(ln[2:], style='Title')
    elif ln.startswith('## '):
        flush(); doc.add_heading(ln[3:], 1)
    elif ln.startswith('### '):
        flush(); doc.add_heading(ln[4:], 2)
    elif ln.startswith('#### '):
        flush(); doc.add_heading(ln[5:], 3)
    elif ln.strip() == '---':
        flush()
    elif ln.startswith('> '):
        flush(); buf = [ln[2:]]
        while i + 1 < len(lines) and lines[i + 1].startswith('> '):
            i += 1; buf.append(lines[i][2:])
        flush()
    elif re.match(r'^- ', ln) or re.match(r'^\d+\. ', ln):
        flush()
        style = 'List Bullet' if ln.startswith('- ') else 'List Number'
        text = re.sub(r'^(- |\d+\. )', '', ln)
        buf = [text]
        while i + 1 < len(lines) and lines[i + 1].startswith('  ') and lines[i + 1].strip():
            i += 1; buf.append(lines[i])
        flush(style)
    elif ln.strip() == '':
        flush()
    else:
        buf.append(ln)
    i += 1
flush(); flush_table()
doc.save(dst)
print('saved', dst, '| images:', img_counter[0])
