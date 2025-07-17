import math
from collections.abc import Callable

from ...selection import Selection
from ...types import Number
from .cardinal import BezierTrait
from .common import Curve


class CardinalClosedCurve(Curve, BezierTrait):
    def __init__(self, context, tension):
        self._context = context
        self._k = (1 - tension) / 6
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
        if self._point == 0:
            self._point = 1
            self._x3 = x
            self._y3 = y
        elif self._point == 1:
            self._point = 2
            self._x4 = x
            self._y4 = y
            self._context.move_to(x, y)
        elif self._point == 2:
            self._point = 3
            self._x5 = x
            self._y5 = y
        else:
            self._bezier_curve_to(x, y)
        self._x0 = self._x1
        self._x1 = self._x2
        self._x2 = x
        self._y0 = self._y1
        self._y1 = self._y2
        self._y2 = y


def curve_cardinal_closed(
    context_or_tension: Selection | Number,
) -> Callable[[Selection], Curve] | Curve:
    """
    Produces a closed cubic cardinal spline using the specified control points.
    When a line segment ends, the first three control points are repeated,
    producing a closed loop.
    The default tension is :code:`0`.

    Parameters
    ----------
    context_or_tension : Selection | Number
        Context or tension value in range :math:`[0, 1]` determining the length
        of the tangents. A tension of one yields all zero tangents, equivalent
        to :func:`curve_linear`

    Returns
    -------
    Callable[[Selection], Curve] | Curve
        Curve object or function which makes a curve object with tension value
        set
    """
    if isinstance(context_or_tension, (int, float)):
        tension = context_or_tension

        def local_curve(context):
            return CardinalClosedCurve(context, tension)

        return local_curve
    context = context_or_tension
    return CardinalClosedCurve(context, 0.0)
