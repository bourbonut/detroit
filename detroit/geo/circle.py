from .cartesian import cartesian, cartesian_normalize_in_place, spherical
from .constant import constant
from .rotation import RotateRadians
from math import acos, cos, degrees, radians, sin, pi

EPISLON = 1e-6
TAU = 2 * pi

def circle_stream(stream, radius, delta, direction, t0=None, t1=None):
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

def circle_radius(cos_radius, point):
    point = cartesian(point)
    point[0] -= cos_radius
    cartesian_normalize_in_place(point)
    radius = acos(-point[1])
    radius = -radius if -point[2] < 0 else radius
    return (radius + TAU - EPISLON) % TAU

class GeoCircle:

    def __init__(self):
        self._center = constant([0, 0])
        self._radius = constant(90)
        self._precision = constant(2)
        self._ring = None
        self._rotate = None
        self._stream = self

    def __call__(self, *args):
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

    def point(self, x, y):
        x = self._rotate(x, y)
        self._ring.append(x)
        x[0] = degrees(x[0])
        x[1] = degrees(x[1])
    
    def set_center(self, center):
        if callable(center):
            self._center = center
        else:
            self._center = constant(center)
        return self

    def set_radius(self, radius):
        if callable(radius):
            self._radius = radius
        else:
            self._radius = constant(radius)
        return self

    def set_precision(self, precision):
        if callable(precision):
            self._precision = precision
        else:
            self._precision = constant(precision)
        return self

def geo_circle() -> GeoCircle:
    return GeoCircle()
