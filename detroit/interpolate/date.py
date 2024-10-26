import datetime

def date_interpolator(a, b):
    d = datetime.datetime.now()
    a, b = a.timestamp(), b.timestamp()
    def interpolate(t):
        d = datetime.datetime.fromtimestamp(a * (1 - t) + b * t)
        return d
    return interpolate
