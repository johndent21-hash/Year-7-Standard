"""Geometry question generators (angles, triangles, quadrilaterals). Year 7 content.

NCM 7 Ch 2 (angles) -> MA4-ANG-C-01; NCM 7 Ch 6 (triangles, quadrilaterals) -> MA4-GEO-C-01.
Every diagram is drawn exactly to the angles in the question.
"""
import math
from svg import Fig, angle_mark, X_LABEL, pol, unit
from mathfmt import gap

FIND_X = 'Find the value of <i>x</i>.'
FIND_X_R = 'Find the value of <i>x</i>. Give a reason.'


def Q(**kw):
    base = dict(year=7, unit='Y7', strand='G', calc=False, reasoning=False, body='', answer_alt='',
                labels=None, box='F')
    base.update(kw)
    return base


def deg(v):
    return f'{v}°'


def _finish(q, reasoning, reason_text):
    if reasoning:
        q['prompt'] = FIND_X_R
        q['reasoning'] = True
        q['answer'] = f"{q['answer']} ({reason_text})"
        q['labels'] = ['COPY', 'SUBSTITUTE', 'REASON', 'ANSWER']
    return q


def _box(text, gtext, name):
    return dict(box_text=text, box_gap=gtext, box_name=name)


# ---------------------------------------------------------------- complementary
def g_comp(rng, reasoning=False):
    a = rng.choice([x for x in range(22, 69) if x not in (45,)])
    xv = 90 - a
    layout = rng.choice(['BL', 'BR', 'ROT'])
    d1, d2 = {'BL': (0, 90), 'BR': (90, 180), 'ROT': (rng.choice([15, 20, 25]), None)}[layout]
    if d2 is None:
        d2 = d1 + 90
    x_first = rng.random() < 0.5
    p1 = xv if x_first else a
    split = d1 + p1
    f = Fig(); V = (0, 0)
    for d in (d1, d2, split):
        f.line(V, pol(V, 62, d))
    f.dot(V)
    f.right_angle(V, d1, d2, s=6)
    if x_first:
        angle_mark(f, V, d1, split, X_LABEL, is_x=True, r_min=14)
        angle_mark(f, V, split, d2, deg(a), r_min=14)
    else:
        angle_mark(f, V, d1, split, deg(a), r_min=14)
        angle_mark(f, V, split, d2, X_LABEL, is_x=True, r_min=14)
    q = Q(skill='g_comp', outcome='MA4-ANG-C-01', ncm='NCM 7 §2.04', prompt=FIND_X, body=f.svg(),
          answer=f'<i>x</i> = {xv}', key=f'comp-{a}-{layout}-{x_first}',
          **_box('Complementary angles add to 90°', f'Complementary angles add to {gap()}°',
                 'complementary angles'))
    return _finish(q, reasoning, 'complementary angles add to 90°')


# ---------------------------------------------------------------- supplementary
def g_supp(rng, reasoning=False):
    th = rng.choice([x for x in range(28, 153) if abs(x - 90) > 8])
    down = rng.random() < 0.25
    x_left = rng.random() < 0.5
    left, right = 180 - th, th
    f = Fig(); V = (0, 0)
    f.line((-70, 0), (70, 0))
    if not down:
        f.line(V, pol(V, 62, th))
        r_seg = (0, th); l_seg = (th, 180)
    else:
        f.line(V, pol(V, 62, -th))
        r_seg = (-th, 0); l_seg = (180, 360 - th)
    f.dot(V)
    given = right if x_left else left
    xv = left if x_left else right
    if x_left:
        angle_mark(f, V, *l_seg, X_LABEL, is_x=True)
        angle_mark(f, V, *r_seg, deg(given))
    else:
        angle_mark(f, V, *l_seg, deg(given))
        angle_mark(f, V, *r_seg, X_LABEL, is_x=True)
    q = Q(skill='g_supp', outcome='MA4-ANG-C-01', ncm='NCM 7 §2.04', prompt=FIND_X, body=f.svg(max_h=80),
          answer=f'<i>x</i> = {xv}', key=f'supp-{th}-{down}-{x_left}',
          **_box('Angles on a straight line add to 180°', f'Angles on a straight line add to {gap()}°',
                 'angles on a straight line (supplementary)'))
    return _finish(q, reasoning, 'angles on a straight line add to 180°')


# ---------------------------------------------------------------- vertically opposite
def g_vopp(rng, reasoning=False):
    a = rng.choice([x for x in range(30, 151) if abs(x - 90) > 10])
    r0 = rng.choice([-25, -20, -15, -10, 10, 15, 20])
    t1, t2 = r0, r0 + a                      # angle a between rays t1..t2
    f = Fig(); V = (0, 0)
    f.line(pol(V, 66, t1), pol(V, 66, t1 + 180))
    f.line(pol(V, 66, t2), pol(V, 66, t2 + 180))
    f.dot(V)
    side = rng.choice([0, 1])
    if side == 0:   # use the a-angle and its opposite
        angle_mark(f, V, t1, t2, deg(a))
        angle_mark(f, V, t1 + 180, t2 + 180, X_LABEL, is_x=True)
    else:           # the supplementary pair: b = 180 - a
        b = 180 - a
        angle_mark(f, V, t2, t1 + 180, deg(b))
        angle_mark(f, V, t2 + 180, t1 + 360, X_LABEL, is_x=True)
    xv = a if side == 0 else 180 - a
    q = Q(skill='g_vopp', outcome='MA4-ANG-C-01', ncm='NCM 7 §2.05', prompt=FIND_X, body=f.svg(max_h=82),
          answer=f'<i>x</i> = {xv}', key=f'vopp-{a}-{r0}-{side}',
          **_box('Vertically opposite angles are equal', f'Vertically opposite angles are {gap(34)}',
                 'vertically opposite angles'))
    return _finish(q, reasoning, 'vertically opposite angles are equal')


# ---------------------------------------------------------------- angles at a point
def g_point(rng, reasoning=False):
    while True:
        n = rng.choice([3, 3, 4])
        if n == 3:
            A = [rng.randrange(60, 161, 5) for _ in range(2)]
            A.append(360 - sum(A))
            if min(A) < 60 or max(A) > 160:
                continue
        else:
            A = [rng.randrange(50, 131, 1) for _ in range(3)]
            A.append(360 - sum(A))
            if min(A) < 50 or max(A) > 150:
                continue
            # no two rays may look like a straight line
            if abs(A[0] + A[1] - 180) < 20 or abs(A[1] + A[2] - 180) < 20:
                continue
        if any(t == 90 for t in A):
            continue
        break
    xi = rng.randrange(n)
    d0 = rng.choice([-30, -20, -10, 0, 10, 15, 20, 25])
    dirs = [d0]
    for t in A[:-1]:
        dirs.append(dirs[-1] + t)
    f = Fig(); V = (0, 0)
    for d in dirs:
        f.line(V, pol(V, 58, d))
    f.dot(V)
    for i in range(n):
        s, e = dirs[i], dirs[i] + A[i]
        gapdeg = 3
        if i == xi:
            angle_mark(f, V, s + gapdeg, e - gapdeg, X_LABEL, is_x=True, r_min=12)
        else:
            angle_mark(f, V, s + gapdeg, e - gapdeg, deg(A[i]), r_min=12)
    xv = A[xi]
    q = Q(skill='g_point', outcome='MA4-ANG-C-01', ncm='NCM 7 §2.05', prompt=FIND_X, body=f.svg(max_h=84),
          answer=f'<i>x</i> = {xv}', key=f'point-{"-".join(map(str, A))}-{xi}',
          **_box('Angles at a point add to 360°', f'Angles at a point add to {gap()}°', 'angles at a point'))
    return _finish(q, reasoning, 'angles at a point add to 360°')


# ---------------------------------------------------------------- parallel lines
QUADS = {'AR': (0, 'phi'), 'AL': ('phi', 180), 'BL': (180, 'phi+180'), 'BR': ('phi+180', 360)}


def _quad_dirs(q, phi):
    s, e = QUADS[q]
    ev = lambda t: phi if t == 'phi' else (phi + 180 if t == 'phi+180' else t)
    return ev(s), ev(e)


def _quad_measure(q, phi):
    return phi if q in ('AR', 'BL') else 180 - phi


def _parallel(rng, kind):
    phi = rng.choice([x for x in range(48, 133) if abs(x - 90) > 12])
    if kind == 'corr':
        qu = rng.choice(['AR', 'AL', 'BL', 'BR'])
        pair = (qu, qu)
    elif kind == 'alt':
        pair = rng.choice([('BR', 'AL'), ('BL', 'AR')])
    else:  # co-interior
        pair = rng.choice([('BR', 'AR'), ('BL', 'AL')])
    x_on_upper = rng.random() < 0.5
    H = 40
    xL = rng.choice([-12, -6, 0, 6, 12])
    xU = xL + H / math.tan(math.radians(phi))
    IU, IL = (xU, H), (xL, 0)
    u = unit(phi)
    f = Fig()
    f.line((-72, H), (72, H)); f.line((-72, 0), (72, 0))
    f.line((IL[0] - 26 * u[0], IL[1] - 26 * u[1]), (IU[0] + 26 * u[0], IU[1] + 26 * u[1]))
    f.arrows((-55, H), 0); f.arrows((-55, 0), 0)
    qU, qL = pair
    mU, mL = _quad_measure(qU, phi), _quad_measure(qL, phi)
    given_on_upper = not x_on_upper
    for (I, qq, m, is_x) in ((IU, qU, mU, x_on_upper), (IL, qL, mL, not x_on_upper)):
        d1, d2 = _quad_dirs(qq, phi)
        angle_mark(f, I, d1, d2, X_LABEL if is_x else deg(m), is_x=is_x, r_min=10)
    given = mL if x_on_upper else mU
    xv = mU if x_on_upper else mL
    return f, given, xv, f'{kind}-{phi}-{qU}{qL}-{x_on_upper}-{xL}'


def g_corr(rng, reasoning=False):
    f, given, xv, key = _parallel(rng, 'corr')
    q = Q(skill='g_corr', outcome='MA4-ANG-C-01', ncm='NCM 7 §2.07', prompt=FIND_X, body=f.svg(max_h=84),
          answer=f'<i>x</i> = {xv}', key=key,
          **_box('Corresponding angles on parallel lines are equal',
                 f'Corresponding angles on parallel lines are {gap(30)}', 'corresponding angles'))
    return _finish(q, reasoning, 'corresponding angles on parallel lines are equal')


def g_alt(rng, reasoning=False):
    f, given, xv, key = _parallel(rng, 'alt')
    q = Q(skill='g_alt', outcome='MA4-ANG-C-01', ncm='NCM 7 §2.08', prompt=FIND_X, body=f.svg(max_h=84),
          answer=f'<i>x</i> = {xv}', key=key,
          **_box('Alternate angles on parallel lines are equal',
                 f'Alternate angles on parallel lines are {gap(30)}', 'alternate angles'))
    return _finish(q, reasoning, 'alternate angles on parallel lines are equal')


def g_coint(rng, reasoning=False):
    f, given, xv, key = _parallel(rng, 'coint')
    q = Q(skill='g_coint', outcome='MA4-ANG-C-01', ncm='NCM 7 §2.09', prompt=FIND_X, body=f.svg(max_h=84),
          answer=f'<i>x</i> = {xv}', key=key,
          **_box('Co-interior angles on parallel lines add to 180°',
                 f'Co-interior angles on parallel lines add to {gap()}°', 'co-interior angles'))
    return _finish(q, reasoning, 'co-interior angles on parallel lines add to 180°')


# ---------------------------------------------------------------- triangles
def _dir(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) % 360


def interior(v, p, q):
    """Directions (d1, d2) with anticlockwise sweep d1->d2 equal to the interior angle pVq (< 180)."""
    a, b = _dir(v, p), _dir(v, q)
    if (b - a) % 360 <= 180:
        return a, b
    return b, a


def triangle_pts(A, B, base=100):
    C = 180 - A - B
    AC = base * math.sin(math.radians(B)) / math.sin(math.radians(C))
    PA, PB = (0, 0), (base, 0)
    PC = (AC * math.cos(math.radians(A)), AC * math.sin(math.radians(A)))
    return PA, PB, PC


def g_tri(rng, reasoning=False):
    while True:
        A = rng.randrange(35, 86); B = rng.randrange(35, 86); C = 180 - A - B
        if 35 <= C <= 100 and len({A, B, C}) == 3:
            break
    PA, PB, PC = triangle_pts(A, B)
    f = Fig(); f.poly([PA, PB, PC])
    xi = rng.randrange(3)
    vals = [A, B, C]; pts = [PA, PB, PC]
    for i in range(3):
        v = pts[i]; p, q = pts[(i + 1) % 3], pts[(i + 2) % 3]
        d1, d2 = interior(v, p, q)
        angle_mark(f, v, d1, d2, X_LABEL if i == xi else deg(vals[i]), is_x=(i == xi), r_min=10)
    q = Q(skill='g_tri', outcome='MA4-GEO-C-01', ncm='NCM 7 §6.06', prompt=FIND_X, body=f.svg(max_h=84),
          answer=f'<i>x</i> = {vals[xi]}', key=f'tri-{A}-{B}-{xi}',
          **_box('Angle sum of a triangle = 180°', f'Angle sum of a triangle = {gap()}°', 'angle sum of a triangle'))
    return _finish(q, reasoning, 'angle sum of a triangle is 180°')


def g_ext(rng, reasoning=False):
    while True:
        A = rng.randrange(35, 80); C = rng.randrange(35, 90); B = 180 - A - C
        if 35 <= B <= 95 and A != C:
            break
    PA, PB, PC = triangle_pts(A, B)
    f = Fig(); f.poly([PA, PB, PC]); f.line(PB, (PB[0] + 40, 0))
    mode = rng.choice(['ext', 'ext', 'int'])          # mostly find the exterior angle
    d1, d2 = interior(PA, PB, PC)
    e1, e2 = interior(PC, PA, PB)
    if mode == 'ext':
        angle_mark(f, PA, d1, d2, deg(A), r_min=10)
        angle_mark(f, PC, e1, e2, deg(C), r_min=10)
        angle_mark(f, PB, 0, 180 - B, X_LABEL, is_x=True, r_min=10)
        xv = A + C
    else:                                              # exterior given, find an interior opposite angle
        angle_mark(f, PA, d1, d2, X_LABEL, is_x=True, r_min=10)
        angle_mark(f, PC, e1, e2, deg(C), r_min=10)
        angle_mark(f, PB, 0, 180 - B, deg(A + C), r_min=10)
        xv = A
    q = Q(skill='g_ext', outcome='MA4-GEO-C-01', ncm='NCM 7 §6.07', prompt=FIND_X, body=f.svg(max_h=84),
          answer=f'<i>x</i> = {xv}', key=f'ext-{A}-{C}-{mode}',
          **_box('Exterior angle = sum of the 2 interior opposite angles',
                 f'Exterior angle = {gap(34)} of the 2 interior opposite angles', 'exterior angle of a triangle'))
    return _finish(q, reasoning, 'the exterior angle of a triangle equals the sum of the 2 interior opposite angles')


def g_isos(rng, reasoning=False):
    apex = rng.choice([x for x in range(30, 121, 2) if x != 60])
    base = (180 - apex) // 2
    PA, PB, PC = triangle_pts(base, base)
    f = Fig(); f.poly([PA, PB, PC]); f.tick(PA, PC, 1); f.tick(PB, PC, 1)
    mode = rng.choice(['base', 'apex'])
    d1, d2 = interior(PB, PC, PA)
    e1, e2 = interior(PC, PA, PB)
    if mode == 'base':
        angle_mark(f, PC, e1, e2, deg(apex), r_min=10)
        angle_mark(f, PB, d1, d2, X_LABEL, is_x=True, r_min=10)
        xv = base
    else:
        angle_mark(f, PB, d1, d2, deg(base), r_min=10)
        angle_mark(f, PC, e1, e2, X_LABEL, is_x=True, r_min=10)
        xv = apex
    q = Q(skill='g_isos', outcome='MA4-GEO-C-01', ncm='NCM 7 §6.05–6.06', prompt=FIND_X, body=f.svg(max_h=84),
          answer=f'<i>x</i> = {xv}', key=f'isos-{apex}-{mode}',
          **_box('Isosceles triangle: base angles are equal; angle sum = 180°',
                 f'Isosceles triangle: base angles are {gap(28)}; angle sum = 180°', 'isosceles triangle'))
    return _finish(q, reasoning, 'base angles of an isosceles triangle are equal and the angle sum is 180°')


# ---------------------------------------------------------------- quadrilateral
def quad_pts(angles, rng):
    """Convex quadrilateral P0..P3 (anticlockwise) with the given interior angles."""
    a0, a1, a2, a3 = angles
    h = [0, 180 - a1, 360 - a1 - a2, 540 - a1 - a2 - a3]
    best = None
    for L0 in (1.0, 1.1, 1.2, 1.3, 1.4):
        for L1 in (0.6, 0.7, 0.8, 0.9, 1.0):
            # solve L2*u2 + L3*u3 = -(L0*u0 + L1*u1)
            u = [unit(t) for t in h]
            rx = -(L0 * u[0][0] + L1 * u[1][0]); ry = -(L0 * u[0][1] + L1 * u[1][1])
            det = u[2][0] * u[3][1] - u[3][0] * u[2][1]
            if abs(det) < 1e-9:
                continue
            L2 = (rx * u[3][1] - u[3][0] * ry) / det
            L3 = (u[2][0] * ry - rx * u[2][1]) / det
            Ls = [L0, L1, L2, L3]
            if min(Ls) <= 0.6:
                continue
            score = max(Ls) / min(Ls)
            pts = [(0, 0)]
            for i in range(3):
                pts.append((pts[-1][0] + Ls[i] * u[i][0], pts[-1][1] + Ls[i] * u[i][1]))
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            asp = (max(xs) - min(xs)) / max(1e-6, (max(ys) - min(ys)))
            score += abs(math.log(asp / 1.5))
            if best is None or score < best[0]:
                best = (score, pts)
    return best[1] if best else None


def g_quad(rng, reasoning=False):
    while True:
        ang = [rng.randrange(62, 129) for _ in range(3)]
        ang.append(360 - sum(ang))
        if not (62 <= ang[3] <= 128) or len(set(ang)) < 4 or 90 in ang:
            continue
        pts = quad_pts(ang, rng)
        if pts:
            break
    xi = rng.randrange(4)
    f = Fig(); f.poly([(p[0] * 100, p[1] * 100) for p in pts])
    P = [(p[0] * 100, p[1] * 100) for p in pts]
    for i in range(4):
        d1, d2 = interior(P[i], P[(i + 1) % 4], P[(i - 1) % 4])
        angle_mark(f, P[i], d1, d2, X_LABEL if i == xi else deg(ang[i]), is_x=(i == xi), r_min=10)
    q = Q(skill='g_quad', outcome='MA4-GEO-C-01', ncm='NCM 7 §6.09', prompt=FIND_X, body=f.svg(max_h=84),
          answer=f'<i>x</i> = {ang[xi]}', key=f'quad-{"-".join(map(str, ang))}-{xi}',
          **_box('Angle sum of a quadrilateral = 360°', f'Angle sum of a quadrilateral = {gap()}°',
                 'angle sum of a quadrilateral'))
    return _finish(q, reasoning, 'angle sum of a quadrilateral is 360°')


GEO_SKILLS = {
    'g_comp': g_comp, 'g_supp': g_supp, 'g_vopp': g_vopp, 'g_point': g_point,
    'g_corr': g_corr, 'g_alt': g_alt, 'g_coint': g_coint, 'g_tri': g_tri,
    'g_ext': g_ext, 'g_isos': g_isos, 'g_quad': g_quad,
}
