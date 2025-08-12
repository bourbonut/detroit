import math
from typing import Callable, Generic, TypeVar, overload

from ..array import tick_increment, ticks
from ..types import Number, T
from .continuous import Transformer, copy
from .init import init_range
from .tick_format import tick_format

TLinearBase = TypeVar("Itself", bound="LinearBase")


class LinearBase:
    def ticks(self, count: int | None = None) -> list[Number]:
        """
        Returns approximately count representative values
        from the scale's domain.

        Parameters
        ----------
        count : int | None
            Count. If specified, the scale may return more or fewer
            values depending on the domain

        Returns
        -------
        list[Number]
            Tick values are uniformly spaced, have human-readable values
            (such as multiples of powers of 10), and are guaranteed to be
            within the extent of the domain. Ticks are often used to display
            reference lines, or tick marks, in conjunction with the visualized data.
        """
        d = self.get_domain()
        return ticks(d[0], d[-1], count if count is not None else 10)

    def tick_format(
        self, count: int | None = None, specifier: str | None = None
    ) -> Callable[[Number], str]:
        """
        Returns a number format function suitable for displaying
        a tick value, automatically computing the appropriate
        precision based on the fixed interval between tick values.
        The specified count should have the same value as the count
        that is used to generate the tick values.

        Parameters
        ----------
        count : int | None
            Count. It should have the same value as the count
            that is used to generate the tick values.
        specifier : str | None
            Specifier

        Returns
        -------
        Callable[[Number], str]
            Tick format function
        """
        d = self.get_domain()
        return tick_format(d[0], d[-1], count if count is not None else 10, specifier)

    def nice(self, count: int | None = None) -> TLinearBase:
        """
        Extends the domain so that it starts and ends on nice round values.

        Parameters
        ----------
        count : int | None
            Count argument allows greater control over the step size
            used to extend the bounds, guaranteeing that the returned
            ticks will exactly cover the domain

        Returns
        -------
        LinearBase
            Itself
        """
        if count is None:
            count = 10

        d = self.get_domain()
        i0 = 0
        i1 = len(d) - 1
        start = d[i0]
        stop = d[i1]
        prestep = None
        step = None
        max_iter = 10

        if stop < start:
            step = start
            start = stop
            stop = step
            step = i0
            i0 = i1
            i1 = step

        while max_iter > 0:
            step = tick_increment(start, stop, count)
            if step == prestep:
                d[i0] = start
                d[i1] = stop
                return self.set_domain(d)
            elif step > 0:
                start = math.floor(start / step) * step
                stop = math.ceil(stop / step) * step
            elif step < 0:
                start = math.ceil(start * step) / step
                stop = math.floor(stop * step) / step
            else:
                break
            prestep = step
            max_iter -= 1

        return self

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


class ScaleLinear(Transformer[T], LinearBase, Generic[T]):
    """
    Linear scales map a continuous, quantitative input domain to a continuous
    output range using a linear transformation (translate and scale). If the
    range is also numeric, the mapping may be inverted. Linear scales are a good
    default choice for continuous quantitative data because they preserve
    proportional differences. Each range value y can be expressed as a function
    of the domain value x: :math:`y = m \\cdot x + b`.

    Parameters
    ----------
    t : Callable[[Number], T]
        Transform function
    u : Callable[[T], Number]
        Untransform function
    """

    def copy(self):
        return copy(self, ScaleLinear())


@overload
def scale_linear() -> ScaleLinear[T]: ...


@overload
def scale_linear(range_vals: list[T]) -> ScaleLinear[T]: ...


@overload
def scale_linear(domain: list[Number], range_vals: list[T]) -> ScaleLinear[T]: ...


def scale_linear(*args):
    """
    Builds a new linear scale with the specified domain
    and range, the default interpolator, and clamping disabled.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    range_vals : list[T]
        Array of values

    Returns
    -------
    ScaleLinear[T]
        Scale object

    Examples
    --------

    >>> scale = d3.scale_linear([0, 100], ["red", "blue"])
    >>> for x in range(11):
    ...     x = x * 10
    ...     print(x, scale(x))
    ...
    ...
    0 rgb(255, 0, 0)
    10 rgb(230, 0, 26)
    20 rgb(204, 0, 51)
    30 rgb(178, 0, 76)
    40 rgb(153, 0, 102)
    50 rgb(128, 0, 128)
    60 rgb(102, 0, 153)
    70 rgb(76, 0, 178)
    80 rgb(51, 0, 204)
    90 rgb(26, 0, 230)
    100 rgb(0, 0, 255)
    """
    scale = ScaleLinear()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
