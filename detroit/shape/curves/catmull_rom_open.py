import math
from collections.abc import Callable

from ...selection import Selection
from ...types import Number
from .cardinal_open import curve_cardinal_open
from .catmull_rom import BezierTrait
from .common import Curve, isvaluable


class CatmullRomOpenCurve(Curve, BezierTrait):
    def __init__(self, context, alpha):
        self._context = context
        self._alpha = alpha
        self._line = math.nan

    def area_start(self):
        self._line = 0

    def area_end(self):
        self._line = math.nan

    def line_start(self):
        self._x0 = math.nan
        self._y0 = math.nan
        self._x1 = math.nan
        self._y1 = math.nan
        self._x2 = math.nan
        self._y2 = math.nan
        self._l01_a = 0
        self._l12_a = 0
        self._l23_a = 0
        self._l01_2a = 0
        self._l12_2a = 0
        self._l23_2a = 0
        self._point = 0

    def line_end(self):
        if isvaluable(self._line) or (self._line != 0 and self._point == 3):
            self._context.close_path()
        self._line = 1 - self._line

    def point(self, x, y):
        if self._point != 0:
            x23 = self._x2 - x
            y23 = self._y2 - y
            self._l23_2a = math.pow(x23 * x23 + y23 * y23, self._alpha)
            self._l23_a = math.sqrt(self._l23_2a)

        if self._point == 0:
            self._point = 1
        elif self._point == 1:
            self._point = 2
        elif self._point == 2:
            self._point = 3
            if isvaluable(self._line):
                self._context.line_to(self._x2, self._y2)
            else:
                self._context.move_to(self._x2, self._y2)
        elif self._point == 3:
            self._point = 4
            self._bezier_curve_to(x, y)
        else:
            self._bezier_curve_to(x, y)

        self._l01_a = self._l12_a
        self._l12_a = self._l23_a
        self._l01_2a = self._l12_2a
        self._l12_2a = self._l23_2a
        self._x0 = self._x1
        self._x1 = self._x2
        self._x2 = x
        self._y0 = self._y1
        self._y1 = self._y2
        self._y2 = y


def curve_catmull_rom_open(
    context_or_alpha: Selection | Number,
) -> Callable[[Selection], Curve] | Curve:
    """
    Produces a cubic Catmull–Rom spline using the specified control points and
    the parameter alpha, as proposed by Yuksel et al. Unlike curveCatmullRom,
    one-sided differences are not used for the first and last piece, and thus
    the curve starts at the second point and ends at the penultimate point.
    Default alpha value is :code:`0.5`.


    Parameters
    ----------
    context_or_alpha : Selection | Number
        Context or alpha value in range :math:`[0, 1]`. If alpha is zero,
        produces a uniform spline, equivalent to curveCardinal with a tension
        of zero; if alpha is one, produces a chordal spline; if alpha is 0.5,
        produces a centripetal spline. Centripetal splines are recommended to
        avoid self-intersections and overshoot.

    Returns
    -------
    Callable[[Selection], Curve] | Curve
        Curve object or function which makes a curve object with alpha value
        set
    """
    if isinstance(context_or_alpha, (int, float)):
        alpha = context_or_alpha
        if alpha == 0.0:
            return curve_cardinal_open(0.0)

        def local_curve(context):
            return CatmullRomOpenCurve(context, alpha)

        return local_curve
    context = context_or_alpha
    return CatmullRomOpenCurve(context, 0.5)
