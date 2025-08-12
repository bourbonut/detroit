from ...types import T
from ..series import Series
from .ascending import order_ascending


def order_descending(series: list[Series[T]]) -> list[int]:
    """
    Returns a series order such that the largest series (according to the sum
    of values) is at the bottom.

    Parameters
    ----------
    series : list[Series[T]]
        List of series

    Returns
    -------
    list[int]
        List of ordered indices
    """
    return order_ascending(series)[::-1]
