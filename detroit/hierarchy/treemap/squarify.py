from math import sqrt
from typing import TypeVar

from ..hierarchy import Node
from .dice import dice
from .slice import slice

TSquarify = TypeVar("Squarify", bound="Squarify")

PHI = (1 + sqrt(5)) * 0.5


def squarify_ratio(
    ratio: float, parent: Node, x0: float, y0: float, x1: float, y1: float
) -> list[Node]:
    rows = []
    nodes = parent.children
    i0 = 0
    i1 = 0
    n = len(nodes)
    value = parent.value

    while i0 < n:
        dx = x1 - x0
        dy = y1 - y0

        while True:
            sum_value = nodes[i1].value
            i1 += 1
            if sum_value or i1 >= n:
                break

        min_value = max_value = sum_value
        alpha = 0
        if value != 0 and dx != 0 and dy != 0:
            alpha = max(dy / dx, dx / dy) / (value * ratio)
        beta = sum_value * sum_value * alpha
        min_ratio = 0
        if beta != 0:
            min_ratio = max(max_value / beta, beta / min_value)

        while i1 < n:
            node_value = nodes[i1].value
            sum_value += node_value
            if node_value < min_value:
                min_value = node_value
            if node_value > max_value:
                max_value = node_value
            beta = sum_value * sum_value * alpha
            new_ratio = 0
            if beta != 0:
                new_ratio = max(max_value / beta, beta / min_value)
            if new_ratio > min_ratio:
                sum_value -= node_value
                break
            min_ratio = new_ratio
            i1 += 1

        row = Node(None)
        row.value = sum_value
        row.dice = dx < dy
        row.children = nodes[i0:i1]
        rows.append(row)
        if row.dice:
            if value:
                y = y0 + dy * sum_value / value
                dice(row, x0, y0, x1, y)
                y0 = y
            else:
                dice(row, x0, y0, x1, y1)
        else:
            if value:
                x = x0 + dx * sum_value / value
                slice(row, x0, y0, x, y1)
                x0 = x
            else:
                slice(row, x0, y0, x1, y1)
        value -= sum_value
        i0 = i1
    return rows


class Squarify:
    """
    Squarify object

    Parameters
    ----------
    ratio : float
        Ratio value
    """
    def __init__(self, ratio: float):
        self._ratio = ratio

    def __call__(self, parent: Node, x0: float, y0: float, x1: float, y1: float):
        """
        Implements the squarified treemap algorithm by Bruls et al., which
        seeks to produce rectangles of a given aspect ratio.

        Parameters
        ----------
        parent : Node
            Parent node
        x0 : float
            X-coordinate rectangular edge
        y0 : float
            Y-coordinate rectangular edge
        x1 : float
            X-coordinate rectangular edge
        y1 : float
            Y-coordinate rectangular edge
        """
        squarify_ratio(self._ratio, parent, x0, y0, x1, y1)

    def set_ratio(self, ratio: float) -> TSquarify:
        """
        Specifies the desired aspect ratio of the generated rectangles. The
        ratio must be specified as a number greater than or equal to one. Note
        that the orientation of the generated rectangles (tall or wide) is not
        implied by the ratio; for example, a ratio of two will attempt to
        produce a mixture of rectangles whose width:height ratio is either
        :code:`2:1` or :code:`1:2`. (However, you can approximately achieve
        this result by generating a square treemap at different dimensions, and
        then stretching the treemap to the desired aspect ratio.) Furthermore,
        the specified ratio is merely a hint to the tiling algorithm; the
        rectangles are not guaranteed to have the specified aspect ratio. If
        not specified, the aspect ratio defaults to the golden ratio,
        :math:`\\phi = (1 + \\sqrt{5}) / 2`, per `Kong et
        al<http://vis.stanford.edu/papers/perception-treemaps>_`.

        Parameters
        ----------
        ratio : float
            Ratio value

        Returns
        -------
        Squarify
            New Squarify object
        """
        return Squarify(ratio if ratio > 1 else 1)


squarify = Squarify(PHI)
