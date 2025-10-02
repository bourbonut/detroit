import detroit as d3
from detroit.hierarchy import Node

def init_node(values):
    node = Node(None)
    node.value = values.get("value")
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

def test_binary_1():
    tile = d3.treemap_binary
    root = init_node(
        {
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
        {"x0": 0.00, "x1": 3.00, "y0": 0.00, "y1": 2.00},
        {"x0": 0.00, "x1": 3.00, "y0": 2.00, "y1": 4.00},
        {"x0": 3.00, "x1": 4.71, "y0": 0.00, "y1": 2.33},
        {"x0": 4.71, "x1": 6.00, "y0": 0.00, "y1": 2.33},
        {"x0": 3.00, "x1": 4.20, "y0": 2.33, "y1": 4.00},
        {"x0": 4.20, "x1": 5.40, "y0": 2.33, "y1": 4.00},
        {"x0": 5.40, "x1": 6.00, "y0": 2.33, "y1": 4.00}
    ]

def test_binary_2():
    data = {"children": [{"value": 0}, {"value": 0}, {"value": 1}]}
    root = d3.hierarchy(data).sum(lambda d: d.get("value"))
    treemapper = d3.treemap().set_tile(d3.treemap_binary)
    treemapper(root)
    a = [[d.x0, d.x1, d.y0, d.y1] for d in root.leaves()]
    assert a == [[0, 1, 0, 0], [1, 1, 0, 0], [0, 1, 0, 1]]
