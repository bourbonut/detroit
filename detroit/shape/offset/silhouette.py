from math import isnan

from ...types import T
from ..series import Series
from .none import offset_none


def offset_silhouette(series: list[Series[T]], order: list[int]):
    """
    Shifts the baseline down such that the center of the streamgraph is always
    at zero.

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
    s0 = series[order[0]]
    m = len(s0)
    for j in range(m):
        y = 0.0
        for i in range(n):
            x = series[i][j][1]
            y += 0.0 if isnan(x) else x
        s0[j][0] = -y / 2
        s0[j][1] += s0[j][0]
    offset_none(series, order)
