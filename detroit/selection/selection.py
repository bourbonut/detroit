from .namespace import namespace
from .style import style_value
from .bind import bind_key, bind_index
from .constant import constant
from .attr import attr_function, attr_constant
from .enter import EnterNode
from lxml import etree

class Node:
    def __init__(self, parent, datum=None):
        self._parent = parent
        self._data = datum or []

def selector(element, selection):
    if "." in selection:
        tag, class_name = selection.split(".")
        tag = tag or "*"
        class_name = f"[@class='{class_name}']" if class_name else ""
        return element.xpath(f"//{tag}{class_name}")
    return element.xpath(f"//{selection}")

def creator(node, fullname):
    return (
        etree.SubElement(node, fullname["local"], attrs=fullname["space"])
        if isinstance(fullname, dict)
        else etree.SubElement(node, fullname)
    )

class Selection:
    def __init__(self, groups, parents, enter=None, exit=None, data=None):
        self._groups = groups
        self._parents = parents
        self._enter = enter
        self._exit = exit
        self._data = data or {}

    def select(self, selection):
        subgroups = [
            selector(node, selection)[:1]
            for group in self._groups for node in group if node is not None
        ]
        return Selection(subgroups, self._parents, data=self._data)

    def select_all(self, selection):
        subgroups = [
            selector(node, selection)
            for group in self._groups for node in group if node is not None
        ]
        return Selection(subgroups, self._parents, data=self._data)

    def enter(self):
        return Selection(
            self._enter or [[None] * len(group) for group in self._groups],
            self._parents,
            data=self._data,
        )

    def exit(self):
        return Selection(
            self._exit or [[None] * len(group) for group in self._groups],
            self._parents,
            data=self._data,
        )

    def merge(self, context):
        selection = context.selection() if hasattr(context, 'selection') else context

        merges = []
        for groups0, groups1 in zip(self._groups, selection._groups):
            merge = []
            for group0, group1 in zip(groups0, groups1):
                node = group0 or group1
                merge.append(node)
            merges.append(merge)

        for j in range(len(merges), len(self._groups)):
            merges.append(self._groups[j])

        return Selection(merges, self._parents, data=self._data)

    def append(self, name):
        fullname = namespace(name)
        subgroups = []
        for group in self._groups:
            subgroup = []
            for node in group:
                if isinstance(node, EnterNode):
                    node = node._parent
                subnode = creator(node, fullname)
                node.append(subnode)
                subgroup.append(subnode)
            subgroups.append(subgroup)
        return Selection(subgroups, self._parents, data=self._data)

    def each(self, callback):
        for group in self._groups:
            for i, node in enumerate(group):
                if node is not None:
                    if isinstance(node, EnterNode):
                        node = node._parent
                    callback(node, self._data.get(node), i, group)

    def attr(self, name, value=None):
        if value is None:
            return self.node().get(name)
        elif callable(value):
            self.each(attr_function(name, value))
        else:
            self.each(attr_constant(name, value))
        return self

    def style(self, name, value=None): # TODO : update this method
        if value is None:
            return style_value(self.nodes[0].get("style"), name)
        for selected in self.nodes:
            current_value = selected.get("style", "")
            selected.set("style", f"{current_value}{name}:{value};")
        return self

    def datum(self, value):
        self._data[self.node()] = value
        return self

    def data(self, values, key=None):
        bind = bind_key if key else bind_index
        parents = self._parents
        groups = self._groups

        if not callable(values):
            values = constant(values)

        update = [None] * len(groups)
        enter = [None] * len(groups)
        exit = [None] * len(groups)
        for j in range(len(groups)):
            parent = parents[j]
            group = groups[j]
            data = list(values(parent, self._data.get(parent), j, parents))
            enter[j] = enter_group = [None] * len(data)
            update[j] = update_group = [None] * len(data)
            exit[j] = exit_group = [None] * len(group)

            bind(self._data, parent, group, enter_group, update_group, exit_group, data, key)

            for i0 in range(len(data)):
                previous = enter_group[i0]
                if previous:
                    i1 = i0 + 1
                    while not (update_group[i1] if i1 < len(update_group) else None) and i1 < len(data):
                        i1 += 1
                    previous._next = update_group[i1] if i1 < len(data) else None

        return Selection(update, parents, enter, exit, self._data)

    def order(self): # TODO : test it
        for group in self._groups:
            next_node = None
            for node in reversed(group):
                if node is not None:
                    if next_node is not None and (node.getprevious() == next_node):
                        parent = next_node.getparent()
                        index = parent.index(next_node)
                        parent.pop(index)
                        parent.insert(index, node)
                    next_node = node
        return self

    def insert(self, name, before):
        fullname = namespace(name)
        for group in self._groups:
            for node in group:
                if node is not None:
                    if isinstance(node, EnterNode):
                        node = node._parent
                    if selection := selector(node, before):
                        index = node.index(selection[0])
                        node.insert(index, creator(node, fullname))
        return self

    def remove(self):
        def remove(node, data, i, group):
            parent = node.getparent()
            if parent is not None:
                parent.remove(node)
        self.each(remove)
        return self

    def call(self, func, *args):
        return func(self, *args)

    def node(self):
        return next(iter(self))

    def nodes(self):
        return list(self)

    def __iter__(self):
        for group in self._groups:
            for node in group:
                if node is not None:
                    yield node

    def selection(self):
        return self

    def __str__(self):
        return etree.tostring(self._parents[0]).decode("utf-8")

    def __repr__(self):
        selected_nodes = [
            f"{element.tag}{'.' + element.attrib.get('class', '')}" for element in self.nodes
        ]
        return f"Selection(root={self.root.tag}, nodes=[{', '.join(selected_nodes)}])"
