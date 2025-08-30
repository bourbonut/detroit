from collections.abc import Callable
from typing import Any, Generic, TypeVar

from ..array import argpass
from ..types import T, U, V
from .constant import constant
from .offset import offset_none
from .order import order_none
from .series import Serie, Series

TStack = TypeVar("Stack", bound="Stack")


def stack_value(d: U, key: V) -> T:
    """
    Default stack value function for `Stack` class

    Parameters
    ----------
    d : U
        Data
    key : V
        Series key to access specific element of the data

    Returns
    -------
    T
        Element accessed in the data
    """
    return d[key]


def stack_series(key: T) -> Series:
    """
    Default function to make a stack series

    Parameters
    ----------
    key : T
        Key of the series

    Returns
    -------
    Series
        New series with the associated key
    """
    series = Series()
    series.key = key
    return series


class Stack(Generic[T]):
    """
    Builds a new stack generator with the default settings.
    """

    def __init__(self):
        self._keys = argpass(constant([]))
        self._order = order_none
        self._offset = offset_none
        self._value = argpass(stack_value)

    def __call__(self, data: list[T], *args: Any) -> list[Series]:
        """
        Generates a stack for the given array of data and returns an array
        representing each series.

        Parameters
        ----------
        data : list[T]
            List of data
        *args : Any
            Additional arguments passed to :code:`keys` method.

        Returns
        -------
        list[Series]
            List of series
        """
        args = [data] + list(args)
        sz: list[Series] = list(map(stack_series, self._keys(*args)))
        n = len(sz)
        j = -1

        for d in data:
            j += 1
            for i in range(n):
                series = sz[i]
                series.append(Serie([0, self._value(d, series.key, j, data)], d))

        oz = list(self._order(sz))
        for i in range(n):
            sz[oz[i]].index = i

        self._offset(sz, oz)
        return sz

    def set_keys(self, keys: Callable[[...], list[str]] | list[str]) -> TStack:
        """
        Sets the :code:`keys` method and returns itself.

        Parameters
        ----------
        keys : Callable[[...], str] | list[str]
            List of keys or function which returns a list of keys

        Returns
        -------
        TStack
            Itself

        Notes
        -----
        The arguments of the function are the same as the additional arguments
        of :code:`Stack.__call__` method.
        """
        if callable(keys):
            self._keys = keys
        else:
            self._keys = constant(list(keys))
        self._keys = argpass(self._keys)
        return self

    def set_value(
        self, value: Callable[[T, str, int, list[T]], float] | float
    ) -> TStack:
        """
        Sets the :code:`value` method and returns itself.

        Parameters
        ----------
        value : Callable[[T, str, int, list[T]], float] | float
            Value number or function which takes the optional argument: data,
            key, index, list of data. The function must returns a float value.

        Returns
        -------
        TStack
            Itself

        Notes
        -----
        You can pass a function with only the data and key arguments for example.
        """
        if callable(value):
            self._value = value
        else:
            self._value = constant(float(value))
        self._value = argpass(self._value)
        return self

    def set_order(
        self, order: Callable[[list[Series]], list[int]] | list[int] | None = None
    ) -> TStack:
        """
        Sets the :code:`order` method and returns itself.

        Parameters
        ----------
        order : Callable[[list[Series]], list[int]] | list[int] | None
            If none value, resets the method. List of indices or function which
            takes in argument a list of series and returns the order list.

        Returns
        -------
        TStack
            Itself
        """
        if order is None:
            self._order = order_none
        elif callable(order):
            self._order = order
        else:
            self._order = constant(list(order))
        return self

    def set_offset(
        self, offset: Callable[[list[Series], list[int]], None] | None = None
    ) -> TStack:
        """
        Sets the :code:`offset` and returns itself.

        Parameters
        ----------
        offset : Callable[[list[Series], list[int]], None] | None
            If none value, resets the method. Function which takes in arguments
            a list of series and the order list and updates lower and upper
            values int the series list.

        Returns
        -------
        TStack
            Itself
        """
        if offset is None:
            self._offset = offset_none
        else:
            self._offset = offset
        return self

    def get_keys(self) -> Callable[[...], str]:
        return self._keys

    def get_value(self) -> Callable[[T, str, int, list[T]], float]:
        return self._value

    def get_order(self) -> Callable[[list[Series]], list[int]]:
        return self._order

    def get_offset(self) -> Callable[[list[Series], list[int]], None]:
        return self._offset
