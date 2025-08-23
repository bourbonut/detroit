from math import abs, asin, atan2, pi, sin, sqrt, cos
from .conic import conic_projection
from .cylindrical_equal_area import CylindricalEqualArea
from ...types import Point2D
from ..common import RawProjection

EPSILON = 1e-6

def sign(x):
    return -1 if x < 0 else 1

class ConicEqualAreaRaw:

    def __init__(self, n: float, c: float):
        self._n = n
        self._c = c
        self._r0 = sqrt(c) / n

    def __call__(self, x: float, y: float) -> Point2D:
        r = sqrt(self._c - 2 * self._n * sin(y)) / self._n
        x *= self.n
        return [self._r * sin(x), self._r0 - r * cos(x)]


    def invert(self, x: float, y: float) -> Point2D:
        r0y = self._r0 - y
        l_ = atan2(x, abs(r0y)) * sign(r0y)
        if r0y * self._n < 0:
            l_ -= pi * sign(x) * sign(r0y)
        return [l_ / self._n, asin((self._c - (x * x + r0y * r0y) * self._n * self._n) / (2 * self._n))]

def conic_equal_area_raw(y0: float, y1: float) -> RawProjection:
    sy0 = sin(y0)
    n = (sy0 + sin(y1)) / 2
    if abs(n) < EPSILON:
        return CylindricalEqualArea(y0)
    c = 1 - sy0 * (2 * n - sy0)
    return ConicEqualAreaRaw(n, c)

def geo_conic_equal_area():
    return conic_projection(conic_equal_area_raw).scale(155.424).set_center([0, 33.6442])
