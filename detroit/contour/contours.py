from inspect import signature
from math import floor, inf, isfinite, isnan, nan

from ..array import extent, nice, ticks
from ..array.threshold import threshold_sturges
from .area import area
from .constant import constant
from .contains import contains

CASES = [
    [],
    [[[1.0, 1.5], [0.5, 1.0]]],
    [[[1.5, 1.0], [1.0, 1.5]]],
    [[[1.5, 1.0], [0.5, 1.0]]],
    [[[1.0, 0.5], [1.5, 1.0]]],
    [[[1.0, 1.5], [0.5, 1.0]], [[1.0, 0.5], [1.5, 1.0]]],
    [[[1.0, 0.5], [1.0, 1.5]]],
    [[[1.0, 0.5], [0.5, 1.0]]],
    [[[0.5, 1.0], [1.0, 0.5]]],
    [[[1.0, 1.5], [1.0, 0.5]]],
    [[[0.5, 1.0], [1.0, 0.5]], [[1.5, 1.0], [1.0, 1.5]]],
    [[[1.5, 1.0], [1.0, 0.5]]],
    [[[0.5, 1.0], [1.5, 1.0]]],
    [[[1.0, 1.5], [1.5, 1.0]]],
    [[[0.5, 1.0], [1.0, 1.5]]],
    [],
]


def sign(x):
    return -1 if x < 0 else 1


def finite(x):
    return x if isfinite(x) else nan


def valid(v):
    if v is None or isnan(v):
        return -inf
    else:
        return v


def above(x, value):
    return False if x is None else (x >= value)


def get(values, index):
    index = int(index)
    return values[index] if index < len(values) else None


def smooth1(x, v0, v1, value):
    a = value - v0
    b = v1 - v0
    d = 0.0
    if isfinite(a) or isfinite(b):
        d = a / b if b != 0.0 else nan
    else:
        d = sign(a) / sign(b)
    return x if isnan(d) else x + d - 0.5


class Contours:
    def __init__(self):
        self._dx = 1
        self._dy = 1
        self._threshold = threshold_sturges
        self._smooth = self.smooth_linear

    def __call__(self, values):
        tz = self._threshold(values)
        if not isinstance(tz, list):
            e = extent(values, finite)
            tz = ticks(*nice(e[0], e[1], tz), tz)
            while tz[len(tz) - 1] >= e[1]:
                tz.pop()
            while tz[1] < e[0]:
                tz.pop(0)
        else:
            tz = sorted(tz)

        return list(map(lambda value: self.contour(values, value), tz))

    def contour(self, values, value):
        v = nan if value is None else value
        if not isinstance(v, (int, float)) or isnan(v):
            raise ValueError(f"Invalid value: {value}")

        polygons = []
        holes = []

        def callback(ring):
            args = [ring, values, v]
            nargs = len(signature(self._smooth).parameters)
            self._smooth(*args[:nargs])
            if area(ring) > 0:
                polygons.append([ring])
            else:
                holes.append(ring)

        self.isorings(values, v, callback)
        for hole in holes:
            for polygon in polygons:
                if contains(polygon[0], hole) != -1:
                    polygon.append(hole)
                    break

        return {
            "type": "MultiPolygon",
            "value": value,
            "coordinates": polygons,
        }

    def isorings(self, values, value, callback):
        fragment_by_start = {}
        fragment_by_end = {}

        x = y = -1

        def stitch(line):
            start = [line[0][0] + x, line[0][1] + y]
            end = [line[1][0] + x, line[1][1] + y]
            start_index = self.index(start)
            end_index = self.index(end)
            if f := fragment_by_end.get(start_index):
                if g := fragment_by_start.get(end_index):
                    fragment_by_end.pop(f["end"])
                    fragment_by_start.pop(g["start"])
                    if f == g:
                        f["ring"].append(end)
                        callback(f["ring"])
                    else:
                        fragment_by_start[f["start"]] = fragment_by_end[g["end"]] = {
                            "start": f["start"],
                            "end": g["end"],
                            "ring": f["ring"] + g["ring"],
                        }
                else:
                    fragment_by_end.pop(f["end"])
                    f["ring"].append(end)
                    f["end"] = end_index
                    fragment_by_end[end_index] = f
            elif f := fragment_by_start.get(end_index):
                if g := fragment_by_end.get(start_index):
                    fragment_by_start.pop(f["start"])
                    fragment_by_end.pop(g["end"])
                    if f == g:
                        f["ring"].append(end)
                        callback(f["ring"])
                    else:
                        fragment_by_start[g["start"]] = fragment_by_end[f["end"]] = {
                            "start": g["start"],
                            "end": f["end"],
                            "ring": g["ring"] + f["ring"],
                        }
                else:
                    fragment_by_start.pop(f["start"])
                    f["ring"].insert(0, start)
                    f["start"] = start_index
                    fragment_by_start[start_index] = f
            else:
                fragment_by_start[start_index] = fragment_by_end[end_index] = {
                    "start": start_index,
                    "end": end_index,
                    "ring": [start, end],
                }

        t1 = above(get(values, 0), value)
        for line in CASES[t1 << 1]:
            stitch(line)

        while x + 1 < self._dx - 1:
            x += 1
            t0 = t1
            t1 = above(get(values, x + 1), value)
            for line in CASES[t0 | t1 << 1]:
                stitch(line)
        x += 1
        for line in CASES[t1 << 0]:
            stitch(line)

        while y + 1 < self._dy - 1:
            y += 1
            x = -1
            t1 = above(get(values, y * self._dx + self._dx), value)
            t2 = above(get(values, y * self._dx), value)
            for line in CASES[t1 << 1 | t2 << 2]:
                stitch(line)
            while x + 1 < self._dx - 1:
                x += 1
                t0 = t1
                t1 = above(get(values, y * self._dx + self._dx + x + 1), value)
                t3 = t2
                t2 = above(get(values, y * self._dx + x + 1), value)
                for line in CASES[t0 | t1 << 1 | t2 << 2 | t3 << 3]:
                    stitch(line)
            x += 1
            for line in CASES[t1 | t2 << 3]:
                stitch(line)

        y += 1
        x = -1
        t2 = get(values, y * self._dx) >= value
        for line in CASES[t2 << 2]:
            stitch(line)
        while x + 1 < self._dx - 1:
            x += 1
            t3 = t2
            t2 = above(get(values, y * self._dx + x + 1), value)
            for line in CASES[t2 << 2 | t3 << 3]:
                stitch(line)

        x += 1
        for line in CASES[t2 << 3]:
            stitch(line)

    def smooth_linear(self, ring, values, value):
        for point in ring:
            x = point[0]
            y = point[1]
            xt = int(x)
            yt = int(y)
            v1 = valid(get(values, yt * self._dx + xt))
            if x > 0 and x < self._dx and xt == x:
                point[0] = smooth1(
                    x, valid(get(values, yt * self._dx + xt - 1)), v1, value
                )
            if y > 0 and y < self._dy and yt == y:
                point[1] = smooth1(
                    y, valid(get(values, (yt - 1) * self._dx + xt)), v1, value
                )

    def index(self, point):
        return int(point[0] * 2 + point[1] * (self._dx + 1) * 4)

    def set_size(self, size):
        dx = floor(size[0])
        dy = floor(size[1])
        if dx < 0.0 or dy < 0.0:
            raise ValueError("Invalid size: negative values")
        self._dx = dx
        self._dy = dy
        return self

    def set_thresholds(self, thresholds):
        if callable(thresholds):
            self._threshold = thresholds
        else:
            self._threshold = constant(thresholds)
        return self

    def set_smooth(self, smooth):
        def noop():
            return

        self._smooth = self.smooth_linear if smooth else noop
        return self

    def get_size(self):
        return [self._dx, self._dy]

    def get_thresholds(self):
        return self._threshold

    def get_smooth(self):
        return self._smooth
