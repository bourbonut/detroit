from .namespace import namespace
from .style import style_value
from lxml import etree

def find_nodes(root, selection):
    if "." in selection:
        tag, class_name = selection.split(".")
        tag = tag or "*"
        class_name = f"[@class='{class_name}']" if class_name else ""
        return root.xpath(f"//{tag}{class_name}")
    else:
        return root.xpath(f"//{selection}")

class Selection:
    def __init__(self, nodes, root):
        self.root = root
        self.nodes = nodes
        self.bound_data = None

    def select(self, selection):
        return Selection(find_nodes(self.root, selection)[:1], self.root)

    def select_all(self, selection):
        return Selection(find_nodes(self.root, selection), self.root)

    def append(self, name):
        fullname = namespace(name)
        nodes = []
        for selected in self.nodes:
            node = (
                etree.SubElement(selected, fullname["local"], attrs=fullname["space"])
                if isinstance(fullname, dict)
                else etree.SubElement(selected, fullname)
            )
            selected.append(node)
            nodes.append(node)
        return Selection(nodes, self.root)

    def attr(self, name, value=None):
        if value is None:
            return self.nodes[0].get(name)
        elif callable(value):
            for item, selected in zip(self.data, self.nodes):
                selected.set(name, str(item))
        else:
            for selected in self.nodes:
                selected.set(name, str(value))
        return self

    def style(self, name, value=None):
        if value is None:
            return style_value(self.nodes[0].get("style"), name)
        for selected in self.nodes:
            current_value = selected.get("style", "")
            selected.set("style", f"{current_value}{name}:{value};")
        return self

    def datum(self, value):
        self.bound_data = [value]
        return self

    def data(self, values, key=None):
        if key:
            self.bound_data = list(map(key, values))
        else:
            self.bound_data = values
        return self

    def call(self, func, *args):
        return func(self, *args)

    def __str__(self):
        return etree.tostring(self.root).decode("utf-8")

    def __repr__(self):
        selected_nodes = [
            f"{element.tag}{'.' + element.attrib.get('class', '')}" for element in self.nodes
        ]
        return f"Selection(root={self.root.tag}, nodes=[{', '.join(selected_nodes)}])"
