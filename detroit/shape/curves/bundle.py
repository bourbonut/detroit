from collections.abc import Callable

from ...selection import Selection
from ...types import Number
from .basis import BasisCurve, curve_basis
from .common import Curve


class BundleCurve(Curve):
    def __init__(self, context, beta):
        self._basis = BasisCurve(context)
        self._beta = beta
        self._x = None
        self._y = None

    def area_start(self):
        return

    def area_end(self):
        return

    def line_start(self):
        self._x = []
        self._y = []
        self._basis.line_start()

    def line_end(self):
        x = self._x
        y = self._y
        j = len(x) - 1

        if j > 0:
            x0 = x[0]
            y0 = y[0]
            dx = x[j] - x0
            dy = y[j] - y0

            i = 0
            while i <= j:
                t = i / j
                self._basis.point(
                    self._beta * x[i] + (1 - self._beta) * (x0 + t * dx),
                    self._beta * y[i] + (1 - self._beta) * (y0 + t * dy),
                )
                i += 1

        self._x = None
        self._y = None
        self._basis.line_end()

    def point(self, x, y):
        self._x.append(x)
        self._y.append(y)


def curve_bundle(
    context_or_beta: Selection | Number,
) -> Callable[[Selection], Curve] | Curve:
    """
    Produces a straightened cubic basis spline using the specified control
    points, with the spline straightened according to the curve's beta. This
    curve is typically used in hierarchical edge bundling to disambiguate
    connections, as proposed by Danny Holten in Hierarchical Edge Bundles:
    Visualization of Adjacency Relations in Hierarchical Data.
    Default value of beta is :code:`0.85`.

    Parameters
    ----------
    context_or_beta : Selection | Number
        Context or beta value in range :math:`[0, 1]` representing the bundle
        strength

    Returns
    -------
    Callable[[Selection], Curve] | Curve
        Curve object or function which makes a curve object with beta value set
    """
    if isinstance(context_or_beta, (int, float)):
        beta = context_or_beta
        if beta == 1:
            return curve_basis

        def local_curve(context):
            return BundleCurve(context, beta)

        return local_curve
    context = context_or_beta
    return BundleCurve(context, 0.85)
