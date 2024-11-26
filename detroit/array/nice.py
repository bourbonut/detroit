import math
from typing import TypeVar

from .ticks import tick_increment

T = TypeVar("T")


def nice(start: T, stop: T, count: int) -> tuple[T, T]:
    """
    Returns a new interval :code:`[nice_start, nice_stop]` covering
    the given interval :code:`[start, stop]` and where :code:`nice_start` and
    :code:`nice_stop` are guaranteed to align with the corresponding
    :code:`tick_step`.

    Parameters
    ----------
    start : T
        Start value
    stop : T
        End value
    count : int
        Count value

    Returns
    -------
    tuple[T, T]
        Aligned interval
    """
    prestep = None
    while True:
        step = tick_increment(start, stop, count)
        if step == prestep or step == 0 or not math.isfinite(step):
            return [start, stop]
        elif step > 0:
            start = math.floor(start / step) * step
            stop = math.ceil(stop / step) * step
        elif step < 0:
            start = math.ceil(start * step) / step
            stop = math.floor(stop * step) / step
        prestep = step
