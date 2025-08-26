from math import nan, pi

from ..common import Context, PolygonStream

TAU = 2 * pi


class PathContext(PolygonStream):
    def __init__(self, context: Context):
        self._context = context
        self._radius = 4.5
        self._line = nan
        self._point = nan

    def point_radius(self, radius: float):
        self._radius = radius
        return self

    def polygon_start(self):
        self._line = 0

    def polygon_end(self):
        self._line = nan

    def line_start(self):
        self._point = 0

    def line_end(self):
        if self._line == 0:
            self._context.close_path()
        self._point = nan

    def point(self, x: float, y: float):
        if self._point == 0:
            self._context.move_to(x, y)
            self._point = 1
        elif self._point == 1:
            self._context.line_to(x, y)
        else:
            self._context.move_to(x + self._radius, y)
            self._context.arc(x, y, self._radius, 0, TAU)

    def result(self):
        return
