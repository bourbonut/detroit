import math
from statistics import stdev


def threshold_scott(values: list[float | None], mini: float, maxi: float) -> int:
    """
    Returns the number of bins according to Scott's normal reference rule; the
    input values must be numbers.

    Parameters
    ----------
    values : list[float | None]
        Input values
    mini : float
        Minimum value
    maxi : float
        Maximum value

    Returns
    -------
    int
       Number of bins according to Scott's normal
    """
    values = [v for v in values if v is not None]
    c = len(values)
    if len(values) <= 1:
        d = 0
    else:
        d = stdev(values)
    return math.ceil((maxi - mini) * (c ** (1 / 3)) / (3.49 * d)) if c and d else 1
