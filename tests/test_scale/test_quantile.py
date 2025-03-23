import math

import detroit as d3


def test_quantile_1():
    s = d3.scale_quantile()
    assert s.get_domain() == []
    assert s.get_range() == []
    assert s.get_unknown() is None


def test_quantile_2():
    s = (
        d3.scale_quantile()
        .set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
        .set_range([0, 1, 2, 3])
    )
    assert list(map(s, [3, 6, 6.9, 7, 7.1])) == [0, 0, 0, 0, 0]
    assert list(map(s, [8, 8.9])) == [1, 1]
    assert list(map(s, [9, 9.1, 10, 13])) == [2, 2, 2, 2]
    assert list(map(s, [14.9, 15, 15.1, 16, 20])) == [3, 3, 3, 3, 3]
    s.set_domain([3, 6, 7, 8, 8, 9, 10, 13, 15, 16, 20]).set_range([0, 1, 2, 3])
    assert list(map(s, [3, 6, 6.9, 7, 7.1])) == [0, 0, 0, 0, 0]
    assert list(map(s, [8, 8.9])) == [1, 1]
    assert list(map(s, [9, 9.1, 10, 13])) == [2, 2, 2, 2]
    assert list(map(s, [14.9, 15, 15.1, 16, 20])) == [3, 3, 3, 3, 3]


def test_quantile_3():
    s = (
        d3.scale_quantile()
        .set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
        .set_range([0, 1, 2, 3])
    )
    assert s(math.nan) is None


def test_quantile_4():
    s = d3.scale_quantile().set_domain([6, 3, 7, 8, 8, 13, 20, 15, 16, 10])
    assert s.get_domain() == [3, 6, 7, 8, 8, 10, 13, 15, 16, 20]


def test_quantile_5():
    s = d3.scale_quantile().set_domain(["6", "13", "20"])
    assert s.get_domain() == [6, 13, 20]


def test_quantile_6():
    s = d3.scale_quantile().set_domain({6, 13, 20})
    assert s.get_domain() == [6, 13, 20]


def test_quantile_7():
    s = d3.scale_quantile().set_domain([1, 2, 0, 0, None])
    assert s.get_domain() == [0, 0, 1, 2]


def test_quantile_8():
    s = d3.scale_quantile().set_domain(
        [6, 3, math.nan, None, 7, 8, 8, 13, None, 20, 15, 16, 10, math.nan]
    )
    assert s.get_domain() == [3, 6, 7, 8, 8, 10, 13, 15, 16, 20]


def test_quantile_9():
    s = (
        d3.scale_quantile()
        .set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
        .set_range([0, 1, 2, 3])
    )
    assert s.get_quantiles() == [7.25, 9, 14.5]
    s.set_domain([3, 6, 7, 8, 8, 9, 10, 13, 15, 16, 20]).set_range([0, 1, 2, 3])
    assert s.get_quantiles() == [7.5, 9, 14]


def test_quantile_10():
    s = d3.scale_quantile().set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
    assert s.set_range([0, 1, 2, 3]).get_quantiles() == [7.25, 9, 14.5]
    assert s.set_range([0, 1]).get_quantiles() == [9]


def test_quantile_11():
    s = (
        d3.scale_quantile()
        .set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
        .set_range({0, 1, 2, 3})
    )
    assert s.get_range() == [0, 1, 2, 3]


def test_quantile_12():
    a = "a"
    b = "b"
    c = "c"
    s = (
        d3.scale_quantile()
        .set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
        .set_range([a, b, c, a])
    )
    assert list(map(s, [3, 6, 6.9, 7, 7.1])) == [a, a, a, a, a]
    assert list(map(s, [8, 8.9])) == [b, b]
    assert list(map(s, [9, 9.1, 10, 13])) == [c, c, c, c]
    assert list(map(s, [14.9, 15, 15.1, 16, 20])) == [a, a, a, a, a]


def test_quantile_13():
    s = (
        d3.scale_quantile()
        .set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
        .set_range([0, 1, 2, 3])
    )
    assert s.invert_extent(0) == [3, 7.25]
    assert s.invert_extent(1) == [7.25, 9]
    assert s.invert_extent(2) == [9, 14.5]
    assert s.invert_extent(3) == [14.5, 20]


def test_quantile_14():
    a = "a"
    b = "b"
    s = (
        d3.scale_quantile()
        .set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
        .set_range([a, b])
    )
    assert s.invert_extent(a) == [3, 9]
    assert s.invert_extent(b) == [9, 20]


def test_quantile_15():
    s = d3.scale_quantile().set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
    assert all(map(math.isnan, s.invert_extent(-1)))
    assert all(map(math.isnan, s.invert_extent(0.5)))
    assert all(map(math.isnan, s.invert_extent(2)))
    assert all(map(math.isnan, s.invert_extent("a")))


def test_quantile_16():
    s = (
        d3.scale_quantile()
        .set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
        .set_range([0, 1, 2, 0])
    )
    assert s.invert_extent(0) == [3, 7.25]
    assert s.invert_extent(1) == [7.25, 9]
    assert s.invert_extent(2) == [9, 14.5]


def test_quantile_17():
    s = (
        d3.scale_quantile()
        .set_domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
        .set_range([0, 1, 2, 3])
        .set_unknown(-1)
    )
    assert s(None) == -1
    assert s(None) == -1
    assert s(math.nan) == -1
    assert s(2) == 0
    assert s(3) == 0
    assert s(21) == 3
