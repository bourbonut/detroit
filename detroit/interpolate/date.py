from datetime import datetime

def interpolate_date(a, b):
    d = datetime.now()
    a, b = a.timestamp(), b.timestamp()
    def interpolate(t):
        d = datetime.fromtimestamp(a * (1 - t) + b * t)
        return d
    return interpolate
