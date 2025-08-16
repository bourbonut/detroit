from inspect import signature
from math import floor, isnan, log, sqrt, ulp

from ..array import blur2, ticks
from .constant import constant
from .contours import Contours


def default_x(d):
    return d[0]


def default_y(d):
    return d[1]


def default_weight():
    return 1


class Contour:
    def __init__(self, values, contours, pow4k, transform):
        self._values = values
        self._contours = contours
        self._pow4k = pow4k
        self._transform = transform

    def __call__(self, value):
        c = self._transform(self._contours.contour(self._values, value * self._pow4k))
        c["value"] = value
        return c

    def max(self):
        return max(self._values) / self._pow4k


class Density:
    def __init__(self):
        self._x = default_x
        self._y = default_y
        self._weight = default_weight
        self._dx = 960
        self._dy = 500
        self._r = 20
        self._k = 2
        self._o = self._r * 3
        self._n = (self._dx + self._o * 2) >> self._k
        self._m = (self._dy + self._o * 2) >> self._k
        self._threshold = constant(20)

    def grid(self, data):
        values = [0.0] * (self._n * self._m)
        pow2k = pow(2, -self._k)
        i = -1

        for d in data:
            args = [d, i, data]
            xnargs = len(signature(self._x).parameters)
            xi = (self._x(*args[:xnargs]) + self._o) * pow2k
            i += 1
            args = [d, i, data]
            ynargs = len(signature(self._y).parameters)
            yi = (self._y(*args[:ynargs]) + self._o) * pow2k
            wnargs = len(signature(self._weight).parameters)
            wi = self._weight(*args[:wnargs])
            if (
                wi
                and not isnan(wi)
                and xi >= 0.0
                and xi < self._n
                and yi >= 0.0
                and yi < self._m
            ):
                x0 = floor(xi)
                y0 = floor(yi)
                xt = xi - x0 - 0.5
                yt = yi - y0 - 0.5
                values[x0 + y0 * self._n] += (1 - xt) * (1 - yt) * wi
                values[x0 + 1 + y0 * self._n] += xt * (1 - yt) * wi
                values[x0 + 1 + (y0 + 1) * self._n] += xt * yt * wi
                values[x0 + (y0 + 1) * self._n] += (1 - xt) * yt * wi

        blur2({"data": values, "width": self._n, "height": self._m}, self._r * pow2k)
        return values

    def __call__(self, data):
        values = self.grid(data)
        tz = self._threshold(values)
        pow4k = pow(2, 2 * self._k)

        if not isinstance(tz, list):
            max_values = max(values)
            tz = ticks(ulp(0.0), max_values / pow4k, tz) if max_values != 0.0 else []

        density = (
            Contours()
            .set_size([self._n, self._m])
            .set_thresholds(list(map(lambda d: d * pow4k, tz)))(values)
        )

        def func(pair):
            i, c = pair
            c["value"] = tz[i]
            return self.transform(c)

        return list(map(func, enumerate(density)))

    def contours(self, data):
        contours = Contours().set_size([self._n, self._m])
        values = self.grid(data)
        pow4k = pow(2, 2 * self._k)
        return Contour(values, contours, pow4k, self.transform)

    def transform(self, geometry):
        for coordinates in geometry["coordinates"]:
            self.transform_polygon(coordinates)
        return geometry

    def transform_polygon(self, coordinates):
        for ring in coordinates:
            self.transform_ring(ring)

    def transform_ring(self, ring):
        for point in ring:
            self.transform_point(point)

    def transform_point(self, coordinates):
        coordinates[0] = coordinates[0] * pow(2, self._k) - self._o
        coordinates[1] = coordinates[1] * pow(2, self._k) - self._o

    def resize(self):
        self._o = self._r * 3
        self._n = int(self._dx + self._o * 2) >> self._k
        self._m = int(self._dy + self._o * 2) >> self._k
        return self

    def x(self, x):
        if callable(x):
            self._x = x
        else:
            self._x = constant(x)
        return self

    def y(self, y):
        if callable(y):
            self._y = y
        else:
            self._y = constant(y)
        return self

    def set_weight(self, weight):
        if callable(weight):
            self._weight = weight
        else:
            self._weight = constant(weight)
        return self

    def set_size(self, size):
        dx = size[0]
        dy = size[1]
        if dx < 0.0 or dy < 0.0:
            raise ValueError("Invalid size: negative values")
        self._dx = dx
        self._dy = dy
        return self.resize()

    def set_cell_size(self, cell_size):
        self._k = floor(log(cell_size) / log(2))
        return self.resize()

    def set_thresholds(self, thresholds):
        if callable(thresholds):
            self._threshold = thresholds
        elif isinstance(thresholds, list):
            self._threshold = constant(thresholds)
        return self

    def set_bandwidth(self, bandwidth):
        self._r = (sqrt(4 * bandwidth * bandwidth + 1) - 1) / 2
        return self.resize()

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_weight(self):
        return self._weight

    def get_size(self):
        return [self._dx, self._dy]

    def get_cell_size(self):
        return 1 << self._k

    def get_thresholds(self):
        return self._threshold

    def get_bandwidth(self):
        return sqrt(self._r * (self._r + 1))
