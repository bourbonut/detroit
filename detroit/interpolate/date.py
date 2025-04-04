from collections.abc import Callable
from datetime import datetime


def interpolate_date(a: datetime, b: datetime) -> Callable[[float], datetime]:
    """
    Returns an interpolator between the two dates a and b.

    Parameters
    ----------
    a : datetime
        Date a
    b : datetime
        Date b

    Returns
    -------
    Callable[[float], datetime]
        Interpolator function

    Examples
    --------

    >>> from datetime import datetime
    >>> interpolator = d3.interpolate_date(datetime(2000, 1, 1), datetime(2000, 1, 2))
    >>> interpolator(0)
    datetime.datetime(2000, 1, 1, 0, 0)
    >>> interpolator(1)
    datetime.datetime(2000, 1, 2, 0, 0)
    >>> interpolator(0.5)
    datetime.datetime(2000, 1, 1, 12, 0)
    """
    a, b = a.timestamp(), b.timestamp()

    def interpolate(t):
        d = datetime.fromtimestamp(a * (1 - t) + b * t)
        return d

    return interpolate
