from collections.abc import Callable
from math import acos, cos, degrees, pi, radians, sin
from typing import Any, TypeVar

from ..types import GeoJSON, Point2D, Point3D
from .cartesian import cartesian, cartesian_normalize_in_place, spherical
from .common import LineStream
from .constant import constant
from .rotation import RotateRadians

TGeoCircle = TypeVar("GeoCircle", bound="GeoCircle")

EPISLON = 1e-6
TAU = 2 * pi


def circle_stream(
    stream: LineStream,
    radius: float,
    delta: float,
    direction: float,
    t0: float | None = None,
    t1: float | None = None,
):
    if not delta:
        return

    cos_radius = cos(radius)
    sin_radius = sin(radius)
    step = direction * delta

    if t0 is None:
        t0 = radius + direction * TAU
        t1 = radius - step * 0.5
    else:
        t0 = circle_radius(cos_radius, t0)
        t1 = circle_radius(cos_radius, t1)
        condition = t0 < t1 if direction > 0 else t0 > t1
        if condition:
            t0 += direction * TAU

    t = t0
    while True:
        point = spherical([cos_radius, -sin_radius * cos(t), -sin_radius * sin(t)])
        stream.point(point[0], point[1])
        t -= step
        condition = t < t1 if direction > 0 else t > t1
        if condition:
            break


def circle_radius(cos_radius: float, point: Point3D) -> float:
    point = cartesian(point)
    point[0] -= cos_radius
    cartesian_normalize_in_place(point)
    radius = acos(-point[1])
    radius = -radius if -point[2] < 0 else radius
    return (radius + TAU - EPISLON) % TAU


class GeoCircle:
    """
    Circle generator
    """

    def __init__(self):
        self._center = constant([0, 0])
        self._radius = constant(90)
        self._precision = constant(2)
        self._ring = None
        self._rotate = None
        self._stream = self

    def __call__(self, *args: Any) -> GeoJSON:
        """
        Returns a new GeoJSON geometry object of type "Polygon" approximating a
        circle on the surface of a sphere, with the current center, radius and
        precision. Any arguments are passed to the accessors.


        Parameters
        ----------
        *args : Any
            Arguments passed to the accessors

        Returns
        -------
        GeoJSON
            GeoJSON object
        """
        c = self._center(*args)
        r = radians(self._radius(*args))
        p = radians(self._precision(*args))
        self._ring = []
        self._rotate = RotateRadians(radians(-c[0]), radians(-c[1]), 0).invert
        circle_stream(self._stream, r, p, 1)
        c = {"type": "Polygon", "coordinates": [self._ring]}
        self._ring = None
        self._rotate = None
        return c

    def point(self, x: float, y: float):
        x = self._rotate(x, y)
        self._ring.append(x)
        x[0] = degrees(x[0])
        x[1] = degrees(x[1])

    def set_center(self, center: Callable[..., Point2D] | Point2D) -> TGeoCircle:
        """
        If center is specified, sets the circle center to the specified point
        :code:`[longitude, latitude]` in degrees, and returns this circle
        generator. The center may also be specified as a function.

        Parameters
        ----------
        center : Callable[..., Point2D] | Point2D
            Center function or constant value

        Returns
        -------
        GeoCircle
            Itself
        """
        if callable(center):
            self._center = center
        else:
            self._center = constant(center)
        return self

    def set_radius(self, radius: Callable[..., float] | float) -> TGeoCircle:
        """
        If radius is specified, sets the circle radius to the specified angle
        in degrees, and returns this circle generator. The radius may also be
        specified as a function.

        Parameters
        ----------
        radius : Callable[..., float] | float
            Radius function or constant value

        Returns
        -------
        GeoCircle
            Itself
        """
        if callable(radius):
            self._radius = radius
        else:
            self._radius = constant(radius)
        return self

    def set_precision(self, precision: Callable[..., float] | float) -> TGeoCircle:
        """
        If precision is specified, sets the circle precision to the specified
        angle in degrees, and returns this circle generator. The precision may
        also be specified as a function.

        Parameters
        ----------
        precision : Callable[..., float] | float
            Precision function or constant value

        Returns
        -------
        GeoCircle
            Itself
        """
        if callable(precision):
            self._precision = precision
        else:
            self._precision = constant(precision)
        return self


def geo_circle() -> GeoCircle:
    """
    Returns a new circle generator.

    Returns
    -------
    GeoCircle
        GeoCircle
    """
    return GeoCircle()
