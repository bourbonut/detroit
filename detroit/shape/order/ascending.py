from .none import order_none
from ..series import Series
from math import isnan

def order_ascending(series):
    sums = list(map(_sum, series))
    return sorted(order_none(series), key=lambda i: sums[i])

def _sum(series: list[Series]) -> float:
    s = 0
    for i in range(len(series)):
        v = float(series[i][1])
        if not isnan(v):
            s += v
    return s
