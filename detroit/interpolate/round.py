def interpolate_round(a, b):
    a, b = float(a), float(b)
    return lambda t: round(a * (1 - t) + b * t)
