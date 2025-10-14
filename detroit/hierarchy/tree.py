# Comments from original code source
# https://github.com/d3/d3-hierarchy/blob/main/src/tree.js
from collections.abc import Callable
from typing import TypeVar

from .hierarchy import Node

TTree = TypeVar("Tree", bound="Tree")


class TreeNode(Node):
    def __init__(self, node: Node, i: int):
        super().__init__(None)
        self.node = node
        self.parent = None
        self.children = None
        self.A = None  # default ancestor
        self.a = self  # ancestor
        self.z = 0  # prelim
        self.m = 0  # mod
        self.c = 0  # change
        self.s = 0  # shift
        self.t = None  # thread
        self.i = i  # number


def default_separation(a: TreeNode, b: TreeNode) -> int:
    return 1 if a.parent == b.parent else 2


def next_left(v: TreeNode) -> TreeNode:
    """
    This function is used to traverse the left contour of a subtree (or
    subforest). It returns the successor of v on this contour. This successor
    is either given by the leftmost child of v or by the thread of v. The
    function returns null if and only if v is on the highest level of its
    subtree.
    """
    children = v.children
    return children[0] if children else v.t


def next_right(v: TreeNode) -> TreeNode:
    """
    This function works analogously to next_left.
    """
    children = v.children
    return children[-1] if children else v.t


def move_subtree(wm: TreeNode, wp: TreeNode, shift: float):
    """
    Shifts the current subtree rooted at w+. This is done by increasing
    prelim(w+) and mod(w+) by shift.
    """
    change = shift / (wp.i - wm.i)
    wp.c -= change
    wp.s += shift
    wm.c += change
    wp.z += shift
    wp.m += shift


def execute_shifts(v: TreeNode):
    """
    All other shifts, applied to the smaller subtrees between w- and w+, are
    performed by this function. To prepare the shifts, we have to adjust
    change(w+), shift(w+), and change(w-).
    """
    shift = 0
    change = 0
    for w in reversed(v.children):
        w.z += shift
        w.m += shift
        change += w.c
        shift += w.s + change


def next_ancestor(vim: TreeNode, v: TreeNode, ancestor: TreeNode) -> TreeNode:
    """
    If vi-'s ancestor is a sibling of v, returns vi-'s ancestor. Otherwise,
    returns the specified (default) ancestor.
    """
    return vim.a if vim.a.parent == v.parent else ancestor


def tree_root(root: Node) -> TreeNode:
    tree = TreeNode(root, 0)
    nodes = [tree]

    while nodes:
        node = nodes.pop()
        if children := node.node.children:
            node.children = [None] * len(children)
            for i, c in reversed(list(enumerate(children))):
                child = node.children[i] = TreeNode(c, i)
                child.parent = node
                nodes.append(child)

    parent = tree.parent = TreeNode(None, 0)
    parent.children = [tree]
    return tree


# Node-link tree diagram using the Reingold-Tilford "tidy" algorithm
class Tree:
    """
    Tree layout
    """
    def __init__(self):
        self._separation = default_separation
        self._dx = 1
        self._dy = 1
        self._node_size = None

    def __call__(self, root: Node) -> Node:
        """
        Lays out the specified root hierarchy, assigning the following
        properties on root and its descendants:

        * :code:`node.x` - the x-coordinate of the node
        * :code:`node.y` - the y coordinate of the node

        The coordinates :code:`x` and :code:`y` represent an arbitrary
        coordinate system; for example, you can treat :code:`x` as an angle and
        :code:`y` as a radius to produce a radial layout. You may want to call
        :code:`root.sort` before passing the hierarchy to the tree layout.

        Parameters
        ----------
        root : Node
            Root node

        Returns
        -------
        Node
            Node organized as tree
        """
        t = tree_root(root)

        # Compute the layout using Buchheim et al.'s algorithm.
        t.each_after(self._first_walk)
        t.parent.m = -t.z
        t.each_before(self._second_walk)

        # If a fixed node size is specified, scale x and y.
        if self._node_size:
            root.each_before(self._size_node)
        else:
            # If a fixed tree size is specified, scale x and y based on the
            # extent. Compute the left-most, right-most, and depth-most nodes
            # for extents.
            left = root
            right = root
            bottom = root

            def walk(node: Node):
                nonlocal left, right, bottom
                if node.x < left.x:
                    left = node
                if node.x > right.x:
                    right = node
                if node.depth > bottom.depth:
                    bottom = node

            root.each_before(walk)
            s = 1 if left == right else self._separation(left, right) * 0.5
            tx = s - left.x
            kx = self._dx / (right.x + s + tx)
            ky = self._dy / (bottom.depth or 1)

            def walk(node: Node):
                node.x = (node.x + tx) * kx
                node.y = node.depth * ky

            root.each_before(walk)
        return root

    def _first_walk(self, v: TreeNode):
        """
        Computes a preliminary x-coordinate for v. Before that, FIRST WALK is
        applied recursively to the children of v, as well as the function
        APPORTION. After spacing out the children by calling EXECUTE SHIFTS,
        the node v is placed to the midpoint of its outermost children.
        """
        children = v.children
        siblings = v.parent.children
        w = siblings[v.i - 1] if v.i else None

        if children:
            execute_shifts(v)
            midpoint = (children[0].z + children[-1].z) * 0.5
            if w:
                v.z = w.z + self._separation(v.node, w.node)
                v.m = v.z - midpoint
            else:
                v.z = midpoint
        elif w:
            v.z = w.z + self._separation(v.node, w.node)
        v.parent.A = self._apportion(v, w, v.parent.A or siblings[0])

    def _second_walk(self, v: TreeNode):
        """
        Computes all real x-coordinates by summing up the modifiers
        recursively.
        """
        v.node.x = v.z + v.parent.m
        v.m += v.parent.m

    def _apportion(self, v: TreeNode, w: TreeNode, ancestor: TreeNode) -> TreeNode:
        """
        The core of the algorithm. Here, a new subtree is combined with the
        previous subtrees. Threads are used to traverse the inside and outside
        contours of the left and right subtree up to the highest common level.
        The vertices used for the traversals are vi+, vi-, vo-, and vo+, where
        the superscript o means outside and i means inside, the subscript -
        means left subtree and + means right subtree. For summing up the
        modifiers along the contour, we use respective variables si+, si-, so-,
        and so+. Whenever two nodes of the inside contours conflict, we compute
        the left one of the greatest uncommon ancestors using the function
        ANCESTOR and call MOVE SUBTREE to shift the subtree and prepare the
        shifts of smaller subtrees. Finally, we add a new thread (if
        necessary).
        """
        if w:
            vip = v
            vop = v
            vim = w
            vom = vip.parent.children[0]
            sip = vip.m
            sop = vop.m
            sim = vim.m
            som = vom.m

            vim = next_right(vim)
            vip = next_left(vip)
            while vim and vip:
                vom = next_left(vom)
                vop = next_right(vop)
                vop.a = v
                shift = vim.z + sim - vip.z - sip + self._separation(vim.node, vip.node)
                if shift > 0:
                    move_subtree(next_ancestor(vim, v, ancestor), v, shift)
                    sip += shift
                    sop += shift
                sim += vim.m
                sip += vim.m
                som += vim.m
                sop += vim.m
                vim = next_right(vim)
                vip = next_left(vip)
            if vim and not next_right(vop):
                vop.t = vim
                vim.m += sim - sop
            if vip and not next_left(vom):
                vom.t = vip
                vom.m += sip - som
                ancestor = v
        return ancestor

    def _size_node(self, node: Node):
        node.x *= self._dx
        node.y = node.depth * self._dy

    def set_separation(self, separation: Callable[[Node, Node], int]) -> TTree:
        """
        Sets the :code:`separation` accessor to the specified function and
        returns this tree layout.

        Parameters
        ----------
        separation : Callable[[Node, Node], int]
            Separation function which compares two nodes.

        Returns
        -------
        Tree
            Itself
        """
        self._separation = separation
        return self

    def set_size(self, size: tuple[float, float]) -> TTree:
        """
        Sets this tree layout's size to the specified two-element array of
        numbers :code:`[width, height]` and returns this tree layout. A layout
        size of :code:`None` indicates that a node size will be used instead.
        The coordinates :code:`x` and :code:`y` represent an arbitrary
        coordinate system; for example, to produce a radial layout, a size of
        :code:`[360, radius]` corresponds to a breadth of 360° and a depth of
        radius.

        Parameters
        ----------
        size : tuple[float, float]
            Tree layout's size

        Returns
        -------
        Tree
            Itself
        """
        self._node_size = False
        self._dx = size[0]
        self._dy = size[1]

    def set_node_size(self, node_size: tuple[float, float]) -> TTree:
        """
        Sets this tree layout's node size to the specified two-element array of
        numbers :code:`[width, height]` and returns this tree layout. A node
        size of :code:`None` indicates that a layout size will be used instead.
        When a node size is specified, the root node is always positioned at
        :math:`(0, 0)`.

        Parameters
        ----------
        node_size : tuple[float, float]
            Tree layout's node size

        Returns
        -------
        Tree
            Itself
        """
        self._node_size = True
        self._dx = node_size[0]
        self._dy = node_size[1]
        return self

    def get_separation(self) -> Callable[[Node, Node], int]:
        return self._separation

    def get_size(self) -> tuple[float, float] | None:
        if self._node_size:
            return
        return [self._dx, self._dy]

    def get_node_size(self) -> tuple[float, float] | None:
        if self._node_size:
            return [self._dx, self._dy]
        return None


def tree() -> Tree:
    """
    Builds a new tree layout with default settings.

    Returns
    -------
    Tree
        Tree object
    """
    return Tree()
