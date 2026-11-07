"""Number generators, Year 7 (NCM 7 Ch 1, 3, 4, 7).
Integers MA4-INT-C-01; powers, roots, primes MA4-IND-C-01; fractions, decimals, percentages MA4-FRC-C-01."""
from fractions import Fraction as F
from mathfmt import gap, frac, fr, sup, sqrt, cbrt, rec, num, money, MINUS

CTX_WHOLE = [('of the {n} nippers at the surf club', 'nippers'), ('of the {n} stalls at the Kingscliff markets', 'stalls'),
             ('of the {n} students in a class', 'students'), ('of the {n} players in a touch footy squad', 'players')]


def Q(**kw):
    base = dict(year=7, unit='Y7', strand='N', calc=False, reasoning=False, body='', answer_alt='',
                labels=None, box='M')
    base.update(kw)
    return base


def big(expr):
    return f'<div class="expr">{expr}</div>'


def n(x):
    return num(x)


# ---------------------------------------------------------------- order of operations
def n_ooo(rng, reasoning=False):
    while True:
        form = rng.choice(['a+b*c', 'a-b*c', '(a+b)*c', 'a*b-c*d', 'a/b+c', '(a-b)*c', 'a-b/c', '-a+b*c'])
        a, b, c, d = (rng.randrange(2, 13) for _ in range(4))
        if form == 'a+b*c': val = a + b * c; s = f'{a} + {b} × {c}'
        elif form == 'a-b*c': val = a - b * c; s = f'{a} {MINUS} {b} × {c}'
        elif form == '(a+b)*c': val = (a + b) * c; s = f'({a} + {b}) × {c}'
        elif form == '(a-b)*c': val = (a - b) * c; s = f'({a} {MINUS} {b}) × {c}'
        elif form == 'a*b-c*d': val = a * b - c * d; s = f'{a} × {b} {MINUS} {c} × {d}'
        elif form == 'a/b+c':
            a = b * rng.randrange(2, 9); val = a // b + c; s = f'{a} ÷ {b} + {c}'
        elif form == 'a-b/c':
            b = c * rng.randrange(2, 7); val = a - b // c; s = f'{a} {MINUS} {b} ÷ {c}'
        else:
            val = -a + b * c; s = f'{MINUS}{a} + {b} × {c}'
        if -30 <= val <= 120:
            break
    q = Q(skill='n_ooo', outcome='MA4-INT-C-01', ncm='NCM 7 §1.08', prompt='Evaluate.', body=big(s),
          answer=n(val), key=f'ooo-{s}',
          box_text='Brackets, then × and ÷ (left to right), then + and − (left to right)',
          box_gap=f'Brackets, then × and ÷ (left to right), then {gap(30)} (left to right)',
          box_name='order of operations')
    if reasoning:
        wrong = (a + b) * c if form == 'a+b*c' else None
        if form == 'a+b*c':
            q.update(prompt=f'Sam says {a} + {b} × {c} = {wrong}. Explain the mistake and give the correct answer.',
                     body='', reasoning=True, labels=['RULE', 'WORKING', '', 'EXPLAIN'],
                     answer=f'Sam added first; × must be done before +. Correct answer {n(val)}.')
    return q


# ---------------------------------------------------------------- integers
def n_int(rng, reasoning=False):
    op = rng.choice(['add', 'sub', 'subneg', 'mul', 'div'])
    a = rng.randrange(2, 16); b = rng.randrange(2, 16)
    if op == 'add':
        val = -a + b; s = f'{MINUS}{a} + {b}'
        rule = 'Start at the first number on a number line; adding moves right'
        rgap = f'Start at the first number on a number line; adding moves {gap(26)}'
        name = 'adding integers'
    elif op == 'sub':
        val = a - (a + b); s = f'{a} {MINUS} {a + b}'
        rule = 'Subtracting moves left on a number line'
        rgap = f'Subtracting moves {gap(24)} on a number line'
        name = 'subtracting integers'
    elif op == 'subneg':
        val = -a + b; s = f'{MINUS}{a} {MINUS} ({MINUS}{b})'
        rule = 'Subtracting a negative is the same as adding'
        rgap = f'Subtracting a negative is the same as {gap(28)}'
        name = 'subtracting a negative'
    elif op == 'mul':
        sa, sb = rng.choice([(-1, 1), (1, -1), (-1, -1)])
        a, b = rng.randrange(2, 10), rng.randrange(2, 10)
        val = sa * a * sb * b
        s = f'{n(sa*a)} × {"(" + n(sb*b) + ")" if sb < 0 else n(sb*b)}'
        rule = 'Same signs: answer positive. Different signs: answer negative'
        rgap = f'Same signs: answer {gap(28)}. Different signs: answer negative'
        name = 'multiplying and dividing integers'
    else:
        sa, sb = rng.choice([(-1, 1), (1, -1), (-1, -1)])
        b = rng.randrange(2, 10); q_ = rng.randrange(2, 10); a = b * q_
        val = (sa * a) // (sb * b)
        s = f'{n(sa*a)} ÷ {"(" + n(sb*b) + ")" if sb < 0 else n(sb*b)}'
        rule = 'Same signs: answer positive. Different signs: answer negative'
        rgap = f'Same signs: answer {gap(28)}. Different signs: answer negative'
        name = 'multiplying and dividing integers'
    return Q(skill='n_int', outcome='MA4-INT-C-01', ncm='NCM 7 §1.04–1.07', prompt='Evaluate.', body=big(s),
             answer=n(val), key=f'int-{s}', box_text=rule, box_gap=rgap, box_name=name)


# ---------------------------------------------------------------- powers and roots
def n_pow(rng, reasoning=False):
    form = rng.choice(['single', 'single', 'sum', 'tens'])
    if form == 'single':
        b, e = rng.choice([(2, 5), (2, 6), (3, 3), (3, 4), (4, 3), (5, 3), (2, 4), (10, 4), (6, 2), (9, 2), (11, 2), (1, 7), (7, 2)])
        val = b ** e; s = sup(b, e)
    elif form == 'sum':
        b1, e1, b2, e2 = rng.choice([(2, 3, 3, 2), (4, 2, 2, 3), (5, 2, 3, 3), (10, 2, 2, 4), (6, 2, 2, 2), (3, 3, 1, 5), (2, 5, 5, 2)])
        val = b1 ** e1 + b2 ** e2; s = f'{sup(b1, e1)} + {sup(b2, e2)}'
    else:
        e = rng.choice([3, 4, 5]); val = 10 ** e; s = sup(10, e)
    q = Q(skill='n_pow', outcome='MA4-IND-C-01', ncm='NCM 7 §3.07', box='F', prompt='Evaluate.', body=big(s),
          answer=n(val), key=f'pow-{s}',
          box_text='<i>a</i><sup><i>n</i></sup> = <i>a</i> × <i>a</i> × … × <i>a</i> (<i>n</i> factors)',
          box_gap=f'<i>a</i><sup><i>n</i></sup> = <i>a</i> × <i>a</i> × … × <i>a</i> ({gap(14)} factors)',
          box_name='index notation')
    if reasoning and form == 'single' and b > 1:
        q.update(prompt=f'Mia says {sup(b, e)} = {b*e}. Explain her mistake and give the correct value.', body='',
                 reasoning=True, labels=['RULE', 'WORKING', '', 'EXPLAIN'],
                 answer=f'Mia multiplied {b} × {e}; {sup(b, e)} means {" × ".join([str(b)]*e)} = {n(val)}.')
    return q


def n_root(rng, reasoning=False):
    if rng.random() < 0.6:
        r = rng.choice([4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 20]); s = sqrt(r * r); kind = 'sq'
    else:
        r = rng.choice([2, 3, 4, 5, 10]); s = cbrt(r ** 3); kind = 'cb'
    return Q(skill='n_root', outcome='MA4-IND-C-01', ncm='NCM 7 §3.08', prompt='Evaluate.', body=big(s), answer=n(r),
             key=f'root-{kind}-{r}',
             box_text='√<i>a</i> is the number that squares to <i>a</i>; ' + cbrt('<i>a</i>') + ' is the number that cubes to <i>a</i>',
             box_gap=f'√<i>a</i> is the number that {gap(28)} to <i>a</i>; ' + cbrt('<i>a</i>') + ' is the number that cubes to <i>a</i>',
             box_name='square roots and cube roots')


def n_prime(rng, reasoning=False):
    m = rng.choice([12, 18, 20, 28, 30, 42, 44, 45, 50, 52, 63, 66, 70, 75, 98])
    fs = []; t = m; p = 2
    while t > 1:
        while t % p == 0:
            fs.append(p); t //= p
        p += 1
    return Q(skill='n_prime', outcome='MA4-IND-C-01', ncm='NCM 7 §3.09–3.10',
             prompt=f'Write {m} as a product of its prime factors.', answer=' × '.join(map(str, fs)), key=f'prime-{m}',
             box_text='Use a factor tree: keep splitting until every branch ends in a prime',
             box_gap=f'Use a factor tree: keep splitting until every branch ends in a {gap(26)}',
             box_name='prime factors (factor tree)')


# ---------------------------------------------------------------- fractions and percentages
CTX_RANGE = {'nippers': (24, 80), 'stalls': (20, 60), 'students': (20, 32), 'players': (12, 24)}


def n_fracq(rng, reasoning=False):
    use_ctx = rng.random() < 0.45
    tmpl, noun = rng.choice(CTX_WHOLE)
    while True:
        d = rng.choice([3, 4, 5, 6, 8, 10, 12]); a = rng.randrange(1, d)
        if F(a, d).denominator != d:
            continue
        k = rng.randrange(2, 13); qty = d * k
        lo, hi = CTX_RANGE[noun] if use_ctx else (6, 200)
        if lo <= qty <= hi:
            break
    val = a * k
    if use_ctx:
        verb = {'nippers': 'passed the swim test', 'stalls': 'sell food', 'students': 'walk to school',
                'players': 'are in Year 8'}[noun]
        prompt = f'{frac(a, d)} {tmpl.format(n=qty)} {verb}. How many {noun} is that?'
        body = ''; ans = f'{val} {noun}'
    else:
        unit_ = rng.choice(['', ' kg', ' m', ' L', ''])
        if rng.random() < 0.3:
            body = big(f'{frac(a, d)} of ${qty}'); ans = f'${val}'
        else:
            body = big(f'{frac(a, d)} of {qty}{unit_}'); ans = f'{val}{unit_}'
        prompt = 'Calculate.'
    return Q(skill='n_fracq', outcome='MA4-FRC-C-01', ncm='NCM 7 §4.05', box='F', prompt=prompt, body=body, answer=ans,
             key=f'fracq-{a}-{d}-{qty}', box_text='Fraction of a quantity = fraction × quantity',
             box_gap=f'Fraction of a quantity = fraction {gap(14)} quantity', box_name='fraction of a quantity')


def n_pctq(rng, reasoning=False):
    while True:
        p = rng.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 90, 12])
        qty = rng.choice([20, 40, 50, 60, 80, 120, 140, 160, 200, 240, 300, 350, 400, 45, 75, 90])
        val = F(p * qty, 100)
        if val.denominator == 1:
            break
    unit_ = rng.choice(['$', ' kg', ' m', ' L', ' km', '$'])
    if unit_ == '$':
        s = f'{p}% of ${qty}'; ans = f'${val}'
    else:
        s = f'{p}% of {qty}{unit_}'; ans = f'{val}{unit_}'
    return Q(skill='n_pctq', outcome='MA4-FRC-C-01', ncm='NCM 7 §4.11', box='F', prompt='Calculate.', body=big(s), answer=ans,
             key=f'pctq-{p}-{qty}-{unit_}', box_text='Percentage of a quantity = percentage ÷ 100 × quantity',
             box_gap=f'Percentage of a quantity = percentage ÷ {gap(18)} × quantity', box_name='percentage of a quantity')


def n_pctof(rng, reasoning=False):
    while True:
        whole = rng.choice([10, 20, 25, 40, 50, 16, 24, 30, 60, 80, 12, 35, 45, 200])
        part = rng.randrange(1, whole)
        pct = F(part * 100, whole)
        if pct.denominator == 1:
            break
    ctx = rng.choice(['plain', 'quiz', 'goals', 'games'])
    if ctx == 'plain':
        prompt = 'Write as a percentage.'; body = big(f'{part} out of {whole}')
    elif ctx == 'quiz':
        name = rng.choice(['Mia', 'Noah', 'Priya', 'Leo', 'Zoe', 'Theo'])
        prompt = f'{name} scored {part} out of {whole} on a quiz. Write this as a percentage.'; body = ''
    elif ctx == 'goals':
        prompt = f'A netball shooter scored {part} goals from {whole} shots. What percentage of the shots were goals?'; body = ''
    else:
        prompt = f'The Kingscliff touch footy team won {part} of its {whole} games. What percentage of its games did it win?'; body = ''
    return Q(skill='n_pctof', outcome='MA4-FRC-C-01', ncm='NCM 7 §4.12', box='F', prompt=prompt, body=body,
             answer=f'{pct}%', key=f'pctof-{part}-{whole}',
             box_text='Percentage = part ÷ whole × 100%', box_gap=f'Percentage = part ÷ whole × {gap(22)}',
             box_name='writing one amount as a percentage of another')


def n_fdp(rng, reasoning=False):
    kind = rng.choice(['f2d', 'd2p', 'p2f', 'd2f', 'p2d', 'f2p'])
    if kind == 'f2d':
        a, d = rng.choice([(1, 4), (3, 4), (2, 5), (3, 5), (1, 8), (3, 8), (7, 20), (9, 25), (1, 20), (4, 5)])
        prompt = 'Write as a decimal.'; body = big(frac(a, d)); ans = num(a / d)
        rule = 'Fraction to decimal: numerator ÷ denominator'; rg = f'Fraction to decimal: numerator ÷ {gap(32)}'
        name = 'fraction to decimal'
    elif kind == 'd2p':
        x = rng.choice(['0.35', '0.08', '0.6', '0.72', '0.125', '0.4', '0.05', '1.2'])
        prompt = 'Write as a percentage.'; body = big(x); ans = f'{num(round(float(x)*100, 3))}%'
        rule = 'Decimal to percentage: decimal × 100%'; rg = f'Decimal to percentage: decimal × {gap(22)}'
        name = 'decimal to percentage'
    elif kind == 'p2f':
        p = rng.choice([45, 64, 15, 80, 35, 12, 75, 24, 60, 5])
        prompt = 'Write as a fraction in simplest form.'; body = big(f'{p}%'); ans = fr(F(p, 100))
        rule = 'Percentage to fraction: write over 100, then simplify'; rg = f'Percentage to fraction: write over {gap(18)}, then simplify'
        name = 'percentage to fraction'
    elif kind == 'd2f':
        x = rng.choice(['0.6', '0.35', '0.48', '0.25', '0.8', '0.15', '0.04'])
        prompt = 'Write as a fraction in simplest form.'; body = big(x); ans = fr(F(x))
        rule = 'Decimal to fraction: write over 10, 100 or 1000, then simplify'
        rg = f'Decimal to fraction: write over 10, 100 or 1000, then {gap(26)}'
        name = 'decimal to fraction'
    elif kind == 'p2d':
        p = rng.choice([7, 35, 64, 3, 120, 50, 8])
        prompt = 'Write as a decimal.'; body = big(f'{p}%'); ans = num(p / 100)
        rule = 'Percentage to decimal: percentage ÷ 100'; rg = f'Percentage to decimal: percentage ÷ {gap(18)}'
        name = 'percentage to decimal'
    else:
        a, d = rng.choice([(2, 5), (9, 10), (7, 20), (3, 25), (1, 4), (3, 50), (11, 20), (3, 4)])
        prompt = 'Write as a percentage.'; body = big(frac(a, d)); ans = f'{num(a*100/d)}%'
        rule = 'Fraction to percentage: fraction × 100%'; rg = f'Fraction to percentage: fraction × {gap(22)}'
        name = 'fraction to percentage'
    key = f'fdp-{kind}-{body}'
    return Q(skill='n_fdp', outcome='MA4-FRC-C-01', ncm='NCM 7 §4.10, 7.02', prompt=prompt, body=body, answer=ans,
             key=key, box_text=rule, box_gap=rg, box_name=name)


def n_p10(rng, reasoning=False):
    x = rng.choice(['0.64', '4.8', '12.4', '0.038', '5.19', '0.25', '7.5', '56.2', '3.06', '0.9', '450', '82', '9', '3060', '260'])
    op = rng.choice(['×', '÷'])
    p = rng.choice([10, 100, 1000])
    val = float(x) * p if op == '×' else float(x) / p
    s = f'{x} {op} {p}'
    return Q(skill='n_p10', outcome='MA4-FRC-C-01', ncm='NCM 7 §7.05', prompt='Calculate.', body=big(s),
             answer=num(round(val, 6)), key=f'p10-{s}',
             box_text='× 10, 100, 1000: digits move 1, 2, 3 places left. ÷: they move right',
             box_gap=f'× 10, 100, 1000: digits move 1, 2, 3 places {gap(22)}. ÷: they move right',
             box_name='multiplying and dividing by 10, 100, 1000')


def n_fracop(rng, reasoning=False):
    kind = rng.choice(['addsame', 'subsame', 'addhalf', 'mul'])
    if kind == 'addsame':
        d = rng.choice([5, 7, 8, 9, 11]); a = rng.randrange(1, d - 1); b = rng.randrange(1, d - a)
        s = f'{frac(a, d)} + {frac(b, d)}'; val = F(a + b, d)
        rule = 'Same denominators: add or subtract the numerators, then simplify'
    elif kind == 'subsame':
        d = rng.choice([5, 7, 8, 9, 10]); a = rng.randrange(2, d); b = rng.randrange(1, a)
        s = f'{frac(a, d)} {MINUS} {frac(b, d)}'; val = F(a - b, d)
        rule = 'Same denominators: add or subtract the numerators, then simplify'
    elif kind == 'addhalf':
        a, b, d2 = rng.choice([(1, 1, 4), (1, 3, 8), (1, 1, 6), (1, 3, 10), (1, 1, 8)])
        s = f'{frac(1, 2)} + {frac(b, d2)}'; val = F(1, 2) + F(b, d2)
        rule = 'Make the denominators the same, then add the numerators'
    else:
        a, b, c, d = rng.choice([(2, 3, 3, 4), (1, 2, 4, 5), (3, 5, 5, 6), (2, 5, 1, 4), (3, 4, 2, 9), (1, 3, 3, 7)])
        s = f'{frac(a, b)} × {frac(c, d)}'; val = F(a, b) * F(c, d)
        rule = 'Multiply the numerators and multiply the denominators, then simplify'
    rg = rule.replace('simplify', gap(26)) if 'simplify' in rule else rule.replace('same', gap(20))
    return Q(skill='n_fracop', outcome='MA4-FRC-C-01', ncm='NCM 7 §4.03–4.06', prompt='Calculate. Give your answer in simplest form.',
             body=big(s), answer=fr(val), key=f'fracop-{s}', box_text=rule, box_gap=rg,
             box_name='adding, subtracting and multiplying fractions')


def n_dec(rng, reasoning=False):
    kind = rng.choice(['add', 'sub', 'mul', 'div'])
    if kind == 'add':
        a, b = rng.choice([('3.6', '2.45'), ('12.5', '4.75'), ('0.8', '1.35'), ('6.25', '3.9'), ('4.07', '2.6')])
        val = round(float(a) + float(b), 4); s = f'{a} + {b}'; rule = 'Line up the decimal points, then add'
    elif kind == 'sub':
        a, b = rng.choice([('7.2', '3.5'), ('10', '4.65'), ('5.4', '2.08'), ('8.3', '0.75')])
        val = round(float(a) - float(b), 4); s = f'{a} {MINUS} {b}'; rule = 'Line up the decimal points, then subtract'
    elif kind == 'mul':
        a, b = rng.choice([('0.6', '0.3'), ('1.2', '4'), ('0.5', '0.7'), ('2.5', '3'), ('0.04', '6')])
        val = round(float(a) * float(b), 4); s = f'{a} × {b}'
        rule = 'Ignore the points, multiply, then count the decimal places back in'
    else:
        a, b = rng.choice([('4.8', '4'), ('7.5', '5'), ('9.6', '3'), ('1.44', '12'), ('6.3', '7')])
        val = round(float(a) / float(b), 4); s = f'{a} ÷ {b}'; rule = 'Divide as normal; keep the decimal point in line'
    rg = rule.replace('decimal points', f'decimal {gap(24)}') if 'decimal points' in rule else rule.replace('decimal places', f'{gap(26)} places').replace('decimal point', f'decimal {gap(22)}')
    return Q(skill='n_dec', outcome='MA4-FRC-C-01', ncm='NCM 7 §7.03–7.07', prompt='Calculate.', body=big(s),
             answer=num(val), key=f'dec-{s}', box_text=rule, box_gap=rg, box_name='operations with decimals')


def n_round(rng, reasoning=False):
    x = rng.choice(['3.4672', '12.358', '0.7349', '8.0952', '5.6618', '24.9071', '1.0449', '7.385'])
    dp = rng.choice([1, 2])
    from decimal import Decimal, ROUND_HALF_UP
    val = Decimal(x).quantize(Decimal('1.' + '0' * dp), rounding=ROUND_HALF_UP)
    return Q(skill='n_round', outcome='MA4-FRC-C-01', ncm='NCM 7 §7.10',
             prompt=f'Round to {dp} decimal place{"s" if dp > 1 else ""}.', body=big(x), answer=str(val), key=f'round-{x}-{dp}',
             box_text='Look at the next digit: 5 or more, round up; 4 or less, leave it',
             box_gap=f'Look at the next digit: {gap(14)} or more, round up; 4 or less, leave it', box_name='rounding decimals')


def n_recur(rng, reasoning=False):
    a, d, ans = rng.choice([(1, 3, '0.' + rec('3')), (2, 3, '0.' + rec('6')), (1, 9, '0.' + rec('1')), (4, 9, '0.' + rec('4')),
                            (5, 6, '0.8' + rec('3')), (1, 6, '0.1' + rec('6')), (7, 9, '0.' + rec('7')), (2, 9, '0.' + rec('2'))])
    return Q(skill='n_recur', outcome='MA4-FRC-C-01', ncm='NCM 7 §7.09',
             prompt='Write as a recurring decimal (use dot notation).', body=big(frac(a, d)), answer=ans, key=f'recur-{a}-{d}',
             box_text='Numerator ÷ denominator; put a dot over each repeating digit',
             box_gap=f'Numerator ÷ denominator; put a {gap(18)} over each repeating digit',
             box_name='recurring decimals')


NUM_SKILLS = {
    'n_ooo': n_ooo, 'n_int': n_int, 'n_pow': n_pow, 'n_root': n_root, 'n_prime': n_prime,
    'n_fracq': n_fracq, 'n_pctq': n_pctq, 'n_pctof': n_pctof, 'n_fdp': n_fdp, 'n_p10': n_p10,
    'n_fracop': n_fracop, 'n_dec': n_dec, 'n_round': n_round, 'n_recur': n_recur,
}
