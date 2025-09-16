from math import isnan
from typing import TypeVar

from ..types import Point2D

Quadtree = TypeVar("Quadtree", bound="Quadtree")


def add(tree: Quadtree, x: float, y: float, d: Point2D) -> Quadtree:
    if isnan(x) or isnan(y):
        return tree

    parent = None
    node = tree._root
    leaf = {"data": d}
    x0 = tree._x0
    y0 = tree._y0
    x1 = tree._x1
    y1 = tree._y1

    if not node:
        tree._root = leaf
        return tree

    while isinstance(node, list):
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
            parent[i] = leaf
            return tree

    xp = tree._x(node["data"])
    yp = tree._y(node["data"])
    if x == xp and y == yp:
        leaf["next"] = node
        if parent:
            parent[i] = leaf
        else:
            tree._root = leaf
        return tree

    while True:
        if parent:
            parent[i] = [None] * 4
            parent = parent[i]
        else:
            parent = tree._root = [None] * 4

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

        i = bottom << 1 | right
        j = (yp >= ym) << 1 | (xp >= xm)
        if i != j:
            break

    parent[j] = node
    parent[i] = leaf
    return tree
