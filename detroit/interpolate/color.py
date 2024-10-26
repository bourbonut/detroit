from .constant import constant
import math

def linear(a, d):
    return lambda t: a + t * d

def exponential(a, b, y):
    return lambda t: math.pow(a + t * (math.pow(b, y) - a), 1 / y)

def hue(a, b):
    d = b - a
    return linear(a, d if abs(d) <= 180 else d - 360 * round(d / 360)) if d else constant(math.isnan(a) and b or a)

def gamma(y):
    y = float(y)
    if y == 1:
        return nogamma
    else:
        return lambda a, b: exponential(a, b, y) if b - a else constant(math.isnan(a) and b or a)

def nogamma(a, b):
    d = b - a
    return linear(a, d) if d else constant(math.isnan(a) and b or a)
