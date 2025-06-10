from inspect import signature
from collections.abc import Callable
from ..types import T

def nest(
    values: list[T],
    map_function: Callable[[dict], list],
    reduce_function: Callable[[list[T]], dict],
    keys: list[Callable[[T, int, list[T]], str]]
):
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
    values: list[T],
    *keys: list[Callable[[T, int, list[T]], str]],
) -> dict:
    return nest(values, identity, unique, keys)

def indexes(
    values: list[T],
    *keys: list[Callable[[T, int, list[T]], str]],
) -> dict:
    return nest(values, array_from, unique, keys)

def group(
    values: list[T],
    *keys: list[Callable[[T, int, list[T]], str]],
) -> dict:
    return nest(values, identity, identity, keys)

def groups(
    values: list[T],
    *keys: list[Callable[[T, int, list[T]], str]],
) -> dict:
    return nest(values, array_from, identity, keys)

def rollup(
    values: list[T],
    reduce_function: Callable[[list[T]], dict],
    *keys: list[Callable[[T, int, list[T]], str]],
) -> dict:
    return nest(values, identity, reduce_function, keys)

def rollups(
    values: list[T],
    reduce_function: Callable[[list[T]], dict],
    *keys: list[Callable[[T, int, list[T]], str]],
) -> dict:
    return nest(values, array_from, reduce_function, keys)
