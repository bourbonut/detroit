from __future__ import annotations

import math
from bisect import bisect
from typing import Any, TypeVar, overload

from .init import init_range
from .linear import LinearBase

T = TypeVar("T")


class ScaleQuantize(LinearBase):
    def __init__(self):
        self._x0 = 0
        self._x1 = 1
        self._n = 1
        self._domain = [0.5]
        self._range_vals = [0, 1]
        self._unknown = None

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
        if x is not None and not math.isnan(x):
            return self._range_vals[bisect(self._domain, x, 0, self._n)]
        else:
            return self._unknown

    def rescale(self):
        x0, x1 = self._x0, self._x1
        n = self._n
        self._domain = [((i + 1) * x1 - (i - n) * x0) / (n + 1) for i in range(n)]
        return self

    def set_domain(self, domain: list[int | float]) -> ScaleQuantize:
        """
        Sets the scale’s domain to the specified two-element array of numbers.

        Parameters
        ----------
        domain : list[int | float]
            Domain

        Returns
        -------
        ScaleQuantize
            Itself
        """
        self._x0, self._x1 = map(float, sorted(domain)[:2])
        return self.rescale()

    @property
    def domain(self) -> list[int | float]:
        return [self._x0, self._x1]

    def set_range(self, range_vals: list[T]) -> ScaleQuantize:
        """
        Sets the scale’s range to the specified array of values

        Parameters
        ----------
        range_vals : list[T]
            Range values

        Returns
        -------
        ScaleQuantize
            Itself
        """
        self._range_vals = list(range_vals)
        self._n = len(self._range_vals) - 1
        return self.rescale()

    @property
    def range(self) -> list[T]:
        return self._range_vals.copy()

    def invert_extent(self, y: T) -> int | float:
        """
        Returns the extent of values in the domain :math:`[x_0, x_1]`
        for the corresponding value in the range: the inverse of quantize.
        This method is useful for interaction, say to determine the value
        in the domain that corresponds to the pixel location under the mouse.

        Parameters
        ----------
        y : T
            Input value

        Returns
        -------
        int | float
            Output value
        """
        i = self._range_vals.index(y)
        if i < 0:
            return [math.nan, math.nan]
        elif i < 1:
            return [self._x0, self._domain[0]]
        elif i >= self._n:
            return [self._domain[self._n - 1], self._x1]
        else:
            return [self._domain[i - 1], self._domain[i]]

    def set_unknown(self, unknown: Any) -> ScaleQuantize:
        """
        Sets the scale's unknown value

        Parameters
        ----------
        unknown : Any
            Unknown value

        Returns
        -------
        ScaleQuantize
            Itself
        """
        self._unknown = unknown
        return self

    @property
    def unknown(self) -> Any:
        return self._unknown

    @property
    def thresholds(self):
        return self._domain.copy()

    def copy(self):
        return (
            ScaleQuantize()
            .domain([self._x0, self._x1])
            .range(self._range_vals)
            .unknown(self._unknown)
        )


@overload
def scale_quantize() -> ScaleQuantize: ...


@overload
def scale_quantize(range_vals: list[T]) -> ScaleQuantize: ...


@overload
def scale_quantize(domain: list[int | float], range_vals: list[T]) -> ScaleQuantize: ...


def scale_quantize(*args):
    """
    Builds a new quantize scale with the specified domain and range.

    Parameters
    ----------
    domain : list[int | float]
        Array of numbers
    range_vals : list[T]
        Array of values

    Returns
    -------
    ScaleQuantize
        Scale object

    Examples
    --------

    >>> d3.scale_quantize()
    """
    scale = ScaleQuantize()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
