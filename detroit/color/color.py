import math
import re
from typing import TypeVar, overload

TRGB = TypeVar("RGB", bound="RGB")
THSL = TypeVar("HSL", bound="HSL")

DARKER = 0.7
BRIGHTER = 1 / DARKER

RE_I = re.compile(r"\s*([+-]?\d+)\s*")
RE_N = re.compile(r"\s*([+-]?(?:\d*\.)?\d+(?:[eE][+-]?\d+)?)\s*")
RE_P = re.compile(r"\s*([+-]?(?:\d*\.)?\d+(?:[eE][+-]?\d+)?)%\s*")
RE_HEX = re.compile(r"^#([0-9a-f]{3,8})$")
RE_RGB_INTEGER = re.compile(rf"^rgb\({RE_I.pattern},{RE_I.pattern},{RE_I.pattern}\)$")
RE_RGB_PERCENT = re.compile(rf"^rgb\({RE_P.pattern},{RE_P.pattern},{RE_P.pattern}\)$")
RE_RGBA_INTEGER = re.compile(
    rf"^rgba\({RE_I.pattern},{RE_I.pattern},{RE_I.pattern},{RE_N.pattern}\)$"
)
RE_RGBA_PERCENT = re.compile(
    rf"^rgba\({RE_P.pattern},{RE_P.pattern},{RE_P.pattern},{RE_N.pattern}\)$"
)
RE_HSL_PERCENT = re.compile(rf"^hsl\({RE_N.pattern},{RE_P.pattern},{RE_P.pattern}\)$")
RE_HSLA_PERCENT = re.compile(
    rf"^hsla\({RE_N.pattern},{RE_P.pattern},{RE_P.pattern},{RE_N.pattern}\)$"
)


NAMED = {
    "aliceblue": 0xF0F8FF,
    "antiquewhite": 0xFAEBD7,
    "aqua": 0x00FFFF,
    "aquamarine": 0x7FFFD4,
    "azure": 0xF0FFFF,
    "beige": 0xF5F5DC,
    "bisque": 0xFFE4C4,
    "black": 0x000000,
    "blanchedalmond": 0xFFEBCD,
    "blue": 0x0000FF,
    "blueviolet": 0x8A2BE2,
    "brown": 0xA52A2A,
    "burlywood": 0xDEB887,
    "cadetblue": 0x5F9EA0,
    "chartreuse": 0x7FFF00,
    "chocolate": 0xD2691E,
    "coral": 0xFF7F50,
    "cornflowerblue": 0x6495ED,
    "cornsilk": 0xFFF8DC,
    "crimson": 0xDC143C,
    "cyan": 0x00FFFF,
    "darkblue": 0x00008B,
    "darkcyan": 0x008B8B,
    "darkgoldenrod": 0xB8860B,
    "darkgray": 0xA9A9A9,
    "darkgreen": 0x006400,
    "darkgrey": 0xA9A9A9,
    "darkkhaki": 0xBDB76B,
    "darkmagenta": 0x8B008B,
    "darkolivegreen": 0x556B2F,
    "darkorange": 0xFF8C00,
    "darkorchid": 0x9932CC,
    "darkred": 0x8B0000,
    "darksalmon": 0xE9967A,
    "darkseagreen": 0x8FBC8F,
    "darkslateblue": 0x483D8B,
    "darkslategray": 0x2F4F4F,
    "darkslategrey": 0x2F4F4F,
    "darkturquoise": 0x00CED1,
    "darkviolet": 0x9400D3,
    "deeppink": 0xFF1493,
    "deepskyblue": 0x00BFFF,
    "dimgray": 0x696969,
    "dimgrey": 0x696969,
    "dodgerblue": 0x1E90FF,
    "firebrick": 0xB22222,
    "floralwhite": 0xFFFAF0,
    "forestgreen": 0x228B22,
    "fuchsia": 0xFF00FF,
    "gainsboro": 0xDCDCDC,
    "ghostwhite": 0xF8F8FF,
    "gold": 0xFFD700,
    "goldenrod": 0xDAA520,
    "gray": 0x808080,
    "green": 0x008000,
    "greenyellow": 0xADFF2F,
    "grey": 0x808080,
    "honeydew": 0xF0FFF0,
    "hotpink": 0xFF69B4,
    "indianred": 0xCD5C5C,
    "indigo": 0x4B0082,
    "ivory": 0xFFFFF0,
    "khaki": 0xF0E68C,
    "lavender": 0xE6E6FA,
    "lavenderblush": 0xFFF0F5,
    "lawngreen": 0x7CFC00,
    "lemonchiffon": 0xFFFACD,
    "lightblue": 0xADD8E6,
    "lightcoral": 0xF08080,
    "lightcyan": 0xE0FFFF,
    "lightgoldenrodyellow": 0xFAFAD2,
    "lightgray": 0xD3D3D3,
    "lightgreen": 0x90EE90,
    "lightgrey": 0xD3D3D3,
    "lightpink": 0xFFB6C1,
    "lightsalmon": 0xFFA07A,
    "lightseagreen": 0x20B2AA,
    "lightskyblue": 0x87CEFA,
    "lightslategray": 0x778899,
    "lightslategrey": 0x778899,
    "lightsteelblue": 0xB0C4DE,
    "lightyellow": 0xFFFFE0,
    "lime": 0x00FF00,
    "limegreen": 0x32CD32,
    "linen": 0xFAF0E6,
    "magenta": 0xFF00FF,
    "maroon": 0x800000,
    "mediumaquamarine": 0x66CDAA,
    "mediumblue": 0x0000CD,
    "mediumorchid": 0xBA55D3,
    "mediumpurple": 0x9370DB,
    "mediumseagreen": 0x3CB371,
    "mediumslateblue": 0x7B68EE,
    "mediumspringgreen": 0x00FA9A,
    "mediumturquoise": 0x48D1CC,
    "mediumvioletred": 0xC71585,
    "midnightblue": 0x191970,
    "mintcream": 0xF5FFFA,
    "mistyrose": 0xFFE4E1,
    "moccasin": 0xFFE4B5,
    "navajowhite": 0xFFDEAD,
    "navy": 0x000080,
    "oldlace": 0xFDF5E6,
    "olive": 0x808000,
    "olivedrab": 0x6B8E23,
    "orange": 0xFFA500,
    "orangered": 0xFF4500,
    "orchid": 0xDA70D6,
    "palegoldenrod": 0xEEE8AA,
    "palegreen": 0x98FB98,
    "paleturquoise": 0xAFEEEE,
    "palevioletred": 0xDB7093,
    "papayawhip": 0xFFEFD5,
    "peachpuff": 0xFFDAB9,
    "peru": 0xCD853F,
    "pink": 0xFFC0CB,
    "plum": 0xDDA0DD,
    "powderblue": 0xB0E0E6,
    "purple": 0x800080,
    "rebeccapurple": 0x663399,
    "red": 0xFF0000,
    "rosybrown": 0xBC8F8F,
    "royalblue": 0x4169E1,
    "saddlebrown": 0x8B4513,
    "salmon": 0xFA8072,
    "sandybrown": 0xF4A460,
    "seagreen": 0x2E8B57,
    "seashell": 0xFFF5EE,
    "sienna": 0xA0522D,
    "silver": 0xC0C0C0,
    "skyblue": 0x87CEEB,
    "slateblue": 0x6A5ACD,
    "slategray": 0x708090,
    "slategrey": 0x708090,
    "snow": 0xFFFAFA,
    "springgreen": 0x00FF7F,
    "steelblue": 0x4682B4,
    "tan": 0xD2B48C,
    "teal": 0x008080,
    "thistle": 0xD8BFD8,
    "tomato": 0xFF6347,
    "turquoise": 0x40E0D0,
    "violet": 0xEE82EE,
    "wheat": 0xF5DEB3,
    "white": 0xFFFFFF,
    "whitesmoke": 0xF5F5F5,
    "yellow": 0xFFFF00,
    "yellowgreen": 0x9ACD32,
}


class Color:
    """
    Color base class used by :code:`RGB`, :code:`HSL`, :code:`Cubehelix`,
    :code:`LAB` and :code:`HCL`.
    """

    def format_hex(self) -> str:
        """
        Returns the color formatted as hex color.

        Returns
        -------
        str
            Hex color

        Examples
        --------

        >>> d3.rgb(128, 250, 102, 0.2).format_hex()
        '#80fa66'
        """
        return self.rgb().format_hex()

    def format_hex_8(self) -> str:
        """
        Returns the color formatted as hex color with alpha channel (opacity).

        Returns
        -------
        str
            Hex color

        Examples
        --------

        >>> d3.rgb(128, 250, 102, 0.2).format_hex_8()
        '#80fa6633'
        """
        return self.rgb().format_hex_8()

    def format_hsl(self) -> str:
        """
        Returns the color formatted as HSL color.

        Returns
        -------
        str
            HSL color

        Examples
        --------

        >>> d3.rgb(128, 250, 102, 0.2).format_hsl()
        'hsla(109.45945945945947, 93.67088607594937%, 69.01960784313725%, 0.2)'
        """
        return hsl_convert(self).format_hsl()

    def format_rgb(self) -> str:
        """
        Returns the color formatted as RGB color.

        Returns
        -------
        str
            RGB color

        Examples
        --------

        >>> d3.rgb(128, 250, 102, 0.2).format_rgb()
        'rgba(128, 250, 102, 0.2)'
        """
        return self.rgb().format_rgb()

    def __str__(self):
        return self.format_rgb()


def color(format: str) -> TRGB | THSL | None:
    """
    Parses the specified CSS Color specifier string,
    returning an RGB or HSL color.
    If the specifier was not valid, None is returned.

    Parameters
    ----------
    format : str
        Specifier

    Returns
    -------
    RGB | HSL | None
        Formatted color

    Examples
    --------

    >>> d3.color("#2e65ffff")
    RGB(r=46, g=101, b=255, opacity=1.0)
    >>> d3.color("rgb(108, 10, 204)")
    RGB(r=108, g=10, b=204, opacity=1.0)
    >>> d3.color("hsl(210.4, 90%, 70%)")
    HSL(h=210.4, s=0.9, l=0.7, opacity=1.0)
    >>> d3.color("bad") is None
    True
    """
    format = format.strip().lower()
    if format == "transparent":
        return RGB(math.nan, math.nan, math.nan, 0)
    elif m := RE_HEX.match(format):
        length = len(m.group(1))
        m = int(m.group(1), 16)
        if length == 6:
            return rgbn(m)  # #ff0000
        elif length == 3:
            return RGB(
                (m >> 8 & 0xF) | (m >> 4 & 0xF0),
                (m >> 4 & 0xF) | (m & 0xF0),
                ((m & 0xF) << 4) | (m & 0xF),
                1,
            )  # #f00
        elif length == 8:
            return rgba(
                m >> 24 & 0xFF, m >> 16 & 0xFF, m >> 8 & 0xFF, (m & 0xFF) / 0xFF
            )  # #ff000000
        elif length == 4:
            return rgba(
                (m >> 12 & 0xF) | (m >> 8 & 0xF0),
                (m >> 8 & 0xF) | (m >> 4 & 0xF0),
                (m >> 4 & 0xF) | (m & 0xF0),
                (((m & 0xF) << 4) | (m & 0xF)) / 0xFF,
            )  # #f000
        return None  # invalid hex
    elif m := RE_RGB_INTEGER.match(format):
        return RGB(
            int(m.group(1)), int(m.group(2)), int(m.group(3)), 1
        )  # rgb(255, 0, 0)
    elif m := RE_RGB_PERCENT.match(format):
        return RGB(
            float(m.group(1)) * 255 / 100,
            float(m.group(2)) * 255 / 100,
            float(m.group(3)) * 255 / 100,
            1,
        )  # rgb(100%, 0%, 0%)
    elif m := RE_RGBA_INTEGER.match(format):
        return rgba(
            int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4))
        )  # rgba(255, 0, 0, 1)
    elif m := RE_RGBA_PERCENT.match(format):
        return rgba(
            float(m.group(1)) * 255 / 100,
            float(m.group(2)) * 255 / 100,
            float(m.group(3)) * 255 / 100,
            float(m.group(4)),
        )  # rgb(100%, 0%, 0%, 1)
    elif m := RE_HSL_PERCENT.match(format):
        return hsla(
            float(m.group(1)), float(m.group(2)) / 100, float(m.group(3)) / 100, 1
        )  # hsl(120, 50%, 50%)
    elif m := RE_HSLA_PERCENT.match(format):
        return hsla(
            float(m.group(1)),
            float(m.group(2)) / 100,
            float(m.group(3)) / 100,
            float(m.group(4)),
        )  # hsla(120, 50%, 50%, 1)
    elif format in NAMED:
        return rgbn(NAMED[format])
    return None


def rgbn(n):
    return RGB(n >> 16 & 0xFF, n >> 8 & 0xFF, n & 0xFF, 1)


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


def clamph(value):
    value = (value or 0) % 360
    return value + 360 if value < 0 else value


def clampt(value):
    return max(0, min(1, value or 0))


def hsl2rgb(h, m1, m2):
    if h < 60:
        return (m1 + (m2 - m1) * h / 60) * 255
    elif h < 180:
        return m2 * 255
    elif h < 240:
        return (m1 + (m2 - m1) * (240 - h) / 60) * 255
    else:
        return m1 * 255


class RGB(Color):
    """
    RGB color format

    Parameters
    ----------
    r : int
        Red channel value
    g : int
        Green channel value
    b : int
        Blue channel value
    opacity : float
        Opacity value
    """

    def __init__(self, r: int, g: int, b: int, opacity: float = 1):
        self.r = float(r)
        self.g = float(g)
        self.b = float(b)
        self.opacity = float(opacity)

    def brighter(self, k: float | None = None) -> TRGB:
        """
        Returns a brighter copy of this color.
        For example, if k is 1, steelblue in RGB color space becomes rgb(100, 186, 255).
        The parameter k controls how much brighter the returned color should be (in arbitrary units);
        if k is not specified, it defaults to 1. The behavior of this method is dependent
        on the implementing color space.

        Parameters
        ----------
        k : float | None
            Brightness coefficient

        Returns
        -------
        RGB
            Brighter RGB
        """
        k = BRIGHTER if k is None else BRIGHTER**k
        return RGB(self.r * k, self.g * k, self.b * k, self.opacity)

    def darker(self, k: float | None = None) -> TRGB:
        """
        Returns a darker copy of this color.
        For example, if k is 1, steelblue in RGB color space becomes rgb(49, 91, 126).
        The parameter k controls how much darker the returned color should be (in arbitrary units);
        if k is not specified, it defaults to 1. The behavior of this method is dependent
        on the implementing color space.

        Parameters
        ----------
        k : float | None
            Darkness coefficient

        Returns
        -------
        RGB
            Darker RGB
        """
        k = DARKER if k is None else DARKER**k
        return RGB(self.r * k, self.g * k, self.b * k, self.opacity)

    def rgb(self) -> TRGB:
        """
        Returns the RGB equivalent of this color

        Returns
        -------
        RGB
            RGB color format
        """
        return self

    def clamp(self) -> TRGB:
        """
        Returns a new RGB color where the r, g, and b channels are clamped
        to the range [0, 255] and rounded to the nearest integer value, and
        the opacity is clamped to the range [0, 1].

        Returns
        -------
        RGB
            Clamped color
        """
        return RGB(clampi(self.r), clampi(self.g), clampi(self.b), clampa(self.opacity))

    def displayable(self) -> bool:
        """
        Returns :code:`True` if and only if the color is displayable on standard hardware.
        For example, this returns false for an RGB color if any channel value is
        less than zero or greater than 255 when rounded, or if the opacity is not
        in the range [0, 1].

        Returns
        -------
        bool
            Is displayable
        """
        return (
            (-0.5 <= self.r < 255.5)
            and (-0.5 <= self.g < 255.5)
            and (-0.5 <= self.b < 255.5)
            and (0 <= self.opacity <= 1)
        )

    def format_hex(self) -> str:
        """
        Returns a hexadecimal string representing this color in RGB space, such as #4682b4.
        If this color is not displayable, a suitable displayable color is returned instead.
        For example, RGB channel values greater than 255 are clamped to 255.

        Returns
        -------
        str
            Hex color representation
        """
        return f"#{hex(self.r)}{hex(self.g)}{hex(self.b)}"

    def format_hex_8(self) -> str:
        """
        Returns a hexadecimal string representing this color in RGBA space, such as #4682b4cc.
        If this color is not displayable, a suitable displayable color is returned instead.
        For example, RGB channel values greater than 255 are clamped to 255.

        Returns
        -------
        str
            Hex 8 color representation
        """
        return f"#{hex(self.r)}{hex(self.g)}{hex(self.b)}{hex((1 if math.isnan(self.opacity) else self.opacity) * 255)}"

    def format_rgb(self) -> str:
        """
        Returns a string representing this color according to the CSS Object Model specification,
        such as rgb(247, 234, 186) or rgba(247, 234, 186, 0.2). If this color is not displayable,
        a suitable displayable color is returned instead by clamping RGB channel values to the
        interval [0, 255].

        Returns
        -------
        str
            RGB color representation
        """
        a = clampa(self.opacity)
        return f"{'rgb(' if a == 1 else 'rgba('}{clampi(self.r)}, {clampi(self.g)}, {clampi(self.b)}{')' if a == 1 else f', {a})'}"

    def __repr__(self) -> str:
        return f"RGB(r={int(self.r)}, g={int(self.g)}, b={int(self.b)}, opacity={self.opacity})"


class HSL(Color):
    """
    HSL color format

    Parameters
    ----------
    h : float
        Hue channel value
    s : float
        Saturation channel value
    l : float
        Lightness channel value
    opacity : float
        Opacity value
    """

    def __init__(self, h: float, s: float, l: float, opacity: float = 1.0):
        self.h = float(h)
        self.s = float(s)
        self.l = float(l)
        self.opacity = float(opacity)

    def brighter(self, k: float | None = None) -> THSL:
        """
        Returns a brighter copy of this color.
        For example, if k is 1, steelblue in RGB color space becomes rgb(100, 186, 255).
        The parameter k controls how much brighter the returned color should be (in arbitrary units);
        if k is not specified, it defaults to 1. The behavior of this method is dependent
        on the implementing color space.

        Parameters
        ----------
        k : float | None
            Brightness coefficient

        Returns
        -------
        HSL
            Brighter HSL
        """
        k = BRIGHTER if k is None else BRIGHTER**k
        return HSL(self.h, self.s, self.l * k, self.opacity)

    def darker(self, k: float | None = None) -> THSL:
        """
        Returns a darker copy of this color.
        For example, if k is 1, steelblue in RGB color space becomes rgb(49, 91, 126).
        The parameter k controls how much darker the returned color should be (in arbitrary units);
        if k is not specified, it defaults to 1. The behavior of this method is dependent
        on the implementing color space.

        Parameters
        ----------
        k : float | None
            Darkness coefficient

        Returns
        -------
        HSL
            Darker HSL
        """
        k = DARKER if k is None else DARKER**k
        return HSL(self.h, self.s, self.l * k, self.opacity)

    def rgb(self) -> RGB:
        """
        Returns the RGB equivalent of this color

        Returns
        -------
        RGB
            RGB color format
        """
        h = self.h % 360
        s = 0 if math.isnan(h) or math.isnan(self.s) else self.s
        l = self.l
        m2 = l + (l if l < 0.5 else 1 - l) * s
        m1 = 2 * l - m2
        return RGB(
            hsl2rgb(h - 240 if h >= 240 else h + 120, m1, m2),
            hsl2rgb(h, m1, m2),
            hsl2rgb(h + 240 if h < 120 else h - 120, m1, m2),
            self.opacity,
        )

    def clamp(self) -> THSL:
        """
        Returns a new HSL color where the h channel is clamped to the range [0, 360),
        and the s, l, and opacity channels are clamped to the range [0, 1].

        Returns
        -------
        HSL
            Clamped color
        """
        return HSL(clamph(self.h), clampt(self.s), clampt(self.l), clampa(self.opacity))

    def displayable(self) -> bool:
        """
        Returns :code:`True` if and only if the color is displayable on standard hardware.
        For example, this returns false for an HSL color if any channel value are in the
        range [0, 1] or if the opacity is not in the range [0, 1].

        Returns
        -------
        bool
            Is displayable
        """
        return (
            (0 <= self.s <= 1 or math.isnan(self.s))
            and (0 <= self.l <= 1)
            and (0 <= self.opacity <= 1)
        )

    def format_hsl(self) -> str:
        a = clampa(self.opacity)
        h = str(clamph(self.h)).removesuffix(".0")
        s = str(clampt(self.s) * 100).removesuffix(".0")
        l = str(clampt(self.l) * 100).removesuffix(".0")
        return f"{'hsl(' if a == 1 else 'hsla('}{h}, {s}%, {l}%{')' if a == 1 else f', {a})'}"

    def __repr__(self) -> str:
        return f"HSL(h={self.h}, s={self.s}, l={self.l}, opacity={self.opacity})"


@overload
def rgb(specifier: str) -> RGB: ...


@overload
def rgb(r: int, g: int, b: int) -> RGB: ...


@overload
def rgb(r: int, g: int, b: int, opacity: float) -> RGB: ...


def rgb(*args):
    """
    Builds a new RGB color.

    Parameters
    ----------
    specifier : str
        String which represents a color
    r : int
        Red value between 0 and 255
    g : int
        Green value between 0 and 255
    b : int
        Blue value between 0 and 255
    opacity : float
        Opacity value between 0 and 1

    Returns
    -------
    RGB
        RGB object

    Examples
    --------

    >>> d3.rgb("#2e65ffff")
    RGB(r=46, g=101, b=255, opacity=1.0)
    >>> d3.rgb(128, 250, 102, 0.2)
    RGB(r=128, g=250, b=102, opacity=0.2)
    """
    if len(args) == 1:
        return rgb_convert(args[0])
    elif len(args) == 3:
        r, g, b = args
        opacity = 1
        return RGB(r, g, b, opacity)
    elif len(args) == 4:
        r, g, b, opacity = args
        return RGB(r, g, b, opacity)


@overload
def hsl(specifier: str) -> HSL: ...


@overload
def hsl(h: float, s: float, l: float) -> HSL: ...


@overload
def hsl(h: float, s: float, l: float, opacity: float) -> HSL: ...


def hsl(*args):
    """
    Build a new HSL color.

    Parameters
    ----------
    specifier : str
        String which represents a color
    h : float
        Hue channel value between 0 and 360
    s : float
        Saturation channel value between 0 and 1
    l : float
        Lightness channel value between 0 and 1
    opacity : float
        Opacity value between 0 and 1

    Returns
    -------
    HSL
        HSL object

    Examples
    --------

    >>> d3.hsl("#2e65ffff")
    HSL(h=224.21052631578948, s=1.0, l=0.5901960784313726, opacity=1.0)
    >>> d3.hsl(210.4, 0.9, 0.7, 0.8)
    HSL(h=210.4, s=0.9, l=0.7, opacity=0.8)
    """
    if len(args) == 1:
        return hsl_convert(args[0])
    elif len(args) == 3:
        h, l, s = args
        opacity = 1
        return HSL(h, l, s, opacity)
    elif len(args) == 4:
        h, l, s, opacity = args
        return HSL(h, l, s, opacity)
