"""Build The Fractal Five v3 (Year 8, 2027): four student booklets + four answer files.

    python3 build.py            # build everything into ../out
"""
import html, json, os, re, subprocess, sys
from collections import OrderedDict, Counter

import pypdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, 'build')
OUT = os.path.join(ROOT, 'out')
sys.path.insert(0, HERE)
from schedule import build_year, UNLOCK, UNIT_NAME   # noqa: E402

VERSION = 'v3'
SEED = 2027
ROW_H = 132.2

INSTR = {1: 'Copy the formula or rule, then use it to answer.',
         2: 'Copy the formula or rule, then use it to answer.',
         3: 'Fill the gap in each formula or rule, then use it.',
         4: 'Recall each formula or rule, then use it.'}
FIRST_LABEL = {1: None, 2: None, 3: 'WRITE IT IN FULL', 4: 'FROM MEMORY'}
COVER_BADGE = {1: None, 2: None, 3: 'FILL THE GAP', 4: 'FORMULAS FROM MEMORY'}

OUTCOMES = OrderedDict([
    ('MA4-INT-C-01', 'compares, orders and calculates with integers to solve problems'),
    ('MA4-FRC-C-01', 'represents and operates with fractions, decimals and percentages to solve problems'),
    ('MA4-IND-C-01', 'operates with primes and roots, positive-integer and zero indices involving numerical bases and establishes the relevant index laws'),
    ('MA4-ALG-C-01', 'generalises number properties to operate with algebraic expressions including expansion and factorisation'),
    ('MA4-EQU-C-01', 'solves linear equations of up to 2 steps and quadratic equations of the form ax² = c'),
    ('MA4-LIN-C-01', 'creates and displays number patterns and finds graphical solutions to problems involving linear relationships'),
    ('MA4-LEN-C-01', 'applies knowledge of the perimeter of plane shapes and the circumference of circles to solve problems'),
    ('MA4-ARE-C-01', 'applies knowledge of area and composite area involving triangles, quadrilaterals and circles to solve problems'),
    ('MA4-VOL-C-01', 'applies knowledge of volume and capacity to solve problems involving right prisms and cylinders'),
    ('MA4-PYT-C-01', "applies Pythagoras' theorem to solve problems in various contexts"),
    ('MA4-ANG-C-01', 'applies angle relationships to solve problems, including those related to transversals on sets of parallel lines'),
    ('MA4-GEO-C-01', 'identifies and applies the properties of triangles and quadrilaterals to solve problems'),
    ('MA4-DAT-C-02', 'analyses simple datasets using measures of centre, range and shape of the data'),
    ('MA4-PRO-C-01', 'solves problems involving the probabilities of simple chance experiments'),
])
STRAND_NAME = OrderedDict([('N', 'Number'), ('A', 'Algebra and equations'), ('M', 'Measurement'),
                           ('G', 'Geometry: angles'), ('S', 'Statistics and probability')])

CALC_SVG = ('<svg class="calc" viewBox="0 0 11 13" xmlns="http://www.w3.org/2000/svg"><rect x="0.6" y="0.6" width="9.8" height="11.8" rx="1.6" '
            'fill="#fff" stroke="#3b7fc0" stroke-width="0.9"/><rect x="2.2" y="2.1" width="6.6" height="2.6" rx="0.5" fill="#cfe0f2" stroke="#3b7fc0" stroke-width="0.6"/>'
            + ''.join(f'<circle cx="{2.9 + 2.6 * c}" cy="{7 + 2.4 * r}" r="0.75" fill="#3b7fc0"/>' for r in range(2) for c in range(3)) + '</svg>')

PIPS = {1: [(0.5, 0.5)], 2: [(0.28, 0.72), (0.72, 0.28)], 3: [(0.26, 0.74), (0.5, 0.5), (0.74, 0.26)],
        4: [(0.28, 0.28), (0.72, 0.28), (0.28, 0.72), (0.72, 0.72)],
        5: [(0.28, 0.28), (0.72, 0.28), (0.5, 0.5), (0.28, 0.72), (0.72, 0.72)],
        6: [(0.28, 0.24), (0.72, 0.24), (0.28, 0.5), (0.72, 0.5), (0.28, 0.76), (0.72, 0.76)]}


def die_svg(n):
    dots = ''.join(f'<circle cx="{x*21:.1f}" cy="{y*21:.1f}" r="1.9" fill="#35322d"/>' for x, y in PIPS[n])
    return (f'<svg width="21pt" height="21pt" viewBox="0 0 21 21" xmlns="http://www.w3.org/2000/svg"><rect x="0.6" y="0.6" width="19.8" height="19.8" rx="3.5" '
            f'fill="#fff" stroke="#3b7fc0" stroke-width="1.1"/>{dots}</svg>')


def visible_len(s):
    return len(html.unescape(re.sub(r'<[^>]+>', '', s)))


# ---------------------------------------------------------------- page parts
def head(title_html, term, kicker='MATHEMATICS · YEAR 8 · THE FRACTAL FIVE', instr=True, namebox=True):
    h = ['<img class="logo" src="../assets/kingscliff-logo.jpg">',
         f'<div class="kicker">{kicker}</div>',
         f'<div class="title">{title_html}</div>',
         f'<div class="termpill">TERM {term}</div>']
    if instr:
        h.append(f'<div class="instr">{INSTR[term]}</div>')
    if namebox:
        h.append('<div class="namebox"><div class="lab" style="top:12.6pt">NAME</div><div class="ln" style="top:18.9pt"></div>'
                 '<div class="lab" style="top:34.7pt">DATE</div><div class="ln" style="top:41pt"></div></div>')
    h.append('<img class="band-top" src="../assets/band-top.jpg">')
    return ''.join(h)


def foot():
    return '<img class="band-bottom" src="../assets/band-bottom.jpg">'


def box_content(q, term):
    if q.get('nofade') or term in (1, 2):
        return q['box_text'], False
    if term == 3:
        return q['box_gap'], False
    kind = 'formula' if q['box'] == 'F' else 'rule'
    return f'Write the {kind}: <b>{q["box_name"]}</b>', True


def labels_for(q, term):
    if q.get('labels'):
        lab = list(q['labels'])
    else:
        lab = ['COPY', 'SUBSTITUTE', '', 'ANSWER'] if q['box'] == 'F' else ['RULE', 'WORKING', '', 'ANSWER']
    if not q.get('nofade') and FIRST_LABEL[term]:
        lab[0] = FIRST_LABEL[term]
    return lab


def body_html(q):
    b = q.get('body') or ''
    if '<div class="dice">' in b:
        b = '<div class="dice">' + ''.join(die_svg(i) for i in range(1, 7)) + '</div>'
    return b


def row_html(q, k, term, sid):
    top = 21 + k * ROW_H
    txt, recall = box_content(q, term)
    cls = 'ftxt' + (' recall' if recall else (' sm' if visible_len(txt) > 30 else ''))
    flab = 'FORMULA' if q['box'] == 'F' else 'METHOD'
    lab = labels_for(q, term)
    lines = []
    for j, (ly, ty) in enumerate(((52.3, 44.6), (76.3, 68.6), (100.3, 92.6), (124.2, 116.5))):
        lines.append(f'<div class="wl" style="top:{ly}pt"></div>')
        if lab[j]:
            c = 'wlab' + (' wa' if lab[j] == 'ANSWER' else (' exp' if lab[j] in ('EXPLAIN', 'REASON') else ''))
            lines.append(f'<div class="{c}" style="top:{ty}pt">{lab[j]}</div>')
    tags = ''
    if q.get('reasoning'):
        tags += f'<div class="tag">{"REASON" if "REASON" in lab else "EXPLAIN"}</div>'
    if q.get('calc'):
        tags += CALC_SVG
    body = body_html(q)
    body_div = f'<div class="qbody">{body}</div>' if body else ''
    pw = ' pw-tag' if q.get('reasoning') else (' pw-calc' if q.get('calc') else '')
    prompt = re.sub(r'(<i>[A-Za-z]</i>|\b[A-Za-z]) = (\u2212?\d)', r'\1&nbsp;=&nbsp;\2', q['prompt'])
    return (f'<div class="qrow{" first" if k == 0 else ""}" style="top:{top:.1f}pt" data-id="{sid} Q{k+1} {q["skill"]}">'
            f'<div class="qn">{k+1}</div><div class="qcell"><div class="prompt{pw}">{prompt}</div>{body_div}{tags}</div>'
            f'<div class="wcell"><div class="fbox"><div class="flab">{flab}</div><div class="{cls}">{txt}</div></div>{"".join(lines)}</div></div>')


def session_page(S):
    t, w, s = S['term'], S['week'], S['session']
    sid = f'T{t} W{w} S{s}'
    title = f'Week {w}<span class="dot">·</span><span class="ss">Session {s}</span>'
    rows = ''.join(row_html(q, k, t, sid) for k, q in enumerate(S['questions']))
    sheet = ('<div class="sheet"><div class="head"><div class="h" style="left:12.9pt">QUESTION</div>'
             '<div class="h" style="left:269pt">WORKING</div><div class="score"><span class="lab">SCORE</span><span class="box">/ 5</span></div></div>'
             f'<div class="vline"></div>{rows}</div>')
    return f'<div class="page">{head(title, t)}{sheet}{foot()}</div>'


FAMILY = {
    'fraction to decimal': 'Converting fractions, decimals and percentages',
    'decimal to percentage': 'Converting fractions, decimals and percentages',
    'percentage to fraction': 'Converting fractions, decimals and percentages',
    'decimal to fraction': 'Converting fractions, decimals and percentages',
    'percentage to decimal': 'Converting fractions, decimals and percentages',
    'fraction to percentage': 'Converting fractions, decimals and percentages',
    'adding integers': 'Integers', 'subtracting integers': 'Integers', 'subtracting a negative': 'Integers',
    'multiplying and dividing integers': 'Integers',
    'index notation': 'Powers and roots', 'square roots and cube roots': 'Powers and roots',
    'index law for multiplying': 'Index laws', 'index law for dividing': 'Index laws', 'power of a power': 'Index laws',
    'the zero index': 'Index laws',
    'percentage increase': 'Percentage increase and decrease', 'percentage decrease': 'Percentage increase and decrease',
    'discounts': 'Percentage increase and decrease', 'percentage change': 'Percentage increase and decrease',
    'GST': 'Profit, loss and GST', 'profit and loss as a percentage': 'Profit, loss and GST',
    'fraction of a quantity': 'Fractions and percentages of a quantity',
    'percentage of a quantity': 'Fractions and percentages of a quantity',
    'writing one amount as a percentage of another': 'Fractions and percentages of a quantity',
    'circumference of a circle (diameter)': 'Circumference of a circle', 'circumference of a circle (radius)': 'Circumference of a circle',
    'area of a rectangle': 'Area of rectangles and squares', 'area of a square': 'Area of rectangles and squares',
    'area of a rectangle and a square': 'Area of rectangles and squares',
    'perimeter of a rectangle': 'Perimeter', 'perimeter of a square': 'Perimeter', 'perimeter of a shape': 'Perimeter',
    'volume of a rectangular prism': 'Volume of prisms', 'volume of a prism': 'Volume of prisms',
    'volume and capacity units': 'Units of area, volume and capacity', 'area units': 'Units of area, volume and capacity',
    'the mean': 'Mean, median, mode and range', 'the median': 'Mean, median, mode and range',
    'the mode': 'Mean, median, mode and range', 'the range': 'Mean, median, mode and range',
    'complementary angles': 'Angles at a point and on a line', 'angles on a straight line (supplementary)': 'Angles at a point and on a line',
    'angles at a point': 'Angles at a point and on a line', 'vertically opposite angles': 'Angles at a point and on a line',
    'corresponding angles': 'Angles on parallel lines', 'alternate angles': 'Angles on parallel lines', 'co-interior angles': 'Angles on parallel lines',
    'angle sum of a triangle': 'Triangles and quadrilaterals', 'exterior angle of a triangle': 'Triangles and quadrilaterals',
    'isosceles triangle': 'Triangles and quadrilaterals', 'angle sum of a quadrilateral': 'Triangles and quadrilaterals',
    'simplifying like terms': 'Like terms', 'like terms': 'Like terms',
    'multiplying terms': 'Multiplying and dividing terms', 'dividing terms': 'Multiplying and dividing terms',
    'multiplying and dividing terms': 'Multiplying and dividing terms',
    'solving equations': 'Solving equations', 'checking a solution': 'Solving equations',
    "Pythagoras' theorem": "Pythagoras' theorem", "converse of Pythagoras' theorem": "Pythagoras' theorem",
    'estimating square roots': "Pythagoras' theorem",
    'probability of an event': 'Probability', 'complementary events': 'Probability', 'observed (experimental) probability': 'Probability',
    'tables of values': 'Linear relationships', 'points on a line': 'Linear relationships', 'coordinates': 'Linear relationships',
}


def _ref_item_h(texts):
    import math
    h = 13.5
    for t in texts:
        h += 11.2 * max(1, math.ceil(visible_len(t) * 4.55 / 232)) + 3.6
    return h + 5


def reference_page(term, sessions):
    fams = OrderedDict()
    for S in sessions:
        for q in S['questions']:
            if q.get('nofade'):
                continue
            fam = FAMILY.get(q['box_name'], q['box_name'][0].upper() + q['box_name'][1:])
            key = (q['strand'], fam)
            if key not in fams:
                fams[key] = [OrderedDict(), True]
            fams[key][0].setdefault(q['box_text'], q['box_name'])
            if q['unit'] == 'Y7':
                fams[key][1] = False
    groups = OrderedDict((k, []) for k in STRAND_NAME)
    for (st, fam), (texts, y8only) in fams.items():
        groups[st].append((fam, list(texts), y8only))
    # all entries go on page 1; layout.js moves entries to page 2 until page 1 fits
    parts = []
    for st, lst in groups.items():
        if not lst:
            continue
        parts.append(f'<div class="refgroup" data-g="{st}" data-name="{STRAND_NAME[st].upper()}">{STRAND_NAME[st].upper()}</div>')
        for fam, texts, y8 in sorted(lst, key=lambda x: (x[2], -len(x[1]), x[0])):
            tag = ' · Year 8' if y8 else ''
            tx = ''.join(f'<div class="tx">{t}</div>' for t in texts)
            parts.append(f'<div class="refitem" data-g="{st}"><div class="nm">{fam}{tag}</div>{tx}</div>')
    pages = []
    for pi in range(2):
        title = ('Formula<span class="dot" style="font-weight:500;color:#b9b3a8;margin:0 6pt">·</span>'
                 f'<span class="ss">Reference {pi + 1}</span>')
        sub = 'Every formula and rule used in this booklet.' if pi == 0 else 'Every formula and rule used in this booklet (continued).'
        content = ''.join(parts) if pi == 0 else ''
        pages.append(f'<div class="page">{head(title, term, instr=False, namebox=False)}'
                     f'<div class="instr" style="left:204.6pt">{sub}</div>'
                     f'<div class="panel"><div class="refgrid" data-flow="{pi + 1}">{content}</div></div>{foot()}</div>')
    return ''.join(pages), len(fams)


def tracker_page(term, sessions):
    rows = []
    for w in range(1, 11):
        rows.append(f'<tr><td class="wk">Week {w}</td><td>/ 5</td><td>/ 5</td><td>/ 5</td><td class="tot">/ 15</td></tr>')
    rows.append('<tr class="sum"><td class="wk" style="color:#3b7fc0">TERM TOTAL</td><td></td><td></td><td></td><td class="tot" style="color:#3b7fc0">/ 150</td></tr>')
    table = ('<table class="tracker"><tr><th style="text-align:left">WEEK</th><th>SESSION 1</th><th>SESSION 2</th><th>SESSION 3</th><th>WEEK TOTAL</th></tr>'
             + ''.join(rows) + '</table>')
    used = Counter(); srcs = {}
    for S in sessions:
        for q in S['questions']:
            used[q['outcome']] += 1
            srcs.setdefault(q['outcome'], set()).add('NCM 8' if q['unit'] != 'Y7' else 'NCM 7')
    orow = ''.join(f'<tr><td class="code">{c}</td><td>{d}</td><td class="src">{", ".join(sorted(srcs[c]))}</td></tr>'
                   for c, d in OUTCOMES.items() if c in used)
    orow += ('<tr><td class="code">MAO-WM-01</td><td>Working mathematically: the weekly reasoning questions (marked EXPLAIN or REASON) '
             'ask students to explain, check or justify.</td><td class="src"></td></tr>')
    units_live = [u for u in UNLOCK if UNLOCK[u][0] <= term]
    if units_live:
        unit_txt = '; '.join(f'{UNIT_NAME[u]} from T{UNLOCK[u][0]} Wk {UNLOCK[u][1]}' for u in units_live)
        note = (f'Year 8 units in these warm-ups (each starts once its teaching ends in the 2027 Year 8 mixed ability program): {unit_txt}. '
                'All other questions revise Year 7 (NCM 7 Ch 1–11). Ratios, rates and time (NCM 7 Ch 12) are held back until Year 8 teaches them.')
    else:
        note = ('All questions revise Year 7 (NCM 7 Ch 1–11). Year 8 units are added once their teaching ends. '
                'Ratios, rates and time (NCM 7 Ch 12) are held back until Year 8 teaches them.')
    outbox = (f'<div class="outbox"><h3>OUTCOMES IN THIS BOOKLET · NSW MATHEMATICS K–10 (2022), STAGE 4</h3><table>{orow}</table>'
              f'<div class="note">{note}</div></div>')
    title = 'My<span class="dot" style="font-weight:500;color:#b9b3a8;margin:0 6pt">·</span><span class="ss">Tracker</span>'
    return (f'<div class="page">{head(title, term, instr=False)}<div class="instr" style="left:204.6pt">Write your score after each session.</div>'
            f'<div class="panel">{table}{outbox}</div>{foot()}</div>')


def answers_pages(term, sessions):
    tables = []
    for w in range(1, 11):
        rows = []
        for S in [x for x in sessions if x['week'] == w]:
            cells = []
            for q in S['questions']:
                a = q['answer']
                extra = ''
                if q.get('answer_alt'):
                    extra += f'<span class="alt">Also accept {q["answer_alt"]}</span>'
                cells.append(f'<td>{a}{extra}</td>')
            rows.append(f'<tr><td>S{S["session"]}</td>{"".join(cells)}</tr>')
        tables.append(f'<table class="ans"><colgroup><col style="width:36pt">' + '<col>' * 5 + '</colgroup>'
                      f'<tr><th>WK {w}</th><th>Q1</th><th>Q2</th><th>Q3</th><th>Q4</th><th>Q5</th></tr>{"".join(rows)}</table>')
    title = 'Answers<span class="dot" style="font-weight:500;color:#b9b3a8;margin:0 6pt">·</span><span class="ss">Term ' + str(term) + '</span>'
    note = ('<div class="ans-note">Teacher copy. Answers were calculated in code and checked. Circumference and Pythagoras answers use the π and √ keys; '
            'where π ≈ 3.14 gives a different 1 d.p. answer it is listed as an alternative. Reasoning answers are model responses: '
            'accept any correct explanation.</div>')
    # all tables start on page 1; layout.js moves tables forward until every page fits
    pages = []
    for pi in range(4):
        content = (note + ''.join(tables)) if pi == 0 else ''
        pages.append(f'<div class="page ans-page">{head(title, term, kicker="MATHEMATICS · YEAR 8 · THE FRACTAL FIVE · TEACHER", instr=False, namebox=False)}'
                     f'<div class="ans-wrap" data-flow="{pi + 1}">{content}</div>{foot()}</div>')
    return ''.join(pages)


def doc(body, extra_css=''):
    return (f'<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><link rel="stylesheet" href="../src/style.css">'
            f'<style>{extra_css}</style></head><body>{body}<script src="../src/layout.js"></script></body></html>')


def cover_overlay(term):
    parts = ['<div class="abs" style="left:308.6pt;top:733.6pt;width:245pt;height:42.4pt;background:#fff"></div>',
             '<div class="abs" style="right:49.6pt;top:740.4pt;font:500 6.6pt/1 Poppins;letter-spacing:1.7pt;color:#1c1a33;white-space:nowrap">APOLLONIAN GASKET</div>',
             '<div class="abs" style="right:50.3pt;top:749.9pt;font:400 7.6pt/11.4pt \'Open Sans\';color:#1c1a33;text-align:right;white-space:nowrap">'
             'each circle fills a gap between three touching circles;<br>every curvature (1 ÷ radius) is an integer</div>']
    if COVER_BADGE[term]:
        parts += ['<div class="abs" style="left:41.6pt;top:319.2pt;width:118pt;height:17.4pt;background:#fff"></div>',
                  f'<div class="abs" style="left:42.5pt;top:320.2pt;height:15.2pt;padding:0 8.4pt 0 8.7pt;border:0.75pt solid #1b998b;border-radius:3pt;'
                  f'font:500 7.2pt/13.7pt Poppins;letter-spacing:1.55pt;color:#1b998b;white-space:nowrap">{COVER_BADGE[term]}</div>']
    return doc(f'<div class="page" style="background:transparent">{"".join(parts)}</div>',
               'html,body{background:transparent!important}')


def build():
    os.makedirs(BUILD, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    sessions = build_year(SEED)
    json.dump(sessions, open(os.path.join(BUILD, 'year.json'), 'w'), indent=1, ensure_ascii=False)
    jobs = []
    meta = {}
    for t in range(1, 5):
        ss = [S for S in sessions if S['term'] == t]
        pages = ''.join(session_page(S) for S in ss)
        ref, nref = reference_page(t, ss)
        pages += ref + tracker_page(t, ss)
        meta[t] = nref
        open(os.path.join(BUILD, f'T{t}_booklet.html'), 'w').write(doc(pages))
        open(os.path.join(BUILD, f'T{t}_answers.html'), 'w').write(doc(answers_pages(t, ss)))
        open(os.path.join(BUILD, f'T{t}_cover.html'), 'w').write(cover_overlay(t))
        jobs += [os.path.join(BUILD, f'T{t}_booklet.html'), os.path.join(BUILD, f'T{t}_booklet.pdf'), 'O',
                 os.path.join(BUILD, f'T{t}_answers.html'), os.path.join(BUILD, f'T{t}_answers.pdf'), 'O',
                 os.path.join(BUILD, f'T{t}_cover.html'), os.path.join(BUILD, f'T{t}_cover.pdf'), 'T']
    print('reference items per term:', meta)
    r = subprocess.run(['node', os.path.join(HERE, 'render.js')] + jobs, capture_output=True, text=True)
    print(r.stdout[-6000:]); print(r.stderr[-3000:])
    if r.returncode:
        raise SystemExit('render failed')
    for t in range(1, 5):
        assemble(t)


def assemble(t):
    cover = pypdf.PdfReader(os.path.join(ROOT, 'assets', f'v2_cover_T{t}.pdf')).pages[0]
    over = pypdf.PdfReader(os.path.join(BUILD, f'T{t}_cover.pdf')).pages[0]
    cover.merge_page(over)
    w = pypdf.PdfWriter()
    w.add_page(cover)
    for p in pypdf.PdfReader(os.path.join(BUILD, f'T{t}_booklet.pdf')).pages:
        w.add_page(p)
    w.add_metadata({'/Title': f'The Fractal Five — Year 8, Term {t} ({VERSION})',
                    '/Author': 'Kingscliff High School Mathematics Faculty',
                    '/Subject': 'Year 8 warm-ups (2027): 30 sessions, 150 questions. NSW Mathematics K–10 (2022) Stage 4.'})
    for p in w.pages:
        p.compress_content_streams(level=9)
    w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    fn = os.path.join(OUT, f'Yr8_The_Fractal_Five_Term_{t}_Warm-Ups_{VERSION}.pdf')
    with open(fn, 'wb') as fh:
        w.write(fh)
    a = pypdf.PdfWriter()
    for p in pypdf.PdfReader(os.path.join(BUILD, f'T{t}_answers.pdf')).pages:
        a.add_page(p)
    a.add_metadata({'/Title': f'The Fractal Five — Year 8, Term {t} answers ({VERSION})',
                    '/Author': 'Kingscliff High School Mathematics Faculty'})
    with open(os.path.join(OUT, f'Yr8_The_Fractal_Five_Term_{t}_Answers_{VERSION}.pdf'), 'wb') as fh:
        a.write(fh)
    print('wrote', fn, os.path.getsize(fn) // 1024, 'KB')


if __name__ == '__main__':
    build()
