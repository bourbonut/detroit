from ..cartesian import cartesian
from math import asin, atan2, cos, radians, sqrt, nan
from ..transform import GeoTransformer
from ..common import PolygonStream
from typing import TypeVar

ProjectionMutator = TypeVar("ProjectionMutator")

EPSILON = 1e-6
max_depth = 16
cos_min_distance = cos(radians(30))

def resample_none(project: ProjectionMutator) -> GeoTransformer:
    def point(self, x: float, y: float):
        x = project(x, y)
        self._stream.point(x[0], x[1])
    return GeoTransformer({"point": point})

class Resample(PolygonStream):
    def __init__(self, project: ProjectionMutator, delta2: float, stream: PolygonStream):
        self._project = project
        self._delta2 = delta2
        self._stream = stream

        self._lambda00 = None
        self._x00 = None
        self._y00 = None
        self._a00 = None
        self._b00 = None
        self._c00 = None
        self._lambda0 = None
        self._x0 = None
        self._y0 = None
        self._a0 = None
        self._b0 = None
        self._c0 = None

        self._point = self._point_default
        self._line_start = self._line_start_default
        self._line_end = self._line_end_default

    def resample_line_to(self, x0, y0, lambda0, a0, b0, c0, x1, y1, lambda1, a1, b1, c1, depth):
        dx = x1 - x0
        dy = y1 - y0
        d2 = dx * dx + dy * dy
        if d2 > 4 * self._delta2 and depth:
            depth -= 1
            a = a0 + a1
            b = b0 + b1
            c = c0 + c1
            m = sqrt(a * a + b * b + c * c)
            c /= m
            phi2 = asin(c)
            if abs(abs(c) - 1) < EPSILON or abs(lambda0 - lambda1) < EPSILON:
                lambda2 = (lambda0 + lambda1) / 2
            else:
                lambda2 = atan2(b, a)
            p = self._project(lambda2, phi2)
            x2 = p[0]
            y2 = p[1]
            dx2 = x2 - x0
            dy2 = y2 - y0
            dz = dy * dx2 - dx * dy2
            if (
                dz * dz / d2 > self._delta2
                or abs((dx * dx2 + dy * dy2) / d2 - 0.5) > 0.3
                or a0 * a1 + b0 * b1 + c0 * c1 < cos_min_distance
            ):
                a /= m
                b /= m
                self.resample_line_to(x0, y0, lambda0, a0, b0, c0, x2, y2, lambda2, a, b, c, depth)
                self._stream.point(x2, y2)
                self.resample_line_to(x2, y2, lambda2, a, b, c, x1, y1, lambda1, a1, b1, c1, depth)

    def line_start(self):
        self._line_start()

    def line_end(self):
        self._line_end()

    def point(self, lambda_, phi):
        return self._point(lambda_, phi)

    def polygon_start(self):
        self._stream.polygon_start()
        self._line_start = self.ring_start

    def polygon_end(self):
        self._stream.polygon_end()
        self._line_start = self._line_start_default

    def _point_default(self, x, y):
        x = self._project(x, y)
        self._stream.point(x[0], x[1])

    def _line_start_default(self):
        self._x0 = nan
        self._y0 = nan
        self._point = self._line_point
        self._stream.line_start()

    def _line_point(self, lambda_: float, phi: float):
        c = cartesian([lambda_, phi])
        p = self._project(lambda_, phi)
        self.resample_line_to(
            self._x0,
            self._y0,
            self._lambda0,
            self._a0,
            self._b0,
            self._c0,
            p[0],
            p[1],
            lambda_,
            c[0],
            c[1],
            c[2],
            max_depth,
        )
        self._x0 = p[0]
        self._y0 = p[1]
        self._lambda0 = lambda_
        self._a0 = c[0]
        self._b0 = c[1]
        self._c0 = c[2]
        self._stream.point(self._x0, self._y0)

    def _line_end_default(self):
        self._point = self._point_default
        self._stream.line_end()

    def ring_start(self):
        self._line_start_default()
        self._point = self.ring_point
        self._line_end = self.ring_end

    def ring_point(self, lambda_: float, phi: float):
        self._lambda00 = lambda_
        self._line_point(lambda_, phi)
        self._x00 = self._x0
        self._y00 = self._y0
        self._a00 = self._a0
        self._b00 = self._b0
        self._c00 = self._c0
        self._point = self._line_point

    def ring_end(self):
        self.resample_line_to(
            self._x0,
            self._y0,
            self._lambda0,
            self._a0,
            self._b0,
            self._c0,
            self._x00,
            self._y00,
            self._lambda00,
            self._a00,
            self._b00,
            self._c00,
            max_depth
        )
        self._line_end = self._line_end_default
        self._line_end_default()

    def __str__(self):
        return f"Resample({self._stream})"

def resample(project: ProjectionMutator, delta2: float):
    if delta2:
        def resample(stream: PolygonStream) -> Resample:
            return Resample(project, delta2, stream)
        return resample
    else:
        return resample_none(project)
