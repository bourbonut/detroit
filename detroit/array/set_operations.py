from collections.abc import Iterable, Hashable
from functools import reduce
from operator import iand, ior
from ..types import T

def union(*iterables: Iterable[Hashable]) -> set[T]:
    """
    Returns a new set containing every distinct value that appears in any of
    the givven iterables.

    Parameters
    ----------
    iterables : Iterable[Hashable]
        Iterables

    Returns
    -------
    set[T]
        Set of all united values from iterables
    """
    return reduce(ior, map(set, iterables))

def difference(iterable: Iterable[Hashable], *others: Iterable[Hashable]) -> set[T]:
    """
    Returns a new set containing every value of iterable that is not in any of
    the other iterables.

    Parameters
    ----------
    iterable : Iterable[Hashable]
        Iterable to differenciate
    others : Iterable[Hashable]
        Other iterables

    Returns
    -------
    set[T]
        Set of the iterable differenciated with other iterables
    """
    return set(iterable) - union(*others)

def intersection(*iterables: Iterable[Hashable]) -> set[T]:
    """
    Returns a new set containing every distinct value that appears in all of
    the given iterables.

    Parameters
    ----------
    iterables : Iterable[Hashable]
        Iterables

    Returns
    -------
    set[T]
        Set of all intersected iterables
    """
    return reduce(iand, map(set, iterables))

def superset(a: Iterable[Hashable], b: Iterable[Hashable]) -> bool:
    """
    Returns True if every value in the given iterable b is also in the given
    iterable a.

    Parameters
    ----------
    a : Iterable[Hashable]
        Iterable a
    b : Iterable[Hashable]
        Iterable b

    Returns
    -------
    bool
        True if a is a superset of b
    """
    return not(bool(len(set(b) - set(a))))

def subset(a: Iterable[Hashable], b: Iterable[Hashable]) -> bool:
    """
    Returns True if every value in the given iterable a is also in the given
    iterable b.

    Parameters
    ----------
    a : Iterable[Hashable]
        Iterable a
    b : Iterable[Hashable]
        Iterable b

    Returns
    -------
    bool
        True if a is a subset of b
    """
    return not(bool(len(set(a) - set(b))))

def disjoint(a: Iterable[Hashable], b: Iterable[Hashable]) -> bool:
    """
    Returns True if a and b contain no shared value

    Parameters
    ----------
    a : Iterable[Hashable]
        Iterable a
    b : Iterable[Hashable]
        Iterable b

    Returns
    -------
    bool
        True if a and b are disjoint
    """
    return not(bool(len(set(a) & set(b))))
