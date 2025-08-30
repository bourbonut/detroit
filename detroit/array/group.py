from collections.abc import Callable

from ..types import T, U, V
from .argpass import argpass


def nest(
    values: list[U],
    map_function: Callable[[dict], list],
    reduce_function: Callable[[list[U]], dict],
    keys: list[Callable[[U, int, list[U]], V]],
) -> list:
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


def array_from(groups: dict) -> list:
    return list(groups.items())


def index(
    values: list[U],
    *keys: Callable[[U, int, list[U]], V],
) -> dict[V, U]:
    """
    Groups and reduces the specified list of values into a nested dictionary.
    The reducer extracts the first element from each group.

    Parameters
    ----------
    values : list[U]
        List of values
    keys : Callable[[U, int, list[U]], V]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    dict[V, U]
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
    values: list[U],
    *keys: Callable[[U, int, list[U]], V],
) -> list[tuple[V, U]]:
    """
    Equivalent to :func:`d3.index <index>`, returns a list of collections [key, array of
    values]. The reducer extracts the first element from each group.

    Parameters
    ----------
    values : list[U]
        List of values
    *keys : Callable[[U, int, list[U]], V]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    list[tuple[V, U]]
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
    values: list[U],
    *keys: Callable[[U, int, list[U]], V],
) -> dict[V, list[U]]:
    """
    Groups the specified list of values into a nested dictionary given keys.

    Parameters
    ----------
    values : list[U]
        List of values
    *keys : Callable[[U, int, list[U]], V]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    dict[V, list[U]]
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
    values: list[U],
    *keys: Callable[[U, int, list[U]], V],
) -> list[tuple[V, list[U]]]:
    """
    Equivalent to :func:`d3.group <group>`, returns a list of collections [key; array of
    values].

    Parameters
    ----------
    values : list[U]
        List of values
    *keys : Callable[[U, int, list[U]], V]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    list[tuple[V, list[U]]]
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
    reduce_function: Callable[[list[T]], V],
    *keys: Callable[[T, int, list[T]], U],
) -> dict[U, V]:
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
    dict[U, V]
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
    reduce_function: Callable[[list[T]], V],
    *keys: Callable[[T, int, list[T]], U],
) -> list[tuple[U, V]]:
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
    list[tuple[U, V]]
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
