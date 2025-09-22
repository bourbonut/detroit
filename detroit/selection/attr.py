from lxml import etree
from typing import Any

from ..array import argpass
from ..types import Accessor, EtreeFunction, Number, T


def tostring(value: list[Any] | Any) -> str:
    """
    If :code:`value` is a list of elements, the function converts elements
    strings, concatenate them into a single string and return it.
    If :code:`value` is a single element, the function converts it into a
    string.

    Parameters
    ----------
    value : list[Any] | Any
        Value to convert into string

    Returns
    -------
    str
        Output
    """
    return " ".join(map(str, value)) if isinstance(value, list) else str(value)


def attr_constant(name: str, value: list[Any] | Any) -> EtreeFunction[T, None]:
    """
    Returns a function which adds an attribute to nodes given a constant value.

    Parameters
    ----------
    name : str
        Attribute name
    value : list[Any] | Any
        Constant value of the attribute

    Returns
    -------
    EtreeFunction[T, None]
        Function which adds an attribute to nodes
    """
    value = tostring(value)

    def callback(node: etree.Element, data: T, i: int, group: list[etree.Element]):
        node.set(name, value)

    return callback


def attr_function(
    name: str, value: Accessor[T, str | Number]
) -> EtreeFunction[T, None]:
    """
    Returns a function which adds an attribute to nodes based on an accessor
    function.

    Parameters
    ----------
    name : str
        Attribute name
    value : Accessor[T, str | Number]
        Accessor function

    Returns
    -------
    EtreeFunction[T, None]
        Function which adds an attribute to nodes
    """
    value = argpass(value)

    def callback(node: etree.Element, data: T, i: int, group: list[etree.Element]):
        node.set(name, tostring(value(data, i, group)))

    return callback
