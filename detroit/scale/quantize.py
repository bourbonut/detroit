from bisect import bisect
from .linear import LinearBase
from .init import init_range
import math

class ScaleQuantize(LinearBase):
    def __init__(self):
        self._x0 = 0
        self._x1 = 1
        self._n = 1
        self._domain = [0.5]
        self._range_vals = [0, 1]
        self._unknown = None

    def __call__(self, x = None):
        if x is not None and not math.isnan(x):
            return self._range_vals[bisect(self._domain, x, 0, self._n)]
        else:
            return self._unknown

    def rescale(self):
        x0, x1 = self._x0, self._x1
        n = self._n
        self._domain = [((i + 1) * x1 - (i - n) * x0) / (n + 1) for i in range(n)]
        return self

    def domain(self, *args):
        if args:
            self._x0, self._x1 = map(float, sorted(args[0])[:2])
            return self.rescale()
        else:
            return [self._x0, self._x1]

    def range(self, *args):
        if args:
            self._range_vals = list(args[0])
            self._n = len(self._range_vals) - 1
            return self.rescale()
        return self._range_vals.copy()

    def invert_extent(self, y):
        i = self._range_vals.index(y)
        if i < 0:
            return [math.nan, math.nan]
        elif i < 1:
            return [self._x0, self._domain[0]]
        elif i >= self._n:
            return [self._domain[self._n - 1], self._x1]
        else:
            return [self._domain[i - 1], self._domain[i]]

    def unknown(self, *args):
        if args:
            self._unknown = args[0]
            return self
        return self._unknown

    def thresholds(self):
        return self._domain.copy()

    def copy(self):
        return ScaleQuantize().domain([self._x0, self._x1]).range(self._range_vals).unknown(self._unknown)


def scale_quantize():
    return init_range(ScaleQuantize())
