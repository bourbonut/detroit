from collections.abc import Callable
from typing import TypeVar

from ..selection import Selection
from ..types import Accessor, Number, T
from .area import Area
from .curves import Curve, curve_radial, curve_radial_linear
from .line_radial import LineRadial

TAreaRadial = TypeVar("AreaRadial", bound="AreaRadial")


class AreaRadial(Area[T]):
    def __init__(self):
        Area.__init__(self)
        super().set_curve(curve_radial_linear)

    def set_curve(self, curve: Callable[[Selection], Curve]) -> TAreaRadial:
        """
        Sets curve.

        Parameters
        ----------
        curve : Callable[[Selection], Curve]
            Curve factory function

        Returns
        -------
        AreaRadial
            Itself
        """
        return super().set_curve(curve_radial(curve))

    def angle(self, angle: Accessor[T, float] | Number) -> TAreaRadial:
        """
        Sets angle accessor function

        Parameters
        ----------
        angle : Accessor[T, float] | Number
            angle accessor function

        Returns
        -------
        AreaRadial
            Itself
        """
        return super().x(angle)

    def start_angle(self, start_angle: Accessor[T, float] | Number) -> TAreaRadial:
        """
        Sets start angle accessor function

        Parameters
        ----------
        start_angle : Accessor[T, float] | Number
            angle accessor function

        Returns
        -------
        AreaRadial
            Itself
        """
        return super().x0(start_angle)

    def end_angle(self, end_angle: Accessor[T, float] | Number) -> TAreaRadial:
        """
        Sets start angle accessor function

        Parameters
        ----------
        end_angle : Accessor[T, float] | Number
            angle accessor function

        Returns
        -------
        AreaRadial
            Itself
        """
        return super().x1(end_angle)

    def radius(self, radius: Accessor[T, float] | Number) -> TAreaRadial:
        """
        Sets radius accessor function

        Parameters
        ----------
        radius : Accessor[T, float] | Number
            radius accessor function

        Returns
        -------
        AreaRadial
            Itself
        """
        return super().y(radius)

    def inner_radius(self, inner_radius: Accessor[T, float] | Number) -> TAreaRadial:
        """
        Sets inner radius accessor function

        Parameters
        ----------
        inner_radius : Accessor[T, float] | Number
            radius accessor function

        Returns
        -------
        AreaRadial
            Itself
        """
        return super().y0(inner_radius)

    def outer_radius(self, outer_radius: Accessor[T, float] | Number) -> TAreaRadial:
        """
        Sets outer radius accessor function

        Parameters
        ----------
        outer_radius : Accessor[T, float] | Number
            radius accessor function

        Returns
        -------
        AreaRadial
            Itself
        """
        return super().y1(outer_radius)

    def line_start_angle(self) -> LineRadial:
        """
        Returns a new radial line generator that has this radial area
        generator's current defined accessor, curve and context. The line's
        angle accessor is this area's start angle accessor, and the line's
        radius accessor is this area's inner radius accessor.


        Returns
        -------
        LineRadial
            Radial line generator based on the area parameters
        """
        line_x0 = super().line_x0()
        return (
            LineRadial()
            .angle(line_x0.get_x())
            .radius(line_x0.get_y())
            .set_defined(line_x0.get_defined())
            .set_context(line_x0.get_context())
            .set_curve(line_x0.get_curve())
        )

    def line_end_angle(self) -> LineRadial:
        """
        Returns a new radial line generator that has this radial area
        generator's current defined accessor, curve and context. The line's
        angle accessor is this area's end angle accessor, and the line's radius
        accessor is this area's inner radius accessor.

        Returns
        -------
        LineRadial
            Radial line generator based on the area parameters
        """
        line_x1 = super().line_x1()
        return (
            LineRadial()
            .angle(line_x1.get_x())
            .radius(line_x1.get_y())
            .set_defined(line_x1.get_defined())
            .set_context(line_x1.get_context())
            .set_curve(line_x1.get_curve())
        )

    def line_inner_radius(self) -> LineRadial:
        """
        Returns a new radial line generator that has this radial area
        generator's current defined accessor, curve and context. The line's
        angle accessor is this area's start angle accessor, and the line's
        radius accessor is this area's inner radius accessor.

        Returns
        -------
        LineRadial
            Radial line generator based on the area parameters
        """
        line_y0 = super().line_y0()
        return (
            LineRadial()
            .angle(line_y0.get_x())
            .radius(line_y0.get_y())
            .set_defined(line_y0.get_defined())
            .set_context(line_y0.get_context())
            .set_curve(line_y0.get_curve())
        )

    def line_outer_radius(self) -> LineRadial:
        """
        Returns a new radial line generator that has this radial area
        generator's current defined accessor, curve and context. The line's
        angle accessor is this area's start angle accessor, and the line's
        radius accessor is this area's outer radius accessor.

        Returns
        -------
        LineRadial
            Radial line generator based on the area parameters
        """
        line_y1 = super().line_y1()
        return (
            LineRadial()
            .angle(line_y1.get_x())
            .radius(line_y1.get_y())
            .set_defined(line_y1.get_defined())
            .set_context(line_y1.get_context())
            .set_curve(line_y1.get_curve())
        )

    def get_angle(self) -> Accessor[T, float]:
        return super().get_x()

    def get_start_angle(self) -> Accessor[T, float]:
        return super().get_x0()

    def get_end_angle(self) -> Accessor[T, float]:
        return super().get_x1()

    def get_radius(self) -> Accessor[T, float]:
        return super().get_y()

    def get_inner_radius(self) -> Accessor[T, float]:
        return super().get_y0()

    def get_outer_radius(self) -> Accessor[T, float]:
        return super().get_y1()


def area_radial() -> AreaRadial:
    """
    A radial area generator is like the Cartesian area generator except the x
    and y accessors are replaced with angle and radius accessors. Radial areas
    are positioned relative to the origin; use a transform to change the
    origin.

    Returns
    -------
    AreaRadial
        Radial area generator
    """
    return AreaRadial()
