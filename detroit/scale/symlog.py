from __future__ import annotations

import math
from typing import TypeVar, overload

from .continuous import Transformer, copy
from .init import init_range
from .linear import LinearBase
from ..types import T, Number

TScaleSymlog = TypeVar("Itself", bound="ScaleSymlog")


def sign(x):
    return -1 if x < 0 else 1


def transform_symlog(c):
    return lambda x: sign(x) * math.log1p(abs(x / c))


def transform_symexp(c):
    return lambda x: sign(x) * math.expm1(abs(x)) * c


class ScaleSymlog(Transformer[float], LinearBase):
    """
    A bi-symmetric log transformation for wide-range data by Webber for
    details. Unlike a log scale, a symlog scale domain can include zero.

    Parameters
    ----------
    c : Number
        Symlog constant value
    """
    def __init__(self, c: Number = 1):
        self._c = c
        super().__init__(transform_symlog(self._c), transform_symexp(self._c))

    def set_constant(self, c: Number) -> TScaleSymlog:
        """
        Sets the symlog constant to the specified number and returns this scale.

        Parameters
        ----------
        c : Number
            Constant value

        Returns
        -------
        ScaleSymlog
            Itself
        """
        self._c = float(c)
        self._transform = transform_symlog(self._c)
        self._untransform = transform_symexp(self._c)
        self._rescale()
        return self

    def get_constant(self):
        return self._c

    def copy(self):
        return copy(self, ScaleSymlog()).set_constant(self.get_constant())


@overload
def scale_symlog() -> ScaleSymlog: ...


@overload
def scale_symlog(range_vals: list[T]) -> ScaleSymlog: ...


@overload
def scale_symlog(domain: list[Number], range_vals: list[T]) -> ScaleSymlog: ...


def scale_symlog(*args):
    """
    Builds a new continuous scale with the specified domain and
    range, the constant 1, the default interpolator and clamping
    disabled.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    range_vals : list[Number]
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
