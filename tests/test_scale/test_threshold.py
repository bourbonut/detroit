import detroit as d3
import math

def test_threshold_1():
    x = d3.scale_threshold()
    assert x.domain == [0.5]
    assert x.range == [0, 1]
    assert x(0.50) == 1
    assert x(0.49) == 0

def test_threshold_2():
    x = d3.scale_threshold().set_domain([1/3, 2/3]).set_range(["a", "b", "c"])
    assert x(0) == "a"
    assert x(0.2) == "a"
    assert x(0.4) == "b"
    assert x(0.6) == "b"
    assert x(0.8) == "c"
    assert x(1) == "c"

def test_threshold_3():
    x = d3.scale_threshold().set_domain([1/3, 2/3]).set_range(["a", "b", "c"])
    assert x() is None
    assert x(None) is None
    assert x(math.nan) is None
    assert x(None) is None

def test_threshold_4():
    x = d3.scale_threshold().set_domain(["10", "2"]).set_range([0, 1, 2])
    assert x.domain[0] == "10"
    assert x.domain[1] == "2"
    assert x("0") == 0
    assert x("12") == 1
    assert x("3") == 2

def test_threshold_5():
    x = d3.scale_threshold().set_domain({"10", "2"}).set_range([0, 1, 2])
    assert sorted(x.domain) == sorted(["10", "2"])

def test_threshold_6():
    a = "a"
    b = "b"
    c = "c"
    x = d3.scale_threshold().set_domain([1/3, 2/3]).set_range([a, b, c])
    assert x(0) == a
    assert x(0.2) == a
    assert x(0.4) == b
    assert x(0.6) == b
    assert x(0.8) == c
    assert x(1) == c

def test_threshold_7():
    x = d3.scale_threshold().set_domain(["10", "2"]).set_range({0, 1, 2})
    assert x.range == [0, 1, 2]

def test_threshold_8():
    a = "a"
    b = "b"
    c = "c"
    x = d3.scale_threshold().set_domain([1/3, 2/3]).set_range([a, b, c])
    assert x.invert_extent(a) == [None, 1/3]
    assert x.invert_extent(b) == [1/3, 2/3]
    assert x.invert_extent(c) == [2/3, None]
    assert x.invert_extent({}) == [None, None]
