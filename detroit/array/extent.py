import math
from collections.abc import Callable, Iterable
from inspect import signature
from typing import TypeVar

T = TypeVar("T")


# TODO : use min and max instead of doing manually
def extent(
    values: Iterable[T], accessor: Callable[[T, int, Iterable[T]], T] | None = None
) -> tuple[T, T]:
    """
    Returns the minimum and maximum value in
    the given iterable using natural order.

    Parameters
    ----------
    values : Iterable[T]
        Iterator
    accessor : Callable[[T, int, Iterable[T]], T] | None
        Accessor function

    Returns
    -------
    tuple[T, T]
        Minimum, maximum
    """
    mini = None
    maxi = None
    if accessor is None:
        for value in values:
            if value is not None and (isinstance(value, str) or not math.isnan(value)):
                if mini is None:
                    mini = maxi = value
                else:
                    if mini > value:
                        mini = value
                    if maxi < value:
                        maxi = value
    else:
        nargs = len(signature(accessor).parameters)
        for index, value in enumerate(values):
            args = [value, index, values][:nargs]
            new_value = accessor(*args)
            if new_value is not None and (
                isinstance(new_value, str) or not math.isnan(new_value)
            ):
                value = new_value
                if mini is None:
                    mini = maxi = value
                else:
                    if mini > value:
                        mini = value
                    if maxi < value:
                        maxi = value
    return [mini, maxi]  # TODO: remove brackets and fix tests
