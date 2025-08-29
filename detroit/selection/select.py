from lxml import etree

from .selection import Selection


def select(node: etree.Element) -> Selection:
    """
    Returns a selection object given a node

    Parameters
    ----------
    node : etree.Element
        Node

    Returns
    -------
    Selection
        Selection object
    """
    return Selection([[node]], [node])
