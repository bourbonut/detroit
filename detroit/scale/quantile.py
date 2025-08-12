import math
from bisect import bisect
from statistics import quantiles
from typing import Any, Generic, TypeVar, overload

from ..types import Number, T
from .init import init_range

TScaleQuantile = TypeVar("Itself", bound="ScaleQuantile")


class ScaleQuantile(Generic[T]):
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

    def __call__(self, x: Number) -> T:
        """
        Given a value in the input domain, returns the
        corresponding value in the output range.

        Parameters
        ----------
        x : Number
            Input value

        Returns
        -------
        T
            Output value
        """
        if x is None or isinstance(x, float) and math.isnan(x):
            return self._unknown
        return self._range_vals[bisect(self._thresholds, x)]

    def invert_extent(self, y: T) -> Number:
        """
        Returns the extent of values in the domain :math:`[x_0, x_1]`
        for the corresponding value in the range: the inverse of quantile.

        Parameters
        ----------
        y : T
            Input value

        Returns
        -------
        Number
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

    def set_domain(self, domain: list[Number]) -> TScaleQuantile:
        """
        Sets the domain of the quantile scale to the specified
        set of discrete numeric values .

        Parameters
        ----------
        domain : list[Number]
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

    def get_domain(self) -> list[Number]:
        return self._domain.copy()

    def set_range(self, range_vals: list[T]) -> TScaleQuantile:
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

    def get_range(self) -> list[T]:
        return self._range_vals.copy()

    def set_unknown(self, unknown: Any) -> TScaleQuantile:
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

    def get_unknown(self) -> Any:
        return self._unknown

    def get_quantiles(self):
        return self._thresholds.copy()

    def copy(self):
        return (
            ScaleQuantile()
            .set_domain(self._domain)
            .set_range(self._range_vals)
            .set_unknown(self._unknown)
        )

    def __str__(self) -> str:
        name = self.__class__.__name__
        attrbs = ["domain", "range"]
        attrbs = (f"{a}={getattr(self, f'get_{a}')()}" for a in attrbs)
        attrbs = ", ".join(attrbs)
        return f"{name}({attrbs})"

    def __repr__(self) -> str:
        name = self.__class__.__name__
        addr = id(self)
        return f"<{name} at {hex(addr)}>"


@overload
def scale_quantile() -> ScaleQuantile[T]: ...


@overload
def scale_quantile(range_vals: list[T]) -> ScaleQuantile[T]: ...


@overload
def scale_quantile(domain: list[Number], range_vals: list[T]) -> ScaleQuantile[T]: ...


def scale_quantile(*args):
    """
    Builds a new quantile scale with the specified domain and range.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    range_vals : list[T]
        Array of values

    Returns
    -------
    ScaleQuantile[T]
        Scale object

    Examples
    --------

    >>> scale = d3.scale_quantile().set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
    >>> scale = scale.set_range([0, 1, 2, 3])
    >>> for x in range(21):
    ...     print(x, scale(x))
    ...
    ...
    0 0
    1 0
    2 0
    3 0
    4 0
    5 0
    6 0
    7 0
    8 1
    9 2
    10 2
    11 2
    12 2
    13 2
    14 2
    15 3
    16 3
    17 3
    18 3
    19 3
    20 3
    """
    scale = ScaleQuantile()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
