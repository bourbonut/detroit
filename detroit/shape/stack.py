from inspect import signature
from typing import Generic, TypeVar
from collections.abc import Callable
from .offset.none import offset_none
from .order.none import order_none
from .constant import constant
from .series import Series, Serie
from ..types import T, U, V

TStack = TypeVar("Stack", bound="Stack")

def stack_value(d: U, key: V) -> T:
    return d[key]

def stack_series(key: T) -> Series:
    series = Series()
    series.key = key
    return series

class Stack(Generic[T]):
    def __init__(self):
        self._keys = constant([])
        self._order = order_none
        self._offset = offset_none
        self._value = stack_value

    def __call__(self, data: list[T], *args) -> list[Series]:
        nargs = len(signature(self._keys).parameters)
        sz: list[Series] = list(map(stack_series, self._keys(*args[:nargs])))
        n = len(sz)
        j = -1

        nargs = len(signature(self._value).parameters)

        for d in data:
            j += 1
            for i in range(n):
                series = sz[i]
                args = [d, series.key, j, data]
                series.append(Serie([0, self._value(*args[:nargs])], d))

        oz = list(order_none(sz))
        for i in range(n):
            sz[oz[i]].index = i

        offset_none(sz, oz)
        return sz

    def set_keys(self, keys: Callable[[], str] | list[str]) -> TStack:
        if callable(keys):
            self._keys = keys
        else:
            self._keys = constant(list(keys))
        return self


    def set_value(self, value: Callable[[T, str, int, list[T]], float] | float) -> TStack:
        if callable(value):
            self._value = value
        else:
            self._value = constant(float(value))
        return self

    def set_order(self, order: Callable[[list[Series]], list[int]] | list[int] | None = None) -> TStack:
        if order is None:
            self._order = order_none
        elif callable(order):
            self._order = order
        else:
            self._order = constant(list(order))
        return self

    
    def set_offset(self, offset: Callable[[list[Series], list[int]], None] | None = None) -> TStack:
        if offset is None:
            self._offset = offset_none
        else:
            self._offset = offset
        return self
