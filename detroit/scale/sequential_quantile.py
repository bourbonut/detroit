from __future__ import annotations

import math
from bisect import bisect
from collections.abc import Callable
from statistics import quantiles
from typing import overload

from .continuous import identity
from .init import init_interpolator


class SequentialQuantile:
    def __init__(self):
        self._domain = []
        self._interpolator = identity

    def __call__(self, x: int | float) -> int | float:
        """
        Given a value from the domain, returns the corresponding value from the range.

        Parameters
        ----------
        x : int | float
            Input value

        Returns
        -------
        int | float
            Output value
        """
        if x is not None and not (isinstance(x, float) and math.isnan(x)):
            return self._interpolator(
                (bisect(self.domain, x, 1) - 1) / (len(self.domain) - 1)
            )

    def set_domain(self, domain: list[int | float]) -> SequentialQuantile:
        """
        Sets the scale's domain to the specified array of numbers

        Parameters
        ----------
        domain : list[int | float]
            Domain

        Returns
        -------
        SequentialQuantile
            Itself
        """
        self._domain.clear()
        for d in domain:
            if d is not None and not (isinstance(d, float) and math.isnan(d)):
                self._domain.append(d)
        self._domain = sorted(self._domain)
        return self

    @property
    def domain(self) -> list[int | float]:
        return self._domain.copy()

    def set_interpolator(self, interpolator: Callable) -> SequentialQuantile:
        """
        Sets the scale's interpolator function

        Parameters
        ----------
        interpolator : Callable
            Interpolator function

        Returns
        -------
        SequentialQuantile
            Itself
        """
        self._interpolator = interpolator
        return self

    @property
    def interpolator(self) -> Callable:
        return self._interpolator

    @property
    def range(self) -> list[float]:
        """
        Returns an array of interpolated values from domain values
        using interpolator function.

        Returns
        -------
        list[float]
            Interpolated values
        """
        return [
            self._interpolator(i / (len(self.domain) - 1))
            for i in range(len(self.domain))
        ]

    def quantiles(self, n: int) -> list[float]:
        """
        Returns an array of :math:`n + 1` quantiles.

        Parameters
        ----------
        n : int
            :math:`n` value

        Returns
        -------
        list[float]
            Array of :math:`n + 1` quantiles
        """
        return (
            [self.domain[0]]
            + quantiles(self.domain, n=n, method="inclusive")
            + [self.domain[-1]]
        )

    def copy(self):
        return SequentialQuantile().set_domain(self.domain)


@overload
def scale_sequential_quantile() -> SequentialQuantile: ...


@overload
def scale_sequential_quantile(domain: list[int | float]) -> SequentialQuantile: ...


def scale_sequential_quantile(*args):
    """
    Returns a new sequential scale with a p-quantile
    transform, analogous to a quantile scale.

    Parameters
    ----------
    domain : list[int | float]
        Array of numbers

    Returns
    -------
    SequentialQuantile
        Scale object

    Examples
    --------

    >>> d3.scale_sequential_quantile()
    """
    scale = SequentialQuantile()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    return init_interpolator(scale)
