from ..series import Series


def order_none(series: list[Series]) -> list[int]:
    """
    Default order function which generates a list of indices representing stack
    order.

    Parameters
    ----------
    series : list[Series]
        List of series

    Returns
    -------
    list[int]
        Order list
    """
    return list(range(len(series)))
