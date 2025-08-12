from math import isnan

from ...types import T
from ..series import Series
from .none import offset_none


def offset_wiggle(series: list[Series[T]], order: list[int]):
    """
    Shifts the baseline so as to minimize the weighted wiggle of layers. This
    offset is recommended for streamgraphs in conjunction with
    :func:`d3.stack_order_inside_out <stack_order_inside_out>`.

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
    if m == 0:
        return
    y = 0
    for j in range(1, m):
        s1 = 0
        s2 = 0
        for i in range(n):
            si = series[order[i]]
            x1 = si[j][1]
            x2 = si[j - 1][1]
            sij0 = 0.0 if isnan(x1) else x1
            sij1 = 0.0 if isnan(x2) else x2
            s3 = (sij0 - sij1) / 2
            for k in range(i):
                sk = series[order[k]]
                x1 = sk[j][1]
                x2 = sk[j - 1][1]
                skj0 = 0.0 if isnan(x1) else x1
                skj1 = 0.0 if isnan(x2) else x2
                s3 += skj0 - skj1
            s1 += sij0
            s2 += s3 * sij0
        s0[j - 1][0] = y
        s0[j - 1][1] += s0[j - 1][0]
        if s1 and not isnan(s1):
            y -= s2 / s1
    s0[j][0] = y
    s0[j][1] += s0[j][0]
    offset_none(series, order)
