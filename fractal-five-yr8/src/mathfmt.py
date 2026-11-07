"""Small HTML helpers for typesetting maths in the booklets."""
from fractions import Fraction

MINUS = '−'


def v(x):
    """Pronumeral in italics."""
    return f'<i>{x}</i>'


def num(n):
    """Format a number: integers plain, negatives with a true minus sign, thin-space thousands."""
    if isinstance(n, Fraction):
        if n.denominator == 1:
            n = n.numerator
        else:
            return frac(n.numerator, n.denominator)
    if isinstance(n, float):
        if abs(n - round(n)) < 1e-9:
            n = int(round(n))
        else:
            s = f'{n:.6f}'.rstrip('0').rstrip('.')
            return s.replace('-', MINUS)
    s = f'{abs(n):,}'.replace(',', ' ') if abs(n) >= 10000 else str(abs(n))
    return (MINUS + s) if n < 0 else s


def dec(x, dp=None):
    if dp is None:
        s = f'{x:.6f}'.rstrip('0').rstrip('.')
    else:
        s = f'{x:.{dp}f}'
    return s.replace('-', MINUS)


def frac(a, b, cls='fr'):
    a = str(a).replace('-', MINUS)
    return f'<span class="{cls}"><span class="n">{a}</span><span class="d">{b}</span></span>'


def mixed(n, a, b):
    return f'{n}{frac(a, b)}'


def fr(F):
    """Fraction object -> HTML (simplest form, integers plain)."""
    F = Fraction(F)
    if F.denominator == 1:
        return num(F.numerator)
    s = MINUS if F < 0 else ''
    return s + frac(abs(F.numerator), F.denominator)


def fr_text(F):
    F = Fraction(F)
    if F.denominator == 1:
        return str(F.numerator)
    return f'{F.numerator}/{F.denominator}'


def sup(base, e):
    return f'{base}<sup>{e}</sup>'


def sqrt(x):
    return f'<span class="rt">√<span class="rad">{x}</span></span>'


def cbrt(x):
    return f'<span class="rt"><sup class="ri">3</sup>√<span class="rad">{x}</span></span>'


def rec(digits):
    """Digits with a recurring dot over each (dot notation)."""
    return ''.join(f'<span class="rec">{d}</span>' for d in digits)


def money(x):
    if isinstance(x, Fraction):
        x = float(x)
    if abs(x - round(x)) < 1e-9:
        return f'${int(round(x))}'
    return f'${x:.2f}'


def signed_term(coef, var_html, first=False):
    """Format a term like ' + 3x', ' − x', '5x' (first)."""
    if coef == 0:
        return ''
    a = abs(coef)
    body = (var_html if a == 1 and var_html else f'{a}{var_html}')
    if first:
        return (MINUS if coef < 0 else '') + body
    return (f' {MINUS} ' if coef < 0 else ' + ') + body


def lin(m, c, x='x'):
    """m x + c as HTML."""
    s = signed_term(m, v(x), first=True) if m != 0 else ''
    if c:
        s += signed_term(c, '', first=(m == 0))
    return s or '0'


def gap(w=22):
    return f'<span class="gap" style="width:{w}pt"></span>'
