from __future__ import annotations

import math
from collections.abc import Callable
from typing import TypeVar, overload

from .continuous import Transformer, copy, identity
from .init import init_range
from .linear import LinearBase

T = TypeVar("T")


def transform_pow(exponent):
    return lambda x: (-math.pow(-x, exponent) if x < 0 else math.pow(x, exponent))


def transform_sqrt(x):
    return -math.sqrt(-x) if x < 0 else math.sqrt(x)


def transform_square(x):
    return -x * x if x < 0 else x * x


class ScalePow(Transformer, LinearBase):
    """
    Power ("pow") scales are similar to linear scales, except an exponential
    transform is applied to the input domain value before the output range
    value is computed.
    Each range value y can be expressed as a function of the domain value x:
    :math:`y = m \\cdot x^k + b`, where :math:`k` is the exponent value.
    Power scales also support negative domain values, in which case the
    input value and the resulting output value are multiplied by -1.

    Parameters
    ----------
    t : Callable
        Transform function
    u : Callable
        Untransform function
    exponent : float | int
        Exponent
    """

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

    def set_exponent(self, exponent: int | float) -> ScalePow:
        """
        Sets the current exponent to the given numeric value.

        Parameters
        ----------
        exponent : int | float
            exponent

        Returns
        -------
        ScalePow
            Itself
        """
        self._exponent = float(exponent)
        return self._rescale()

    @property
    def exponent(self):
        return self._exponent

    def copy(self):
        return copy(self, ScalePow()).set_exponent(self.exponent)


@overload
def scale_pow() -> ScalePow: ...


@overload
def scale_pow(range_vals: list[T]) -> ScalePow: ...


@overload
def scale_pow(domain: list[int | float], range_vals: list[T]) -> ScalePow: ...


def scale_pow(*args) -> ScalePow:
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
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)


@overload
def scale_sqrt() -> ScalePow: ...


@overload
def scale_sqrt(range_vals: list[T]) -> ScalePow: ...


@overload
def scale_sqrt(domain: list[int | float], range_vals: list[T]) -> ScalePow: ...


def scale_sqrt(*args) -> ScalePow:
    """
    Constructs a new pow scale with the specified domain and range,
    the exponent 0.5, the default interpolator and clamping disabled.

    Returns
    -------
    ScalePow
        Scale object
    """
    scale = ScalePow().set_exponent(0.5)
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
