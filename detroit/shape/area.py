from collections.abc import Callable, Iterable
from typing import Generic, TypeVar

from ..array import argpass
from ..selection.selection import Selection
from ..types import Accessor, Number, T
from .constant import constant
from .curves import Curve, curve_linear
from .line import Line
from .path import WithPath
from .point import x as point_x
from .point import y as point_y

TArea = TypeVar("Area", bound="Area")


class Area(Generic[T], WithPath):
    """
    The area generator produces an area defined by a topline and a baseline as in
    an area chart. Typically, the two lines share the same x-values (x0 = x1),
    differing only in y-value (y0 and y1); most commonly, y0 is defined as a
    constant representing zero (the y scale's output for zero). The topline
    is defined by x1 and y1 and is rendered first; the baseline is defined by
    x0 and y0 and is rendered second with the points in reverse order. With a
    curveLinear curve, this produces a clockwise polygon. See also radial areas.

    Parameters
    ----------
    x0 : Accessor[T, float] | None
        x0 accessor function for data points
    y0 : Accessor[T, float] | None
        y0 accessor function for data points
    y1 : Accessor[T, float] | None
        y1 accessor function for data points

    Returns
    -------
    Area
        New area generator
    """

    def __init__(
        self,
        x0: Accessor[T, float] | None = None,
        y0: Accessor[T, float] | None = None,
        y1: Accessor[T, float] | None = None,
    ):
        super().__init__()
        self._x1 = None
        self._defined = constant(True)
        self._context = None
        self._curve = curve_linear
        self._output = None

        if x0 is None:
            self._x0 = point_x
        elif callable(x0):
            self._x0 = x0
        else:
            self._x0 = constant(x0)

        if y0 is None:
            self._y0 = constant(0)
        elif callable(y0):
            self._y0 = y0
        else:
            self._y0 = constant(y0)

        if y1 is None:
            self._y1 = point_y
        elif callable(y1):
            self._y1 = y1
        else:
            self._y1 = constant(y1)

        self._x0 = argpass(self._x0)
        self._x1 = argpass(self._x1) if self._x1 else None
        self._y0 = argpass(self._y0)
        self._y1 = argpass(self._y1) if self._y1 else None

    def __call__(self, data: Iterable[T]) -> str | None:
        """
        Generates an area for the given array of data.

        Parameters
        ----------
        data : Iterable[T]
            Data values

        Returns
        -------
        str | None
            Generated area if the area is not associated to a context

        Examples
        --------

        >>> svg.append("path").attr("d", area(data))
        """
        data = list(data)
        n = len(data)
        if n == 0:
            return None
        defined0 = False

        x0z = [0] * n
        y0z = [0] * n

        buffer = None
        if self._context is None:
            buffer = self._path()
            self._output = self._curve(buffer)

        j = 0
        for i in range(n + 1):
            d = data[i] if i < n else None
            if not (i < n and self._defined(d, i, data) == defined0):
                defined0 = not defined0
                if defined0:
                    j = i
                    self._output.area_start()
                    self._output.line_start()
                else:
                    self._output.line_end()
                    self._output.line_start()
                    for k in range(i - 1, j - 1, -1):
                        self._output.point(x0z[k], y0z[k])
                    self._output.line_end()
                    self._output.area_end()

            if defined0:
                x0z[i] = self._x0(d, i, data)
                y0z[i] = self._y0(d, i, data)
                self._output.point(
                    self._x1(d, i, data) if self._x1 else x0z[i],
                    self._y1(d, i, data) if self._y1 else y0z[i],
                )

        if buffer:
            self._output = None
            return str(buffer) or None

    def area_line(self) -> Line:
        """
        Returns a new line generator from the definition of the area.

        Returns
        -------
        Line
            Line generator based on the area parameters
        """
        return (
            Line()
            .set_defined(self._defined)
            .set_curve(self._curve)
            .set_context(self._context)
        )

    def line_x0(self) -> Line:
        """
        Returns a new line generator that has this area generator's current
        defined accessor, curve and context. The line's x-accessor is this
        area's x0-accessor, and the line's y-accessor is this area's
        y0-accessor.

        Returns
        -------
        Line
            Line generator based on the area parameters
        """
        return self.area_line().x(self._x0).y(self._y0)

    def line_y0(self) -> Line:
        """
        Returns a new line generator that has this area generator's current
        defined accessor, curve and context. The line's x-accessor is this
        area's x0-accessor, and the line's y-accessor is this area's
        y0-accessor.

        Returns
        -------
        Line
            Line generator based on the area parameters
        """
        return self.area_line().x(self._x0).y(self._y0)

    def line_x1(self) -> Line:
        """
        Returns a new line generator that has this area generator's current
        defined accessor, curve and context. The line's x-accessor is this
        area's x1-accessor, and the line's y-accessor is this area's
        y0-accessor.

        Returns
        -------
        Line
            Line generator based on the area parameters
        """
        return self.area_line().x(self._x1).y(self._y0)

    def line_y1(self) -> Line:
        """
        Returns a new line generator that has this area generator's current
        defined accessor, curve and context. The line's x-accessor is this
        area's x0-accessor, and the line's y-accessor is this area's
        y1-accessor.

        Returns
        -------
        Line
            Line generator based on the area parameters
        """
        return self.area_line().x(self._x0).y(self._y1)

    def x(self, x: Accessor[T, float] | Number) -> TArea:
        """
        Sets x0 accessor function and sets x1
        accessor function to :code:`None`

        Parameters
        ----------
        x : Accessor[T, float] | Number
            x accessor function

        Returns
        -------
        Area
            Itself
        """
        if callable(x):
            self._x0 = x
        else:
            self._x0 = constant(x)
        self._x0 = argpass(self._x0)
        self._x1 = None
        return self

    def x0(self, x0: Accessor[T, float] | Number) -> TArea:
        """
        Sets x0 accessor function

        Parameters
        ----------
        x0 : Accessor[T, float] | Number
            x0 accessor function

        Returns
        -------
        Area
            Itself
        """
        if callable(x0):
            self._x0 = x0
        else:
            self._x0 = constant(x0)
        self._x0 = argpass(self._x0)
        return self

    def x1(self, x1: Accessor[T, float] | Number) -> TArea:
        """
        Sets x1 accessor function

        Parameters
        ----------
        x1 : Accessor[T, float] | Number
            x1 accessor function

        Returns
        -------
        Area
            Itself
        """
        if callable(x1):
            self._x1 = x1
        else:
            self._x1 = constant(x1)
        self._x1 = argpass(self._x1)
        return self

    def y(self, y: Accessor[T, float] | Number) -> TArea:
        """
        Sets y0 accessor function and sets y1
        accessor function to :code:`None`

        Parameters
        ----------
        y : Accessor[T, float] | Number
            y accessor function

        Returns
        -------
        Area
            Itself
        """
        if callable(y):
            self._y0 = y
        else:
            self._y0 = constant(y)
        self._y0 = argpass(self._y0)
        self._y1 = None
        return self

    def y0(self, y0: Accessor[T, float] | Number) -> TArea:
        """
        Sets y accessor function

        Parameters
        ----------
        y0 : Accessor[T, float] | Number
            y0 accessor function

        Returns
        -------
        Area
            Itself
        """
        if callable(y0):
            self._y0 = y0
        else:
            self._y0 = constant(y0)
        self._y0 = argpass(self._y0)
        return self

    def y1(self, y1: Accessor[T, float] | Number) -> TArea:
        """
        Sets y accessor function

        Parameters
        ----------
        y1 : Accessor[T, float] | Number
            y1 accessor function

        Returns
        -------
        Area
            Itself
        """
        if callable(y1):
            self._y1 = y1
        else:
            self._y1 = constant(y1)
        self._y1 = argpass(self._y1)
        return self

    def set_defined(self, defined: Accessor[T, bool] | Number) -> TArea:
        """
        Sets defined accessor

        When an area is generated, the defined accessor will be invoked
        for each element in the input data array, being passed the element
        :code:`d`, the index :code:`i`, and the array :code:`data` as three
        arguments. If the given element is defined (i.e., if the defined
        accessor returns a truthy value for this element), the :code:`x0`,
        :code:`x1`, :code:`y0` and :code:`y1` accessors will subsequently
        be evaluated and the point will be added to the current area segment.
        Otherwise, the element will be skipped, the current area segment will
        be ended, and a new area segment will be generated for the next
        defined point. As a result, the generated area may have several
        discrete segments.


        Parameters
        ----------
        defined : Accessor[T, bool] | Number
            defined accessor function

        Returns
        -------
        Area
            Itself
        """
        if callable(defined):
            self._defined = defined
        else:
            self._defined = constant(bool(defined))
        return self

    def set_curve(self, curve: Callable[[Selection], Curve] | None = None) -> TArea:
        """
        Sets curve factory.

        Parameters
        ----------
        curve : Callable[[Selection], Curve] | None
            Curve factory function

        Returns
        -------
        Area
            Itself
        """
        self._curve = curve
        if self._context is not None:
            self._output = self._curve(self._context)
        return self

    def set_context(self, context: Selection | None = None) -> TArea:
        """
        Sets the context.

        Parameters
        ----------
        context : Selection | None
            Selection

        Returns
        -------
        Area
            Itself
        """
        if context is None:
            self._context = None
            self._output = None
        else:
            self._context = context
            self._output = self._curve(self._context)
        return self

    def get_x(self) -> Accessor[T, float]:
        return self._x0

    def get_y(self) -> Accessor[T, float]:
        return self._y0

    def get_x0(self) -> Accessor[T, float]:
        return self._x0

    def get_x1(self) -> Accessor[T, float]:
        return self._x1

    def get_y0(self) -> Accessor[T, float]:
        return self._y0

    def get_y1(self) -> Accessor[T, float]:
        return self._y1

    def get_defined(self) -> Accessor[T, float]:
        return self._defined

    def get_curve(self) -> Callable[[Selection], Curve]:
        return self._curve

    def get_context(self) -> Selection:
        return self._context
