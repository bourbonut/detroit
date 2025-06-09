from ..series import Series

def order_reverse(series: list[Series]) -> list[int]:
    """
    Returns the reverse order of a given list of series.

    Parameters
    ----------
    series : list[Series]
        List of series

    Returns
    -------
    list[int]
        Order list
    """
    return list(reversed(range(len(series))))
