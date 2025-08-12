from math import isnan

from ...types import T
from ..series import Series
from .none import order_none


def order_ascending(series: list[Series[T]]) -> list[int]:
    """
    Returns a series order such that the smallest series (according to the sum
    of values) is at the bottom.

    Parameters
    ----------
    series : list[Series[T]]
        List of series

    Returns
    -------
    list[int]
        List of ordered indices
    """
    sums = list(map(_sum, series))
    return sorted(order_none(series), key=lambda i: sums[i])


def _sum(series: list[Series[T]]) -> float:
    s = 0
    for i in range(len(series)):
        v = float(series[i][1])
        if not isnan(v):
            s += v
    return s
