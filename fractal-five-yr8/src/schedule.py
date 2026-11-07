"""Builds the year: 4 terms x 10 weeks x 3 sessions x 5 questions, following the
2027 Year 8 mixed ability scope and sequence (Master Information Kiosk, T1/T2 2027).

Rules agreed with the teacher (7 Nov 2026):
- Year 7 (NCM 7) content is available from T1 Wk 1, EXCEPT NCM 7 Ch 12 (ratios, rates, time): held back.
- A Year 8 unit's questions start as soon as its teaching ends (before its test).
- Terms 3-4 use only Year 7 content + the five Term 1-2 Year 8 units.
- Gradual shift: Term 1 mostly Year 7; then 1-2 Year 8 questions per session; ~two-thirds Year 8 by Term 4.
- Hybrid slots: Q1-Q2 from recently completed Year 8 units; Q3-Q5 rotate through earlier content.
- About one reasoning item per week. No exact repeats. All questions kept easy.
"""
import random
from collections import Counter

import re
import svg


def _plain(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h or '')).strip()


def signature(q):
    nums = sorted(re.findall(r'\d+(?:\.\d+)?', _plain(q.get('body', '')) + ' ' + _plain(q['prompt'])))
    strip = lambda t: re.sub(r'\b(mm|cm|km|m|kg|g|mL|L)\b', '', t)
    return (q['skill'].split('_')[0], strip(_plain(q['prompt'])), tuple(nums), strip(_plain(q['answer'])))

from bank_geo import GEO_SKILLS
from bank_meas import MEAS_SKILLS, MEAS_REASON
from bank_num import NUM_SKILLS
from bank_alg import ALG_SKILLS
from bank_stat import STAT_SKILLS, STAT_REASON
from bank_y8 import Y8_SKILLS, f8_reason

Y7 = {'G': GEO_SKILLS, 'M': MEAS_SKILLS, 'N': NUM_SKILLS, 'A': ALG_SKILLS, 'S': STAT_SKILLS}
UNITS = ['FRC8', 'IND8', 'PYT8', 'ALG8', 'EQU8']
UNIT_NAME = {'FRC8': 'Rational numbers, percentages & financial maths', 'IND8': 'Index laws',
             'PYT8': "Pythagoras' theorem", 'ALG8': 'Algebra 2', 'EQU8': 'Equations 2'}
# teaching ends in this half-week; first session after it (S1, S2 = first half of the week, S3 = second half)
UNLOCK = {'FRC8': (1, 5, 3), 'IND8': (1, 7, 1), 'PYT8': (1, 10, 3), 'ALG8': (2, 4, 1), 'EQU8': (2, 9, 1)}
UNIT_STRAND = {'FRC8': 'N', 'IND8': 'N', 'PYT8': 'M', 'ALG8': 'A', 'EQU8': 'A'}

W8 = {'p8_hyp': 3, 'p8_short': 3, 'p8_test': 2, 'p8_dec': 1, 'p8_est': 1,
      'i8_mult': 2, 'i8_div': 2, 'i8_pow': 2, 'i8_zero': 1, 'i8_prime': 1.2,
      'a8_expand': 3, 'a8_expsimp': 2, 'a8_fact': 3, 'a8_sub': 1, 'a8_like2': 1, 'a8_multdiv': 1,
      'e8_both': 3, 'e8_quad': 2, 'e8_formula': 2, 'e8_word': 1.2, 'e8_nonint': 1}
W7 = {'g_isos': 0.7, 'm_cap': 0.6, 'm_areaunit': 0.6, 'm_volA': 0.8, 'n_prime': 0.6, 'n_recur': 0.6,
      'n_round': 0.7, 'n_dec': 0.8, 'n_fracop': 0.8, 'a_write': 0.8, 'l_coord': 0.7, 's_stem': 0.7}

# reasoning support
REASON_Y7 = {'G': list(GEO_SKILLS), 'N': ['n_pow', 'n_ooo'], 'A': ['l_point', 'e_two'],
             'M': ['m_compare'], 'S': ['s_compare', 'p_more']}
REASON_Y8 = {'FRC8': 'f8_reason', 'IND8': 'i8_mult', 'PYT8': 'p8_test', 'ALG8': 'a8_expand', 'EQU8': 'e8_both'}
EXTRA = {'m_compare': MEAS_REASON['m_compare'], 's_compare': STAT_REASON['s_compare'],
         'p_more': STAT_REASON['p_more'], 'f8_reason': f8_reason}


def idx(t, w, s):
    return ((t - 1) * 10 + (w - 1)) * 3 + (s - 1)


def n_year8(t, w, s, avail):
    if not avail:
        return 0
    if t == 1:
        if avail == ['FRC8']:
            return 1
        return 2 if s == 2 else 1
    if t == 2:
        return 2
    if t == 3:
        return 3
    return 4 if s == 2 else 3


def gen_fn(skill):
    for d in list(Y7.values()) + list(Y8_SKILLS.values()):
        if skill in d:
            return d[skill]
    return EXTRA[skill]


class Year:
    def __init__(self, seed=2027):
        self.seed = seed
        self.rng = random.Random(seed)
        self.keys = set()
        self.sigs = set()
        self.last = {}
        self.strand_use = Counter()
        self.unit_use = Counter()
        self.skill_use = Counter()
        self.sessions = []
        self.collision_retries = 0
        self.exhausted = []

    # ---------------------------------------------------------- picking helpers
    def pick_skill(self, pool, i, week_used, weights):
        best, bs = None, -1e9
        for sk in pool:
            age = i - self.last.get(sk, -60)
            score = age * weights.get(sk, 1.0) + self.rng.random() * 2.5
            if sk in week_used:
                score -= 1000
            if score > bs:
                best, bs = sk, score
        return best

    def make(self, skill, reasoning=False, where=''):
        fn = gen_fn(skill)
        for attempt in range(120):
            svg.COLLISIONS[:] = []
            qrng = random.Random(f'{self.seed}|{where}|{skill}|{int(reasoning)}|{attempt}')
            q = fn(qrng, reasoning=reasoning)
            if svg.COLLISIONS:
                self.collision_retries += 1
                continue
            if reasoning and not q.get('reasoning'):
                continue
            if q['key'] in self.keys or signature(q) in self.sigs:
                continue
            self.keys.add(q['key']); self.sigs.add(signature(q))
            return q
        return None

    def pick_units(self, avail, k, i):
        if k == 0:
            return []
        chosen = []
        newest = max(avail, key=lambda u: idx(*UNLOCK[u]))
        age_new = i - idx(*UNLOCK[newest])

        def weight(u):
            age = i - idx(*UNLOCK[u])
            rec = 1.0 / (1.0 + age / 9.0)
            bal = 1.0 / (1.0 + self.unit_use[u] / 12.0)
            return rec * 0.6 + bal * 0.4

        # Q1: the newest unit for its first ~4 weeks, else weighted by recency
        if age_new <= 12 and self.rng.random() < 0.75:
            chosen.append(newest)
        while len(chosen) < min(k, 2):
            cand = [u for u in avail if u not in chosen] or avail
            ws = [weight(u) for u in cand]
            chosen.append(self.rng.choices(cand, ws)[0])
        # extra Year 8 slots (Terms 3-4): balance across units
        while len(chosen) < k:
            cand = [u for u in avail if u not in chosen] or avail
            cand.sort(key=lambda u: (self.unit_use[u] + self.rng.random() * 3))
            chosen.append(cand[0])
        return chosen

    def pick_strands(self, k, taken, must=None):
        out = []
        if must:
            out.append(must)
        target = {'G': 0.21, 'M': 0.20, 'N': 0.24, 'A': 0.15, 'S': 0.20}
        tot = sum(self.strand_use.values()) + 1
        while len(out) < k:
            cand = [s for s in 'GMNAS' if s not in out] or list('GMNAS')
            def score(s):
                sc = self.strand_use[s] / tot - target[s]
                if s in taken:
                    sc += 0.05
                return sc + self.rng.random() * 0.03
            cand.sort(key=score)
            out.append(cand[0])
        return out[:k]

    # ---------------------------------------------------------- build
    def build(self):
        rcats = ['G', 'Y8', 'A', 'N', 'Y8', 'M', 'S']
        rc_i = 0
        for t in range(1, 5):
            for w in range(1, 11):
                week_used = set()
                rs = ((t * 10 + w) % 3) + 1                        # session that carries the reasoning item
                for s in range(1, 4):
                    i = idx(t, w, s)
                    avail = [u for u in UNITS if i >= idx(*UNLOCK[u])]
                    k8 = n_year8(t, w, s, avail)
                    units = self.pick_units(avail, k8, i)
                    # reasoning category for this week
                    rcat = None
                    if s == rs:
                        while True:
                            rcat = rcats[rc_i % len(rcats)]; rc_i += 1
                            if rcat != 'Y8' or units:
                                break
                    taken = {UNIT_STRAND[u] for u in units}
                    must = rcat if rcat in ('G', 'M', 'N', 'A', 'S') else None
                    strands = self.pick_strands(5 - k8, taken, must)
                    qs = []
                    # Year 8 questions
                    for j, u in enumerate(units):
                        reason = (rcat == 'Y8' and j == 0)
                        pool = list(Y8_SKILLS[u])
                        if reason:
                            sk = REASON_Y8[u]
                        else:
                            sk = self.pick_skill(pool, i, week_used, W8)
                        q = self.make(sk, reasoning=reason, where=f'{i}-y8-{j}')
                        tried = {sk}
                        while q is None and len(tried) < len(pool):
                            self.exhausted.append(sk)
                            sk = self.pick_skill([p for p in pool if p not in tried], i, week_used, W8)
                            tried.add(sk)
                            q = self.make(sk, where=f'{i}-y8-{j}-b')
                        q['slot'] = 'recent' if j < 2 else 'earlier'
                        self.unit_use[u] += 1
                        self.last[sk] = i; self.skill_use[sk] += 1; week_used.add(sk)
                        qs.append(q)
                    # Year 7 questions
                    for st in strands:
                        reason = (rcat == st)
                        if reason:
                            pool = REASON_Y7[st]
                        else:
                            pool = list(Y7[st])
                        sk = self.pick_skill(pool, i, week_used, W7)
                        q = self.make(sk, reasoning=reason, where=f'{i}-y7-{st}')
                        tried = {sk}
                        while q is None:
                            self.exhausted.append(sk)
                            rest = [p for p in pool if p not in tried] or [p for p in Y7[st] if p not in tried]
                            sk = self.pick_skill(rest, i, week_used, W7)
                            tried.add(sk)
                            q = self.make(sk, reasoning=reason, where=f'{i}-y7-{st}-b') or self.make(sk, where=f'{i}-y7-{st}-c')
                        q['slot'] = 'earlier'
                        if reason:
                            rcat = 'done'
                        self.strand_use[st] += 1
                        self.last[sk] = i; self.skill_use[sk] += 1; week_used.add(sk)
                        qs.append(q)
                    # order: recent Year 8 first, then the rest shuffled
                    recent = [q for q in qs if q['slot'] == 'recent']
                    rest = [q for q in qs if q['slot'] != 'recent']
                    self.rng.shuffle(rest)
                    qs = recent + rest
                    for n_, q in enumerate(qs, 1):
                        q['n'] = n_
                    self.sessions.append(dict(term=t, week=w, session=s, idx=i, avail=avail, questions=qs))
        return self.sessions


def build_year(seed=2027):
    y = Year(seed)
    out = y.build()
    if y.exhausted:
        print('skills that ran out of unique variants (fallback used):', Counter(y.exhausted))
    return out


if __name__ == '__main__':
    ss = build_year()
    c = Counter(); r = 0
    for S in ss:
        for q in S['questions']:
            c[(S['term'], q['unit'])] += 1
            r += q['reasoning']
    for k in sorted(c):
        print(k, c[k])
    print('reasoning items:', r, ' sessions:', len(ss))
