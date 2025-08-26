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

    def __repr__(self):
        return str(self)

    # def append_child(self, child):
    #     return self._parent.insert_before(child, self._next)
    #
    # def insert_before(self, child, next):
    #     return self._parent.insert_before(child, next)
    #
    # def query_selector(self, selector):
    #     return self._parent.query_selector(selector)
    #
    # def query_selector_all(self, selector):
    #     return self._parent.query_selector_all(selector)
