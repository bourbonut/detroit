from ..hierarchy import Node


def slice(parent: Node, x0: float, y0: float, x1: float, y1: float):
    """
    Divides the rectangular area specified by :math:`x_0:, :math:`y_0`,
    :math:`x_1`, :math:`y_1` vertically according the value of each of the
    specified node's children. The children are positioned in order, starting
    with the top edge (:math:`y_0`) of the given rectangle. If the sum of the
    children’s values is less than the specified node’s value (i.e., if the
    specified node has a non-zero internal value), the remaining empty space
    will be positioned on the bottom edge (:math:`y_1`) of the given rectangle.

    Parameters
    ----------
    parent : Node
        Parent node
    x0 : float
        X-coordinate top edge
    y0 : float
        Y-coordinate top edge
    x1 : float
        X-coordinate bottom edge
    y1 : float
        Y-coordinate bottom edge
    """
    nodes = parent.children
    k = 0 if parent.value is None or parent.value == 0 else (y1 - y0) / parent.value

    for node in nodes:
        node.x0 = x0
        node.x1 = x1
        node.y0 = y0
        y0 += node.value * k
        node.y1 = y0
