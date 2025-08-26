from math import fsum

from ...array import argpass
from ..common import PolygonStream


@argpass
def noop():
    return


class AreaStream(PolygonStream):
    def __init__(self):
        self._area_sum = []
        self._area_ring_sum = []
        self._point = noop
        self._line_start = noop
        self._line_end = noop

    def line_start(self):
        return self._line_start()

    def line_end(self):
        return self._line_end()

    def polygon_start(self):
        self._line_start = self._area_ring_start
        self._line_end = self._area_ring_end

    def polygon_end(self):
        self._line_start = self._line_end = self._point = noop
        self._area_sum.append(abs(fsum(self._area_ring_sum)))
        self._area_ring_sum = []

    def point(self, x: float, y: float):
        return self._point(x, y)

    def result(self) -> float:
        area = fsum(self._area_sum) * 0.5
        self._area_sum = []
        return area

    def _area_ring_start(self):
        self._point = self._area_point_first

    def _area_point_first(self, x: float, y: float):
        self._point = self._area_point
        self._x00 = x
        self._x0 = x
        self._y00 = y
        self._y0 = y

    def _area_point(self, x: float, y: float):
        self._area_ring_sum.append(self._y0 * x - self._x0 * y)
        self._x0 = x
        self._y0 = y

    def _area_ring_end(self):
        self._area_point(self._x00, self._y00)

    def __str__(self):
        return "AreaStream()"
