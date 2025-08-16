from math import isnan

from ...types import T
from ..series import Series


def offset_none(series: list[Series[T]], order: list[int]):
    """
    Applies a zero baseline.

    Parameters
    ----------
    series : list[Series[T]]
        List of series
    order : list[int]
        List of ordered indices
    """
    n = len(series)
    if n == 0:
        return
    s1: Series[T] = series[order[0]]
    m = len(s1)
    for i in range(1, n):
        s0: Series[T] = s1
        s1: Series[T] = series[order[i]]
        for j in range(m):
            s1[j][0] = s0[j][0] if isnan(s0[j][1]) else s0[j][1]
            s1[j][1] += s1[j][0]
