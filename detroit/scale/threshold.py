from __future__ import annotations

import math
from bisect import bisect
from typing import Any, TypeVar, overload

from .init import init_range

T = TypeVar("T")


class ScaleThreshold:
    """
    Threshold scales are similar to quantize scales, except they allow
    you to map arbitrary subsets of the domain to discrete values in
    the range. The input domain is still continuous, and divided into
    slices based on a set of threshold values. See this choropleth for
    an example.
    """

    def __init__(self):
        self._domain = [0.5]
        self._range_vals = [0, 1]
        self._unknown = None
        self._n = 1

    def __call__(self, x: int | float | None = None) -> T:
        """
        Given a value in the input domain, returns the corresponding
        value in the output range.

        Parameters
        ----------
        x : int | float | None
            Input value

        Returns
        -------
        T
            Output value
        """
        if x is not None and not (isinstance(x, float) and math.isnan(x)):
            return self._range_vals[bisect(self._domain, x, 0, self._n)]
        else:
            return self._unknown

    def set_domain(self, domain: list[int | float]) -> ScaleThreshold:
        """
        Sets the scale’s domain to the specified array of values.

        Parameters
        ----------
        domain : list[int | float]
            Domain

        Returns
        -------
        ScaleThreshold
            Itself
        """
        self._domain = list(domain)
        self._n = min(len(self._domain), len(self._range_vals) - 1)
        return self

    @property
    def domain(self) -> list[int | float]:
        return self._domain.copy()

    def set_range(self, range_vals: list[T]) -> ScaleThreshold:
        """
        Sets the scale’s range to the specified array of values.

        Parameters
        ----------
        range_vals : list[T]
            Range

        Returns
        -------
        ScaleThreshold
            Itself
        """
        self._range_vals = list(range_vals)
        self._n = min(len(self._domain), len(self._range_vals) - 1)
        return self

    @property
    def range(self) -> list[T]:
        return self._range_vals.copy()

    def invert_extent(self, y: T) -> list[int | float | None]:
        """
        Returns the extent of values in the domain :math:`[x_0, x_1]`
        for the corresponding value in the range, representing the
        inverse mapping from range to domain.

        Parameters
        ----------
        y : T
            Input value

        Returns
        -------
        list[int | float | None]
            :math:`[x_0, x_1]` values
        """
        if y not in self._range_vals:
            return [None, None]
        i = self._range_vals.index(y)
        if i == 0:
            return [None, self._domain[i]]
        if i == len(self._domain):
            return [self._domain[i - 1], None]
        return [self._domain[i - 1], self._domain[i]]

    def set_unknown(self, unknown: Any) -> ScaleThreshold:
        """
        Sets the scale's unknown value.

        Parameters
        ----------
        unknown : Any
            Unknown value

        Returns
        -------
        ScaleThreshold
            Itself
        """
        self._unknown = unknown
        return self

    @property
    def unknown(self) -> Any:
        return self._unknown

    def copy(self):
        return (
            ScaleThreshold()
            .set_domain(self.domain)
            .set_range(self.range_vals)
            .set_unknown(self.unknown)
        )


@overload
def scale_threshold() -> ScaleThreshold: ...


@overload
def scale_threshold(range_vals: list[T]) -> ScaleThreshold: ...


@overload
def scale_threshold(
    domain: list[int | float], range_vals: list[T]
) -> ScaleThreshold: ...


def scale_threshold(*args):
    """
    Builds a new threshold scale with the specified domain and range.

    Parameters
    ----------
    domain : list[int | float]
        Array of numbers
    range_vals : list[int | float]
        Array of values

    Returns
    -------
    ScaleThreshold
        Scale object

    Examples
    --------

    >>> d3.scale_threshold([0, 1], ["red", "white", "blue"])
    """
    scale = ScaleThreshold()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
