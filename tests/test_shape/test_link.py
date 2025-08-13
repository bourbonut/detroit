import detroit as d3
import math

def test_link_1():
    l = d3.link(d3.curve_linear)
    assert l.get_source()({"source": 42}) == 42
    assert l.get_target()({"target": 34}) == 34
    assert l.get_x()([42, 34]) == 42
    assert l.get_y()([42, 34]) == 34
    assert l.get_context() is None
    assert l({"source": [0, 1], "target": [2, 3]}) == "M0,1L2,3"

def test_link_2():
    l = d3.link(d3.curve_linear)
    def x(d):
        return d["x"]
    assert l.set_source(x) == l
    assert l.get_source() == x
    assert l({"x": [0, 1], "target": [2, 3]}) == "M0,1L2,3"

def test_link_3():
    l = d3.link(d3.curve_linear)
    def x(d):
        return d["x"]
    assert l.set_target(x) == l
    assert l.get_target() == x
    assert l({"source": [0, 1], "x": [2, 3]}) == "M0,1L2,3"

def test_link_4():
    data = {"source": [0, 1], "target": [2, 3]}
    extra = {"name": "extra"}
    actual = []
    def foo(d, extra):
        actual.append([d, extra])
        return d["source"]
    d3.link(d3.curve_linear).set_source(foo)(data, extra)
    assert actual == [[data, extra]]

def test_link_5():
    data = {"source": [0, 1], "target": [2, 3]}
    extra = {"name": "extra"}
    actual = []
    def foo(d, extra):
        actual.append([d, extra])
        return d["target"]
    d3.link(d3.curve_linear).set_target(foo)(data, extra)
    assert actual == [[data, extra]]

def test_link_6():
    l = d3.link(d3.curve_linear)
    def x(d):
        return d["x"]
    assert l.x(x) == l
    assert l.get_x() == x
    assert l({"source": {"x": 0, 1: 1}, "target": {"x": 2, 1: 3}}) == "M0,1L2,3"

def test_link_7():
    l = d3.link(d3.curve_linear)
    def y(d):
        return d["y"]
    assert l.y(y) == l
    assert l.get_y() == y
    assert l({"source": {0: 0, "y": 1}, "target": {0: 2, "y": 3}}) == "M0,1L2,3"

def test_link_8():
    data = {"source": [0, 1], "target": [2, 3]}
    extra = {"name": "extra"}
    actual = []
    def foo(d, extra):
        actual.append([d, extra])
        return d[0]
    d3.link(d3.curve_linear).x(foo)(data, extra)
    assert actual == [[[0, 1], extra], [[2, 3], extra]]

def test_link_9():
    data = {"source": [0, 1], "target": [2, 3]}
    extra = {"name": "extra"}
    actual = []
    def foo(d, extra):
        actual.append([d, extra])
        return d[1]
    d3.link(d3.curve_linear).y(foo)(data, extra)
    assert actual == [[[0, 1], extra], [[2, 3], extra]]

def test_link_10():
    l = d3.link_horizontal()
    l2 = d3.link(d3.curve_bump_x)
    assert l.get_source() == l2.get_source()
    assert l.get_target() == l2.get_target()
    assert l.get_x() == l2.get_x()
    assert l.get_y() == l2.get_y()
    assert l.get_context() == l2.get_context()
    assert l({"source": [0, 1], "target": [2, 3]}) == l2({"source": [0, 1], "target": [2, 3]})

def test_link_11():
    l = d3.link_vertical()
    l2 = d3.link(d3.curve_bump_y)
    assert l.get_source() == l2.get_source()
    assert l.get_target() == l2.get_target()
    assert l.get_x() == l2.get_x()
    assert l.get_y() == l2.get_y()
    assert l.get_context() == l2.get_context()
    assert l({"source": [0, 1], "target": [2, 3]}) == l2({"source": [0, 1], "target": [2, 3]})

def test_link_12():
    p = d3.path(6)
    l = d3.link(d3.curve_linear).set_context(p)
    assert l({"source": [0, math.e], "target": [math.pi, 3]}) is None
    assert str(p) == "M0,2.718282L3.141593,3"

def test_link_13():
    l = d3.link_radial()
    l2 = d3.link(d3.curve_bump_radial)
    assert l.get_source() == l2.get_source()
    assert l.get_target() == l2.get_target()
    assert l.get_angle() == l2.get_x()
    assert l.get_radius() == l2.get_y()
    assert l.get_context() == l2.get_context()
    assert l({"source": [0, 1], "target": [math.pi/2, 3]}) == "M0,-1C0,-2,2,0,3,0"
