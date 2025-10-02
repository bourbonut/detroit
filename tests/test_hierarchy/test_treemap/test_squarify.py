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

def test_squarify_1():
    tile = d3.treemap_squarify
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
        {"x0": 3.00, "x1": 5.40, "y0": 2.33, "y1": 3.17},
        {"x0": 3.00, "x1": 5.40, "y0": 3.17, "y1": 4.00},
        {"x0": 5.40, "x1": 6.00, "y0": 2.33, "y1": 4.00}
    ]

def test_squarify_2():
    tile = d3.treemap_squarify
    root = init_node({"value": 20, "children": [{"value": 10}, {"value": 10}]})
    tile(root, 0, 0, 20, 10)
    assert list(map(special_round, root.children)) == [
        {"x0":  0, "x1": 10, "y0":  0, "y1": 10},
        {"x0": 10, "x1": 20, "y0":  0, "y1": 10}
    ]
    tile(root, 0, 0, 10, 20)
    assert list(map(special_round, root.children)) == [
        {"x0":  0, "x1": 10, "y0":  0, "y1": 10},
        {"x0":  0, "x1": 10, "y0": 10, "y1": 20}
    ]

def test_squarify_3():
    tile = d3.treemap_squarify.set_ratio(1)
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

def test_squarify_4():
    tile = d3.treemap_squarify
    root = init_node({"value": 0, "children": [{"value": 0}, {"value": 0}]})
    tile(root, 0, 0, 0, 4)
    assert list(map(special_round, root.children)) == [
        {"x0": 0.00, "x1": 0.00, "y0": 0.00, "y1": 4.00},
        {"x0": 0.00, "x1": 0.00, "y0": 0.00, "y1": 4.00}
    ]

def test_squarify_5():
    tile = d3.treemap_squarify
    root = init_node({"value": 0, "children": [{"value": 0}, {"value": 0}]})
    tile(root, 0, 0, 4, 0)
    assert list(map(special_round, root.children)) == [
        {"x0": 0.00, "x1": 4.00, "y0": 0.00, "y1": 0.00},
        {"x0": 0.00, "x1": 4.00, "y0": 0.00, "y1": 0.00}
    ]

def test_squarify_6():
    tile = d3.treemap_squarify
    root = init_node(
        {
            "value": 24,
            "children": [
                {"value": 0},
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
        {"x0": 0.00, "x1": 3.00, "y0": 0.00, "y1": 0.00},
        {"x0": 0.00, "x1": 3.00, "y0": 0.00, "y1": 2.00},
        {"x0": 0.00, "x1": 3.00, "y0": 2.00, "y1": 4.00},
        {"x0": 3.00, "x1": 4.71, "y0": 0.00, "y1": 2.33},
        {"x0": 4.71, "x1": 6.00, "y0": 0.00, "y1": 2.33},
        {"x0": 3.00, "x1": 5.40, "y0": 2.33, "y1": 3.17},
        {"x0": 3.00, "x1": 5.40, "y0": 3.17, "y1": 4.00},
        {"x0": 5.40, "x1": 6.00, "y0": 2.33, "y1": 4.00}
    ]
