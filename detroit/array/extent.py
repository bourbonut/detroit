import math
from collections.abc import Iterable
from datetime import datetime
from itertools import starmap

from ..types import Accessor, T
from .argpass import argpass


def extent(values: Iterable[T], accessor: Accessor[T, T] | None = None) -> tuple[T, T]:
    """
    Returns the minimum and maximum value in
    the given iterable using natural order.

    Parameters
    ----------
    values : Iterable[T]
        Iterator
    accessor : Accessor[T, T] | None
        Accessor function

    Returns
    -------
    tuple[T, T]
        Minimum, maximum

    Examples
    --------

    >>> a = [1, 4, -2, 8]
    >>> d3.extent(a)
    [-2, 8]
    >>> b = [{"a": 8}, {"a": 1}, {"a": 16}]
    >>> d3.extent(b, lambda x: x["a"])
    [1, 16]

    Notes
    -----

    The accessor function can take one, two or three arguments where :

    * the first one is the value over iteration
    * the second one is its index
    * the last one is the input :code:`values` without any modification
    """

    def is_valid(value):
        """Check if the value is valid"""
        return value is not None and (
            isinstance(value, (str, datetime)) or not math.isnan(value)
        )

    if accessor is not None:
        accessor = argpass(accessor)

        def access(index, value):
            """Access value given the accessor function"""
            return accessor(value, index, values)

        values = list(filter(is_valid, starmap(access, enumerate(values))))
    else:
        values = list(filter(is_valid, values))

    return [min(values) if values else None, max(values) if values else None]
