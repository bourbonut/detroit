from bisect import bisect
from .init import init_range
import math


class ScaleThreshold:
    def __init__(self):
        self._domain = [0.5]
        self._range_vals = [0, 1]
        self._unknown = None
        self._n = 1

    def __call__(self, x=None):
        if x is not None and not (isinstance(x, float) and math.isnan(x)):
            return self._range_vals[bisect(self._domain, x, 0, self._n)]
        else:
            return self._unknown

    def set_domain(self, domain):
        self._domain = list(domain)
        self._n = min(len(self._domain), len(self._range_vals) - 1)
        return self

    @property
    def domain(self):
        return self._domain.copy()

    def set_range(self, range_vals):
        self._range_vals = list(range_vals)
        self._n = min(len(self._domain), len(self._range_vals) - 1)
        return self

    @property
    def range(self):
        return self._range_vals.copy()

    def invert_extent(self, y):
        if y not in self._range_vals:
            return [None, None]
        i = self._range_vals.index(y)
        if i == 0:
            return [None, self._domain[i]]
        if i == len(self._domain):
            return [self._domain[i - 1], None]
        return [self._domain[i - 1], self._domain[i]]

    def set_unknown(self, unknown):
        self._unknown = unknown
        return self

    @property
    def unknown(self):
        return self._unknown

    def copy(self):
        return (
            ScaleThreshold()
            .set_domain(self.domain)
            .set_range(self.range_vals)
            .set_unknown(self.unknown)
        )


def scale_threshold(*args):
    scale = ScaleThreshold()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
