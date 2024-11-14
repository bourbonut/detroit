import detroit as d3
import math
from datetime import datetime

def test_symlog_1():
    s = d3.scale_symlog()
    assert s.domain() == [0, 1]
    assert s.range() == [0, 1]
    assert s.clamp() is False
    assert s.constant() == 1

def test_symlog_2():
    s = d3.scale_symlog().domain([-100, 100])
    assert s(-100) == 0
    assert s(100) == 1
    assert s(0) == 0.5

def test_symlog_3():
    s = d3.scale_symlog().domain([-100, 100])
    assert s.invert(1) == 100

def test_symlog_4():
    s = d3.scale_symlog().range(["-3", "3"])
    assert s.invert(3) == 1

def test_symlog_5():
    assert(math.isnan(d3.scale_symlog().range(["#000", "#fff"]).invert("#999")))
    assert(math.isnan(d3.scale_symlog().range([0, "#fff"]).invert("#999")))

def test_symlog_6():
    s = d3.scale_symlog().constant(5)
    assert s.constant() == 5

def test_symlog_7():
    s = d3.scale_symlog().constant(2)
    assert s.domain() == [0, 1]
    assert s.range() == [0, 1]

def test_symlog_8():
    assert d3.scale_symlog().domain([]).domain() == []
    assert d3.scale_symlog().domain([1, 0]).domain() == [1, 0]
    assert d3.scale_symlog().domain([1, 2, 3]).domain() == [1, 2, 3]

def test_symlog_9():
    assert d3.scale_symlog().domain([datetime(1990, 0, 1), datetime(1991, 0, 1)]).domain() == [631152000000, 662688000000]
    assert d3.scale_symlog().domain(["0.0", "1.0"]).domain() == [0, 1]
    assert d3.scale_symlog().domain([0, 1]).domain() == [0, 1]

def test_symlog_10():
    d = [1, 2]
    s = d3.scale_symlog().domain(d)
    assert s.domain() == [1, 2]
    d.push(3)
    assert s.domain() == [1, 2]
    assert d == [1, 2, 3]

def test_symlog_11():
    s = d3.scale_symlog()
    d = s.domain()
    assert d == [0, 1]
    d.push(3)
    assert s.domain() == [0, 1]

def test_symlog_12():
    s = d3.scale_symlog().range(["0px", "2px"])
    assert s.range() == ["0px", "2px"]
    assert s(1) == "2px"

def test_symlog_13():
    assert d3.scale_symlog().range([{"color": "red"}, {"color": "blue"}])(1), {"color": "rgb(0, 0, 255)"}
    assert d3.scale_symlog().range([["red"], ["blue"]])(0), ["rgb(255, 0, 0)"]

def test_symlog_14():
    r = [1, 2]
    s = d3.scale_symlog().range(r)
    assert s.range() == [1, 2]
    r.push(3)
    assert s.range() == [1, 2]
    assert r == [1, 2, 3]

def test_symlog_15():
    s = d3.scale_symlog()
    r = s.range()
    assert r == [0, 1]
    r.push(3)
    assert s.range() == [0, 1]

def test_symlog_16():
    assert d3.scale_symlog().clamp() is False
    assert d3.scale_symlog().range([10, 20])(3) == 30
    assert d3.scale_symlog().range([10, 20])(-1) == 0
    assert d3.scale_symlog().range([10, 20]).invert(30) == 3
    assert d3.scale_symlog().range([10, 20]).invert(0) == -1

def test_symlog_17():
    assert d3.scale_symlog().clamp(True).range([10, 20])(2) == 20
    assert d3.scale_symlog().clamp(True).range([10, 20])(-1) == 10

def test_symlog_18():
    assert d3.scale_symlog().clamp(True).range([10, 20]).invert(30) ==  1
    assert d3.scale_symlog().clamp(True).range([10, 20]).invert(0) == 0

def test_symlog_19():
    assert d3.scale_symlog().clamp("True").clamp() is True
    assert d3.scale_symlog().clamp(1).clamp() is True
    assert d3.scale_symlog().clamp("").clamp() is False
    assert d3.scale_symlog().clamp(0).clamp() is False

def test_symlog_20():
    x = d3.scale_symlog()
    y = x.copy()
    x.domain([1, 2])
    assert y.domain() == [0, 1]
    assert x(1) == 0
    assert y(1) == 1
    y.domain([2, 3])
    assert x(2) == 1
    assert y(2) == 0
    assert x.domain() == [1, 2]
    assert y.domain() == [2, 3]
    y2 = x.domain([1, 1.9]).copy()
    x.nice(5)
    assert x.domain() == [1, 2]
    assert y2.domain() == [1, 1.9]

def test_symlog_21():
    x = d3.scale_symlog()
    y = x.copy()
    x.range([1, 2])
    assert x.invert(1) == 0
    assert y.invert(1) == 1
    assert y.range() == [0, 1]
    y.range([2, 3])
    assert x.invert(2) == 1
    assert y.invert(2) == 0
    assert x.range() == [1, 2]
    assert y.range() == [2, 3]

def test_symlog_22():
    x = d3.scale_symlog().clamp(True)
    y = x.copy()
    x.clamp(False)
    assert x(3) == 2
    assert y(2) == 1
    assert y.clamp() is True
    y.clamp(False)
    assert x(3) == 2
    assert y(3) == 2
    assert x.clamp() is False

def test_symlog_23():
    x = d3.scale_symlog().domain([1, 20]).clamp(True)
    assert x.invert(0) == 1
    assert x.invert(1) == 20
