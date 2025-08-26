from math import atan2, cos, fsum, pi, radians, sin

from ..array import argpass
from ..types import GeoJSON
from .common import PolygonStream
from .stream import geo_stream

QUARTER_PI = pi * 0.25
TAU = 2 * pi


@argpass
def noop():
    return


class AreaStream(PolygonStream):
    def __init__(self):
        self._point = noop
        self._line_start = noop
        self._line_end = noop

        self._area_ring_sum = []
        self._area_sum = []

        self._lambda00 = None
        self._phi00 = None
        self._lambda0 = None
        self._cos_phi0 = None
        self._sin_phi0 = None

    def point(self, x: float, y: float):
        return self._point(x, y)

    def line_start(self):
        return self._line_start()

    def line_end(self):
        return self._line_end()

    def polygon_start(self):
        self._area_ring_sum = []
        self._line_start = self._area_ring_start
        self._line_end = self._area_ring_end

    def polygon_end(self):
        area_ring = fsum(self._area_ring_sum)
        area_ring = TAU + area_ring if area_ring < 0 else area_ring
        self._area_sum.append(area_ring)
        self._point = noop
        self._line_start = noop
        self._line_end = noop

    def sphere(self):
        self._area_sum.append(TAU)

    def _area_ring_start(self):
        self._point = self._area_point_first

    def _area_ring_end(self):
        self._area_point(self._lambda00, self._phi00)

    def _area_point_first(self, lambda_: float, phi: float):
        self._point = self._area_point
        self._lambda00 = lambda_
        self._phi00 = phi
        lambda_ = radians(lambda_)
        phi = radians(phi)
        self._lambda0 = lambda_
        phi = phi * 0.5 + QUARTER_PI
        self._cos_phi0 = cos(phi)
        self._sin_phi0 = sin(phi)

    def _area_point(self, lambda_: float, phi: float):
        lambda_ = radians(lambda_)
        phi = radians(phi)
        phi = phi * 0.5 + QUARTER_PI

        d_lambda = lambda_ - self._lambda0
        sd_lambda = 1 if d_lambda >= 0 else -1
        ad_lambda = sd_lambda * d_lambda
        cos_phi = cos(phi)
        sin_phi = sin(phi)
        k = self._sin_phi0 * sin_phi
        u = self._cos_phi0 * cos_phi + k * cos(ad_lambda)
        v = k * sd_lambda * sin(ad_lambda)

        self._area_ring_sum.append(atan2(v, u))
        self._lambda0 = lambda_
        self._cos_phi0 = cos_phi
        self._sin_phi0 = sin_phi

    def result(self) -> float:
        return fsum(self._area_sum) * 2


def geo_area(obj: GeoJSON) -> float:
    """
    Returns the spherical area of the specified GeoJSON object in steradians.
    This is the spherical equivalent of :func:`GeoPath.area
    <detroit.geo.path.path.GeoPath.area>`.

    Parameters
    ----------
    obj : GeoJSON
        GeoJSON object

    Returns
    -------
    float
        Spherical area
    """
    stream = AreaStream()
    geo_stream(obj, stream)
    return stream.result()
