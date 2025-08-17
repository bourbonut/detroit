from collections.abc import Callable, Iterable
from typing import Generic, TypeVar

from ..array import argpass
from ..selection.selection import Selection
from ..types import Accessor, Number, T
from .constant import constant
from .curves import Curve, curve_linear
from .path import WithPath
from .point import x as point_x
from .point import y as point_y

TLine = TypeVar("Line", bound="Line")


class Line(Generic[T], WithPath):
    """
    The line generator produces a spline or polyline as in a line chart.
    Lines also appear in many other visualization types, such as the links
    in hierarchical edge bundling.

    Parameters
    ----------
    x : Accessor[T, float] | None
        x accessor function for data points
    y : Accessor[T, float] | None
        y accessor function for data points

    Returns
    -------
    Line
        New line generator
    """

    def __init__(
        self, x: Accessor[T, float] | None = None, y: Accessor[T, float] | None = None
    ):
        super().__init__()
        self._defined = constant(True)
        self._context = None
        self._curve = curve_linear
        self._output = None

        if x is None:
            self._x = point_x
        elif callable(x):
            self._x = x
        else:
            self._x = constant(x)

        if y is None:
            self._y = point_y
        elif callable(y):
            self._y = y
        else:
            self._y = constant(y)

        self._x = argpass(self._x)
        self._y = argpass(self._y)

    def __call__(self, data: Iterable[T]) -> str | None:
        """
        Generate a line for the given list of data

        Parameters
        ----------
        data : Iterable[T]
            Data values

        Returns
        -------
        str | None
            Generated line if the line is not associated to a context

        Examples
        --------

        >>> svg.append("path").attr("d", line(data)).attr("stroke", "currentColor")
        """
        data = list(data)
        n = len(data)
        if n == 0:
            return None
        defined0 = False

        buffer = None
        if self._context is None:
            buffer = self._path()
            self._output = self._curve(buffer)

        for i in range(n + 1):
            d = data[i] if i < n else None
            if not (i < n and self._defined(d, i, data) == defined0):
                defined0 = not defined0
                if defined0:
                    self._output.line_start()
                else:
                    self._output.line_end()
            if defined0:
                self._output.point(self._x(d, i, data), self._y(d, i, data))

        if buffer:
            self._output = None
            return str(buffer) or None

    def x(self, x: Accessor[T, float] | Number) -> TLine:
        """
        Sets x accessor function

        Parameters
        ----------
        x : Accessor[T, float] | Number
            x accessor function

        Returns
        -------
        Line
            Itself
        """
        if callable(x):
            self._x = x
        else:
            self._x = constant(x)
        self._x = argpass(self._x)
        return self

    def y(self, y: Accessor[T, float] | Number) -> TLine:
        """
        Sets y accessor function

        Parameters
        ----------
        y : Accessor[T, float] | Number
            y accessor function

        Returns
        -------
        Line
            Itself
        """
        if callable(y):
            self._y = y
        else:
            self._y = constant(y)
        self._y = argpass(self._y)
        return self

    def set_defined(self, defined: Accessor[T, bool] | Number) -> TLine:
        """
        Sets defined accessor

        When a line is generated, the defined accessor will be invoked
        for each element in the input data array, being passed the element
        :code:`d`, the index :code:`i`, and the array :code:`data` as three
        arguments. If the given element is defined (i.e., if the defined accessor
        returns a truthy value for this element), the x and y accessors will
        subsequently be evaluated and the point will be added to the current
        line segment. Otherwise, the element will be skipped, the current line
        segment will be ended, and a new line segment will be generated for the
        next defined point.

        Parameters
        ----------
        defined : Accessor[T, bool] | Number
            defined accessor function

        Returns
        -------
        Line
            Itself
        """
        if defined is None:
            self._defined = defined
        elif callable(defined):
            self._defined = defined
        else:
            self._defined = constant(bool(defined))
        return self

    def set_curve(self, curve: Callable[[Selection], Curve] | None = None) -> TLine:
        """
        Sets curve factory.

        Parameters
        ----------
        curve : Callable[[Selection], Curve] | None
            Curve factory function

        Returns
        -------
        Line
            Itself
        """
        self._curve = curve
        if self._context is not None:
            self._output = self._curve(self._context)
        return self

    def set_context(self, context: Selection | None = None) -> TLine:
        """
        Sets the context.

        Parameters
        ----------
        context : Selection | None
            Selection

        Returns
        -------
        Line
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
        return self._x

    def get_y(self) -> Accessor[T, float]:
        return self._y

    def get_defined(self) -> Accessor[T, bool]:
        return self._defined

    def get_curve(self) -> Callable[[Selection], Curve]:
        return self._curve

    def get_context(self) -> Selection:
        return self._context
