import detroit as d3
from math import pi, inf, nan

def test_pie_1():
    p = d3.pie()
    assert p._value(42) == 42
    assert p._sort_values(1) > p._sort_values(2)
    assert p._sort_values(2) < p._sort_values(1)
    assert p._sort_values(1) == p._sort_values(1)
    assert p._sort == None
    assert p._start_angle() == 0
    assert p._end_angle() == 2 * pi
    assert p._pad_angle() == 0

def test_pie_2():
    p = d3.pie()
    assert p([1, 3, 2]) == [
        {"data": 1, "value": 1, "index": 2, "start_angle": 5.235987755982988, "end_angle": 6.283185307179585, "pad_angle": 0},
        {"data": 3, "value": 3, "index": 0, "start_angle": 0.000000000000000, "end_angle": 3.141592653589793, "pad_angle": 0},
        {"data": 2, "value": 2, "index": 1, "start_angle": 3.141592653589793, "end_angle": 5.235987755982988, "pad_angle": 0}
    ]

def test_pie_3():
    p = d3.pie()
    assert p([1, 0, -1]) == [
        {"data":    1, "value":    1, "index": 0, "start_angle": 0.000000000000000, "end_angle": 6.283185307179586, "pad_angle": 0},
        {"data":    0, "value":    0, "index": 1, "start_angle": 6.283185307179586, "end_angle": 6.283185307179586, "pad_angle": 0},
        {"data": -1, "value": -1, "index": 2, "start_angle": 6.283185307179586, "end_angle": 6.283185307179586, "pad_angle": 0}
    ]

def test_pie_4():
    p = d3.pie()
    assert p([0, 0]) == [
        {"data": 0, "value": 0, "index": 0, "start_angle": 0, "end_angle": 0, "pad_angle": 0},
        {"data": 0, "value": 0, "index": 1, "start_angle": 0, "end_angle": 0, "pad_angle": 0}
    ]
    assert p.start_angle(1)([0, 0]) == [
        {"data": 0, "value": 0, "index": 0, "start_angle": 1, "end_angle": 1, "pad_angle": 0},
        {"data": 0, "value": 0, "index": 1, "start_angle": 1, "end_angle": 1, "pad_angle": 0}
    ]

def test_pie_5():
    p = d3.pie()
    assert p.start_angle(0).end_angle(7)([1, 2]) == [
        {"data": 1, "value": 1, "index": 1, "start_angle": 4.1887902047863905, "end_angle": 6.2831853071795860, "pad_angle": 0},
        {"data": 2, "value": 2, "index": 0, "start_angle": 0.0000000000000000, "end_angle": 4.1887902047863905, "pad_angle": 0}
    ]
    assert p.start_angle(7).end_angle(0)([1, 2]) == [
        {"data": 1, "value": 1, "index": 1, "start_angle": 2.8112097952136095, "end_angle": 0.7168146928204142, "pad_angle": 0},
        {"data": 2, "value": 2, "index": 0, "start_angle": 7.0000000000000000, "end_angle": 2.8112097952136095, "pad_angle": 0}
    ]
    assert p.start_angle(1).end_angle(8)([1, 2]) == [
        {"data": 1, "value": 1, "index": 1, "start_angle": 5.1887902047863905, "end_angle": 7.2831853071795860, "pad_angle": 0},
        {"data": 2, "value": 2, "index": 0, "start_angle": 1.0000000000000000, "end_angle": 5.1887902047863905, "pad_angle": 0}
    ]
    assert p.start_angle(8).end_angle(1)([1, 2]) == [
        {"data": 1, "value": 1, "index": 1, "start_angle": 3.8112097952136095, "end_angle": 1.7168146928204142, "pad_angle": 0},
        {"data": 2, "value": 2, "index": 0, "start_angle": 8.0000000000000000, "end_angle": 3.8112097952136095, "pad_angle": 0}
    ]

def test_pie_6():
    assert d3.pie().value(lambda d, i: i)([None] * 3) == [
        {"data": None, "value": 0, "index": 2, "start_angle": 6.2831853071795860, "end_angle": 6.2831853071795860, "pad_angle": 0},
        {"data": None, "value": 1, "index": 1, "start_angle": 4.1887902047863905, "end_angle": 6.2831853071795860, "pad_angle": 0},
        {"data": None, "value": 2, "index": 0, "start_angle": 0.0000000000000000, "end_angle": 4.1887902047863905, "pad_angle": 0}
    ]

def test_pie_7():
    data = ["a", "b"]
    actual = []
    def test_function(d, i, data):
        actual.append([d, i, data])
        return -1
    d3.pie().value(test_function)(data)
    assert actual == [["a", 0, data], ["b", 1, data]]

def test_pie_8():
    expected = {"that": {}, "args": [42]}
    actual = {}
    def test_function():
        actual["that"] = {}
        actual["args"] = [42]
        return 0
    d3.pie().start_angle(test_function)([0])
    assert actual == expected

def test_pie_9():
    assert d3.pie().start_angle(pi)([1, 2, 3]) == [
        {"data": 1, "value": 1, "index": 2, "start_angle": 5.759586531581287, "end_angle": 6.283185307179586, "pad_angle": 0},
        {"data": 2, "value": 2, "index": 1, "start_angle": 4.712388980384690, "end_angle": 5.759586531581287, "pad_angle": 0},
        {"data": 3, "value": 3, "index": 0, "start_angle": 3.141592653589793, "end_angle": 4.712388980384690, "pad_angle": 0}
    ]

def test_pie_10():
    assert d3.pie().end_angle(pi)([1, 2, 3]) == [
        {"data": 1, "value": 1, "index": 2, "start_angle": 2.6179938779914940, "end_angle": 3.1415926535897927, "pad_angle": 0},
        {"data": 2, "value": 2, "index": 1, "start_angle": 1.5707963267948966, "end_angle": 2.6179938779914940, "pad_angle": 0},
        {"data": 3, "value": 3, "index": 0, "start_angle": 0.0000000000000000, "end_angle": 1.5707963267948966, "pad_angle": 0}
    ]

def test_pie_11():
    assert d3.pie().pad_angle(0.1)([1, 2, 3]) == [
        {"data": 1, "value": 1, "index": 2, "start_angle": 5.1859877559829880, "end_angle": 6.2831853071795850, "pad_angle": 0.1},
        {"data": 2, "value": 2, "index": 1, "start_angle": 3.0915926535897933, "end_angle": 5.1859877559829880, "pad_angle": 0.1},
        {"data": 3, "value": 3, "index": 0, "start_angle": 0.0000000000000000, "end_angle": 3.0915926535897933, "pad_angle": 0.1}
    ]

def test_pie_12():
    expected = {"that": {}, "args": [42]}
    actual = {}
    def test_function():
        actual["that"] = {}
        actual["args"] = [42]
        return 0
    d3.pie().end_angle(test_function)([0])
    assert actual == expected

def test_pie_13():
    expected = {"that": {}, "args": [42]}
    actual = {}
    def test_function():
        actual["that"] = {}
        actual["args"] = [42]
        return 0
    d3.pie().pad_angle(test_function)([0])
    assert actual == expected

def test_pie_14():
    assert d3.pie().start_angle(0).end_angle(pi).pad_angle(inf)([1, 2, 3]) == [
        {"data": 1, "value": 1, "index": 2, "start_angle":    2.0943951023931953, "end_angle":    3.1415926535897930, "pad_angle": 1.0471975511965976},
        {"data": 2, "value": 2, "index": 1, "start_angle":    1.0471975511965976, "end_angle":    2.0943951023931953, "pad_angle": 1.0471975511965976},
        {"data": 3, "value": 3, "index": 0, "start_angle":    0.0000000000000000, "end_angle":    1.0471975511965976, "pad_angle": 1.0471975511965976}
    ]
    assert d3.pie().start_angle(0).end_angle(-pi).pad_angle(inf)([1, 2, 3]) == [
        {"data": 1, "value": 1, "index": 2, "start_angle": -2.0943951023931953, "end_angle": -3.1415926535897930, "pad_angle": 1.0471975511965976},
        {"data": 2, "value": 2, "index": 1, "start_angle": -1.0471975511965976, "end_angle": -2.0943951023931953, "pad_angle": 1.0471975511965976},
        {"data": 3, "value": 3, "index": 0, "start_angle":    0.0000000000000000, "end_angle": -1.0471975511965976, "pad_angle": 1.0471975511965976}
    ]

def test_pie_15():
    p = d3.pie()
    assert p.sort_values(lambda x: x)([1, 3, 2]) == [
        {"data": 1, "value": 1, "index": 0, "start_angle": 0.0000000000000000, "end_angle": 1.0471975511965976, "pad_angle": 0},
        {"data": 3, "value": 3, "index": 2, "start_angle": 3.1415926535897930, "end_angle": 6.2831853071795860, "pad_angle": 0},
        {"data": 2, "value": 2, "index": 1, "start_angle": 1.0471975511965976, "end_angle": 3.1415926535897930, "pad_angle": 0}
    ]
    assert p.sort_values(lambda x: -x)([1, 3, 2]) == [
        {"data": 1, "value": 1, "index": 2, "start_angle": 5.2359877559829880, "end_angle": 6.2831853071795850, "pad_angle": 0},
        {"data": 3, "value": 3, "index": 0, "start_angle": 0.0000000000000000, "end_angle": 3.1415926535897930, "pad_angle": 0},
        {"data": 2, "value": 2, "index": 1, "start_angle": 3.1415926535897930, "end_angle": 5.2359877559829880, "pad_angle": 0}
    ]
    assert p._sort == None

def test_pie_16():
    a = {"value": 1, "name": "a"}
    b = {"value": 2, "name": "b"}
    c = {"value": 3, "name": "c"}
    p = d3.pie()
    assert p.value(lambda d: d["value"]).sort(lambda x: x["name"])([a, c, b]) == [
        {"data": a, "value": 1, "index": 0, "start_angle": 0.0000000000000000, "end_angle": 1.0471975511965976, "pad_angle": 0},
        {"data": c, "value": 3, "index": 2, "start_angle": 3.1415926535897930, "end_angle": 6.2831853071795860, "pad_angle": 0},
        {"data": b, "value": 2, "index": 1, "start_angle": 1.0471975511965976, "end_angle": 3.1415926535897930, "pad_angle": 0}
    ]
    assert p._sort_values == None
