from copy import deepcopy, copy
from typing import Generic

from lxml import etree

from ..types import T


class EnterNode(Generic[T]):
    """
    Enter node which holds parent element, a datum and next element in some
    specific cases.

    Parameters
    ----------
    parent : etree.Element
        Parent node
    datum : T
        Data to hold
    """

    def __init__(self, parent: etree.Element, datum: T):
        self._next = None
        self._parent = parent
        self.__data__ = datum

    def __str__(self):
        if self._parent is None:
            return f"EnterNode({self._parent}, {self.__data__})"
        tag = self._parent.tag
        class_name = self._parent.attrib.get("class")
        if class_name:
            return f"EnterNode({tag}.{class_name}, {self.__data__})"
        return f"EnterNode({tag}, {self.__data__})"

    def clone(self, deep: bool = False):
        copy_func = deepcopy if deep else copy
        node = EnterNode(
            copy_func(self._parent),
            copy_func(self.__data__),
        )
        node._next = copy_func(self._next)
        return node

    def __repr__(self):
        return str(self)
