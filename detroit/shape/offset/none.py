from ..series import Series
from math import isnan


def offset_none(series: list[Series], order: list[int]):
    """
    Default offset function for updating the lower and upper values in the
    series list.

    Parameters
    ----------
    series : list[Series]
        List of series
    order : list[int]
        Order list
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
