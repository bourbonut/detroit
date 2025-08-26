from math import fsum, nan, sqrt

from ...array import argpass
from ..common import PolygonStream


@argpass
def noop():
    return


class LengthStream(PolygonStream):
    def __init__(self):
        self._point = noop
        self._length_sum = []
        self._length_ring = False
        self._x00 = nan
        self._y00 = nan
        self._x0 = nan
        self._y0 = nan

    def line_start(self):
        self._point = self._length_point_first

    def line_end(self):
        if self._length_ring:
            self._length_point(self._x00, self._y00)
        self._point = noop

    def polygon_start(self):
        self._length_ring = True

    def polygon_end(self):
        self._length_ring = False

    def point(self, x: float, y: float):
        return self._point(x, y)

    def result(self):
        length = fsum(self._length_sum)
        self._length_sum = []
        return length

    def _length_point_first(self, x: float, y: float):
        self._point = self._length_point
        self._x00 = self._x0 = x
        self._y00 = self._y0 = y

    def _length_point(self, x: float, y: float):
        self._x0 -= x
        self._y0 -= y
        self._length_sum.append(sqrt(self._x0 * self._x0 + self._y0 * self._y0))
        self._x0 = x
        self._y0 = y
