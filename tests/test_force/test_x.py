import detroit as d3

def node_equal(actual, expected, delta=1e-6):
    return actual["index"] == expected["index"] and abs(actual["x"] - expected["x"]) < delta and abs(actual["vx"] - expected["vx"]) < delta and abs(actual["y"] - expected["y"]) < delta and abs(actual["vy"] - expected["vy"]) < delta and not(abs(actual["fx"] - expected["fx"]) > delta) and not(abs(actual["fy"] - expected["fy"]) > delta)

def test_x_1():
    x = d3.force_x(200)
    f = d3.force_simulation().set_force("x", x)
    a = { "x": 100, "y": 0 }
    b = { "x": 200, "y": 0 }
    c = { "x": 300, "y": 0 }
    f.set_nodes([a, b, c])
    f.tick(30)
    assert a["x"] > 190
    assert a["vx"] > 0
    assert b["x"] == 200
    assert b["vx"] == 0
    assert c["x"] < 210
    assert c["vx"] < 0

def test_x_2():
    y = d3.force_y(200)
    f = d3.force_simulation().set_force("y", y)
    a = { "y": 100, "x": 0 }
    b = { "y": 200, "x": 0 }
    c = { "y": 300, "x": 0 }
    f.set_nodes([a, b, c])
    f.tick(30)
    assert a["y"] > 190
    assert a["vy"] > 0
    assert b["y"] == 200
    assert b["vy"] == 0
    assert c["y"] < 210
    assert c["vy"] < 0

def test_x_3():
    x = d3.force_x(200)
    f = d3.force_simulation().set_force("x", x)
    a = { "fx": 0, "fy":0 }
    b = {}
    c = {}
    f.set_nodes([a, b, c])
    f.tick()
    assert node_equal(a, { "fx": 0, "fy": 0, "index": 0, "x": 0, "y": 0, "vy": 0, "vx": 0 })

def test_x_4():
    y = d3.force_x(200)
    f = d3.force_simulation().set_force("y", y)
    a = { "fx": 0, "fy":0 }
    b = {}
    c = {}
    f.set_nodes([a, b, c])
    f.tick()
    assert node_equal(a, { "fx": 0, "fy": 0, "index": 0, "x": 0, "y": 0, "vy": 0, "vx": 0 })

def test_x_5():
    x = d3.force_x().x(lambda d: d["x0"])
    f = d3.force_simulation().set_force("x", x)
    a = { "x": 100, "y": 0, "x0": 300 }
    b = { "x": 200, "y": 0, "x0": 200 }
    c = { "x": 300, "y": 0, "x0": 100 }
    f.set_nodes([a, b, c])
    f.tick(30)
    assert a["x"] > 290
    assert a["vx"] > 0
    assert b["x"] == 200
    assert b["vx"] == 0
    assert c["x"] < 110
    assert c["vx"] < 0

def test_x_6():
    y = d3.force_y().y(lambda d: d["y0"])
    f = d3.force_simulation().set_force("y", y)
    a = { "y": 100, "x": 0, "y0": 300 }
    b = { "y": 200, "x": 0, "y0": 200 }
    c = { "y": 300, "x": 0, "y0": 100 }
    f.set_nodes([a, b, c])
    f.tick(30)
    assert a["y"] > 290
    assert a["vy"] > 0
    assert b["y"] == 200
    assert b["vy"] == 0
    assert c["y"] < 110
    assert c["vy"] < 0
