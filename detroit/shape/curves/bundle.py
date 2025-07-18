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
    >>> line = d3.line().curve(d3.curve_bundle)
    >>> line(points)
    'M2,2L2.657,2.850C3.313,3.700,4.627,5.400,5.940,6.533C7.253,7.667,8.567,8.233,9.597,8.517C10.627,8.800,11.373,8.800,12.120,7.950C12.867,7.100,13.613,5.400,14.927,4.550C16.240,3.700,18.120,3.700,19.717,4.267C21.313,4.833,22.627,5.967,24.082,6.250C25.537,6.533,27.133,5.967,28.447,5.400C29.760,4.833,30.790,4.267,31.820,4.125C32.850,3.983,33.880,4.267,34.910,3.983C35.940,3.700,36.970,2.850,37.485,2.425L38,2'
    >>> line = d3.line().curve(d3.curve_bundle(0.5))
    >>> line(points)
    'M2,2L2.633,2.500C3.267,3,4.533,4,5.800,4.667C7.067,5.333,8.333,5.667,9.433,5.833C10.533,6,11.467,6,12.400,5.500C13.333,5,14.267,4,15.533,3.500C16.800,3,18.400,3,19.833,3.333C21.267,3.667,22.533,4.333,23.883,4.500C25.233,4.667,26.667,4.333,27.933,4C29.200,3.667,30.300,3.333,31.400,3.250C32.500,3.167,33.600,3.333,34.700,3.167C35.800,3,36.900,2.500,37.450,2.250L38,2'

    **Result**

    .. image:: ../../figures/light_curve_bundle.svg
       :align: center
       :class: only-light

    .. image:: ../../figures/dark_curve_bundle.svg
       :align: center
       :class: only-dark
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
