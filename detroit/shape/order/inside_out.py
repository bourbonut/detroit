from ...types import T
from ..series import Series
from .appearance import order_appearance
from .ascending import _sum


def order_inside_out(series: list[Series[T]]) -> list[int]:
    """
    Returns a series order such that the earliest series (according to the
    maximum value) are on the inside and the later series are on the outside.
    This order is recommended for streamgraphs in conjunction with
    :func:`d3.stack_offset_wiggle <stack_offset_wiggle>`.

    Parameters
    ----------
    series : list[Series[T]]
        List of series

    Returns
    -------
    list[int]
        List of ordered indices
    """
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
