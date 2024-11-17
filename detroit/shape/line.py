from .constant import constant
from .path import WithPath
from .point import x as point_x, y as point_y
from .curves.linear import LinearCurve

from collections.abc import Callable

class Line(WithPath):
    """
    Builds a line generator given x and y accessor
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

    def __call__(self, data: list):
        """
        Generate a line for the given list of data
        """
        data = list(data)
        n = len(data)
        defined0 = False
        
        if self._context is None:
            buffer = self._path()
            self._output = self._curve(buffer)


        for i in range(n):
            d = data[i]
            if i == n or self._defined(d, i, data) != defined0:
                defined0 = not defined0
                if defined0:
                    self._output.line_start()
                else:
                    self._output.line_end()
            if defined0:
                self._output.point(self._x(d, i, data), self._y(d, i, data))

        i += 1
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

    def x(self, *args):
        """
        Set x accessor
        """
        if args:
            x = args[0]
            if x is None:
                self._x = point_x
            elif callable(x):
                self._x = x
            else:
                self._x = constant(x)
            return self
        return self._x

    def y(self, *args):
        """
        Set y accessor
        """
        if args:
            y = args[0]
            if y is None:
                self._y = point_y
            elif callable(y):
                self._y = y
            else:
                self._y = constant(y)
            return self
        return self._y

    def defined(self, *args):
        """
        Set defined accessor
        """
        if args:
            defined = args[0]
            if defined is None:
                self._defined = defined
            elif callable(defined):
                self._defined = defined
            else:
                self._defined = constant(bool(defined))
            return self
        return self._defined

    def curve(self, *args):
        """
        Set curve factory
        """
        if args:
            self._curve = args[0]
            if self._context is not None:
                self._output = self._curve(self._context)
            return self
        return self._curve

    def context(self, *args):
        """
        Set line context
        """
        if args:
            context = args[0]
            if context is None:
                self._context = None
                self._output = None
            else:
                self._context = context
                self._output = self._curve(self._context)
            return self
        return self._context
