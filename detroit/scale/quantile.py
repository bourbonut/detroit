from bisect import bisect
from .init import init_range
import math
from statistics import quantiles

class ScaleQuantile:
    
    def __init__(self):
        self._domain = []
        self._range_vals = []
        self._thresholds = []
        self._unknown = None

    def rescale(self):
        n = max(1, len(self._range_vals))
        self._thresholds = quantiles(self._domain, n=n, method="inclusive")
        return self

    def __call__(self, x):
        if x is None or isinstance(x, float) and math.isnan(x):
            return self._unknown
        return self._range_vals[bisect(self._thresholds, x)]

    def invert_extent(self, y):
        if y not in self._range_vals:
            return [math.nan, math.nan]
        i = self._range_vals.index(y)
        return [None, None] if i < 0 else [
            self._thresholds[i - 1] if i > 0 else self._domain[0],
            self._thresholds[i] if i < len(self._thresholds) else self._domain[-1]
        ]

    def domain(self, *args):
        if args:
            self._domain.clear()
            for d in args[0]:
                if isinstance(d, str):
                    d = float(d)
                if d is not None and not (isinstance(d, float) and math.isnan(d)):
                    self._domain.append(d)
            self._domain = sorted(self._domain)
            return self.rescale()
        return self._domain.copy()

    def range(self, *args):
        if args:
            self._range_vals = list(args[0])
            return self.rescale()
        return self._range_vals.copy()

    def unknown(self, *args):
        if args:
            self._unknown = args[0]
            return self
        return self._unknown

    def quantiles(self):
        return self._thresholds.copy()

    def copy(self):
        return ScaleQuantile().domain(self._domain).range(self._range_vals).unknown(self._unknown)


def scale_quantile(*args):
    scale = ScaleQuantile()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
