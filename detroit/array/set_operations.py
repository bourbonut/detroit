from collections.abc import Hashable, Iterable
from functools import reduce
from operator import iand, ior


def union(*iterables: Iterable[Hashable]) -> set[Hashable]:
    """
    Returns a new set containing every distinct value that appears in any of
    the givven iterables.

    Parameters
    ----------
    iterables : Iterable[Hashable]
        Iterables

    Returns
    -------
    set[Hashable]
        Set of all united values from iterables

    Examples
    --------
    >>> d3.union([1, 2], [3, 4], [5])
    {1, 2, 3, 4, 5}
    """
    return reduce(ior, map(set, iterables))


def difference(
    iterable: Iterable[Hashable], *others: Iterable[Hashable]
) -> set[Hashable]:
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
    set[Hashable]
        Set of the iterable differenciated with other iterables

    Examples
    --------
    >>> d3.difference([1, 2, 3], [2, 5], [3])
    {1}
    """
    return set(iterable) - union(*others)


def intersection(*iterables: Iterable[Hashable]) -> set[Hashable]:
    """
    Returns a new set containing every distinct value that appears in all of
    the given iterables.

    Parameters
    ----------
    iterables : Iterable[Hashable]
        Iterables

    Returns
    -------
    set[Hashable]
        Set of all intersected iterables

    Examples
    --------
    >>> d3.intersection([1, 2, 3], [3, 4], [2, 3])
    {3}
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

    Examples
    --------
    >>> d3.superset([1, 2, 3], [1, 2])
    True
    >>> d3.superset([1, 2, 3], [4, 2])
    False
    """
    return not (bool(len(set(b) - set(a))))


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

    Examples
    --------
    >>> d3.subset([1, 2], [1, 2, 3])
    True
    >>> d3.subset([4, 2], [1, 2, 3])
    False
    """
    return not (bool(len(set(a) - set(b))))


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

    Examples
    --------
    >>> d3.disjoint([1, 3], [2, 4])
    True
    >>> d3.disjoint([1, 3], [3, 4])
    False
    """
    return not (bool(len(set(a) & set(b))))
