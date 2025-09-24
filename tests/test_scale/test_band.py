import math

import pytest

import detroit as d3


def test_band_1():
    s = d3.scale_band()
    assert s.get_domain() == []
    assert s.get_range() == [0, 1]
    assert s.get_bandwidth() == 1
    assert s.get_step() == 1
    assert s.get_round() is False
    assert s.get_padding_inner() == 0
    assert s.get_padding_outer() == 0
    assert s.get_align() == 0.5


def test_band_2():
    s = d3.scale_band([0, 960])
    assert s("foo") is None
    s.set_domain(["foo", "bar"])
    assert s("foo") == 0
    assert s("bar") == 480
    s.set_domain(["a", "b", "c"]).set_range([0, 120])
    assert list(map(s, s.get_domain())) == [0, 40, 80]
    assert s.get_bandwidth() == 40
    s.set_padding(0.2)
    assert list(map(s, s.get_domain())) == [7.5, 45, 82.5]
    assert s.get_bandwidth() == 30


def test_band_3():
    s = d3.scale_band(["a", "b", "c"], [0, 1])
    assert s("d") is None
    assert s("e") is None
    assert s("f") is None


def test_band_4():
    s = d3.scale_band(["a", "b", "c"], [0, 1])
    s("d")
    s("e")
    assert s.get_domain() == ["a", "b", "c"]


def test_band_5():
    s = d3.scale_band([0, 960])
    assert s.set_domain(["foo"]).get_step() == 960
    assert s.set_domain(["foo", "bar"]).get_step() == 480
    assert s.set_domain(["foo", "bar", "baz"]).get_step() == 320
    s.set_padding(0.5)
    assert s.set_domain(["foo"]).get_step() == 640
    assert s.set_domain(["foo", "bar"]).get_step() == 384


def test_band_6():
    s = d3.scale_band([0, 960])
    assert s.set_domain([]).get_bandwidth() == 960
    assert s.set_domain(["foo"]).get_bandwidth() == 960
    assert s.set_domain(["foo", "bar"]).get_bandwidth() == 480
    assert s.set_domain(["foo", "bar", "baz"]).get_bandwidth() == 320
    s.set_padding(0.5)
    assert s.set_domain([]).get_bandwidth() == 480
    assert s.set_domain(["foo"]).get_bandwidth() == 320
    assert s.set_domain(["foo", "bar"]).get_bandwidth() == 192


def test_band_7():
    s = d3.scale_band([0, 960]).set_domain([])
    assert s.get_step() == 960
    assert s.get_bandwidth() == 960
    s.set_padding(0.5)
    assert s.get_step() == 960
    assert s.get_bandwidth() == 480
    s.set_padding(1)
    assert s.get_step() == 960
    assert s.get_bandwidth() == 0


def test_band_8():
    s = d3.scale_band([0, 960]).set_domain(["foo"])
    assert s("foo") == 0
    assert s.get_step() == 960
    assert s.get_bandwidth() == 960
    s.set_padding(0.5)
    assert s("foo") == 320
    assert s.get_step() == 640
    assert s.get_bandwidth() == 320
    s.set_padding(1)
    assert s("foo") == 480
    assert s.get_step() == 480
    assert s.get_bandwidth() == 0


def test_band_9():
    s = d3.scale_band().set_domain(["a", "b", "c"]).set_range_round([0, 100])
    assert list(map(s, s.get_domain())) == [0, 33, 66]
    assert s.get_bandwidth() == 33
    s.set_domain(["a", "b", "c", "d"])
    assert list(map(s, s.get_domain())) == [0, 25, 50, 75]
    assert s.get_bandwidth() == 25


def test_band_10():
    assert sorted(d3.scale_band().set_domain({"a", "b", "c"}).get_domain()) == sorted(
        ["a", "b", "c"]
    )


def test_band_11():
    domain = ["red", "green"]
    s = d3.scale_band().set_domain(domain)
    domain.append("blue")
    assert s.get_domain() == ["red", "green"]


def test_band_12():
    s = d3.scale_band().set_domain(["red", "green"])
    domain = s.get_domain()
    assert domain == ["red", "green"]
    domain.append("blue")
    assert s.get_domain() == ["red", "green"]


def test_band_13():
    s = d3.scale_band().set_domain(["a", "b", "c"]).set_range([120, 0])
    assert list(map(s, s.get_domain())) == [80, 40, 0]
    assert s.get_bandwidth() == 40
    s.set_padding(0.2)
    assert list(map(s, s.get_domain())) == [82.5, 45, 7.5]
    assert s.get_bandwidth() == 30


def test_band_14():
    range_ = [1, 2]
    s = d3.scale_band().set_range(range_)
    range_.append("blue")
    assert s.get_range() == [1, 2]


def test_band_15():
    s = d3.scale_band().set_range([1, 2])
    range_ = s.get_range()
    assert range_ == [1, 2]
    range_.append("blue")
    assert s.get_range() == [1, 2]


def test_band_16():
    s = d3.scale_band().set_range({1, 2})
    assert s.get_range() == [1, 2]


def test_band_17():
    s = d3.scale_band().set_range_round({1, 2})
    assert s.get_range() == [1, 2]


def test_band_18():
    s = d3.scale_band().set_range(["1.0", "2.0"])
    assert s.get_range() == [1, 2]


def test_band_19():
    s = d3.scale_band().set_range_round(["1.0", "2.0"])
    assert s.get_range() == [1, 2]


def test_band_20():
    s = (
        d3.scale_band()
        .set_domain(["a", "b", "c"])
        .set_range([120, 0])
        .set_padding_inner(0.1)
        .set_round(True)
    )
    assert list(map(s, s.get_domain())) == [83, 42, 1]
    assert s.get_bandwidth() == 37
    s.set_padding_inner(0.2)
    assert list(map(s, s.get_domain())) == [85, 43, 1]
    assert s.get_bandwidth() == 34


def test_band_21():
    s = d3.scale_band()
    assert s.set_padding_inner("1.0").get_padding_inner() == 1
    assert s.set_padding_inner("-1.0").get_padding_inner() == -1
    assert s.set_padding_inner("2.0").get_padding_inner() == 1
    assert s.set_padding_inner(math.nan).get_padding_inner() == 1


def test_band_22():
    s = (
        d3.scale_band()
        .set_domain(["a", "b", "c"])
        .set_range([120, 0])
        .set_padding_inner(0.2)
        .set_padding_outer(0.1)
    )
    assert list(map(s, s.get_domain())) == [84, 44, 4]
    assert s.get_bandwidth() == 32
    s.set_padding_outer(1)
    assert list(map(s, s.get_domain())) == [75, 50, 25]
    assert s.get_bandwidth() == 20


def test_band_23():
    s = d3.scale_band()
    assert s.set_padding_outer("1.0").get_padding_outer() == 1
    assert s.set_padding_outer("-1.0").get_padding_outer() == -1
    assert s.set_padding_outer("2.0").get_padding_outer() == 2
    assert math.isnan(s.set_padding_outer(math.nan).get_padding_outer())


def test_band_24():
    s = d3.scale_band().set_domain(["a", "b", "c"]).set_range_round([0, 100])
    assert s.get_range() == [0, 100]
    assert s.get_round() is True


def test_band_25():
    s = d3.scale_band().set_domain(["a", "b", "c"]).set_range([0, 100]).set_round(True)
    assert list(map(s, s.get_domain())) == [0, 33, 66]
    assert s.get_bandwidth() == 33
    s.set_padding(0.2)
    assert list(map(s, s.get_domain())) == [7, 38, 69]
    assert s.get_bandwidth() == 25


def test_band_26():
    s1 = (
        d3.scale_band()
        .set_domain(["red", "green"])
        .set_range([1, 2])
        .set_round(True)
        .set_padding_inner(0.1)
        .set_padding_outer(0.2)
    )
    s2 = s1.copy()
    assert s2.get_domain() == s1.get_domain()
    assert s2.get_range() == s1.get_range()
    assert s2.get_round() == s1.get_round()
    assert s2.get_padding_inner() == s1.get_padding_inner()
    assert s2.get_padding_outer() == s1.get_padding_outer()


def test_band_27():
    s1 = d3.scale_band().set_domain(["foo", "bar"]).set_range([0, 2])
    s2 = s1.copy()
    s1.set_domain(["red", "blue"])
    assert s2.get_domain() == ["foo", "bar"]
    assert list(map(s1, s1.get_domain())) == [0, 1]
    assert list(map(s2, s2.get_domain())) == [0, 1]
    s2.set_domain(["red", "blue"])
    assert s1.get_domain() == ["red", "blue"]
    assert list(map(s1, s1.get_domain())) == [0, 1]
    assert list(map(s2, s2.get_domain())) == [0, 1]


def test_band_28():
    s1 = d3.scale_band().set_domain(["foo", "bar"]).set_range([0, 2])
    s2 = s1.copy()
    s1.set_range([3, 5])
    assert s2.get_range() == [0, 2]
    assert list(map(s1, s1.get_domain())) == [3, 4]
    assert list(map(s2, s2.get_domain())) == [0, 1]
    s2.set_range([5, 7])
    assert s1.get_range() == [3, 5]
    assert list(map(s1, s1.get_domain())) == [3, 4]
    assert list(map(s2, s2.get_domain())) == [5, 6]
