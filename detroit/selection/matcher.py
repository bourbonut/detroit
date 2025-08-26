from collections.abc import Callable

from ..array import argpass
from ..types import Accessor, T


def matcher(match: Accessor[T, bool] | int | float | str) -> Callable[[T], bool]:
    """
    Returns a function whichs checks if the data input matches a arbitrary condition.

    Parameters
    ----------
    match : Accessor[T, bool] | int | float | str
        Match function or constant that data input should match.

    Returns
    -------
    Callable[[T], bool]
        Matching function
    """
    if callable(match):
        return argpass(match)

    def match_func(d: T) -> bool:
        return d == match

    return argpass(match_func)
