import math

import pytest

import detroit as d3


def frange(start, end, step=1):
    rep = int((end - start) / step)
    return (start + i * step for i in range(rep))


def test_quantize_1():
    s = d3.scale_quantize()
    assert s.domain() == [0, 1]
    assert s.range() == [0, 1]
    assert s.thresholds() == [0.5]
    assert s(0.25) == 0
    assert s(0.75) == 1


def test_quantize_2():
    s = d3.scale_quantize().range([0, 1, 2])
    assert s.thresholds() == [1 / 3, 2 / 3]
    assert s(0.0) == 0
    assert s(0.2) == 0
    assert s(0.4) == 1
    assert s(0.6) == 1
    assert s(0.8) == 2
    assert s(1.0) == 2


def test_quantize_3():
    a = {}
    b = {}
    c = {}
    s = d3.scale_quantize().range([a, b, c])
    assert s(-0.5) == a
    assert s(+1.5) == c


def test_quantize_4():
    s = d3.scale_quantize().range([0, 1, 2]).unknown(-1)
    assert s(None) == -1
    assert s(None) == -1
    assert s(math.nan) == -1


def test_quantize_5():
    s = d3.scale_quantize().domain(["-1.20", "2.40"])
    assert s.domain() == [-1.2, 2.4]
    assert s(-1.2) == 0
    assert s(0.5) == 0
    assert s(0.7) == 1
    assert s(2.4) == 1


def test_quantize_6():
    s = d3.scale_quantize().domain({1, 2})
    assert s.domain() == [1, 2]


def test_quantize_7():
    s = d3.scale_quantize().domain([-1, 100, 200])
    assert s.domain() == [-1, 100]


def test_quantize_8():
    s = d3.scale_quantize()
    assert math.isclose(s.range(frange(0, 1.001, 0.001))(1 / 3), 0.333, rel_tol=1e-6)
    assert math.isclose(s.range(frange(0, 1.010, 0.010))(1 / 3), 0.330, rel_tol=1e-6)
    assert math.isclose(s.range(frange(0, 1.100, 0.100))(1 / 3), 0.300, rel_tol=1e-6)
    assert math.isclose(s.range(frange(0, 1.200, 0.200))(1 / 3), 0.200, rel_tol=1e-6)
    assert math.isclose(s.range(frange(0, 1.250, 0.250))(1 / 3), 0.250, rel_tol=1e-6)
    assert math.isclose(s.range(frange(0, 1.500, 0.500))(1 / 3), 0.500, rel_tol=1e-6)
    assert math.isclose(s.range(frange(0, 1))(1 / 3), 0, rel_tol=1e-6)


def test_quantize_9():
    a = {}
    b = {}
    c = {}
    s = d3.scale_quantize().range([a, b, c])
    assert s(0.0) == a
    assert s(0.2) == a
    assert s(0.4) == b
    assert s(0.6) == b
    assert s(0.8) == c
    assert s(1.0) == c


def test_quantize_10():
    s = d3.scale_quantize().range([0, 1, 2, 3])
    assert s.invert_extent(0) == [0.00, 0.25]
    assert s.invert_extent(1) == [0.25, 0.50]
    assert s.invert_extent(2) == [0.50, 0.75]
    assert s.invert_extent(3) == [0.75, 1.00]


# def test_quantize_11():
#     a = {}
#     b = {}
#     s = d3.scale_quantize().range([a, b])
#     assert s.invert_extent(a) == [0.0, 0.5]
#     assert s.invert_extent(b) == [0.5, 1.0]


def test_quantize_11():
    s = d3.scale_quantize()
    with pytest.raises(ValueError):
        s.invert_extent(-1)
    with pytest.raises(ValueError):
        s.invert_extent(0.5)
    with pytest.raises(ValueError):
        s.invert_extent(2)
    with pytest.raises(ValueError):
        s.invert_extent("a")


def test_quantize_12():
    s = d3.scale_quantize().range([0, 1, 2, 0])
    assert s.invert_extent(0) == [0.00, 0.25]
    assert s.invert_extent(1) == [0.25, 0.50]


def test_quantize_13():
    s = d3.scale_quantize().domain([4.2, 6.2]).range(range(10))
    for y in s.range():
        e = s.invert_extent(y)
        assert s(e[0]) == y
        assert s(e[1]) == (y + 1 if y < 9 else y)
