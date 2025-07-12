import math

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

class BasisCurve(BezierTrait):

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

        if (self._line is not None and not math.isnan(self._line) and self._line) or (self._line != 0 and self._point == 1):
            self._context.close_path()
        self._line = 1 - self._line

    def point(self, x, y):
        if self._point == 0:
            self._point = 1
            if self._line is not None and not math.isnan(self._line) and self._line:
                self._context.line_to(x, y)
            else:
                self._context.move_to(x, y)
        elif self._point == 1:
            self._point = 2
        elif self._point == 2:
            self._point = 3
            self._context.line_to((5 * self._x0 + self._x1) / 6, (5 * self._y0 + self._y1) / 6)
            self._bezier_curve_to(x, y)
        else:
            self._bezier_curve_to(x, y)
        self._x0 = self._x1
        self._x1 = x
        self._y0 = self._y1
        self._y1 = y


def curve_basis(context):
    return BasisCurve(context)
