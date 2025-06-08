from .none import offset_none
from ..series import Series

def offset_expand(series: list[Series], order: list[int]):
    if len(series) == 0:
        return
    j = 0
    n = len(series)
    m = len(series[0])
    for j in range(m):
        y = 0
        for i in range(n):
            y += series[i][j][1] or 0
        if y:
            for i in range(n):
                series[i][j][1] /= y
    offset_none(series, order)
