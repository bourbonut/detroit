from math import asin, atan2, cos, degrees, fsum, hypot, nan, radians, sin, sqrt

from ..types import GeoJSON, Point2D
from .common import PolygonStream
from .stream import geo_stream

EPSILON = 1e-6
EPSILON2 = 1e-12


class CentroidStream(PolygonStream):
    def __init__(self):
        self._W0 = 0
        self._W1 = 0
        self._X0 = 0
        self._Y0 = 0
        self._Z0 = 0
        self._X1 = 0
        self._Y1 = 0
        self._Z1 = 0

        self._X2 = []
        self._Y2 = []
        self._Z2 = []

        self._x0 = None
        self._y0 = None
        self._z0 = None

        self._lambda00 = None
        self._phi00 = None

        self._point = self._centroid_point
        self._line_start = self._centroid_line_start
        self._line_end = self._centroid_line_end

    def point(self, x: float, y: float):
        return self._point(x, y)

    def line_start(self):
        return self._line_start()

    def line_end(self):
        return self._line_end()

    def polygon_start(self):
        self._line_start = self._centroid_ring_start
        self._line_end = self._centroid_ring_end

    def polygon_end(self):
        self._line_start = self._centroid_line_start
        self._line_end = self._centroid_line_end

    def sphere(self):
        return

    def _centroid_point(self, lambda_: float, phi: float):
        lambda_ = radians(lambda_)
        phi = radians(phi)
        cos_phi = cos(phi)
        self._centroid_point_cartesian(
            cos_phi * cos(lambda_), cos_phi * sin(lambda_), sin(phi)
        )

    def _centroid_point_cartesian(self, x: float, y: float, z: float):
        self._W0 += 1
        self._X0 += (x - self._X0) / self._W0
        self._Y0 += (y - self._Y0) / self._W0
        self._Z0 += (z - self._Z0) / self._W0

    def _centroid_line_start(self):
        self._point = self._centroid_line_point_first

    def _centroid_line_point_first(self, lambda_: float, phi: float):
        lambda_ = radians(lambda_)
        phi = radians(phi)
        cos_phi = cos(phi)
        self._x0 = cos_phi * cos(lambda_)
        self._y0 = cos_phi * sin(lambda_)
        self._z0 = sin(phi)
        self._point = self._centroid_line_point
        self._centroid_point_cartesian(self._x0, self._y0, self._z0)

    def _centroid_line_point(self, lambda_: float, phi: float):
        lambda_ = radians(lambda_)
        phi = radians(phi)
        cos_phi = cos(phi)
        x = cos_phi * cos(lambda_)
        y = cos_phi * sin(lambda_)
        z = sin(phi)
        w = atan2(
            sqrt(
                (self._y0 * z - self._z0 * y) * (self._y0 * z - self._z0 * y)
                + (self._z0 * x - self._x0 * z) * (self._z0 * x - self._x0 * z)
                + (self._x0 * y - self._y0 * x) * (self._x0 * y - self._y0 * x)
            ),
            self._x0 * x + self._y0 * y + self._z0 * z,
        )

        self._W1 += w
        self._X1 += w * (self._x0 + x)
        self._Y1 += w * (self._y0 + y)
        self._Z1 += w * (self._z0 + z)
        self._x0 = x
        self._y0 = y
        self._z0 = z
        self._centroid_point_cartesian(self._x0, self._y0, self._z0)

    def _centroid_line_end(self):
        self._point = self._centroid_point

    def _centroid_ring_start(self):
        self._point = self._centroid_ring_point_first

    def _centroid_ring_end(self):
        self._centroid_ring_point(self._lambda00, self._phi00)
        self._point = self._centroid_point

    def _centroid_ring_point_first(self, lambda_: float, phi: float):
        self._lambda00 = lambda_
        self._phi00 = phi
        lambda_ = radians(lambda_)
        phi = radians(phi)
        self._point = self._centroid_ring_point
        cos_phi = cos(phi)
        self._x0 = cos_phi * cos(lambda_)
        self._y0 = cos_phi * sin(lambda_)
        self._z0 = sin(phi)
        self._centroid_point_cartesian(self._x0, self._y0, self._z0)

    def _centroid_ring_point(self, lambda_: float, phi: float):
        lambda_ = radians(lambda_)
        phi = radians(phi)
        cos_phi = cos(phi)
        x = cos_phi * cos(lambda_)
        y = cos_phi * sin(lambda_)
        z = sin(phi)
        cx = self._y0 * z - self._z0 * y
        cy = self._z0 * x - self._x0 * z
        cz = self._x0 * y - self._y0 * x
        m = hypot(cx, cy, cz)
        w = asin(m)
        v = -w / m if m != 0 else 0.0

        self._X2.append(v * cx)
        self._Y2.append(v * cy)
        self._Z2.append(v * cz)
        self._W1 += w
        self._X1 += w * (self._x0 + x)
        self._Y1 += w * (self._y0 + y)
        self._Z1 += w * (self._z0 + z)
        self._x0 = x
        self._y0 = y
        self._z0 = z
        self._centroid_point_cartesian(self._x0, self._y0, self._z0)

    def result(self) -> Point2D:
        x = fsum(self._X2)
        y = fsum(self._Y2)
        z = fsum(self._Z2)
        m = hypot(x, y, z)
        if m < EPSILON2:
            x = self._X1
            y = self._Y1
            z = self._Z1
            if self._W1 < EPSILON:
                x = self._X0
                y = self._Y0
                z = self._Z0
            m = hypot(x, y, z)
            if m < EPSILON2:
                return [nan, nan]
        return [degrees(atan2(y, x)), degrees(asin(z / m))]


def geo_centroid(obj: GeoJSON) -> Point2D:
    """
    Returns the spherical centroid of the specified GeoJSON object. This is the
    spherical equivalent of :func:`GeoPath.centroid
    <detroit.geo.path.path.GeoPath.centroid>`.

    Parameters
    ----------
    obj : GeoJSON
        GeoJSON object

    Returns
    -------
    Point2D
        Spherical centroid
    """
    stream = CentroidStream()
    geo_stream(obj, stream)
    return stream.result()
