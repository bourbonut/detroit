from .continuous import identity
from .init import init_interpolator

import math
from bisect import bisect
from statistics import quantiles

class SequentialQuantile:

    def __init__(self):
        self._domain = []
        self._interpolator = identity

    def __call__(self, x):
        if x is not None and not (isinstance(x, float) and math.isnan(x)):
            return self._interpolator((bisect(self.domain, x, 1) - 1) / (len(self.domain) - 1))

    def set_domain(self, domain):
        self._domain.clear()
        for d in domain:
            if d is not None and not (isinstance(d, float) and math.isnan(d)):
                self._domain.append(d)
        self._domain = sorted(self._domain)
        return self

    @property
    def domain(self):
        return self._domain.copy()

    def set_interpolator(self, interpolator):
        self._interpolator = interpolator
        return self

    @property
    def interpolator(self):
        return self._interpolator

    @property
    def range(self):
        return [self._interpolator(i / (len(self.domain) - 1)) for i in range(len(self.domain))]

    def quantiles(self, n):
        return [self.domain[0]] + quantiles(self.domain, n=n, method="inclusive") + [self.domain[-1]]

    def copy(self):
        return SequentialQuantile().set_domain(self.domain)


def scale_sequential_quantile(*args):
    scale = SequentialQuantile()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)
