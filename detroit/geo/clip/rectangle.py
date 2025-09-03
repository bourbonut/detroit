from collections.abc import Callable
from itertools import chain
from math import nan

from ...types import Point2D
from ..common import PolygonStream
from .buffer import ClipBuffer
from .line import clip_line
from .rejoin import EPSILON, Intersection, clip_rejoin

clip_max = 1e9
clip_min = -1e9


def clamp(x):
    if x > clip_max:
        return clip_max
    if x < clip_min:
        return clip_min
    return x


class ClipRectangle(PolygonStream):
    def __init__(
        self, x0: float, y0: float, x1: float, y1: float, stream: PolygonStream
    ):
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1
        self._stream = stream

        self._point = self._point_default

        self._active_stream = stream
        self._buffer_stream = ClipBuffer()
        self._segments = None
        self._polygon = None
        self._fpx = None
        self._fpy = None
        self._fpv = None
        self._ppx = None
        self._ppy = None
        self._ppv = None
        self._ring = None
        self._clean = None

    def _visible(self, x: float, y: float) -> bool:
        return self._x0 <= x <= self._x1 and self._y0 <= y <= self._y1

    def _interpolate(
        self,
        vfrom: float | None,
        vto: float | None,
        direction: float,
        stream: PolygonStream,
    ):
        a = 0
        a1 = 0
        if vfrom is not None:
            a = self._corner(vfrom, direction)
            a1 = self._corner(vto, direction)
        if (
            vfrom is None
            or (a != a1)
            or (self._compare_point(vfrom, vto) < 0) ^ (direction > 0)
        ):
            while True:
                x = self._x0 if a == 0 or a == 3 else self._x1
                y = self._y1 if a > 1 else self._y0
                stream.point(x, y)
                a = (a + direction + 4) % 4
                if a == a1:
                    break
        else:
            stream.point(vto[0], vto[1])

    def _corner(self, p: Point2D, direction: float) -> int:
        if abs(p[0] - self._x0) < EPSILON:
            return 0 if direction > 0 else 3
        elif abs(p[0] - self._x1) < EPSILON:
            return 2 if direction > 0 else 1
        elif abs(p[1] - self._y0) < EPSILON:
            return 1 if direction > 0 else 0
        return 3 if direction > 0 else 2

    def _compare_intersection(self, a: Intersection, b: Intersection) -> float:
        return self._compare_point(a.x, b.x)

    def _compare_point(self, a: Point2D, b: Point2D) -> float:
        ca = self._corner(a, 1)
        cb = self._corner(b, 1)
        if ca != cb:
            return ca - cb
        elif ca == 0:
            return b[1] - a[1]
        elif ca == 1:
            return a[0] - b[0]
        elif ca == 2:
            return a[1] - b[1]
        else:
            return b[0] - a[0]

    def point(self, x: float, y: float):
        return self._point(x, y)

    def _point_default(self, x: float, y: float):
        if self._visible(x, y):
            self._active_stream.point(x, y)

    def polygon_inside(self):
        winding = 0

        for ring in self._polygon:
            point = ring[0]
            b0 = point[0]
            b1 = point[1]
            for j in range(1, len(ring)):
                a0 = b0
                a1 = b1
                point = ring[j]
                b0 = point[0]
                b1 = point[1]
                if a1 <= self._y1:
                    if b1 > self._y1 and (b0 - a0) * (self._y1 - a1) > (b1 - a1) * (
                        self._x0 - a0
                    ):
                        winding += 1
                else:
                    if b1 <= self._y1 and (b0 - a0) * (self._y1 - a1) < (b1 - a1) * (
                        self._x0 - a0
                    ):
                        winding -= 1
        return winding

    def polygon_start(self):
        self._active_stream = self._buffer_stream
        self._segments = []
        self._polygon = []
        self._clean = True

    def polygon_end(self):
        start_inside = self.polygon_inside()
        clean_inside = self._clean and start_inside
        self._segments = list(chain.from_iterable(self._segments))
        visible = len(self._segments)
        if clean_inside or visible:
            self._stream.polygon_start()
            if clean_inside:
                self._stream.line_start()
                self._interpolate(None, None, 1, self._stream)
                self._stream.line_end()
            if visible:
                clip_rejoin(
                    self._segments,
                    self._compare_intersection,
                    start_inside,
                    self._interpolate,
                    self._stream,
                )
            self._stream.polygon_end()
        self._active_stream = self._stream
        self._segments = None
        self._polygon = None
        self._ring = None

    def line_start(self):
        self._point = self._line_point
        if self._polygon is not None:
            self._ring = []
            self._polygon.append(self._ring)
        self._first = True
        self._ppv = False
        self._ppx = nan
        self._ppy = nan

    def line_end(self):
        if self._segments is not None:
            self._line_point(self._fpx, self._fpy)
            if self._fpv and self._ppv:
                self._buffer_stream.rejoin()
            self._segments.append(self._buffer_stream.result())
        self._point = self._point_default
        if self._ppv:
            self._active_stream.line_end()

    def _line_point(self, x: float, y: float):
        v = self._visible(x, y)
        if self._polygon is not None:
            self._ring.append([x, y])
        if self._first:
            self._fpx = x
            self._fpy = y
            self._fpv = v
            self._first = False
            if v:
                self._active_stream.line_start()
                self._active_stream.point(x, y)
        else:
            if v and self._ppv:
                self._active_stream.point(x, y)
            else:
                self._ppx = clamp(self._ppx)
                self._ppy = clamp(self._ppy)
                x = clamp(x)
                y = clamp(y)
                if result := clip_line(
                    self._ppx, self._ppy, x, y, self._x0, self._y0, self._x1, self._y1
                ):
                    x1, y1, x2, y2 = result
                    if not self._ppv:
                        self._active_stream.line_start()
                        self._active_stream.point(x1, y1)
                    self._active_stream.point(x2, y2)
                    if not v:
                        self._active_stream.line_end()
                    self._clean = False
                elif v:
                    self._active_stream.line_start()
                    self._active_stream.point(x, y)
                    self._clean = False
        self._ppx = x
        self._ppy = y
        self._ppv = v

    def __str__(self) -> str:
        return f"ClipRectangle({self._stream}, {[[self._x0, self._y0], [self._x1, self._y1]]})"


class ClipRectangleWrapper:
    def __init__(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
    ):
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1

    def __call__(self, stream: PolygonStream):
        return ClipRectangle(self._x0, self._y0, self._x1, self._y1, stream)


def geo_clip_rectangle(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
) -> Callable[[PolygonStream], ClipRectangle]:
    """
    Generates a clipping function which transforms a stream such that
    geometries are bounded by a rectangle of coordinates :math:`[[x_0, y_0],
    [x_1, y_1]]`. Typically used for post-clipping.

    Parameters
    ----------
    x0 : float
        :math:`x_0` coordinate of the rectangle
    y0 : float
        :math:`y_0` coordinate of the rectangle
    x1 : float
        :math:`x_1` coordinate of the rectangle
    y1 : float
        :math:`y_1` coordinate of the rectangle

    Returns
    -------
    Callable[[PolygonStream], ClipRectangle]
        Clipping function
    """

    return ClipRectangleWrapper(x0, y0, x1, y1)
