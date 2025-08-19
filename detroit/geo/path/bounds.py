from math import inf
from ...array import argpass

@argpass
def noop():
    return

class BoundsStream:

    def __init__(self):
        self._point = self._bounds_point
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

    def point(self, x, y):
        return self._point(x, y)

    def result(self):
        bounds = [[self._x0, self._y0], [self._x1, self._y1]]
        self._y0 = self._x0 = inf
        self._x1 = self._y1 = -inf
        return bounds

    def _bounds_point(self, x, y):
        if self._x < self._x0:
            self._x0 = self._x
        if self._x > self._x1:
            self._x1 = self._x
        if self._y < self._y0:
            self._y0 = self._y
        if self._y > self._y1:
            self._y1 = self._y
