import math
from typing import TypeVar, overload

from .color import BRIGHTER, DARKER, RGB, Color, rgb_convert
from .lab import HCL, hcl_convert

TCubehelix = TypeVar("Cubehelix", bound="Cubehelix")

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
    if l == 0 or l == 1:
        s = math.nan
    else:
        s = (k * k + bl * bl) ** 0.5 / (E * l * (1 - l))  # NaN if l=0 or l=1
    h = (math.degrees(math.atan2(k, bl)) - 120) if not math.isnan(s) and s else math.nan
    return Cubehelix(h + 360 if h < 0 else h, s, l, obj.opacity)


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
    """
    Cubehelix color format

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

    def brighter(self, k: float | None = None) -> TCubehelix:
        """
        Returns a brighter copy of this color.

        Parameters
        ----------
        k : float | None
            Brightness coefficient

        Returns
        -------
        Cubehelix
            Brighter Cubehelix
        """
        k = BRIGHTER if k is None else BRIGHTER**k
        return Cubehelix(self.h, self.s, self.l * k, self.opacity)

    def darker(self, k: float | None = None) -> TCubehelix:
        """
        Returns a darker copy of this color.

        Parameters
        ----------
        k : float | None
            Darkness coefficient

        Returns
        -------
        Cubehelix
            Darker Cubehelix
        """
        k = DARKER if k is None else DARKER**k
        return Cubehelix(self.h, self.s, self.l * k, self.opacity)

    def rgb(self) -> RGB:
        """
        Returns the RGB equivalent of this color

        Returns
        -------
        RGB
            RGB color format
        """
        h = 0 if math.isnan(self.h) else math.radians(self.h + 120)
        l = self.l
        a = 0 if math.isnan(self.s) else self.s * l * (1 - l)
        cosh = math.cos(h)
        sinh = math.sin(h)
        return RGB(
            255 * (l + a * (A * cosh + B * sinh)),
            255 * (l + a * (C * cosh + D * sinh)),
            255 * (l + a * (E * cosh)),
            self.opacity,
        )

    def __repr__(self) -> str:
        return f"Cubehelix(h={self.h}, s={self.s}, l={self.l}, opacity={self.opacity})"


@overload
def cubehelix(specifier: str) -> Cubehelix: ...


@overload
def cubehelix(h: float, s: float, l: float) -> Cubehelix: ...


@overload
def cubehelix(h: float, s: float, l: float, opacity: float) -> Cubehelix: ...


def cubehelix(*args):
    """
    Build a new Cubehelix color

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
    Cubehelix
        Cubehelix object

    Examples
    --------

    >>> d3.cubehelix("#2e65ffff")
    Cubehelix(h=222.45389380826435, s=1.3363126255145055, l=0.3978037691833379, opacity=1.0)
    >>> d3.cubehelix(210.4, 0.9, 0.7, 0.8)
    Cubehelix(h=210.4, s=0.9, l=0.7, opacity=0.8)
    """
    if len(args) == 1:
        return cubehelix_convert(args[0])
    elif len(args) == 3:
        h, s, l = args
        opacity = 1
        return Cubehelix(h, s, l, opacity)
    elif len(args) == 4:
        h, s, l, opacity = args
        return Cubehelix(h, s, l, opacity)
