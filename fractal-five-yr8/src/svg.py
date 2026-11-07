"""SVG diagram helpers for The Fractal Five (v3).

Every diagram is built to scale from the numbers in its question.  Geometry is
given in a maths frame (y up).  Decorations (angle arcs, right-angle marks,
tick marks, labels) are sized in points so they look the same at any scale.
The figure is then fitted into the space available in the question cell.
"""
import math, re

BLUE = '#3b7fc0'
DARK = '#1f5e9e'
INK = '#35322d'
SOFT = '#9a948a'
FONTFAM = "'Open Sans',sans-serif"


def fmt(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)


def text_width(s, size):
    """Rough rendered width of a label in pt (Open Sans)."""
    t = strip_tags(s)
    w = 0
    for ch in t:
        if ch in '1il.,:;|!\'':
            w += 0.30
        elif ch == ' ':
            w += 0.27
        elif ch in '°':
            w += 0.40
        elif ch.isupper() or ch in 'mw':
            w += 0.66
        else:
            w += 0.56
    return w * size


def unit(deg):
    a = math.radians(deg)
    return (math.cos(a), math.sin(a))


def pol(c, r, deg):
    u = unit(deg)
    return (c[0] + r * u[0], c[1] + r * u[1])


X_LABEL = ('<tspan font-weight="700" font-style="italic" fill="#1f5e9e">x</tspan>'
           '<tspan font-weight="700" fill="#1f5e9e">°</tspan>')


def var_label(v='x', unit_txt=''):
    s = f'<tspan font-weight="700" font-style="italic" fill="#1f5e9e">{v}</tspan>'
    if unit_txt:
        s += f'<tspan font-weight="700" fill="#1f5e9e">{unit_txt}</tspan>'
    return s


COLLISIONS = []      # set by Fig.svg(): list of collision descriptions for the last figure


def _seg_hits_box(a, b, box):
    (x0, y0, x1, y1) = box
    # Liang-Barsky clip test
    dx, dy = b[0] - a[0], b[1] - a[1]
    p = [-dx, dx, -dy, dy]
    q = [a[0] - x0, x1 - a[0], a[1] - y0, y1 - a[1]]
    u0, u1 = 0.0, 1.0
    for pi, qi in zip(p, q):
        if abs(pi) < 1e-12:
            if qi < 0:
                return False
        else:
            t = qi / pi
            if pi < 0:
                u0 = max(u0, t)
            else:
                u1 = min(u1, t)
            if u0 > u1:
                return False
    return True


class Fig:
    def __init__(self):
        self.geo = []      # geometry items (maths coords)
        self.dec = []      # decorations (anchored in maths coords, sized in pt)
        self.pts = []      # geometry points for scaling

    # ---- geometry ----
    def line(self, p, q, w=1.125, col=BLUE, dash=None, obstacle=True):
        self.geo.append(('line', p, q, w, col, dash, obstacle)); self.pts += [p, q]

    def poly(self, pts, w=1.125, col=BLUE, fill='none', closed=True, dash=None):
        self.geo.append(('poly', list(pts), w, col, fill, closed, dash)); self.pts += list(pts)

    def circle(self, c, r, w=1.125, col=BLUE, fill='none'):
        self.geo.append(('circle', c, r, w, col, fill))
        self.pts += [(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)]

    def ghost(self, p):
        """Point included in the bounding box only."""
        self.pts.append(p)

    # ---- decorations ----
    def dot(self, c, r=1.7, col=INK):
        self.dec.append(('dot', c, r, col))

    def arc(self, c, r, a0, a1, w=0.825, col=BLUE):
        """Arc of screen radius r, anticlockwise from a0 to a1 (degrees, maths frame)."""
        self.dec.append(('arc', c, r, a0, a1, w, col))

    def right_angle(self, c, d1, d2, s=6.5, col=BLUE, w=0.75):
        self.dec.append(('rangle', c, d1, d2, s, col, w))

    def tick(self, p, q, n=1, col=BLUE):
        self.dec.append(('tick', p, q, n, col))

    def arrows(self, c, deg, n=1, col=BLUE):
        self.dec.append(('arrows', c, deg, n, col))

    def label(self, c, s, deg=None, dist=0, size=9.8, anchor='middle', col=INK, weight=400, italic=False):
        """Text at maths point c, pushed `dist` pt in direction deg (screen)."""
        self.dec.append(('label', c, s, deg, dist, size, anchor, col, weight, italic))

    def dim(self, p, q, s, side='above', off=9, size=9.8, at=0.5):
        """Length label beside segment pq (screen offset perpendicular), `at` = fraction along pq."""
        self.dec.append(('dim', p, q, s, side, off, size, at))

    def arrow_dim(self, p, q, s, off=10, size=9.8, side='right', at_x=None):
        """Dimension line with arrow heads (e.g. a height) offset to one side.
        If at_x is given (maths units) the dimension line sits `off` pt beyond x = at_x."""
        self.dec.append(('adim', p, q, s, off, size, side, at_x))

    # ---- output ----
    def svg(self, max_w=230, max_h=86, pad=3, max_scale=None):
        xs = [p[0] for p in self.pts]; ys = [p[1] for p in self.pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        gw, gh = max(x1 - x0, 1e-6), max(y1 - y0, 1e-6)
        scale = min(max_w / gw, max_h / gh)
        if max_scale:
            scale = min(scale, max_scale)
        for _ in range(6):
            self._lbl, self._seg = [], []
            body, bb = self._render(scale, x0, y1)
            bw, bh = bb[2] - bb[0], bb[3] - bb[1]
            f = min(max_w / bw, max_h / bh, 1.0)
            if f > 0.995:
                break
            scale *= f * 0.995
        W, H = bw + 2 * pad, bh + 2 * pad
        tx, ty = pad - bb[0], pad - bb[1]
        self.collisions = []
        boxes = []
        for b, t in self._lbl:
            sh = min(1.6, 0.1 * (b[3] - b[1]) / 0.84)        # small text: smaller allowance
            boxes.append((b[0] + sh, b[1] + sh, b[2] - sh, b[3] - sh, t))
        for i, B in enumerate(boxes):
            for (a, c) in self._seg:
                if _seg_hits_box(a, c, B[:4]):
                    self.collisions.append(f'label {B[4]!r} crosses a line'); break
            for C in boxes[i + 1:]:
                if not (B[2] < C[0] or C[2] < B[0] or B[3] < C[1] or C[3] < B[1]):
                    self.collisions.append(f'labels {B[4]!r} and {C[4]!r} overlap')
        COLLISIONS[:] = self.collisions
        return (f'<svg class="dg" width="{fmt(W)}pt" height="{fmt(H)}pt" viewBox="0 0 {fmt(W)} {fmt(H)}" '
                f'xmlns="http://www.w3.org/2000/svg"><g transform="translate({fmt(tx)},{fmt(ty)})">'
                + body + '</g></svg>')

    def _render(self, s, x0, y1):
        def T(p):
            return ((p[0] - x0) * s, (y1 - p[1]) * s)
        out, box = [], [1e9, 1e9, -1e9, -1e9]

        def grow(x, y):
            box[0] = min(box[0], x); box[1] = min(box[1], y)
            box[2] = max(box[2], x); box[3] = max(box[3], y)

        def sline(a, b, w, col, dash=None, cap='round', record=True):
            if record:
                self._seg.append((a, b))
            ds = f' stroke-dasharray="{dash}"' if dash else ''
            out.append(f'<line x1="{fmt(a[0])}" y1="{fmt(a[1])}" x2="{fmt(b[0])}" y2="{fmt(b[1])}" '
                       f'stroke="{col}" stroke-width="{w}" stroke-linecap="{cap}"{ds}/>')
            grow(*a); grow(*b)

        for it in self.geo:
            k = it[0]
            if k == 'line':
                _, p, q, w, col, dash, obstacle = it
                sline(T(p), T(q), w, col, dash, record=obstacle)
            elif k == 'poly':
                _, pts, w, col, fill, closed, dash = it
                tp = [T(p) for p in pts]
                for p in tp: grow(*p)
                for j in range(len(tp) - (0 if closed else 1)):
                    self._seg.append((tp[j], tp[(j + 1) % len(tp)]))
                tag = 'polygon' if closed else 'polyline'
                ds = f' stroke-dasharray="{dash}"' if dash else ''
                out.append(f'<{tag} points="{" ".join(fmt(a)+","+fmt(b) for a,b in tp)}" fill="{fill}" '
                           f'stroke="{col}" stroke-width="{w}" stroke-linejoin="round"{ds}/>')
            elif k == 'circle':
                _, c, r, w, col, fill = it
                a = T(c); R = r * s
                out.append(f'<circle cx="{fmt(a[0])}" cy="{fmt(a[1])}" r="{fmt(R)}" fill="{fill}" stroke="{col}" stroke-width="{w}"/>')
                grow(a[0] - R, a[1] - R); grow(a[0] + R, a[1] + R)

        for it in self.dec:
            k = it[0]
            if k == 'dot':
                _, c, r, col = it
                a = T(c)
                out.append(f'<circle cx="{fmt(a[0])}" cy="{fmt(a[1])}" r="{r}" fill="{col}"/>')
                grow(a[0] - r, a[1] - r); grow(a[0] + r, a[1] + r)
            elif k == 'arc':
                _, c, r, a0, a1, w, col = it
                a = T(c)
                sweep = (a1 - a0) % 360
                p0 = (a[0] + r * math.cos(math.radians(a0)), a[1] - r * math.sin(math.radians(a0)))
                p1 = (a[0] + r * math.cos(math.radians(a1)), a[1] - r * math.sin(math.radians(a1)))
                large = 1 if sweep > 180 else 0
                out.append(f'<path d="M {fmt(p0[0])} {fmt(p0[1])} A {fmt(r)} {fmt(r)} 0 {large} 0 {fmt(p1[0])} {fmt(p1[1])}" '
                           f'fill="none" stroke="{col}" stroke-width="{w}"/>')
                for t in range(0, 21):
                    ang = a0 + sweep * t / 20
                    grow(a[0] + r * math.cos(math.radians(ang)), a[1] - r * math.sin(math.radians(ang)))
            elif k == 'rangle':
                _, c, d1, d2, sz, col, w = it
                a = T(c)
                u = (math.cos(math.radians(d1)), -math.sin(math.radians(d1)))
                v = (math.cos(math.radians(d2)), -math.sin(math.radians(d2)))
                p1 = (a[0] + sz * u[0], a[1] + sz * u[1])
                p2 = (a[0] + sz * (u[0] + v[0]), a[1] + sz * (u[1] + v[1]))
                p3 = (a[0] + sz * v[0], a[1] + sz * v[1])
                out.append(f'<polyline points="{fmt(p1[0])},{fmt(p1[1])} {fmt(p2[0])},{fmt(p2[1])} {fmt(p3[0])},{fmt(p3[1])}" '
                           f'fill="none" stroke="{col}" stroke-width="{w}"/>')
                for p in (p1, p2, p3): grow(*p)
            elif k == 'tick':
                _, p, q, n, col = it
                a, b = T(p), T(q)
                mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                L = math.hypot(b[0] - a[0], b[1] - a[1])
                ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
                nx, ny = -uy, ux
                for j in range(n):
                    off = (j - (n - 1) / 2) * 3.2
                    cx, cy = mx + ux * off, my + uy * off
                    sline((cx - nx * 4, cy - ny * 4), (cx + nx * 4, cy + ny * 4), 0.75, col, cap='butt', record=False)
            elif k == 'arrows':
                _, c, deg, n, col = it
                a = T(c)
                ux, uy = math.cos(math.radians(deg)), -math.sin(math.radians(deg))
                nx, ny = -uy, ux
                for j in range(n):
                    cx, cy = a[0] + ux * (j - (n - 1) / 2) * 4.5, a[1] + uy * (j - (n - 1) / 2) * 4.5
                    tip = (cx + ux * 2.6, cy + uy * 2.6)
                    b1 = (cx - ux * 2.6 + nx * 3.2, cy - uy * 2.6 + ny * 3.2)
                    b2 = (cx - ux * 2.6 - nx * 3.2, cy - uy * 2.6 - ny * 3.2)
                    out.append(f'<polyline points="{fmt(b1[0])},{fmt(b1[1])} {fmt(tip[0])},{fmt(tip[1])} {fmt(b2[0])},{fmt(b2[1])}" '
                               f'fill="none" stroke="{col}" stroke-width="0.9" stroke-linejoin="round"/>')
                    for p in (b1, tip, b2): grow(*p)
            elif k == 'label':
                _, c, txt, deg, dist, size, anchor, col, weight, italic = it
                a = T(c)
                if deg is not None:
                    a = (a[0] + dist * math.cos(math.radians(deg)), a[1] - dist * math.sin(math.radians(deg)))
                self._text(out, grow, a, txt, size, anchor, col, weight, italic)
            elif k == 'dim':
                _, p, q, txt, side, off, size, at = it
                a, b = T(p), T(q)
                mx, my = a[0] + (b[0] - a[0]) * at, a[1] + (b[1] - a[1]) * at
                dx, dy = b[0] - a[0], b[1] - a[1]
                L = math.hypot(dx, dy)
                nx, ny = dy / L, -dx / L          # left normal in screen coords
                if side in ('below', 'right'):
                    nx, ny = -nx, -ny
                # choose direction explicitly for axis-aligned segments
                if side == 'above': nx, ny = 0, -1
                if side == 'below': nx, ny = 0, 1
                if side == 'left': nx, ny = -1, 0
                if side == 'right': nx, ny = 1, 0
                w = text_width(txt, size)
                cx = mx + nx * (off + (w / 2 if nx else 0))
                cy = my + ny * (off + (size * 0.35 if ny else 0))
                self._text(out, grow, (cx, cy), txt, size, 'middle', INK, 400, False)
            elif k == 'adim':
                _, p, q, txt, off, size, side, at_x = it
                a, b = T(p), T(q)
                sx = off if side == 'right' else -off
                if at_x is not None:
                    xx = T((at_x, 0))[0] + sx
                    a2, b2 = (xx, a[1]), (xx, b[1])
                else:
                    a2, b2 = (a[0] + sx, a[1]), (b[0] + sx, b[1])
                sline(a2, b2, 0.75, INK, cap='butt', record=False)
                self._seg.append((a2, b2))
                for (pp, other) in ((a2, b2), (b2, a2)):
                    dirn = 1 if other[1] > pp[1] else -1
                    out.append(f'<polygon points="{fmt(pp[0])},{fmt(pp[1])} {fmt(pp[0]-2.2)},{fmt(pp[1]+dirn*4)} {fmt(pp[0]+2.2)},{fmt(pp[1]+dirn*4)}" fill="{INK}"/>')
                # dotted extension lines
                sline(a, a2, 0.6, SOFT, '1.5,1.5', cap='butt', record=False); sline(b, b2, 0.6, SOFT, '1.5,1.5', cap='butt', record=False)
                w = text_width(txt, size)
                tx = a2[0] + (5 + w / 2 if side == 'right' else -(5 + w / 2))
                self._text(out, grow, (tx, (a2[1] + b2[1]) / 2), txt, size, 'middle', INK, 400, False)
        return ''.join(out), box

    def _text(self, out, grow, a, txt, size, anchor, col, weight, italic):
        w = text_width(txt, size)
        st = 'font-style:italic;' if italic else ''
        out.append(f'<text x="{fmt(a[0])}" y="{fmt(a[1] + size * 0.35)}" text-anchor="{anchor}" '
                   f'style="font-family:{FONTFAM};font-size:{size}px;font-weight:{weight};{st}fill:{col}">{txt}</text>')
        if anchor == 'middle':
            xa, xb = a[0] - w / 2, a[0] + w / 2
        elif anchor == 'start':
            xa, xb = a[0], a[0] + w
        else:
            xa, xb = a[0] - w, a[0]
        grow(xa, a[1] - size * 0.45); grow(xb, a[1] + size * 0.45)
        self._lbl.append(((xa, a[1] - size * 0.42, xb, a[1] + size * 0.42), strip_tags(txt)))


# ---------------------------------------------------------------------------
# Angle-label placement: put the label on the bisector, far enough out that it
# fits between the arms, and draw the arc just inside the label.
# ---------------------------------------------------------------------------
def angle_mark(fig, v, d1, d2, txt, is_x=False, r_min=11, label_size=9.8, arc=True):
    """Mark the angle at v swept anticlockwise from direction d1 to d2."""
    sweep = (d2 - d1) % 360
    mid = d1 + sweep / 2
    w = text_width(txt, label_size) + 3
    half = math.radians(min(sweep, 170) / 2)
    need = (w / 2) / max(math.sin(half), 0.2) + 3
    dist = max(r_min + 9, need)
    r = max(r_min, min(dist - 9, 22))
    if arc:
        fig.arc(v, r, d1, d1 + sweep, col=DARK if is_x else BLUE)
    fig.label(v, txt, deg=mid, dist=dist, size=label_size,
              col=DARK if is_x else INK, weight=700 if is_x else 400)
    return dist
