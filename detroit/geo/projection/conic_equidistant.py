from math import atan2, cos, pi, sin, sqrt

from ...types import Point2D
from ..common import Projection, RawProjection
from .conic import conic_projection
from .equirectangular import EquirectangularRaw

EPSILON = 1e-6


def sign(x):
    return -1 if x < 0 else 1


class ConicEquidistantRaw:
    def __init__(self, n: float, g: float):
        self._n = n
        self._g = g

    def __call__(self, x: float, y: float) -> Point2D:
        gy = self._g - y
        nx = self._n * x
        return [gy * sin(nx), self._g - gy * cos(nx)]

    def invert(self, x: float, y: float) -> Point2D:
        gy = self._g - y
        l_ = atan2(x, abs(gy)) * sign(gy)
        if gy * self._n < 0:
            l_ -= pi * sign(x) * sign(gy)
        return [l_ / self._n, self._g - sign(self._n) * sqrt(x * x + gy * gy)]


def conic_equidistant_raw(y0: float, y1: float) -> RawProjection:
    cy0 = cos(y0)
    n = sin(y0) if y0 == y1 else (cy0 - cos(y1)) / (y1 - y0)
    g = cy0 / n + y0
    return EquirectangularRaw() if abs(n) < EPSILON else ConicEquidistantRaw(n, g)


def geo_conic_equidistant() -> Projection:
    """
    The Albers' equidistant conic projection.

    returns
    -------
    Projection
        Projection object
    """
    return (
        conic_projection(conic_equidistant_raw).scale(131.154).set_center([0, 13.9389])
    )
