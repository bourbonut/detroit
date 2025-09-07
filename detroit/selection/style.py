from lxml import etree

from ..array import argpass
from ..types import Accessor, EtreeFunction, T


def str_to_attrs(style: str) -> dict[str, str]:
    """
    Transforms a string into a dictionary containing style attributes

    Parameters
    ----------
    style : str
        Style string

    Returns
    -------
    dict[str, str]
        Dictionary containing style attributes
    """
    if not style:
        return {}
    style = style[:-1] if style.endswith(";") else style
    return {
        property: value
        for property, value in (desc.split(":") for desc in style.split(";"))
    }


def attrs_to_str(attrs: dict[str, str]) -> str:
    """
    Transforms a dictionary containing style attributes into a string

    Parameters
    ----------
    attrs : dict[str, str]
        Style attributes

    Returns
    -------
    str
        Style string
    """
    style = ";".join((":".join(pair) for pair in attrs.items()))
    return f"{style};"


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
        style = node.get("style", "")
        attrs = str_to_attrs(style)
        if name in attrs:
            attrs[name] = str(value)
            style = attrs_to_str(attrs)
        else:
            style = f"{style}{name}:{value};"
        node.set("style", style)

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
        style = node.get("style", "")
        new_value = value(data, i, group)
        attrs = str_to_attrs(style)
        if name in attrs:
            attrs[name] = str(new_value)
            style = attrs_to_str(attrs)
        else:
            style = f"{style}{name}:{new_value};"
        node.set("style", style)

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
