import math

import detroit as d3


def test_diverging_1():
    s = d3.scale_diverging()
    assert s.domain == [0, 0.5, 1]
    assert s.interpolator(0.42) == 0.42
    assert s.clamp is False
    assert s(-0.5) == -0.5
    assert s(0.0) == 0.0
    assert s(0.5) == 0.5
    assert s(1.0) == 1.0
    assert s(1.5) == 1.5


def test_diverging_2():
    s = d3.scale_diverging().set_clamp(True)
    assert s.clamp is True
    assert s(-0.5) == 0.0
    assert s(0.0) == 0.0
    assert s(0.5) == 0.5
    assert s(1.0) == 1.0
    assert s(1.5) == 1.0


def test_diverging_3():
    s = d3.scale_diverging().set_domain(["-1.20", " 0", "2.40"])
    assert s.domain == [-1.2, 0, 2.4]
    assert s(-1.2) == 0.000
    assert s(0.6) == 0.625
    assert s(2.4) == 1.000


def test_diverging_4():
    s = d3.scale_diverging().set_domain({-1.2, 0, 2.4})
    assert sorted(s.domain) == sorted([-1.2, 0, 2.4])


def test_diverging_5():
    s = d3.scale_diverging().set_domain([2, 2, 3])
    assert s.domain == [2, 2, 3]
    assert s(-1.2) == 0.5
    assert s(0.6) == 0.5
    assert s(2.4) == 0.7
    assert s.set_domain([1, 2, 2]).domain == [1, 2, 2]
    assert s(-1.0) == -1
    assert s(0.5) == -0.25
    assert s(2.4) == 0.5
    assert s.set_domain([2, 2, 2]).domain == [2, 2, 2]
    assert s(-1.0) == 0.5
    assert s(0.5) == 0.5
    assert s(2.4) == 0.5


def test_diverging_6():
    s = d3.scale_diverging().set_domain([4, 2, 1])
    assert s.domain == [4, 2, 1]
    assert s(1.2) == 0.9
    assert s(2.0) == 0.5
    assert s(3.0) == 0.25


def test_diverging_7():
    s = d3.scale_diverging_log().set_domain([3, 2, 1])
    assert s.domain == [3, 2, 1]
    assert math.isclose(s(1.2), 1 - 0.1315172029168969, rel_tol=1e-6)
    assert math.isclose(s(2.0), 1 - 0.5000000000000000, rel_tol=1e-6)
    assert math.isclose(s(2.8), 1 - 0.9149213210862197, rel_tol=1e-6)


def test_diverging_8():
    s = d3.scale_diverging_log().set_domain([-1, -2, -3])
    assert s.domain == [-1, -2, -3]
    assert math.isclose(s(-1.2), 0.1315172029168969, rel_tol=1e-6)
    assert math.isclose(s(-2.0), 0.5000000000000000, rel_tol=1e-6)
    assert math.isclose(s(-2.8), 0.9149213210862197, rel_tol=1e-6)


def test_diverging_9():
    s = d3.scale_diverging().set_domain([math.nan, 2, 3])
    assert math.isnan(s.domain[0])
    assert math.isnan(s(-1.2)) is True
    assert math.isnan(s(0.6)) is True
    assert s(2.4) == 0.7
    assert math.isnan(s.set_domain([1, math.nan, 2]).domain[1])
    assert math.isnan(s(-1.0)) is True
    assert math.isnan(s(0.5)) is True
    assert math.isnan(s(2.4)) is True
    assert math.isnan(s.set_domain([0, 1, math.nan]).domain[2])
    assert s(-1.0) == -0.5
    assert s(0.5) == 0.25
    assert math.isnan(s(2.4)) is True


def test_diverging_10():
    s = d3.scale_diverging().set_domain([-1, 100, 200, 3])
    assert s.domain == [-1, 100, 200]


def test_diverging_11():
    s1 = d3.scale_diverging().set_domain([1, 2, 3]).set_clamp(True)
    s2 = s1.copy()
    assert s2.domain == [1, 2, 3]
    assert s2.clamp is True
    s1.set_domain([-1, 1, 2])
    assert s2.domain == [1, 2, 3]
    s1.set_clamp(False)
    assert s2.clamp is True
    s2.set_domain([3, 4, 5])
    assert s1.domain == [-1, 1, 2]
    s2.set_clamp(True)
    assert s1.clamp is False


def test_diverging_12():
    s = d3.scale_diverging(lambda t: 2 * t + 1)
    assert s.range == [1, 2, 3]


def test_diverging_13():
    def i0(t):
        return t

    def i1(t):
        return t * 2

    s = d3.scale_diverging(i0)
    assert s.interpolator == i0
    assert s.set_interpolator(i1) == s
    assert s.interpolator == i1
    assert s(-0.5) == -1.0
    assert s(0.0) == 0.0
    assert s(0.5) == 1.0


def test_diverging_14():
    s = d3.scale_diverging().set_range([1, 3, 10])
    assert s.interpolator(0.5) == 3
    assert s.range == [1, 3, 10]


def test_diverging_15():
    s = d3.scale_diverging().set_range([1, 3, 10, 20])
    assert s.interpolator(0.5) == 3
    assert s.range == [1, 3, 10]


def test_diverging_16():
    s = d3.scale_diverging([1, 3, 10])
    assert s.interpolator(0.5) == 3
    assert s.range == [1, 3, 10]
