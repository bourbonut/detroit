from .color import hue
import math

def interpolate_hue(a, b):
    i = hue(float(a), float(b))
    def interpolate(t):
        x = i(t)
        return x - 360 * math.floor(x / 360)
    return interpolate
