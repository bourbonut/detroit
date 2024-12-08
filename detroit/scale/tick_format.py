import math
from collections.abc import Callable
from typing import TypeVar

from ..array import tick_step
from ..format import (
    format_prefix,
    format_specifier,
    locale_format,
    precision_fixed,
    precision_prefix,
    precision_round,
)

T = TypeVar("T")


def tick_format(
    start: T, stop: T, count: int, specifier: str | None = None
) -> Callable[[T], str]:
    """
    Returns a number format function suitable for displaying a tick value,
    automatically computing the appropriate precision based on the fixed
    interval between tick values, as determined by d3.tickStep.

    Parameters
    ----------
    start : T
        Start value
    stop : T
        Stop value
    count : int
        Count value
    specifier : str | None
        Specifier allows a custom format where the precision of the format
        is automatically set by the scale as appropriate for the tick interval.
    """
    step = tick_step(start, stop, count)
    precision = None
    specifier = format_specifier(specifier if specifier is not None else ",f")

    if specifier.type == "s":
        value = max(abs(start), abs(stop))
        if specifier.precision is None and not math.isnan(
            precision := precision_prefix(step, value)
        ):
            specifier.precision = precision
        return format_prefix(specifier, value)
    elif specifier.type in ("", "e", "g", "p", "r"):
        if specifier.precision is None and not math.isnan(
            precision := precision_round(step, max(abs(start), abs(stop)))
        ):
            specifier.precision = precision - (specifier.type == "e")
    elif specifier.type in ("f", "%"):
        if specifier.precision is None and not math.isnan(
            precision := precision_fixed(step)
        ):
            specifier.precision = precision - (specifier.type == "%") * 2

    return locale_format(specifier)
