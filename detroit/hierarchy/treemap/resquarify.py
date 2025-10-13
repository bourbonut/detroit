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
    def __init__(self, ratio: float):
        self._ratio = ratio

    def __call__(self, parent: Node, x0: float, y0: float, x1: float, y1: float):
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
        return Resquarify(ratio if ratio > 1 else 1)


resquarify = Resquarify(PHI)
