from .none import offset_none
from math import isnan

def offset_silhouette(series, order):
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
