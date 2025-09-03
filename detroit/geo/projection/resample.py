from collections.abc import Callable
from math import asin, atan2, cos, fabs, hypot, nan, radians

from ..cartesian import cartesian
from ..common import PolygonStream, Projection
from ..transform import GeoTransformer

EPSILON = 1e-6
max_depth = 16
cos_min_distance = cos(radians(30))


def resample_none(project: Projection) -> GeoTransformer:
    def point(self, x: float, y: float):
        a, b = project(x, y)
        self._stream.point(a, b)

    return GeoTransformer({"point": point})


class Resample(PolygonStream):
    def __init__(self, project: Projection, delta2: float, stream: PolygonStream):
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

    def resample_line_to(
        self, x0, y0, lambda0, a0, b0, c0, x1, y1, lambda1, a1, b1, c1, depth
    ):
        dx = x1 - x0
        dy = y1 - y0
        d2 = dx * dx + dy * dy
        if d2 > 4 * self._delta2 and depth:
            depth -= 1
            a = a0 + a1
            b = b0 + b1
            c = c0 + c1
            m = hypot(a, b, c)
            c /= m
            if fabs(fabs(c) - 1.0) < EPSILON or fabs(lambda0 - lambda1) < EPSILON:
                lambda2 = (lambda0 + lambda1) * 0.5
            else:
                lambda2 = atan2(b, a)
            x2, y2 = self._project(lambda2, asin(c))
            dx2 = x2 - x0
            dy2 = y2 - y0
            dz = dy * dx2 - dx * dy2
            if (
                dz * dz / d2 > self._delta2
                or fabs((dx * dx2 + dy * dy2) / d2 - 0.5) > 0.3
                or a0 * a1 + b0 * b1 + c0 * c1 < cos_min_distance
            ):
                a /= m
                b /= m
                self.resample_line_to(
                    x0, y0, lambda0, a0, b0, c0, x2, y2, lambda2, a, b, c, depth
                )
                self._stream.point(x2, y2)
                self.resample_line_to(
                    x2, y2, lambda2, a, b, c, x1, y1, lambda1, a1, b1, c1, depth
                )

    def line_start(self):
        self._line_start()

    def line_end(self):
        self._line_end()

    def point(self, lambda_: float, phi: float):
        return self._point(lambda_, phi)

    def polygon_start(self):
        self._stream.polygon_start()
        self._line_start = self.ring_start

    def polygon_end(self):
        self._stream.polygon_end()
        self._line_start = self._line_start_default

    def _point_default(self, x: float, y: float):
        a, b = self._project(x, y)
        self._stream.point(a, b)

    def _line_start_default(self):
        self._x0 = nan
        self._y0 = nan
        self._point = self._line_point
        self._stream.line_start()

    def _line_point(self, lambda_: float, phi: float):
        a1, b1, c1 = cartesian([lambda_, phi])
        x1, y1 = self._project(lambda_, phi)
        self.resample_line_to(
            self._x0,
            self._y0,
            self._lambda0,
            self._a0,
            self._b0,
            self._c0,
            x1,
            y1,
            lambda_,
            a1,
            b1,
            c1,
            max_depth,
        )
        self._x0 = x1
        self._y0 = y1
        self._lambda0 = lambda_
        self._a0 = a1
        self._b0 = b1
        self._c0 = c1
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
            max_depth,
        )
        self._line_end = self._line_end_default
        self._line_end_default()

    def __str__(self):
        return f"Resample({self._stream})"


class ResampleWrapper:
    def __init__(self, project: Projection, delta2: float):
        self._project = project
        self._delta2 = delta2

    def __call__(self, stream: PolygonStream) -> Resample:
        return Resample(self._project, self._delta2, stream)


def resample(
    project: Projection, delta2: float
) -> Callable[[PolygonStream], PolygonStream]:
    if delta2:
        return ResampleWrapper(project, delta2)
    else:
        return resample_none(project)
