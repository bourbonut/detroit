from .appearance import order_appearance
from .ascending import _sum
from ..series import Series


def order_inside_out(series: list[Series]) -> list[int]:
    n = len(series)
    sums = list(map(_sum, series))
    order = order_appearance(series)
    top = 0
    bottom = 0
    tops = []
    bottoms = []

    for i in range(n):
        j = order[i]
        if top < bottom:
            top += sums[j]
            tops.append(j)
        else:
            bottom += sums[j]
            bottoms.append(j)

    return bottoms[::-1] + tops
