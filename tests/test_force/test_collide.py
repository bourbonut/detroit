import detroit as d3

def node_equal(actual, expected, delta):
    return actual["index"] == expected["index"] and abs(actual["x"] - expected["x"]) < delta and abs(actual["vx"] - expected["vx"]) < delta and abs(actual["y"] - expected["y"]) < delta and abs(actual["vy"] - expected["vy"]) < delta

def test_collide_1():
    collide = d3.force_collide(1)
    f = d3.force_simulation().set_force("collide", collide)
    a = {}
    b = {}
    c = {}
    f.set_nodes([a, b, c])
    f.tick(10)
    assert a == { "index": 0, "x": 7.0710678118654755, "y": 0, "vy": 0, "vx": 0 }
    assert b == { "index": 1, "x": -9.03088751750192,  "y": 8.273032735715967, "vy": 0, "vx": 0 }
    assert c == { "index": 2, "x": 1.3823220809823638, "y": -15.750847141167634, "vy": 0, "vx": 0 }
    collide.set_radius(100)
    f.tick(10)
    assert a == {
      "index": 0,
      "x": 174.08616723117228,
      "y": 66.51743051995625,
      "vy": 0.26976816231064354,
      "vx": 0.677346615710878
    }
    assert b == {
      "index": 1,
      "x": -139.73606544743998,
      "y": 95.69860503079263,
      "vy": 0.3545632444404687,
      "vx": -0.5300880593105067
    }
    assert c == {
      "index": 2,
      "x": -34.9275994083864,
      "y": -169.69384995620052,
      "vy": -0.6243314067511122,
      "vx": -0.1472585564003713
    }


def test_collide_2():
    collide = d3.force_collide(1)
    f = d3.force_simulation().set_force("collide", collide)
    a = {"fx": 0, "fy": 0}
    b = {}
    c = {}
    f.set_nodes([a, b, c])
    f.tick(10)
    assert a == { "fx": 0, "fy": 0, "index": 0, "x": 0, "y": 0, "vy": 0, "vx": 0 }
    collide.set_radius(100)
    f.tick(10)
    assert a == { "fx": 0, "fy": 0, "index": 0, "x": 0, "y": 0, "vy": 0, "vx": 0 }

def test_collide_3():
    collide = d3.force_collide(1)
    f = d3.force_simulation().set_force("collide", collide)
    a = {"x": 0, "y": 0}
    b = {"x": 0, "y": 0}
    f.set_nodes([a, b])
    f.tick()
    assert a["x"] != b["x"]
    assert a["y"] != b["y"]
    assert a["vx"] == -b["vx"]
    assert a["vy"] == -b["vy"]

def test_collide_4():
    nodes = [{"x": 0, "y": 0} for _ in range(10)]
    d3.force_simulation().set_nodes(nodes).set_force("collide", d3.force_collide()).tick(50)
    assert node_equal(nodes[0], {"x": -5.371433857229194, "y": -2.6644608278592576, "index": 0, "vy": 0, "vx": 0}, 1e-6)
