"""Measurement generators (Year 7: NCM 7 Ch 8). Perimeter/circumference MA4-LEN-C-01,
area MA4-ARE-C-01, volume and capacity MA4-VOL-C-01."""
import math
from svg import Fig, pol
from mathfmt import gap, sup, frac, v, num

UNITS = ['cm', 'm', 'cm', 'm', 'mm']


def Q(**kw):
    base = dict(year=7, unit='Y7', strand='M', calc=False, reasoning=False, body='', answer_alt='',
                labels=None, box='F')
    base.update(kw)
    return base


def _box(text, gtext, name):
    return dict(box_text=text, box_gap=gtext, box_name=name)


def sq(u):
    return f'{u}<sup>2</sup>'


def cu(u):
    return f'{u}<sup>3</sup>'


# ---------------------------------------------------------------- circumference
def m_circ(rng, reasoning=False):
    use_d = rng.random() < 0.5
    u = rng.choice(['cm', 'cm', 'm'])
    if use_d:
        d = rng.choice([4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 40, 50])
        exact = math.pi * d; approx = 3.14 * d
        f = Fig(); f.circle((0, 0), 30); f.line((-30, 0), (30, 0)); f.dot((0, 0), 1.6)
        f.label((0, 0), f'{d} {u}', deg=90, dist=8)
        box = _box('<i>C</i> = π<i>d</i>', f'<i>C</i> = {gap()} × <i>d</i>', 'circumference of a circle (diameter)')
        key = f'circ-d{d}{u}'
    else:
        r = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 20, 25])
        exact = 2 * math.pi * r; approx = 2 * 3.14 * r
        f = Fig(); f.circle((0, 0), 30); f.line((0, 0), (30, 0)); f.dot((0, 0), 1.6)
        f.label((15, 0), f'{r} {u}', deg=90, dist=8)
        box = _box('<i>C</i> = 2π<i>r</i>', f'<i>C</i> = 2 × {gap()} × <i>r</i>', 'circumference of a circle (radius)')
        key = f'circ-r{r}{u}'
    a1 = f'{exact:.1f}'; a2 = f'{approx:.1f}'
    alt = f'{a2} {u} if π ≈ 3.14 is used' if a1 != a2 else ''
    return Q(skill='m_circ', outcome='MA4-LEN-C-01', ncm='NCM 7 §8.03', calc=True,
             prompt='Find the circumference of this circle, correct to 1 decimal place.',
             body=f.svg(max_h=74), answer=f'{a1} {u}', answer_alt=alt, key=key, **box)


# ---------------------------------------------------------------- perimeter
def m_perim(rng, reasoning=False):
    kind = rng.choice(['rect', 'square', 'tri', 'L'])
    u = rng.choice(['cm', 'm'])
    f = Fig()
    if kind == 'rect':
        l = rng.randrange(6, 21); w = rng.randrange(3, l)
        f.poly([(0, 0), (l, 0), (l, w), (0, w)]); f.right_angle((0, 0), 0, 90, 5)
        f.dim((0, 0), (l, 0), f'{l} {u}', 'below'); f.dim((l, 0), (l, w), f'{w} {u}', 'right')
        ans = 2 * (l + w); key = f'per-rect-{l}-{w}{u}'
        box = _box('<i>P</i> = 2(<i>l</i> + <i>w</i>)', f'<i>P</i> = {gap()}(<i>l</i> + <i>w</i>)', 'perimeter of a rectangle')
        prompt = 'Find the perimeter of this rectangle.'
    elif kind == 'square':
        s = rng.randrange(4, 26)
        f.poly([(0, 0), (s, 0), (s, s), (0, s)]); f.right_angle((0, 0), 0, 90, 5)
        for p, q in (((0, 0), (s, 0)), ((s, 0), (s, s)), ((s, s), (0, s)), ((0, s), (0, 0))):
            f.tick(p, q)
        f.dim((0, 0), (s, 0), f'{s} {u}', 'below')
        ans = 4 * s; key = f'per-sq-{s}{u}'
        box = _box('<i>P</i> = 4<i>s</i>', f'<i>P</i> = {gap()} × <i>s</i>', 'perimeter of a square')
        prompt = 'Find the perimeter of this square.'
    elif kind == 'tri':
        while True:
            a, b, c = sorted(rng.sample(range(5, 22), 3))
            if a + b > c + 2:
                break
        # place base c, apex from a and b
        x = (c * c + a * a - b * b) / (2 * c); y = math.sqrt(max(a * a - x * x, 0))
        P0, P1, P2 = (0, 0), (c, 0), (x, y)
        f.poly([P0, P1, P2])
        f.dim(P0, P1, f'{c} {u}', 'below')
        f.label(((P0[0] + P2[0]) / 2, (P0[1] + P2[1]) / 2), f'{a} {u}', deg=150, dist=14)
        f.label(((P1[0] + P2[0]) / 2, (P1[1] + P2[1]) / 2), f'{b} {u}', deg=30, dist=14)
        ans = a + b + c; key = f'per-tri-{a}-{b}-{c}{u}'
        box = dict(box='M', box_text='Perimeter = the sum of all the side lengths',
                   box_gap=f'Perimeter = the {gap(26)} of all the side lengths', box_name='perimeter of a shape')
        prompt = 'Find the perimeter of this triangle.'
    else:
        while True:
            W = rng.randrange(8, 15); H = rng.randrange(6, 12)
            w2 = rng.randrange(3, W - 2); h1 = rng.randrange(2, H - 2)
            if 0.4 * W <= W - w2 <= 0.6 * W and 0.4 * H <= H - h1 <= 0.6 * H and 0.6 <= H / W <= 1.1:
                break
        pts = [(0, 0), (W, 0), (W, h1), (w2, h1), (w2, H), (0, H)]
        f.poly(pts)
        for i in range(6):
            f.right_angle(pts[i], *_corner_dirs(pts, i), s=4.5) if i in (0, 1, 4, 5) else None
        f.dim(pts[0], pts[1], f'{W} {u}', 'below'); f.dim(pts[1], pts[2], f'{h1} {u}', 'right')
        f.dim(pts[2], pts[3], f'{W - w2} {u}', 'above', at=0.22); f.dim(pts[3], pts[4], f'{H - h1} {u}', 'right', at=0.86)
        f.dim(pts[4], pts[5], f'{w2} {u}', 'above'); f.dim(pts[5], pts[0], f'{H} {u}', 'left')
        ans = 2 * (W + H); key = f'per-L-{W}-{H}-{w2}-{h1}{u}'
        box = dict(box='M', box_text='Perimeter = the sum of all the side lengths',
                   box_gap=f'Perimeter = the {gap(26)} of all the side lengths', box_name='perimeter of a shape')
        prompt = 'Find the perimeter of this shape.'
    if 'box' not in box:
        box['box'] = 'F'
    return Q(skill='m_perim', outcome='MA4-LEN-C-01', ncm='NCM 7 §8.02', prompt=prompt, body=f.svg(max_w=215, max_h=96),
             answer=f'{ans} {u}', key=key, **box)


def _corner_dirs(pts, i):
    import math as _m
    p = pts[i]; a = pts[(i + 1) % len(pts)]; b = pts[i - 1]
    d1 = _m.degrees(_m.atan2(a[1] - p[1], a[0] - p[0])) % 360
    d2 = _m.degrees(_m.atan2(b[1] - p[1], b[0] - p[0])) % 360
    if (d2 - d1) % 360 > 180:
        d1, d2 = d2, d1
    return d1, d2


# ---------------------------------------------------------------- areas
def m_rect(rng, reasoning=False):
    u = rng.choice(['cm', 'm', 'mm'])
    if rng.random() < 0.35:
        s = rng.randrange(3, 16)
        f = Fig(); f.poly([(0, 0), (s, 0), (s, s), (0, s)]); f.right_angle((0, 0), 0, 90, 5)
        for p, q in (((0, 0), (s, 0)), ((s, 0), (s, s)), ((s, s), (0, s)), ((0, s), (0, 0))):
            f.tick(p, q)
        f.dim((0, 0), (s, 0), f'{s} {u}', 'below')
        return Q(skill='m_rect', outcome='MA4-ARE-C-01', ncm='NCM 7 §8.05', prompt='Find the area of this square.',
                 body=f.svg(max_h=76), answer=f'{s*s} {sq(u)}', key=f'area-sq-{s}{u}',
                 **_box('<i>A</i> = <i>s</i><sup>2</sup>', f'<i>A</i> = <i>s</i><sup>{gap(10)}</sup>', 'area of a square'))
    l = rng.randrange(5, 21); w = rng.randrange(2, l)
    f = Fig(); f.poly([(0, 0), (l, 0), (l, w), (0, w)]); f.right_angle((0, 0), 0, 90, 5)
    f.dim((0, 0), (l, 0), f'{l} {u}', 'below'); f.dim((l, 0), (l, w), f'{w} {u}', 'right')
    return Q(skill='m_rect', outcome='MA4-ARE-C-01', ncm='NCM 7 §8.05', prompt='Find the area of this rectangle.',
             body=f.svg(max_h=76), answer=f'{l*w} {sq(u)}', key=f'area-rect-{l}-{w}{u}',
             **_box('<i>A</i> = <i>lw</i>', f'<i>A</i> = <i>l</i> × {gap()}', 'area of a rectangle'))


def m_tri(rng, reasoning=False):
    u = rng.choice(['cm', 'm'])
    while True:
        b = rng.randrange(6, 21); h = rng.randrange(3, 13)
        if (b * h) % 2 == 0 and h <= 0.75 * b:
            break
    p = b * rng.choice([0.25, 0.3, 0.35, 0.65, 0.7])
    f = Fig(); f.poly([(0, 0), (b, 0), (p, h)]); f.line((p, h), (p, 0), w=0.8, dash='2.5,2')
    f.right_angle((p, 0), 0, 90, 4.5)
    f.dim((0, 0), (b, 0), f'{b} {u}', 'below')
    if p > b / 2:
        f.label((p, h / 2), f'{h} {u}', deg=180, dist=5, anchor='end')
    else:
        f.label((p, h / 2), f'{h} {u}', deg=0, dist=5, anchor='start')
    return Q(skill='m_tri', outcome='MA4-ARE-C-01', ncm='NCM 7 §8.06', prompt='Find the area of this triangle.',
             body=f.svg(max_h=78), answer=f'{num(b*h//2)} {sq(u)}', key=f'area-tri-{b}-{h}{u}',
             **_box('<i>A</i> = ½<i>bh</i>', f'<i>A</i> = {gap()} × <i>b</i> × <i>h</i>', 'area of a triangle'))


def m_para(rng, reasoning=False):
    u = rng.choice(['cm', 'm'])
    while True:
        b = rng.randrange(5, 17); h = rng.randrange(3, 11)
        if h <= 0.8 * b:
            break
    s = round(b * rng.choice([0.25, 0.35, 0.45]), 1)
    f = Fig(); f.poly([(0, 0), (b, 0), (b + s, h), (s, h)])
    f.line((s, h), (s, 0), w=0.8, dash='2.5,2'); f.right_angle((s, 0), 0, 90, 4.5)
    f.dim((0, 0), (b, 0), f'{b} {u}', 'below')
    f.label((s, h / 2), f'{h} {u}', deg=0, dist=6, anchor='start')
    return Q(skill='m_para', outcome='MA4-ARE-C-01', ncm='NCM 7 §8.07', prompt='Find the area of this parallelogram.',
             body=f.svg(max_h=76), answer=f'{b*h} {sq(u)}', key=f'area-para-{b}-{h}{u}',
             **_box('<i>A</i> = <i>bh</i>', f'<i>A</i> = <i>b</i> × {gap()}', 'area of a parallelogram'))


def m_comp(rng, reasoning=False):
    u = rng.choice(['cm', 'm'])
    kind = rng.choice(['L', 'L', 'house', 'step'])
    f = Fig()
    if kind == 'house':
        while True:
            W = rng.randrange(6, 13); h1 = rng.randrange(3, 8); h2 = rng.randrange(2, 7)
            if (W * h2) % 2 == 0 and h1 <= W and h2 <= 0.7 * W and h1 + h2 <= 1.1 * W:
                break
        pts = [(0, 0), (W, 0), (W, h1), (W / 2, h1 + h2), (0, h1)]
        f.poly(pts); f.line((0, h1), (W, h1), w=0.6, dash='2,2', obstacle=False)
        f.line((W / 2, h1 + h2), (W / 2, h1), w=0.8, dash='2.5,2', obstacle=False); f.right_angle((W / 2, h1), 0, 90, 4)
        f.dim((0, 0), (W, 0), f'{W} {u}', 'below'); f.dim((W, 0), (W, h1), f'{h1} {u}', 'right')
        f.arrow_dim((W / 2, h1 + h2), (W, h1), f'{h2} {u}', off=10, size=9.8, side='right', at_x=W)
        ans = W * h1 + W * h2 // 2
        key = f'comp-house-{W}-{h1}-{h2}{u}'
    else:
        while True:
            W = rng.randrange(7, 15); H = rng.randrange(6, 13)
            w2 = rng.randrange(3, W - 2); h1 = rng.randrange(2, H - 2)
            if 0.4 * W <= W - w2 <= 0.6 * W and 0.4 * H <= H - h1 <= 0.6 * H and 0.6 <= H / W <= 1.1:
                break
        if kind == 'L':
            pts = [(0, 0), (W, 0), (W, h1), (w2, h1), (w2, H), (0, H)]
            f.poly(pts)
            f.dim(pts[0], pts[1], f'{W} {u}', 'below'); f.dim(pts[1], pts[2], f'{h1} {u}', 'right')
            f.dim(pts[2], pts[3], f'{W - w2} {u}', 'above', at=0.22); f.dim(pts[3], pts[4], f'{H - h1} {u}', 'right', at=0.86)
            f.dim(pts[4], pts[5], f'{w2} {u}', 'above'); f.dim(pts[5], pts[0], f'{H} {u}', 'left')
        else:   # mirrored step (notch at top-left)
            pts = [(0, 0), (W, 0), (W, H), (W - w2, H), (W - w2, h1), (0, h1)]
            f.poly(pts)
            f.dim(pts[0], pts[1], f'{W} {u}', 'below'); f.dim(pts[1], pts[2], f'{H} {u}', 'right')
            f.dim(pts[2], pts[3], f'{w2} {u}', 'above'); f.dim(pts[3], pts[4], f'{H - h1} {u}', 'left', at=0.14)
            f.dim(pts[4], pts[5], f'{W - w2} {u}', 'above', at=0.78); f.dim(pts[5], pts[0], f'{h1} {u}', 'left')
        ans = W * h1 + w2 * (H - h1)
        key = f'comp-{kind}-{W}-{H}-{w2}-{h1}{u}'
    return Q(skill='m_comp', outcome='MA4-ARE-C-01', ncm='NCM 7 §8.08', box='M', prompt='Find the area of this shape.',
             body=f.svg(max_w=215, max_h=96), answer=f'{num(ans)} {sq(u)}', key=key,
             box_text='Split the shape into rectangles (and triangles), then add their areas',
             box_gap=f'Split the shape into rectangles (and triangles), then {gap(24)} their areas',
             box_name='area of a composite shape')


# ---------------------------------------------------------------- volume
def prism_fig(l, w, h, labels):
    f = Fig()
    k = 0.55; ang = math.radians(35)
    dx, dy = w * k * math.cos(ang), w * k * math.sin(ang)
    F = [(0, 0), (l, 0), (l, h), (0, h)]
    B = [(x + dx, y + dy) for x, y in F]
    f.poly(F, fill='#eef3fa')
    f.poly([F[3], F[2], B[2], B[3]], fill='#e4ecf7')
    f.poly([F[1], B[1], B[2], F[2]], fill='#d7e3f3')
    f.line(F[0], B[0], w=0.6, dash='2,2'); f.line(B[0], B[1], w=0.6, dash='2,2'); f.line(B[0], B[3], w=0.6, dash='2,2')
    lt, wt, ht = labels
    f.dim(F[0], F[1], lt, 'below'); f.dim(F[3], F[0], ht, 'left')
    f.label(((F[1][0] + B[1][0]) / 2, (F[1][1] + B[1][1]) / 2), wt, deg=-35, dist=12)
    return f


def m_vol(rng, reasoning=False):
    u = rng.choice(['cm', 'm'])
    l = rng.randrange(3, 13); w = rng.randrange(2, 9); h = rng.randrange(2, 9)
    f = prism_fig(l, w, h, (f'{l} {u}', f'{w} {u}', f'{h} {u}'))
    return Q(skill='m_vol', outcome='MA4-VOL-C-01', ncm='NCM 7 §8.11', prompt='Find the volume of this rectangular prism.',
             body=f.svg(max_h=80), answer=f'{l*w*h} {cu(u)}', key=f'vol-{l}-{w}-{h}{u}',
             **_box('<i>V</i> = <i>lwh</i>', f'<i>V</i> = <i>l</i> × <i>w</i> × {gap()}', 'volume of a rectangular prism'))


def m_volA(rng, reasoning=False):
    u = rng.choice(['cm', 'm'])
    A = rng.choice([6, 8, 10, 12, 15, 18, 20, 24, 25, 30])
    h = rng.randrange(3, 11)
    f = Fig()
    b, t = 6.0, 5.0
    k = 0.7; ang = math.radians(25); L = 9.0
    dx, dy = L * k * math.cos(ang), L * k * math.sin(ang)
    T = [(0, 0), (b, 0), (b * 0.45, t)]
    Bk = [(x + dx, y + dy) for x, y in T]
    f.poly(T, fill='#d7e3f3')
    f.line(T[1], Bk[1]); f.line(T[2], Bk[2]); f.line(Bk[1], Bk[2])
    f.line(T[0], Bk[0], w=0.6, dash='2,2'); f.line(Bk[0], Bk[1], w=0.6, dash='2,2'); f.line(Bk[0], Bk[2], w=0.6, dash='2,2')
    f.label(((T[1][0] + Bk[1][0]) / 2, (T[1][1] + Bk[1][1]) / 2), f'{h} {u}', deg=-30, dist=12)
    return Q(skill='m_volA', outcome='MA4-VOL-C-01', ncm='NCM 7 §8.12',
             prompt=f'The shaded cross-section has an area of {A} {sq(u)}. Find the volume of this prism.',
             body=f.svg(max_h=74), answer=f'{A*h} {cu(u)}', key=f'volA-{A}-{h}{u}',
             **_box('<i>V</i> = <i>Ah</i>', f'<i>V</i> = <i>A</i> × {gap()}', 'volume of a prism'))


def m_cap(rng, reasoning=False):
    kind = rng.choice(['L-mL', 'mL-L', 'cm3-mL', 'cm3-L', 'm3-L', 'L-cm3'])
    if kind == 'L-mL':
        a = rng.choice([1.5, 2, 2.5, 3, 0.75, 1.2, 4, 0.5, 3.25]); ans = f'{num(int(round(a*1000)))} mL'; q = f'Convert {num(a)} L to millilitres.'
    elif kind == 'mL-L':
        a = rng.choice([500, 1500, 2500, 750, 3000, 250, 4500, 1250]); ans = f'{num(a/1000)} L'; q = f'Convert {num(a)} mL to litres.'
    elif kind == 'cm3-mL':
        a = rng.choice([250, 600, 750, 1200, 80, 330]); ans = f'{num(a)} mL'; q = f'Convert {num(a)} cm<sup>3</sup> to millilitres.'
    elif kind == 'cm3-L':
        a = rng.choice([2000, 3000, 5000, 1500, 4000]); ans = f'{num(a/1000)} L'; q = f'Convert {num(a)} cm<sup>3</sup> to litres.'
    elif kind == 'm3-L':
        a = rng.choice([2, 3, 4, 5, 1.5]); ans = f'{num(int(a*1000))} L'; q = f'A tank holds {num(a)} m<sup>3</sup> of water. How many litres is that?'
    else:
        a = rng.choice([2, 3, 1.5, 0.5, 4]); ans = f'{num(int(a*1000))} cm<sup>3</sup>'; q = f'Convert {num(a)} L to cubic centimetres.'
    return Q(skill='m_cap', outcome='MA4-VOL-C-01', ncm='NCM 7 §8.10, 8.13', prompt=q, answer=ans, key=f'cap-{kind}-{a}',
             **_box('1 cm<sup>3</sup> = 1 mL, 1 L = 1000 mL, 1 m<sup>3</sup> = 1000 L',
                    f'1 cm<sup>3</sup> = 1 mL, 1 L = {gap()} mL, 1 m<sup>3</sup> = 1000 L', 'volume and capacity units'))


def m_areaunit(rng, reasoning=False):
    kind = rng.choice(['cm2-mm2', 'm2-cm2', 'ha-m2', 'm2-ha', 'mm2-cm2'])
    if kind == 'cm2-mm2':
        a = rng.choice([3, 5, 8, 12, 2.5]); ans = f'{num(int(a*100))} mm<sup>2</sup>'; q = f'Convert {num(a)} cm<sup>2</sup> to mm<sup>2</sup>.'
    elif kind == 'mm2-cm2':
        a = rng.choice([400, 900, 1500, 250]); ans = f'{num(a/100)} cm<sup>2</sup>'; q = f'Convert {num(a)} mm<sup>2</sup> to cm<sup>2</sup>.'
    elif kind == 'm2-cm2':
        a = rng.choice([2, 3, 5, 1.5]); ans = f'{num(int(a*10000))} cm<sup>2</sup>'; q = f'Convert {num(a)} m<sup>2</sup> to cm<sup>2</sup>.'
    elif kind == 'ha-m2':
        a = rng.choice([2, 3, 4, 1.5, 6]); ans = f'{num(int(a*10000))} m<sup>2</sup>'; q = f'A farm paddock covers {num(a)} ha. Convert this to m<sup>2</sup>.'
    else:
        a = rng.choice([30000, 50000, 20000, 15000, 80000]); ans = f'{num(a/10000)} ha'; q = f'A sports field covers {num(a)} m<sup>2</sup>. Convert this to hectares.'
    return Q(skill='m_areaunit', outcome='MA4-ARE-C-01', ncm='NCM 7 §8.04', prompt=q, answer=ans, key=f'au-{kind}-{a}',
             **_box('1 cm<sup>2</sup> = 100 mm<sup>2</sup>, 1 m<sup>2</sup> = 10 000 cm<sup>2</sup>, 1 ha = 10 000 m<sup>2</sup>',
                    f'1 cm<sup>2</sup> = {gap()} mm<sup>2</sup>, 1 m<sup>2</sup> = 10 000 cm<sup>2</sup>, 1 ha = 10 000 m<sup>2</sup>',
                    'area units'))


MEAS_SKILLS = {
    'm_circ': m_circ, 'm_perim': m_perim, 'm_rect': m_rect, 'm_tri': m_tri, 'm_para': m_para,
    'm_comp': m_comp, 'm_vol': m_vol, 'm_volA': m_volA, 'm_cap': m_cap, 'm_areaunit': m_areaunit,
}


def m_compare(rng, reasoning=True):
    while True:
        l, w = rng.randrange(3, 13), rng.randrange(2, 9); s = rng.randrange(3, 10)
        if l * w != s * s and abs(l * w - s * s) <= 6 and l != w:
            break
    u = rng.choice(['cm', 'm'])
    big_ = 'rectangle' if l * w > s * s else 'square'
    return Q(skill='m_compare', outcome='MA4-ARE-C-01', ncm='NCM 7 §8.05', reasoning=True, labels=['COPY', 'WORKING', '', 'EXPLAIN'],
             prompt=f'Which has the larger area: a {l} {u} by {w} {u} rectangle or a square with sides of {s} {u}? Explain.',
             key=f'mcomp-{l}-{w}-{s}{u}', box_text='<i>A</i> = <i>lw</i> and <i>A</i> = <i>s</i><sup>2</sup>',
             box_gap=f'<i>A</i> = <i>lw</i> and <i>A</i> = <i>s</i><sup>{gap(10)}</sup>', box_name='area of a rectangle and a square',
             answer=f'The {big_}: rectangle {l*w} {sq(u)}, square {s*s} {sq(u)}.')


MEAS_REASON = {'m_compare': m_compare}
