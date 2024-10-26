import re
from .number import number

reA = re.compile(r'[-+]?(?:\d+\.?\d*|\.?\d+)(?:[eE][-+]?\d+)?')
reB = re.compile(reA.pattern)

def zero(b):
    return lambda: b

def one(b):
    return lambda t: str(b(t))

def string(a, b):
    a, b = str(a), str(b)
    
    bi = 0
    s = []
    q = []

    for am in reA.finditer(a):
        bm = reB.search(b, bi)
        if bm:
            if bm.start() > bi:
                s.append(b[bi:bm.start()])
            
            if am.group() == bm.group():
                s.append(bm.group())
            else:
                s.append(None)
                q.append({'i': len(s) - 1, 'x': number(float(am.group()), float(bm.group()))})
            
            bi = bm.end()

    if bi < len(b):
        s.append(b[bi:])

    if len(s) < 2:
        return one(q[0]['x']) if q else zero(b)
    
    def interpolator(t):
        for o in q:
            s[o['i']] = str(o['x'](t))
        return ''.join(s)

    return interpolator
