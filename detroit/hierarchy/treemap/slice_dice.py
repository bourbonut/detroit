from ..hierarchy import Node
from .dice import dice
from .slice import slice


def slice_dice(parent: Node, x0: float, y0: float, x1: float, y1: float):
    if parent.depth & 1:
        slice(parent, x0, y0, x1, y1)
    else:
        dice(parent, x0, y0, x1, y1)
