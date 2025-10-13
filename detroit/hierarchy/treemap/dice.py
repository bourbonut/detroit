from ..hierarchy import Node


def dice(parent: Node, x0: float, y0: float, x1: float, y1: float):
    nodes = parent.children
    k = 0 if parent.value is None or parent.value == 0 else (x1 - x0) / parent.value

    for node in nodes:
        node.y0 = y0
        node.y1 = y1
        node.x0 = x0
        x0 += node.value * k
        node.x1 = x0
