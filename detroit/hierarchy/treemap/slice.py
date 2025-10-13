from ..hierarchy import Node


def slice(parent: Node, x0: float, y0: float, x1: float, y1: float):
    nodes = parent.children
    k = 0 if parent.value is None or parent.value == 0 else (y1 - y0) / parent.value

    for node in nodes:
        node.x0 = x0
        node.x1 = x1
        node.y0 = y0
        y0 += node.value * k
        node.y1 = y0
