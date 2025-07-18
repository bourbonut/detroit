import math

from ...selection import Selection
from .common import Curve, fdiv, isvaluable, sign


class HermiteInterpolation:
    def _slope3(self, x2, y2):
        h0 = self._x1 - self._x0
        h1 = x2 - self._x1
        s0 = fdiv(self._y1 - self._y0, h0)
        s0 = -s0 if h1 < 0 else s0
        s1 = fdiv(y2 - self._y1, h1)
        s1 = -s1 if h0 < 0 else s1
        p = fdiv(s0 * h1 + s1 * h0, h0 + h1)
        r = (sign(s0) + sign(s1)) * min(abs(s0), abs(s1), 0.5 * abs(p))
        return 0.0 if math.isnan(r) or math.isinf(r) else r

    def _slope2(self, t):
        h = self._x1 - self._x0
        return (3 * (self._y1 - self._y0) / h - t) * 0.5 if h else t

    def _hermite_point(self, t0, t1):
        x0 = self._x0
        y0 = self._y0
        x1 = self._x1
        y1 = self._y1
        dx = (x1 - x0) / 3
        self._context.bezier_curve_to(
            x0 + dx, y0 + dx * t0, x1 - dx, y1 - dx * t1, x1, y1
        )


class Monotone(Curve, HermiteInterpolation):
    def __init__(self, context):
        self._context = context
        self._line = math.nan
        self._x0 = math.nan
        self._y0 = math.nan
        self._x1 = math.nan
        self._y1 = math.nan
        self._t0 = math.nan

    def area_start(self):
        self._line = 0

    def area_end(self):
        self._line = math.nan

    def line_start(self):
        self._x0 = math.nan
        self._y0 = math.nan
        self._x1 = math.nan
        self._y1 = math.nan
        self._t0 = math.nan
        self._point = 0

    def line_end(self):
        if self._point == 2:
            self._context.line_to(self._x1, self._y1)
        elif self._point == 3:
            self._hermite_point(self._t0, self._slope2(self._t0))

        if isvaluable(self._line) or (self._line != 0 and self._point == 1):
            self._context.close_path()

        self._line = 1 - self._line

    def point(self, x, y):
        t1 = math.nan
        if x == self._x1 and y == self._y1:
            return

        if self._point == 0:
            self._point = 1
            if isvaluable(self._line):
                self._context.line_to(x, y)
            else:
                self._context.move_to(x, y)
        elif self._point == 1:
            self._point = 2
        elif self._point == 2:
            self._point = 3
            t1 = self._slope3(x, y)
            self._hermite_point(self._slope2(t1), t1)
        else:
            t1 = self._slope3(x, y)
            self._hermite_point(self._t0, t1)

        self._x0 = self._x1
        self._x1 = x
        self._y0 = self._y1
        self._y1 = y
        self._t0 = t1


class ReflectContext:
    def __init__(self, context):
        self._context = context

    def move_to(self, x, y):
        self._context.move_to(y, x)

    def line_to(self, x, y):
        self._context.line_to(y, x)

    def close_path(self):
        self._context.close_path()

    def bezier_curve_to(self, x1, y1, x2, y2, x, y):
        self._context.bezier_curve_to(y1, x1, y2, x2, y, x)


class MonotoneX(Monotone):
    def __init__(self, context):
        Monotone.__init__(self, context)


class MonotoneY(Monotone):
    def __init__(self, context):
        Monotone.__init__(self, ReflectContext(context))

    def point(self, x, y):
        super().point(y, x)


def curve_monotone_x(context: Selection) -> Curve:
    """
    Produces a cubic spline that preserves monotonicity in y, assuming
    monotonicity in x, as proposed by Steffen in A simple method for monotonic
    interpolation in one dimension: "a smooth curve with continuous first-order
    derivatives that passes through any given set of data points without
    spurious oscillations. Local extrema can occur only at grid points where
    they are given by the data, but not in between two adjacent grid points."

    Parameters
    ----------
    context : Selection
        Context

    Returns
    -------
    Curve
        Curve object

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
    >>> line = d3.line().curve(d3.curve_monotone_x)
    >>> line(points)
    'M2,2C3.333,4.333,4.667,6.667,6,8C7.333,9.333,8.667,10,10,10C10.667,10,11.333,10,12,10C12.667,10,13.333,4,14,4C16,4,18,4,20,4C21.333,4,22.667,8,24,8C25.667,8,27.333,6.944,29,6C30,5.433,31,4,32,4C33,4,34,5,35,5C36,5,37,3.500,38,2'

    **Result**

    .. image:: ../../figures/light_curve_monotone_x.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_monotone_x.svg
       :align: center
       :class: only-dark
    """
    return MonotoneX(context)


def curve_monotone_y(context: Selection) -> Curve:
    """
    Produces a cubic spline that preserves monotonicity in x, assuming
    monotonicity in y, as proposed by Steffen in A simple method for monotonic
    interpolation in one dimension: "a smooth curve with continuous first-order
    derivatives that passes through any given set of data points without
    spurious oscillations. Local extrema can occur only at grid points where
    they are given by the data, but not in between two adjacent grid points."

    Parameters
    ----------
    context : Selection
        Context

    Returns
    -------
    Curve
        Curve object

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
    >>> line = d3.line().curve(d3.curve_monotone_y)
    >>> line(points)
    'M2,2C2.667,4,3.333,6,6,8C6.889,8.667,7.333,9.333,10,10C10,10,12,10,12,10C13.333,8,12.667,6,14,4C14,4,20,4,20,4C22.667,5.333,26.667,6.667,24,8C25.333,7.333,30.333,6.667,29,6C27.667,5.333,30,4.667,32,4C31,4.333,35.667,4.667,35,5C37,4,37.500,3,38,2'

    **Result**

    .. image:: ../../figures/light_curve_monotone_y.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_monotone_y.svg
       :align: center
       :class: only-dark
    """
    return MonotoneY(context)
