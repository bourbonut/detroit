from .namespace import namespace
from .style import style_value
from lxml import etree

class Selection:
    def __init__(self, node):
        root = node.getparent()
        self.root = root if root is not None else node
        self.node = node
        self.data = None

    def append(self, name):
        fullname = namespace(name)
        node = (
            etree.SubElement(self.root, fullname["local"], attrs=fullname["space"])
            if isinstance(fullname, dict)
            else etree.SubElement(self.root, fullname)
        )
        self.node.append(node)
        return Selection(node)

    def attr(self, name, value=None):
        if value is None:
            return self.node.get(name)
        elif callable(value):
            for item in self.data:
                self.node.set(name, str(item))
        else:
            self.node.set(name, str(value))
        return self

    def style(self, name, value=None):
        if value is None:
            return style_value(self.node.get("style"), name)
        current_value = self.node.get("style", "")
        self.node.set("style", f"{current_value}{name}:{value};")
        return self

    def datum(self, value):
        self.data = [value]
        return self

    def call(self, func, *args):
        return func(self, *args)

    def __str__(self):
        root = self.root
        node = self.node
        while node != self.root:
            node = node.getparent()
            root = root.getparent()
        return etree.tostring(root).decode("utf-8")
