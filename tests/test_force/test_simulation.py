import detroit as d3

def node_equal(actual, expected, delta=1e-6):
    return actual["index"] == expected["index"] and abs(actual["x"] - expected["x"]) < delta and abs(actual["vx"] - expected["vx"]) < delta and abs(actual["y"] - expected["y"]) < delta and abs(actual["vy"] - expected["vy"]) < delta

def test_simulation_1():
    attributes = [
        "get_alpha",
        "get_alpha_decay",
        "get_alpha_min",
        "get_velocity_decay",
        "set_alpha",
        "set_alpha_decay",
        "set_alpha_min",
        "set_velocity_decay",
        '_alpha',
        '_alpha_decay',
        '_alpha_min',
        '_alpha_target',
        '_velocity_decay',
        'find',
        'get_force',
        'get_nodes',
        'get_random_source',
        'set_force',
        'set_nodes',
        'set_random_source',
    ]
    f = d3.force_simulation()
    for attribute in attributes:
        assert hasattr(f, attribute)

def test_simulation_2():
    f = d3.force_simulation()
    a = {}
    b = {}
    c = {}
    f.set_nodes([a, b, c])
    assert node_equal(a, {"index": 0, "x": 7.0710678118654755, "y": 0, "vy": 0, "vx": 0})
    assert node_equal(b, {"index": 1, "x": -9.03088751750192, "y": 8.27303273571596, "vy": 0, "vx": 0})
    assert node_equal(c, {"index": 2, "x": 1.3823220809823638, "y": -15.750847141167634, "vy": 0, "vx": 0})

