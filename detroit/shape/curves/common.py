from abc import ABC, abstractclassmethod
from math import cos, inf, isnan, pi, sin

from ...types import Number


def isvaluable(x: Number | None) -> bool:
    return x is not None and not isnan(x) and x


def point_radial(x: Number, y: Number) -> tuple[Number, Number]:
    x -= pi * 0.5
    return y * cos(x), y * sin(x)


def sign(x: Number) -> bool:
    return -1 if x < 0 else 1


def fdiv(y: float, x: float) -> float:
    try:
        return y / x
    except ZeroDivisionError:
        return inf if y > 0 else -inf


class Curve(ABC):
    """
    Curves are typically not used directly, instead being passed to line.curve
    and area.curve. However, you can define your own curve implementation
    should none of the built-in curves satisfy your needs using the following
    interface; see the curveLinear source for an example implementation. You
    can also use this low-level interface with a built-in curve type as an
    alternative to the line and area generators.
    """

    @abstractclassmethod
    def area_start(self):
        """
        Indicates the start of a new area segment. Each area segment consists
        of exactly two line segments: the topline, followed by the baseline,
        with the baseline points in reverse order.

        """
        ...

    @abstractclassmethod
    def area_end(self):
        """
        Indicates the end of the current area segment.
        """
        ...

    @abstractclassmethod
    def line_start(self):
        """
        Indicates the start of a new line segment. Zero or more points will
        follow.
        """
        ...

    @abstractclassmethod
    def line_end(self):
        """
        Indicates the end of the current line segment.
        """
        ...

    @abstractclassmethod
    def point(self, x: float, y: float):
        """
        Indicates a new point in the current line segment with the given x- and y-values.

        Parameters
        ----------
        x : float
            x value
        y : float
            y value
        """
        ...
