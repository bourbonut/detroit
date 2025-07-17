from .cardinal_closed import curve_cardinal_closed
from .common import Curve
from .catmull_rom import BezierTrait
from ...selection import Selection
from ...types import Number
from collections.abc import Callable
import math

class CatmullRomClosedCurve(Curve, BezierTrait):

    def __init__(self, context, alpha):
        self._context = context
        self._alpha = alpha
        self._line = math.nan

    def area_start(self):
        return

    def area_end(self):
        return

    def line_start(self):
        self._x0 = math.nan
        self._y0 = math.nan
        self._x1 = math.nan
        self._y1 = math.nan
        self._x2 = math.nan
        self._y2 = math.nan
        self._x3 = math.nan
        self._y3 = math.nan
        self._x4 = math.nan
        self._y4 = math.nan
        self._x5 = math.nan
        self._y5 = math.nan
        self._l01_a = 0
        self._l12_a = 0
        self._l23_a = 0
        self._l01_2a = 0
        self._l12_2a = 0
        self._l23_2a = 0
        self._point = 0

    def line_end(self):
        if self._point == 1:
            self._context.move_to(self._x3, self._y3)
            self._context.close_path()
        elif self._point == 2:
            self._context.line_to(self._x3, self._y3)
            self._context.close_path()
        elif self._point == 3:
            self.point(self._x3, self._y3)
            self.point(self._x4, self._y4)
            self.point(self._x5, self._y5)

    def point(self, x, y):
        if self._point != 0:
            x23 = self._x2 - x
            y23 = self._y2 - y
            self._l23_2a = math.pow(x23 * x23 + y23 * y23, self._alpha)
            self._l23_a = math.sqrt(self._l23_2a)

        if self._point == 0:
            self._point = 1
            self._x3 = x
            self._y3 = y
        elif self._point == 1:
            self._point = 2
            self._x4 = x
            self._y4 = y
            self._context.move_to(self._x4, self._y4)
        elif self._point == 2:
            self._point = 3
            self._x5 = x
            self._y5 = y
        else:
            self._bezier_curve_to(x, y)

        self._l01_a = self._l12_a
        self._l12_a = self._l23_a
        self._l01_2a = self._l12_2a
        self._l12_2a = self._l23_2a
        self._x0 = self._x1
        self._x1 = self._x2
        self._x2 = x
        self._y0 = self._y1
        self._y1 = self._y2
        self._y2 = y

def curve_catmull_rom_closed(context_or_alpha: Selection | Number) -> Callable[[Selection], Curve] | Curve:
    if isinstance(context_or_alpha, (int, float)):
        alpha = context_or_alpha
        if alpha == 0.0:
            return curve_cardinal_closed(0.0)
        def local_curve(context):
            return CatmullRomClosedCurve(context, alpha)
        return local_curve
    context = context_or_alpha
    return CatmullRomClosedCurve(context, 0.5)
