from collections.abc import Callable
from datetime import datetime
from math import isnan

from ..types import GenValue, T


def is_null(x: float | None) -> bool:
    """
    Returns if the input value is :code:`None` or :code:`math.nan`.

    Parameters
    ----------
    x : float | None
        Input value to check

    Returns
    -------
    bool
        If value is :code:`None` or :code:`math.nan`.
    """
    return x is None or isnan(x)


def as_float(x: GenValue) -> float:
    """
    Converts the input into :code:`float` type.

    Parameters
    ----------
    x : datetime | str | int | float
        Input to be converted

    Returns
    -------
    float
        Input converted into :code:`float`
    """
    if isinstance(x, datetime):
        return x.timestamp()
    else:
        return float(x)


def constant(x: T) -> Callable[..., T]:
    """
    Takes a value :code:`x` and returns a function which takes any argument
    and gives the value :code:`x`.

    Parameters
    ----------
    x : T
        Value to be returned by the constant function

    Returns
    -------
    Callable[..., T]
        Function which takes any argument and returns the :code:`x` value
    """

    def f(*args):
        return x

    return f


def identity(x: T) -> T:
    """
    Returns the input without any modification.

    Parameters
    ----------
    x : T
        Input

    Returns
    -------
    T
        Same value as input
    """
    return x
