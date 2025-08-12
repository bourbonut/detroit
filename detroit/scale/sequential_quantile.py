import math
from bisect import bisect
from collections.abc import Callable
from statistics import quantiles
from typing import TypeVar, overload

from .continuous import identity
from .init import init_interpolator

TSequentialQuantile = TypeVar("Itself", bound="SequentialQuantile")


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
                (bisect(self.get_domain(), x, 1) - 1) / (len(self.get_domain()) - 1)
            )

    def set_domain(self, domain: list[int | float]) -> TSequentialQuantile:
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

    def get_domain(self) -> list[int | float]:
        return self._domain.copy()

    def set_interpolator(self, interpolator: Callable) -> TSequentialQuantile:
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

    def get_interpolator(self) -> Callable:
        return self._interpolator

    def get_range(self) -> list[float]:
        """
        Returns an array of interpolated values from domain values
        using interpolator function.

        Returns
        -------
        list[float]
            Interpolated values
        """
        return [
            self._interpolator(i / (len(self.get_domain()) - 1))
            for i in range(len(self.get_domain()))
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
            [self.get_domain()[0]]
            + quantiles(self.get_domain(), n=n, method="inclusive")
            + [self.get_domain()[-1]]
        )

    def copy(self):
        return SequentialQuantile().set_domain(self.get_domain())

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

    >>> scale = d3.scale_sequential_quantile().set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
    >>> scale = scale.set_interpolator(d3.interpolate_blues)
    >>> for x in range(21):
    ...     print(x, scale(x))
    ...
    ...
    0 rgb(247, 251, 255)
    1 rgb(247, 251, 255)
    2 rgb(247, 251, 255)
    3 rgb(247, 251, 255)
    4 rgb(247, 251, 255)
    5 rgb(247, 251, 255)
    6 rgb(225, 237, 248)
    7 rgb(202, 222, 240)
    8 rgb(130, 186, 219)
    9 rgb(130, 186, 219)
    10 rgb(89, 161, 207)
    11 rgb(89, 161, 207)
    12 rgb(89, 161, 207)
    13 rgb(55, 135, 192)
    14 rgb(55, 135, 192)
    15 rgb(28, 106, 175)
    16 rgb(11, 77, 148)
    17 rgb(11, 77, 148)
    18 rgb(11, 77, 148)
    19 rgb(11, 77, 148)
    20 rgb(8, 48, 107)
    >>> d3.interpolate_blues(0)
    'rgb(247, 251, 255)'
    >>> d3.interpolate_blues(1)
    'rgb(8, 48, 107)'
    """
    scale = SequentialQuantile()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    return init_interpolator(scale)
