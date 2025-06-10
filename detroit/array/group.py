from inspect import signature
from collections.abc import Callable
from ..types import T, U, V

def nest(
    values: list[U],
    map_function: Callable[[dict], list],
    reduce_function: Callable[[list[U]], dict],
    keys: list[Callable[[U, int, list[U]], V]]
) -> list:
    if len(keys) == 0:
        raise ValueError("At least one key must be declared.")
    def regroup(values, i):
        if i >= len(keys):
            return reduce_function(values)
        groups = {}
        keyof = keys[i]
        i += 1
        index = -1
        for value in values:
            index += 1
            nargs = len(signature(keyof).parameters)
            args = [value, index, values][:nargs]
            key = keyof(*args)
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
    *keys: list[Callable[[U, int, list[U]], V]],
) -> dict:
    """
    Groups and reduces the specified list of values into a nested dictionary.
    The reducer extracts the first element from each group.

    Parameters
    ----------
    values : list[U]
        List of values
    keys : list[Callable[[U, int, list[U]], V]]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    dict
        Nested dictionary.
    """
    return nest(values, identity, unique, keys)

def indexes(
    values: list[U],
    *keys: list[Callable[[U, int, list[U]], V]],
) -> list:
    """
    Equivalent to `d3.index`, returns a list of collections [key, array of
    values]. The reducer extracts the first element from each group.

    Parameters
    ----------
    values : list[U]
        List of values
    keys : list[Callable[[U, int, list[U]], V]]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    list
        Nested list of collections [key; array of values].
    """
    return nest(values, array_from, unique, keys)

def group(
    values: list[U],
    *keys: list[Callable[[U, int, list[U]], V]],
) -> dict:
    """
    Groups the specified list of values into a nested dictionary given keys.

    Parameters
    ----------
    values : list[U]
        List of values
    keys : list[Callable[[U, int, list[U]], V]]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    dict
        Nested dictionary
    """
    return nest(values, identity, identity, keys)

def groups(
    values: list[U],
    *keys: list[Callable[[U, int, list[U]], V]],
) -> list:
    """
    Equivalent to `d3.group`, returns a list of collections [key; array of
    values].

    Parameters
    ----------
    values : list[U]
        List of values
    keys : list[Callable[[U, int, list[U]], V]]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    list
        Nested list of collections [key; array of values].
    """
    return nest(values, array_from, identity, keys)

def rollup(
    values: list[U],
    reduce_function: Callable[[list[U]], dict],
    *keys: list[Callable[[U, int, list[U]], V]],
) -> dict:
    """
    Groups and reduces the specified list of values into a nested dictionary.

    Parameters
    ----------
    values : list[U]
        List of values
    reduce_function : Callable[[list[U]], dict]
        Reducer function
    keys : list[Callable[[U, int, list[U]], V]]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    dict
        Nested dictionary
    """
    return nest(values, identity, reduce_function, keys)

def rollups(
    values: list[U],
    reduce_function: Callable[[list[U]], dict],
    *keys: list[Callable[[U, int, list[U]], V]],
) -> list:
    """
    Equivalent to `d3.rollup`, returns a list of collections [key; array of
    values].

    Parameters
    ----------
    values : list[U]
        List of values
    reduce_function : Callable[[list[U]], dict]
        Reducer function
    keys : list[Callable[[U, int, list[U]], V]]
        List of functions which take in arguments data, index and list of data
        and returns the key value of the data.

    Returns
    -------
    list
        Nested list of collections [key; array of values].
    """
    return nest(values, array_from, reduce_function, keys)
