import math

from ...selection import Selection
from .common import Curve, isvaluable, point_radial


class BumpCurve(Curve):
    def __init__(self, context, x):
        self._context = context
        self._x = x
        self._line = math.nan
        self._x0 = math.nan
        self._y0 = math.nan

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
            if self._x:
                self._x0 = (self._x0 + x) / 2
                self._context.bezier_curve_to(self._x0, self._y0, self._x0, y, x, y)
            else:
                self._y0 = (self._y0 + y) / 2
                self._context.bezier_curve_to(self._x0, self._y0, x, self._y0, x, y)
        else:
            if self._x:
                self._x0 = (self._x0 + x) / 2
                self._context.bezier_curve_to(self._x0, self._y0, self._x0, y, x, y)
            else:
                self._y0 = (self._y0 + y) / 2
                self._context.bezier_curve_to(self._x0, self._y0, x, self._y0, x, y)
        self._x0 = x
        self._y0 = y


class BumpRadialCurve(Curve):
    def __init__(self, context):
        self._context = context
        self._x0 = math.nan
        self._y0 = math.nan

    def area_start(self):
        return

    def area_end(self):
        return

    def line_start(self):
        self._point = 0

    def line_end(self):
        return

    def point(self, x, y):
        if self._point == 0:
            self._point = 1
        else:
            p0 = point_radial(self._x0, self._y0)
            self._y0 = (self._y0 + y) / 2
            p1 = point_radial(self._x0, self._y0)
            p2 = point_radial(x, self._y0)
            p3 = point_radial(x, y)
            self._context.move_to(*p0)
            self._context.bezier_curve_to(*p1, *p2, *p3)
        self._x0 = x
        self._y0 = y


def curve_bump_x(context: Selection) -> Curve:
    """
    Produces a Bézier curve between each pair of points, with horizontal
    tangents at each point.

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
    >>> line = d3.line().curve(d3.curve_bump_x)
    >>> line(points)
    'M2,2C4,2,4,8,6,8C8,8,8,10,10,10C11,10,11,10,12,10C13,10,13,4,14,4C17,4,17,4,20,4C22,4,22,8,24,8C26.500,8,26.500,6,29,6C30.500,6,30.500,4,32,4C33.500,4,33.500,5,35,5C36.500,5,36.500,2,38,2'

    **Result**

    .. image:: ../../figures/light_curve_bump_x.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_bump_x.svg
       :align: center
       :class: only-dark
    """
    return BumpCurve(context, True)


def curve_bump_y(context: Selection) -> Curve:
    """
    Produces a Bézier curve between each pair of points, with vertical tangents
    at each point.

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
    >>> line = d3.line().curve(d3.curve_bump_y)
    >>> line(points)
    'M2,2C2,5,6,5,6,8C6,9,10,9,10,10C10,10,12,10,12,10C12,7,14,7,14,4C14,4,20,4,20,4C20,6,24,6,24,8C24,7,29,7,29,6C29,5,32,5,32,4C32,4.500,35,4.500,35,5C35,3.500,38,3.500,38,2'

    **Result**

    .. image:: ../../figures/light_curve_bump_y.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_bump_y.svg
       :align: center
       :class: only-dark
    """
    return BumpCurve(context, False)


def curve_bump_radial(context: Selection) -> Curve:
    return BumpRadialCurve(context)
