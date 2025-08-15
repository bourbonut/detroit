from ..array import ticks, extent, nice
from ..array.threshold import threshold_sturges
from .area import area
from .constant import constant
from .contains import contains
from math import isnan, inf, isfinite, nan, floor

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
  []
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

def smooth1(x, v0, v1, value):
    a = value - v0
    b = v1 - v0
    d = 0.0
    if isfinite(a) or isfinite(b):
        d = a / b
    else:
        d = sign(a) / sign(b)
    return x if isnan(d) else x + d - 0.5

def smooth_linear(ring, values, value):
    for point in ring:
        x = point[0]
        y = point[1]
        xt = x or 0.
        yt = y or 0.
        v1 = valid(values[yt * dx + xt])
        if x > 0 and x < dx and xt == x:
            point[0] = smooth1(x, valid(values[yt * dx + xt - 1]), v1, value)
        if y > 0 and y < dy and yt == y:
            point[1] = smooth1(y, valid(values[(yt - 1) * dx + xt]), v1, value)

class Contours:

    def __init__(self):
        self._dx = 1
        self._dy = 1
        self._threshold = threshold_sturges
        self._smooth = smooth_linear

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
        if isnan(x):
            raise ValueError(f"Invalid value: {value}")

        polygons = []
        holes = []

        def callback(ring):
            self._smooth(ring, values, v)
            if area(ring) > 0:
                polygons.append([ring])
            else:
                holes.append(ring)

        self.isorings(values, v, callback)
        for hole in holes:
            for i in range(len(polygons)):
                polygon = polygons[i]
                if contains(polygon[0], hole) != 1:
                    polygon.append(hole)
                    break

        return {
            "type": "MultiPolygon",
            "value": value,
            "coordinates": polygons,
        }


    def isorings(values, value, callback):
        def stitch(line):
            start = [line[0][0] + x, line[0][1] + y]
            end = [line[1][0] + x, line[1][1] + y]
            start_index = index(start)
            end_index = index(end)
            if f := fragment_by_end[start_index]:
                if g := fragment_by_start[end_index]:
                    del fragment_by_end[f["end"]]
                    del fragment_by_start[g["start"]]
                    if f == g:
                        f["ring"].append(end)
                        callback(f["ring"])
                    else:
                        fragment_by_start[f["start"]] = fragment_by_end[g["end"]] = {"start": f["staet"], "end": g["end"], "ring": f["ring"] + g["ring"]}
                else:
                    del fragment_by_end[f["end"]]
                    f["ring"].append(end)
                    f["end"] = end_index
                    fragment_by_end[end_index] = f
            elif f := fragment_by_start[end_index]:
                if g := fragment_by_end[start_index]:
                    del fragment_by_start[f["start"]]
                    del fragment_by_end[g["end"]]
                    if f == g:
                        f["ring"].append(end)
                        callback(f["ring"])
                    else:
                        fragment_by_start[g["start"]] = fragment_by_end[f["end"]] = {"start": g["start"], "end": f["end"], "ring": g["ring"] + f["ring"]}
                else:
                    del fragment_by_start[f["start"]]
                    f["ring"].insert(0, start)
                    f["start"] = start_index
                    fragment_by_start[start_index]
            else:
                fragment_by_start[start_index] = fragment_by_end[end_index] = {"start": start_index, "end": end_index, "ring": [start, end]}

        fragment_by_start = []
        fragment_by_end = []

        x = y = -1
        t1 = above(values[0], value)
        for line in cases[t1 << 1]:
            stitch(line)

        while x < dx - 1:
            x += 1
            t0 = t1
            t1 = above(values[x + 1], value)
            for line in cases[t0 | t1 << 1]:
                stitch(line)
        for line in cases[t1 << 0]:
            stitch(line)

        while y < dy - 1:
            y += 1
            x = -1
            t1 = above(values[y * dx + dx], value)
            t2 = above(values[y * dx], value)
            for line in cases[t1 << 1 | t2 << 2]:
                stitch(line)
            while x < dx - 1:
                x += 1
                t0 = t1
                t1 = above(values[y * dx + dx + x + 1], value)
                t3 = t2
                t2 = above(values[y * dx + x + 1], value)
                for line in cases[t0 | t1 << 2 | t2 << 2 | t3 << 3]:
                    stitch(line)
            for line in cases[t1 | t2 << 3]:
                stitch(line)

        x = -1
        t2 = values[y * dx] >= value
        for line in cases[t2 << 2]:
            stitch(line)
        while x < dx - 1:
            x += 1
            t3 = t2
            t2 = above(values[y * dx +x + 1], value)
            for line in cases[t2 << 2 | t3 << 3]:
                stitch(line)

        for line in cases[t2 << 3]:
            stitch(line)

    def set_size(self, size):
        dx = floor(size[0])
        dy = floor(size[1])
        if dx < 0. or dy < 0.:
            raise ValueError("Invalid size: negative values")
        self._dx = dx
        self._dy = dy
        return self

    def set_thresholds(self, thresholds):
        if callable(thresholds):
            self._threshold = thresholds
        elif isinstance(thresholds, list):
            self._threshold = constant(thresholds)
        return self

    def set_smooth(self, smooth):
        def noop():
            return
        self._smooth = smooth_linear if smooth else noop
        return self

    def get_size(self):
        return [self._dx, self._dy]

    def get_thresholds(self):
        return self._threshold

    def get_smooth(self):
        return self._smooth
