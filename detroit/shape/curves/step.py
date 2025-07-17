import math

from ...selection import Selection
from .common import Curve, isvaluable


class StepCurve(Curve):
    def __init__(self, context, t):
        self._context = context
        self._t = t
        self._line = math.nan
        self._x = math.nan
        self._y = math.nan

    def area_start(self):
        self._line = 0

    def area_end(self):
        self._line = math.nan

    def line_start(self):
        self._x = math.nan
        self._y = math.nan
        self._point = 0

    def line_end(self):
        if 0 < self._t < 1 and self._point == 2:
            self._context.line_to(self._x, self._y)
        if isvaluable(self._line) or (self._line != 0 and self._point == 1):
            self._context.close_path()
        if self._line >= 0:
            self._t = 1 - self._t
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
            if self._t <= 0:
                self._context.line_to(self.x, y)
                self._context.line_to(x, y)
            else:
                x1 = self._x * (1 - self._t) + x * self._t
                self._context.line_to(x1, self._y)
                self._context.line_to(x1, y)
        else:
            if self._t <= 0:
                self._context.line_to(self.x, y)
                self._context.line_to(x, y)
            else:
                x1 = self._x * (1 - self._t) + x * self._t
                self._context.line_to(x1, self._y)
                self._context.line_to(x1, y)
        self._x = x
        self._y = y


def curve_step(context: Selection) -> Curve:
    return StepCurve(context, 0.5)


def curve_step_before(context: Selection) -> Curve:
    return StepCurve(context, 0.0)


def curve_step_after(context: Selection) -> Curve:
    return StepCurve(context, 1.0)
