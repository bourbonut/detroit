from ...types import T
from ..series import Series


def order_none(series: list[Series[T]]) -> list[int]:
    """
    Returns the given series order :math:`[0, 1, ..., n - 1]` where :math:`n`
    is the number of elements in series. Thus the stack is given by the key
    accessor.

    Parameters
    ----------
    series : list[Series[T]]
        List of series

    Returns
    -------
    list[int]
        List of ordered indices
    """
    return list(range(len(series)))
