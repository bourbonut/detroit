from .value import value
from .numberArray import numberArray, isNumberArray

def array(a, b):
    return numberArray(a, b) if isNumberArray(b) else genericArray(a, b)

def genericArray(a, b):
    nb = len(b) if b else 0
    na = min(nb, len(a)) if a else 0
    x = [value(a[i], b[i]) for i in range(na)]
    c = list(b)

    def interpolate(t):
        for i in range(na):
            c[i] = x[i](t)
        return c

    return interpolate
