from math import isnan, nan, sqrt

from ...types import Point2D
from ..common import PolygonStream


class CentroidStream(PolygonStream):
    def __init__(self):
        self._point = self._centroid_point
        self._line_start = self._centroid_line_start
        self._line_end = self._centroid_line_end
        self._X0 = 0
        self._Y0 = 0
        self._Z0 = 0
        self._X1 = 0
        self._Y1 = 0
        self._Z1 = 0
        self._X2 = 0
        self._Y2 = 0
        self._Z2 = 0
        self._x00 = nan
        self._y00 = nan
        self._x0 = nan
        self._y0 = nan

    def line_start(self):
        return self._line_start()

    def line_end(self):
        return self._line_end()

    def polygon_start(self):
        self._line_start = self._centroid_ring_start
        self._line_end = self._centroid_ring_end

    def polygon_end(self):
        self._point = self._centroid_point
        self._line_start = self._centroid_line_start
        self._line_end = self._centroid_line_end

    def point(self, x: float, y: float):
        return self._point(x, y)

    def result(self) -> Point2D:
        centroid = [nan, nan]
        if self._Z2 and not isnan(self._Z2):
            centroid = [self._X2 / self._Z2, self._Y2 / self._Z2]
        elif self._Z1 and not isnan(self._Z1):
            centroid = [self._X1 / self._Z1, self._Y1 / self._Z1]
        elif self._Z0 and not isnan(self._Z0):
            centroid = [self._X0 / self._Z0, self._Y0 / self._Z0]
        self._X0 = 0
        self._Y0 = 0
        self._Z0 = 0
        self._X1 = 0
        self._Y1 = 0
        self._Z1 = 0
        self._X2 = 0
        self._Y2 = 0
        self._Z2 = 0
        return centroid

    def _centroid_point(self, x: float, y: float):
        self._X0 += x
        self._Y0 += y
        self._Z0 += 1

    def _centroid_line_start(self):
        self._point = self._centroid_point_first_line

    def _centroid_point_first_line(self, x: float, y: float):
        self._point = self._centroid_point_line
        self._x0 = x
        self._y0 = y
        self._centroid_point(x, y)

    def _centroid_point_line(self, x: float, y: float):
        dx = x - self._x0
        dy = y - self._y0
        z = sqrt(dx * dx + dy * dy)

        self._X1 += z * (self._x0 + x) * 0.5
        self._Y1 += z * (self._y0 + y) * 0.5
        self._Z1 += z

        self._x0 = x
        self._y0 = y
        self._centroid_point(x, y)

    def _centroid_line_end(self):
        self._point = self._centroid_point

    def _centroid_ring_start(self):
        self._point = self._centroid_point_first_ring

    def _centroid_ring_end(self):
        self._centroid_point_ring(self._x00, self._y00)

    def _centroid_point_first_ring(self, x: float, y: float):
        self._point = self._centroid_point_ring
        self._x00 = x
        self._x0 = x
        self._y00 = y
        self._y0 = y
        self._centroid_point(x, y)

    def _centroid_point_ring(self, x: float, y: float):
        dx = x - self._x0
        dy = y - self._y0
        z = sqrt(dx * dx + dy * dy)

        self._X1 += z * (self._x0 + x) * 0.5
        self._Y1 += z * (self._y0 + y) * 0.5
        self._Z1 += z

        z = self._y0 * x - self._x0 * y
        self._X2 += z * (self._x0 + x)
        self._Y2 += z * (self._y0 + y)
        self._Z2 += z * 3

        self._x0 = x
        self._y0 = y
        self._centroid_point(x, y)
