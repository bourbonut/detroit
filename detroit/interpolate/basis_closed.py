from .basis import basis
from collections.abc import Callable


def interpolate_basis_closed(values: list[float]) -> Callable[[float], float]:
    """
    Returns a uniform nonrational B-spline interpolator through
    the specified array of values, which must be numbers.

    The control points are implicitly repeated such that the resulting
    one-dimensional spline has cyclical :math:`C^2` continuity when repeated
    around :math:`t` in :math:`[0, 1]`.

    Parameters
    ----------
    values : list[float]
        List of inputs

    Returns
    -------
    Callable[[float], float]
        Interpolator function
    """
    n = len(values)

    def interpolate(t):
        i = int((t % 1) * n)
        v0 = values[(i + n - 1) % n]
        v1 = values[i % n]
        v2 = values[(i + 1) % n]
        v3 = values[(i + 2) % n]
        return basis((t - i / n) * n, v0, v1, v2, v3)

    return interpolate
