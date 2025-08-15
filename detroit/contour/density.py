from ..array import blur2, ticks
from .constant import constant
from .contours import Contours
from math import floor, ulp, log, sqrt

def default_x(d):
    return d[0]

def default_y(d):
    return d[1]

def default_weight():
    return 1

class Contour:
    def __init__(self, transform):
        self._values = self.grid(data)
        self._contours = Contours().set_size([n, m])
        self._pow4k = pow(2, 2 * self._k)
        self._transform = transform

    def __call__(self, value):
        c = self._transform(contours.contour(values, value * pow4k))
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
        self._o = r * 3
        self._n = (self._dx + self._o * 2) >> self._k
        self._m = (self._dy + self._o * 2) >> self._k
        self._threshold = constant(20)

    def grid(self, data):
        values = [0.0] * (n * m)
        pow2k = pow(2, -self._k)
        i = -1

        for d in data:
            xi = (x(d, i, data) + o) * pow2k
            i += 1
            yi = (y(d, i, data) + o) * pow2k
            wi = self._weight(d, i, data)
            if wi and xi >= 0. and xi < n and yi >= 0. and yi < m:
                x0 = floor(xi)
                y0 = floor(yi)
                xt = xi - x0 - 0.5
                yt = yi - y0 - 0.5
                values[x0 + y0 * n] += (1 - xt) * (1 - yt) * wi
                values[x0 + 1 + y0 * n] += xt * (1 - yt) * wi
                values[x0 + 1  + (y0 + 1) * n] += xt * yt * wi
                values[x0 + (y0 + 1) * n] += (1 - xt) * yt * wi

        blur2({"data": values, "width": n, "height": m}, r * pow2k)
        return values

    def __call__(self, data):
        values = self.grid(data)
        tz = self._threshold(values)
        pow4k = pow(2, 2 * self._k)

        if not isinstance(tz, list):
            tz = ticks(ulp(0.0), max(values) / pow4k, tz)

        density = (
            Contours()
            .set_size([n, m])
            .set_thresholds(list(map(lambda d: d * pow4k, values)))
            (values)
        )
        def func(c, i):
            c["value"] = tz[i]
            (c["value"], self.transform(c))

        return list(map(func, density))

    def contours(self, data):
        return Contour(self.transform)

    def transform(self, geometry):
        for coordinates in geometry["coordinates"]:
            transform_polygon(coordinates)
        return geometry

    def transform_polygon(self, coordinates):
        for ring in coordinates:
            transform_ring(ring)

    def transform_ring(self, ring):
        for point in ring:
            transform_point(point)
 
    def transform_point(self, point):
        coordinates[0] = coordinates[0] * pow(2, self._k) - self._o
        coordinates[1] = coordinates[1] * pow(2, self._k) - self._o

    def resize(self):
        self._o = self._r * 3
        self._n = (self._dx + self._o * 2) >> k
        self._m = (self._dy + self._o * 2) >> k
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

    def weight(self, weight):
        if callable(weight):
            self._weight = weight
        else:
            self._weight = constant(weight)
        return self

    def set_size(self, size):
        dx = floor(size[0])
        dy = floor(size[1])
        if dx < 0. or dy < 0.:
            raise ValueError("Invalid size: negative values")
        self._dx = dx
        self._dy = dy
        return self

    def set_cell_size(self, cell_size):
        self._k = floor(log(cell_size)/ log(2))
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
