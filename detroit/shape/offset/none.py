from math import isnan

from ..series import Series


def offset_none(series: list[Series], order: list[int]):
    """
    Applies a zero baseline.

    Parameters
    ----------
    series : list[Series]
        List of series
    order : list[int]
        List of ordered indices
    """
    n = len(series)
    if n == 0:
        return
    s1: Series = series[order[0]]
    m = len(s1)
    for i in range(1, n):
        s0: Series = s1
        s1: Series = series[order[i]]
        for j in range(m):
            s1[j][0] = s0[j][0] if isnan(s0[j][1]) else s0[j][1]
            s1[j][1] += s1[j][0]
