from collections.abc import Callable
from typing import TypeVar

from ..accessors import required
from ..constant import constant, constant_zero
from ..hierarchy import Node
from .round import round_node
from .squarify import squarify

TTreeMap = TypeVar("TreeMap", bound="TreeMap")


class TreeMap:
    """
    TreeMap layout
    """
    def __init__(self):
        self._tile = squarify
        self._round = False
        self._dx = 1
        self._dy = 1
        self._padding_stack = {0: 0}
        self._padding_inner = constant_zero
        self._padding_top = constant_zero
        self._padding_right = constant_zero
        self._padding_bottom = constant_zero
        self._padding_left = constant_zero

    def __call__(self, root: Node) -> Node:
        """
        Lays out the specified root hierarchy, assigning the following
        properties on root and its descendants:

        * :code:`node.x0` - the left edge of the rectangle
        * :code:`node.y0` - the top edge of the rectangle
        * :code:`node.x1` - the right edge of the rectangle
        * :code:`node.y1` - the bottom edge of the rectangle

        You must call :code:`root.sum` before passing the hierarchy to the treemap
        layout. You probably also want to call root.sort to order the hierarchy
        before computing the layout.

        Parameters
        ----------
        root : Node
            Root node

        Returns
        -------
        Node
            Node organized as treemap
        """
        root.x0 = 0
        root.y0 = 0
        root.x1 = self._dx
        root.y1 = self._dy
        root.each_before(self._position_node)
        self._padding_stack = {0: 0}
        if self._round:
            root.each_before(round_node)
        return root

    def _position_node(self, node: Node):
        p = self._padding_stack[node.depth]
        x0 = node.x0 + p
        y0 = node.y0 + p
        x1 = node.x1 - p
        y1 = node.y1 - p

        if x1 < x0:
            x0 = x1 = (x0 + x1) * 0.5
        if y1 < y0:
            y0 = y1 = (y0 + y1) * 0.5

        node.x0 = x0
        node.y0 = y0
        node.x1 = x1
        node.y1 = y1

        if node.children:
            p = self._padding_stack[node.depth + 1] = self._padding_inner(node) * 0.5
            x0 += self._padding_left(node) - p
            y0 += self._padding_top(node) - p
            x1 -= self._padding_right(node) - p
            y1 -= self._padding_bottom(node) - p
            if x1 < x0:
                x0 = x1 = (x0 + x1) * 0.5
            if y1 < y0:
                y0 = y1 = (y0 + y1) * 0.5
            self._tile(node, x0, y0, x1, y1)

    def set_round(self, round_value: bool) -> TTreeMap:
        """
        If :code:`round` is specified, enables or disables rounding according
        to the given boolean and returns this treemap layout.

        Parameters
        ----------
        round_value : bool
            Round value

        Returns
        -------
        TreeMap
            Itself
        """
        self._round = round_value
        return self

    def set_size(self, size: tuple[float, float]) -> TTreeMap:
        """
        If :code:`size` is specified, sets this treemap layout's size to the
        specified two-element array of numbers :code:`[width, height]` and
        returns this treemap layout.

        Parameters
        ----------
        size : tuple[float, float]
            Size values

        Returns
        -------
        TreeMap
            Itself
        """
        self._dx = size[0]
        self._dy = size[1]
        return self

    def set_tile(
        self, tile: Callable[[Node, float, float, float, float], None]
    ) -> TTreeMap:
        """
        Sets this treemap layout's tile and returns this treemap layout.

        Available treemap tiles:

        * :func:`d3.treemap_binary <detroit.treemap_binary>`
        * :func:`d3.treemap_dice <detroit.treemap_dice>`
        * :func:`d3.treemap_slice <detroit.treemap_slice>`
        * :func:`d3.treemap_slice_dice <detroit.treemap_slice_dice>`
        * :func:`d3.treemap_squarify <detroit.treemap_squarify>`
        * :func:`d3.treemap_resquarify <detroit.treemap_resquarify>`

        Parameters
        ----------
        tile : Callable[[Node, float, float, float, float], None]
            Tile function

        Returns
        -------
        TreeMap
            Itself
        """
        self._tile = required(tile)
        return self

    def set_padding(self, padding: Callable[[Node], float] | float) -> TTreeMap:
        """
        Sets the inner and outer padding to the specified number or function
        and returns this treemap layout.

        Parameters
        ----------
        padding : Callable[[Node], float] | float
            Padding function or constant padding value

        Returns
        -------
        TreeMap
            Itself
        """
        return self.set_padding_inner(padding).set_padding_outer(padding)

    def set_padding_inner(
        self, padding_inner: Callable[[Node], float] | float
    ) -> TTreeMap:
        """
        Sets the inner padding to the specified number or function and returns
        this treemap layout. If :code:`padding_inner` is a function, it is
        invoked for each node with children, being passed the current node. The
        inner padding is used to separate a node's adjacent children.

        Parameters
        ----------
        padding_inner : Callable[[Node], float] | float
            Inner padding function or constant inner padding value

        Returns
        -------
        TreeMap
            Itself
        """
        if callable(padding_inner):
            self._padding_inner = padding_inner
        else:
            self._padding_inner = constant(padding_inner)
        return self

    def set_padding_outer(
        self, padding_outer: Callable[[Node], float] | float
    ) -> TTreeMap:
        """
        Sets the top, right, bottom and left padding to the specified number or
        function and returns this treemap layout.

        Parameters
        ----------
        padding_outer : Callable[[Node], float] | float
            Outer padding function or constant outer padding value

        Returns
        -------
        TreeMap
            Itself
        """
        return (
            self.set_padding_top(padding_outer)
            .set_padding_right(padding_outer)
            .set_padding_bottom(padding_outer)
            .set_padding_left(padding_outer)
        )

    def set_padding_top(self, padding_top: Callable[[Node], float] | float) -> TTreeMap:
        """
        Sets the top padding to the specified number or function and returns
        this treemap layout. If :code:`padding_top` is a function, it is
        invoked for each node with children, being passed the current node. The
        top padding is used to separate the top edge of a node from its
        children.

        Parameters
        ----------
        padding_top : Callable[[Node], float] | float
            Top padding function or constant top padding value

        Returns
        -------
        TreeMap
            Itself
        """
        if callable(padding_top):
            self._padding_top = padding_top
        else:
            self._padding_top = constant(padding_top)
        return self

    def set_padding_right(
        self, padding_right: Callable[[Node], float] | float
    ) -> TTreeMap:
        """
        Sets the right padding to the specified number or function and returns
        this treemap layout. If :code:`padding_right` is a function, it is
        invoked for each node with children, being passed the current node. The
        right padding is used to separate the right edge of a node from its
        children.

        Parameters
        ----------
        padding_right : Callable[[Node], float] | float
            Right padding function or constant right padding value

        Returns
        -------
        TreeMap
            Itself
        """
        if callable(padding_right):
            self._padding_right = padding_right
        else:
            self._padding_right = constant(padding_right)
        return self

    def set_padding_bottom(
        self, padding_bottom: Callable[[Node], float] | float
    ) -> TTreeMap:
        """
        Sets the bottom padding to the specified number or function and returns
        this treemap layout. If :code:`padding_bottom` is a function, it is
        invoked for each node with children, being passed the current node. The
        bottom padding is used to separate the bottom edge of a node from its
        children.

        Parameters
        ----------
        padding_bottom : Callable[[Node], float] | float
            Bottom padding function or constant bottom padding value

        Returns
        -------
        TreeMap
            Itself
        """
        if callable(padding_bottom):
            self._padding_bottom = padding_bottom
        else:
            self._padding_bottom = constant(padding_bottom)
        return self

    def set_padding_left(
        self, padding_left: Callable[[Node], float] | float
    ) -> TTreeMap:
        """
        Sets the left padding to the specified number or function and returns
        this treemap layout. If :code:`padding_left` is a function, it is
        invoked for each node with children, being passed the current node. The
        left padding is used to separate the left edge of a node from its
        children.

        Parameters
        ----------
        padding_left : Callable[[Node], float] | float
            Left padding function or constant left padding value

        Returns
        -------
        TreeMap
            Itself
        """
        if callable(padding_left):
            self._padding_left = padding_left
        else:
            self._padding_left = constant(padding_left)
        return self

    def get_round(self) -> bool:
        return self._round

    def get_size(self) -> tuple[float, float]:
        return [self._dx, self._dy]

    def get_tile(self) -> Callable[[Node, float, float, float, float], None]:
        return self._tile

    def get_padding(self) -> Callable[[Node], float] | float:
        return self.get_padding_inner()

    def get_padding_inner(self) -> Callable[[Node], float] | float:
        return self._padding_inner

    def get_padding_outer(self) -> Callable[[Node], float] | float:
        return self.get_padding_top()

    def get_padding_top(self) -> Callable[[Node], float] | float:
        return self._padding_top

    def get_padding_right(self) -> Callable[[Node], float] | float:
        return self._padding_right

    def get_padding_bottom(self) -> Callable[[Node], float] | float:
        return self._padding_bottom

    def get_padding_left(self) -> Callable[[Node], float] | float:
        return self._padding_left


def treemap() -> TreeMap:
    """
    Builds a new treemap layout with default settings.

    Returns
    -------
    TreeMap
        TreeMap object
    """
    return TreeMap()
