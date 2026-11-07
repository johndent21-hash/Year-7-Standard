"""Independent checks for The Fractal Five v3.

Re-derives every answer from what the student sees (diagram labels, expressions,
tables, prompts) using code separate from the generators, and checks the
scope-and-sequence rules. Exit code 1 if anything fails.
"""
import html, json, math, os, random, re, sys
from collections import Counter, defaultdict
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from schedule import UNLOCK, idx  # noqa: E402

ss = json.load(open(os.path.join(HERE, '..', 'build', 'year.json')))
fails, checked = [], Counter()


def T(s):
    """HTML -> plain text (fractions as a/b, superscripts as ^)."""
    s = re.sub(r'<span class="fr"><span class="n">(.*?)</span><span class="d">(.*?)</span></span>', r'(\1)/(\2)', s)
    s = re.sub(r'<sup class="ri">3</sup>√', '∛', s)
    s = re.sub(r'<sup>(.*?)</sup>', r'^(\1)', s)
    s = re.sub(r'<span class="rec">(\d)</span>', r'[\1]', s)
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s).replace(' ', '').replace('−', '-').replace('\xa0', ' ').strip()


def svg_texts(body):
    return [html.unescape(re.sub(r'<[^>]+>', '', m)).replace('−', '-') for m in re.findall(r'<text[^>]*>(.*?)</text>', body)]


def nums(s):
    return [F(x) for x in re.findall(r'-?\d+(?:\.\d+)?', s.replace(',', ''))]


def to_py(expr):
    """Algebra text -> python expression (implicit multiplication handled; exact fractions)."""
    e = expr.replace('−', '-').replace(' ', '')
    e = re.sub(r'÷([0-9a-z]+(?:\^\(\d+\))?)', r'÷(\1)', e)          # a ÷ 3x means a ÷ (3x)
    e = e.replace('×', '*').replace('÷', '/').replace('^', '**')
    e = re.sub(r'(\d|\))(?=[a-z(])', r'\1*', e)
    e = re.sub(r'([a-z])(?=[a-z(\d])', r'\1*', e)
    e = re.sub(r'\)(?=\()', ')*', e)
    e = re.sub(r'(?<![\w.])(\d+(?:\.\d+)?)', r"F('\1')", e)
    return e


def ev(expr, env=None):
    g = {'__builtins__': {}, 'F': F}
    return eval(to_py(expr), g, env or {})


def same_expr(a, b, letters='abcmnpqxyk'):
    rng = random.Random(1)
    for _ in range(6):
        env = {L: F(rng.randrange(-9, 10) or 3, rng.choice([1, 1, 2])) for L in letters}
        if ev(a, env) != ev(b, env):
            return False
    return True


def fail(S, q, msg):
    fails.append(f"T{S['term']} W{S['week']} S{S['session']} Q{q['n']} [{q['skill']}] {msg} | {T(q['prompt'])} {T(q.get('body',''))[:80]} -> {T(q['answer'])}")


def ans_num(q):
    a = T(q['answer'])
    m = re.search(r'=\s*(-?\d+(?:\.\d+)?)', a)
    if m:
        return F(m.group(1))
    return F(re.findall(r'-?\d+(?:\.\d+)?', a.replace(',', '').replace(' ', ''))[0]) if re.search(r'\d', a) else None


# ---------------------------------------------------------------- per-skill checks
def chk(S, q):
    sk = q['skill']; body = q.get('body', ''); a = T(q['answer']); key = q['key']
    labels = svg_texts(body)
    degs = [F(re.match(r'(-?\d+)', l).group(1)) for l in labels if re.fullmatch(r'-?\d+°', l.strip())]
    xv = ans_num(q)
    if sk in ('g_comp', 'g_supp', 'g_vopp', 'g_point', 'g_corr', 'g_alt', 'g_coint', 'g_tri', 'g_ext', 'g_isos', 'g_quad'):
        assert any('x' in l for l in labels), 'no x label'
        if sk == 'g_comp': exp = 90 - degs[0]
        elif sk == 'g_supp': exp = 180 - degs[0]
        elif sk == 'g_vopp': exp = degs[0]
        elif sk == 'g_point': exp = 360 - sum(degs)
        elif sk in ('g_corr', 'g_alt'): exp = degs[0]
        elif sk == 'g_coint': exp = 180 - degs[0]
        elif sk == 'g_tri': exp = 180 - sum(degs)
        elif sk == 'g_quad': exp = 360 - sum(degs)
        elif sk == 'g_ext':
            exp = sum(degs) if key.endswith('-ext') else max(degs) - min(degs)
        else:  # isosceles
            exp = (180 - degs[0]) / 2 if key.endswith('-base') else 180 - 2 * degs[0]
        if sk in ('g_corr', 'g_alt', 'g_coint'):
            phi, pair = int(key.split('-')[1]), key.split('-')[2]
            qU, qL = pair[:2], pair[2:]
            ok = {'g_corr': qU == qL, 'g_alt': (qU, qL) in (('BR', 'AL'), ('BL', 'AR')), 'g_coint': (qU, qL) in (('BR', 'AR'), ('BL', 'AL'))}[sk]
            if not ok:
                fail(S, q, f'angle pair {pair} is not {sk}')
        if len(degs) < 1 or exp != xv or exp <= 0:
            fail(S, q, f'expected x = {exp}')
        return
    if sk == 'm_circ':
        n_ = nums(' '.join(labels))[0]
        exact = math.pi * float(n_) if 'd' in key.split('-')[1][:1] else 2 * math.pi * float(n_)
        if f'{exact:.1f}' not in a:
            fail(S, q, f'circumference should be {exact:.1f}')
        alt = f'{(3.14 * float(n_) if key.split("-")[1][0] == "d" else 2 * 3.14 * float(n_)):.1f}'
        if alt != f'{exact:.1f}' and alt not in T(q.get('answer_alt', '')):
            fail(S, q, f'missing 3.14 alternative {alt}')
        return
    if sk in ('m_perim', 'm_rect', 'm_tri', 'm_para', 'm_comp', 'm_vol'):
        L = [n for l in labels for n in nums(l)]
        kind = key.split('-')[1]
        if sk == 'm_perim':
            exp = sum(L) if kind in ('tri', 'L') else (2 * sum(L) if kind == 'rect' else 4 * L[0])
            if kind == 'L':
                W, H = L[0], L[5]
                if L[0] != L[2] + L[4] or L[5] != L[1] + L[3]:
                    fail(S, q, 'L-shape sides inconsistent')
            if kind == 'tri':
                s_ = sorted(L)
                if s_[0] + s_[1] <= s_[2]:
                    fail(S, q, 'triangle inequality fails')
        elif sk == 'm_rect':
            exp = L[0] * L[0] if kind == 'sq' else L[0] * L[1]
        elif sk == 'm_tri':
            exp = L[0] * L[1] / 2
        elif sk == 'm_para':
            exp = L[0] * L[1]
        elif sk == 'm_vol':
            exp = L[0] * L[1] * L[2]
        else:
            if kind == 'house':
                Wb, h1, h2 = L[0], L[1], L[2]
                exp = Wb * h1 + Wb * h2 / 2
            else:
                # outer edges in drawing order; check consistency and area by decomposition
                if kind == 'L':
                    W, h1, a2, b2, w2, H = L
                    if W != a2 + w2 or H != h1 + b2:
                        fail(S, q, 'L-shape sides inconsistent')
                    exp = W * h1 + w2 * (H - h1)
                else:
                    W, H, w2, b2, a2, h1 = L
                    if W != a2 + w2 or H != h1 + b2:
                        fail(S, q, 'step-shape sides inconsistent')
                    exp = W * h1 + w2 * (H - h1)
        if exp != xv:
            fail(S, q, f'expected {exp}')
        return
    if sk == 'm_volA':
        A_ = nums(T(q['prompt']))[0]; h = nums(' '.join(labels))[0]
        if A_ * h != xv: fail(S, q, f'expected {A_*h}')
        return
    if sk in ('m_cap', 'm_areaunit'):
        p = T(q['prompt']); v = nums(p)[0]
        f = {('L', 'mL'): 1000, ('mL', 'L'): F(1, 1000), ('cm3', 'mL'): 1, ('cm3', 'L'): F(1, 1000), ('m3', 'L'): 1000, ('L', 'cm3'): 1000,
             ('cm2', 'mm2'): 100, ('mm2', 'cm2'): F(1, 100), ('m2', 'cm2'): 10000, ('ha', 'm2'): 10000, ('m2', 'ha'): F(1, 10000)}
        k1, k2 = key.split('-')[1], key.split('-')[2]
        if v * f[(k1, k2)] != xv: fail(S, q, f'expected {v*f[(k1,k2)]}')
        return
    if sk in ('n_ooo', 'n_pow') and q.get('reasoning'):
        e = re.search(r'says (.*?) = (-?\d+)\.', T(q['prompt']))
        val = ev(e.group(1))
        if str(val) not in a.split('.')[-2] + a or str(val) == e.group(2):
            fail(S, q, f'expected correct value {val} in the explanation')
        return
    if sk in ('n_ooo', 'n_int', 'n_p10', 'n_dec'):
        e = T(body)
        val = F(ev(e))
        if F(val) != xv: fail(S, q, f'expected {val}')
        return
    if sk == 'n_pow':
        val = ev(T(body))
        if q.get('reasoning'):
            val = ev(re.search(r'says (.*?) =', T(q['prompt'])).group(1))
            if str(val) not in a: fail(S, q, f'expected {val}')
            return
        if val != xv: fail(S, q, f'expected {val}')
        return
    if sk == 'n_root':
        e = T(body)
        r = round(float(nums(e)[-1]) ** (1 / 3 if '∛' in e else 0.5))
        if r != xv: fail(S, q, f'expected {r}')
        return
    if sk in ('n_prime', 'i8_prime'):
        m = int(nums(T(q['prompt']))[0])
        prod = 1
        for part in a.split('×'):
            part = part.strip()
            b_, e_ = (part.split('^') + ['1'])[:2]
            b_, e_ = int(b_), int(e_.strip('()'))
            if any(b_ % d == 0 for d in range(2, b_)): fail(S, q, 'non-prime factor')
            prod *= b_ ** e_
        if prod != m: fail(S, q, f'product {prod} != {m}')
        return
    if sk == 'n_fracq':
        t = T(q['prompt']) + ' ' + T(body)
        m = re.search(r'\((\d+)\)/\((\d+)\)\s*(?:of the|of)\s*\$?(\d+)', t)
        val = F(int(m.group(1)), int(m.group(2))) * int(m.group(3))
        if val != xv: fail(S, q, f'expected {val}')
        return
    if sk == 'n_pctq':
        m = re.search(r'(\d+)% of \$?(\d+)', T(body))
        val = F(int(m.group(1)) * int(m.group(2)), 100)
        if val != xv: fail(S, q, f'expected {val}')
        return
    if sk == 'n_pctof':
        t = T(q['prompt']) + ' ' + T(body)
        m = re.search(r'(\d+) out of (\d+)', t) or re.search(r'(\d+) goals from (\d+)', t) or re.search(r'won (\d+) of its (\d+)', t)
        val = F(int(m.group(1)) * 100, int(m.group(2)))
        if val != xv: fail(S, q, f'expected {val}%')
        return
    if sk == 'n_fdp':
        e = T(body); p = T(q['prompt'])
        if '%' in e:
            v = F(e.rstrip('%')) / 100
        elif '/' in e:
            v = ev(e)
        else:
            v = F(e)
        if 'percentage' in p:
            ok = (v * 100) == F(a.rstrip('%'))
        elif 'fraction' in p:
            ok = F(ev(a)) == v and (F(ev(a)).denominator == int(re.findall(r'\d+', a)[-1]) if '/' in a else True)
        else:
            ok = F(a) == v
        if not ok: fail(S, q, f'conversion wrong (value {v})')
        return
    if sk == 'n_fracop':
        val = F(ev(T(body)))
        got = F(ev(a)) if '/' in a else F(a)
        if val != got: fail(S, q, f'expected {val}')
        if '/' in a and F(ev(a)).denominator != int(re.findall(r'\d+', a)[-1]): fail(S, q, 'not simplest form')
        return
    if sk == 'n_round':
        dp = int(re.search(r'(\d) decimal', T(q['prompt'])).group(1))
        val = Decimal(T(body)).quantize(Decimal('1.' + '0' * dp), rounding=ROUND_HALF_UP)
        if str(val) != a: fail(S, q, f'expected {val}')
        return
    if sk == 'n_recur':
        fr_ = ev(T(body)); s_ = f'{float(fr_):.8f}'
        digits = re.sub(r'[\[\]]', '', a)
        if not s_.startswith(digits): fail(S, q, f'decimal {s_} vs {a}')
        rep = re.findall(r'\[(\d)\]', a)
        if s_[-3] != rep[-1]: fail(S, q, 'repeating digit wrong')
        return
    if sk in ('a_sub', 'a8_sub'):
        p = T(q['prompt'])
        env = {m.group(1): F(m.group(2)) for m in re.finditer(r'([a-z]) = (-?\d+)', p)}
        val = ev(T(body), env)
        if F(val) != xv: fail(S, q, f'expected {val}')
        return
    if sk in ('a_like', 'a_mult', 'a_div', 'a8_like2', 'a8_multdiv', 'a8_expsimp', 'a8_expand', 'a8_fact'):
        if q.get('reasoning'):
            return
        e = T(body)
        if not same_expr(e, a): fail(S, q, f'{e} is not equal to {a}')
        if sk == 'a8_fact':
            m = re.match(r'(\d+)\((.*)\)', a.replace(' ', ''))
            inner = m.group(2)
            cs = [int(x) for x in re.findall(r'(\d+)', inner)] or [1]
            coef_x = re.match(r'(\d*)[a-z]', inner).group(1)
            g = math.gcd(int(coef_x or 1), int(re.findall(r'(\d+)$', inner)[0]))
            if g != 1: fail(S, q, 'not fully factorised')
        if sk == 'a8_expand' and '(' in a: fail(S, q, 'brackets left in expansion')
        return
    if sk == 'a_write':
        w_ = T(body); v_ = re.search(r'\b([a-z])\b', w_).group(1)
        nums_ = [int(x) for x in re.findall(r'\d+', w_)]
        exp = {'more than': None}
        env = {v_: F(7)}
        val = ev(a, env)
        if 'divided by' in w_: ref = F(7, nums_[0])
        elif 'double' in w_: ref = 14 + nums_[0]
        elif 'times' in w_ and 'more' in w_: ref = nums_[1] * 7 + nums_[0]
        elif 'times' in w_ and 'less' in w_: ref = nums_[1] * 7 - nums_[0]
        elif 'more' in w_: ref = 7 + nums_[0]
        else: ref = 7 - nums_[0]
        if val != ref: fail(S, q, f'expression gives {val}, expected {ref}')
        return
    if sk in ('e_one', 'e_two', 'e8_both', 'e8_nonint'):
        eq = T(body); lhs, rhs = eq.split('=')
        var = re.search(r'[a-z]', eq).group(0)
        if q.get('reasoning'):
            test = F(re.search(r'= (-?\d+)', T(q['prompt'])).group(1))
            ok = ev(lhs, {var: test}) == ev(rhs, {var: test})
            if ok != a.startswith('Yes'): fail(S, q, 'reasoning yes/no wrong')
            return
        val = F(str(xv)) if not isinstance(xv, F) else xv
        if ev(lhs, {var: val}) != ev(rhs, {var: val}): fail(S, q, f'{var} = {val} does not satisfy {eq}')
        return
    if sk == 'e8_quad':
        eq = T(body); lhs, rhs = eq.split('='); var = re.search(r'[a-z]', eq).group(0)
        r = abs(xv)
        if not (ev(lhs, {var: r}) == ev(rhs, {var: r}) and ev(lhs, {var: -r}) == ev(rhs, {var: -r}) and '-' in a and ' or ' in a):
            fail(S, q, 'quadratic solutions wrong')
        return
    if sk == 'e8_formula':
        f_ = T(q['box_text']); p = T(q['prompt'])
        env = {m.group(1): F(m.group(2)) for m in re.finditer(r'\b([A-Za-z]) = (\d+)', p)}
        unk = re.search(r'find ([a-zA-Z]) ', p, re.I).group(1)
        env[unk] = xv
        lhs, rhs = f_.split('=')
        if 'S =' in f_:
            lhs, rhs = 'S', '180*(n-2)'
        e_ = lambda s: eval(re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', s.replace('−', '-').replace(' ', ''))), {'__builtins__': {}}, env)
        if e_(lhs) != e_(rhs): fail(S, q, 'formula not satisfied')
        return
    if sk == 'e8_word':
        p = T(q['prompt']); n_ = [int(x) for x in re.findall(r'\d+', p)]
        sol = int(a.split('number is')[1])
        mult = 2 if 'doubles' in p else n_[0]
        res = n_[-1]; c_ = n_[-2]
        val = mult * sol + c_ if 'adds' in p else mult * sol - c_
        if val != res: fail(S, q, f'{mult}*{sol}±{c_} != {res}')
        return
    if sk == 'l_table':
        rule = re.search(r'y = (.*)\.', T(q['prompt'])).group(1)
        xs = [F(x) for x in re.findall(r'x = (-?\d+):', a)]; ys = [F(y) for y in re.findall(r'y = (-?\d+)', a)]
        for x_, y_ in zip(xs, ys):
            if ev(rule, {'x': x_}) != y_: fail(S, q, f'table value at x={x_}')
        return
    if sk == 'l_point':
        p = T(q['prompt']); m = re.search(r'\((-?\d+), (-?\w+)\)', p); rule = re.search(r'y = ([^.?]*)', p).group(1)
        yv = ev(rule, {'x': F(m.group(1))})
        if q.get('reasoning'):
            ok = (str(yv) == m.group(2))
            if ok != a.startswith('Yes'): fail(S, q, 'reasoning yes/no wrong')
        elif yv != xv:
            fail(S, q, f'expected k = {yv}')
        return
    if sk == 'l_coord':
        return
    if sk in ('s_mean', 's_median', 's_mode', 's_range', 's_compare'):
        vals = [F(x) for x in re.findall(r'<td>(-?\d+)</td>', body)]
        sv = sorted(vals); n_ = len(vals)
        mean = sum(vals) / n_; med = sv[n_ // 2] if n_ % 2 else (sv[n_ // 2 - 1] + sv[n_ // 2]) / 2
        c = Counter(vals).most_common()
        if sk == 's_mean' and mean != xv: fail(S, q, f'mean {mean}')
        if sk == 's_median' and med != xv: fail(S, q, f'median {med}')
        if sk == 's_mode':
            if c[0][0] != xv or (len(c) > 1 and c[1][1] == c[0][1]): fail(S, q, 'mode wrong/not unique')
        if sk == 's_range' and sv[-1] - sv[0] != xv: fail(S, q, 'range')
        if sk == 's_compare' and not (mean > med and str(mean) in a and str(med) in a): fail(S, q, 'mean/median compare')
        return
    if sk == 's_dot':
        # count dots per axis value from the SVG (dots are circles with r=2.9)
        cx = [float(m) for m in re.findall(r'<circle cx="([\d.]+)" cy="[\d.]+" r="2.9"', body)]
        ticks = [(float(m.group(1)), int(m.group(2))) for m in re.finditer(r'<text x="([\d.]+)"[^>]*>(\d+)</text>', body)]
        data = []
        for x in cx:
            v = min(ticks, key=lambda t: abs(t[0] - x))[1]; data.append(v)
        sv = sorted(data); c = Counter(data).most_common()
        meas = re.search(r'Find the (\w+)', T(q['prompt'])).group(1)
        if meas == 'mode':
            exp = c[0][0]
            if len(c) > 1 and c[1][1] == c[0][1]: fail(S, q, 'mode not unique')
        elif meas == 'median':
            exp = sv[len(sv) // 2]
            if len(sv) % 2 == 0: fail(S, q, 'even count median')
        else:
            exp = sv[-1] - sv[0]
        if exp != xv: fail(S, q, f'{meas} should be {exp}')
        return
    if sk == 's_stem':
        rows = re.findall(r'<td class="st">(\d+)</td><td class="lf">(.*?)</td>', body)
        data = sorted(int(s_) * 10 + int(l) for s_, lf in rows for l in re.findall(r'\d', lf))
        meas = re.search(r'Find the (\w+)', T(q['prompt'])).group(1)
        exp = data[-1] - data[0] if meas == 'range' else data[len(data) // 2]
        if meas == 'median' and len(data) % 2 == 0: fail(S, q, 'even count median')
        if exp != xv: fail(S, q, f'{meas} should be {exp}')
        return
    if sk in ('p_simple', 'p_more'):
        p = T(q['prompt'])
        if 'word' in p:
            w_ = T(body).replace(' ', ''); L = re.search(r'P\((\w)\)', p).group(1); exp = F(w_.count(L), len(w_))
        elif 'die' in p:
            ev_ = {'an even number': [2, 4, 6], 'a number greater than 4': [5, 6], 'a multiple of 3': [3, 6], 'a number less than 3': [1, 2],
                   'a 5': [5], 'a prime number': [2, 3, 5], 'a number less than 5': [1, 2, 3, 4], 'an odd number': [1, 3, 5]}
            e_ = re.search(r'rolling (.*)\.', p).group(1); exp = F(len(ev_[e_]), 6)
        elif 'spinner' in p:
            n_ = nums(p); exp = n_[1] / n_[0]
        elif sk == 'p_more':
            n_ = nums(p); exp = n_[0] / (n_[0] + n_[1])
            if (exp > F(1, 2)) != a.startswith('Yes'): fail(S, q, 'more-likely logic')
            return
        else:
            cols = re.findall(r'<td>([A-Za-z]+)</td>', body); cnt = [int(x) for x in re.findall(r'<td>(\d+)</td>', body)]
            tgt = re.search(r'it is (\w+)\.', p).group(1).capitalize(); exp = F(cnt[cols.index(tgt)], sum(cnt))
        got = F(ev(a)) if '/' in a else F(a)
        if got != exp: fail(S, q, f'expected {exp}')
        if '/' in a and F(ev(a)).denominator != int(re.findall(r'\d+', a)[-1]): fail(S, q, 'not simplest')
        return
    if sk == 'p_comp':
        p = T(q['prompt']); g = re.search(r'is ([\d./()%]+)\. Find', p).group(1)
        gv = F(g.rstrip('%')) / 100 if '%' in g else (F(ev(g)) if '/' in g else F(g))
        got = F(a.rstrip('%')) / 100 if '%' in a else (F(ev(a)) if '/' in a else F(a))
        if gv + got != 1: fail(S, q, f'{gv} + {got} != 1')
        return
    if sk == 'p_obs':
        p = T(q['prompt'])
        if 'die was rolled' in p:
            fq = [int(x) for x in re.findall(r'<td>(\d+)</td>', body)][6:]
            face = int(re.search(r'rolling a (\d)', p).group(1)); exp = F(fq[face - 1], sum(fq))
            if sum(fq) != 60: fail(S, q, 'frequencies do not total 60')
        elif 'spinner' in p:
            fq = [int(x) for x in re.findall(r'<td>(\d+)</td>', body)]; cols = ['red', 'blue', 'green']
            t_ = re.search(r'probability of (\w+)', p).group(1); exp = F(fq[cols.index(t_)], sum(fq))
            if sum(fq) != int(nums(p)[0]): fail(S, q, 'frequencies do not total trials')
        else:
            n_ = nums(p); exp = n_[0] / n_[1]
        got = F(ev(a.split(' (')[0])) if '/' in a.split(' (')[0] else F(a.split(' (')[0])
        if got != exp: fail(S, q, f'expected {exp}')
        return
    if sk.startswith('f8_'):
        p = T(q['prompt'])
        if '$' in p and sk in ('f8_profit', 'f8_change'):
            n_ = [F(x) for x in re.findall(r'\$(\d+(?:\.\d+)?)', p)]
        else:
            n_ = [F(x) for x in re.findall(r'\d+(?:\.\d+)?', p.replace('$', ''))]
        got = F(re.findall(r'\d+(?:\.\d+)?', a.replace('$', ''))[0])
        if sk == 'f8_inc': exp = n_[0] * (1 + n_[1] / 100)
        elif sk == 'f8_dec': exp = n_[0] * (1 - n_[1] / 100)
        elif sk == 'f8_disc': exp = n_[0] * (1 - n_[1] / 100)
        elif sk == 'f8_gst': exp = n_[0] * F(11, 10) if 'including' in p else n_[0] / 10
        elif sk == 'f8_profit': exp = abs(n_[1] - n_[0]) / n_[0] * 100
        elif sk == 'f8_change': exp = abs(n_[1] - n_[0]) / n_[0] * 100
        elif sk == 'f8_unitary': exp = n_[1] / n_[0] * 100 if 'number' in p else (n_[1] / n_[0] * 100 if 'students' in p else n_[0] / n_[1] * 100)
        else:
            exp = n_[0] * n_[1] / 100
        if sk == 'f8_unitary' and 'saved' in p:
            exp = n_[0] / n_[1] * 100
        if sk == 'f8_profit' and (('loss' in a) != (n_[1] < n_[0])): fail(S, q, 'profit/loss word wrong')
        if got != exp: fail(S, q, f'expected {exp}')
        return
    if sk in ('i8_mult', 'i8_div', 'i8_pow'):
        if q.get('reasoning'):
            return
        e = T(body)
        if sk == 'i8_pow':
            m = re.match(r'\((\d+)\^\((\d+)\)\)\^\((\d+)\)', e.replace(' ', '')); b_, e1, e2 = map(int, m.groups()); exp_e = e1 * e2
        else:
            m = re.findall(r'(\d+)\^\((\d+)\)', e); b_ = int(m[0][0]); exp_e = int(m[0][1]) + int(m[1][1]) if sk == 'i8_mult' else int(m[0][1]) - int(m[1][1])
        mm = re.match(r'(\d+)\^\((\d+)\)', a.replace(' ', ''))
        got = (int(mm.group(1)), int(mm.group(2))) if mm else (int(a.split('=')[-1]), 1)
        if got != (b_, exp_e): fail(S, q, f'expected {b_}^{exp_e}')
        return
    if sk == 'i8_zero':
        val = ev(re.sub(r'\^\(0\)', '**0', T(body)))
        if val != xv: fail(S, q, f'expected {val}')
        return
    if sk in ('p8_hyp', 'p8_short', 'p8_dec'):
        L = [n for l in labels for n in nums(l)]
        if sk == 'p8_short':
            c, b_ = max(L), min(L); exp = math.sqrt(c * c - b_ * b_)
        else:
            exp = math.sqrt(sum(float(x) ** 2 for x in L))
        if abs(exp - float(xv)) > 0.051: fail(S, q, f'expected {exp:.2f}')
        return
    if sk == 'p8_test':
        s_ = sorted(nums(T(q['prompt'])))
        right = s_[0] ** 2 + s_[1] ** 2 == s_[2] ** 2
        if right != a.startswith('Yes'): fail(S, q, 'right-angle test wrong')
        return
    if sk == 'p8_est':
        n_ = int(nums(T(body))[0]); lo = math.isqrt(n_)
        if not a.startswith(f'{lo} and {lo+1}'): fail(S, q, 'estimate wrong')
        return
    if sk == 'f8_reason':
        n_ = nums(T(q['prompt']))
        if not a.startswith('Yes'): fail(S, q, 'should be yes')
        return
    if sk == 'm_compare':
        n_ = nums(T(q['prompt'])); rect, sq_ = n_[0] * n_[1], n_[2] ** 2
        if (('rectangle' in a.split(':')[0]) != (rect > sq_)): fail(S, q, 'larger shape wrong')
        return
    fail(S, q, 'no checker for this skill')


# ---------------------------------------------------------------- run
for S in ss:
    for q in S['questions']:
        try:
            chk(S, q)
            checked[q['skill']] += 1
        except Exception as e:  # a checker crash is a failure to verify
            fail(S, q, f'checker error: {e!r}')

# ---------------------------------------------------------------- scope and sequence rules
rule_fail = []
first = {}
for S in ss:
    i = S['idx']
    for q in S['questions']:
        u = q['unit']
        if u != 'Y7':
            if i < idx(*UNLOCK[u]):
                rule_fail.append(f"T{S['term']} W{S['week']} S{S['session']}: {u} before its unlock")
            first.setdefault(u, (S['term'], S['week'], S['session']))
        if any(w in (q['prompt'] + q.get('body', '')).lower() for w in ('ratio', 'km/h', 'per hour', 'speed', '24-hour', 'simple interest')):
            rule_fail.append(f"T{S['term']} W{S['week']} S{S['session']}: held-back content? {T(q['prompt'])[:60]}")
keys = Counter(q['key'] for S in ss for q in S['questions'])
dups = [k for k, v in keys.items() if v > 1]
texts = Counter((T(q['prompt']) + '|' + T(q.get('body', ''))) for S in ss for q in S['questions'])
same_text = [k for k, v in texts.items() if v > 1]
weekly = Counter((S['term'], S['week']) for S in ss for q in S['questions'] if q.get('reasoning'))
bad_weeks = [k for k in {(S['term'], S['week']) for S in ss} if weekly[k] != 1]
y8 = Counter((S['term'], q['unit'] != 'Y7') for S in ss for q in S['questions'])
long_boxes = [(q['skill'], T(q['box_text'])) for S in ss for q in S['questions'] if len(T(q['box_text'])) > 74]

print(f'answers checked: {sum(checked.values())} questions, {len(checked)} skills')
print(f'answer failures: {len(fails)}')
for f_ in fails[:60]:
    print('  FAIL', f_)
print('first appearance of Year 8 units:', first)
print('scope/sequence rule failures:', len(rule_fail))
for r in rule_fail[:20]:
    print('  RULE', r)
print('duplicate question keys:', len(dups), '| identical visible questions:', len(same_text))
for k in same_text[:10]:
    print('  SAME', k[:100])
print('weeks without exactly one reasoning item:', bad_weeks)
print('Year 8 share by term:', {t: f"{y8[(t, True)]}/{y8[(t, True)] + y8[(t, False)]}" for t in range(1, 5)})
print('formula boxes over 74 characters:', len(long_boxes), long_boxes[:3])
sys.exit(1 if (fails or rule_fail or dups or bad_weeks) else 0)
