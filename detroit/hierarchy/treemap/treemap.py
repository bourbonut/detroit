from collections.abc import Callable
from typing import TypeVar

from ..accessors import required
from ..constant import constant, constant_zero
from ..hierarchy import Node
from .round import round_node
from .squarify import squarify

TTreeMap = TypeVar("TreeMap", bound="TreeMap")


class TreeMap:
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
        self._round = round_value
        return self

    def set_size(self, size: tuple[float, float]) -> TTreeMap:
        self._dx = size[0]
        self._dy = size[1]
        return self

    def set_tile(
        self, tile: Callable[[Node, float, float, float, float], None]
    ) -> TTreeMap:
        self._tile = required(tile)
        return self

    def set_padding(self, padding: Callable[[Node], float] | float) -> TTreeMap:
        return self.set_padding_inner(padding).set_padding_outer(padding)

    def set_padding_inner(
        self, padding_inner: Callable[[Node], float] | float
    ) -> TTreeMap:
        if callable(padding_inner):
            self._padding_inner = padding_inner
        else:
            self._padding_inner = constant(padding_inner)
        return self

    def set_padding_outer(
        self, padding_outer: Callable[[Node], float] | float
    ) -> TTreeMap:
        return (
            self.set_padding_top(padding_outer)
            .set_padding_right(padding_outer)
            .set_padding_bottom(padding_outer)
            .set_padding_left(padding_outer)
        )

    def set_padding_top(self, padding_top: Callable[[Node], float] | float) -> TTreeMap:
        if callable(padding_top):
            self._padding_top = padding_top
        else:
            self._padding_top = constant(padding_top)
        return self

    def set_padding_right(
        self, padding_right: Callable[[Node], float] | float
    ) -> TTreeMap:
        if callable(padding_right):
            self._padding_right = padding_right
        else:
            self._padding_right = constant(padding_right)
        return self

    def set_padding_bottom(
        self, padding_bottom: Callable[[Node], float] | float
    ) -> TTreeMap:
        if callable(padding_bottom):
            self._padding_bottom = padding_bottom
        else:
            self._padding_bottom = constant(padding_bottom)
        return self

    def set_padding_left(
        self, padding_left: Callable[[Node], float] | float
    ) -> TTreeMap:
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
    return TreeMap()
