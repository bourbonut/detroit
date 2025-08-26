from lxml import etree

from ..array import argpass
from ..types import Accessor, EtreeFunction, T


def text_constant(value: str) -> EtreeFunction[T, None]:
    """
    Returns a function which adds text value to nodes given a constant
    value.

    Parameters
    ----------
    value : str
        Constant text value

    Returns
    -------
    EtreeFunction[T, None]
        Function which adds a text value to nodes
    """

    def callback(node: etree.Element, data: T, i: int, group: list[etree.Element]):
        node.text = value

    return callback


def text_function(value: Accessor[T, str]) -> EtreeFunction[T, None]:
    """
    Returns a function which adds text value to nodes given a constant
    value.

    Parameters
    ----------
    value : Accessor[T, str]
        Accessor function

    Returns
    -------
    EtreeFunction[T, None]
        Function which adds a text value to nodes
    """
    value = argpass(value)

    def callback(node: etree.Element, data: T, i: int, group: list[etree.Element]):
        node.text = value(data, i, group)

    return callback
