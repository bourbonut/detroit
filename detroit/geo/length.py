from math import atan2, cos, fsum, radians, sin, sqrt

from ..array import argpass
from ..types import GeoJSON
from .common import PolygonStream
from .stream import geo_stream


@argpass
def noop():
    return


class LengthStream(PolygonStream):
    def __init__(self):
        self._point = noop
        self._line_start = self._length_line_start
        self._line_end = noop

        self._length_sum = []
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
        return

    def polygon_end(self):
        return

    def sphere(self):
        return

    def _length_line_start(self):
        self._point = self._length_point_first
        self._line_end = self._length_line_end

    def _length_line_end(self):
        self._point = noop
        self._line_end = noop

    def _length_point_first(self, lambda_: float, phi: float):
        lambda_ = radians(lambda_)
        phi = radians(phi)
        self._lambda0 = lambda_
        self._sin_phi0 = sin(phi)
        self._cos_phi0 = cos(phi)
        self._point = self._length_point

    def _length_point(self, lambda_: float, phi: float):
        lambda_ = radians(lambda_)
        phi = radians(phi)

        sin_phi = sin(phi)
        cos_phi = cos(phi)
        delta = abs(lambda_ - self._lambda0)
        cos_delta = cos(delta)
        sin_delta = sin(delta)
        x = cos_phi * sin_delta
        y = self._cos_phi0 * sin_phi - self._sin_phi0 * cos_phi * cos_delta
        z = self._sin_phi0 * sin_phi + self._cos_phi0 * cos_phi * cos_delta
        self._length_sum.append(atan2(sqrt(x * x + y * y), z))

        self._lambda0 = lambda_
        self._cos_phi0 = cos_phi
        self._sin_phi0 = sin_phi

    def result(self) -> float:
        return fsum(self._length_sum)


def geo_length(obj: GeoJSON) -> float:
    """
    Returns the great-arc length of the specified GeoJSON object in radians.
    For polygons, returns the perimeter of the exterior ring plus that of any
    interior rings. This is the spherical equivalent of :func:`GeoPath.measure
    <detroit.geo.path.path.GeoPath.measure>`.

    Parameters
    ----------
    obj : GeoJSON
        GeoJSON object

    Returns
    -------
    float
        Great-arc length
    """
    stream = LengthStream()
    geo_stream(obj, stream)
    return stream.result()
