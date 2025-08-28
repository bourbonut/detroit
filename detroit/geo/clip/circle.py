from collections.abc import Callable
from math import cos, pi, radians, sqrt

from ...array import argpass
from ...types import Point2D
from ..cartesian import (
    cartesian,
    cartesian_add_in_place,
    cartesian_cross,
    cartesian_dot,
    cartesian_scale,
    spherical,
)
from ..circle import circle_stream
from ..common import LineStream, PolygonStream, Stream
from ..point_equal import point_equal
from .clip import Clip, clip

EPSILON = 1e-6


class ClipCircle(LineStream):
    def __init__(
        self,
        radius: float,
        cr: float,
        delta: float,
        small_radius: bool,
        not_hemisphere: bool,
        stream: Stream,
    ):
        self._radius = radius
        self._cr = cr
        self._delta = delta
        self._small_radius = small_radius
        self._not_hemisphere = not_hemisphere

        self._stream = stream
        self._point0 = None
        self._c0 = None
        self._v0 = None
        self._v00 = None
        self._clean = None

    def line_start(self):
        self._v00 = False
        self._v0 = False
        self._clean = 1

    def point(self, lambda_: float, phi: float):
        point1 = [lambda_, phi]
        v = cos(lambda_) * cos(phi) > self._cr
        c = 0
        if self._small_radius and not v:
            c = self._code(lambda_, phi)
        elif v:
            cst = pi if lambda_ < 0 else -pi
            c = self._code(lambda_ + cst, phi)

        if not self._point0:
            self._v00 = v
            self._v0 = v
            if v:
                self._stream.line_start()
        if v != self._v0:
            point2 = self._intersect(self._point0, point1)
            if (
                not point2
                or point_equal(self._point0, point2)
                or point_equal(point1, point2)
            ):
                if len(point1) == 2:
                    point2.append(1)
                else:
                    point1[2] = 1

        if v != self._v0:
            self._clean = 0
            if v:
                self._stream.line_start()
                point2 = self._intersect(point1, self._point0)
                self._stream.point(point2[0], point2[1])
            else:
                point2 = self._intersect(self._point0, point1)
                argpass(self._stream.point)(point2[0], point2[1], 2)
                self._stream.line_end()
            self._point0 = point2
        elif self._not_hemisphere and self._point0 and self._small_radius ^ v:
            t = self._intersect(point1, self._point0, True)
            if not (c & self._c0) and t:
                self._clean = 0
                if self._small_radius:
                    self._stream.line_start()
                    self._stream.point(t[0][0], t[0][1])
                    self._stream.point(t[1][0], t[1][1])
                    self._stream.line_end()
                else:
                    self._stream.point(t[1][0], t[1][1])
                    self._stream.line_end()
                    self._stream.line_start()
                    argpass(self._stream.point)(t[0][0], t[0][1], 3)
        if v and (not self._point0 or not point_equal(self._point0, point1)):
            self._stream.point(point1[0], point1[1])
        self._point0 = point1
        self._v0 = v
        self._c0 = c

    def line_end(self):
        if self._v0:
            self._stream.line_end()
        self._point0 = None

    def clean(self) -> int:
        return self._clean | ((self._v00 and self._v0) << 1)

    def _intersect(self, a: Point2D, b: Point2D, two: bool = False) -> Point2D:
        pa = cartesian(a)
        pb = cartesian(b)

        n1 = [1, 0, 0]
        n2 = cartesian_cross(pa, pb)
        n2n2 = cartesian_dot(n2, n2)
        n1n2 = n2[0]
        determinant = n2n2 - n1n2 * n1n2

        if not determinant:
            return not two and a

        c1 = self._cr * n2n2 / determinant
        c2 = -self._cr * n1n2 / determinant
        n1xn2 = cartesian_cross(n1, n2)
        A = cartesian_scale(n1, c1)
        B = cartesian_scale(n2, c2)
        cartesian_add_in_place(A, B)

        u = n1xn2
        w = cartesian_dot(A, u)
        uu = cartesian_dot(u, u)
        t2 = w * w - uu * (cartesian_dot(A, A) - 1)

        if t2 < 0:
            return

        t = sqrt(t2)
        q = cartesian_scale(u, (-w - t) / uu)
        cartesian_add_in_place(q, A)
        q = spherical(q)

        if not two:
            return q

        lambda0 = a[0]
        lambda1 = b[0]
        phi0 = a[1]
        phi1 = b[1]

        if lambda1 < lambda0:
            z = lambda0
            lambda0 = lambda1
            lambda1 = z

        delta = lambda1 - lambda0
        polar = abs(delta - pi) < EPSILON
        meridian = polar or delta < EPSILON

        if not polar and phi1 < phi0:
            z = phi0
            phi0 = phi1
            phi1 = z

        condition = (delta > pi) ^ (lambda0 <= q[0] and q[0] <= lambda1)
        if meridian:
            if polar:
                cst = phi0 if EPSILON else phi1
                condition = (phi0 + phi1 > 0) ^ (q[1] < (abs(q[0] - lambda0) < cst))
            else:
                condition = phi0 <= q[1] and q[1] <= phi1

        if condition:
            q1 = cartesian_scale(u, (-w + t) / uu)
            cartesian_add_in_place(q1, A)
            return [q, spherical(q1)]

    def _code(self, lambda_: float, phi: float) -> int:
        r = self._radius if self._small_radius else pi - self._radius
        code = 0
        if lambda_ < -r:
            code |= 1
        elif lambda_ > r:
            code |= 2
        if phi < -r:
            code |= 4
        elif phi > r:
            code |= 8
        return code


class ClipCircleWrapper:
    def __init__(self, angle: float):
        self._angle = angle
        self._cr = cos(angle)
        self._delta = radians(2)
        self._small_radius = self._cr > 0
        self._not_hemisphere = abs(self._cr) > EPSILON
        self._start = (
            [0, -self._angle] if self._small_radius else [-pi, self._angle - pi]
        )

    def clip_line(self, stream: Stream) -> ClipCircle:
        return ClipCircle(
            self._angle,
            self._cr,
            self._delta,
            self._small_radius,
            self._not_hemisphere,
            stream,
        )

    def interpolate(
        self,
        vfrom: float | None,
        vto: float | None,
        direction: float,
        stream: LineStream,
    ):
        circle_stream(stream, self._angle, self._delta, direction, vfrom, vto)

    def visible(self, lambda_: float, phi: float) -> bool:
        return cos(lambda_) * cos(phi) > self._cr

    @property
    def start(self) -> Point2D:
        return self._start


def geo_clip_circle(angle: float) -> Callable[[PolygonStream], Clip]:
    """
    Generates a clipping function which transforms a stream such that
    geometries are bounded by a small circle of radius angle around the
    projection's center. Typically used for pre-clipping.


    Parameters
    ----------
    angle : float
        Radius Angle value around the projection's center

    Returns
    -------
    Callable[[PolygonStream], Clip]
        Clipping function
    """
    clip_circle = ClipCircleWrapper(angle)
    return clip(
        clip_circle.visible,
        clip_circle.clip_line,
        clip_circle.interpolate,
        clip_circle.start,
    )
