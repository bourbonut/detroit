import math

class LinearCurve:
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
        if (
            self._line is not None and not math.isnan(self._line) and self._line
        ) or (
            self._line != 0 and self._point == 1
        ):
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
            self._context.line_to(x, y)
        else:
            self._context.line_to(x, y)
