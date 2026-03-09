from collections.abc import Callable
from typing import TypeAlias, TypeVar

from .argpass import argpass

T = TypeVar("T")
V = TypeVar("V")
K = TypeVar("K")
R = TypeVar("R")

Index: TypeAlias = int

NestedAccessor: TypeAlias = (
    Callable[[T], K] | Callable[[T, Index], K] | Callable[[T, Index, list[T]], K]
)


def nest(
    values: list[T],
    map_function: Callable[[dict[K, V]], R],
    reduce_function: Callable[[list[T]], V],
    keys: tuple[NestedAccessor, ...],
) -> R:
    if len(keys) == 0:
        raise ValueError("At least one key must be declared.")

    def regroup(values, i):
        if i >= len(keys):
            return reduce_function(values)
        groups = {}
        keyof = argpass(keys[i])
        i += 1
        index = -1
        for value in values:
            index += 1
            key = keyof(value, index, values)
            if group := groups.get(key):
                group.append(value)
            else:
                groups[key] = [value]
        for key, values in groups.items():
            groups[key] = regroup(values, i)
        return map_function(groups)

    return regroup(values, 0)


def identity(x: T) -> T:
    return x


def unique(values: list[T]) -> T:
    if len(values) != 1:
        raise IndexError("Duplicate key")
    return values[0]


def array_from(groups: dict[K, V]) -> list[tuple[K, V]]:
    return list(groups.items())


def index(
    values: list[T],
    *keys: NestedAccessor,
) -> dict[K, T]:
    """
    Groups and reduces the specified list of values into a nested dictionary.
    The reducer extracts the first element from each group.

    Parameters
    ----------
    values : list[T]
        List of values
    keys : Callable[[T], K] | Callable[[T, Index], K] | Callable[[T, Index, list[T]], K]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    dict[K, T]
        Nested dictionary.

    Examples
    --------

    >>> data = [
    ...     {"id": 0, "value": 10},
    ...     {"id": 0, "value": 20},
    ...     {"id": 1, "value": 3},
    ... ]
    >>> d3.index(data, lambda d: d["value"])
    {10: {'id': 0, 'value': 10}, 20: {'id': 0, 'value': 20}, 3: {'id': 1, 'value': 3}}
    """
    return nest(values, identity, unique, keys)


def indexes(
    values: list[T],
    *keys: NestedAccessor,
) -> list[tuple[K, T]]:
    """
    Equivalent to :func:`d3.index <index>`, returns a list of collections [key, array of
    values]. The reducer extracts the first element from each group.

    Parameters
    ----------
    values : list[U]
        List of values
    *keys : Callable[[T], K] | Callable[[T, Index], K] | Callable[[T, Index, list[T]], K]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    list[tuple[K, T]]
        Nested list of collections [key; array of values].

    Examples
    --------

    >>> data = [
    ...     {"id": 0, "value": 10},
    ...     {"id": 0, "value": 20},
    ...     {"id": 1, "value": 3},
    ... ]
    >>> d3.indexes(data, lambda d: d["value"])
    [(10, {'id': 0, 'value': 10}), (20, {'id': 0, 'value': 20}), (3, {'id': 1, 'value': 3})]
    """
    return nest(values, array_from, unique, keys)


def group(
    values: list[T],
    *keys: NestedAccessor,
) -> dict[K, list[T]]:
    """
    Groups the specified list of values into a nested dictionary given keys.

    Parameters
    ----------
    values : list[U]
        List of values
    *keys : Callable[[T], K] | Callable[[T, Index], K] | Callable[[T, Index, list[T]], K]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    dict[K, list[T]]
        Nested dictionary

    Examples
    --------

    >>> data = [
    ...     {"id": 0, "value": 10},
    ...     {"id": 0, "value": 20},
    ...     {"id": 1, "value": 3},
    ... ]
    >>> d3.group(data, lambda d: d["id"])
    {0: [{'id': 0, 'value': 10}, {'id': 0, 'value': 20}], 1: [{'id': 1, 'value': 3}]}
    """
    return nest(values, identity, identity, keys)


def groups(
    values: list[T],
    *keys: NestedAccessor,
) -> list[tuple[K, list[T]]]:
    """
    Equivalent to :func:`d3.group <group>`, returns a list of collections [key; array of
    values].

    Parameters
    ----------
    values : list[U]
        List of values
    *keys : Callable[[T], K] | Callable[[T, Index], K] | Callable[[T, Index, list[T]], K]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    list[tuple[K, list[T]]]
        Nested list of collections [key; array of values].

    Examples
    --------

    >>> data = [
    ...     {"id": 0, "value": 10},
    ...     {"id": 0, "value": 20},
    ...     {"id": 1, "value": 3},
    ... ]
    >>> d3.groups(data, lambda d: d["id"])
    [(0, [{'id': 0, 'value': 10}, {'id': 0, 'value': 20}]), (1, [{'id': 1, 'value': 3}])]
    """
    return nest(values, array_from, identity, keys)


def rollup(
    values: list[T],
    reduce_function: Callable[[list[T]], R],
    *keys: NestedAccessor,
) -> dict[K, R]:
    """
    Groups and reduces the specified list of values into a nested dictionary.

    Parameters
    ----------
    values : list[T]
        List of values
    reduce_function : Callable[[list[T]], V]
        Reducer function
    *keys : Callable[[T, int, list[T]], U]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    dict[K, R]
        Nested dictionary

    Examples
    --------

    >>> data = [
    ...     {"id": 0, "value": 10},
    ...     {"id": 0, "value": 20},
    ...     {"id": 1, "value": 3},
    ... ]
    >>> d3.rollup(
    ...     data,
    ...     lambda values: sum([d["value"] for d in values]),
    ...     lambda d: d["id"],
    ... )
    {0: 30, 1: 3}
    """
    return nest(values, identity, reduce_function, keys)


def rollups(
    values: list[T],
    reduce_function: Callable[[list[T]], R],
    *keys: NestedAccessor,
) -> list[tuple[K, R]]:
    """
    Equivalent to `d3.rollup`, returns a list of collections [key; array of
    values].

    Parameters
    ----------
    values : list[T]
        List of values
    reduce_function : Callable[[list[T]], V]
        Reducer function
    *keys : Callable[[T, int, list[T]], U]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    list[tuple[K, R]]
        Nested list of collections [key; array of values].

    Examples
    --------

    >>> data = [
    ...     {"id": 0, "value": 10},
    ...     {"id": 0, "value": 20},
    ...     {"id": 1, "value": 3},
    ... ]
    >>> d3.rollups(
    ...     data,
    ...     lambda values: sum([d["value"] for d in values]),
    ...     lambda d: d["id"],
    ... )
    [(0, 30), (1, 3)]
    """
    return nest(values, array_from, reduce_function, keys)
