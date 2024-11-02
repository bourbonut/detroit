from .linear import LinearBase
from .continuous import copy, identity, Transformer
from .init import init_range
import math

def transform_pow(exponent):
    return lambda x: (-math.pow(-x, exponent) if x < 0 else math.pow(x, exponent))

def transform_sqrt(x):
    return (-math.sqrt(-x) if x < 0 else math.sqrt(x))

def transform_square(x):
    return (-x * x if x < 0 else x * x)

class ScalePow(Transformer, LinearBase):
    def __init__(self, t = identity, u = identity, exponent = 1):
        super().__init__(t, u)
        self._exponent = exponent

    def _rescale(self):
        if self._exponent == 1:
            self.transform = identity
            self.untransform = identity
            self.rescale()
            return self
        elif self._exponent == 0.5:
            self.transform = transform_sqrt
            self.untransform = transform_square
            self.rescale()
            return self
        else:
            self.transform = transform_pow(self._exponent)
            self.untransform = transform_pow(1 / self._exponent)
            self.rescale()
            return self

    def exponent(self, *args):
        if args:
            self._exponent = float(args[0])
            return self._rescale()
        return self._exponent

    def copy(self):
        return copy(self, ScalePow()).exponent(self.exponent())

def scale_pow():
    scale = ScalePow()
    return init_range(scale)


def scale_sqrt():
    return ScalePow().exponent(0.5)
