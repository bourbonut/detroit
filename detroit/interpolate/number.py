def interpolate_number(a, b):
    a, b = float(a), float(b)
    return lambda t: a * (1 - t) + b * t
