import math
from typing import Any


def threshold_sturges(values: list[float | None], *args: Any) -> int:
    """
    Returns the number of bins according to Sturges' formula; the input values
    must be numbers.

    Parameters
    ----------
    values : list[float | None]
        Input values
    *args: Any
        Unused arguments

    Returns
    -------
    int
       Number of bins according to Sturges' formula
    """
    values = [v for v in values if v is not None]
    if len(values) == 0:
        return 1
    return max(1, math.ceil(math.log(len(values)) / math.log(2)) + 1)
