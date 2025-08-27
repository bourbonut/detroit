from math import inf

from ...array import argpass
from ...types import Point2D
from ..common import PolygonStream


@argpass
def noop():
    return


class BoundsStream(PolygonStream):
    def __init__(self):
        self._line_start = noop
        self._line_end = noop
        self._polygon_start = noop
        self._polygon_end = noop
        self._x0 = inf
        self._y0 = inf
        self._x1 = -inf
        self._y1 = -inf

    def line_start(self):
        return self._line_start()

    def line_end(self):
        return self._line_end()

    def polygon_start(self):
        return self._polygon_start()

    def polygon_end(self):
        return self._polygon_end()

    def point(self, x: float, y: float):
        return self._bounds_point(x, y)

    def result(self) -> tuple[Point2D, Point2D]:
        bounds = [[self._x0, self._y0], [self._x1, self._y1]]
        self._y0 = self._x0 = inf
        self._x1 = self._y1 = -inf
        return bounds

    def _bounds_point(self, x: float, y: float):
        if x < self._x0:
            self._x0 = x
        if x > self._x1:
            self._x1 = x
        if y < self._y0:
            self._y0 = y
        if y > self._y1:
            self._y1 = y

    def __str__(self):
        return f"BoundsStream({[[self._x0, self._y0], [self._x1, self._y1]]})"
