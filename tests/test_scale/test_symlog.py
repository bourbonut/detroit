import detroit as d3
import math
import pytest
from datetime import datetime

def test_symlog_1():
    s = d3.scale_symlog()
    assert s.domain == [0, 1]
    assert s.range == [0, 1]
    assert s.clamp is False
    assert s.constant == 1

def test_symlog_2():
    s = d3.scale_symlog().set_domain([-100, 100])
    assert s(-100) == 0
    assert s(100) == 1
    assert s(0) == 0.5

def test_symlog_3():
    s = d3.scale_symlog().set_domain([-100, 100])
    assert math.isclose(s.invert(1), 100, rel_tol=1e-6)

def test_symlog_4():
    s = d3.scale_symlog().set_range(["-3", "3"])
    assert s.invert(3) == 1

def test_symlog_5():
    with pytest.raises(ValueError):
        assert(math.isnan(d3.scale_symlog().set_range(["#000", "#fff"]).invert("#999")))
    with pytest.raises(TypeError):
        assert(math.isnan(d3.scale_symlog().set_range([0, "#fff"]).invert("#999")))

def test_symlog_6():
    s = d3.scale_symlog().set_constant(5)
    assert s.constant == 5

def test_symlog_7():
    s = d3.scale_symlog().set_constant(2)
    assert s.domain == [0, 1]
    assert s.range == [0, 1]

def test_symlog_8():
    assert d3.scale_symlog().set_domain([]).domain == []
    assert d3.scale_symlog().set_domain([1, 0]).domain == [1, 0]
    assert d3.scale_symlog().set_domain([1, 2, 3]).domain == [1, 2, 3]

def test_symlog_9():
    assert d3.scale_symlog().set_domain([datetime(1990, 1, 1), datetime(1991, 1, 1)]).domain == [datetime(1990, 1, 1), datetime(1991, 1, 1)]
    assert d3.scale_symlog().set_domain(["0.0", "1.0"]).domain == [0, 1]
    assert d3.scale_symlog().set_domain([0, 1]).domain == [0, 1]

def test_symlog_10():
    d = [1, 2]
    s = d3.scale_symlog().set_domain(d)
    assert s.domain == [1, 2]
    d.append(3)
    assert s.domain == [1, 2]
    assert d == [1, 2, 3]

def test_symlog_11():
    s = d3.scale_symlog()
    d = s.domain
    assert d == [0, 1]
    d.append(3)
    assert s.domain == [0, 1]

def test_symlog_12():
    s = d3.scale_symlog().set_range(["0px", "2px"])
    assert s.range == ["0px", "2px"]
    assert s(1) == "2px"

def test_symlog_13():
    assert d3.scale_symlog().set_range([{"color": "red"}, {"color": "blue"}])(1), {"color": "rgb(0, 0, 255)"}
    assert d3.scale_symlog().set_range([["red"], ["blue"]])(0), ["rgb(255, 0, 0)"]

def test_symlog_14():
    r = [1, 2]
    s = d3.scale_symlog().set_range(r)
    assert s.range == [1, 2]
    r.append(3)
    assert s.range == [1, 2]
    assert r == [1, 2, 3]

def test_symlog_15():
    s = d3.scale_symlog()
    r = s.range
    assert r == [0, 1]
    r.append(3)
    assert s.range == [0, 1]

def test_symlog_16():
    assert d3.scale_symlog().clamp is False
    assert d3.scale_symlog().set_range([10, 20])(3) == 30
    assert d3.scale_symlog().set_range([10, 20])(-1) == 0
    assert d3.scale_symlog().set_range([10, 20]).invert(30) == 3
    assert d3.scale_symlog().set_range([10, 20]).invert(0) == -1

def test_symlog_17():
    assert d3.scale_symlog().set_clamp(True).set_range([10, 20])(2) == 20
    assert d3.scale_symlog().set_clamp(True).set_range([10, 20])(-1) == 10

def test_symlog_18():
    assert d3.scale_symlog().set_clamp(True).set_range([10, 20]).invert(30) ==  1
    assert d3.scale_symlog().set_clamp(True).set_range([10, 20]).invert(0) == 0

def test_symlog_19():
    assert d3.scale_symlog().set_clamp("True").clamp is True
    assert d3.scale_symlog().set_clamp(1).clamp is True
    assert d3.scale_symlog().set_clamp("").clamp is False
    assert d3.scale_symlog().set_clamp(0).clamp is False

def test_symlog_20():
    x = d3.scale_symlog()
    y = x.copy()
    x.set_domain([1, 2])
    assert y.domain == [0, 1]
    assert x(1) == 0
    assert y(1) == 1
    y.set_domain([2, 3])
    assert x(2) == 1
    assert y(2) == 0
    assert x.domain == [1, 2]
    assert y.domain == [2, 3]
    y2 = x.set_domain([1, 1.9]).copy()
    x.nice(5)
    assert x.domain == [1, 2]
    assert y2.domain == [1, 1.9]

def test_symlog_21():
    x = d3.scale_symlog()
    y = x.copy()
    x.set_range([1, 2])
    assert x.invert(1) == 0
    assert y.invert(1) == 1
    assert y.range == [0, 1]
    y.set_range([2, 3])
    assert x.invert(2) == 1
    assert y.invert(2) == 0
    assert x.range == [1, 2]
    assert y.range == [2, 3]

def test_symlog_22():
    x = d3.scale_symlog().set_clamp(True)
    y = x.copy()
    x.set_clamp(False)
    assert x(3) == 2
    assert y(2) == 1
    assert y.clamp is True
    y.set_clamp(False)
    assert x(3) == 2
    assert y(3) == 2
    assert x.clamp is False

def test_symlog_23():
    x = d3.scale_symlog().set_domain([1, 20]).set_clamp(True)
    assert x.invert(0) == 1
    assert x.invert(1) == 20
