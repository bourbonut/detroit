from math import atan, cos, fabs, nan, pi, sin

from ..common import LineStream
from .clip import clip

half_pi = pi * 0.5
EPSILON = 1e-6


class ClipAntimeridianLine(LineStream):
    def __init__(self, stream: LineStream):
        self._lambda0 = nan
        self._phi0 = nan
        self._sign0 = nan
        self._clean = None
        self._stream = stream

    def line_start(self):
        self._stream.line_start()
        self._clean = 1

    def line_end(self):
        self._stream.line_end()
        self._lambda0 = nan
        self._phi0 = nan

    def point(self, lambda1: float, phi1: float):
        sign1 = pi if lambda1 > 0 else -pi
        delta = fabs(lambda1 - self._lambda0)

        if abs(delta - pi) < EPSILON:
            self._phi0 = half_pi if (self._phi0 + phi1) * 0.5 > 0 else -half_pi
            self._stream.point(self._lambda0, self._phi0)
            self._stream.point(self._sign0, self._phi0)
            self._stream.line_end()
            self._stream.line_start()
            self._stream.point(sign1, self._phi0)
            self._stream.point(lambda1, self._phi0)
            self._clean = 0
        elif self._sign0 != sign1 and delta >= pi:
            if fabs(self._lambda0 - self._sign0) < EPSILON:
                self._lambda0 -= self._sign0 * EPSILON
            if fabs(lambda1 - sign1) < EPSILON:
                lambda1 -= sign1 * EPSILON
            self._phi0 = clip_antimeridian_intersect(
                self._lambda0, self._phi0, lambda1, phi1
            )
            self._stream.point(self._sign0, self._phi0)
            self._stream.line_end()
            self._stream.line_start()
            self._stream.point(sign1, self._phi0)
            self._clean = 0
        self._lambda0 = lambda1
        self._phi0 = phi1
        self._stream.point(self._lambda0, self._phi0)
        self._sign0 = sign1

    def clean(self) -> int:
        return 2 - self._clean

    def __str__(self):
        return f"ClipAntimeridianLine({self._stream})"


def clip_antimeridian_intersect(
    lambda0: float, phi0: float, lambda1: float, phi1: float
) -> float:
    sin_lambd0_lambda1 = sin(lambda0 - lambda1)
    if abs(sin_lambd0_lambda1) > EPSILON:
        cos_phi0 = cos(phi0)
        cos_phi1 = cos(phi1)
        return atan(
            (sin(phi0) * cos_phi1 * sin(lambda1) - sin(phi1) * cos_phi0 * sin(lambda0))
            / (cos_phi0 * cos_phi1 * sin_lambd0_lambda1)
        )
    else:
        return (phi0 + phi1) * 0.5


def clip_antimeridian_interpolate(
    vfrom: float | None,
    vto: float | None,
    direction: float,
    stream: LineStream,
):
    if vfrom is None:
        phi = direction * half_pi
        stream.point(-pi, phi)
        stream.point(0, phi)
        stream.point(pi, phi)
        stream.point(pi, 0)
        stream.point(pi, -phi)
        stream.point(0, -phi)
        stream.point(-pi, -phi)
        stream.point(-pi, 0)
        stream.point(-pi, phi)
    elif abs(vfrom[0] - vto[0]) > EPSILON:
        lambda_ = pi if vfrom[0] < vto[0] else -pi
        phi = direction * lambda_ * 0.5
        stream.point(-lambda_, phi)
        stream.point(0, phi)
        stream.point(lambda_, phi)
    else:
        stream.point(vto[0], vto[1])


def visible(*args) -> bool:
    return True


geo_clip_antimeridian = clip(
    visible, ClipAntimeridianLine, clip_antimeridian_interpolate, [-pi, -half_pi]
)
geo_clip_antimeridian.__doc__ = """
A clipping function which transforms a stream such that geometries (lines or
polygons) that cross the antimeridian line are cut in two, one on each side.
Typically used for pre-clipping.

Returns
-------
Callable[[PolygonStream], ClipRectangle]
    Clipping function
"""
