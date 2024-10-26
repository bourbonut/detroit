from define import define, extend
from color import Color, rgbConvert, Rgb, darker, brighter
from math import degrees, radians

A = -0.14861
B = +1.78277
C = -0.29227
D = -0.90649
E = +1.97294
ED = E * D
EB = E * B
BC_DA = B * C - D * A

def cubehelixConvert(o):
    if isinstance(o, Cubehelix):
        return Cubehelix(o.h, o.s, o.l, o.opacity)
    if not isinstance(o, Rgb):
        o = rgbConvert(o)
    r = o.r / 255
    g = o.g / 255
    b = o.b / 255
    l = (BC_DA * b + ED * r - EB * g) / (BC_DA + ED - EB)
    bl = b - l
    k = (E * (g - l) - C * bl) / D
    s = (k * k + bl * bl) ** 0.5 / (E * l * (1 - l))  # NaN if l=0 or l=1
    h = (math.atan2(k, bl) * degrees - 120) if s else float('nan')
    return Cubehelix(h + 360 if h < 0 else h, s, l, o.opacity)

def cubehelix(h, s, l, opacity=None):
    if opacity is None:
        opacity = 1
    return cubehelixConvert(h) if isinstance(h, (Cubehelix, Rgb)) else Cubehelix(h, s, l, opacity)

class Cubehelix:
    def __init__(self, h, s, l, opacity):
        self.h = float(h)
        self.s = float(s)
        self.l = float(l)
        self.opacity = float(opacity)

    def brighter(self, k=None):
        k = brighter if k is None else brighter ** k
        return Cubehelix(self.h, self.s, self.l * k, self.opacity)

    def darker(self, k=None):
        k = darker if k is None else darker ** k
        return Cubehelix(self.h, self.s, self.l * k, self.opacity)

    def rgb(self):
        h = 0 if math.isnan(self.h) else (self.h + 120) * radians
        l = self.l
        a = 0 if math.isnan(self.s) else self.s * l * (1 - l)
        cosh = math.cos(h)
        sinh = math.sin(h)
        return Rgb(
            255 * (l + a * (A * cosh + B * sinh)),
            255 * (l + a * (C * cosh + D * sinh)),
            255 * (l + a * (E * cosh)),
            self.opacity
        )

define(Cubehelix, cubehelix, extend(Color, Cubehelix.__dict__))
