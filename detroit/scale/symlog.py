from .linear import LinearBase
from .continuous import copy, Transformer
from .init import init_range
import math


def sign(x):
    return -1 if x < 0 else 1


def transform_symlog(c):
    return lambda x: sign(x) * math.log1p(abs(x / c))


def transform_symexp(c):
    return lambda x: sign(x) * math.expm1(abs(x)) * c


class ScaleSymlog(Transformer, LinearBase):
    def __init__(self, c=1):
        self._c = c
        super().__init__(transform_symlog(self._c), transform_symexp(self._c))

    def set_constant(self, c):
        self._c = float(c)
        self.transform = transform_symlog(self._c)
        self.untransform = transform_symexp(self._c)
        self.rescale()
        return self

    @property
    def constant(self):
        return self._c

    def copy(self):
        return copy(self, ScaleSymlog()).set_constant(self.constant)


def scale_symlog(*args):
    scale = ScaleSymlog()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
