from collections.abc import Callable
from typing import TypeVar

from .hierarchy import Node
from .treemap.dice import dice
from .treemap.round import round_node

TPartition = TypeVar("Partition", bound="Partition")


class Partition:
    """
    Partition layout
    """
    def __init__(self):
        self._dx = 1
        self._dy = 1
        self._padding = 0
        self._round = False

    def __call__(self, root: Node) -> Node:
        """
        Lays out the specified root hierarchy, assigning the following
        properties on root and its descendants:

        * :code:`node.x0` - the left edge of the rectangle
        * :code:`node.y0` - the top edge of the rectangle
        * :code:`node.x1` - the right edge of the rectangle
        * :code:`node.y1` - the bottom edge of the rectangle

        You must call :code:`root.sum` before passing the hierarchy to the
        partition layout. You probably also want to call root.sort to order the
        hierarchy before computing the layout.

        Parameters
        ----------
        root : Node
            Root node

        Returns
        -------
        Node
            Node organized as partition
        """
        n = root.height + 1
        root.x0 = self._padding
        root.y0 = self._padding
        root.x1 = self._dx
        root.y1 = self._dy / n
        root.each_before(self._position_node(self._dy, n))
        if self._round:
            root.each_before(round_node)
        return root

    def _position_node(self, dy: float, n: int) -> Callable[[Node], None]:
        def local_function(node):
            if node.children:
                dice(
                    node,
                    node.x0,
                    dy * (node.depth + 1) / n,
                    node.x1,
                    dy * (node.depth + 2) / n,
                )
            x0 = node.x0
            y0 = node.y0
            x1 = node.x1 - self._padding
            y1 = node.y1 - self._padding
            if x1 < x0:
                x0 = x1 = (x0 + x1) * 0.5
            if y1 < y0:
                y0 = y1 = (y0 + y1) * 0.5
            node.x0 = x0
            node.y0 = y0
            node.x1 = x1
            node.y1 = y1

        return local_function

    def set_round(self, round: bool) -> TPartition:
        """
        Enables or disables rounding according to the given boolean and returns
        this partition layout.

        Parameters
        ----------
        round : bool
            Round boolean value

        Returns
        -------
        Partition
            Itself
        """
        self._round = round
        return self

    def set_size(self, size: tuple[float, float]) -> TPartition:
        """
        Sets this partition layout’s size to the specified two-element array of
        numbers :code:`[width, height]` and returns this partition layout.

        Parameters
        ----------
        size : tuple[float, float]
            Size values

        Returns
        -------
        Partition
            Itself
        """
        self._dx = size[0]
        self._dy = size[1]
        return self

    def set_padding(self, padding: float) -> TPartition:
        """
        Sets the padding to the specified number and returns this partition
        layout.

        Parameters
        ----------
        padding : float
            Padding value

        Returns
        -------
        Partition
            Itself
        """
        self._padding = padding
        return self

    def get_round(self) -> bool:
        return self._round

    def get_size(self) -> tuple[float, float]:
        return [self._dx, self._dy]

    def get_padding(self) -> float:
        return self._padding


def partition() -> Partition:
    """
    Builds a new partition layout with the default settings.

    Returns
    -------
    Partition
        Partition object
    """
    return Partition()
