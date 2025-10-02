import detroit as d3
# from detroit.hierarchy import Node
import polars as pl
import json

# def init_node(values):
#     node = Node(None)
#     node.value = values.get("value")
#     node.x0 = values.get("x0")
#     node.y0 = values.get("y0")
#     node.x1 = values.get("x1")
#     node.y1 = values.get("y1")
#     node.id = None
#     node.parent = None
#     node.data = None
#     node._squarify = None
#     node.height = None
#     if children := values.get("children"):
#         node.children = [init_node(child) for child in children]
#     return node

def special_round(d):
    return round(d * 100) / 100

def check(data, expected, tile):
    def parent_id(d):
        parts = d["id"].split(".")
        if len(parts) > 1:
            return ".".join(parts[:-1])
    stratifier = d3.stratify().set_parent_id(parent_id)
    treemapper = d3.treemap().set_tile(tile).set_size([960, 500])

    actual = treemapper(
        stratifier(data).sum(lambda d: d.get("value")).sort(lambda d: -d.value or -d.id)
    )

    def visit(node):
        new_node = {}
        new_node["name"] = node.data["id"].split(".")[-1]
        new_node["x0"] = special_round(node.x0)
        new_node["y0"] = special_round(node.y0)
        new_node["x1"] = special_round(node.x1)
        new_node["y1"] = special_round(node.y1)
        new_node["value"] = node.value
        new_node["depth"] = node.depth
        if node.children:
            new_node["children"] = [visit(child) for child in node.children]
        return new_node

    actual = visit(actual)

    def visit(node):
        node["x0"] = special_round(node["x"])
        node["y0"] = special_round(node["y"])
        node["x1"] = special_round(node["x"] + node["dx"])
        node["y1"] = special_round(node["y"] + node["dy"])
        node.pop("x")
        node.pop("y")
        node.pop("dx")
        node.pop("dy")
        if children := node.get("children"):
            children.reverse()
            for child in children:
                visit(child)
    visit(expected)

    assert actual == expected

def test_flare_1():
    data = pl.read_csv("data/flare.csv").to_dicts()
    with open("data/flare-phi.json") as file:
        expected = json.load(file)
    check(data, expected, d3.treemap_squarify)

def test_flare_2():
    data = pl.read_csv("data/flare.csv").to_dicts()
    with open("data/flare-one.json") as file:
        expected = json.load(file)
    check(data, expected, d3.treemap_squarify.set_ratio(1))
