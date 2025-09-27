from ..types import T, Accessor, EtreeFunction
from ..array import argpass
from lxml import etree
import re

CLASS_PATTERN = re.compile(r"^|\s+")

def class_array(string: str) -> list[str]:
    """
    Splits a class string into several class names.

    Parameters
    ----------
    string : str
        Class string

    Returns
    -------
    list[str]
        Class names
    """
    return CLASS_PATTERN.split(string.strip())

def classed_add(node: etree.Element, names: list[str]):
    """
    Adds the list of :code:`names` into class property of the specified node.

    Parameters
    ----------
    node : etree.Element
        Node to update
    names : list[str]
        Class names
    """
    class_names = []
    if class_string := node.get("class"):
        class_names = class_string.split(" ")
    for name in names:
        if name not in class_names:
            class_names.append(name)
    node.set("class", " ".join(class_names).strip())

def classed_remove(node: etree.Element, names: list[str]):
    """
    Removes the list of :code:`names` into class property of the specified
    node.

    Parameters
    ----------
    node : etree.Element
        Node to update
    names : list[str]
        Class names
    """
    class_names = []
    if class_string := node.get("class"):
        class_names = class_string.split(" ")
    length = len(class_names)
    for name in names:
        # Not clean but faster than checking if `class_names` contain `name`
        try:
            class_names.remove(name)
        except ValueError:
            pass
    if len(class_names) != length:
        node.set("class", " ".join(class_names).strip())

def classed_constant(class_names: str, value: bool) -> EtreeFunction[T, None]:
    """
    Returns a function which adds or removes specified classes of a specified
    node given a condition :code:`value`.

    Parameters
    ----------
    class_names : str
        Class name
    value : bool
        Constant condition for adding or removing class name

    Returns
    -------
    EtreeFunction[T, None]
        Function for adding or removing class name
    """
    names = class_array(class_names)
    classed = classed_add if value else classed_remove

    def callback(node: etree.Element, data: T, i: int, group: list[etree.Element]):
        classed(node, names)

    return callback


def classed_function(
    class_names: str,
    value: Accessor[T, str | bool],
) -> EtreeFunction[T, None]:
    """
    Returns a function which adds or removes specified classes of a specified
    node given a condition :code:`value`.

    Parameters
    ----------
    class_names : str
        Class name
    value : Accessor[T, str | bool]
        Condition function which returns a boolean indicating if the class name
        must be added or removed from the node.

    Returns
    -------
    EtreeFunction[T, None]
        Function for adding or removing class name
    """
    names = class_array(class_names)
    value = argpass(value)

    def callback(node: etree.Element, data: T, i: int, group: list[etree.Element]):
        if value(data, i, group):
            classed_add(node, names)
        else:
            classed_remove(node, names)

    return callback
