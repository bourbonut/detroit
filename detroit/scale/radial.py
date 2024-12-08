from __future__ import annotations

import math
from collections.abc import Callable
from typing import overload

from .continuous import Transformer, identity
from .init import init_range
from .linear import LinearBase
from .number import number


def sign(x):
    return -1 if x < 0 else 1


def square(x):
    return sign(x) * x * x


def unsquare(x):
    return sign(x) * math.sqrt(abs(x))


class ScaleRadial(Transformer, LinearBase):
    """
    Radial scales are a variant of linear scales where the range
    is internally squared so that an input value corresponds linearly
    to the squared output value. These scales are useful when you want
    the input value to correspond to the area of a graphical mark and
    the mark is specified by radius, as in a radial bar chart.
    Radial scales do not support interpolate.

    Parameters
    ----------
    t : Callable
        Tranform function
    u : Callable
        Untranform function
    """

    def __init__(self, t: Callable = identity, u: Callable = identity):
        super().__init__(t, u)
        self._range_vals = [0, 1]
        self._round = False
        self._unknown = None

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
            Corresponding value from the range
        """
        y = unsquare(super().__call__(x))
        if isinstance(y, float) and math.isnan(y):
            return self._unknown
        elif self._round:
            return round(y)
        else:
            return y

    def invert(self, y: int | float) -> int | float:
        """
        Given a value from the range, returns the corresponding value
        from the domain. Inversion is useful for interaction, say to
        determine the data value corresponding to the position of the mouse.

        Parameters
        ----------
        y : int | float
            Input value

        Returns
        -------
        int | float
            Corresponding value from the domain
        """
        return super().invert(square(y))

    def set_range(self, range_vals: list[int | float]) -> ScaleRadial:
        """
        Sets the scale's range to the specified array of values

        Parameters
        ----------
        range_vals : list[int | float]
            Range values

        Returns
        -------
        ScaleRadial
            Itself
        """
        self._range_vals = [number(x) for x in range_vals]
        super().set_range([square(x) for x in self._range_vals])
        return self

    @property
    def range(self):
        return self._range_vals.copy()

    def set_range_round(self, range_vals: list[int | float]) -> ScaleRadial:
        """
        Sets the scale's range to the specified array of values
        and sets scale's interpolator to :code:`interpolate_round`.

        Parameters
        ----------
        range_vals : list[int | float]
            Range values

        Returns
        -------
        ScaleRadial
            Itself
        """
        return super().set_range(range_vals).set_round(True)

    def set_round(self, round_val: bool) -> ScaleRadial:
        """
        Enables or disables rounding accordingly

        Parameters
        ----------
        round_val : bool
            Round value

        Returns
        -------
        ScaleRadial
            Itself
        """
        self._round = bool(round_val)
        return self

    @property
    def round(self):
        return self._round

    def copy(self):
        return (
            ScaleRadial()
            .set_domain(self.domain)
            .set_range(self.range)
            .set_round(self.round)
            .set_clamp(self.clamp)
            .set_unknown(self._unknown)
        )


@overload
def scale_radial() -> ScaleRadial: ...


@overload
def scale_radial(range_vals: list[int | float]) -> ScaleRadial: ...


@overload
def scale_radial(
    domain: list[int | float], range_vals: list[int | float]
) -> ScaleRadial: ...


def scale_radial(*args):
    """
    Builds  a new radial scale with the specified domain and range.

    Parameters
    ----------
    domain : list[int | float]
        Array of numbers
    range_vals : list[int | float]
        Array of values

    Returns
    -------
    ScaleRadial
        Scale object

    Examples
    --------

    >>> d3.scale_radial([100, 200], [0, 480])
    """
    scale = ScaleRadial()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
