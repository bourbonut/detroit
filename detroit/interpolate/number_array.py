def interpolate_number_array(a, b):
    if b is None:
        b = []
    n = min(len(b), len(a)) if a else 0
    c = list(b)

    def interpolate(t):
        for i in range(n):
            c[i] = a[i] * (1 - t) + b[i] * t
        return c

    return interpolate

def is_number_array(x):
    return isinstance(x, list) and all(isinstance(i, (int, float)) for i in x)
