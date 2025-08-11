from .none import order_none
from math import inf
from ..series import Series

def order_appearance(series: list[Series]) -> list[int]:
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
