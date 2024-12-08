from __future__ import annotations

import math
from bisect import bisect
from statistics import quantiles
from typing import Any, TypeVar, overload

from .init import init_range

T = TypeVar("T")


class ScaleQuantile:
    """
    Quantile scales map a sampled input domain to a discrete range.
    The domain is considered continuous and thus the scale will accept
    any reasonable input value; however, the domain is specified as a
    discrete set of sample values. The number of values in (the cardinality
    of) the output range determines the number of quantiles that will be
    computed from the domain. To compute the quantiles, the domain is sorted,
    and treated as a population of discrete values; see quantile.
    """

    def __init__(self):
        self._domain = []
        self._range_vals = []
        self._thresholds = []
        self._unknown = None

    def rescale(self):
        n = max(1, len(self._range_vals))
        self._thresholds = quantiles(self._domain, n=n, method="inclusive")
        return self

    def __call__(self, x: int | float) -> T:
        """
        Given a value in the input domain, returns the
        corresponding value in the output range.

        Parameters
        ----------
        x : int | float
            Input value

        Returns
        -------
        T
            Output value
        """
        if x is None or isinstance(x, float) and math.isnan(x):
            return self._unknown
        return self._range_vals[bisect(self._thresholds, x)]

    def invert_extent(self, y: T) -> int | float:
        """
        Returns the extent of values in the domain :math:`[x_0, x_1]`
        for the corresponding value in the range: the inverse of quantile.

        Parameters
        ----------
        y : T
            Input value

        Returns
        -------
        int | float
            Output value
        """
        if y not in self._range_vals:
            return [math.nan, math.nan]
        i = self._range_vals.index(y)
        return (
            [None, None]
            if i < 0
            else [
                self._thresholds[i - 1] if i > 0 else self._domain[0],
                self._thresholds[i] if i < len(self._thresholds) else self._domain[-1],
            ]
        )

    def set_domain(self, domain: list[int | float]) -> ScaleQuantile:
        """
        Sets the domain of the quantile scale to the specified
        set of discrete numeric values .

        Parameters
        ----------
        domain : list[int | float]
            Domain

        Returns
        -------
        ScaleQuantile
            Itself
        """
        self._domain.clear()
        for d in domain:
            if isinstance(d, str):
                d = float(d)
            if d is not None and not (isinstance(d, float) and math.isnan(d)):
                self._domain.append(d)
        self._domain = sorted(self._domain)
        return self.rescale()

    @property
    def domain(self) -> list[int | float]:
        return self._domain.copy()

    def set_range(self, range_vals: list[T]) -> ScaleQuantile:
        """
        Sets the discrete values in the range.

        Parameters
        ----------
        range_vals : list[T]
            Range values

        Returns
        -------
        ScaleQuantile
            Itself
        """
        self._range_vals = list(range_vals)
        return self.rescale()

    @property
    def range(self) -> list[T]:
        return self._range_vals.copy()

    def set_unknown(self, unknown: Any) -> ScaleQuantile:
        """
        Sets the scale's unknown value.

        Parameters
        ----------
        unknown : Any
            Unknown value

        Returns
        -------
        ScaleQuantile
            Itself
        """
        self._unknown = unknown
        return self

    @property
    def unknown(self) -> Any:
        return self._unknown

    @property
    def quantiles(self):
        return self._thresholds.copy()

    def copy(self):
        return (
            ScaleQuantile()
            .domain(self._domain)
            .range(self._range_vals)
            .unknown(self._unknown)
        )


@overload
def scale_quantile() -> ScaleQuantile: ...


@overload
def scale_quantile(range_vals: list[T]) -> ScaleQuantile: ...


@overload
def scale_quantile(domain: list[int | float], range_vals: list[T]) -> ScaleQuantile: ...


def scale_quantile(*args):
    """
    Builds a new quantile scale with the specified domain and range.

    Parameters
    ----------
    domain : list[int | float]
        Array of numbers
    range_vals : list[T]
        Array of values

    Returns
    -------
    ScaleQuantile
        Scale object

    Examples
    --------

    >>> d3.scale_quantile()
    """
    scale = ScaleQuantile()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
