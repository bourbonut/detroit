import math
from collections.abc import Callable

from .continuous import Transformer, copy, identity
from .init import init_range
from .linear import LinearBase


def transform_pow(exponent):
    return lambda x: (-math.pow(-x, exponent) if x < 0 else math.pow(x, exponent))


def transform_sqrt(x):
    return -math.sqrt(-x) if x < 0 else math.sqrt(x)


def transform_square(x):
    return -x * x if x < 0 else x * x


class ScalePow(Transformer, LinearBase):
    def __init__(
        self, t: Callable = identity, u: Callable = identity, exponent: float | int = 1
    ):
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

    def set_exponent(self, exponent):
        self._exponent = float(exponent)
        return self._rescale()

    @property
    def exponent(self):
        return self._exponent

    def copy(self):
        return copy(self, ScalePow()).set_exponent(self.exponent)


def scale_pow() -> ScalePow:
    """
    Constructs a new pow scale with the specified domain and
    range, the exponent 1, the default interpolator and
    clamping disabled.

    Returns
    -------
    ScalePow
        Scale object
    """
    scale = ScalePow()
    return init_range(scale)


def scale_sqrt() -> ScalePow:
    """
    Constructs a new pow scale with the specified domain and range,
    the exponent 0.5, the default interpolator and clamping disabled.

    Returns
    -------
    ScalePow
        Scale object
    """
    return ScalePow().set_exponent(0.5)
