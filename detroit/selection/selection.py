from itertools import zip_longest

from lxml import etree

from .attr import attr_constant, attr_function
from .bind import bind_index, bind_key
from .constant import constant
from .enter import EnterNode
from .namespace import namespace
from .style import style_value
from .text import text_constant, text_function


def selector(element, selection, whole=False):
    if selection is None:
        return element
    prefix = "//" if whole else "/"
    if "." in selection:
        tag, class_name = selection.split(".")
        tag = tag or "*"
        class_name = f"[@class='{class_name}']" if class_name else ""
        return element.xpath(f"{prefix}{tag}{class_name}")
    return element.xpath(f"{prefix}{selection}")


def creator(node, fullname):
    return (
        etree.SubElement(node, fullname["local"], attrs=fullname["space"])
        if isinstance(fullname, dict)
        else etree.SubElement(node, fullname)
    )


class DataDict:
    def __init__(self, keys=None, items=None):
        self.keys = keys or []
        self.items = items or []

    def __getitem__(self, key):
        return self.items[self.keys.index(key)]

    def __setitem__(self, key, item):
        self.keys.append(key)
        self.items.append(item)

    def __or__(self, other):
        k1 = set(self.keys)
        k2 = set(other.keys)
        common_keys = list(k1 & k2)
        keys_left = list(k1 - k2)
        keys_right = list(k2 - k1)
        keys = common_keys + keys_left + keys_right
        items = (
            [self[key] for key in common_keys]
            + [self[key] for key in keys_left]
            + [other[key] for key in keys_right]
        )
        return DataDict(keys, items)

    def get(self, key):
        if key in self.keys:
            return self[key]

    def __str__(self):
        return (
            "{"
            + ", ".join(f"{key}:{item}" for key, item in zip(self.keys, self.items))
            + "}"
        )


class Selection:
    def __init__(self, groups, parents, enter=None, exit=None, data=None):
        self._groups = groups
        self._parents = parents
        self._enter = enter
        self._exit = exit
        self._data = data or {}

    def select(self, selection=None):
        subgroups = [
            selector(node, selection)[:1]
            for group in self._groups
            for node in group
            if node is not None
        ]
        parents = [
            (group[0]._parent if isinstance(group[0], EnterNode) else group[0])
            for group in self._groups
            if group[0] is not None
        ]
        return Selection(subgroups, parents or self._parents, data=self._data)

    def select_all(self, selection=None):
        subgroups = [
            selector(node, selection)
            for group in self._groups
            for node in group
            if node is not None
        ]
        parents = [
            (group[0]._parent if isinstance(group[0], EnterNode) else group[0])
            for group in self._groups
            if group[0] is not None
        ]
        return Selection(subgroups, parents or self._parents, data=self._data)

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
        selection = context.selection() if hasattr(context, "selection") else context

        merges = []
        for groups0, groups1 in zip_longest(
            self._groups, selection._groups, fillvalue=[]
        ):
            merge = []
            for group0, group1 in zip_longest(groups0, groups1, fillvalue=None):
                node = group0 if group0 is not None else group1
                merge.append(node)
            merges.append(merge)

        for j in range(len(merges), len(self._groups)):
            merges.append(self._groups[j])

        return Selection(merges, self._parents, data=self._data | selection._data)

    def append(self, name):
        fullname = namespace(name)
        subgroups = []
        for group in self._groups:
            subgroup = []
            for node in group:
                if node is None:
                    continue
                if isinstance(node, EnterNode):
                    enter_node = node
                    node = enter_node._parent
                    subnode = creator(node, fullname)
                    node.append(subnode)
                    subgroup.append(subnode)
                    self._data[subnode] = enter_node.__data__
                else:
                    subnode = creator(node, fullname)
                    node.append(subnode)
                    subgroup.append(subnode)
                    self._data[subnode] = self._data.get(node)
            subgroups.append(subgroup)
        parents = [
            (group[0]._parent if isinstance(group[0], EnterNode) else group[0])
            for group in self._groups
            if group[0] is not None
        ]
        return Selection(subgroups, parents or self._parents, data=self._data)

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

    def style(self, name, value=None):  # TODO : update this method
        if value is None:
            return style_value(self.nodes[0].get("style"), name)
        for selected in self.nodes:
            current_value = selected.get("style", "")
            selected.set("style", f"{current_value}{name}:{value};")
        return self

    def text(self, value=None):
        if value is None:
            return self.node().get("text")
        elif callable(value):
            self.each(text_function(value))
        else:
            self.each(text_constant(value))
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

            bind(
                self._data,
                parent,
                group,
                enter_group,
                update_group,
                exit_group,
                data,
                key,
            )

            for i0 in range(len(data)):
                previous = enter_group[i0]
                if previous:
                    i1 = i0 + 1
                    while not (
                        update_group[i1] if i1 < len(update_group) else None
                    ) and i1 < len(data):
                        i1 += 1
                    previous._next = update_group[i1] if i1 < len(data) else None

        return Selection(update, parents, enter, exit, self._data)

    def order(self):  # TODO : test it
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

    def join(self, onenter, onupdate=None, onexit=None):
        enter = self.enter()
        update = self
        exit = self.exit()

        # Enter
        if callable(onenter):
            enter = onenter(enter)
            if enter:
                enter = enter.selection()
        else:
            enter = enter.append(onenter)

        # Update
        if onupdate is not None:
            update = onupdate(update)
            if update:
                update = update.selection()

        # Exit
        if onexit is None:
            exit.remove()
        else:
            onexit(exit)

        if enter and update:
            return enter.merge(update).order()
        else:
            return update

    def insert(self, name, before):
        fullname = namespace(name)
        for group in self._groups:
            for i, node in enumerate(group):
                if node is not None:
                    if isinstance(node, EnterNode):
                        node = node._parent
                    selection = selector(node, before, True)
                    if selection := [
                        found for found in selection if found.getparent() == node
                    ]:
                        index = node.index(selection[0])
                        created = creator(node, fullname)
                        node.insert(index, created)
                        group[i] = created
        return self

    def remove(self):
        def remove(node, data, i, group):
            parent = node.getparent()
            if parent is not None:
                parent.remove(node)

        self.each(remove)
        return self

    def call(self, func, *args):
        func(self, *args)
        return self

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

    def to_string(self, pretty_print=True):
        return etree.tostring(self._parents[0], pretty_print=pretty_print).decode(
            "utf-8"
        )

    def __str__(self):
        return self.to_string(False)

    def __repr__(self):
        def node_repr(node):
            if node is None:
                return str(node)
            if isinstance(node, EnterNode):
                return str(node)
            tag = node.tag
            class_name = node.attrib.get("class")
            if class_name:
                return f"{tag}.{class_name}"
            return tag

        groups = [
            f"[{', '.join(node_repr(node) for node in group)}]"
            for group in self._groups
        ]
        parents = f"[{', '.join(node_repr(parent) for parent in self._parents)}]"
        return (
            f"Selection(\n    groups=[{', '.join(groups)}],\n    parents={parents},"
            f"\n    enter={self._enter},\n    exit={self._exit},\n    data={self._data},\n)"
        )
