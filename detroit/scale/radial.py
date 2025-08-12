import math
from collections.abc import Callable
from typing import TypeVar, overload

from ..types import Number
from .continuous import Transformer, identity
from .init import init_range
from .linear import LinearBase
from .utils import as_float

TScaleRadial = TypeVar("Itself", bound="ScaleRadial")


def sign(x: float) -> float:
    return -1 if x < 0 else 1


def square(x: float) -> float:
    return sign(x) * x * x


def unsquare(x: float) -> float:
    return sign(x) * math.sqrt(abs(x))


class ScaleRadial(Transformer[float], LinearBase):
    """
    Radial scales are a variant of linear scales where the range
    is internally squared so that an input value corresponds linearly
    to the squared output value. These scales are useful when you want
    the input value to correspond to the area of a graphical mark and
    the mark is specified by radius, as in a radial bar chart.
    Radial scales do not support interpolate.

    Parameters
    ----------
    t : Callable[[float], float]
        Tranform function
    u : Callable[[float], float]
        Untranform function
    """

    def __init__(
        self,
        t: Callable[[float], float] = identity,
        u: Callable[[float], float] = identity,
    ):
        super().__init__(t, u)
        self._range_vals = [0, 1]
        self._round = False
        self._unknown = None

    def __call__(self, x: Number) -> Number:
        """
        Given a value from the domain, returns the corresponding value from the range.

        Parameters
        ----------
        x : Number
            Input value

        Returns
        -------
        Number
            Corresponding value from the range
        """
        y = unsquare(super().__call__(x))
        if isinstance(y, float) and math.isnan(y):
            return self._unknown
        elif self._round:
            return round(y)
        else:
            return y

    def invert(self, y: Number) -> Number:
        """
        Given a value from the range, returns the corresponding value
        from the domain. Inversion is useful for interaction, say to
        determine the data value corresponding to the position of the mouse.

        Parameters
        ----------
        y : Number
            Input value

        Returns
        -------
        Number
            Corresponding value from the domain
        """
        return super().invert(square(y))

    def set_range(self, range_vals: list[Number]) -> TScaleRadial:
        """
        Sets the scale's range to the specified array of values

        Parameters
        ----------
        range_vals : list[Number]
            Range values

        Returns
        -------
        ScaleRadial
            Itself
        """
        self._range_vals = [as_float(x) for x in range_vals]
        super().set_range([square(x) for x in self._range_vals])
        return self

    def get_range(self):
        return self._range_vals.copy()

    def set_range_round(self, range_vals: list[Number]) -> TScaleRadial:
        """
        Sets the scale's range to the specified array of values
        and sets scale's interpolator to :code:`interpolate_round`.

        Parameters
        ----------
        range_vals : list[Number]
            Range values

        Returns
        -------
        ScaleRadial
            Itself
        """
        return super().set_range(range_vals).set_round(True)

    def set_round(self, round_val: bool) -> TScaleRadial:
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

    def get_round(self):
        return self._round

    def copy(self):
        return (
            ScaleRadial()
            .set_domain(self.get_domain())
            .set_range(self.get_range())
            .set_round(self.get_round())
            .set_clamp(self.get_clamp())
            .set_unknown(self.get_unknown())
        )


@overload
def scale_radial() -> ScaleRadial: ...


@overload
def scale_radial(range_vals: list[Number]) -> ScaleRadial: ...


@overload
def scale_radial(domain: list[Number], range_vals: list[Number]) -> ScaleRadial: ...


def scale_radial(*args):
    """
    Builds a new radial scale with the specified domain and range.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    range_vals : list[Number]
        Array of values

    Returns
    -------
    ScaleRadial
        Scale object

    Examples
    --------

    >>> scale = d3.scale_radial([100, 200], [0, 480])
    >>> for x in range(11):
    ...     x = 100 + x * 10
    ...     print(x, scale(x))
    ...
    ...
    100 0.0
    110 151.7893276880822
    120 214.66252583997982
    130 262.9068276024797
    140 303.5786553761644
    150 339.4112549695428
    160 371.806401235912
    170 401.59681273635624
    180 429.32505167995964
    190 455.36798306424663
    200 480.0
    """
    scale = ScaleRadial()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
