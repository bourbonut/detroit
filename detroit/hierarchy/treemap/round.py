from ..hierarchy import Node


def round_node(node: Node):
    node.x0 = round(node.x0)
    node.y0 = round(node.y0)
    node.x1 = round(node.x1)
    node.y1 = round(node.y1)
