import math


import detroit as d3
from detroit.shape.curves.linear import curve_linear


def test_line_1():
    l = d3.line()
    assert l.get_x()([42, 34]) == 42
    assert l.get_y()([42, 34]) == 34
    assert l.get_defined()([42, 34]) is True
    assert l.get_curve() == curve_linear
    assert l.get_context() is None
    assert str(l([[0, 1], [2, 3], [4, 5]])) == "M0,1L2,3L4,5"


def test_line_2():
    def x(*args):
        return

    def y(*args):
        return

    assert d3.line(x).get_x() == x
    assert d3.line(x, y).get_y() == y
    assert d3.line(3, 2).get_x()("aa") == 3
    assert d3.line(3, 2).get_y()("aa") == 2


def test_line_3():
    data = ["a", "b"]
    actual_x = []
    actual_y = []

    def fx(d, i, data):
        actual_x.append([d, i, data])
        return 0

    def fy(d, i, data):
        actual_y.append([d, i, data])
        return 0

    d3.line().x(fx).y(fy)(data)
    assert actual_x == [["a", 0, data], ["b", 1, data]]
    assert actual_y == [["a", 0, data], ["b", 1, data]]


def test_line_4():
    data = ["a", "b"]
    actual = []

    def f(*args):
        actual.append(list(args))
        return True

    def c(d, i, data):
        return 0

    d3.line().x(c).y(c).set_defined(f)(data)
    assert actual == [["a", 0, data], ["b", 1, data]]


def test_line_5():
    def x(d, *args):
        return d["x"]

    l = d3.line().x(x)
    assert str(l([{"x": 0, 1: 1}, {"x": 2, 1: 3}, {"x": 4, 1: 5}])) == "M0,1L2,3L4,5"


def test_line_6():
    l = d3.line().x(0)
    assert str(l([{1: 1}, {1: 3}, {1: 5}])) == "M0,1L0,3L0,5"


def test_line_7():
    def y(d, *args):
        return d["y"]

    l = d3.line().y(y)
    assert str(l([{0: 0, "y": 1}, {0: 2, "y": 3}, {0: 4, "y": 5}])) == "M0,1L2,3L4,5"


def test_line_8():
    l = d3.line().y(0)
    assert str(l([{0: 0}, {0: 2}, {0: 4}])) == "M0,0L2,0L4,0"


def test_line_9():
    l = d3.line().set_curve(d3.curve_linear_closed)
    assert l([]) is None
    assert str(l([[0, 1], [2, 3]])) == "M0,1L2,3Z"


def test_line_10():
    points = [[0, math.pi], [math.e, 4]]
    l = d3.line()
    assert l.digits() == 3
    assert l(points) == "M0,3.142L2.718,4"
    assert l.digits(6) == l
    assert l.digits() == 6
    assert str(l(points)) == "M0,3.141593L2.718282,4"
    assert d3.line()(points) == "M0,3.142L2.718,4"
    assert str(d3.line()(points)) == "M0,3.142L2.718,4"
    assert l.digits(3) == l
    assert l.digits() == 3
    assert str(l(points)) == "M0,3.142L2.718,4"
