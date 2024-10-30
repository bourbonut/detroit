from .color import Color, rgb_convert, RGB, DARKER, BRIGHTER
from .lab import hcl_convert, HCL
import math

A = -0.14861
B = +1.78277
C = -0.29227
D = -0.90649
E = +1.97294
ED = E * D
EB = E * B
BC_DA = B * C - D * A

def cubehelix_convert(obj):
    if isinstance(obj, Cubehelix):
        return Cubehelix(obj.h, obj.s, obj.l, obj.opacity)
    if not isinstance(obj, RGB):
        obj = rgb_convert(obj)
    r = obj.r / 255
    g = obj.g / 255
    b = obj.b / 255
    l = (BC_DA * b + ED * r - EB * g) / (BC_DA + ED - EB)
    bl = b - l
    k = (E * (g - l) - C * bl) / D
    s = (k * k + bl * bl) ** 0.5 / (E * l * (1 - l))  # NaN if l=0 or l=1
    h = (math.degrees(math.atan2(k, bl)) - 120) if s else math.nan
    return Cubehelix(h + 360 if h < 0 else h, s, l, obj.opacity)

def cubehelix(*args):
    if len(args) == 1:
        return cubehelix_convert(args[0])
    elif len(args) == 3:
        h, s, l = args
        opacity = 1
        return Cubehelix(h, s, l, opacity)
    elif len(args) == 4:
        h, s, l, opacity = args
        return Cubehelix(h, s, l, opacity)

def lch(*args):
    if len(args) == 1:
        return hcl_convert(args[0])
    elif len(args) == 3:
        l, c, h = args
        opacity = 1
        return HCL(h, c, l, opacity)
    elif len(args) == 4:
        l, c, h, opacity = args
        return HCL(h, c, l, opacity)

class Cubehelix(Color):
    def __init__(self, h, s, l, opacity):
        self.h = float(h)
        self.s = float(s)
        self.l = float(l)
        self.opacity = float(opacity)

    def brighter(self, k=None):
        k = BRIGHTER if k is None else BRIGHTER ** k
        return Cubehelix(self.h, self.s, self.l * k, self.opacity)

    def darker(self, k=None):
        k = DARKER if k is None else DARKER ** k
        return Cubehelix(self.h, self.s, self.l * k, self.opacity)

    def rgb(self):
        h = 0 if math.isnan(self.h) else math.radians(self.h + 120)
        l = self.l
        a = 0 if math.isnan(self.s) else self.s * l * (1 - l)
        cosh = math.cos(h)
        sinh = math.sin(h)
        return RGB(
            255 * (l + a * (A * cosh + B * sinh)),
            255 * (l + a * (C * cosh + D * sinh)),
            255 * (l + a * (E * cosh)),
            self.opacity
        )
