from .constant import constant
import math

def linear(a, d):
    def f(t):
        return a + t * d
    return f

def exponential(a, b, y):
    def f(t):
        return math.pow(a + t * (math.pow(b, y) - a), 1 / y)
    return f

def hue(a, b):
    d = b - a
    return linear(a, d if abs(d) <= 180 else d - 360 * round(d / 360)) if d else constant(math.isnan(a) and b or a)

def gamma(y):
    if round(y) == 1.:
        return nogamma
    def f(a, b):
        return exponential(a, b, y) if b - a else constant(math.isnan(a) and b or a)
    return f

def nogamma(a, b):
    d = b - a
    return linear(a, d) if d else constant(math.isnan(a) and b or a)
