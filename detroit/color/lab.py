from define import define, extend
from color import Color, rgbConvert, Rgb
from math import degrees, radians

K = 18
Xn = 0.96422
Yn = 1
Zn = 0.82521
t0 = 4 / 29
t1 = 6 / 29
t2 = 3 * t1 * t1
t3 = t1 * t1 * t1

def labConvert(o):
    if isinstance(o, Lab):
        return Lab(o.l, o.a, o.b, o.opacity)
    if isinstance(o, Hcl):
        return hcl2lab(o)
    if not isinstance(o, Rgb):
        o = rgbConvert(o)
    r = rgb2lrgb(o.r)
    g = rgb2lrgb(o.g)
    b = rgb2lrgb(o.b)
    y = xyz2lab((0.2225045 * r + 0.7168786 * g + 0.0606169 * b) / Yn)
    if r == g == b:
        x = z = y
    else:
        x = xyz2lab((0.4360747 * r + 0.3850649 * g + 0.1430804 * b) / Xn)
        z = xyz2lab((0.0139322 * r + 0.0971045 * g + 0.7141733 * b) / Zn)
    return Lab(116 * y - 16, 500 * (x - y), 200 * (y - z), o.opacity)

def gray(l, opacity=None):
    if opacity is None:
        opacity = 1
    return Lab(l, 0, 0, opacity)

def lab(l, a, b, opacity=None):
    if opacity is None:
        opacity = 1
    return labConvert(l) if isinstance(l, (Lab, Hcl, Rgb)) else Lab(l, a, b, opacity)

class Lab:
    def __init__(self, l, a, b, opacity):
        self.l = float(l)
        self.a = float(a)
        self.b = float(b)
        self.opacity = float(opacity)

    def brighter(self, k=None):
        return Lab(self.l + K * (1 if k is None else k), self.a, self.b, self.opacity)

    def darker(self, k=None):
        return Lab(self.l - K * (1 if k is None else k), self.a, self.b, self.opacity)

    def rgb(self):
        y = (self.l + 16) / 116
        x = y if math.isnan(self.a) else y + self.a / 500
        z = y if math.isnan(self.b) else y - self.b / 200
        x = Xn * lab2xyz(x)
        y = Yn * lab2xyz(y)
        z = Zn * lab2xyz(z)
        return Rgb(
            lrgb2rgb(3.1338561 * x - 1.6168667 * y - 0.4906146 * z),
            lrgb2rgb(-0.9787684 * x + 1.9161415 * y + 0.0334540 * z),
            lrgb2rgb(0.0719453 * x - 0.2289914 * y + 1.4052427 * z),
            self.opacity
        )

def xyz2lab(t):
    return t ** (1 / 3) if t > t3 else t / t2 + t0

def lab2xyz(t):
    return t ** 3 if t > t1 else t2 * (t - t0)

def lrgb2rgb(x):
    return 255 * (12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055)

def rgb2lrgb(x):
    x /= 255
    return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4

def hclConvert(o):
    if isinstance(o, Hcl):
        return Hcl(o.h, o.c, o.l, o.opacity)
    if not isinstance(o, Lab):
        o = labConvert(o)
    if o.a == 0 and o.b == 0:
        return Hcl(float('nan'), 0 if 0 < o.l < 100 else float('nan'), o.l, o.opacity)
    h = math.atan2(o.b, o.a) * degrees
    return Hcl(h + 360 if h < 0 else h, (o.a ** 2 + o.b ** 2) ** 0.5, o.l, o.opacity)

def lch(l, c, h, opacity=None):
    if opacity is None:
        opacity = 1
    return hclConvert(l) if isinstance(l, (Hcl, Lab, Rgb)) else Hcl(h, c, l, opacity)

def hcl(h, c, l, opacity=None):
    if opacity is None:
        opacity = 1
    return hclConvert(h) if isinstance(h, (Hcl, Lab, Rgb)) else Hcl(h, c, l, opacity)

class Hcl:
    def __init__(self, h, c, l, opacity):
        self.h = float(h)
        self.c = float(c)
        self.l = float(l)
        self.opacity = float(opacity)

    def brighter(self, k=None):
        return Hcl(self.h, self.c, self.l + K * (1 if k is None else k), self.opacity)

    def darker(self, k=None):
        return Hcl(self.h, self.c, self.l - K * (1 if k is None else k), self.opacity)

    def rgb(self):
        return hcl2lab(self).rgb()

def hcl2lab(o):
    if math.isnan(o.h):
        return Lab(o.l, 0, 0, o.opacity)
    h = o.h * radians
    return Lab(o.l, math.cos(h) * o.c, math.sin(h) * o.c, o.opacity)

define(Hcl, hcl, extend(Color, Hcl.__dict__))
