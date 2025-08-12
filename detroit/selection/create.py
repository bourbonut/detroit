from lxml import etree

from .namespace import namespace
from .selection import Selection


def create(name: str) -> Selection:
    """
    Given the specified element name, returns a single-element selection
    containing a detached element of the given name in the current document.
    This method assumes the HTML namespace, so you must specify a namespace
    explicitly when creating SVG or other non-HTML elements.

    Parameters
    ----------
    name : str
        Tag name

    Returns
    -------
    Selection
        XML tree
    """
    fullname = namespace(name)
    document = (
        etree.Element(fullname["local"], attrib={"xmlns": fullname["space"][None]})
        if isinstance(fullname, dict)
        else etree.Element(fullname)
    )
    return Selection([[document]], [document])
