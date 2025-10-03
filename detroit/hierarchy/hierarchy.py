from ..array import argpass
from collections.abc import Callable, Iterable
from typing import Any, TypeVar

TNode = TypeVar("Node", bound="Node")

class Node:

    def __init__(self, data: Any):
        self.data = data
        self.depth = 0
        self.height = 0
        self.parent = None
        self.value = None
        self.children = None

    def __iter__(self):
        node = self
        next = [node]
        while True:
            next.reverse()
            current = next
            next = []
            while current:
                node = current.pop()
                yield node
                children = node.children
                if children is not None:
                    next.extend(children)
            if len(next) == 0:
                break

    def ancestors(self):
        node = self
        nodes = [node]
        while node := node.parent:
            nodes.append(node)
        return nodes

    def count(self):
        return self.each_after(count)

    def copy(self):
        return hierarchy(self, node_children).each_before(copy_data)

    def descendants(self):
        return list(self)

    def each(self, callback: Callable[[TNode, int, TNode], None]) -> TNode:
        callback = argpass(callback)
        for i, node in enumerate(self):
            callback(node, i, self)
        return self

    def each_after(self, callback: Callable[[TNode, int, TNode], None]) -> TNode:
        callback = argpass(callback)
        node = self
        nodes = [node]
        next = []
        index = -1
        while nodes:
            node = nodes.pop()
            next.append(node)
            children = node.children
            if children is not None:
                nodes.extend(children)
        while next:
            index += 1
            node = next.pop()
            callback(node, index, self)
        return self

    def each_before(self, callback: Callable[[TNode, int, TNode], None]) -> TNode:
        callback = argpass(callback)
        node = self
        nodes = [node]
        index = -1
        while nodes:
            node = nodes.pop()
            index += 1
            callback(node, index, self)
            children = node.children
            if children is not None:
                nodes.extend(reversed(children))
        return self

    def find(self, callback: Callable[[TNode, int, TNode], None]) -> TNode:
        callback = argpass(callback)
        for i, node in enumerate(self):
            if callback(node, i, self):
                return node

    def leaves(self) -> list[TNode]:
        leaves = []
        def leave(node):
            if node.children is None:
                leaves.append(node)
        self.each_before(leave)
        return leaves

    def links(self) -> list[dict[str, TNode]]:
        root = self
        links = []
        def link(node):
            if node != root:
                links.append({"source": node.parent, "target": node})
        root.each(link)
        return links

    def path(self, end: TNode) -> list[TNode]:
        start = self
        ancestor = least_common_ancestor(start, end)
        nodes = [start]
        while start != ancestor:
            start = start.parent
            nodes.append(start)

        k = len(nodes)
        while end != ancestor:
            nodes.insert(k, end)
            end = end.parent
        return nodes

    def sort(self, compare: Callable[[TNode], float]) -> TNode:
        def sort(node):
            if node.children is not None:
                node.children.sort(key=compare)
        return self.each_before(sort)

    def sum(self, value: Callable[[dict[str, Any]], float]) -> TNode:
        def sum_node(node):
            v = value(node.data)
            sum_value = 0 if v is None else v
            children = node.children
            i = 0 if children is None else len(children)
            i -= 1
            while i >= 0:
                sum_value += children[i].value
                i -= 1
            node.value = sum_value
        return self.each_after(sum_node)

    def __str__(self):
        dict_ = self.__dict__
        attributs = "\n    ".join(f"{key}: {dict_[key]}" for key in dict_)
        return f"Node(\n    {attributs}\n)"

    def __repr__(self):
        return f"Node(value={self.value})"

def node_children(d: Node) -> list[Node] | None:
    return d.children

def object_children(d: dict[str, Any]) -> Any | None:
    return d.get("children")

def copy_data(node: Node):
    if node.data.value is not None:
        node.value = node.data.value
    node.data = node.data.data

def count(node: Node):
    sum_value = 0
    children = node.children
    i = 0 if children is None else len(children)
    if i == 0:
        sum_value = 1
    else:
        i -= 1
        while i >= 0:
            sum_value += children[i].value
            i -= 1
    node.value = sum_value

def least_common_ancestor(a: Node, b: Node):
    if a == b:
        return a
    a_nodes = a.ancestors()
    b_nodes = b.ancestors()
    c = None
    a = a_nodes.pop()
    b = b_nodes.pop()
    while a == b:
        c = a
        a = a_nodes.pop()
        b = b_nodes.pop()
    return c

def compute_height(node: Node):
    height = 0
    while True:
        node.height = height
        node = node.parent
        height += 1
        if node is None or node.height >= height:
            break

def hierarchy(
    data: dict[str, Any] | Node,
    children: Callable[[dict[str, Any]], Any | None] = None
) -> Node:
    if isinstance(data, Node):
        children = node_children
    elif children is None:
        children = object_children

    root = Node(data)
    nodes = [root]

    while nodes:
        node = nodes.pop()
        childs = children(node.data)
        if childs is None:
            continue
        childs = list(childs) if isinstance(childs, Iterable) else []
        n = len(childs)
        if n == 0:
            continue
        node.children = childs
        for i in range(n - 1, -1, -1):
            child = childs[i] = Node(childs[i])
            nodes.append(child)
            child.parent = node
            child.depth = node.depth + 1

    return root.each_before(compute_height)
