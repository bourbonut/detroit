from math import asin, atan2, cos, degrees, radians, sin, sqrt

from ..types import Point2D


def haversin(x: float) -> float:
    x = sin(x * 0.5)
    return x * x


class Interpolate:
    def __init__(self, a: Point2D, b: Point2D):
        self._x0 = radians(a[0])
        self._y0 = radians(a[1])
        self._x1 = radians(b[0])
        self._y1 = radians(b[1])
        self._cy0 = cos(self._y0)
        self._sy0 = sin(self._y0)
        self._cy1 = cos(self._y1)
        self._sy1 = sin(self._y1)
        self._kx0 = self._cy0 * cos(self._x0)
        self._ky0 = self._cy0 * sin(self._x0)
        self._kx1 = self._cy1 * cos(self._x1)
        self._ky1 = self._cy1 * sin(self._x1)
        self._d = 2 * asin(
            sqrt(
                haversin(self._y1 - self._y0)
                + self._cy0 * self._cy1 * haversin(self._x1 - self._x0)
            )
        )
        self._k = sin(self._d)
        self._interpolate = (
            self._interpolate_non_null if self._d else self._interpolate_null
        )

    def __call__(self, t: float) -> Point2D:
        return self._interpolate(t)

    def _interpolate_non_null(self, t: float) -> Point2D:
        t *= self._d
        B = sin(t) / self._k
        A = sin(self._d - t) / self._k
        x = A * self._kx0 + B * self._kx1
        y = A * self._ky0 + B * self._ky1
        z = A * self._sy0 + B * self._sy1
        return [degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y)))]

    def _interpolate_null(self, t: float) -> Point2D:
        return [degrees(self._x0), degrees(self._y0)]

    def get_distance(self) -> float:
        return self._d


def geo_interpolate(a: Point2D, b: Point2D) -> Interpolate:
    """
    Returns an interpolator function given two points a and b. Each point must
    be specified as a two-element array :code:`[longitude, latitude]` in
    degrees. The returned interpolator function takes a single argument t,
    where t is a number ranging from 0 to 1; a value of 0 returns the point a,
    while a value of 1 returns the point b. Intermediate values interpolate
    from a to b along the great arc that passes through both a and b. If a and
    b are antipodes, an arbitrary great arc is chosen.

    Parameters
    ----------
    a : Point2D
        2D point
    b : Point2D
        2D point

    Returns
    -------
    Interpolate
        Interpolate function
    """
    return Interpolate(a, b)
