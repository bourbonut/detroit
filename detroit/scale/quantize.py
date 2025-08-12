import math
from bisect import bisect
from typing import Any, Generic, TypeVar, overload

from ..types import Number, T
from .init import init_range
from .linear import LinearBase

TScaleQuantize = TypeVar("Itself", bound="ScaleQuantize")


class ScaleQuantize(LinearBase, Generic[T]):
    def __init__(self):
        self._x0 = 0
        self._x1 = 1
        self._n = 1
        self._domain = [0.5]
        self._range_vals = [0, 1]
        self._unknown = None

    def __call__(self, x: Number | None = None) -> T:
        """
        Given a value in the input domain, returns the corresponding
        value in the output range.

        Parameters
        ----------
        x : Number | None
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

    def set_domain(self, domain: list[Number]) -> TScaleQuantize:
        """
        Sets the scale’s domain to the specified two-element array of numbers.

        Parameters
        ----------
        domain : list[Number]
            Domain

        Returns
        -------
        ScaleQuantize
            Itself
        """
        self._x0, self._x1 = map(float, sorted(domain)[:2])
        return self.rescale()

    def get_domain(self) -> list[Number]:
        return [self._x0, self._x1]

    def set_range(self, range_vals: list[T]) -> TScaleQuantize:
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

    def get_range(self) -> list[T]:
        return self._range_vals.copy()

    def invert_extent(self, y: T) -> Number:
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
        Number
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

    def set_unknown(self, unknown: Any) -> TScaleQuantize:
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

    def get_unknown(self) -> Any:
        return self._unknown

    def get_thresholds(self):
        return self._domain.copy()

    def copy(self):
        return (
            ScaleQuantize()
            .set_domain(self.get_domain())
            .set_range(self.get_range())
            .set_unknown(self.get_unknown())
        )


@overload
def scale_quantize() -> ScaleQuantize[T]: ...


@overload
def scale_quantize(range_vals: list[T]) -> ScaleQuantize[T]: ...


@overload
def scale_quantize(domain: list[Number], range_vals: list[T]) -> ScaleQuantize[T]: ...


def scale_quantize(*args):
    """
    Builds a new quantize scale with the specified domain and range.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    range_vals : list[T]
        Array of values

    Returns
    -------
    ScaleQuantize[T]
        Scale object

    Examples
    --------

    >>> scale = d3.scale_quantize([0, 100], d3.SCHEME_BLUES[6])
    >>> for x in range(11):
    ...     x = 10 * x
    ...     print(x, scale(x))
    ...
    ...
    0 #f7fbff
    10 #f7fbff
    20 #deebf7
    30 #c6dbef
    40 #9ecae1
    50 #6baed6
    60 #4292c6
    70 #2171b5
    80 #08519c
    90 #08306b
    100 #08306b
    """
    scale = ScaleQuantize()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
