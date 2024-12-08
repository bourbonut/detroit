from __future__ import annotations

import math
from typing import TypeVar, overload

from .continuous import Transformer, copy
from .init import init_range
from .linear import LinearBase

T = TypeVar("T")


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

    def set_constant(self, c: int | float) -> ScaleSymlog:
        """
        Sets the symlog constant to the specified number and returns this scale.

        Parameters
        ----------
        c : int | float
            Constant value

        Returns
        -------
        ScaleSymlog
            Itself
        """
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


@overload
def scale_symlog() -> ScaleSymlog: ...


@overload
def scale_symlog(range_vals: list[T]) -> ScaleSymlog: ...


@overload
def scale_symlog(domain: list[int | float], range_vals: list[T]) -> ScaleSymlog: ...


def scale_symlog(*args):
    """
    Builds a new continuous scale with the specified domain and
    range, the constant 1, the default interpolator and clamping
    disabled.

    Parameters
    ----------
    domain : list[int | float]
        Array of numbers
    range_vals : list[int | float]
        Array of values

    Returns
    -------
    ScaleSymlog
        Scale object

    Examples
    --------

    >>> d3.scale_symlog([0, 100], [0, 960])
    """
    scale = ScaleSymlog()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
