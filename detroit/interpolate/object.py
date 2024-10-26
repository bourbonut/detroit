from .value import value

def object_interpolator(a, b):
    i = {}
    c = {}

    if a is None or not isinstance(a, dict):
        a = {}
    if b is None or not isinstance(b, dict):
        b = {}

    for k in b:
        if k in a:
            i[k] = value(a[k], b[k])
        else:
            c[k] = b[k]

    def interpolate(t):
        for k in i:
            c[k] = i[k](t)
        return c

    return interpolate
