import detroit as d3
from detroit.hierarchy import Node

def init_node(values):
    node = Node(None)
    node.value = values.get("value")
    node.depth = values.get("depth")
    if children := values.get("children"):
        node.children = [init_node(child) for child in children]
    return node

def special_round(d):
    return {
        "x0": round(d.x0 * 100) / 100,
        "y0": round(d.y0 * 100) / 100,
        "x1": round(d.x1 * 100) / 100,
        "y1": round(d.y1 * 100) / 100,
    }

def test_treemap_slice_dice_1():
    tile = d3.treemap_slice_dice
    root = init_node(
        {
            "depth": 1,
            "value": 24,
            "children": [
                {"value": 6},
                {"value": 6},
                {"value": 4},
                {"value": 3},
                {"value": 2},
                {"value": 2},
                {"value": 1}
            ]
        }
    )
    tile(root, 0, 0, 6, 4)
    assert list(map(special_round, root.children)) == [
        {"x0": 0.00, "x1": 6.00, "y0": 0.00, "y1": 1.00},
        {"x0": 0.00, "x1": 6.00, "y0": 1.00, "y1": 2.00},
        {"x0": 0.00, "x1": 6.00, "y0": 2.00, "y1": 2.67},
        {"x0": 0.00, "x1": 6.00, "y0": 2.67, "y1": 3.17},
        {"x0": 0.00, "x1": 6.00, "y0": 3.17, "y1": 3.50},
        {"x0": 0.00, "x1": 6.00, "y0": 3.50, "y1": 3.83},
        {"x0": 0.00, "x1": 6.00, "y0": 3.83, "y1": 4.00}
    ]

def test_treemap_slice_dice_2():
    tile = d3.treemap_slice_dice
    root = init_node(
        {
            "depth": 2,
            "value": 24,
            "children": [
                {"value": 6},
                {"value": 6},
                {"value": 4},
                {"value": 3},
                {"value": 2},
                {"value": 2},
                {"value": 1}
            ]
        }
    )
    tile(root, 0, 0, 4, 6)
    assert list(map(special_round, root.children)) == [
        {"x0": 0.00, "x1": 1.00, "y0": 0.00, "y1": 6.00},
        {"x0": 1.00, "x1": 2.00, "y0": 0.00, "y1": 6.00},
        {"x0": 2.00, "x1": 2.67, "y0": 0.00, "y1": 6.00},
        {"x0": 2.67, "x1": 3.17, "y0": 0.00, "y1": 6.00},
        {"x0": 3.17, "x1": 3.50, "y0": 0.00, "y1": 6.00},
        {"x0": 3.50, "x1": 3.83, "y0": 0.00, "y1": 6.00},
        {"x0": 3.83, "x1": 4.00, "y0": 0.00, "y1": 6.00}
    ]
