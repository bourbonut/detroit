import detroit as d3

def node_equal(actual, expected, delta = 1e-6):
    return actual["index"] == expected["index"] and abs(actual["x"] - expected["x"]) < delta and abs(actual["vx"] - expected["vx"]) < delta and abs(actual["y"] - expected["y"]) < delta and abs(actual["vy"] - expected["vy"]) < delta

def test_center_1():
    center = d3.force_center(0, 0)
    f = d3.force_simulation().set_force("center", center)
    a = {"x": 100, "y": 0}
    b = {"x": 200, "y": 0}
    c = {"x": 300, "y": 0}
    f.set_nodes([a, b, c])
    f.tick()
    assert node_equal(a, {"index": 0, "x": -100, "y": 0, "vy": 0, "vx": 0})
    assert node_equal(b, {"index": 1, "x": 0, "y": 0, "vy": 0, "vx": 0})
    assert node_equal(c, {"index": 2, "x": 100, "y": 0, "vy": 0, "vx": 0})

def test_center_2():
    center = d3.force_center()
    f = d3.force_simulation().set_force("center", center)
    a = {"fx": 0, "fy": 0}
    b = {}
    c = {}
    f.set_nodes([a, b, c])
    f.tick()
    assert a == {"fx": 0, "fy": 0, "index": 0, "x": 0, "y": 0, "vy": 0, "vx": 0}
