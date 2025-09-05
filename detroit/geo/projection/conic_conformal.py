from math import atan, atan2, cos, log, pi, pow, sin, sqrt, tan

from ...types import Point2D
from ..common import Projection, RawProjection
from .conic import conic_projection
from .mercator import MercatorRaw

EPSILON = 1e-6
HALF_PI = pi * 0.5


def tany(y):
    return tan((HALF_PI + y) * 0.5)


def sign(x):
    return -1 if x < 0 else 1


class ConicConformalRaw:
    def __init__(self, n: float, f: float):
        self._n = n
        self._f = f

    def __call__(self, x: float, y: float) -> Point2D:
        if self._f > 0.0:
            if y < -HALF_PI + EPSILON:
                y = -HALF_PI + EPSILON
        else:
            if y > HALF_PI - EPSILON:
                y = HALF_PI - EPSILON
        r = self._f / pow(tan((HALF_PI + y) * 0.5), self._n)
        return [r * sin(self._n * x), self._f - r * cos(self._n * x)]

    def invert(self, x: float, y: float) -> Point2D:
        fy = self._f - y
        r = sign(self._n) * sqrt(x * x + fy * fy)
        l_ = atan2(x, abs(fy)) * sign(fy)
        if fy * self._n < 0:
            l_ -= pi * sign(x) * sign(fy)
        return [l_ / self._n, 2 * atan(pow(self._f / r, 1 / self._n)) - HALF_PI]


def conic_conformal_raw(y0: float, y1: float) -> RawProjection:
    cy0 = cos(y0)
    n = sin(y0) if y0 == y1 else log(cy0 / cos(y1)) / log(tany(y1) / tany(y0))
    f = cy0 * pow(tany(y0), n) / n
    return MercatorRaw() if n == 0.0 else ConicConformalRaw(n, f)


def geo_conic_conformal() -> Projection:
    """
    the conic conformal projection. the parallels default to [30°, 30°]
    resulting in flat top.

    returns
    -------
    projection
        projection object
    """
    return conic_projection(conic_conformal_raw).scale(109.5).parallels([30, 30])
