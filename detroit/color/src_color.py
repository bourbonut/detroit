# src/index.py
from color import color, rgb, hsl
from lab import lab, hcl, lch, gray
from cubehelix import cubehelix

# -----

# src/cubehelix.py
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

# -----

# src/color.py
from define import define, extend

class Color:
    pass

darker = 0.7
brighter = 1 / darker

reI = r"\s*([+-]?\d+)\s*"
reN = r"\s*([+-]?(?:\d*\.)?\d+(?:[eE][+-]?\d+)?)\s*"
reP = r"\s*([+-]?(?:\d*\.)?\d+(?:[eE][+-]?\d+)?)%\s*"
reHex = r"^#([0-9a-f]{3,8})$"
reRgbInteger = re.compile(rf"^rgb\({reI},{reI},{reI}\)$")
reRgbPercent = re.compile(rf"^rgb\({reP},{reP},{reP}\)$")
reRgbaInteger = re.compile(rf"^rgba\({reI},{reI},{reI},{reN}\)$")
reRgbaPercent = re.compile(rf"^rgba\({reP},{reP},{reP},{reN}\)$")
reHslPercent = re.compile(rf"^hsl\({reN},{reP},{reP}\)$")
reHslaPercent = re.compile(rf"^hsla\({reN},{reP},{reP},{reN}\)$")

named = {
    "aliceblue": 0xf0f8ff,
    "antiquewhite": 0xfaebd7,
    "aqua": 0x00ffff,
    "aquamarine": 0x7fffd4,
    "azure": 0xf0ffff,
    "beige": 0xf5f5dc,
    "bisque": 0xffe4c4,
    "black": 0x000000,
    "blanchedalmond": 0xffebcd,
    "blue": 0x0000ff,
    "blueviolet": 0x8a2be2,
    "brown": 0xa52a2a,
    "burlywood": 0xdeb887,
    "cadetblue": 0x5f9ea0,
    "chartreuse": 0x7fff00,
    "chocolate": 0xd2691e,
    "coral": 0xff7f50,
    "cornflowerblue": 0x6495ed,
    "cornsilk": 0xfff8dc,
    "crimson": 0xdc143c,
    "cyan": 0x00ffff,
    "darkblue": 0x00008b,
    "darkcyan": 0x008b8b,
    "darkgoldenrod": 0xb8860b,
    "darkgray": 0xa9a9a9,
    "darkgreen": 0x006400,
    "darkgrey": 0xa9a9a9,
    "darkkhaki": 0xbdb76b,
    "darkmagenta": 0x8b008b,
    "darkolivegreen": 0x556b2f,
    "darkorange": 0xff8c00,
    "darkorchid": 0x9932cc,
    "darkred": 0x8b0000,
    "darksalmon": 0xe9967a,
    "darkseagreen": 0x8fbc8f,
    "darkslateblue": 0x483d8b,
    "darkslategray": 0x2f4f4f,
    "darkslategrey": 0x2f4f4f,
    "darkturquoise": 0x00ced1,
    "darkviolet": 0x9400d3,
    "deeppink": 0xff1493,
    "deepskyblue": 0x00bfff,
    "dimgray": 0x696969,
    "dimgrey": 0x696969,
    "dodgerblue": 0x1e90ff,
    "firebrick": 0xb22222,
    "floralwhite": 0xfffaf0,
    "forestgreen": 0x228b22,
    "fuchsia": 0xff00ff,
    "gainsboro": 0xdcdcdc,
    "ghostwhite": 0xf8f8ff,
    "gold": 0xffd700,
    "goldenrod": 0xdaa520,
    "gray": 0x808080,
    "green": 0x008000,
    "greenyellow": 0xadff2f,
    "grey": 0x808080,
    "honeydew": 0xf0fff0,
    "hotpink": 0xff69b4,
    "indianred": 0xcd5c5c,
    "indigo": 0x4b0082,
    "ivory": 0xfffff0,
    "khaki": 0xf0e68c,
    "lavender": 0xe6e6fa,
    "lavenderblush": 0xfff0f5,
    "lawngreen": 0x7cfc00,
    "lemonchiffon": 0xfffacd,
    "lightblue": 0xadd8e6,
    "lightcoral": 0xf08080,
    "lightcyan": 0xe0ffff,
    "lightgoldenrodyellow": 0xfafad2,
    "lightgray": 0xd3d3d3,
    "lightgreen": 0x90ee90,
    "lightgrey": 0xd3d3d3,
    "lightpink": 0xffb6c1,
    "lightsalmon": 0xffa07a,
    "lightseagreen": 0x20b2aa,
    "lightskyblue": 0x87cefa,
    "lightslategray": 0x778899,
    "lightslategrey": 0x778899,
    "lightsteelblue": 0xb0c4de,
    "lightyellow": 0xffffe0,
    "lime": 0x00ff00,
    "limegreen": 0x32cd32,
    "linen": 0xfaf0e6,
    "magenta": 0xff00ff,
    "maroon": 0x800000,
    "mediumaquamarine": 0x66cdaa,
    "mediumblue": 0x0000cd,
    "mediumorchid": 0xba55d3,
    "mediumpurple": 0x9370db,
    "mediumseagreen": 0x3cb371,
    "mediumslateblue": 0x7b68ee,
    "mediumspringgreen": 0x00fa9a,
    "mediumturquoise": 0x48d1cc,
    "mediumvioletred": 0xc71585,
    "midnightblue": 0x191970,
    "mintcream": 0xf5fffa,
    "mistyrose": 0xffe4e1,
    "moccasin": 0xffe4b5,
    "navajowhite": 0xffdead,
    "navy": 0x000080,
    "oldlace": 0xfdf5e6,
    "olive": 0x808000,
    "olivedrab": 0x6b8e23,
    "orange": 0xffa500,
    "orangered": 0xff4500,
    "orchid": 0xda70d6,
    "palegoldenrod": 0xeee8aa,
    "palegreen": 0x98fb98,
    "paleturquoise": 0xafeeee,
    "palevioletred": 0xdb7093,
    "papayawhip": 0xffefd5,
    "peachpuff": 0xffdab9,
    "peru": 0xcd853f,
    "pink": 0xffc0cb,
    "plum": 0xdda0dd,
    "powderblue": 0xb0e0e6,
    "purple": 0x800080,
    "rebeccapurple": 0x663399,
    "red": 0xff0000,
    "rosybrown": 0xbc8f8f,
    "royalblue": 0x4169e1,
    "saddlebrown": 0x8b4513,
    "salmon": 0xfa8072,
    "sandybrown": 0xf4a460,
    "seagreen": 0x2e8b57,
    "seashell": 0xfff5ee,
    "sienna": 0xa0522d,
    "silver": 0xc0c0c0,
    "skyblue": 0x87ceeb,
    "slateblue": 0x6a5acd,
    "slategray": 0x708090,
    "slategrey": 0x708090,
    "snow": 0xfffafa,
    "springgreen": 0x00ff7f,
    "steelblue": 0x4682b4,
    "tan": 0xd2b48c,
    "teal": 0x008080,
    "thistle": 0xd8bfd8,
    "tomato": 0xff6347,
    "turquoise": 0x40e0d0,
    "violet": 0xee82ee,
    "wheat": 0xf5deb3,
    "white": 0xffffff,
    "whitesmoke": 0xf5f5f5,
    "yellow": 0xffff00,
    "yellowgreen": 0x9acd32
}

def color_formatHex(self):
    return self.rgb().formatHex()

def color_formatHex8(self):
    return self.rgb().formatHex8()

def color_formatHsl(self):
    return hslConvert(self).formatHsl()

def color_formatRgb(self):
    return self.rgb().formatRgb()

def color(format):
    format = format.strip().lower()
    m = reHex.match(format)
    if m:
        l = len(m.group(1))
        m = int(m.group(1), 16)
        if l == 6:
            return rgbn(m)  # #ff0000
        elif l == 3:
            return Rgb((m >> 8 & 0xf) | (m >> 4 & 0xf0), (m >> 4 & 0xf) | (m & 0xf0), ((m & 0xf) << 4) | (m & 0xf), 1)  # #f00
        elif l == 8:
            return rgba(m >> 24 & 0xff, m >> 16 & 0xff, m >> 8 & 0xff, (m & 0xff) / 0xff)  # #ff000000
        elif l == 4:
            return rgba((m >> 12 & 0xf) | (m >> 8 & 0xf0), (m >> 8 & 0xf) | (m >> 4 & 0xf0), (m >> 4 & 0xf) | (m & 0xf0), (((m & 0xf) << 4) | (m & 0xf)) / 0xff)  # #f000
        else:
            return None  # invalid hex
    m = reRgbInteger.match(format)
    if m:
        return Rgb(int(m.group(1)), int(m.group(2)), int(m.group(3)), 1)  # rgb(255, 0, 0)
    m = reRgbPercent.match(format)
    if m:
        return Rgb(float(m.group(1)) * 255 / 100, float(m.group(2)) * 255 / 100, float(m.group(3)) * 255 / 100, 1)  # rgb(100%, 0%, 0%)
    m = reRgbaInteger.match(format)
    if m:
        return rgba(int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4)))  # rgba(255, 0, 0, 1)
    m = reRgbaPercent.match(format)
    if m:
        return rgba(float(m.group(1)) * 255 / 100, float(m.group(2)) * 255 / 100, float(m.group(3)) * 255 / 100, float(m.group(4)))  # rgb(100%, 0%, 0%, 1)
    m = reHslPercent.match(format)
    if m:
        return hsla(float(m.group(1)), float(m.group(2)) / 100, float(m.group(3)) / 100, 1)  # hsl(120, 50%, 50%)
    m = reHslaPercent.match(format)
    if m:
        return hsla(float(m.group(1)), float(m.group(2)) / 100, float(m.group(3)) / 100, float(m.group(4)))  # hsla(120, 50%, 50%, 1)
    if format in named:
        return rgbn(named[format])
    if format == "transparent":
        return Rgb(float('nan'), float('nan'), float('nan'), 0)
    return None

def rgbn(n):
    return Rgb(n >> 16 & 0xff, n >> 8 & 0xff, n & 0xff, 1)

def rgba(r, g, b, a):
    if a <= 0:
        r = g = b = float('nan')
    return Rgb(r, g, b, a)

def rgbConvert(o):
    if not isinstance(o, Color):
        o = color(o)
    if not o:
        return Rgb()
    o = o.rgb()
    return Rgb(o.r, o.g, o.b, o.opacity)

def rgb(r, g, b, opacity=None):
    if opacity is None:
        opacity = 1
    return rgbConvert(r) if isinstance(r, (Color, Rgb)) else Rgb(r, g, b, opacity)

class Rgb:
    def __init__(self, r, g, b, opacity):
        self.r = float(r)
        self.g = float(g)
        self.b = float(b)
        self.opacity = float(opacity)

    def brighter(self, k=None):
        k = brighter if k is None else brighter ** k
        return Rgb(self.r * k, self.g * k, self.b * k, self.opacity)

    def darker(self, k=None):
        k = darker if k is None else darker ** k
        return Rgb(self.r * k, self.g * k, self.b * k, self.opacity)

    def rgb(self):
        return self

    def clamp(self):
        return Rgb(clampi(self.r), clampi(self.g), clampi(self.b), clampa(self.opacity))

    def displayable(self):
        return (-0.5 <= self.r < 255.5) and (-0.5 <= self.g < 255.5) and (-0.5 <= self.b < 255.5) and (0 <= self.opacity <= 1)

    def formatHex(self):
        return f"#{hex(self.r)}{hex(self.g)}{hex(self.b)}"

    def formatHex8(self):
        return f"#{hex(self.r)}{hex(self.g)}{hex(self.b)}{hex((1 if math.isnan(self.opacity) else self.opacity) * 255)}"

    def formatRgb(self):
        a = clampa(self.opacity)
        return f"{'rgb(' if a == 1 else 'rgba('}{clampi(self.r)}, {clampi(self.g)}, {clampi(self.b)}{')' if a == 1 else f', {a})'}"

def clampa(opacity):
    return 1 if math.isnan(opacity) else max(0, min(1, opacity))

def clampi(value):
    return max(0, min(255, round(value) or 0))

def hex(value):
    value = clampi(value)
    return f"{'0' if value < 16 else ''}{value:x}"

def hsla(h, s, l, a):
    if a <= 0:
        h = s = l = float('nan')
    elif l <= 0 or l >= 1:
        h = s = float('nan')
    elif s <= 0:
        h = float('nan')
    return Hsl(h, s, l, a)

def hslConvert(o):
    if isinstance(o, Hsl):
        return Hsl(o.h, o.s, o.l, o.opacity)
    if not isinstance(o, Color):
        o = color(o)
    if not o:
        return Hsl()
    if isinstance(o, Hsl):
        return o
    o = o.rgb()
    r = o.r / 255
    g = o.g / 255
    b = o.b / 255
    min_val = min(r, g, b)
    max_val = max(r, g, b)
    h = float('nan')
    s = max_val - min_val
    l = (max_val + min_val) / 2
    if s:
        if r == max_val:
            h = (g - b) / s + (g < b) * 6
        elif g == max_val:
            h = (b - r) / s + 2
        else:
            h = (r - g) / s + 4
        s /= l < 0.5 and (max_val + min_val) or (2 - max_val - min_val)
        h *= 60
    else:
        s = l > 0 and l < 1 and 0 or h
    return Hsl(h, s, l, o.opacity)

def hsl(h, s, l, opacity=None):
    if opacity is None:
        opacity = 1
    return hslConvert(h) if isinstance(h, (Hsl, Color)) else Hsl(h, s, l, opacity)

class Hsl:
    def __init__(self, h, s, l, opacity):
        self.h = float(h)
        self.s = float(s)
        self.l = float(l)
        self.opacity = float(opacity)

    def brighter(self, k=None):
        k = brighter if k is None else brighter ** k
        return Hsl(self.h, self.s, self.l * k, self.opacity)

    def darker(self, k=None):
        k = darker if k is None else darker ** k
        return Hsl(self.h, self.s, self.l * k, self.opacity)

    def rgb(self):
        h = self.h % 360 + (self.h < 0) * 360
        s = 0 if math.isnan(h) or math.isnan(self.s) else self.s
        l = self.l
        m2 = l + (l < 0.5 and l or 1 - l) * s
        m1 = 2 * l - m2
        return Rgb(
            hsl2rgb(h >= 240 and h - 240 or h + 120, m1, m2),
            hsl2rgb(h, m1, m2),
            hsl2rgb(h < 120 and h + 240 or h - 120, m1, m2),
            self.opacity
        )

    def clamp(self):
        return Hsl(clamph(self.h), clampt(self.s), clampt(self.l), clampa(self.opacity))

    def displayable(self):
        return (0 <= self.s <= 1 or math.isnan(self.s)) and (0 <= self.l <= 1) and (0 <= self.opacity <= 1)

    def formatHsl(self):
        a = clampa(self.opacity)
        return f"{'hsl(' if a == 1 else 'hsla('}{clamph(self.h)}, {clampt(self.s) * 100}%, {clampt(self.l) * 100}%{')' if a == 1 else f', {a})'}"

def clamph(value):
    value = (value or 0) % 360
    return value + 360 if value < 0 else value

def clampt(value):
    return max(0, min(1, value or 0))

def hsl2rgb(h, m1, m2):
    return (m1 + (m2 - m1) * h / 60 if h < 60 else m2 if h < 180 else m1 + (m2 - m1) * (240 - h) / 60 if h < 240 else m1) * 255

# -----

# src/lab.py
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

# -----

# src/math.py
import math

radians = math.pi / 180
degrees = 180 / math.pi

# -----

# src/define.py
def define(constructor, factory, prototype):
    constructor.prototype = factory.prototype = prototype
    prototype.constructor = constructor

def extend(parent, definition):
    prototype = type('Prototype', (parent,), {})
    for key, value in definition.items():
        setattr(prototype, key, value)
    return prototype

