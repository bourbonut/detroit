from .color import hue

def hue_interpolator(a, b):
    i = hue(float(a), float(b))
    def interpolate(t):
        x = i(t)
        return x - 360 * math.floor(x / 360)
    return interpolate
