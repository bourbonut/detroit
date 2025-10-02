import detroit as d3
import pytest

def special_round(d):
    return {
        "x0": round(d.x0 * 100) / 100,
        "y0": round(d.y0 * 100) / 100,
        "x1": round(d.x1 * 100) / 100,
        "y1": round(d.y1 * 100) / 100,
    }

def default_value(d):
    return d.get("value")

def ascending_value(d):
    return d.value

def decending_value(d):
    return -d.value

@pytest.fixture
def simple():
    return (
        {
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

@pytest.fixture
def simple_foo():
    return (
        {
            "children": [
                {"foo": 6},
                {"foo": 6},
                {"foo": 4},
                {"foo": 3},
                {"foo": 2},
                {"foo": 2},
                {"foo": 1}
            ]
        }
    )

def test_treemap_1():
    t = d3.treemap()
    assert t.get_tile() == d3.treemap_squarify
    assert t.get_size() == [1, 1]
    assert t.get_round() is False

def test_treemap_2(simple):
    t = d3.treemap().set_size([600, 400]).set_round(True)
    root = t(d3.hierarchy(simple).sum(default_value).sort(decending_value))
    nodes = list(map(special_round, root.descendants()))
    assert t.get_round() is True
    assert nodes == [
        {"x0":   0, "x1": 600, "y0":   0, "y1": 400},
        {"x0":   0, "x1": 300, "y0":   0, "y1": 200},
        {"x0":   0, "x1": 300, "y0": 200, "y1": 400},
        {"x0": 300, "x1": 471, "y0":   0, "y1": 233},
        {"x0": 471, "x1": 600, "y0":   0, "y1": 233},
        {"x0": 300, "x1": 540, "y0": 233, "y1": 317},
        {"x0": 300, "x1": 540, "y0": 317, "y1": 400},
        {"x0": 540, "x1": 600, "y0": 233, "y1": 400}
    ]

def test_treemap_3():
    t = d3.treemap().set_padding(42)
    assert t.get_padding()() == 42
    assert t.get_padding_inner()() == 42
    assert t.get_padding_outer()() == 42
    assert t.get_padding_top()() == 42
    assert t.get_padding_right()() == 42
    assert t.get_padding_bottom()() == 42
    assert t.get_padding_left()() == 42

def test_treemap_4(simple):
    t = d3.treemap().set_size([6, 4]).set_padding_inner(0.5)
    root = t(d3.hierarchy(simple).sum(default_value).sort(decending_value))
    nodes = list(map(special_round, root.descendants()))
    assert t.get_padding_inner()() == 0.5
    assert t.get_size() == [6, 4]
    assert nodes == [
        {"x0": 0.00, "x1": 6.00, "y0": 0.00, "y1": 4.00},
        {"x0": 0.00, "x1": 2.75, "y0": 0.00, "y1": 1.75},
        {"x0": 0.00, "x1": 2.75, "y0": 2.25, "y1": 4.00},
        {"x0": 3.25, "x1": 4.61, "y0": 0.00, "y1": 2.12},
        {"x0": 5.11, "x1": 6.00, "y0": 0.00, "y1": 2.12},
        {"x0": 3.25, "x1": 5.35, "y0": 2.62, "y1": 3.06},
        {"x0": 3.25, "x1": 5.35, "y0": 3.56, "y1": 4.00},
        {"x0": 5.85, "x1": 6.00, "y0": 2.62, "y1": 4.00}
    ]

def test_treemap_5(simple):
    t = d3.treemap().set_size([6, 4]).set_padding_outer(0.5)
    root = t(d3.hierarchy(simple).sum(default_value).sort(decending_value))
    nodes = list(map(special_round, root.descendants()))
    assert t.get_padding_outer()() == 0.5
    assert t.get_padding_top()() == 0.5
    assert t.get_padding_right()() == 0.5
    assert t.get_padding_bottom()() == 0.5
    assert t.get_padding_left()() == 0.5
    assert t.get_size() == [6, 4]
    assert nodes == [
        {"x0": 0.00, "x1": 6.00, "y0": 0.00, "y1": 4.00},
        {"x0": 0.50, "x1": 3.00, "y0": 0.50, "y1": 2.00},
        {"x0": 0.50, "x1": 3.00, "y0": 2.00, "y1": 3.50},
        {"x0": 3.00, "x1": 4.43, "y0": 0.50, "y1": 2.25},
        {"x0": 4.43, "x1": 5.50, "y0": 0.50, "y1": 2.25},
        {"x0": 3.00, "x1": 5.00, "y0": 2.25, "y1": 2.88},
        {"x0": 3.00, "x1": 5.00, "y0": 2.88, "y1": 3.50},
        {"x0": 5.00, "x1": 5.50, "y0": 2.25, "y1": 3.50}
    ]

def test_treemap_6(simple):
    t = d3.treemap().set_size([6, 4])
    root = t(d3.hierarchy(simple).sum(default_value).sort(decending_value))
    nodes = list(map(special_round, root.descendants()))
    assert t.get_size() == [6, 4]
    assert nodes == [
        {"x0": 0.00, "x1": 6.00, "y0": 0.00, "y1": 4.00},
        {"x0": 0.00, "x1": 3.00, "y0": 0.00, "y1": 2.00},
        {"x0": 0.00, "x1": 3.00, "y0": 2.00, "y1": 4.00},
        {"x0": 3.00, "x1": 4.71, "y0": 0.00, "y1": 2.33},
        {"x0": 4.71, "x1": 6.00, "y0": 0.00, "y1": 2.33},
        {"x0": 3.00, "x1": 5.40, "y0": 2.33, "y1": 3.17},
        {"x0": 3.00, "x1": 5.40, "y0": 3.17, "y1": 4.00},
        {"x0": 5.40, "x1": 6.00, "y0": 2.33, "y1": 4.00}
    ]

def test_treemap_7(simple):
    size = [6, 4]
    t = d3.treemap().set_size(size)
    size[1] = 100
    root = t(d3.hierarchy(simple).sum(default_value).sort(decending_value))
    nodes = list(map(special_round, root.descendants()))
    assert t.get_size() == [6, 4]
    t.get_size()[1] = 100
    assert t.get_size() == [6, 4]
    assert nodes == [
        {"x0": 0.00, "x1": 6.00, "y0": 0.00, "y1": 4.00},
        {"x0": 0.00, "x1": 3.00, "y0": 0.00, "y1": 2.00},
        {"x0": 0.00, "x1": 3.00, "y0": 2.00, "y1": 4.00},
        {"x0": 3.00, "x1": 4.71, "y0": 0.00, "y1": 2.33},
        {"x0": 4.71, "x1": 6.00, "y0": 0.00, "y1": 2.33},
        {"x0": 3.00, "x1": 5.40, "y0": 2.33, "y1": 3.17},
        {"x0": 3.00, "x1": 5.40, "y0": 3.17, "y1": 4.00},
        {"x0": 5.40, "x1": 6.00, "y0": 2.33, "y1": 4.00}
    ]

def test_treemap_8(simple_foo):
    def foo(d):
        return d.get("foo")
    t = d3.treemap().set_size([6, 4])
    root = t(d3.hierarchy(simple_foo).sum(foo).sort(decending_value))
    nodes = list(map(special_round, root.descendants()))
    assert t.get_size() == [6, 4]
    assert nodes == [
        {"x0": 0.00, "x1": 6.00, "y0": 0.00, "y1": 4.00},
        {"x0": 0.00, "x1": 3.00, "y0": 0.00, "y1": 2.00},
        {"x0": 0.00, "x1": 3.00, "y0": 2.00, "y1": 4.00},
        {"x0": 3.00, "x1": 4.71, "y0": 0.00, "y1": 2.33},
        {"x0": 4.71, "x1": 6.00, "y0": 0.00, "y1": 2.33},
        {"x0": 3.00, "x1": 5.40, "y0": 2.33, "y1": 3.17},
        {"x0": 3.00, "x1": 5.40, "y0": 3.17, "y1": 4.00},
        {"x0": 5.40, "x1": 6.00, "y0": 2.33, "y1": 4.00}
    ]

def test_treemap_9(simple):
    t = d3.treemap()
    root = t(d3.hierarchy(simple).sum(default_value).sort(ascending_value))
    assert [d.value for d in root.descendants()] == [24, 1, 2, 2, 3, 4, 6, 6]
