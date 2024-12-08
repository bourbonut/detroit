from __future__ import annotations

import math
from typing import overload

from .color import RGB, Color, rgb_convert

K = 18
XN = 0.96422
YN = 1
ZN = 0.82521
T0 = 4 / 29
T1 = 6 / 29
T2 = 3 * T1 * T1
T3 = T1 * T1 * T1


def lab_convert(obj):
    if isinstance(obj, LAB):
        return LAB(obj.l, obj.a, obj.b, obj.opacity)
    if isinstance(obj, HCL):
        return hcl2lab(obj)
    if not isinstance(obj, RGB):
        obj = rgb_convert(obj)
    r = rgb2lrgb(obj.r)
    g = rgb2lrgb(obj.g)
    b = rgb2lrgb(obj.b)
    y = xyz2lab((0.2225045 * r + 0.7168786 * g + 0.0606169 * b) / YN)
    if r == g == b:
        x = z = y
    else:
        x = xyz2lab((0.4360747 * r + 0.3850649 * g + 0.1430804 * b) / XN)
        z = xyz2lab((0.0139322 * r + 0.0971045 * g + 0.7141733 * b) / ZN)
    return LAB(116 * y - 16, 500 * (x - y), 200 * (y - z), obj.opacity)


def gray(*args):
    if len(args) == 1:
        l = args[0]
        opacity = 1
        return LAB(l, 0, 0, opacity)
    elif len(args) == 2:
        l, opacity = args
        return LAB(l, 0, 0, opacity)


@overload
def lab(specifier: str) -> LAB: ...


@overload
def lab(l: int | float, a: int | float, b: int | float) -> LAB: ...


@overload
def lab(
    l: int | float, a: int | float, b: int | float, opacity: int | float
) -> LAB: ...


def lab(*args):
    """
    Builds a new LAB color
    """
    if len(args) == 1:
        return lab_convert(args[0])
    elif len(args) == 3:
        l, a, b = args
        opacity = 1
        return LAB(l, a, b, opacity)
    elif len(args) == 4:
        l, a, b, opacity = args
        return LAB(l, a, b, opacity)


class LAB(Color):
    """
    LAB color format

    Parameters
    ----------
    l : int | float
        L* channel value
    a : int | float
        a* channel value
    b : int | float
        b* channel value
    opacity : int | float
        Opacity value
    """

    def __init__(
        self, l: int | float, a: int | float, b: int | float, opacity: int | float = 1
    ):
        self.l = float(l)
        self.a = float(a)
        self.b = float(b)
        self.opacity = float(opacity)

    def brighter(self, k: float | None = None) -> LAB:
        """
        Returns a brighter copy of this color.

        Parameters
        ----------
        k : float | None
            Brightness coefficient

        Returns
        -------
        LAB
            Brighter LAB
        """
        return LAB(self.l + K * (1 if k is None else k), self.a, self.b, self.opacity)

    def darker(self, k: float | None = None) -> LAB:
        """
        Returns a darker copy of this color.

        Parameters
        ----------
        k : float | None
            Brightness coefficient

        Returns
        -------
        LAB
            Brighter LAB
        """
        return LAB(self.l - K * (1 if k is None else k), self.a, self.b, self.opacity)

    def rgb(self) -> RGB:
        """
        Returns the RGB equivalent of this color

        Returns
        -------
        RGB
            RGB color format
        """
        y = (self.l + 16) / 116
        x = y if math.isnan(self.a) else y + self.a / 500
        z = y if math.isnan(self.b) else y - self.b / 200
        x = XN * lab2xyz(x)
        y = YN * lab2xyz(y)
        z = ZN * lab2xyz(z)
        return RGB(
            lrgb2rgb(3.1338561 * x - 1.6168667 * y - 0.4906146 * z),
            lrgb2rgb(-0.9787684 * x + 1.9161415 * y + 0.0334540 * z),
            lrgb2rgb(0.0719453 * x - 0.2289914 * y + 1.4052427 * z),
            self.opacity,
        )


def xyz2lab(t):
    return t ** (1 / 3) if t > T3 else t / T2 + T0


def lab2xyz(t):
    return t**3 if t > T1 else T2 * (t - T0)


def lrgb2rgb(x):
    return 255 * (12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055)


def rgb2lrgb(x):
    x /= 255
    return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4


def hcl_convert(obj):
    if isinstance(obj, HCL):
        return HCL(obj.h, obj.c, obj.l, obj.opacity)
    if not isinstance(obj, LAB):
        obj = lab_convert(obj)
    if obj.a == 0 and obj.b == 0:
        return HCL(
            float("nan"), 0 if 0 < obj.l < 100 else float("nan"), obj.l, obj.opacity
        )
    h = math.degrees(math.atan2(obj.b, obj.a))
    return HCL(
        h + 360 if h < 0 else h, (obj.a**2 + obj.b**2) ** 0.5, obj.l, obj.opacity
    )


@overload
def lch(specifier: str) -> HCL: ...


@overload
def lch(l: int | float, c: int | float, h: int | float) -> HCL: ...


@overload
def lch(
    l: int | float, c: int | float, h: int | float, opacity: int | float
) -> HCL: ...


def lch(*args):
    """
    Builds a new HCL color
    """
    if len(args) == 1:
        return hcl_convert(args[0])
    elif len(args) == 3:
        l, c, h = args
        opacity = 1
        return HCL(h, c, l, opacity)
    elif len(args) == 4:
        l, c, h, opacity = args
        return HCL(h, c, l, opacity)


@overload
def hcl(specifier: str) -> HCL: ...


@overload
def hcl(h: int | float, c: int | float, l: int | float) -> HCL: ...


@overload
def hcl(
    h: int | float, c: int | float, l: int | float, opacity: int | float
) -> HCL: ...


def hcl(*args):
    """
    Builds a new HCL color
    """
    if len(args) == 1:
        return hcl_convert(args[0])
    elif len(args) == 3:
        h, c, l = args
        opacity = 1
        return HCL(h, c, l, opacity)
    elif len(args) == 4:
        h, c, l, opacity = args
        return HCL(h, c, l, opacity)


class HCL(Color):
    """
    HCL color format

    Parameters
    ----------
    h : int | float
        Hue channel value
    c : int | float
        Chroma channel value
    l : int | float
        Luminance channel value
    opacity : int | float
        Opacity value
    """

    def __init__(
        self, h: int | float, c: int | float, l: int | float, opacity: int | float
    ):
        self.h = float(h)
        self.c = float(c)
        self.l = float(l)
        self.opacity = float(opacity)

    def brighter(self, k: float | None = None) -> HCL:
        """
        Returns a brighter copy of this color.

        Parameters
        ----------
        k : float | None
            Brightness coefficient

        Returns
        -------
        HCL
            Brighter HCL
        """
        return HCL(self.h, self.c, self.l + K * (1 if k is None else k), self.opacity)

    def darker(self, k: float | None = None) -> HCL:
        """
        Returns a darker copy of this color.

        Parameters
        ----------
        k : float | None
            Brightness coefficient

        Returns
        -------
        HCL
            Brighter HCL
        """
        return HCL(self.h, self.c, self.l - K * (1 if k is None else k), self.opacity)

    def rgb(self) -> RGB:
        """
        Returns the RGB equivalent of this color

        Returns
        -------
        RGB
            RGB color format
        """
        return hcl2lab(self).rgb()


def hcl2lab(obj):
    if math.isnan(obj.h):
        return LAB(obj.l, 0, 0, obj.opacity)
    h = math.radians(obj.h)
    return LAB(obj.l, math.cos(h) * obj.c, math.sin(h) * obj.c, obj.opacity)
