import math

from ...selection import Selection
from .basis import BezierTrait
from .common import Curve, isvaluable


class BasisOpenCurve(Curve, BezierTrait):
    def __init__(self, context):
        self._context = context
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
        self._point = 0

    def line_end(self):
        if isvaluable(self._line) or (self._line != 0 and self._point == 3):
            self._context.close_path()
        self._line = 1 - self._line

    def point(self, x, y):
        if self._point == 0:
            self._point = 1
        elif self._point == 1:
            self._point = 2
        elif self._point == 2:
            self._point = 3
            x0 = (self._x0 + 4 * self._x1 + x) / 6
            y0 = (self._y0 + 4 * self._y1 + y) / 6
            if isvaluable(self._line):
                self._context.line_to(x0, y0)
            else:
                self._context.move_to(x0, y0)
        elif self._point == 3:
            self._point = 4
            self._bezier_curve_to(x, y)
        else:
            self._bezier_curve_to(x, y)
        self._x0 = self._x1
        self._x1 = x
        self._y0 = self._y1
        self._y1 = y


def curve_basis_open(context: Selection) -> Curve:
    """
    Produces a cubic basis spline using the specified control points. Unlike
    basis, the first and last points are not repeated, and thus the curve
    typically does not intersect these points.

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
    >>> line = d3.line().curve(d3.curve_basis_open)
    >>> line(points)
    'M6,7.333C7.333,8.667,8.667,9.333,9.667,9.667C10.667,10,11.333,10,12,9C12.667,8,13.333,6,14.667,5C16,4,18,4,19.667,4.667C21.333,5.333,22.667,6.667,24.167,7C25.667,7.333,27.333,6.667,28.667,6C30,5.333,31,4.667,32,4.500C33,4.333,34,4.667,35,4.333'

    **Result**

    .. image:: ../../figures/light_curve_basis_open.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_basis_open.svg
       :align: center
       :class: only-dark
    """
    return BasisOpenCurve(context)
