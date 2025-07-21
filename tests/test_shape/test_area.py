import detroit as d3

def test_area_1():
    a = d3.area()
    assert a.get_x0()([42, 34]) == 42
    assert a.get_x1() is None
    assert a.get_y0()([42, 34]) == 0
    assert a.get_y1()([42, 34]) == 34
    assert a.get_defined()([42, 34]) is True
    assert a.get_curve() == d3.curve_linear
    assert a.get_context() is None
    assert a([[0, 1], [2, 3], [4, 5]]) == "M0,1L2,3L4,5L4,0L2,0L0,0Z"

def test_area_2():
    def x():
        return

    def y():
        return
    assert d3.area(x).get_x0() == x
    assert d3.area(x, y).get_y0() == y
    assert d3.area(x, 0, y).get_y1() == y
    assert d3.area(3, 2, 1).get_x0()("aa") == 3
    assert d3.area(3, 2, 1).get_y0()("aa") == 2
    assert d3.area(3, 2, 1).get_y1()("aa") == 1

def test_area_3():
    data = [[10, 10], [20, 20]]
    actual = []
    def foo(d, i, data):
        actual.append([d, i, data])
        return d[0]
    d3.area().x(foo)(data)
    assert actual == [[[10, 10], 0, data], [[20, 20], 1, data]]

def test_area_4():
    data = [[10, 10], [20, 20]]
    actual = []
    def foo(d, i, data):
        actual.append([d, i, data])
        return d[0]
    d3.area().x0(foo)(data)
    assert actual == [[[10, 10], 0, data], [[20, 20], 1, data]]

def test_area_5():
    data = [[10, 10], [20, 20]]
    actual = []
    def foo(d, i, data):
        actual.append([d, i, data])
        return d[0]
    d3.area().x1(foo)(data)
    assert actual == [[[10, 10], 0, data], [[20, 20], 1, data]]

def test_area_6():
    data = [[10, 10], [20, 20]]
    actual = []
    def foo(d, i, data):
        actual.append([d, i, data])
        return d[1]
    d3.area().y(foo)(data)
    assert actual == [[[10, 10], 0, data], [[20, 20], 1, data]]

def test_area_7():
    data = [[10, 10], [20, 20]]
    actual = []
    def foo(d, i, data):
        actual.append([d, i, data])
        return d[1]
    d3.area().y0(foo)(data)
    assert actual == [[[10, 10], 0, data], [[20, 20], 1, data]]

def test_area_8():
    data = [[10, 10], [20, 20]]
    actual = []
    def foo(d, i, data):
        actual.append([d, i, data])
        return d[1]
    d3.area().y1(foo)(data)
    assert actual == [[[10, 10], 0, data], [[20, 20], 1, data]]

def test_area_9():
    data = [[10, 10], [20, 20]]
    actual = []
    def foo(d, i, data):
        actual.append([d, i, data])
        return bool(d)
    d3.area().set_defined(foo)(data)
    assert actual == [[[10, 10], 0, data], [[20, 20], 1, data]]

def test_area_10():
    def x(d):
      return d["x"]
    a = d3.area().x(x)
    assert a.get_x() == x
    assert a.get_x0() == x
    assert a.get_x1() is None
    assert a([{"x": 0, 1: 1}, {"x": 2, 1: 3}, {"x": 4, 1: 5}]) == "M0,1L2,3L4,5L4,0L2,0L0,0Z"

def test_area_11():
    x = 0
    a = d3.area().x(x)
    assert a.get_x()() == 0
    assert a.get_x0()() == 0
    assert a.get_x1() is None
    assert a([{1: 1}, {1: 3}, {1: 5}]) == "M0,1L0,3L0,5L0,0L0,0L0,0Z"

def test_area_12():
    def y(d):
      return d["y"]
    a = d3.area().y(y)
    assert a.get_y() == y
    assert a.get_y0() == y
    assert a.get_y1() is None
    assert a([{0: 0, "y": 1}, {0: 2, "y": 3}, {0: 4, "y": 5}]) == "M0,1L2,3L4,5L4,5L2,3L0,1Z"

def test_area_13():
    a = d3.area().y(0)
    assert a.get_y()() == 0
    assert a.get_y0()() == 0
    assert a.get_y1() is None
    assert a([{0: 0}, {0: 2}, {0: 4}]) == "M0,0L2,0L4,0L4,0L2,0L0,0Z"

def test_area_14():
    a = d3.area().set_curve(d3.curve_cardinal)
    assert a([[0, 1], [1, 3], [2, 1], [3, 3]]) == "M0,1C0,1,0.667,3,1,3C1.333,3,1.667,1,2,1C2.333,1,3,3,3,3L3,0C3,0,2.333,0,2,0C1.667,0,1.333,0,1,0C0.667,0,0,0,0,0Z"

def test_area_15():
    a = d3.area().set_curve(d3.curve_cardinal(0.1))
    assert a([]) is None
    assert a([[0, 1]]) == "M0,1L0,0Z"
    assert a([[0, 1], [1, 3]]) == "M0,1L1,3L1,0L0,0Z"
    assert a([[0, 1], [1, 3], [2, 1]]) == "M0,1C0,1,0.700,3,1,3C1.300,3,2,1,2,1L2,0C2,0,1.300,0,1,0C0.700,0,0,0,0,0Z"
    assert a([[0, 1], [1, 3], [2, 1], [3, 3]]) == "M0,1C0,1,0.700,3,1,3C1.300,3,1.700,1,2,1C2.300,1,3,3,3,3L3,0C3,0,2.300,0,2,0C1.700,0,1.300,0,1,0C0.700,0,0,0,0,0Z"

def test_area_16():
    a = d3.area().set_curve(d3.curve_cardinal(0.1))
    assert a([]) is None
    assert a([[0, 1]]) == "M0,1L0,0Z"
    assert a([[0, 1], [1, 3]]) == "M0,1L1,3L1,0L0,0Z"
    assert a([[0, 1], [1, 3], [2, 1]]) == "M0,1C0,1,0.700,3,1,3C1.300,3,2,1,2,1L2,0C2,0,1.300,0,1,0C0.700,0,0,0,0,0Z"
    assert a([[0, 1], [1, 3], [2, 1], [3, 3]]) == "M0,1C0,1,0.700,3,1,3C1.300,3,1.700,1,2,1C2.300,1,3,3,3,3L3,0C3,0,2.300,0,2,0C1.700,0,1.300,0,1,0C0.700,0,0,0,0,0Z"

def test_area_17():
    def defined():
      return True
    curve = d3.curve_cardinal
    context = {}
    def x0():
        return
    def x1():
        return
    def y():
        return
    a = d3.area().set_defined(defined).set_curve(curve).set_context(context).y(y).x0(x0).x1(x1)
    l = a.line_x0()
    assert l.get_defined() == defined
    assert l.get_curve() == curve
    assert l.get_context() == context
    assert l.get_x() == x0
    assert l.get_y() == y

def test_area_18():
    def defined():
      return True
    curve = d3.curve_cardinal
    context = {}
    def x0():
        return
    def x1():
        return
    def y():
        return
    a = d3.area().set_defined(defined).set_curve(curve).set_context(context).y(y).x0(x0).x1(x1)
    l = a.line_x1()
    assert l.get_defined() == defined
    assert l.get_curve() == curve
    assert l.get_context() == context
    assert l.get_x() == x1
    assert l.get_y() == y

def test_area_19():
    def defined():
      return True
    curve = d3.curve_cardinal
    context = {}
    def x():
        return
    def y0():
        return
    def y1():
        return
    a = d3.area().set_defined(defined).set_curve(curve).set_context(context).x(x).y0(y0).y1(y1)
    l = a.line_y0()
    assert l.get_defined() == defined
    assert l.get_curve() == curve
    assert l.get_context() == context
    assert l.get_x() == x
    assert l.get_y() == y0

def test_area_20():
    def defined():
      return True
    curve = d3.curve_cardinal
    context = {}
    def x():
        return
    def y0():
        return
    def y1():
        return
    a = d3.area().set_defined(defined).set_curve(curve).set_context(context).x(x).y0(y0).y1(y1)
    l = a.line_y1()
    assert l.get_defined() == defined
    assert l.get_curve() == curve
    assert l.get_context() == context
    assert l.get_x() == x
    assert l.get_y() == y1
