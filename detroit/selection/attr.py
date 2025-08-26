from lxml import etree

from ..array import argpass
from ..types import Accessor, EtreeFunction, Number, T


def attr_constant(name: str, value: str) -> EtreeFunction[T, None]:
    """
    Returns a function which adds an attribute to nodes given a constant value.

    Parameters
    ----------
    name : str
        Attribute name
    value : str
        Constant value of the attribute

    Returns
    -------
    EtreeFunction[T, None]
        Function which adds an attribute to nodes
    """

    def callback(node: etree.Element, data: T, i: int, group: list[etree.Element]):
        node.set(name, str(value))

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
        node.set(name, str(value(data, i, group)))

    return callback
