import math
from collections.abc import Callable

from ...selection import Selection
from ...types import Number
from .common import Curve, isvaluable


class BezierTrait:
    def _bezier_curve_to(self, x, y):
        self._context.bezier_curve_to(
            self._x1 + self._k * (self._x2 - self._x0),
            self._y1 + self._k * (self._y2 - self._y0),
            self._x2 + self._k * (self._x1 - x),
            self._y2 + self._k * (self._y1 - y),
            self._x2,
            self._y2,
        )


class CardinalCurve(Curve, BezierTrait):
    def __init__(self, context, tension):
        self._context = context
        self._k = (1 - tension) / 6
        self._line = math.nan
        self._x0 = math.nan
        self._y0 = math.nan
        self._x1 = math.nan
        self._y1 = math.nan
        self._x2 = math.nan
        self._y2 = math.nan

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
        self._point = 0

    def line_end(self):
        if self._point == 2:
            self._context.line_to(self._x2, self._y2)
        elif self._point == 3:
            self._bezier_curve_to(self._x1, self._y1)

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
            self._x1 = x
            self._y1 = y
        elif self._point == 2:
            self._point = 3
            self._bezier_curve_to(x, y)
        else:
            self._bezier_curve_to(x, y)

        self._x0 = self._x1
        self._x1 = self._x2
        self._x2 = x
        self._y0 = self._y1
        self._y1 = self._y2
        self._y2 = y


def curve_cardinal(
    context_or_tension: Selection | Number,
) -> Callable[[Selection], Curve] | Curve:
    if isinstance(context_or_tension, (int, float)):
        tension = context_or_tension

        def local_curve(context):
            return CardinalCurve(context, tension)

        return local_curve
    context = context_or_tension
    return CardinalCurve(context, 0.0)
