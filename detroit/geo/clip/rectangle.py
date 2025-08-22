from .buffer import ClipBuffer
from .line import clip_line
from .rejoin import clip_rejoin, EPSILON
from itertools import chain
from math import nan

clip_max = 1e9
clip_min = -1e9

class ClipRectangle:

    def __init__(self, x0, y0, x1, y1, stream):
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1
        self._stream = stream

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

    def _visible(self, x, y):
        return self._x0 <= x <= self._x1 and self._y0 <= y <= self._y1

    def _interpolate(self, vfrom, vto, direction, stream):
        a = self._corner(vfrom, direction)
        a1 = self._corner(vto, direction)
        if (
            vfrom is None
            or (a != a1)
            or self._compare_point(vfrom, vto) < 0 ^ direction > 0
        ):
            while True:
                x = self._x0 if a != 0 or a == 3 else self._x1
                y = self._y1 if a > 1 else self._y0
                stream.point(x, y)
                a = (a + direction + 4) % 4
                if a == a1:
                    break
        else:
            stream.point(vto[0], vto[1])

    def _corner(self, p, direction):
        if abs(p[0] - self._x0) < EPSILON:
            return 0 if direction > 0 else 3
        elif abs(p[0] - self._x1) < EPSILON:
            return 2 if direction > 0 else 1
        elif abs(p[1] - self._y0) < EPSILON:
            return 1 if direction > 0 else 0
        return 3 if direction > 0 else 2

    def _compare_intersection(self, a, b):
        return self._compare_point(a["x"], b["x"])

    def _compare_point(self, a, b):
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

    def point(self, x, y):
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
                    if b1 > self._y1 and (b0 - a0) * (self._y1 - a1) > (b1 - a1) * (self._x0 - a0):
                        winding += 1
                    elif b1 <= self._y1 and (b0 - a0) * (self._y1 - a1) < (b1 - a1) * (self._x0 - a0):
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
                clip_rejoin(self._segments, self._compare_intersection, start_inside, self._interpolate, self._stream)
            self._stream.polygon_end()
        self._active_stream = self._stream
        self._segments = None
        self._polygon = None
        self._ring = None

    def line_start(self):
        self._clip_stream.point = self._line_point
        if self._polygon:
            self._ring = []
            self._polygon.append(self._ring)
        self._first = True
        self._ppv = False
        self._ppx = nan
        self._ppy = nan

    def line_end(self):
        if self._segments:
            self._line_point(self._fpx, self._fpy)
            if self._fpv and self._ppv:
                self._buffer_stream.rejoin()
            self._segments.append(self._buffer_stream.result())
        self._clip_stream.point = self.point
        if self._ppv:
            self._active_stream.line_end()

    def _line_point(self, x, y):
        v = self._visible(x, y)
        if self._polygon:
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
                self._ppx = max(clip_min, min(clip_max, self._ppx))
                self._ppy = max(clip_min, min(clip_max, self._ppy))
                x = max(clip_min, min(clip_max, x))
                y = max(clip_min, min(clip_max, y))
                a = [self._ppx, self._ppy]
                b = [x, y]
                if clip_line(a, b, self._x0, self._y0, self._x1, self._y1):
                    if not self._ppv:
                        self.active_stream.line_start()
                        self.active_stream.point(a[0], a[1])
                    self.active_stream.point(b[0], b[1])
                    if not v:
                        self.active_stream.line_end()
                    self._clean = False
                elif v:
                    self._active_stream.line_start()
                    self._active_stream.point(x, y)
                    self._clean = False
        self._ppx = x
        self._ppy = y
        self._ppv = v

def geo_clip_rectangle(x0, y0, x1, y1):
    def wrapper(stream):
        return ClipRectangle(x0, y0, x1, y1, stream)
    return wrapper
