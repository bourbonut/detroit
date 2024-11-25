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
        Interpolator
    """
    a, b = a.timestamp(), b.timestamp()

    def interpolate(t):
        d = datetime.fromtimestamp(a * (1 - t) + b * t)
        return d

    return interpolate
