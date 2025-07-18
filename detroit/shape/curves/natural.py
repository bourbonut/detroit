import math

from ...selection import Selection
from .common import Curve, isvaluable


class NaturalCurve(Curve):
    def __init__(self, context):
        self._context = context
        self._line = math.nan
        self._x = []
        self._y = []

    def area_start(self):
        self._line = 0

    def area_end(self):
        self._line = math.nan

    def line_start(self):
        self._x = []
        self._y = []

    def line_end(self):
        x = self._x
        y = self._y
        n = len(x)

        if n != 0:
            if isvaluable(self._line):
                self._context.line_to(x[0], y[0])
            else:
                self._context.move_to(x[0], y[0])

            if n == 2:
                self._context.line_to(x[1], y[1])
            else:
                px = control_points(x)
                py = control_points(y)
                for i1 in range(1, n):
                    i0 = i1 - 1
                    self._context.bezier_curve_to(
                        px[0][i0], py[0][i0], px[1][i0], py[1][i0], x[i1], y[i1]
                    )

        if isvaluable(self._line) or (self._line != 0 and n == 1):
            self._context.close_path()
        self._line = 1 - self._line
        self._x = math.nan
        self._y = math.nan

    def point(self, x, y):
        self._x.append(x)
        self._y.append(y)


def control_points(x):
    n = len(x) - 1
    if n == 0:
        return [[0], [2]]
    a = [None] * n
    b = [None] * n
    r = [None] * n

    a[0] = 0
    b[0] = 2
    r[0] = x[0] + 2 * x[1]
    for i in range(1, n - 1):
        a[i] = 1
        b[i] = 4
        r[i] = 4 * x[i] + 2 * x[i + 1]
    a[n - 1] = 2
    b[n - 1] = 7
    r[n - 1] = 8 * x[n - 1] + x[n]
    for i in range(1, n):
        m = a[i] / b[i - 1]
        b[i] -= m
        r[i] -= m * r[i - 1]
    a[n - 1] = r[n - 1] / b[n - 1]
    for i in range(n - 2, -1, -1):
        a[i] = (r[i] - a[i + 1]) / b[i]
    b[n - 1] = (x[n] + a[n - 1]) / 2
    for i in range(0, n - 1):
        b[i] = 2 * x[i + 1] - a[i + 1]
    return [a, b]


def curve_natural(context: Selection) -> Curve:
    """
    Produces a natural cubic spline with the second derivative of the spline
    set to zero at the endpoints.

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
    >>> line = d3.line().curve(d3.curve_natural)
    >>> line(points)
    'M2,2C3.293,4.356,4.587,6.711,6,8C7.413,9.289,8.946,9.511,10,10C11.054,10.489,11.630,11.247,12,10C12.370,8.753,12.535,5.503,14,4C15.465,2.497,18.230,2.742,20,4C21.770,5.258,22.546,7.531,24,8C25.454,8.469,27.586,7.136,29,6C30.414,4.864,31.112,3.925,32,4C32.888,4.075,33.968,5.164,35,5C36.032,4.836,37.016,3.418,38,2'

    **Result**

    .. image:: ../../figures/light_curve_natural.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_natural.svg
       :align: center
       :class: only-dark
    """
    return NaturalCurve(context)
