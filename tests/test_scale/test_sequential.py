import math

import pytest

import detroit as d3


def test_sequential_1():
    s = d3.scale_sequential()
    assert s.get_domain() == [0, 1]
    assert s.get_interpolator()(0.42) == 0.42
    assert s.get_clamp() is False
    assert s.get_unknown() is None
    assert s(-0.5) == -0.5
    assert s(0.0) == 0.0
    assert s(0.5) == 0.5
    assert s(1.0) == 1.0
    assert s(1.5) == 1.5


def test_sequential_2():
    s = d3.scale_sequential().set_clamp(True)
    assert s.get_clamp() is True
    assert s(-0.5) == 0.0
    assert s(0.0) == 0.0
    assert s(0.5) == 0.5
    assert s(1.0) == 1.0
    assert s(1.5) == 1.0


def test_sequential_3():
    s = d3.scale_sequential().set_unknown(-1)
    assert s.get_unknown() == -1
    assert s(None) == -1
    assert s(math.nan) == -1
    with pytest.raises(TypeError):
        assert s("N/A") == -1
    assert s(0.4) == 0.4


def test_sequential_4():
    s = d3.scale_sequential().set_domain(["-1.20", "2.40"])
    assert s.get_domain() == [-1.2, 2.4]
    assert s(-1.2) == 0.0
    assert s(0.6) == 0.5
    assert s(2.4) == 1.0


def test_sequential_5():
    s = d3.scale_sequential().set_domain({"-1.20", "2.40"})
    assert sorted(s.get_domain()) == sorted([-1.2, 2.4])


def test_sequential_6():
    s = d3.scale_sequential().set_domain([2, 2])
    assert s.get_domain() == [2, 2]
    assert s(-1.2) == 0.5
    assert s(0.6) == 0.5
    assert s(2.4) == 0.5


def test_sequential_7():
    s = d3.scale_sequential().set_domain([math.nan, 2])
    assert math.isnan(s.get_domain()[0])
    assert s.get_domain()[1] == 2
    assert math.isnan(s(-1.2))
    assert math.isnan(s(0.6))
    assert math.isnan(s(2.4))


def test_sequential_8():
    s = d3.scale_sequential().set_domain([-1, 100, 200])
    assert s.get_domain() == [-1, 100]


def test_sequential_9():
    s1 = d3.scale_sequential().set_domain([1, 3]).set_clamp(True)
    s2 = s1.copy()
    assert s2.get_domain() == [1, 3]
    assert s2.get_clamp() is True
    s1.set_domain([-1, 2])
    assert s2.get_domain() == [1, 3]
    s1.set_clamp(False)
    assert s2.get_clamp() is True
    s2.set_domain([3, 4])
    assert s1.get_domain() == [-1, 2]
    s2.set_clamp(True)
    assert s1.get_clamp() is False


def test_sequential_10():
    def i0(t):
        return t

    def i1(t):
        return t * 2

    s = d3.scale_sequential(i0)
    assert s.get_interpolator() == i0
    assert s.set_interpolator(i1) == s
    assert s.get_interpolator() == i1
    assert s(-0.5) == -1.0
    assert s(0.0) == 0.0
    assert s(0.5) == 1.0


def test_sequential_11():
    s = d3.scale_sequential(lambda t: 2 * t + 1)
    assert s.get_range() == [1, 3]


def test_sequential_12():
    s = d3.scale_sequential().set_range([1, 3])
    assert s.get_interpolator()(0.5) == 2
    assert s.get_range() == [1, 3]


def test_sequential_13():
    s = d3.scale_sequential().set_range([1, 3, 10])
    assert s.get_interpolator()(0.5) == 2
    assert s.get_range() == [1, 3]


def test_sequential_14():
    s = d3.scale_sequential([1, 3])
    assert s.get_interpolator()(0.5) == 2
    assert s.get_range() == [1, 3]
