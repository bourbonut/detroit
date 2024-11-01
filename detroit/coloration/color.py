import re
import math

DARKER = 0.7
BRIGHTER = 1 / DARKER

RE_I = re.compile(r"\s*([+-]?\d+)\s*")
RE_N = re.compile(r"\s*([+-]?(?:\d*\.)?\d+(?:[eE][+-]?\d+)?)\s*")
RE_P = re.compile(r"\s*([+-]?(?:\d*\.)?\d+(?:[eE][+-]?\d+)?)%\s*")
RE_HEX = re.compile(r"^#([0-9a-f]{3,8})$")
RE_RGB_INTEGER = re.compile(rf"^rgb\({RE_I.pattern},{RE_I.pattern},{RE_I.pattern}\)$")
RE_RGB_PERCENT = re.compile(rf"^rgb\({RE_P.pattern},{RE_P.pattern},{RE_P.pattern}\)$")
RE_RGBA_INTEGER = re.compile(rf"^rgba\({RE_I.pattern},{RE_I.pattern},{RE_I.pattern},{RE_N.pattern}\)$")
RE_RGBA_PERCENT = re.compile(rf"^rgba\({RE_P.pattern},{RE_P.pattern},{RE_P.pattern},{RE_N.pattern}\)$")
RE_HSL_PERCENT = re.compile(rf"^hsl\({RE_N.pattern},{RE_P.pattern},{RE_P.pattern}\)$")
RE_HSLA_PERCENT = re.compile(rf"^hsla\({RE_N.pattern},{RE_P.pattern},{RE_P.pattern},{RE_N.pattern}\)$")


NAMED = {
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

class Color:

    def format_hex(self):
        return self.rgb().format_hex()

    def format_hex_8(self):
        return self.rgb().format_hex_8()

    def format_hsl(self):
        return hsl_convert(self).format_hsl()

    def format_rgb(self):
        return self.rgb().format_rgb()

    def __str__(self):
        return self.format_rgb()

def color(format):
    format = format.strip().lower()
    if format == "transparent":
        return RGB(math.nan, math.nan, math.nan, 0)
    elif m := RE_HEX.match(format):
        length = len(m.group(1))
        m = int(m.group(1), 16)
        if length == 6:
            return rgbn(m)  # #ff0000
        elif length == 3:
            return RGB((m >> 8 & 0xf) | (m >> 4 & 0xf0), (m >> 4 & 0xf) | (m & 0xf0), ((m & 0xf) << 4) | (m & 0xf), 1)  # #f00
        elif length == 8:
            return rgba(m >> 24 & 0xff, m >> 16 & 0xff, m >> 8 & 0xff, (m & 0xff) / 0xff)  # #ff000000
        elif length == 4:
            return rgba((m >> 12 & 0xf) | (m >> 8 & 0xf0), (m >> 8 & 0xf) | (m >> 4 & 0xf0), (m >> 4 & 0xf) | (m & 0xf0), (((m & 0xf) << 4) | (m & 0xf)) / 0xff)  # #f000
        return None  # invalid hex
    elif m := RE_RGB_INTEGER.match(format):
        return RGB(int(m.group(1)), int(m.group(2)), int(m.group(3)), 1)  # rgb(255, 0, 0)
    elif m := RE_RGB_PERCENT.match(format):
        return RGB(float(m.group(1)) * 255 / 100, float(m.group(2)) * 255 / 100, float(m.group(3)) * 255 / 100, 1)  # rgb(100%, 0%, 0%)
    elif m := RE_RGBA_INTEGER.match(format):
        return rgba(int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4)))  # rgba(255, 0, 0, 1)
    elif m := RE_RGBA_PERCENT.match(format):
        return rgba(float(m.group(1)) * 255 / 100, float(m.group(2)) * 255 / 100, float(m.group(3)) * 255 / 100, float(m.group(4)))  # rgb(100%, 0%, 0%, 1)
    elif m := RE_HSL_PERCENT.match(format):
        return hsla(float(m.group(1)), float(m.group(2)) / 100, float(m.group(3)) / 100, 1)  # hsl(120, 50%, 50%)
    elif m := RE_HSLA_PERCENT.match(format):
        return hsla(float(m.group(1)), float(m.group(2)) / 100, float(m.group(3)) / 100, float(m.group(4)))  # hsla(120, 50%, 50%, 1)
    elif format in NAMED:
        return rgbn(NAMED[format])
    return None

def rgbn(n):
    return RGB(n >> 16 & 0xff, n >> 8 & 0xff, n & 0xff, 1)

def rgba(r, g, b, a):
    if a <= 0:
        r = g = b = math.nan
    return RGB(r, g, b, a)

def rgb_convert(obj):
    if not isinstance(obj, (Color, RGB, HSL)):
        obj = color(obj)
    if not obj:
        return RGB(0, 0, 0)
    obj = obj.rgb()
    return RGB(obj.r, obj.g, obj.b, obj.opacity)

def rgb(*args):
    if len(args) == 1:
        return rgb_convert(args[0])
    elif len(args) == 3:
        r, g, b = args
        opacity = 1
        return RGB(r, g, b, opacity)
    elif len(args) == 4:
        r, g, b, opacity = args
        return RGB(r, g, b, opacity)

class RGB(Color):
    def __init__(self, r, g, b, opacity=1):
        self.r = float(r)
        self.g = float(g)
        self.b = float(b)
        self.opacity = float(opacity)

    def brighter(self, k=None):
        k = BRIGHTER if k is None else BRIGHTER ** k
        return RGB(self.r * k, self.g * k, self.b * k, self.opacity)

    def darker(self, k=None):
        k = DARKER if k is None else DARKER ** k
        return RGB(self.r * k, self.g * k, self.b * k, self.opacity)

    def rgb(self):
        return self

    def clamp(self):
        return RGB(clampi(self.r), clampi(self.g), clampi(self.b), clampa(self.opacity))

    def displayable(self):
        return (-0.5 <= self.r < 255.5) and (-0.5 <= self.g < 255.5) and (-0.5 <= self.b < 255.5) and (0 <= self.opacity <= 1)

    def format_hex(self):
        return f"#{hex(self.r)}{hex(self.g)}{hex(self.b)}"

    def format_hex_8(self):
        return f"#{hex(self.r)}{hex(self.g)}{hex(self.b)}{hex((1 if math.isnan(self.opacity) else self.opacity) * 255)}"

    def format_rgb(self):
        a = clampa(self.opacity)
        return f"{'rgb(' if a == 1 else 'rgba('}{clampi(self.r)}, {clampi(self.g)}, {clampi(self.b)}{')' if a == 1 else f', {a})'}"

def clampa(opacity):
    return 1 if math.isnan(opacity) else max(0, min(1, opacity))

def clampi(value):
    return 0 if math.isnan(value) else max(0, min(255, round(value) or 0))

def hex(value):
    value = clampi(value)
    return f"{'0' if value < 16 else ''}{value:x}"

def hsla(h, s, l, a):
    if a <= 0:
        h = s = l = math.nan
    elif l <= 0 or l >= 1:
        h = s = math.nan
    elif s <= 0:
        h = math.nan
    return HSL(h, s, l, a)

def hsl_convert(obj):
    if isinstance(obj, HSL):
        return HSL(obj.h, obj.s, obj.l, obj.opacity)
    if not isinstance(obj, Color):
        obj = color(obj)
    if not obj:
        return HSL(0, 0, 0)
    if isinstance(obj, HSL):
        return obj
    obj = obj.rgb()
    r = obj.r / 255
    g = obj.g / 255
    b = obj.b / 255
    min_val = min(r, g, b)
    max_val = max(r, g, b)
    h = math.nan
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
        s = 0 if 0 < l < 1 else h
    return HSL(h, s, l, obj.opacity)

def hsl(*args):
    if len(args) == 1:
        return hsl_convert(args[0])
    elif len(args) == 3:
        h, l, s = args
        opacity = 1
        return HSL(h, l, s, opacity)
    elif len(args) == 4:
        h, l, s, opacity = args
        return HSL(h, l, s, opacity)

class HSL(Color):
    def __init__(self, h, s, l, opacity=1):
        self.h = float(h)
        self.s = float(s)
        self.l = float(l)
        self.opacity = float(opacity)

    def brighter(self, k=None):
        k = BRIGHTER if k is None else BRIGHTER ** k
        return HSL(self.h, self.s, self.l * k, self.opacity)

    def darker(self, k=None):
        k = DARKER if k is None else DARKER ** k
        return HSL(self.h, self.s, self.l * k, self.opacity)

    def rgb(self):
        h = self.h % 360
        s = 0 if math.isnan(h) or math.isnan(self.s) else self.s
        l = self.l
        m2 = l + (l if l < 0.5 else 1 - l) * s
        m1 = 2 * l - m2
        return RGB(
            hsl2rgb(h - 240 if h >= 240 else h + 120, m1, m2),
            hsl2rgb(h, m1, m2),
            hsl2rgb(h + 240 if h < 120 else h - 120, m1, m2),
            self.opacity
        )

    def clamp(self):
        return HSL(clamph(self.h), clampt(self.s), clampt(self.l), clampa(self.opacity))

    def displayable(self):
        return (0 <= self.s <= 1 or math.isnan(self.s)) and (0 <= self.l <= 1) and (0 <= self.opacity <= 1)

    def format_hsl(self):
        a = clampa(self.opacity)
        h = str(clamph(self.h)).removesuffix(".0")
        s = str(clampt(self.s) * 100).removesuffix(".0")
        l = str(clampt(self.l) * 100).removesuffix(".0")
        return f"{'hsl(' if a == 1 else 'hsla('}{h}, {s}%, {l}%{')' if a == 1 else f', {a})'}"

def clamph(value):
    value = (value or 0) % 360
    return value + 360 if value < 0 else value

def clampt(value):
    return max(0, min(1, value or 0))

def hsl2rgb(h, m1, m2):
    # print(h, m1, m2)
    if h < 60:
        return (m1 + (m2 - m1) * h / 60) * 255
    elif h < 180:
        return m2 * 255
    elif h < 240:
        return (m1 + (m2 - m1) * (240 - h) / 60) * 255
    else:
        return m1 * 255
