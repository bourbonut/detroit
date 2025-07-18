import math
from collections.abc import Callable

from ...selection import Selection
from ...types import Number
from .cardinal_closed import curve_cardinal_closed
from .catmull_rom import BezierTrait
from .common import Curve


class CatmullRomClosedCurve(Curve, BezierTrait):
    def __init__(self, context, alpha):
        self._context = context
        self._alpha = alpha
        self._line = math.nan

    def area_start(self):
        return

    def area_end(self):
        return

    def line_start(self):
        self._x0 = math.nan
        self._y0 = math.nan
        self._x1 = math.nan
        self._y1 = math.nan
        self._x2 = math.nan
        self._y2 = math.nan
        self._x3 = math.nan
        self._y3 = math.nan
        self._x4 = math.nan
        self._y4 = math.nan
        self._x5 = math.nan
        self._y5 = math.nan
        self._l01_a = 0
        self._l12_a = 0
        self._l23_a = 0
        self._l01_2a = 0
        self._l12_2a = 0
        self._l23_2a = 0
        self._point = 0

    def line_end(self):
        if self._point == 1:
            self._context.move_to(self._x3, self._y3)
            self._context.close_path()
        elif self._point == 2:
            self._context.line_to(self._x3, self._y3)
            self._context.close_path()
        elif self._point == 3:
            self.point(self._x3, self._y3)
            self.point(self._x4, self._y4)
            self.point(self._x5, self._y5)

    def point(self, x, y):
        if self._point != 0:
            x23 = self._x2 - x
            y23 = self._y2 - y
            self._l23_2a = math.pow(x23 * x23 + y23 * y23, self._alpha)
            self._l23_a = math.sqrt(self._l23_2a)

        if self._point == 0:
            self._point = 1
            self._x3 = x
            self._y3 = y
        elif self._point == 1:
            self._point = 2
            self._x4 = x
            self._y4 = y
            self._context.move_to(self._x4, self._y4)
        elif self._point == 2:
            self._point = 3
            self._x5 = x
            self._y5 = y
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


def curve_catmull_rom_closed(
    context_or_alpha: Selection | Number,
) -> Callable[[Selection], Curve] | Curve:
    """
    Produces a closed cubic Catmull–Rom spline using the specified control
    points and the parameter alpha, as proposed by Yuksel et al. When a line
    segment ends, the first three control points are repeated, producing a
    closed loop.
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

    Examples
    --------

    >>> points = [
    ...     [2, 2],
    ...     [6, 8],
    ...     [10, 10],
    ...     [12, 10],
    ...     [14, 4],
    ...     [20, 4],
    ...     [24, 8],
    ...     [29, 6],
    ...     [32, 4],
    ...     [35, 5],
    ...     [38, 2],
    ... ]
    >>> line = d3.line().curve(d3.curve_catmull_rom_closed)
    >>> line(points)
    'M6,8C7.209,9.067,8.868,9.733,10,10C10.757,10.179,11.438,10.405,12,10C12.999,9.280,12.631,4.987,14,4C15.334,3.039,18.318,3.303,20,4C21.633,4.676,22.477,7.687,24,8C25.486,8.305,27.578,6.748,29,6C30.164,5.388,30.965,4.139,32,4C32.969,3.870,34.063,5.221,35,5C36.085,4.744,38.308,2.744,38,2C37.102,-0.169,3.652,-1.087,2,2C1.261,3.382,4.465,6.645,6,8'
    >>> line = d3.line().curve(d3.curve_catmull_rom_closed(0.2))
    >>> line(points)
    'M6,8C7.275,9.215,8.964,9.693,10,10C10.882,10.261,11.394,10.703,12,10C12.763,9.115,12.653,4.995,14,4C15.333,3.016,18.327,3.321,20,4C21.653,4.671,22.491,7.675,24,8C25.494,8.322,27.637,6.696,29,6C30.258,5.358,30.987,4.156,32,4C32.987,3.848,34.028,5.286,35,5C36.031,4.697,40.483,2.605,38,2C34.192,1.072,5.977,0.401,2,2C-0.884,3.159,4.597,6.663,6,8'

    **Result**

    .. image:: ../../figures/light_curve_catmull_rom_closed.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_catmull_rom_closed.svg
       :align: center
       :class: only-dark
    """
    if isinstance(context_or_alpha, (int, float)):
        alpha = context_or_alpha
        if alpha == 0.0:
            return curve_cardinal_closed(0.0)

        def local_curve(context):
            return CatmullRomClosedCurve(context, alpha)

        return local_curve
    context = context_or_alpha
    return CatmullRomClosedCurve(context, 0.5)
