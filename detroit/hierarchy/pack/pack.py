from collections.abc import Callable
from math import sqrt
from typing import TypeVar

from ..accessors import optional
from ..constant import constant, constant_zero
from ..hierarchy import Node
from .siblings import pack_siblings_random

TPack = TypeVar("Pack", bound="Pack")


def default_radius(d: Node) -> float:
    return sqrt(d.value)


class Pack:
    """
    Pack layout
    """
    def __init__(self):
        self._radius = None
        self._dx = 1
        self._dy = 1
        self._padding = constant_zero

    def __call__(self, root: Node) -> Node:
        """
        Lays out the specified root hierarchy, assigning the following
        properties on root and its descendants:

        * :code:`node.x` - the x-coordinate of the circle’s center
        * :code:`node.y` - the y coordinate of the circle’s center
        * :code:`node.r` - the radius of the circle

        You must call root.sum before passing the hierarchy to the pack layout.
        You probably also want to call root.sort to order the hierarchy before
        computing the layout.


        Parameters
        ----------
        root : Node
            Root node

        Returns
        -------
        Node
            Node organized as pack
        """
        root.x = self._dx * 0.5
        root.y = self._dy * 0.5
        if self._radius:
            (
                root.each_before(radius_leaf(self._radius))
                .each_after(pack_children_random(self._padding, 0.5))
                .each_before(translate_child(1))
            )
        else:
            (
                root.each_before(radius_leaf(default_radius))
                .each_after(pack_children_random(constant_zero, 1))
                .each_after(
                    pack_children_random(
                        self._padding, root.r / min(self._dx, self._dy)
                    )
                )
                .each_before(translate_child(min(self._dx, self._dy) / (2 * root.r)))
            )
        return root

    def set_radius(self, radius: Callable[[Node], float] | None) -> TPack:
        """
        Sets the pack layout's radius accessor to the specified function and
        returns this pack layout. If :code:`radius` is not specified, returns
        the current radius accessor, which defaults to :code:`None`. If the
        radius accessor is :code:`None`, the radius of each leaf circle is
        derived from the leaf :code:`node.value` (computed by
        :code:`node.sum`); the radii are then scaled proportionally to fit the
        layout size. If the :code:`radius` accessor is not :code:`None`, the
        radius of each leaf circle is specified exactly by the function.

        Parameters
        ----------
        radius : Callable[[Node], float] | None
            Radius function or :code:`None` value

        Returns
        -------
        Pack
            Itself
        """
        self._radius = optional(radius)
        return self

    def set_size(self, size: tuple[float, float]) -> TPack:
        """
        Sets this pack layout's size to the specified two-element array of
        numbers :code:`[width, height]` and returns this pack layout.

        Parameters
        ----------
        size : tuple[float, float]
            Size values

        Returns
        -------
        Pack
            Itself
        """
        self._dx = size[0]
        self._dy = size[1]
        return self

    def set_padding(self, padding: Callable[[Node], float] | float) -> TPack:
        """
        If :code:`padding` is specified, sets this pack layout's padding
        accessor to the specified number or function and returns this pack
        layout. When siblings are packed, tangent siblings will be separated by
        approximately the specified padding; the enclosing parent circle will
        also be separated from its children by approximately the specified
        padding. If an explicit radius is not specified, the padding is
        approximate because a two-pass algorithm is needed to fit within the
        layout size: the circles are first packed without padding; a scaling
        factor is computed and applied to the specified padding; and lastly the
        circles are re-packed with padding.

        Parameters
        ----------
        padding : Callable[[Node], float] | float
            Padding function or constant padding value

        Returns
        -------
        Pack
            Itself
        """
        if callable(padding):
            self._padding = padding
        else:
            self._padding = constant(padding)
        return self

    def get_radius(self) -> Callable[[Node], None] | None:
        return self._radius

    def get_size(self) -> tuple[float, float]:
        return [self._dx, self._dy]

    def get_padding(self) -> Callable[[Node], None]:
        return self._padding


def radius_leaf(radius: Callable[[Node], float] | None) -> Callable[[Node], None]:
    def leaf(node: Node):
        if node.children is None:
            node.r = max(0, 0 if radius is None else radius(node))

    return leaf


def pack_children_random(
    padding: Callable[[Node], float], k: float
) -> Callable[[Node], None]:
    def pack_children(node: Node):
        if children := node.children:
            r = padding(node) * k
            if r:
                for child in children:
                    child.r += r
            e = pack_siblings_random(children)
            if r:
                for child in children:
                    child.r -= r
            node.r = e + r

    return pack_children


def translate_child(k: float) -> Callable[[Node], None]:
    def translate(node: Node):
        parent = node.parent
        node.r *= k
        if parent is not None:
            node.x = parent.x + k * node.x
            node.y = parent.y + k * node.y

    return translate


def pack() -> Pack:
    return Pack()
