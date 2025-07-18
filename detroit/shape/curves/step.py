import math

from ...selection import Selection
from .common import Curve, isvaluable


class StepCurve(Curve):
    def __init__(self, context, t):
        self._context = context
        self._t = t
        self._line = math.nan
        self._x = math.nan
        self._y = math.nan

    def area_start(self):
        self._line = 0

    def area_end(self):
        self._line = math.nan

    def line_start(self):
        self._x = math.nan
        self._y = math.nan
        self._point = 0

    def line_end(self):
        if 0 < self._t < 1 and self._point == 2:
            self._context.line_to(self._x, self._y)
        if isvaluable(self._line) or (self._line != 0 and self._point == 1):
            self._context.close_path()
        if self._line >= 0:
            self._t = 1 - self._t
            self._line = 1 - self._line

    def point(self, x, y):
        if self._point == 0:
            self._point = 1
            if isvaluable(self._line):
                self._context.line_to(x, y)
            else:
                self._context.move_to(x, y)
        elif self._point == 1:
            self._point = 2
            if self._t <= 0:
                self._context.line_to(self._x, y)
                self._context.line_to(x, y)
            else:
                x1 = self._x * (1 - self._t) + x * self._t
                self._context.line_to(x1, self._y)
                self._context.line_to(x1, y)
        else:
            if self._t <= 0:
                self._context.line_to(self._x, y)
                self._context.line_to(x, y)
            else:
                x1 = self._x * (1 - self._t) + x * self._t
                self._context.line_to(x1, self._y)
                self._context.line_to(x1, y)
        self._x = x
        self._y = y


def curve_step(context: Selection) -> Curve:
    """
    Produces a piecewise constant function (a step function) consisting of
    alternating horizontal and vertical lines. The y-value changes at the
    midpoint of each pair of adjacent x-values.

    Parameters
    ----------
    context : Selection
        Context

    Returns
    -------
    Curve
        Curve object

    Examples
    --------

    >>> points = [
    ...     [2, 2],
    ...     [6, 8],
    ...     [10, 10],
    ...     [12, 10],
    ...     [14, 4],
    ...     [20, 4],
    ...     [24, 8],
    ...     [29, 6],
    ...     [32, 4],
    ...     [35, 5],
    ...     [38, 2],
    ... ]
    >>> line = d3.line().curve(d3.curve_step)
    >>> line(points)
    'M2,2L4,2L4,8L8,8L8,10L11,10L11,10L13,10L13,4L17,4L17,4L22,4L22,8L26.500,8L26.500,6L30.500,6L30.500,4L33.500,4L33.500,5L36.500,5L36.500,2L38,2'

    **Result**

    .. image:: ../../figures/light_curve_step.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_step.svg
       :align: center
       :class: only-dark
    """
    return StepCurve(context, 0.5)


def curve_step_before(context: Selection) -> Curve:
    """
    Produces a piecewise constant function (a step function) consisting of
    alternating horizontal and vertical lines. The y-value changes before the
    x-value.

    Parameters
    ----------
    context : Selection
        Context

    Returns
    -------
    Curve
        Curve object

    Examples
    --------

    >>> points = [
    ...     [2, 2],
    ...     [6, 8],
    ...     [10, 10],
    ...     [12, 10],
    ...     [14, 4],
    ...     [20, 4],
    ...     [24, 8],
    ...     [29, 6],
    ...     [32, 4],
    ...     [35, 5],
    ...     [38, 2],
    ... ]
    >>> line = d3.line().curve(d3.curve_step_before)
    >>> line(points)
    'M2,2L2,8L6,8L6,10L10,10L10,10L12,10L12,4L14,4L14,4L20,4L20,8L24,8L24,6L29,6L29,4L32,4L32,5L35,5L35,2L38,2'

    **Result**

    .. image:: ../../figures/light_curve_step_before.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_step_before.svg
       :align: center
       :class: only-dark
    """
    return StepCurve(context, 0.0)


def curve_step_after(context: Selection) -> Curve:
    """
    Produces a piecewise constant function (a step function) consisting of
    alternating horizontal and vertical lines. The y-value changes after the
    x-value.

    Parameters
    ----------
    context : Selection
        Context

    Returns
    -------
    Curve
        Curve object

    Examples
    --------

    >>> points = [
    ...     [2, 2],
    ...     [6, 8],
    ...     [10, 10],
    ...     [12, 10],
    ...     [14, 4],
    ...     [20, 4],
    ...     [24, 8],
    ...     [29, 6],
    ...     [32, 4],
    ...     [35, 5],
    ...     [38, 2],
    ... ]
    >>> line = d3.line().curve(d3.curve_step_after)
    >>> line(points)
    'M2,2L6,2L6,8L10,8L10,10L12,10L12,10L14,10L14,4L20,4L20,4L24,4L24,8L29,8L29,6L32,6L32,4L35,4L35,5L38,5L38,2'

    **Result**

    .. image:: ../../figures/light_curve_step_after.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_step_after.svg
       :align: center
       :class: only-dark
    """
    return StepCurve(context, 1.0)
