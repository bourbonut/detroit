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
    """
    return BumpCurve(context, False)


def curve_bump_radial(context: Selection) -> Curve:
    return BumpRadialCurve(context)
