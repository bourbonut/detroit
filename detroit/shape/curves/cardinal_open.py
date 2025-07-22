import math
from collections.abc import Callable

from ...selection import Selection
from ...types import Number
from .cardinal import BezierTrait
from .common import Curve, isvaluable


class CardinalOpenCurve(Curve, BezierTrait):
    def __init__(self, context, tension):
        self._context = context
        self._k = (1 - tension) / 6
        self._line = math.nan

    def area_start(self):
        self._line = 0

    def area_end(self):
        self._line = math.nan

    def line_start(self):
        self._x0 = math.nan
        self._y0 = math.nan
        self._x1 = math.nan
        self._y1 = math.nan
        self._x2 = math.nan
        self._y2 = math.nan
        self._point = 0

    def line_end(self):
        if isvaluable(self._line) or (self._line != 0 and self._point == 3):
            self._context.close_path()
        self._line = 1 - self._line

    def point(self, x, y):
        if self._point == 0:
            self._point = 1
        elif self._point == 1:
            self._point = 2
        elif self._point == 2:
            self._point = 3
            if isvaluable(self._line):
                self._context.line_to(self._x2, self._y2)
            else:
                self._context.move_to(self._x2, self._y2)
        elif self._point == 3:
            self._point = 4
            self._bezier_curve_to(x, y)
        else:
            self._bezier_curve_to(x, y)
        self._x0 = self._x1
        self._x1 = self._x2
        self._x2 = x
        self._y0 = self._y1
        self._y1 = self._y2
        self._y2 = y


def curve_cardinal_open(
    context_or_tension: Selection | Number,
) -> Callable[[Selection], Curve] | Curve:
    """
    Produces a cubic cardinal spline using the specified control points. Unlike
    curveCardinal, one-sided differences are not used for the first and last
    piece, and thus the curve starts at the second point and ends at the
    penultimate point.
    The default tension is :math:`0`.

    Parameters
    ----------
    context_or_tension : Selection | Number
        Context or tension value in range :math:`[0, 1]` determining the length
        of the tangents. A tension of one yields all zero tangents, equivalent
        to :func:`d3.curve_linear <curve_linear>`

    Returns
    -------
    Callable[[Selection], Curve] | Curve
        Curve object or function which makes a curve object with tension value
        set

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
    >>> line(points)
    'M6,8C7.333,9.333,9,9.667,10,10C11,10.333,11.333,11,12,10C12.667,9,12.667,5,14,4C15.333,3,18.333,3.333,20,4C21.667,4.667,22.500,7.667,24,8C25.500,8.333,27.667,6.667,29,6C30.333,5.333,31,4.167,32,4C33,3.833,34,5.333,35,5'
    >>> line = d3.line().curve(d3.curve_cardinal_open(0.5))
    >>> line(points)
    'M6,8C6.667,8.667,9.500,9.833,10,10C10.500,10.167,11.667,10.500,12,10C12.333,9.500,13.333,4.500,14,4C14.667,3.500,19.167,3.667,20,4C20.833,4.333,23.250,7.833,24,8C24.750,8.167,28.333,6.333,29,6C29.667,5.667,31.500,4.083,32,4C32.500,3.917,34.500,5.167,35,5'

    **Result**

    .. image:: ../../figures/light_curve_cardinal_open.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_cardinal_open.svg
       :align: center
       :class: only-dark
    """
    if isinstance(context_or_tension, (int, float)):
        tension = context_or_tension

        def local_curve(context):
            return CardinalOpenCurve(context, tension)

        return local_curve
    context = context_or_tension
    return CardinalOpenCurve(context, 0.0)
