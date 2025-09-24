from lxml import etree
from typing import Any

from ..array import argpass
from ..types import Accessor, EtreeFunction, T


def text_constant(value: Any) -> EtreeFunction[T, None]:
    """
    Returns a function which adds text value to nodes given a constant
    value.

    Parameters
    ----------
    value : Any
        Constant text value

    Returns
    -------
    EtreeFunction[T, None]
        Function which adds a text value to nodes
    """
    value = str(value)

    def callback(node: etree.Element, data: T, i: int, group: list[etree.Element]):
        node.text = value

    return callback


def text_function(value: Accessor[T, Any]) -> EtreeFunction[T, None]:
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
        node.text = str(value(data, i, group))

    return callback
