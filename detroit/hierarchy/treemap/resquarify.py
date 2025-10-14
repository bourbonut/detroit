from collections.abc import Iterator
from typing import TypeVar

from ..hierarchy import Node
from .dice import dice
from .slice import slice
from .squarify import PHI, squarify_ratio

TResquarify = TypeVar("Resquarify", bound="Resquarify")


class SquarifyList:
    def __init__(self, values: list[Node]):
        self._values = values
        self.ratio = None

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[Node]:
        return iter(self._values)

    def __setitem__(self, index: int, value: Node):
        self._values[index] = value

    def __getitem__(self, index: int) -> Node:
        return self._values[index]


class Resquarify:
    """
    Resquarify object

    Parameters
    ----------
    ratio : float
        Ratio value
    """
    def __init__(self, ratio: float):
        self._ratio = ratio

    def __call__(self, parent: Node, x0: float, y0: float, x1: float, y1: float):
        """
        Like :func:`d3.treemap_resquarify <detroit.resquarify>`, except
        preserves the topology (node adjacencies) of the previous layout
        computed by this function, if there is one and it used the same target
        aspect ratio. This tiling method is good for animating changes to
        treemaps because it only changes node sizes and not their relative
        positions, thus avoiding distracting shuffling and occlusion. The
        downside of a stable update, however, is a suboptimal layout for
        subsequent updates: only the first layout uses the Bruls et al.
        squarified algorithm.

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
        rows = parent._squarify if hasattr(parent, "_squarify") else None
        if rows and rows.ratio == self._ratio:
            j = 0
            m = len(rows)
            value = parent.value

            while j < m:
                row = rows[j]
                nodes = row.children
                row.value = sum((node.value for node in nodes))
                if row.dice:
                    if value:
                        y = y0 + (y1 - y0) * row.value / value
                        dice(row, x0, y0, x1, y)
                        y0 = y
                    else:
                        dice(row, x0, y0, x1, y1)
                else:
                    if value:
                        x = x0 + (x1 - x0) * row.value / value
                        slice(row, x0, y0, x, y1)
                        x0 = x
                    else:
                        slice(row, x0, y0, x1, y1)
                value -= row.value
                j += 1
        else:
            parent._squarify = rows = SquarifyList(
                squarify_ratio(self._ratio, parent, x0, y0, x1, y1)
            )
            rows.ratio = self._ratio

    def set_ratio(self, ratio: float) -> TResquarify:
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
        Resquarify
            New Resquarify object
        """
        return Resquarify(ratio if ratio > 1 else 1)


resquarify = Resquarify(PHI)
