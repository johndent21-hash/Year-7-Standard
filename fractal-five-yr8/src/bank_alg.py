"""Algebra, equations and linear relationships, Year 7 (NCM 7 Ch 5, Ch 9).
MA4-ALG-C-01, MA4-EQU-C-01, MA4-LIN-C-01."""
from fractions import Fraction as F
from mathfmt import gap, frac, v, num, lin, MINUS, sup, signed_term
from svg import Fig, BLUE, INK

SUB_RULE = 'Replace each pronumeral with its value (use brackets)'
SUB_GAP = f'Replace each pronumeral with its {gap(24)} (use brackets)'
EQ_RULE = 'Do the same to both sides (use the inverse operation)'
EQ_GAP = f'Do the same to {gap(24)} sides (use the inverse operation)'


def Q(**kw):
    base = dict(year=7, unit='Y7', strand='A', calc=False, reasoning=False, body='', answer_alt='',
                labels=None, box='M')
    base.update(kw)
    return base


def big(expr):
    return f'<div class="expr">{expr}</div>'


def vals_text(d):
    items = [f'{v(k)}&nbsp;=&nbsp;{num(val)}' for k, val in d.items()]
    if len(items) == 1:
        return items[0]
    return ', '.join(items[:-1]) + ' and ' + items[-1]


# ---------------------------------------------------------------- substitution
SUBS = [
    ('3a + 2b', lambda a, b: 3 * a + 2 * b, f'3{v("a")} + 2{v("b")}', 'ab'),
    ('5m - 2n', lambda m, n_: 5 * m - 2 * n_, f'5{v("m")} {MINUS} 2{v("n")}', 'mn'),
    ('p^2 + 4', lambda p: p * p + 4, f'{v("p")}<sup>2</sup> + 4', 'p'),
    ('2(a + b)', lambda a, b: 2 * (a + b), f'2({v("a")} + {v("b")})', 'ab'),
    ('20 - 3k', lambda k: 20 - 3 * k, f'20 {MINUS} 3{v("k")}', 'k'),
    ('ab - 4', lambda a, b: a * b - 4, f'{v("ab")} {MINUS} 4', 'ab'),
    ('4p + q^2', lambda p, q: 4 * p + q * q, f'4{v("p")} + {v("q")}<sup>2</sup>', 'pq'),
    ('x^2 - 2x', lambda x: x * x - 2 * x, f'{v("x")}<sup>2</sup> {MINUS} 2{v("x")}', 'x'),
    ('6 + 2t^2', lambda t: 6 + 2 * t * t, f'6 + 2{v("t")}<sup>2</sup>', 't'),
    ('5(y - 2)', lambda y: 5 * (y - 2), f'5({v("y")} {MINUS} 2)', 'y'),
    ('3(2m - 1)', lambda m: 3 * (2 * m - 1), f'3(2{v("m")} {MINUS} 1)', 'm'),
    ('pq + 10', lambda p, q: p * q + 10, f'{v("pq")} + 10', 'pq'),
    ('(a + b)/2', lambda a, b: F(a + b, 2), frac(f'{v("a")} + {v("b")}', 2), 'ab'),
    ('12/n + 3', lambda n_: F(12, n_) + 3, f'{frac(12, v("n"))} + 3', 'n'),
    ('7x - y', lambda x, y: 7 * x - y, f'7{v("x")} {MINUS} {v("y")}', 'xy'),
    ('2a + 3b - c', lambda a, b, c: 2 * a + 3 * b - c, f'2{v("a")} + 3{v("b")} {MINUS} {v("c")}', 'abc'),
]


def a_sub(rng, reasoning=False):
    while True:
        name, fn, html, letters = rng.choice(SUBS)
        vals = {L: rng.randrange(1, 10) for L in letters}
        if name == '12/n + 3':
            vals['n'] = rng.choice([2, 3, 4, 6, 12])
        if name == '(a + b)/2' and (vals['a'] + vals['b']) % 2:
            continue
        if name == '20 - 3k' and vals['k'] > 6:
            continue
        res = fn(*vals.values())
        if isinstance(res, F) and res.denominator != 1:
            continue
        if res >= 0:
            break
    return Q(skill='a_sub', outcome='MA4-ALG-C-01', ncm='NCM 7 §5.05',
             prompt=f'Find the value of this expression when {vals_text(vals)}.', body=big(html),
             answer=num(int(res)), key=f'sub-{name}-{sorted(vals.items())}', box_text=SUB_RULE, box_gap=SUB_GAP,
             box_name='substitution')


# ---------------------------------------------------------------- like terms, ×, ÷ terms
def a_like(rng, reasoning=False):
    kind = rng.choice(['two', 'mixed', 'const', 'four'])
    x, y = rng.choice([('a', 'b'), ('x', 'y'), ('m', 'n'), ('p', 'q')])
    if kind == 'two':
        a, b = rng.randrange(2, 12), rng.randrange(2, 9)
        if rng.random() < 0.5:
            s = f'{a}{v(x)} + {b}{v(x)}'; ans = f'{a+b}{v(x)}'
        else:
            a = a + b
            s = f'{a}{v(x)} {MINUS} {b}{v(x)}'; ans = f'{a-b}{v(x)}' if a - b != 1 else v(x)
    elif kind == 'mixed':
        a, c, b = rng.randrange(3, 10), rng.randrange(2, 9), rng.randrange(1, 3)
        b = rng.randrange(1, a)
        s = f'{a}{v(x)} + {c}{v(y)} {MINUS} {b}{v(x)}'; ans = f'{signed_term(a-b, v(x), True)} + {c}{v(y)}'
    elif kind == 'const':
        a, b, c = rng.randrange(5, 12), rng.randrange(1, 5), rng.randrange(2, 9)
        s = f'{a}{v(x)} {MINUS} {b}{v(x)} + {c}'; ans = f'{signed_term(a-b, v(x), True)} + {c}'
    else:
        a, b, c, d = rng.randrange(2, 8), rng.randrange(2, 8), rng.randrange(1, 6), rng.randrange(1, 4)
        d = min(d, b - 1) if b > 1 else 1
        s = f'{a}{v(x)} + {b}{v(y)} + {c}{v(x)} {MINUS} {d}{v(y)}'
        ans = f'{signed_term(a+c, v(x), True)} + {signed_term(b-d, v(y), True)}' if b - d > 0 else f'{a+c}{v(x)}'
    return Q(skill='a_like', outcome='MA4-ALG-C-01', ncm='NCM 7 §5.06–5.07', prompt='Simplify.', body=big(s), answer=ans,
             key=f'like-{s}', box_text='Only like terms (the same pronumerals) can be added or subtracted',
             box_gap=f'Only {gap(22)} terms (the same pronumerals) can be added or subtracted', box_name='simplifying like terms')


def a_mult(rng, reasoning=False):
    kind = rng.choice(['num', 'two', 'same'])
    x, y = rng.choice([('a', 'b'), ('x', 'y'), ('m', 'n'), ('p', 'q')])
    a, b = rng.randrange(2, 8), rng.randrange(2, 7)
    if kind == 'num':
        s = f'{a} × {b}{v(x)}'; ans = f'{a*b}{v(x)}'
    elif kind == 'two':
        s = f'{a}{v(x)} × {b}{v(y)}'; ans = f'{a*b}{v(x+y)}'
    else:
        s = f'{v(x)} × {v(x)}'; ans = f'{v(x)}<sup>2</sup>'; a = b = 1
    return Q(skill='a_mult', outcome='MA4-ALG-C-01', ncm='NCM 7 §5.08', prompt='Simplify.', body=big(s), answer=ans,
             key=f'mult-{s}', box_text='Multiply the numbers, then the pronumerals (in alphabetical order)',
             box_gap=f'Multiply the {gap(26)}, then the pronumerals (in alphabetical order)', box_name='multiplying terms')


def a_div(rng, reasoning=False):
    kind = rng.choice(['num', 'cancel', 'frac'])
    x, y = rng.choice([('a', 'b'), ('x', 'y'), ('m', 'n')])
    b = rng.randrange(2, 7); q_ = rng.randrange(2, 8); a = b * q_
    if kind == 'num':
        s = f'{a}{v(x)} ÷ {b}'; ans = f'{q_}{v(x)}'
    elif kind == 'cancel':
        s = f'{a}{v(x+y)} ÷ {b}{v(x)}'; ans = f'{q_}{v(y)}'
    else:
        s = frac(f'{a}{v(x)}', b); ans = f'{q_}{v(x)}'
    return Q(skill='a_div', outcome='MA4-ALG-C-01', ncm='NCM 7 §5.09', prompt='Simplify.', body=big(s), answer=ans,
             key=f'div-{s}', box_text='Divide the numbers, then cancel pronumerals that are top and bottom',
             box_gap=f'Divide the numbers, then {gap(24)} pronumerals that are top and bottom', box_name='dividing terms')


def a_write(rng, reasoning=False):
    x = rng.choice(['n', 'x', 'a', 'm'])
    k = rng.randrange(2, 10); c = rng.randrange(2, 10)
    kind = rng.choice(['more', 'less', 'double', 'times_more', 'divided', 'times_less'])
    if kind == 'more':
        words = f'{c} more than {v(x)}'; ans = f'{v(x)} + {c}'
    elif kind == 'less':
        words = f'{c} less than {v(x)}'; ans = f'{v(x)} {MINUS} {c}'
    elif kind == 'double':
        words = f'double {v(x)}, then add {c}'; ans = f'2{v(x)} + {c}'
    elif kind == 'times_more':
        words = f'{c} more than {k} times {v(x)}'; ans = f'{k}{v(x)} + {c}'
    elif kind == 'divided':
        words = f'{v(x)} divided by {k}'; ans = frac(v(x), k)
    else:
        words = f'{c} less than {k} times {v(x)}'; ans = f'{k}{v(x)} {MINUS} {c}'
    return Q(skill='a_write', outcome='MA4-ALG-C-01', ncm='NCM 7 §5.04', prompt='Write an algebraic expression for:',
             body=big(f'<span class="words">{words}</span>'), answer=ans, key=f'write-{kind}-{x}-{k}-{c}',
             box_text='Turn words into symbols: more than +, less than −, times ×',
             box_gap=f'Turn words into symbols: more than +, less than {gap(14)}, times ×',
             box_name='writing algebraic expressions')


# ---------------------------------------------------------------- equations
def e_one(rng, reasoning=False):
    x = rng.choice(['x', 'm', 'k', 'y', 'p', 'a'])
    kind = rng.choice(['add', 'sub', 'mul', 'div'])
    sol = rng.randrange(2, 16)
    if kind == 'add':
        c = rng.randrange(3, 15); s = f'{v(x)} + {c} = {sol + c}'
    elif kind == 'sub':
        sol = rng.randrange(8, 20); c = rng.randrange(2, sol - 1); s = f'{v(x)} {MINUS} {c} = {sol - c}'
    elif kind == 'mul':
        c = rng.randrange(2, 10); s = f'{c}{v(x)} = {c * sol}'
    else:
        c = rng.randrange(2, 7); q_ = rng.randrange(2, 10); s = f'{frac(v(x), c)} = {q_}'; sol = q_ * c
    return Q(skill='e_one', outcome='MA4-EQU-C-01', ncm='NCM 7 §5.11', prompt='Solve.', body=big(s),
             answer=f'{v(x)} = {num(sol)}', key=f'eone-{s}', box_text=EQ_RULE, box_gap=EQ_GAP, box_name='solving equations')


def e_two(rng, reasoning=False):
    x = rng.choice(['x', 'm', 'k', 'y', 'p', 'a', 'n'])
    sol = rng.randrange(2, 13); a = rng.randrange(2, 8); b = rng.randrange(1, 15)
    kind = rng.choice(['plus', 'minus', 'cplus', 'div'])
    if kind == 'plus':
        s = f'{a}{v(x)} + {b} = {a * sol + b}'
    elif kind == 'minus':
        s = f'{a}{v(x)} {MINUS} {b} = {num(a * sol - b)}'
    elif kind == 'cplus':
        s = f'{b} + {a}{v(x)} = {a * sol + b}'
    else:
        sol = a * rng.randrange(1, 7); s = f'{frac(v(x), a)} + {b} = {sol // a + b}'
    q = Q(skill='e_two', outcome='MA4-EQU-C-01', ncm='NCM 7 §5.12', prompt='Solve.', body=big(s),
          answer=f'{v(x)} = {num(sol)}', key=f'etwo-{s}', box_text=EQ_RULE, box_gap=EQ_GAP, box_name='solving equations')
    if reasoning and kind in ('plus', 'minus', 'cplus'):
        test = sol + rng.choice([-1, 1]) if rng.random() < 0.5 else sol
        ok = test == sol
        q.update(prompt=f'Is {v(x)} = {test} the solution of this equation? Show how you know.', reasoning=True,
                 labels=['RULE', 'WORKING', '', 'EXPLAIN'], box_text='Check a solution by substituting it into both sides',
                 box_gap=f'Check a solution by {gap(30)} it into both sides', box_name='checking a solution',
                 answer=(f'Yes: substituting {v(x)} = {test} makes both sides equal.' if ok else
                         f'No: substituting {v(x)} = {test} does not make both sides equal (the solution is {v(x)} = {sol}).'))
    return q


# ---------------------------------------------------------------- linear relationships
def a_table(rng):
    m = rng.choice([1, 2, 3, 4, 5, -1, -2]); c = rng.randrange(-3, 8)
    if m < 0:
        c = rng.randrange(6, 13)
    start = rng.choice([0, 1, -1]) if m > 0 else rng.choice([0, 1])
    xs = list(range(start, start + 4))
    ys = [m * x + c for x in xs]
    return m, c, xs, ys


def table_html(xs, ys, blanks):
    xr = ''.join(f'<td>{num(x)}</td>' for x in xs)
    yr = ''.join('<td></td>' if i in blanks else f'<td>{num(y)}</td>' for i, y in enumerate(ys))
    return (f'<table class="dt xy"><tr><th><i>x</i></th>{xr}</tr><tr><th><i>y</i></th>{yr}</tr></table>')


def l_table(rng, reasoning=False):
    m, c, xs, ys = a_table(rng)
    blanks = sorted(rng.sample(range(4), 2))
    rule = f'{v("y")} = {lin(m, c)}'
    return Q(skill='l_table', outcome='MA4-LIN-C-01', ncm='NCM 7 §9.04–9.05', prompt=f'Complete the table for {rule}.',
             body=table_html(xs, ys, blanks), answer=', '.join(f'{v("x")} = {num(xs[i])}: {v("y")} = {num(ys[i])}' for i in blanks),
             key=f'ltab-{m}-{c}-{xs[0]}-{blanks}', box_text='Substitute each <i>x</i>-value into the rule',
             box_gap=f'{gap(30)} each <i>x</i>-value into the rule', box_name='tables of values')


def l_point(rng, reasoning=False):
    m = rng.choice([2, 3, 4, 5, -2, 1]); c = rng.randrange(-4, 8)
    x0 = rng.randrange(1, 6)
    y0 = m * x0 + c
    rule = f'{v("y")} = {lin(m, c)}'
    if reasoning:
        on = rng.random() < 0.5
        yq = y0 if on else y0 + rng.choice([-2, -1, 1, 2])
        q = Q(skill='l_point', outcome='MA4-LIN-C-01', ncm='NCM 7 §9.06',
              prompt=f'Does the point ({num(x0)}, {num(yq)}) lie on the line {rule}? Explain.', reasoning=True,
              labels=['RULE', 'WORKING', '', 'EXPLAIN'],
              answer=(f'Yes: when {v("x")} = {x0}, {v("y")} = {num(y0)}.' if on else
                      f'No: when {v("x")} = {x0}, {v("y")} = {num(y0)}, not {num(yq)}.'),
              key=f'lpt-r-{m}-{c}-{x0}-{yq}')
    else:
        q = Q(skill='l_point', outcome='MA4-LIN-C-01', ncm='NCM 7 §9.06',
              prompt=f'The point ({num(x0)}, {v("k")}) lies on the line {rule}. Find the value of {v("k")}.',
              answer=f'{v("k")} = {num(y0)}', key=f'lpt-{m}-{c}-{x0}')
    q.update(box_text='A point lies on a line if its coordinates make the rule true',
             box_gap=f'A point lies on a line if its coordinates make the rule {gap(20)}', box_name='points on a line')
    return q


def grid_fig(points, lim=3):
    f = Fig()
    for i in range(-lim, lim + 1):
        f.line((i, -lim), (i, lim), w=0.45, col='#d9d4ca', obstacle=False); f.line((-lim, i), (lim, i), w=0.45, col='#d9d4ca', obstacle=False)
    f.line((-lim - 0.6, 0), (lim + 0.6, 0), w=0.9, col=INK); f.line((0, -lim - 0.6), (0, lim + 0.6), w=0.9, col=INK)
    f.arrows((lim + 0.6, 0), 0, col=INK); f.arrows((0, lim + 0.6), 90, col=INK)
    f.label((lim + 0.6, 0), '<tspan font-style="italic">x</tspan>', deg=-60, dist=9, size=8.5)
    f.label((0, lim + 0.6), '<tspan font-style="italic">y</tspan>', deg=180, dist=8, size=8.5)
    for i in range(-lim, lim + 1):
        if i == 0:
            continue
        f.label((i, 0), str(i).replace('-', MINUS), deg=-90, dist=6.5, size=6.8, col='#6b665e')
        f.label((0, i), str(i).replace('-', MINUS), deg=180, dist=6.5, size=6.8, col='#6b665e')
    for (px, py, name) in points:
        f.dot((px, py), 2.1, BLUE)
        f.label((px, py), name, deg=45, dist=7.5, size=9, weight=700, col='#1f5e9e')
    return f


def l_coord(rng, reasoning=False):
    while True:
        P = (rng.randrange(-3, 4), rng.randrange(-3, 4))
        if P[0] != 0 and P[1] != 0 and (P[0] < 0 or P[1] < 0):
            break
    f = grid_fig([(P[0], P[1], 'P')])
    return Q(skill='l_coord', outcome='MA4-LIN-C-01', ncm='NCM 7 §9.02–9.03', prompt='Write the coordinates of the point P.',
             body=f.svg(max_w=170, max_h=104), answer=f'({num(P[0])}, {num(P[1])})', key=f'coord-{P}',
             box_text='Coordinates (<i>x</i>, <i>y</i>): across first, then up or down',
             box_gap=f'Coordinates (<i>x</i>, <i>y</i>): {gap(26)} first, then up or down', box_name='coordinates')


ALG_SKILLS = {
    'a_sub': a_sub, 'a_like': a_like, 'a_mult': a_mult, 'a_div': a_div, 'a_write': a_write,
    'e_one': e_one, 'e_two': e_two, 'l_table': l_table, 'l_point': l_point, 'l_coord': l_coord,
}
