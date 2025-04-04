import re
from collections.abc import Callable

from .number import interpolate_number

reA = re.compile(r"[-+]?(?:\d+\.?\d*|\.?\d+)(?:[eE][-+]?\d+)?")
reB = re.compile(reA.pattern)


def zero(b):
    def f(*args):
        return b

    return f


def one(b):
    def f(t):
        return str(b(t))

    return f


def interpolate_string(a: str, b: str) -> Callable[[float], str]:
    """
    Returns an interpolator between the two strings a and b.

    Parameters
    ----------
    a : str
        String a
    b : str
        String b

    Returns
    -------
    Callable[[float], str]
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_string("10.", "20.")
    >>> interpolator(0)
    '10.0'
    >>> interpolator(1)
    '20.0'
    >>> interpolator(0.5)
    '15.0'
    """
    a, b = str(a), str(b)

    bi = 0
    s = []
    q = []

    for am in reA.finditer(a):
        bm = reB.search(b, bi)
        if bm:
            if bm.start() > bi:
                s.append(b[bi : bm.start()])

            if am.group() == bm.group():
                s.append(bm.group())
            else:
                s.append(None)
                q.append(
                    {
                        "i": len(s) - 1,
                        "x": interpolate_number(float(am.group()), float(bm.group())),
                    }
                )

            bi = bm.end()

    if bi < len(b):
        s.append(b[bi:])

    if len(s) < 2:
        return one(q[0]["x"]) if q else zero(b)

    def interpolator(t):
        for o in q:
            s[o["i"]] = str(o["x"](t)).removesuffix(".0")
        return "".join(s)

    return interpolator
