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
    """
    return LinearClosedCurve(context)
