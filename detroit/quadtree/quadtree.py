from collections.abc import Callable
from copy import deepcopy
from math import floor, inf, isnan, nan, sqrt
from typing import Generic, TypeVar

from ..array import argpass
from ..types import Accessor, Point2D, T
from .add import add
from .quad import Quad

TQuadtree = TypeVar("Quadtree", bound="Quadtree")


def default_x(d: Point2D) -> float:
    return d[0]


def default_y(d: Point2D) -> float:
    return d[1]


class Quadtree(Generic[T]):
    """
    A quadtree recursively partitions two-dimensional space into squares,
    dividing each square into four equally-sized squares. Each distinct point
    exists in a unique leaf node; coincident points are represented by a linked
    list. Quadtrees can accelerate various spatial operations, such as the
    `Barnes–Hut approximation
    <https://en.wikipedia.org/wiki/Barnes%E2%80%93Hut_simulation>`_ for
    computing many-body forces, collision detection, and searching for nearby
    points.

    Parameters
    ----------
    x : Accessor[T, float]
        X accessor
    y : Accessor[T, float]
        Y accessor
    x0 : float
        Inclusive lower bound :math:`x_0`
    y0 : float
        Inclusive lower bound :math:`y_0`
    x1 : float
        Inclusive upper bound :math:`x_1`
    y1 : float
        Inclusive upper bound :math:`y_1`
    """
    def __init__(
        self,
        x: Accessor[T, float],
        y: Accessor[T, float],
        x0: float,
        y0: float,
        x1: float,
        y1: float,
    ):
        self._x = argpass(x)
        self._y = argpass(y)
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1
        self._root = None

    def x(self, x: Accessor[T, float]) -> TQuadtree:
        """
        Sets the x-coordinate accessor and returns the quadtree.
        The x accessor is used to derive the x coordinate of data when adding
        to and removing from the tree. It is also used when finding to
        re-access the coordinates of data previously added to the tree;
        therefore, the x and y accessors must be consistent, returning the same
        value given the same input.

        Parameters
        ----------
        x : Accessor[T, float]
            X accessor

        Returns
        -------
        TQuadtree
            Itself
        """
        self._x = argpass(x)
        return self

    def y(self, y: Accessor[T, float]) -> TQuadtree:
        """
        Sets the y-coordinate accessor and returns the quadtree.
        The y accessor is used to derive the y coordinate of data when adding
        to and removing from the tree. It is also used when finding to
        re-access the coordinates of data previously added to the tree;
        therefore, the x and y accessors must be consistent, returning the same
        value given the same input.

        Parameters
        ----------
        y : Accessor[T, float]
            Y accessor

        Returns
        -------
        TQuadtree
            Itself
        """
        self._y = argpass(y)
        return self

    def add(self, d: T) -> TQuadtree:
        """
        Adds the specified datum to the quadtree, deriving its coordinates
        :math:`(x, y)` using the current x and y accessors, and returns the
        quadtree.

        If the new point is outside the current extent of the quadtree, the
        quadtree is automatically expanded to cover the new point.

        Parameters
        ----------
        d : T
            Datum

        Returns
        -------
        TQuadtree
            Itself
        """
        x = self._x(d)
        y = self._y(d)
        return add(self.cover(x, y), x, y, d)

    def add_all(self, data: list[T]) -> TQuadtree:
        """
        Adds the specified iterable of data to the quadtree, deriving each
        element’s coordinates :math:`(x, y)` using the current x and y
        accessors, and return this quadtree.


        Parameters
        ----------
        data : list[T]
            List of data values

        Returns
        -------
        TQuadtree
            Itself
        """
        data = list(data)
        n = len(data)
        xz = [None] * n
        yz = [None] * n
        x0 = inf
        y0 = x0
        x1 = -x0
        y1 = x1

        for i in range(n):
            d = data[i]
            x = self._x(d)
            y = self._y(d)
            if isnan(x) or isnan(y):
                continue
            xz[i] = x
            yz[i] = y
            if x < x0:
                x0 = x
            if x > x1:
                x1 = x
            if y < y0:
                y0 = y
            if y > y1:
                y1 = y

        if x0 > x1 or y0 > y1:
            return self

        self.cover(x0, y0).cover(x1, y1)

        for i in range(n):
            add(self, xz[i], yz[i], data[i])

        return self

    def cover(self, x: float, y: float) -> TQuadtree:
        """
        Expands the quadtree to cover the specified point :math:`(x, y)`, and
        returns the quadtree.

        Parameters
        ----------
        x : float
            X value
        y : float
            Y value

        Returns
        -------
        TQuadtree
            Itself
        """
        if isnan(x) or isnan(y):
            return self

        x0 = self._x0
        y0 = self._y0
        x1 = self._x1
        y1 = self._y1

        if isnan(x0):
            x0 = floor(x)
            y0 = floor(y)
            x1 = x0 + 1
            y1 = y0 + 1
        else:
            z = (x1 - x0) or 1
            node = self._root

            while x0 > x or x >= x1 or y0 > y or y >= y1:
                i = (y < y0) << 1 | (x < x0)
                parent = [None] * 4
                parent[i] = node
                node = parent
                z *= 2
                match i:
                    case 0:
                        x1 = x0 + z
                        y1 = y0 + z
                    case 1:
                        x0 = x1 - z
                        y1 = y0 + z
                    case 2:
                        x1 = x0 + z
                        y0 = y1 - z
                    case 3:
                        x0 = x1 - z
                        y0 = y1 - z

            if self._root and isinstance(self._root, list):
                self._root = node

        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1
        return self

    def set_extent(
        self, extent: list[tuple[float, float], tuple[float, float]]
    ) -> TQuadtree:
        """
        Expands the quadtree to cover the specified points :code:`[[x0, y0],
        [x1, y1]]` and returns the quadtree.

        Parameters
        ----------
        extent : list[tuple[float, float], tuple[float, float]]
            Extent values

        Returns
        -------
        TQuadtree
            Itself
        """
        return self.cover(extent[0][0], extent[0][1]).cover(extent[1][0], extent[1][1])

    def data(self) -> list[T]:
        """
        Returns an array of all data in the quadtree.

        Returns
        -------
        list[T]
            List of all data
        """
        data = []

        def visit(node):
            if isinstance(node, list):
                return
            while True:
                data.append(node["data"])
                node = node.get("next")
                if node is None:
                    break

        self.visit(visit)
        return data

    def find(self, x: float, y: float, radius: float | None = None) -> TQuadtree:
        """
        Returns the datum closest to the position :math:`(x, y)` with the given
        search radius. If radius is not specified, it defaults to infinity.

        Parameters
        ----------
        x : float
            x value
        y : float
            y value
        radius : float | None
            radius value

        Returns
        -------
        TQuadtree
            Itself
        """
        x0 = self._x0
        y0 = self._y0
        x3 = self._x1
        y3 = self._y1
        quads = []
        data = None
        node = self._root

        if node:
            quads.append(Quad(node, x0, y0, x3, y3))
        if radius is None:
            radius = inf
        else:
            x0 = x - radius
            y0 = y - radius
            x3 = x + radius
            y3 = y + radius
            radius *= radius

        while len(quads):
            q = quads.pop()
            node = q.node
            x1 = q.x0
            y1 = q.y0
            x2 = q.x1
            y2 = q.y1
            if not node or x1 > x3 or y1 > y3 or x2 < x0 or y2 < y0:
                continue

            if isinstance(node, list):
                xm = (x1 + x2) * 0.5
                ym = (y1 + y2) * 0.5

                quads.extend(
                    (
                        Quad(node[3], xm, ym, x2, y2),
                        Quad(node[2], x1, ym, xm, y2),
                        Quad(node[1], xm, y1, x2, ym),
                        Quad(node[0], x1, y1, xm, ym),
                    )
                )

                i = (y >= ym) << 1 | (x >= xm)
                if i:
                    q = quads[-1]
                    quads[-1] = quads[-1 - i]
                    quads[-1 - i] = q
            else:
                dx = x - self._x(node["data"])
                dy = y - self._y(node["data"])
                d2 = dx * dx + dy * dy
                if d2 < radius:
                    radius = d2
                    d = sqrt(d2)
                    x0 = x - d
                    y0 = y - d
                    x3 = x + d
                    y3 = y + d
                    data = node["data"]

        return data

    def remove(self, d: T) -> TQuadtree:
        """
        Removes the specified datum from the quadtree, deriving its coordinates
        :math:`(x,y)` using the current x and y accessors, and returns the quadtree.

        Parameters
        ----------
        d : T
            Datum

        Returns
        -------
        TQuadtree
            Itself
        """
        x = self._x(d)
        y = self._y(d)
        if isnan(x) or isnan(y):
            return self

        parent = None
        previous = None
        retainer = None
        node = self._root
        x0 = self._x0
        y0 = self._y0
        x1 = self._x1
        y1 = self._y1

        if node is None:
            return self

        if isinstance(node, list):
            while True:
                xm = (x0 + x1) * 0.5
                right = x >= xm
                if right:
                    x0 = xm
                else:
                    x1 = xm

                ym = (y0 + y1) * 0.5
                bottom = y >= ym
                if bottom:
                    y0 = ym
                else:
                    y1 = ym

                parent = node
                i = bottom << 1 | right
                node = node[i]
                if node is None:
                    return self
                if isinstance(node, dict):
                    break
                if parent[(i + 1) & 3] or parent[(i + 2) & 3] or parent[(i + 3) & 3]:
                    retainer = parent
                    j = i

        while node["data"] is not d:
            previous = node
            node = node.get("next")
            if node is None:
                return self
        next = node.pop("next", None)

        if previous:
            if next:
                previous["next"] = next
            else:
                previous.pop("next")
            return self

        if parent is None:
            self._root = next
            return self

        parent[i] = next

        node = parent[0] or parent[1] or parent[2] or parent[3]
        if node == (parent[3] or parent[2] or parent[1] or parent[0]) and isinstance(
            node, dict
        ):
            if retainer:
                retainer[j] = node
            else:
                self._root = node

        return self

    def remove_all(self, data: list[T]) -> TQuadtree:
        """
        Removes the specified data from the quadtree, deriving their
        coordinates :math:`(x,y)` using the current x and y accessors, and
        returns the quadtree.

        Parameters
        ----------
        data : list[T]
            List of data

        Returns
        -------
        TQuadtree
            Itself
        """
        for d in data:
            self.remove(d)
        return self

    def visit(
        self, callback: Callable[[list | dict | None, float, float, float, float], bool]
    ) -> TQuadtree:
        """
        Visits each node in the quadtree in pre-order traversal, invoking the
        specified callback with arguments :code:`node`, :code:`x0`, :code:`y0`,
        :code:`x1`, :code:`y1` for each node, where node is the node being
        visited, :math:`(x_0, y_0)` are the lower bounds of the node, and
        :math:`(x_1, y_1)` are the upper bounds, and returns the quadtree.
        (Assuming that positive x is right and positive y is down, as is
        typically the case in Canvas and SVG, :math:`(x_0, y_0)` is the
        top-left corner and :math:`(x_1, y_1)` is the lower-right corner;
        however, the coordinate system is arbitrary, so more formally
        :math:`x_0 \\le x_1` and :math:`y0 \\le y1`.)

        If the callback returns true for a given node, then the children of
        that node are not visited; otherwise, all child nodes are visited. This
        can be used to quickly visit only parts of the tree, for example when
        using the `Barnes–Hut approximation
        <https://en.wikipedia.org/wiki/Barnes%E2%80%93Hut_simulation>`_. Note,
        however, that child quadrants are always visited in sibling order:
        top-left, top-right, bottom-left, bottom-right. In cases such as
        search, visiting siblings in a specific order may be faster.

        Parameters
        ----------
        callback : Callable[[list | dict | None, float, float, float, float], bool]
            Callback function

        Returns
        -------
        TQuadtree
            Itself

        Notes
        -----
        The number of arguments for the :code:`callback` function is
        automatically determined. Therefore, you can pass 0 to 5 arguments to
        the :code:`callback` function. For example, `def callback(node):` is a
        valid function.
        """
        callback = argpass(callback)
        quads = []
        node = self._root
        if node:
            quads.append(Quad(node, self._x0, self._y0, self._x1, self._y1))
        while quads:
            q = quads.pop()
            node = q.node
            x0 = q.x0
            y0 = q.y0
            x1 = q.x1
            y1 = q.y1
            if not callback(node, x0, y0, x1, y1) and isinstance(node, list):
                xm = (x0 + x1) * 0.5
                ym = (y0 + y1) * 0.5
                child = node[3]
                if child:
                    quads.append(Quad(child, xm, ym, x1, y1))
                child = node[2]
                if child:
                    quads.append(Quad(child, x0, ym, xm, y1))
                child = node[1]
                if child:
                    quads.append(Quad(child, xm, y0, x1, ym))
                child = node[0]
                if child:
                    quads.append(Quad(child, x0, y0, xm, ym))
        return self

    def visit_after(
        self, callback: Callable[[dict, float, float, float, float], bool]
    ) -> TQuadtree:
        """
        Visits each node in the quadtree in post-order traversal, invoking the
        specified callback with arguments :code:`node`, :code:`x0`, :code:`y0`,
        :code:`x1`, :code:`y1` for each node, where node is the node being
        visited, :code:`(x_0, y_0)` are the lower bounds of the node, and
        :code:`(x_1, y_1)` are the upper bounds, and returns the quadtree.
        (Assuming that positive :code:`x` is right and positive :code:`y` is
        down, as is typically the case in Canvas and SVG, :code:`(x_0, y_0)` is
        the top-left corner and :code:`(x_1, y_1)` is the lower-right corner;
        however, the coordinate system is arbitrary, so more formally
        :math:`x_0 \\lt x_1` and :math:`y0 \\lt y1`.). Returns root.

        Parameters
        ----------
        callback : Callable[[dict, float, float, float, float], bool]
            Callback function

        Returns
        -------
        TQuadtree
            Itself

        Notes
        -----
        The number of arguments for the :code:`callback` function is
        automatically determined. Therefore, you can pass 0 to 5 arguments to
        the :code:`callback` function. For example, `def callback(node):` is a
        valid function.
        """
        callback = argpass(callback)
        quads = []
        next = []
        if self._root:
            quads.append(Quad(self._root, self._x0, self._y0, self._x1, self._y1))
        while quads:
            q = quads.pop()
            node = q.node
            if isinstance(node, list):
                x0 = q.x0
                y0 = q.y0
                x1 = q.x1
                y1 = q.y1
                xm = (x0 + x1) * 0.5
                ym = (y0 + y1) * 0.5
                child = node[0]
                if child:
                    quads.append(Quad(child, x0, y0, xm, ym))
                child = node[1]
                if child:
                    quads.append(Quad(child, xm, y0, x1, ym))
                child = node[2]
                if child:
                    quads.append(Quad(child, x0, ym, xm, y1))
                child = node[3]
                if child:
                    quads.append(Quad(child, xm, ym, x1, y1))
            next.append(q)
        while len(next) != 0:
            q = next.pop()
            callback(q.node, q.x0, q.y0, q.x1, q.y1)
        return self

    def copy(self) -> TQuadtree:
        """
        Returns a deep copy of itself.

        Returns
        -------
        TQuadtree
            Deep copy of itself
        """
        return deepcopy(self)

    def size(self) -> float:
        """
        Returns the total number of data in the quadtree.

        Returns
        -------
        float
            Total number of data in sthe quadtree.
        """
        size = [0]

        def visit(node: list | dict | None):
            if isinstance(node, list):
                return
            while True:
                size[0] += 1
                node = node.get("next")
                if node is None:
                    break

        self.visit(visit)
        return size[0]

    def get_extent(self) -> list[tuple[float, float], tuple[float, float]]:
        if isnan(self._x0):
            return None
        return [[self._x0, self._y0], [self._x1, self._y1]]

    def get_root(self) -> list | dict | None:
        return self._root

    def get_x(self) -> Accessor[T, float]:
        return self._x

    def get_y(self) -> Accessor[T, float]:
        return self._y


def quadtree(
    data: list[T] | None = None,
    x: Accessor[T, float] = None,
    y: Accessor[T, float] = None,
) -> Quadtree[T]:
    """
    Creates a new, empty quadtree with an empty extent and the default x and y
    accessors. If data is specified, adds the specified iterable of data to the
    quadtree.

    Parameters
    ----------
    data : list[T] | None
        List of data values
    x : Accessor[T, float]
        X accessor
    y : Accessor[T, float]
        Y accessor

    Returns
    -------
    Quadtree[T]
        Quadtree object
    """
    tree = Quadtree(
        default_x if x is None else x, default_y if y is None else y, nan, nan, nan, nan
    )
    return tree if data is None else tree.add_all(data)
