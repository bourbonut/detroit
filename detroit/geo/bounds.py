from functools import cmp_to_key
from math import degrees, fsum, inf, isinf, nan, radians

from ..types import GeoJSON, Point2D
from .area import AreaStream
from .cartesian import (
    cartesian,
    cartesian_cross,
    cartesian_normalize_in_place,
    spherical,
)
from .common import PolygonStream
from .stream import geo_stream

EPSILON = 1e-6


def angle(lambda0: float, lambda1: float) -> float:
    lambda1 -= lambda0
    return lambda1 + 360 if lambda1 < 0 else lambda1


def range_compare(a: Point2D, b: Point2D) -> float:
    return a[0] - b[0]


def range_contains(rang: Point2D, x: float) -> bool:
    if rang[0] <= rang[1]:
        return rang[0] <= x <= rang[1]
    else:
        return x < rang[0] or rang[1] < x


class BoundsStream(PolygonStream):
    def __init__(self):
        self._lambda0 = inf
        self._phi0 = inf
        self._lambda1 = -inf
        self._phi1 = -inf

        self._lambda2 = None

        self._lambda00 = None
        self._phi00 = None

        self._p0 = None
        self._delta_sum = []
        self._ranges = []
        self._range = [nan, nan]

        self._point = self._bounds_point
        self._line_start = self._bounds_line_start
        self._line_end = self._bounds_line_end

        self._area_stream = AreaStream()

    def point(self, x: float, y: float):
        return self._point(x, y)

    def line_start(self):
        return self._line_start()

    def line_end(self):
        return self._line_end()

    def polygon_start(self):
        self._point = self._bounds_ring_point
        self._line_start = self._bounds_ring_start
        self._line_end = self._bounds_ring_end
        self._delta_sum = []
        self._area_stream.polygon_start()

    def polygon_end(self):
        self._area_stream.polygon_end()
        self._point = self._bounds_point
        self._line_start = self._bounds_line_start
        self._line_end = self._bounds_line_end
        area_ring_sum = fsum(self._area_stream._area_ring_sum)
        delta_sum = fsum(self._delta_sum)
        if area_ring_sum < 0:
            self._lambda1 = 180
            self._lambda0 = -180
            self._phi1 = 90
            self._phi0 = -90
        elif delta_sum > EPSILON:
            self._phi1 = 90
        elif delta_sum < -EPSILON:
            self._phi0 = -90
        self._range[0] = self._lambda0
        self._range[1] = self._lambda1

    def sphere(self):
        self._lambda1 = 180
        self._lambda0 = -180
        self._phi1 = 90
        self._phi0 = -90

    def _bounds_point(self, lambda_: float, phi: float):
        self._lambda0 = lambda_
        self._lambda1 = lambda_
        self._range = [self._lambda0, self._lambda1]
        self._ranges.append(self._range)
        if phi < self._phi0:
            self._phi0 = phi
        if phi > self._phi1:
            self._phi1 = phi

    def _line_point(self, lambda_: float, phi: float):
        p = cartesian([radians(lambda_), radians(phi)])
        if self._p0:
            normal = cartesian_cross(self._p0, p)
            equatorial = [normal[1], -normal[0], 0]
            inflection = cartesian_cross(equatorial, normal)
            cartesian_normalize_in_place(inflection)
            inflection = spherical(inflection)
            delta = lambda_ - self._lambda2
            sign = 1 if delta > 0 else -1
            lambdai = degrees(inflection[0]) * sign
            antimeridian = abs(delta) > 180

            if antimeridian ^ (
                sign * self._lambda2 < lambdai and lambdai < sign * lambda_
            ):
                phii = degrees(inflection[1])
                if phii > self._phi1:
                    self._phi1 = phii
            else:
                lambdai = (lambdai + 360) % 360 - 180
                if antimeridian ^ (
                    sign * self._lambda2 < lambdai and lambdai < sign * lambda_
                ):
                    phii = degrees(-inflection[1])
                    if phii < self._phi0:
                        self._phi0 = phii
                else:
                    if phi < self._phi0:
                        self._phi0 = phi
                    if phi > self._phi1:
                        self._phi1 = phi

            if antimeridian:
                if lambda_ < self._lambda2:
                    if angle(self._lambda0, lambda_) > angle(
                        self._lambda0, self._lambda1
                    ):
                        self._lambda1 = lambda_
                else:
                    if angle(lambda_, self._lambda1) > angle(
                        self._lambda0, self._lambda1
                    ):
                        self._lambda0 = lambda_
            else:
                if self._lambda1 >= self._lambda0:
                    if lambda_ < self._lambda0:
                        self._lambda0 = lambda_
                    if lambda_ > self._lambda1:
                        self._lambda1 = lambda_
                else:
                    if lambda_ > self._lambda2:
                        if angle(self._lambda0, lambda_) > angle(
                            self._lambda0, self._lambda1
                        ):
                            self._lambda1 = lambda_
                    else:
                        if angle(lambda_, self._lambda1) > angle(
                            self._lambda0, self._lambda1
                        ):
                            self._lambda0 = lambda_
        else:
            self._lambda0 = lambda_
            self._lambda1 = lambda_
            self._range = [self._lambda0, self._lambda1]
            self._ranges.append(self._range)

        if phi < self._phi0:
            self._phi0 = phi
        if phi > self._phi1:
            self._phi1 = phi
        self._p0 = p
        self._lambda2 = lambda_

    def _bounds_line_start(self):
        self._point = self._line_point

    def _bounds_line_end(self):
        self._range[0] = self._lambda0
        self._range[1] = self._lambda1
        self._point = self._bounds_point
        self._p0 = None

    def _bounds_ring_point(self, lambda_: float, phi: float):
        if self._p0:
            delta = lambda_ - self._lambda2
            if abs(delta) > 180:
                delta = delta + (360 if delta > 0 else -360)
            self._delta_sum.append(delta)
        else:
            self._lambda00 = lambda_
            self._phi00 = phi
        self._area_stream.point(lambda_, phi)
        self._line_point(lambda_, phi)

    def _bounds_ring_start(self):
        self._area_stream.line_start()

    def _bounds_ring_end(self):
        self._bounds_ring_point(self._lambda00, self._phi00)
        self._area_stream.line_end()
        delta_sum = fsum(self._delta_sum)
        if abs(delta_sum) > EPSILON:
            self._lambda1 = 180
            self._lambda0 = -180
        self._range[0] = self._lambda0
        self._range[1] = self._lambda1
        self._p0 = None

    def result(self) -> tuple[Point2D, Point2D]:
        if n := len(self._ranges):
            self._ranges.sort(key=cmp_to_key(range_compare))
            a = self._ranges[0]
            merged = [a]
            for i in range(1, n):
                b = self._ranges[i]
                if range_contains(a, b[0]) or range_contains(a, b[1]):
                    if angle(a[0], b[1]) > angle(a[0], a[1]):
                        a[1] = b[1]
                    if angle(b[0], a[1]) > angle(a[0], a[1]):
                        a[0] = b[0]
                else:
                    a = b
                    merged.append(a)

            delta_max = -inf
            n = len(merged)
            a = merged[n - 1]
            for i in range(n):
                b = merged[i]
                delta = angle(a[1], b[0])
                if delta > delta_max:
                    delta_max = delta
                    self._lambda0 = b[0]
                    self._lambda1 = a[1]
                a = b

        self._ranges = []
        self._range = []
        if isinf(self._lambda0) or isinf(self._phi0):
            return [[nan, nan], [nan, nan]]
        else:
            return [[self._lambda0, self._phi0], [self._lambda1, self._phi1]]


def geo_bounds(obj: GeoJSON) -> tuple[Point2D, Point2D]:
    """
    Returns the spherical bounding box for the specified GeoJSON object. The
    bounding box is represented by a two-dimensional array: :code:`[[left,
    bottom], [right, top]]`, where :code:`left` is the minimum longitude,
    :code:`bottom` is the minimum latitude, :code:`right` is maximum longitude,
    and :code:`top` is the maximum latitude. All coordinates are given in
    degrees. (Note that in projected planar coordinates, the minimum latitude
    is typically the maximum y-value, and the maximum latitude is typically the
    minimum y-value.) This is the spherical equivalent of :func:`GeoPath.bounds
    <detroit.geo.path.path.GeoPath.bounds>`.

    Parameters
    ----------
    obj : GeoJSON
        GeoJSON object

    Returns
    -------
    tuple[Point2D, Point2D]
        Spherical bounding box
    """
    stream = BoundsStream()
    geo_stream(obj, stream)
    return stream.result()
