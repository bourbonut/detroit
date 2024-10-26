from .value import value as default_value

def piecewise(interpolate, values=None):
    if values is None:
        values = interpolate
        interpolate = default_value

    i = 0
    n = len(values) - 1
    v = values[0]
    I = [interpolate(v, values[i+1]) for i in range(n)]

    def interpolator(t):
        i = max(0, min(n - 1, int(t * n)))
        return I[i](t * n - i)

    return interpolator
