from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypeVar

from ..array import argpass

TNode = TypeVar("Node", bound="Node")


class Node:
    """
    Node object

    Parameters
    ----------
    data : Any
        Data

    Attributes
    ----------
    data : Any
        The associated data
    depth : int
        Zero for the root, increasing by one for each descendant generation
    height : int
        Greatest distance from any descendant leaf, or zero for leaves
    parent : Node | None
        The parent node or :code:`None` for the root node
    value : float | None
        Optional summed value of the node and its descendants
    children : list[Node] | None
        An array of child nodes, if any, or undefined for leaves
    """
    def __init__(self, data: Any):
        self.data = data
        self.depth = 0
        self.height = 0
        self.parent = None
        self.value = None
        self.children = None

    def __iter__(self) -> Iterator[TNode]:
        """
        Returns an iterator over the node's descendants in breadth-first order.

        Returns
        -------
        Iterator[Node]
            Iterator over the node's descendants
        """
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

    def ancestors(self) -> list[TNode]:
        """
        Returns the array of ancestors nodes, starting with this node, then
        followed by each parent up to the root.

        Returns
        -------
        list[Node]
            List of ancestors
        """
        node = self
        nodes = [node]
        while node := node.parent:
            nodes.append(node)
        return nodes

    def count(self) -> int:
        """
        Computes the number of leaves under this node and assigns it to
        node.value, and similarly for every descendant of node. If this node is
        a leaf, its count is one. Returns this node. See also node.sum.

        Returns
        -------
        int
           Number of leaves 
        """
        return self.each_after(count)

    def copy(self) -> TNode:
        """
        Return a deep copy of the subtree starting at this node. (The returned
        deep copy shares the same data, however.). The returned node is the
        root of a new tree; the returned node's parent is always null and its
        depth is always zero.

        Returns
        -------
        Node
            Copied node
        """
        return hierarchy(self, node_children).each_before(copy_data)

    def descendants(self) -> list[TNode]:
        """
        Returns the array of descendant nodes, starting with this node, then
        followed by each child in topological order.

        Returns
        -------
        list[Node]
            Descendant nodes
        """
        return list(self)

    def each(self, callback: Callable[[TNode, int, TNode], None]) -> TNode:
        """
        Invokes the specified function for node and each descendant in
        breadth-first order, such that a given node is only visited if all
        nodes of lesser depth have already been visited, as well as all
        preceding nodes of the same depth. The specified function is passed the
        current descendant, the zero-based traversal index, and this node. If
        that is specified, it is the this context of the callback.

        Parameters
        ----------
        callback : Callable[[Node, int, Node], None]
            Function to call which takes as argument:

            * **node** (:code:`Node`) - the descendant node
            * **i** (:code:`int`) - the index of the descendant node
            * **self** (:code:`Node`) - the current node itself

        Returns
        -------
        Node
            Itself
        """
        callback = argpass(callback)
        for i, node in enumerate(self):
            callback(node, i, self)
        return self

    def each_after(self, callback: Callable[[TNode, int, TNode], None]) -> TNode:
        """
        Invokes the specified function for node and each descendant in
        post-order traversal, such that a given node is only visited after all
        of its descendants have already been visited. The specified function is
        passed the current descendant, the zero-based traversal index, and this
        node. If that is specified, it is the this context of the callback.

        Parameters
        ----------
        callback : Callable[[Node, int, Node], None]
            Function to call which takes as argument:

            * **node** (:code:`Node`) - the descendant node
            * **i** (:code:`int`) - the index of the descendant node
            * **self** (:code:`Node`) - the current node itself

        Returns
        -------
        Node
            Itself
        """
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
        """
        Invokes the specified function for node and each descendant in
        pre-order traversal, such that a given node is only visited after all
        of its ancestors have already been visited. The specified function is
        passed the current descendant, the zero-based traversal index, and this
        node. If that is specified, it is the this context of the callback.


        Parameters
        ----------
        callback : Callable[[Node, int, Node], None]
            Function to call which takes as argument:

            * **node** (:code:`Node`) - the descendant node
            * **i** (:code:`int`) - the index of the descendant node
            * **self** (:code:`Node`) - the current node itself

        Returns
        -------
        Node
            Itself
        """
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
        """
        Returns the first node in the hierarchy from this node for which the
        specified filter returns a truthy value. Returns undefined if no such
        node is found.

        Parameters
        ----------
        callback : Callable[[Node, int, Node], None]
            Function to call which takes as argument:

            * **node** (:code:`Node`) - the descendant node
            * **i** (:code:`int`) - the index of the descendant node
            * **self** (:code:`Node`) - the current node itself

        Returns
        -------
        Node
            Itself
        """
        callback = argpass(callback)
        for i, node in enumerate(self):
            if callback(node, i, self):
                return node

    def leaves(self) -> list[TNode]:
        """
        Returns the array of leaf nodes in traversal order. A leaf is a node
        with no children.

        Returns
        -------
        list[Node]
            Leaf nodes
        """
        leaves = []

        def leave(node):
            if node.children is None:
                leaves.append(node)

        self.each_before(leave)
        return leaves

    def links(self) -> list[dict[str, TNode]]:
        """
        Returns an array of links for this node and its descendants, where each
        link is an object that defines source and target properties. The source
        of each link is the parent node, and the target is a child node.

        Returns
        -------
        list[dict[str, Node]]
            List of links where :code:`link = {"source": node.parent, "target":
            node}`
        """
        root = self
        links = []

        def link(node):
            if node != root:
                links.append({"source": node.parent, "target": node})

        root.each(link)
        return links

    def path(self, end: TNode) -> list[TNode]:
        """
        Returns the shortest path through the hierarchy from this node to the
        specified target node. The path starts at this node, ascends to the
        least common ancestor of this node and the target node, and then
        descends to the target node. This is useful for hierarchical edge
        bundling.


        Parameters
        ----------
        end : Node
            Target

        Returns
        -------
        list[Node]
            List of nodes
        """
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
        """
        Sorts the children of this node, if any, and each of this node's
        descendants' children, in pre-order traversal using the specified
        compare function, and returns this node.

        Parameters
        ----------
        compare : Callable[[Node], float]
            Compare key function

        Returns
        -------
        Node
            Itself

        Notes
        -----
        :code:`functools.cmp_to_key` should be used to compare two nodes.

        .. code:: python
            
            from functools import cmp_to_key

            def compare(a: Node, b: Node) -> float:
                a_value = 0. if a.value is None else a.value
                b_value = 0. if b.value is None else b.value
                return a_value - b_value

            root = root.sort(compare=cmp_to_key(compare))
        """
        def sort(node):
            if node.children is not None:
                node.children.sort(key=compare)

        return self.each_before(sort)

    def sum(self, value: Callable[[dict[str, Any]], float]) -> TNode:
        """
        Evaluates the specified value function for this node and each
        descendant in post-order traversal, and returns this node. The
        node.value property of each node is set to the numeric value returned
        by the specified function plus the combined value of all children. The
        function is passed the node's data, and must return a non-negative
        number. The value accessor is evaluated for node and every descendant,
        including internal nodes; if you only want leaf nodes to have internal
        value, then return zero for any node with children.

        Parameters
        ----------
        value : Callable[[dict[str, Any]], float]
            Function which takes the node's data as input and return a float
            value as output

        Returns
        -------
        Node
            Itself
        """
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
        dict_ = self.__dict__.copy()
        dict_["data"] = f"{dict_['data'].__class__.__name__}"
        dict_["parent"] = f"{dict_['parent'].__class__.__name__}"
        attributs = ",\n    ".join(f"{key}: {dict_[key]}" for key in dict_)
        return f"Node(\n    {attributs},\n)"

    def __repr__(self):
        children = f"list({len(self.children)}" if self.children else None
        return f"Node(children={children}))"


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
    data: dict[str, Any] | Node, children: Callable[[dict[str, Any]], Any | None] = None
) -> Node:
    """
    Builds a root node from the specified hierarchical data. The specified
    :code:`data` must be an object representing the root node.

    Parameters
    ----------
    data : dict[str, Any] | Node
        Data
    children : Callable[[dict[str, Any]], Any | None]
        Accessor function to get data children

    Returns
    -------
    Node
        Hierarchy node object
    """
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
