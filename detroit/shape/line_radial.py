from .curves import Curve, curve_radial, curve_radial_linear
from .line import Line
from collections.abc import Callable
from ..selection import Selection
from ..types import Accessor, T, Number
from typing import TypeVar

TLineRadial = TypeVar("LineRadial", bound="LineRadial")

class LineRadial(Line):

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
        super().set_curve(curve_radial(curve))

    def angle(self, angle: Accessor[T, float] | Number) -> TLineRadial:
        """
        Sets x accessor function

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
        Sets y accessor function

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

def line_radial():
    return LineRadial()
