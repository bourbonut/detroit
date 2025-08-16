from collections.abc import Callable
from typing import TypeVar

from ..selection import Selection
from ..types import Accessor, Number, T
from .curves import Curve, curve_radial, curve_radial_linear
from .line import Line

TLineRadial = TypeVar("LineRadial", bound="LineRadial")


class LineRadial(Line[T]):
    def __init__(self):
        Line.__init__(self)
        super().set_curve(curve_radial_linear)

    def set_curve(self, curve: Callable[[Selection], Curve]) -> TLineRadial:
        """
        Sets curve.

        Parameters
        ----------
        curve : Callable[[Selection], Curve]
            Curve factory function

        Returns
        -------
        LineRadial
            Itself
        """
        return super().set_curve(curve_radial(curve))

    def angle(self, angle: Accessor[T, float] | Number) -> TLineRadial:
        """
        Sets angle accessor function

        Parameters
        ----------
        angle : Accessor[T, float] | Number
            angle accessor function

        Returns
        -------
        LineRadial
            Itself
        """
        return super().x(angle)

    def radius(self, radius: Accessor[T, float] | Number) -> TLineRadial:
        """
        Sets radius accessor function

        Parameters
        ----------
        radius : Accessor[T, float] | Number
            radius accessor function

        Returns
        -------
        LineRadial
            Itself
        """
        return super().y(radius)

    def get_angle(self) -> Accessor[T, float]:
        return super().get_x()

    def get_radius(self) -> Accessor[T, float]:
        return super().get_y()


def line_radial() -> LineRadial:
    """
    A radial line generator is like the Cartesian line generator except the x
    and y accessors are replaced with angle and radius accessors. Radial lines
    are positioned relative to the origin; use a transform to change the
    origin.

    Returns
    -------
    LineRadial
        Radial line generator
    """
    return LineRadial()
