from ...selection import Selection
from .common import Curve


class LinearClosedCurve(Curve):
    def __init__(self, context):
        self._context = context

    def area_start(self):
        return

    def area_end(self):
        return

    def line_start(self):
        self._point = 0

    def line_end(self):
        if self._point != 0:
            self._context.close_path()

    def point(self, x, y):
        if self._point != 0:
            self._context.line_to(x, y)
        else:
            self._point = 1
            self._context.move_to(x, y)


def curve_linear_closed(context: Selection) -> Curve:
    """
    Produces a closed polyline through the specified points by repeating the
    first point when the line segment ends.

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
    >>> line = d3.line().curve(d3.curve_linear_closed)
    >>> line(points)
    'M2,2L6,8L10,10L12,10L14,4L20,4L24,8L29,6L32,4L35,5L38,2Z'

    **Result**

    .. image:: ../../figures/light_curve_linear_closed.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_linear_closed.svg
       :align: center
       :class: only-dark
    """
    return LinearClosedCurve(context)
