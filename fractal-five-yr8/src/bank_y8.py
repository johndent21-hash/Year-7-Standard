"""Year 8 unit generators (2027 Year 8 mixed ability, NCM 8 3rd edition).

FRC8  Rational numbers, percentages & financial maths  MA4-FRC-C-01  NCM 8 §6.04–6.10 (+ §2.07)
IND8  Index laws (numerical bases)                     MA4-IND-C-01  NCM 8 §2.08, 2.10–2.12
PYT8  Pythagoras' theorem                              MA4-PYT-C-01  NCM 8 Ch 1
ALG8  Algebra 2                                        MA4-ALG-C-01  NCM 8 §3.01–3.10
EQU8  Equations 2                                      MA4-EQU-C-01  NCM 8 §9.01–9.03, 9.05–9.07
No simple interest (Stage 5), no binomial products, no equations with brackets, no change of subject.
"""
import math
from fractions import Fraction as F
from mathfmt import gap, frac, fr, num, money, MINUS, sup, v, lin, signed_term
from svg import Fig

NAMES = ['Mia', 'Noah', 'Priya', 'Leo', 'Zoe', 'Theo', 'Aisha', 'Hamish', 'Freya', 'Omar', 'Grace', 'Felix', 'Nina', 'Eli']


def Q(**kw):
    base = dict(year=8, calc=False, reasoning=False, body='', answer_alt='', labels=None, box='M')
    base.update(kw)
    return base


def big(expr):
    return f'<div class="expr">{expr}</div>'


# =========================================================== FRC8 percentages
FRC = dict(unit='FRC8', strand='N', outcome='MA4-FRC-C-01')
ITEMS = [('a surfboard', 'surfboard'), ('a pair of sneakers', 'pair of sneakers'), ('a beach umbrella', 'beach umbrella'),
         ('a school bag', 'school bag'), ('a skateboard', 'skateboard'), ('a wetsuit', 'wetsuit'), ('a bike helmet', 'bike helmet'),
         ('a pair of goggles', 'pair of goggles'), ('a boogie board', 'boogie board')]
# realistic prices (dollars) for each item
PRICES = {'surfboard': (300, 800), 'pair of sneakers': (80, 240), 'beach umbrella': (30, 90), 'school bag': (40, 120),
          'skateboard': (60, 200), 'wetsuit': (150, 400), 'bike helmet': (40, 120), 'pair of goggles': (20, 60),
          'boogie board': (40, 160)}


def _item_price(rng, p=None):
    """Pick an item and a realistic price; if p is given, the p% must be a whole number of dollars."""
    for _ in range(400):
        item, name = rng.choice(ITEMS)
        lo, hi = PRICES[name]
        a = rng.choice([v for v in range(lo, hi + 1, 10)])
        if p is None or (p * a) % 100 == 0:
            return item, a
    return ('a beach umbrella', 'beach umbrella'), 40
PCTS = [(10, 'easy'), (20, 'easy'), (25, 'easy'), (50, 'easy'), (5, 'easy'), (30, 'ok'), (15, 'ok'), (40, 'ok'), (75, 'ok')]


def _pct_amount(rng):
    while True:
        p = rng.choice([10, 20, 25, 50, 5, 30, 15, 40])
        a = rng.choice([20, 40, 60, 80, 100, 120, 160, 200, 240, 300, 400, 50, 150, 250])
        if (p * a) % 100 == 0:
            return p, a


def f8_inc(rng, reasoning=False):
    p, a = _pct_amount(rng)
    unit_ = rng.choice(['$', ' kg', ' mL', '$'])
    new = a + p * a // 100
    if unit_ == '$':
        prompt = f'Increase {money(a)} by {p}%.'; ans = money(new)
    else:
        prompt = f'Increase {a}{unit_} by {p}%.'; ans = f'{new}{unit_}'
    return Q(skill='f8_inc', ncm='NCM 8 §6.07', prompt=prompt, answer=ans, key=f'inc-{a}-{p}-{unit_}',
             box_text='Find the percentage of the amount, then add it on',
             box_gap=f'Find the percentage of the amount, then {gap(22)} it on', box_name='percentage increase', **FRC)


def f8_dec(rng, reasoning=False):
    p, a = _pct_amount(rng)
    unit_ = rng.choice([' kg', ' L', ' km', '$'])
    new = a - p * a // 100
    if unit_ == '$':
        prompt = f'Decrease {money(a)} by {p}%.'; ans = money(new)
    else:
        prompt = f'Decrease {a}{unit_} by {p}%.'; ans = f'{new}{unit_}'
    return Q(skill='f8_dec', ncm='NCM 8 §6.07', prompt=prompt, answer=ans, key=f'dec-{a}-{p}-{unit_}',
             box_text='Find the percentage of the amount, then take it away',
             box_gap=f'Find the percentage of the amount, then {gap(26)} it away', box_name='percentage decrease', **FRC)


def f8_disc(rng, reasoning=False):
    p = rng.choice([10, 20, 25, 50, 30, 40, 15])
    item, a = _item_price(rng, p)
    sale = a - p * a // 100
    return Q(skill='f8_disc', ncm='NCM 8 §6.07, 6.10',
             prompt=f'{item[0].upper() + item[1:]} costs {money(a)}. It is on sale at {p}% off. Find the sale price.',
             answer=money(sale), key=f'disc-{a}-{p}-{item}',
             box_text='Discount = % × price; sale price = price − discount',
             box_gap=f'Discount = % × price; sale price = price {gap(14)} discount', box_name='discounts', **FRC)


def f8_gst(rng, reasoning=False):
    item, a = _item_price(rng)
    if rng.random() < 0.6:
        prompt = f'The price of {item} is {money(a)} before GST. Add 10% GST to find the price including GST.'
        ans = money(a * 11 / 10); key = f'gst-incl-{a}'
    else:
        prompt = f'The price of {item} is {money(a)} before GST. How much is the GST (10%)?'
        ans = money(a / 10); key = f'gst-amt-{a}'
    return Q(skill='f8_gst', ncm='NCM 8 §6.10', box='F', prompt=prompt, answer=ans, key=key + item,
             box_text='GST = 10% of the price; price incl. GST = price + GST',
             box_gap=f'GST = {gap(18)} of the price; price incl. GST = price + GST', box_name='GST', **FRC)


def f8_profit(rng, reasoning=False):
    who, thing, costs = rng.choice([('The canteen', 'a box of 10 drinks', [10, 20]), ('The canteen', 'a tray of 20 pies', [40, 50, 60]),
                                    ('A surf shop', 'a T-shirt', [20, 25, 40]), ('A surf shop', 'a cap', [10, 20, 25]),
                                    ('A market stall', 'a candle', [10, 20]), ('The school P&amp;C', 'a box of 50 icy poles', [20, 25, 40, 50])])
    while True:
        cost = rng.choice(costs)
        p = rng.choice([10, 20, 25, 50, 40, 5])
        diff = F(cost * p, 100)
        if diff.denominator == 1 and diff > 0:
            break
    loss = rng.random() < 0.3
    sell = cost - diff if loss else cost + diff
    word = 'loss' if loss else 'profit'
    return Q(skill='f8_profit', ncm='NCM 8 §6.10', box='F',
             prompt=f'{who} buys {thing} for {money(cost)} and sells it for {money(sell)}. Find the {word} as a percentage of the cost price.',
             answer=f'{p}% {word}', key=f'profit-{cost}-{sell}',
             box_text=f'Profit (or loss) % = profit (or loss) ÷ cost price × 100%',
             box_gap=f'Profit (or loss) % = profit (or loss) ÷ {gap(34)} × 100%', box_name='profit and loss as a percentage', **FRC)


def f8_change(rng, reasoning=False):
    thing, olds = rng.choice([('the price of a pie', [4, 5, 6, 8]), ('the number of nippers', [40, 50, 60, 80, 120]),
                              ('the cost of a movie ticket', [15, 16, 20]), ('the price of a surf lesson', [40, 50, 60, 80])])
    while True:
        old = rng.choice(olds)
        p = rng.choice([10, 20, 25, 50, 40, 5])
        d = F(old * p, 100)
        if d.denominator == 1:
            break
    up = rng.random() < 0.6
    new = old + d if up else old - d
    is_money = 'price' in thing or 'cost' in thing
    o, nn = (money(old), money(new)) if is_money else (num(old), num(int(new)))
    return Q(skill='f8_change', ncm='NCM 8 §6.07', box='F',
             prompt=f'{thing[0].upper() + thing[1:]} changed from {o} to {nn}. Find the percentage {"increase" if up else "decrease"}.',
             answer=f'{p}%', key=f'chg-{old}-{new}-{thing}',
             box_text='Percentage change = change ÷ original amount × 100%',
             box_gap=f'Percentage change = change ÷ {gap(40)} × 100%', box_name='percentage change', **FRC)


def f8_unitary(rng, reasoning=False):
    p = rng.choice([10, 20, 25, 5, 50, 40])
    whole = rng.choice([40, 60, 80, 120, 200, 240, 300, 160])
    part = whole * p // 100
    if whole * p % 100:
        part = None
    while part is None:
        whole = rng.choice([40, 60, 80, 120, 200, 240, 300, 160]); part = whole * p // 100 if whole * p % 100 == 0 else None
    ctx = rng.choice(['number', 'students', 'savings'])
    if ctx == 'number':
        prompt = f'{p}% of a number is {part}. What is the number?'; ans = num(whole)
    elif ctx == 'students':
        prompt = f'{p}% of the students at a school walk to school. That is {part} students. How many students are at the school?'
        ans = f'{whole} students'
    else:
        nm = rng.choice(NAMES)
        prompt = f'{nm} has saved {money(part)}, which is {p}% of the cost of a new phone. How much does the phone cost?'
        ans = money(whole)
    return Q(skill='f8_unitary', ncm='NCM 8 §6.09', prompt=prompt, answer=ans, key=f'unit-{p}-{whole}-{ctx}',
             box_text='Unitary method: find 1% (or 10%) first, then multiply to get 100%',
             box_gap=f'Unitary method: find {gap(18)} (or 10%) first, then multiply to get 100%',
             box_name='the unitary method', **FRC)


def f8_reason(rng, reasoning=True):
    a, b = rng.choice([(20, 50), (10, 30), (25, 40), (50, 60), (5, 80)])
    return Q(skill='f8_reason', ncm='NCM 8 §6.05, 6.12', reasoning=True, labels=['RULE', 'WORKING', '', 'EXPLAIN'],
             prompt=f'Is {a}% of ${b} the same as {b}% of ${a}? Explain.', key=f'frcR-{a}-{b}',
             answer=f'Yes: both are ${a*b//100} ({a}% of {b} = {b}% of {a} = {a} × {b} ÷ 100).',
             box_text='Percentage of a quantity = percentage ÷ 100 × quantity',
             box_gap=f'Percentage of a quantity = percentage ÷ {gap(18)} × quantity', box_name='percentage of a quantity', **FRC)


# =========================================================== IND8 index laws
IND = dict(unit='IND8', strand='N', outcome='MA4-IND-C-01')


def i8_mult(rng, reasoning=False):
    b = rng.randrange(2, 10); m = rng.randrange(2, 7); n_ = rng.randrange(2, 6)
    q = Q(skill='i8_mult', ncm='NCM 8 §2.11', box='F', prompt='Simplify. Write your answer as a single power.',
          body=big(f'{sup(b, m)} × {sup(b, n_)}'), answer=sup(b, m + n_), key=f'imul-{b}-{m}-{n_}',
          box_text='<i>a</i><sup><i>m</i></sup> × <i>a</i><sup><i>n</i></sup> = <i>a</i><sup><i>m</i> + <i>n</i></sup>',
          box_gap=f'<i>a</i><sup><i>m</i></sup> × <i>a</i><sup><i>n</i></sup> = <i>a</i><sup>{gap(16)}</sup>',
          box_name='index law for multiplying', **IND)
    if reasoning:
        q.update(prompt=f'{rng.choice(NAMES)} says {sup(b, m)} × {sup(b, n_)} = {sup(b*b, m+n_)}. Explain the mistake.',
                 body='', reasoning=True, labels=['RULE', 'WORKING', '', 'EXPLAIN'],
                 answer=f'The base stays {b}; only the indices are added: {sup(b, m)} × {sup(b, n_)} = {sup(b, m+n_)}, not {sup(b*b, m+n_)}.')
    return q


def i8_div(rng, reasoning=False):
    b = rng.randrange(2, 10); n_ = rng.randrange(2, 5); m = n_ + rng.randrange(1, 6)
    return Q(skill='i8_div', ncm='NCM 8 §2.12', box='F', prompt='Simplify. Write your answer as a single power.',
             body=big(f'{sup(b, m)} ÷ {sup(b, n_)}'), answer=sup(b, m - n_) if m - n_ > 1 else f'{b}<sup>1</sup> = {b}',
             key=f'idiv-{b}-{m}-{n_}',
             box_text='<i>a</i><sup><i>m</i></sup> ÷ <i>a</i><sup><i>n</i></sup> = <i>a</i><sup><i>m</i> − <i>n</i></sup>',
             box_gap=f'<i>a</i><sup><i>m</i></sup> ÷ <i>a</i><sup><i>n</i></sup> = <i>a</i><sup>{gap(16)}</sup>',
             box_name='index law for dividing', **IND)


def i8_pow(rng, reasoning=False):
    b = rng.randrange(2, 10); m = rng.randrange(2, 5); n_ = rng.randrange(2, 5)
    return Q(skill='i8_pow', ncm='NCM 8 §2.12', box='F', prompt='Simplify. Write your answer as a single power.',
             body=big(f'({sup(b, m)})<sup>{n_}</sup>'), answer=sup(b, m * n_), key=f'ipow-{b}-{m}-{n_}',
             box_text='(<i>a</i><sup><i>m</i></sup>)<sup><i>n</i></sup> = <i>a</i><sup><i>mn</i></sup>',
             box_gap=f'(<i>a</i><sup><i>m</i></sup>)<sup><i>n</i></sup> = <i>a</i><sup>{gap(16)}</sup>',
             box_name='power of a power', **IND)


def i8_zero(rng, reasoning=False):
    kind = rng.choice(['one', 'sum', 'times', 'mix'])
    b = rng.randrange(2, 13); c = rng.randrange(2, 10)
    if kind == 'one':
        s = sup(b, 0); val = 1
    elif kind == 'sum':
        s = f'{sup(b, 0)} + {sup(c, 0)}'; val = 2
    elif kind == 'times':
        s = f'{c} × {sup(b, 0)}'; val = c
    else:
        s = f'{sup(c, 2)} + {sup(b, 0)}'; val = c * c + 1
    return Q(skill='i8_zero', ncm='NCM 8 §2.12', box='F', prompt='Evaluate.', body=big(s), answer=num(val),
             key=f'izero-{s}', box_text='<i>a</i><sup>0</sup> = 1 (any non-zero number to the power 0 is 1)',
             box_gap=f'<i>a</i><sup>0</sup> = {gap(14)} (any non-zero number to the power 0)', box_name='the zero index', **IND)


def i8_prime(rng, reasoning=False):
    m = rng.choice([24, 36, 40, 48, 54, 56, 72, 80, 90, 96, 100, 108, 120, 135, 144, 200])
    fs = {}; t = m; p = 2
    while t > 1:
        while t % p == 0:
            fs[p] = fs.get(p, 0) + 1; t //= p
        p += 1
    ans = ' × '.join(sup(p, e) if e > 1 else str(p) for p, e in sorted(fs.items()))
    return Q(skill='i8_prime', ncm='NCM 8 §2.10', prompt=f'Write {m} as a product of prime factors in index form.',
             answer=ans, key=f'iprime-{m}',
             box_text='Factor tree to primes, then write repeated primes as powers',
             box_gap=f'Factor tree to primes, then write repeated primes as {gap(28)}',
             box_name='prime factors in index form', **IND)


# =========================================================== PYT8 Pythagoras
PYT = dict(unit='PYT8', strand='M', outcome='MA4-PYT-C-01')
TRIADS = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25), (15, 20, 25), (10, 24, 26),
          (18, 24, 30), (30, 40, 50), (60, 80, 100), (50, 120, 130), (1.5, 2, 2.5), (0.6, 0.8, 1), (2.5, 6, 6.5), (20, 21, 29)]


def _n(v):
    return num(v) if not isinstance(v, float) else (str(v).rstrip('0').rstrip('.') if '.' in str(v) else str(v))


def right_tri_fig(a, b, la, lb, lc, corner):
    """Legs a (horizontal) and b (vertical); right angle at bottom-left or bottom-right."""
    f = Fig()
    if corner == 'BL':
        P = [(0, 0), (a, 0), (0, b)]
        f.poly(P); f.right_angle((0, 0), 0, 90, 6)
        f.dim(P[0], P[1], la, 'below'); f.dim(P[2], P[0], lb, 'left')
        f.label(((a) / 2, b / 2), lc, deg=45, dist=10, anchor='start')
    else:
        P = [(0, 0), (a, 0), (a, b)]
        f.poly(P); f.right_angle((a, 0), 90, 180, 6)
        f.dim(P[0], P[1], la, 'below'); f.dim(P[1], P[2], lb, 'right')
        f.label((a / 2, b / 2), lc, deg=135, dist=10, anchor='end')
    return f


def _xl(s='x'):
    return f'<tspan font-weight="700" font-style="italic" fill="#1f5e9e">{s}</tspan>'


PYT_BOX = dict(box='F', box_text='<i>c</i><sup>2</sup> = <i>a</i><sup>2</sup> + <i>b</i><sup>2</sup> (<i>c</i> is the hypotenuse)',
               box_gap=f'<i>c</i><sup>2</sup> = <i>a</i><sup>2</sup> + {gap(22)} (<i>c</i> is the hypotenuse)',
               box_name="Pythagoras' theorem")


def p8_hyp(rng, reasoning=False):
    a, b, c = rng.choice(TRIADS[:16])
    if rng.random() < 0.5:
        a, b = b, a
    u = rng.choice(['cm', 'm'])
    f = right_tri_fig(a, b, f'{_n(a)} {u}', f'{_n(b)} {u}', _xl(), rng.choice(['BL', 'BR']))
    return Q(skill='p8_hyp', ncm='NCM 8 §1.03', prompt='Find the length of the hypotenuse, <i>x</i>.', body=f.svg(max_h=82),
             answer=f'<i>x</i> = {_n(c)} {u}', key=f'hyp-{a}-{b}{u}', **PYT_BOX, **PYT)


def p8_short(rng, reasoning=False):
    a, b, c = rng.choice(TRIADS[:16])
    u = rng.choice(['cm', 'm'])
    missing_a = rng.random() < 0.5
    la = _xl() if missing_a else f'{_n(a)} {u}'
    lb = f'{_n(b)} {u}' if missing_a else _xl()
    f = right_tri_fig(a, b, la, lb, f'{_n(c)} {u}', rng.choice(['BL', 'BR']))
    ans = a if missing_a else b
    return Q(skill='p8_short', ncm='NCM 8 §1.04', prompt='Find the length of the shorter side, <i>x</i>.', body=f.svg(max_h=82),
             answer=f'<i>x</i> = {_n(ans)} {u}', key=f'short-{a}-{b}-{missing_a}{u}', **PYT_BOX, **PYT)


def p8_test(rng, reasoning=False):
    if rng.random() < 0.55:
        a, b, c = rng.choice([t for t in TRIADS if all(isinstance(v, int) for v in t) and t[2] <= 30])
        ok = True
    else:
        a, b, c = rng.choice([(4, 5, 6), (5, 6, 8), (6, 7, 9), (2, 3, 4), (7, 8, 10), (5, 5, 7), (8, 9, 12), (4, 6, 7)])
        ok = False
    u = rng.choice(['cm', 'm'])
    lhs = a * a + b * b
    q = Q(skill='p8_test', ncm='NCM 8 §1.06', reasoning=reasoning, box='F',
          prompt=f'A triangle has sides {a} {u}, {b} {u} and {c} {u}. Is it right-angled?' + (' Explain.' if reasoning else ''),
          answer=(f'Yes: {a}² + {b}² = {lhs} = {c}²' if ok else f'No: {a}² + {b}² = {lhs}, but {c}² = {c*c}'),
          key=f'test-{a}-{b}-{c}{u}',
          box_text='Right-angled if (longest side)<sup>2</sup> = sum of the squares of the other 2 sides',
          box_gap=f'Right-angled if (longest side)<sup>2</sup> = {gap(22)} of the squares of the other 2 sides',
          box_name="converse of Pythagoras' theorem", **PYT)
    if reasoning:
        q['labels'] = ['RULE', 'WORKING', '', 'EXPLAIN']
    return q


def p8_dec(rng, reasoning=False):
    a, b = rng.choice([(2, 3), (4, 5), (5, 7), (3, 5), (6, 9), (4, 7), (2, 5), (5, 8)])
    u = rng.choice(['cm', 'm'])
    c = math.sqrt(a * a + b * b)
    f = right_tri_fig(a, b, f'{a} {u}', f'{b} {u}', _xl(), rng.choice(['BL', 'BR']))
    return Q(skill='p8_dec', ncm='NCM 8 §1.03', calc=True, prompt='Find the hypotenuse, <i>x</i>, correct to 1 decimal place.',
             body=f.svg(max_h=80), answer=f'<i>x</i> = {c:.1f} {u}', key=f'hdec-{a}-{b}{u}', **PYT_BOX, **PYT)


def p8_est(rng, reasoning=False):
    n_ = rng.choice([n for n in range(5, 120) if int(math.isqrt(n)) ** 2 != n])
    lo = math.isqrt(n_)
    return Q(skill='p8_est', ncm='NCM 8 §1.01', outcome='MA4-IND-C-01', unit='PYT8', strand='M',
             prompt='Between which two whole numbers does this square root lie?', body=big(f'<span class="rt">√<span class="rad">{n_}</span></span>'),
             answer=f'{lo} and {lo + 1} (because {lo*lo} &lt; {n_} &lt; {(lo+1)**2})', key=f'est-{n_}',
             box_text='Find the square numbers just below and just above the number',
             box_gap=f'Find the {gap(26)} numbers just below and just above the number', box_name='estimating square roots')


# =========================================================== ALG8 Algebra 2
ALG = dict(unit='ALG8', strand='A', outcome='MA4-ALG-C-01')
EXP_BOX = dict(box='F', box_text='<i>a</i>(<i>b</i> + <i>c</i>) = <i>ab</i> + <i>ac</i>',
               box_gap=f'<i>a</i>(<i>b</i> + <i>c</i>) = <i>ab</i> + {gap(16)}', box_name='expanding brackets')


def a8_expand(rng, reasoning=False):
    x = rng.choice(['x', 'a', 'm', 'y', 'k', 'p'])
    a = rng.randrange(2, 10); b = rng.randrange(1, 6); c = rng.randrange(1, 10)
    sign = rng.choice([1, -1])
    neg_out = rng.random() < 0.15
    if neg_out:
        a = -a
    inner = f'{signed_term(b, v(x), True)}{" + " if sign > 0 else f" {MINUS} "}{c}'
    s = f'{num(a)}({inner})'
    ans = f'{signed_term(a*b, v(x), True)}{signed_term(a*c*sign, "")}'
    q = Q(skill='a8_expand', ncm='NCM 8 §3.07', prompt='Expand.', body=big(s), answer=ans, key=f'exp-{s}', **EXP_BOX, **ALG)
    if reasoning and not neg_out and b == 1 and sign > 0:
        nm = rng.choice(NAMES)
        q.update(prompt=f'{nm} expanded {s} and got {a}{v(x)} + {c}. Explain the error.', body='', reasoning=True,
                 labels=['COPY', 'WORKING', '', 'EXPLAIN'],
                 answer=f'{nm} only multiplied the first term; both terms must be multiplied by {a}: {a}{v(x)} + {a*c}.')
    return q


def a8_expsimp(rng, reasoning=False):
    x = rng.choice(['x', 'a', 'm', 'n'])
    a = rng.randrange(2, 6); c = rng.randrange(1, 8); d = rng.randrange(1, 9)
    kind = rng.choice(['plusx', 'plusc'])
    if kind == 'plusx':
        s = f'{a}({v(x)} + {c}) + {d}{v(x)}'; ans = f'{a + d}{v(x)} + {a*c}'
    else:
        s = f'{a}({v(x)} + {c}) + {d}'; ans = f'{a}{v(x)} + {a*c + d}'
    return Q(skill='a8_expsimp', ncm='NCM 8 §3.07', prompt='Expand and simplify.', body=big(s), answer=ans, key=f'expsimp-{s}',
             box_text='Expand the brackets, then collect like terms', box_gap=f'Expand the brackets, then collect {gap(22)} terms',
             box_name='expanding and simplifying', **ALG)


def a8_fact(rng, reasoning=False):
    x = rng.choice(['x', 'a', 'm', 'y', 'k'])
    while True:
        h = rng.randrange(2, 10); b = rng.randrange(1, 5); c = rng.randrange(1, 10)
        if math.gcd(b, c) == 1:
            break
    sign = rng.choice([1, 1, -1])
    s = f'{signed_term(h*b, v(x), True)}{" + " if sign > 0 else f" {MINUS} "}{h*c}'
    ans = f'{h}({signed_term(b, v(x), True)}{" + " if sign > 0 else f" {MINUS} "}{c})'
    return Q(skill='a8_fact', ncm='NCM 8 §3.08–3.09', prompt='Factorise.', body=big(s), answer=ans, key=f'fact-{s}',
             box_text='Take out the highest common factor (HCF); check by expanding',
             box_gap=f'Take out the highest common {gap(26)} (HCF); check by expanding', box_name='factorising', **ALG)


def a8_sub(rng, reasoning=False):
    forms = [('3a − b', lambda a, b: 3 * a - b, f'3{v("a")} {MINUS} {v("b")}', 'ab'),
             ('2x^2', lambda x: 2 * x * x, f'2{v("x")}<sup>2</sup>', 'x'),
             ('pq + 5', lambda p, q: p * q + 5, f'{v("pq")} + 5', 'pq'),
             ('m^2 − 4', lambda m: m * m - 4, f'{v("m")}<sup>2</sup> {MINUS} 4', 'm'),
             ('4(a + b)', lambda a, b: 4 * (a + b), f'4({v("a")} + {v("b")})', 'ab')]
    name, fn, html, letters = rng.choice(forms)
    vals = {}
    for L in letters:
        vals[L] = rng.choice([-5, -4, -3, -2, -1, 2, 3, 4, 5])
    if all(val > 0 for val in vals.values()):
        vals[letters[0]] = -abs(vals[letters[0]])
    res = fn(*vals.values())
    vt = ', '.join(f'{v(k)}&nbsp;=&nbsp;{num(val)}' for k, val in vals.items())
    vt = vt.replace(', ', ' and ', 1) if len(vals) == 2 else vt
    return Q(skill='a8_sub', ncm='NCM 8 §3.03', prompt=f'Find the value of this expression when {vt}.', body=big(html),
             answer=num(res), key=f'sub8-{name}-{sorted(vals.items())}',
             box_text='Replace each pronumeral with its value (use brackets)',
             box_gap=f'Replace each pronumeral with its {gap(24)} (use brackets)',
             box_name='substitution', **ALG)


def a8_like2(rng, reasoning=False):
    x = rng.choice(['x', 'a', 'm'])
    a, b, c, d = rng.randrange(2, 7), rng.randrange(2, 8), rng.randrange(1, 4), rng.randrange(1, 6)
    s = f'{a}{v(x)}<sup>2</sup> + {b}{v(x)} {MINUS} {c}{v(x)}<sup>2</sup> + {d}{v(x)}'
    ans = f'{signed_term(a - c, v(x) + "<sup>2</sup>", True)} + {b + d}{v(x)}' if a != c else f'{b + d}{v(x)}'
    return Q(skill='a8_like2', ncm='NCM 8 §3.04', prompt='Simplify.', body=big(s), answer=ans, key=f'like8-{s}',
             box_text='Like terms have exactly the same pronumerals and powers', box_gap=f'Like terms have exactly the same pronumerals and {gap(26)}',
             box_name='like terms', **ALG)


def a8_multdiv(rng, reasoning=False):
    x = rng.choice(['a', 'x', 'm', 'p'])
    a, b = rng.randrange(2, 7), rng.randrange(2, 7)
    if rng.random() < 0.5:
        s = f'{a}{v(x)} × {b}{v(x)}'; ans = f'{a*b}{v(x)}<sup>2</sup>'
        rule = 'Multiply the numbers, then the pronumerals (<i>a</i> × <i>a</i> = <i>a</i><sup>2</sup>)'
        rg = f'Multiply the numbers, then the pronumerals (<i>a</i> × <i>a</i> = {gap(16)})'
    else:
        s = f'{a*b}{v(x)}<sup>2</sup> ÷ {a}{v(x)}'; ans = f'{b}{v(x)}' if b != 1 else v(x)
        rule = 'Divide the numbers, then cancel common pronumerals (<i>a</i><sup>2</sup> ÷ <i>a</i> = <i>a</i>)'
        rg = f'Divide the numbers, then {gap(22)} common pronumerals (<i>a</i><sup>2</sup> ÷ <i>a</i> = <i>a</i>)'
    return Q(skill='a8_multdiv', ncm='NCM 8 §3.05', prompt='Simplify.', body=big(s), answer=ans, key=f'md8-{s}',
             box_text=rule, box_gap=rg, box_name='multiplying and dividing terms', **ALG)


# =========================================================== EQU8 Equations 2
EQU = dict(unit='EQU8', strand='A', outcome='MA4-EQU-C-01')
EQ_RULE = 'Do the same to both sides (use the inverse operation)'
EQ_GAP = f'Do the same to {gap(24)} sides (use the inverse operation)'


def e8_both(rng, reasoning=False):
    x = rng.choice(['x', 'a', 'm', 'n', 'k'])
    while True:
        sol = rng.randrange(1, 10); a = rng.randrange(3, 9); c = rng.randrange(1, a)
        b = rng.randrange(1, 15); d = (a - c) * sol + b
        if d != b:
            break
    s = f'{a}{v(x)} + {b} = {signed_term(c, v(x), True)} + {d}'
    q = Q(skill='e8_both', ncm='NCM 8 §9.03', prompt='Solve.', body=big(s), answer=f'{v(x)} = {sol}', key=f'both-{s}',
          box_text='Move the pronumerals to one side first, then solve',
          box_gap=f'Move the {gap(30)} to one side first, then solve', box_name='pronumerals on both sides', **EQU)
    if reasoning:
        test = sol if rng.random() < 0.5 else sol + 1
        ok = test == sol
        q.update(prompt=f'Is {v(x)} = {test} the solution of this equation? Show how you know.', reasoning=True,
                 labels=['RULE', 'WORKING', '', 'EXPLAIN'], box_text='Check a solution by substituting it into both sides',
                 box_gap=f'Check a solution by {gap(30)} it into both sides', box_name='checking a solution',
                 answer=(f'Yes: both sides equal {a*test+b} when {v(x)} = {test}.' if ok else
                         f'No: left side = {a*test+b}, right side = {c*test+d}; the solution is {v(x)} = {sol}.'))
    return q


def e8_quad(rng, reasoning=False):
    x = rng.choice(['x', 'a', 'm', 'y'])
    r = rng.randrange(2, 13)
    kind = rng.choice(['plain', 'coef', 'plus'])
    if kind == 'plain':
        s = f'{v(x)}<sup>2</sup> = {r*r}'
    elif kind == 'coef':
        k = rng.choice([2, 3, 4, 5]); r = rng.randrange(2, 8); s = f'{k}{v(x)}<sup>2</sup> = {k*r*r}'
    else:
        c = rng.randrange(1, 12); r = rng.randrange(2, 9); s = f'{v(x)}<sup>2</sup> + {c} = {r*r + c}'
    return Q(skill='e8_quad', ncm='NCM 8 §9.05', prompt='Solve.', body=big(s), answer=f'{v(x)} = {r} or {v(x)} = {MINUS}{r}',
             key=f'quad-{s}', box_text='<i>x</i><sup>2</sup> = <i>c</i> has 2 solutions: <i>x</i> = √<i>c</i> or <i>x</i> = −√<i>c</i>',
             box_gap=f'<i>x</i><sup>2</sup> = <i>c</i> has {gap(12)} solutions: <i>x</i> = √<i>c</i> or <i>x</i> = −√<i>c</i>',
             box_name='equations of the form ax² = c', **EQU)


def e8_formula(rng, reasoning=False):
    kind = rng.choice(['P', 'A', 'v', 'C', 'S'])
    if kind == 'P':
        l, w = rng.randrange(5, 15), rng.randrange(2, 9); P = 2 * l + 2 * w
        f_ = '<i>P</i> = 2<i>l</i> + 2<i>w</i>'; prompt = f'Use the formula to find <i>w</i> when <i>P</i> = {P} and <i>l</i> = {l}.'; ans = f'<i>w</i> = {w}'
        key = f'fP-{l}-{w}'
    elif kind == 'A':
        l, w = rng.randrange(4, 13), rng.randrange(2, 10); A = l * w
        f_ = '<i>A</i> = <i>lw</i>'; prompt = f'Use the formula to find <i>l</i> when <i>A</i> = {A} and <i>w</i> = {w}.'; ans = f'<i>l</i> = {l}'
        key = f'fA-{l}-{w}'
    elif kind == 'v':
        u_, a, t = rng.randrange(0, 10), rng.randrange(2, 6), rng.randrange(2, 8); vv = u_ + a * t
        f_ = '<i>v</i> = <i>u</i> + <i>at</i>'; prompt = f'Use the formula to find <i>t</i> when <i>v</i> = {vv}, <i>u</i> = {u_} and <i>a</i> = {a}.'; ans = f'<i>t</i> = {t}'
        key = f'fv-{u_}-{a}-{t}'
    elif kind == 'C':
        h = rng.randrange(1, 8); rate = rng.choice([5, 8, 10, 12, 15]); base = rng.choice([10, 15, 20, 25]); C = base + rate * h
        f_ = f'<i>C</i> = {rate}<i>h</i> + {base}'
        prompt = f'Hiring a kayak at Cudgen Creek costs <i>C</i> dollars for <i>h</i> hours. Use the formula to find <i>h</i> when <i>C</i> = {C}.'
        ans = f'<i>h</i> = {h} (hours)'; key = f'fC-{rate}-{base}-{h}'
    else:
        n_ = rng.randrange(3, 10); S = 180 * (n_ - 2)
        f_ = '<i>S</i> = 180(<i>n</i> − 2)'
        prompt = f'The angle sum of a polygon with <i>n</i> sides is <i>S</i>°. Find <i>n</i> when <i>S</i> = {S}.'
        ans = f'<i>n</i> = {n_}'; key = f'fS-{n_}'
    return Q(skill='e8_formula', ncm='NCM 8 §9.07', box='F', nofade=True, prompt=prompt, answer=ans, key=key,
             box_text=f_, box_gap=f_.replace('</i> = ', f'</i> = ', 1), box_name='substituting into a formula', **EQU)


def e8_word(rng, reasoning=False):
    sol = rng.randrange(2, 13); a = rng.randrange(2, 6); b = rng.randrange(1, 15)
    kind = rng.choice(['plus', 'minus'])
    nm = rng.choice(NAMES)
    if kind == 'plus':
        res = a * sol + b
        mult = {2: 'doubles it', 3: 'multiplies it by 3', 4: 'multiplies it by 4', 5: 'multiplies it by 5'}[a]
        prompt = f'{nm} thinks of a number, {mult} and adds {b}. The answer is {res}. Write and solve an equation to find the number.'
        eq = f'{a}{v("n")} + {b} = {res}'
    else:
        res = a * sol - b
        if res <= 0:
            res = a * sol + b; kind = 'plus'
            prompt = f'{nm} thinks of a number, multiplies it by {a} and adds {b}. The answer is {res}. Write and solve an equation to find the number.'
            eq = f'{a}{v("n")} + {b} = {res}'
        else:
            prompt = f'{nm} thinks of a number, multiplies it by {a} and subtracts {b}. The answer is {res}. Write and solve an equation to find the number.'
            eq = f'{a}{v("n")} {MINUS} {b} = {res}'
    return Q(skill='e8_word', ncm='NCM 8 §9.06', prompt=prompt, answer=f'{eq}; the number is {sol}', key=f'word-{a}-{b}-{sol}-{kind}',
             box_text='Let <i>n</i> be the number; write an equation, then solve it',
             box_gap=f'Let <i>n</i> be the number; write an {gap(30)}, then solve it', box_name='equation problems', **EQU)


def e8_nonint(rng, reasoning=False):
    x = rng.choice(['x', 'a', 'm'])
    while True:
        a = rng.choice([2, 4, 5]); b = rng.randrange(1, 10); c = rng.randrange(b + 1, b + 15)
        sol = F(c - b, a)
        if sol.denominator != 1:
            break
    s = f'{a}{v(x)} + {b} = {c}'
    whole, rem = divmod(sol.numerator, sol.denominator)
    alt = f'{whole}{frac(rem, sol.denominator)}' if whole else fr(sol)
    return Q(skill='e8_nonint', ncm='NCM 8 §9.02', prompt='Solve. Give your answer as a fraction or a decimal.', body=big(s),
             answer=f'{v(x)} = {num(float(sol))} (= {alt})', key=f'nonint-{s}', box_text=EQ_RULE, box_gap=EQ_GAP,
             box_name='solving equations', **EQU)


Y8_SKILLS = {
    'FRC8': {'f8_inc': f8_inc, 'f8_dec': f8_dec, 'f8_disc': f8_disc, 'f8_gst': f8_gst, 'f8_profit': f8_profit,
             'f8_change': f8_change, 'f8_unitary': f8_unitary},
    'IND8': {'i8_mult': i8_mult, 'i8_div': i8_div, 'i8_pow': i8_pow, 'i8_zero': i8_zero, 'i8_prime': i8_prime},
    'PYT8': {'p8_hyp': p8_hyp, 'p8_short': p8_short, 'p8_test': p8_test, 'p8_dec': p8_dec, 'p8_est': p8_est},
    'ALG8': {'a8_expand': a8_expand, 'a8_expsimp': a8_expsimp, 'a8_fact': a8_fact, 'a8_sub': a8_sub,
             'a8_like2': a8_like2, 'a8_multdiv': a8_multdiv},
    'EQU8': {'e8_both': e8_both, 'e8_quad': e8_quad, 'e8_formula': e8_formula, 'e8_word': e8_word, 'e8_nonint': e8_nonint},
}
REASONING_EXTRA = {'FRC8': f8_reason}
