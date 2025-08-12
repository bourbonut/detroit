from math import isnan

from ...types import T
from ..series import Series
from .none import offset_none


def offset_expand(series: list[Series[T]], order: list[int]):
    """
    Applies a zero baseline and normalizes the values for each point such that
    the topline is always one.

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
    m = len(series[0])
    for j in range(m):
        y = 0
        for i in range(n):
            x = series[i][j][1]
            y += 0.0 if isnan(x) else x
        if y:
            for i in range(n):
                series[i][j][1] /= y
    offset_none(series, order)
