from ...types import T
from ..series import Series


def order_reverse(series: list[Series[T]]) -> list[int]:
    """
    Returns the reverse of the given series order :math:`[n - 1, n - 2, ...,
    0]` where :math:`n` is the number of elements in series. Thus, the stack
    order is given by the reverse of the key accessor.


    Parameters
    ----------
    series : list[Series[T]]
        List of series

    Returns
    -------
    list[int]
        Order list
    """
    return list(reversed(range(len(series))))
