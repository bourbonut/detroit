from math import inf

from ...types import T
from ..series import Series
from .none import order_none


def order_appearance(series: list[Series[T]]) -> list[int]:
    """
    Returns a series order such that the earliest series (according to the
    maximum value) is at the bottom.


    Parameters
    ----------
    series : list[Series[T]]
        List of series

    Returns
    -------
    list[int]
        List of ordered indices
    """
    peaks = list(map(peak, series))
    return sorted(order_none(series), key=lambda i: peaks[i])


def peak(series: Series) -> int:
    vj = -inf
    j = 0
    for i in range(len(series)):
        vi = float(series[i][1])
        if vi > vj:
            vj = vi
            j = i
    return j
