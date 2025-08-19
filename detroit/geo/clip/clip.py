from .buffer import ClipBuffer
from .rejoin import clip_rejoin
from ..polygon_contains import polygon_contains
from itertools import chain
from math import pi

EPSILON = 1e-6

def valid_segment(segment):
    return len(segment) > 1

def compare_intersection(point):
    point = point.x
    return point[1] - pi * 0.5 - EPSILON if point[0] < 0 else 0.5 * pi - point[1]

class Clip:

    def __init__(self, point_visible, clip_line, interpolate, start, sink):
        self._line = clip_line(sink)
        self._ring_buffer = ClipBuffer()
        self._ring_sink = clip_line(self._ring_buffer)
        self._polygon_started = False
        self._polygon = None
        self._segments = None
        self._ring = None

        self._start = start
        self._sink = sink
        self._point_visible = point_visible
        self._interpolate = interpolate

        self._line_start = self._line_start_default
        self._line_end = self._line_end_default
        self._point = self._point_default

    def line_start(self):
        return self._line_start()

    def line_end(self):
        return self._line_end()

    def polygon_start(self):
        self._point = self._point_ring
        self._line_start = self._ring_start
        self._line_end = self._ring_end
        self._segments = []
        self._polygon = []

    def polygon_end(self):
        self._point = self._point_default
        self._line_start = self._line_start_default
        self._line_end = self._line_end_default
        self._segments = list(chain.from_iterable(self._segments))
        start_inside = polygon_contains(self._polygon, self._start)
        if len(self._segments) > 0:
            if not self._polygon_started:
                self._sink.polygon_start()
                self._polygon_started = True
            clip_rejoin(self._segments, compare_intersection, start_inside, self._interpolate, self._sink)
        elif start_inside:
            if not self._polygon_started:
                self._sink.polygon_start()
                self._polygon_started = True
            self._sink.line_start()
            self._interpolate(None, None, 1, self._sink)
            self._sink.line_end()
            if self._polygon_started:
                self._sink.polygon_end()
                self._polygon_started = False
            self._segments = None
            self._polygon = None

    def sphere(self):
        self._sink.polygon_start()
        self._sink.line_start()
        self._interpolate(None, None, 1, self._sink)
        self._sink.line_end()
        self._sink.polygon_end()

    def point(self, lambda_, phi):
        return self._point(lambda_, phi)

    def _point_default(self, lambda_, phi):
        if self._point_visible(lambda_, phi):
            self._sink.point(lambda_, phi)

    def _line_start_default(self):
        self._point = self._point_line
        self._line.line_start()

    def _line_end_default(self):
        self._point = self._point_default
        self._line.line_end()

    def _point_ring(self, lambda_, phi):
        self._ring.append([lambda_, phi])
        self._ring_sink.point(lambda_, phi)

    def _ring_start(self):
        self._ring_sink.line_start()
        self._ring = []

    def _ring_end(self):
        self._point_ring(self._ring[0][0], self._ring[0][1])
        self._ring_sink.line_end()

        clean = self._ring_sink.clean()
        ring_segments = self._ring_buffer.result()
        n = len(ring_segments)

        self._ring.pop()
        self._polygon.append(self._ring)
        self._ring = None

        if n == 0:
            return

        if clean & 1:
            segment = ring_segments[0]
            m = len(segment) - 1
            if m > 0:
                if not self._polygon_started:
                    self._sink.polygon_start()
                    self._polygon_started = True
                self._sink.line_start()
                for i in range(m):
                    point = segment[i]
                    self._sink.point(point[0], point[1])
                self._sink.line_end()
            return

        if n > 1 and clean & 2:
            ring_segments.append(ring_segments.pop() + ring_segments.pop(0))
        self._segments.append(list(filter(valid_segment, ring_segments)))

def clip(point_visible, clip_line, interpolate, start):
    def wrapper(sink):
        return Clip(point_visible, clip_line, interpolate, start, sink)
    return wrapper
