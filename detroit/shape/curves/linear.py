import math

from ...selection import Selection
from .common import Curve, isvaluable


class LinearCurve(Curve):
    def __init__(self, context):
        self._context = context
        self._line = math.nan

    def area_start(self):
        self._line = 0

    def area_end(self):
        self._line = math.nan

    def line_start(self):
        self._point = 0

    def line_end(self):
        if isvaluable(self._line) or (self._line != 0 and self._point == 1):
            self._context.close_path()
        self._line = 1 - self._line

    def point(self, x, y):
        if self._point == 0:
            self._point = 1
            if isvaluable(self._line):
                self._context.line_to(x, y)
            else:
                self._context.move_to(x, y)
        elif self._point == 1:
            self._point = 2
            self._context.line_to(x, y)
        else:
            self._context.line_to(x, y)


def curve_linear(context: Selection) -> Curve:
    """
    Produces a polyline through the specified points.

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
    >>> line = d3.line().curve(d3.curve_linear)
    >>> line(points)
    'M2,2L6,8L10,10L12,10L14,4L20,4L24,8L29,6L32,4L35,5L38,2'

    **Result**

    .. image:: ../../figures/light_curve_linear.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_linear.svg
       :align: center
       :class: only-dark
    """
    return LinearCurve(context)
