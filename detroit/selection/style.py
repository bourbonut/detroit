from lxml import etree

from ..array import argpass
from ..types import Accessor, EtreeFunction, T


def style_constant(name: str, value: str) -> EtreeFunction[T, None]:
    """
    Returns a function which adds a style attribute to nodes given a constant
    value.

    Parameters
    ----------
    name : str
        Style name to add on nodes
    value : str
        Value of the style

    Returns
    -------
    EtreeFunction[T, None]
        Function which adds a style attribute to nodes
    """

    def callback(node: etree.Element, data: T, i: int, group: list[etree.Element]):
        current_value = node.get("style", "")
        node.set("style", f"{current_value}{name}:{value};")

    return callback


def style_function(name: str, value: Accessor[T, str]) -> EtreeFunction[T, None]:
    """
    Returns a function which adds a style attribute to nodes based on an
    accessor function.

    Parameters
    ----------
    name : str
        Style name to add on nodes
    value : Accessor[T, str]
        Accessor function

    Returns
    -------
    EtreeFunction[T, None]
        Function which adds a style attribute to nodes
    """
    value = argpass(value)

    def callback(node: etree.Element, data: T, i: int, group: list[etree.Element]):
        current_value = node.get("style", "")
        new_value = value(data, i, group)
        node.set("style", f"{current_value}{name}:{new_value};")

    return callback


def style_value(style: str, name: str) -> str:
    """
    Gets the style value in a style string value.

    Parameters
    ----------
    style : str
        Style string value
    name : str
        Name of the style

    Returns
    -------
    str
        Value of the style
    """
    if style.endswith(";"):
        style = style[:-1]
    attrs = {
        property: value
        for property, value in (desc.split(":") for desc in style.split(";"))
    }
    return attrs.get(name)
