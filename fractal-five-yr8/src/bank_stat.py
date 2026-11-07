"""Statistics and probability, Year 7 (NCM 7 Ch 10, Ch 11). MA4-DAT-C-02, MA4-PRO-C-01."""
from fractions import Fraction as F
from collections import Counter
from mathfmt import gap, frac, fr, num, MINUS
from svg import Fig, BLUE, INK

CONTEXTS = [('Goals', 'goal tallies', 'goals'), ('Tries', 'try tallies', 'tries'), ('Marks', 'test marks', 'marks'),
            ('cm', 'heights', 'cm'), ('°C', 'maximum temperatures', '°C'), ('Points', 'netball scores', 'points'),
            ('Waves', 'waves caught by nippers', 'waves'), ('Scores', 'scores', '')]


def Q(**kw):
    base = dict(year=7, unit='Y7', strand='S', calc=False, reasoning=False, body='', answer_alt='',
                labels=None, box='F')
    base.update(kw)
    return base


def data_table(head, vals):
    h = f'<th>{head}</th>' if head else ''
    return f'<table class="dt hz"><tr>{h}{"".join(f"<td>{num(x)}</td>" for x in vals)}</tr></table>'


def _scale(ctx, rng, k):
    head, desc, unit = ctx
    if head == 'cm':
        base = rng.randrange(140, 171); return [base + rng.randrange(-12, 13) for _ in range(k)]
    if head == '°C':
        base = rng.randrange(18, 28); return [base + rng.randrange(-5, 6) for _ in range(k)]
    if head == 'Marks':
        base = rng.randrange(50, 80); return [base + rng.randrange(-15, 16) for _ in range(k)]
    if head in ('Tries', 'Waves'):
        return [rng.randrange(0, 8) for _ in range(k)]
    return [rng.randrange(2, 20) for _ in range(k)]


def s_mean(rng, reasoning=False):
    while True:
        ctx = rng.choice(CONTEXTS); k = rng.choice([4, 5, 5, 6])
        vals = _scale(ctx, rng, k)
        if sum(vals) % k == 0 and len(set(vals)) > 2:
            break
    head, desc, unit = ctx
    m = sum(vals) // k
    u = f' {unit}' if unit in ('cm', '°C') else ''
    q = Q(skill='s_mean', outcome='MA4-DAT-C-02', ncm='NCM 7 §10.05', prompt=f'Find the mean of these {desc}.',
          body=data_table(head, vals), answer=f'{m}{u}', key=f'mean-{head}-{vals}',
          box_text='Mean = sum of scores ÷ number of scores', box_gap=f'Mean = sum of scores ÷ {gap(40)}',
          box_name='the mean')
    return q


def s_median(rng, reasoning=False):
    while True:
        ctx = rng.choice(CONTEXTS); k = rng.choice([5, 7, 6])
        vals = _scale(ctx, rng, k)
        sv = sorted(vals)
        med = F(sv[k // 2]) if k % 2 else F(sv[k // 2 - 1] + sv[k // 2], 2)
        if med.denominator == 1 and len(set(vals)) == k and sv != vals:
            break
    head, desc, unit = ctx
    u = f' {unit}' if unit in ('cm', '°C') else ''
    return Q(skill='s_median', outcome='MA4-DAT-C-02', ncm='NCM 7 §10.06', prompt=f'Find the median of these {desc}.',
             body=data_table(head, vals), answer=f'{num(med)}{u}', key=f'median-{head}-{vals}',
             box_text='Median = middle score when the scores are in order (2 middles: halfway)',
             box_gap=f'Median = middle score when the scores are in {gap(24)}', box_name='the median')


def s_mode(rng, reasoning=False):
    while True:
        k = rng.choice([7, 8, 9])
        vals = [rng.randrange(1, 10) for _ in range(k)]
        c = Counter(vals).most_common()
        if c[0][1] >= 3 and (len(c) == 1 or c[1][1] < c[0][1]):
            break
    return Q(skill='s_mode', outcome='MA4-DAT-C-02', ncm='NCM 7 §10.05', prompt='Find the mode of these scores.',
             body=data_table('Scores', vals), answer=str(c[0][0]), key=f'mode-{vals}',
             box_text='Mode = the most common score', box_gap=f'Mode = the most {gap(30)} score', box_name='the mode')


def s_range(rng, reasoning=False):
    ctx = rng.choice(CONTEXTS); k = rng.choice([5, 6])
    vals = _scale(ctx, rng, k)
    head, desc, unit = ctx
    u = f' {unit}' if unit in ('cm', '°C') else ''
    return Q(skill='s_range', outcome='MA4-DAT-C-02', ncm='NCM 7 §10.06', prompt=f'Find the range of these {desc}.',
             body=data_table(head, vals), answer=f'{max(vals) - min(vals)}{u}', key=f'range-{head}-{vals}',
             box_text='Range = highest score − lowest score', box_gap=f'Range = {gap(30)} score − lowest score',
             box_name='the range')


def dot_plot(counts, lo, hi, caption):
    f = Fig()
    f.line((lo - 0.6, 0), (hi + 0.6, 0), w=0.9, col=INK)
    for x in range(lo, hi + 1):
        f.line((x, 0), (x, -0.12), w=0.7, col=INK)
        f.label((x, -0.12), str(x), deg=-90, dist=6.5, size=8.2, col='#4a4741')
        for j in range(counts.get(x, 0)):
            f.dot((x, 0.42 + j * 0.62), 2.9, BLUE)
            f.ghost((x, 0.42 + j * 0.62 + 0.3))
    f.label(((lo + hi) / 2, -0.12), caption, deg=-90, dist=17, size=8, col='#8a857c')
    return f


def s_dot(rng, reasoning=False):
    while True:
        lo = rng.choice([0, 1]); hi = lo + rng.choice([5, 6])
        n = rng.randrange(9, 14)
        data = [rng.randrange(lo, hi + 1) for _ in range(n)]
        c = Counter(data)
        if max(c.values()) > 5:
            continue
        measure = rng.choice(['mode', 'median', 'range'])
        sv = sorted(data)
        if measure == 'mode':
            mc = c.most_common()
            if len(mc) > 1 and mc[1][1] == mc[0][1]:
                continue
            ans = mc[0][0]
        elif measure == 'median':
            if n % 2 == 0:
                continue
            ans = sv[n // 2]
        else:
            ans = max(data) - min(data)
        break
    caption, what = rng.choice([('Goals per game', 'goals a netball team scored in each game'),
                                ('Tries per game', 'tries a rugby league team scored in each game'),
                                ('Waves caught', 'waves each nipper caught in a session'),
                                ('Number of pets', 'number of pets each student in a class owns')])
    f = dot_plot(c, lo, hi, caption)
    box = {'mode': ('Mode = the most common score', f'Mode = the most {gap(30)} score', 'the mode'),
           'median': ('Median = middle score when the scores are in order', f'Median = middle score when the scores are in {gap(24)}', 'the median'),
           'range': ('Range = highest score − lowest score', f'Range = {gap(30)} score − lowest score', 'the range')}[measure]
    return Q(skill='s_dot', outcome='MA4-DAT-C-02', ncm='NCM 7 §10.03, 10.07',
             prompt=f'The dot plot shows the {what}. Find the {measure}.', body=f.svg(max_w=200, max_h=70),
             answer=str(ans), key=f'dot-{sorted(c.items())}-{measure}', box_text=box[0], box_gap=box[1], box_name=box[2])


def s_stem(rng, reasoning=False):
    while True:
        s0 = rng.randrange(1, 5); k = rng.choice([3, 3, 4])
        stems = list(range(s0, s0 + k))                       # consecutive stems, as in NCM 7 §10.04
        empty = rng.choice([None, None] + stems[1:-1])        # occasionally an empty middle stem
        leaves = {s: ([] if s == empty else sorted(rng.choices(range(0, 10), k=rng.randrange(2, 5)))) for s in stems}
        data = sorted(10 * s + l for s in stems for l in leaves[s])
        n = len(data)
        measure = rng.choice(['range', 'median'])
        if measure == 'median' and n % 2 == 0:
            continue
        ans = (data[-1] - data[0]) if measure == 'range' else data[n // 2]
        break
    rows = ''.join(f'<tr><td class="st">{s}</td><td class="lf">{"&nbsp;&nbsp;".join(map(str, leaves[s])) or "&nbsp;"}</td></tr>' for s in stems)
    body = f'<table class="stem">{rows}</table><div class="key">Key: {stems[0]} | {leaves[stems[0]][0]} = {10*stems[0]+leaves[stems[0]][0]}</div>'
    box = {'range': ('Range = highest score − lowest score', f'Range = {gap(30)} score − lowest score', 'the range'),
           'median': ('Median = middle score when the scores are in order', f'Median = middle score when the scores are in {gap(24)}', 'the median')}[measure]
    return Q(skill='s_stem', outcome='MA4-DAT-C-02', ncm='NCM 7 §10.04, 10.07',
             prompt=f'The stem-and-leaf plot shows the ages of people at a beach. Find the {measure}.', body=body,
             answer=str(ans), key=f'stem-{data}-{measure}', box_text=box[0], box_gap=box[1], box_name=box[2])


# ---------------------------------------------------------------- probability
P_RULE = 'P(E) = number of favourable outcomes ÷ total number of outcomes'
P_GAP = f'P(E) = number of favourable outcomes ÷ {gap(46)}'
WORDS = ['KINGSCLIFF', 'TWEED', 'NIPPERS', 'MATHEMATICS', 'BANANA', 'SUCCESS', 'CABARITA', 'PELICAN', 'DOLPHIN', 'SEAGULL']


def p_simple(rng, reasoning=False):
    kind = rng.choice(['bag', 'word', 'die', 'spinner'])
    if kind == 'bag':
        cols = rng.sample(['Red', 'Blue', 'Green', 'Yellow', 'White', 'Black'], rng.choice([2, 3]))
        cnt = [rng.randrange(1, 9) for _ in cols]
        tgt = rng.randrange(len(cols))
        p = F(cnt[tgt], sum(cnt))
        body = ('<table class="dt hz"><tr><th>Colour</th>' + ''.join(f'<td>{c}</td>' for c in cols) +
                '</tr><tr><th>Marbles</th>' + ''.join(f'<td>{n}</td>' for n in cnt) + '</tr></table>')
        prompt = f'One marble is chosen at random from this bag. Find the probability that it is {cols[tgt].lower()}.'
        key = f'bag-{cols}-{cnt}-{tgt}'
    elif kind == 'word':
        w = rng.choice(WORDS)
        letters = [ch for ch in set(w)]
        L = rng.choice(sorted(letters))
        p = F(w.count(L), len(w))
        body = f'<div class="word">{" ".join(w)}</div>'
        prompt = f'A letter is chosen at random from this word. Find P({L}).'
        key = f'word-{w}-{L}'
    elif kind == 'die':
        ev, fav = rng.choice([('an even number', [2, 4, 6]), ('a number greater than 4', [5, 6]), ('a multiple of 3', [3, 6]),
                              ('a number less than 3', [1, 2]), ('a 5', [5]), ('a prime number', [2, 3, 5]),
                              ('a number less than 5', [1, 2, 3, 4]), ('an odd number', [1, 3, 5])])
        p = F(len(fav), 6)
        body = '<div class="dice">' + ''.join(f'<span class="die d{i}"></span>' for i in range(1, 7)) + '</div>'
        prompt = f'A fair die is rolled. Find the probability of rolling {ev}.'
        key = f'die-{ev}'
    else:
        nsec = rng.choice([4, 5, 8, 10])
        k = rng.randrange(1, nsec)
        col = rng.choice(['blue', 'red', 'green'])
        p = F(k, nsec)
        prompt = f'A spinner has {nsec} equal sections. {k} of them are {col}. Find the probability of landing on {col}.'
        body = ''
        key = f'spin-{nsec}-{k}-{col}'
    return Q(skill='p_simple', outcome='MA4-PRO-C-01', ncm='NCM 7 §11.02', prompt=prompt, body=body, answer=fr(p),
             key=key, box_text=P_RULE, box_gap=P_GAP, box_name='probability of an event')


def p_comp(rng, reasoning=False):
    ev = rng.choice(['the surf is flat', 'the team wins', 'it rains tomorrow', 'the bus is late', 'a goal is scored',
                     'the flight is delayed', 'the counter is red', 'the student passes', 'the ferry is full'])
    neg = {'the surf is flat': 'the surf is not flat', 'the team wins': 'the team does not win',
           'it rains tomorrow': 'it does not rain tomorrow', 'the bus is late': 'the bus is not late',
           'a goal is scored': 'a goal is not scored', 'the flight is delayed': 'the flight is not delayed',
           'the counter is red': 'the counter is not red', 'the student passes': 'the student does not pass',
           'the ferry is full': 'the ferry is not full'}[ev]
    form = rng.choice(['frac', 'frac', 'dec', 'pct'])
    if form == 'frac':
        d = rng.choice([4, 5, 6, 7, 8, 9, 10, 12, 20]); a = rng.randrange(1, d)
        while F(a, d).denominator != d:
            a = rng.randrange(1, d)
        given = frac(a, d); ans = fr(1 - F(a, d)); key = f'comp-{ev}-{a}/{d}'
    elif form == 'dec':
        x = rng.choice([0.2, 0.35, 0.6, 0.15, 0.7, 0.45, 0.85]); given = num(x); ans = num(round(1 - x, 2)); key = f'comp-{ev}-{x}'
    else:
        x = rng.choice([30, 15, 65, 80, 25, 90]); given = f'{x}%'; ans = f'{100 - x}%'; key = f'comp-{ev}-{x}%'
    return Q(skill='p_comp', outcome='MA4-PRO-C-01', ncm='NCM 7 §11.05',
             prompt=f'The probability that {ev} is {given}. Find the probability that {neg}.', answer=ans, key=key,
             box_text='P(not E) = 1 − P(E)', box_gap=f'P(not E) = {gap(14)} − P(E)', box_name='complementary events')


def p_obs(rng, reasoning=False):
    kind = rng.choice(['coin', 'die', 'spinner', 'shooter'])
    if kind == 'coin':
        n = rng.choice([50, 100, 40, 80]); k = rng.randrange(n // 2 - 8, n // 2 + 9)
        prompt = f'Heads came up {k} times in {n} tosses of a coin. Find the observed probability of heads.'; body = ''
        p = F(k, n); key = f'obs-coin-{k}-{n}'
    elif kind == 'die':
        n = 60
        while True:
            fq = [rng.randrange(6, 15) for _ in range(5)]
            last = n - sum(fq)
            if 6 <= last <= 15:
                fq.append(last); break
        face = rng.randrange(1, 7)
        body = ('<table class="dt hz sm"><tr><th>Number</th>' + ''.join(f'<td>{i}</td>' for i in range(1, 7)) +
                '</tr><tr><th>Frequency</th>' + ''.join(f'<td>{x}</td>' for x in fq) + '</tr></table>')
        prompt = f'A die was rolled 60 times. Find the observed probability of rolling a {face}.'
        p = F(fq[face - 1], n); key = f'obs-die-{fq}-{face}'
    elif kind == 'spinner':
        n = rng.choice([50, 100, 40])
        while True:
            a = rng.randrange(n // 6, n // 2); b = rng.randrange(n // 6, n // 2); c = n - a - b
            if n // 6 <= c <= n // 2:
                break
        cols = ['Red', 'Blue', 'Green']; fq = [a, b, c]; t = rng.randrange(3)
        body = ('<table class="dt hz"><tr><th>Colour</th>' + ''.join(f'<td>{x}</td>' for x in cols) +
                '</tr><tr><th>Frequency</th>' + ''.join(f'<td>{x}</td>' for x in fq) + '</tr></table>')
        prompt = f'A spinner was spun {n} times. Find the observed probability of {cols[t].lower()}.'
        p = F(fq[t], n); key = f'obs-spin-{fq}-{t}'
    else:
        n = rng.choice([20, 25, 40, 50]); k = rng.randrange(n // 2, n)
        prompt = f'A netball goal shooter scored {k} goals from {n} shots. Find the observed probability of scoring a goal.'
        body = ''; p = F(k, n); key = f'obs-shoot-{k}-{n}'
    dec = float(p)
    ans = fr(p) + (f' ({num(round(dec, 3))})' if p.denominator not in (1,) else '')
    return Q(skill='p_obs', outcome='MA4-PRO-C-01', ncm='NCM 7 §11.04', prompt=prompt, body=body, answer=ans, key=key,
             box_text='Observed probability = frequency ÷ number of trials',
             box_gap=f'Observed probability = frequency ÷ {gap(40)}', box_name='observed (experimental) probability')


STAT_SKILLS = {
    's_mean': s_mean, 's_median': s_median, 's_mode': s_mode, 's_range': s_range, 's_dot': s_dot,
    's_stem': s_stem, 'p_simple': p_simple, 'p_comp': p_comp, 'p_obs': p_obs,
}


# ---------------------------------------------------------------- reasoning-only items
def s_compare(rng, reasoning=True):
    while True:
        base = sorted(rng.sample(range(2, 9), 4))
        out = rng.randrange(18, 31)
        vals = base + [out]
        if sum(vals) % 5 == 0:
            break
    mean = sum(vals) // 5; med = sorted(vals)[2]
    shown = vals[:]; rng.shuffle(shown)
    return Q(skill='s_compare', outcome='MA4-DAT-C-02', ncm='NCM 7 §10.05–10.06', reasoning=True,
             labels=['COPY', 'WORKING', '', 'EXPLAIN'], prompt='For these scores, which is larger: the mean or the median? Explain.',
             body=data_table('Scores', shown), key=f'scomp-{vals}',
             answer=f'The mean ({mean}) is larger than the median ({med}) because the outlier {out} pulls the mean up.',
             box_text='Mean = sum of scores ÷ number of scores', box_gap=f'Mean = sum of scores ÷ {gap(40)}', box_name='the mean')


def p_more(rng, reasoning=True):
    a = rng.randrange(2, 9); b = rng.randrange(2, 9)
    while a == b:
        b = rng.randrange(2, 9)
    c1, c2 = rng.sample(['red', 'blue', 'green', 'yellow', 'white'], 2)
    p = F(a, a + b)
    more = p > F(1, 2)
    return Q(skill='p_more', outcome='MA4-PRO-C-01', ncm='NCM 7 §11.02–11.03', reasoning=True,
             labels=['COPY', 'WORKING', '', 'EXPLAIN'],
             prompt=f'A bag holds {a} {c1} and {b} {c2} marbles. One is chosen at random. Is it more likely than not to be {c1}? Explain.',
             key=f'pmore-{a}-{b}-{c1}', box_text=P_RULE, box_gap=P_GAP, box_name='probability of an event',
             answer=(f'Yes: P({c1}) = {fr(p)}, which is more than {frac(1, 2)}.' if more else
                     f'No: P({c1}) = {fr(p)}, which is less than {frac(1, 2)}.'))


STAT_REASON = {'s_compare': s_compare, 'p_more': p_more}
