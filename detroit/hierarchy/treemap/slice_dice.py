from ..hierarchy import Node
from .dice import dice
from .slice import slice


def slice_dice(parent: Node, x0: float, y0: float, x1: float, y1: float):
    """
    If the specified :code:`parent` has odd depth, delegates to
    :func:`d3.treemap_slice <detroit.treemap_slice>`; otherwise delegates to
    :func:`d3.treemap_dice <detroit.treemap_dice>`.

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
    if parent.depth & 1:
        slice(parent, x0, y0, x1, y1)
    else:
        dice(parent, x0, y0, x1, y1)
