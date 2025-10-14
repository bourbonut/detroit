from ..hierarchy import Node


def dice(parent: Node, x0: float, y0: float, x1: float, y1: float):
    """
    Divides the rectangular area specified by :math:`x_0:, :math:`y_0`,
    :math:`x_1`, :math:`y_1` horizontally according the value of each of the
    specified node's children. The children are positioned in order, starting
    with the left edge (:math:`x_0`) of the given rectangle. If the sum of the
    children's values is less than the specified node's value (i.e., if the
    specified node has a non-zero internal value), the remaining empty space
    will be positioned on the right edge (:math:`x_1`) of the given rectangle.

    Parameters
    ----------
    parent : Node
        Parent node
    x0 : float
        X-coordinate left edge
    y0 : float
        Y-coordinate left edge
    x1 : float
        X-coordinate right edge
    y1 : float
        Y-coordinate right edge
    """
    nodes = parent.children
    k = 0 if parent.value is None or parent.value == 0 else (x1 - x0) / parent.value

    for node in nodes:
        node.y0 = y0
        node.y1 = y1
        node.x0 = x0
        x0 += node.value * k
        node.x1 = x0
