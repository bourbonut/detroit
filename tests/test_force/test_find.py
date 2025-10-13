import detroit as d3


def test_find_1():
    f = d3.force_simulation()
    a = {"x": 5, "y": 0}
    b = {"x": 10, "y": 16}
    c = {"x": -10, "y": -4}
    f.set_nodes([a, b, c])
    assert f.find(0, 0) == a
    assert f.find(0, 20) == b


def test_find_2():
    f = d3.force_simulation()
    a = {"x": 5, "y": 0}
    b = {"x": 10, "y": 16}
    c = {"x": -10, "y": -4}
    f.set_nodes([a, b, c])
    assert f.find(0, 0) == a
    assert f.find(0, 0, 1) is None
    assert f.find(0, 20) == b
