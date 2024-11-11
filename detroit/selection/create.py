from .namespace import namespace
from .selection import Selection
from lxml import etree

def create(name):
    fullname = namespace(name)
    document = etree.Element(fullname["local"], attrib=fullname["space"])
    return Selection([[document]], [document])
