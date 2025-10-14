from collections.abc import Callable
from statistics import mean
from typing import TypeVar

from .hierarchy import Node

TCluster = TypeVar("Cluster", bound="Cluster")


def default_separation(a: Node, b: Node) -> int:
    return 1 if a.parent == b.parent else 2


def mean_x(children: list[Node]) -> float:
    return mean((child.x for child in children))


def max_y(children: list[Node]) -> float:
    return 1 + max((child.y for child in children))


def leaf_left(node: Node) -> Node:
    while children := node.children:
        node = children[0]
    return node


def leaf_right(node: Node) -> Node:
    while children := node.children:
        node = children[-1]
    return node


class Cluster:
    """
    Cluster layout
    """
    def __init__(self):
        self._separation = default_separation
        self._dx = 1
        self._dy = 1
        self._node_size = False

    def __call__(self, root: Node) -> Node:
        """
        Lays out the specified root hierarchy, assigning the following
        properties on root and its descendants:

        * :code:`node.x` - the x-coordinate of the node
        * :code:`node.y` - the y coordinate of the node

        The coordinates :code:`x` and :code:`y` represent an arbitrary
        coordinate system; for example, you can treat :code:`x` as an angle and
        :code:`y` as a radius to produce a radial layout. You may want to call
        :code:`root.sort` before passing the hierarchy to the cluster layout.

        Parameters
        ----------
        root : Node
            Root node

        Returns
        -------
        Node
            Node organized as cluster
        """
        x = 0
        previous_node = None

        def cluster(node: Node):
            nonlocal previous_node, x
            children = node.children
            if children:
                node.x = mean_x(children)
                node.y = max_y(children)
            else:
                if previous_node is None:
                    node.x = 0
                else:
                    x += self._separation(node, previous_node)
                    node.x = x
                node.y = 0
                previous_node = node

        root.each_after(cluster)

        left = leaf_left(root)
        right = leaf_right(root)
        x0 = left.x - self._separation(left, right) * 0.5
        x1 = right.x + self._separation(right, left) * 0.5

        if self._node_size:

            def update(node):
                node.x = (node.x - root.x) * self._dx
                node.y = (root.y - node.y) * self._dy
        else:

            def update(node):
                node.x = (node.x - x0) / (x1 - x0) * self._dx
                node.y = (1 - ((node.y / root.y) if root.y else 1)) * self._dy

        return root.each_after(update)

    def set_separation(self, separation: Callable[[Node, Node], int]) -> TCluster:
        """
        Sets the :code:`separation` accessor to the specified function and
        returns this cluster layout.

        Parameters
        ----------
        separation : Callable[[Node, Node], int]
            Separation function which compares two nodes.

        Returns
        -------
        Cluster
            Itself
        """
        self._separation = separation
        return self

    def set_size(self, size: tuple[float, float]) -> TCluster:
        """
        Sets this cluster layout's size to the specified two-element array of
        numbers :code:`[width, height]` and returns this cluster layout. A
        layout size of :code:`None` indicates that a node size will be used
        instead. The coordinates :code:`x` and :code:`y` represent an arbitrary
        coordinate system; for example, to produce a radial layout, a size of
        :code:`[360, radius]` corresponds to a breadth of 360° and a depth of
        radius.

        Parameters
        ----------
        size : tuple[float, float]
            Size values

        Returns
        -------
        Cluster
            Itself
        """
        self._node_size = False
        self._dx = size[0]
        self._dy = size[1]
        return self

    def set_node_size(self, size: tuple[float, float]) -> TCluster:
        """
        Sets this cluster layout's node size to the specified two-element array
        of numbers :code:`[width, height]` and returns this cluster layout. A
        node size of null indicates that a layout size will be used instead.
        When a :code:`size` is specified, the root node is always positioned at
        :math:`(0, 0)`.

        Parameters
        ----------
        size : tuple[float, float]
            Size values

        Returns
        -------
        Cluster
            Itself
        """
        self._node_size = True
        self._dx = size[0]
        self._dy = size[1]
        return self

    def get_separation(self) -> Callable[[Node, Node], int]:
        return self._separation

    def get_size(self) -> tuple[float, float] | None:
        if self._node_size:
            return None
        return [self._dx, self._dy]

    def get_node_size(self) -> tuple[float, float] | None:
        if self._node_size:
            return [self._dx, self._dy]
        return None


def cluster() -> Cluster:
    """
    Builds a new cluster layout with default settings.

    Returns
    -------
    Cluster
        Cluster object
    """
    return Cluster()
