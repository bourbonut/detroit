import math

from ...selection import Selection
from .common import Curve, isvaluable


class BezierTrait:
    def _bezier_curve_to(self, x, y):
        self._context.bezier_curve_to(
            (2 * self._x0 + self._x1) / 3,
            (2 * self._y0 + self._y1) / 3,
            (self._x0 + 2 * self._x1) / 3,
            (self._y0 + 2 * self._y1) / 3,
            (self._x0 + 4 * self._x1 + x) / 6,
            (self._y0 + 4 * self._y1 + y) / 6,
        )


class BasisCurve(Curve, BezierTrait):
    def __init__(self, context):
        self._context = context
        self._line = math.nan
        self._x0 = math.nan
        self._y0 = math.nan
        self._x1 = math.nan
        self._y1 = math.nan

    def area_start(self):
        self._line = 0

    def area_end(self):
        self._line = math.nan

    def line_start(self):
        self._x0 = math.nan
        self._x1 = math.nan
        self._y0 = math.nan
        self._y1 = math.nan
        self._point = 0

    def line_end(self):
        if self._point == 3:
            self._bezier_curve_to(self._x1, self._y1)
            self._context.line_to(self._x1, self._y1)
        elif self._point == 2:
            self._context.line_to(self._x1, self._y1)

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
        elif self._point == 2:
            self._point = 3
            self._context.line_to(
                (5 * self._x0 + self._x1) / 6, (5 * self._y0 + self._y1) / 6
            )
            self._bezier_curve_to(x, y)
        else:
            self._bezier_curve_to(x, y)
        self._x0 = self._x1
        self._x1 = x
        self._y0 = self._y1
        self._y1 = y


def curve_basis(context: Selection) -> Curve:
    """
    Produces a cubic basis spline using the specified control points. The first
    and last points are triplicated such that the spline starts at the first
    point and ends at the last point, and is tangent to the line between the
    first and second points, and to the line between the penultimate and last
    points.

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
    >>> line = d3.line().curve(d3.curve_basis)
    >>> line(points)
    'M2,2L2.667,3C3.333,4,4.667,6,6,7.333C7.333,8.667,8.667,9.333,9.667,9.667C10.667,10,11.333,10,12,9C12.667,8,13.333,6,14.667,5C16,4,18,4,19.667,4.667C21.333,5.333,22.667,6.667,24.167,7C25.667,7.333,27.333,6.667,28.667,6C30,5.333,31,4.667,32,4.500C33,4.333,34,4.667,35,4.333C36,4,37,3,37.500,2.500L38,2'

    **Result**

    .. image:: ../../figures/light_curve_basis.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_basis.svg
       :align: center
       :class: only-dark
    """
    return BasisCurve(context)
