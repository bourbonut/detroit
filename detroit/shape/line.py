from __future__ import annotations

from collections.abc import Callable, Iterable
from inspect import signature

from ..selection.selection import Selection
from .constant import constant
from .curves.linear import LinearCurve
from .path import WithPath
from .point import x as point_x
from .point import y as point_y


class Line(WithPath):
    """
    The line generator produces a spline or polyline as in a line chart.
    Lines also appear in many other visualization types, such as the links
    in hierarchical edge bundling.

    Parameters
    ----------
    x : Callable | None
        x accessor function for data points
    y : Callable | None
        y accessor function for data points

    Returns
    -------
    Line
        New line generator
    """

    def __init__(self, x: Callable | None = None, y: Callable | None = None):
        super().__init__()
        self._defined = constant(True)
        self._context = None
        self._curve = LinearCurve
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

    def __call__(self, data: Iterable) -> str | None:
        """
        Generate a line for the given list of data

        Parameters
        ----------
        data : Iterable
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

        xnargs = len(signature(self._x).parameters)
        ynargs = len(signature(self._y).parameters)
        for i in range(n + 1):
            d = data[i] if i < n else None
            if not(i < n and self._defined(d, i, data) == defined0):
                defined0 = not defined0
                if defined0:
                    self._output.line_start()
                else:
                    self._output.line_end()
            if defined0:
                xargs = [d, i, data][:xnargs]
                yargs = [d, i, data][:ynargs]
                self._output.point(self._x(*xargs), self._y(*yargs))

        if buffer:
            self._output = None
            return str(buffer) or None

    def x(self, x: Callable | int | float) -> Line:
        """
        Sets x accessor function

        Parameters
        ----------
        x : Callable | int | float
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
        return self

    @property
    def fx(self):
        return self._x

    def y(self, y: Callable | int | float) -> Line:
        """
        Sets y accessor function

        Parameters
        ----------
        y : Callable | int | float
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
        return self

    @property
    def fy(self):
        return self._y

    def defined(self, defined: Callable | int | float) -> Line:
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
        defined : Callable | int | float
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

    @property
    def accessor_defined(self):
        return self._defined

    def curve(self, curve: Callable | None = None) -> Line:
        """
        Sets curve factory.

        Parameters
        ----------
        curve : Callable | None
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

    @property
    def fcurve(self):
        return self._curve

    def context(self, context: Selection | None = None) -> Line:
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

    @property
    def own_context(self):
        return self._context
