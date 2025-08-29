import math
from datetime import datetime

import detroit as d3


def test_identity_1():
    s = d3.scale_identity()
    assert s.get_domain() == [0, 1]
    assert s.get_range() == [0, 1]


def test_identity_2():
    s = d3.scale_identity([1, 2])
    assert s.get_domain() == [1, 2]
    assert s.get_range() == [1, 2]


def test_identity_3():
    s = d3.scale_identity().set_domain([1, 2])
    assert s(0.5) == 0.5
    assert s(1) == 1
    assert s(1.5) == 1.5
    assert s(2) == 2
    assert s(2.5) == 2.5


def test_identity_4():
    s = d3.scale_identity().set_domain([1, 2])
    assert s("2") == "2"


def test_identity_5():
    s = d3.scale_identity().set_unknown(-1)
    assert s(None) == -1
    assert s(None) == -1
    assert s(math.nan) == -1
    assert s(0.4) == 0.4


def test_identity_6():
    s = d3.scale_identity().set_domain([1, 2])
    assert s.invert(0.5) == 0.5
    assert s.invert(1) == 1
    assert s.invert(1.5) == 1.5
    assert s.invert(2) == 2
    assert s.invert(2.5) == 2.5


def test_identity_7():
    s = d3.scale_identity().set_range(["0", "2"])
    assert s.invert("1") == "1"
    s.set_range([datetime(1990, 1, 1), datetime(1991, 1, 1)])
    assert s.invert(datetime(1990, 6, 2, 13)) == datetime(1990, 6, 2, 13)
    s.set_range(["#000", "#fff"])
    assert isinstance(s.invert("#999"), str)


def test_identity_8():
    s = d3.scale_identity().set_domain([1, 2])
    assert s.invert("2") == "2"


def test_identity_9():
    s = d3.scale_identity()
    assert s.get_domain() == s.get_range()
    s.set_domain([-10, 0, 100])
    assert s.get_range() == [-10, 0, 100]
    s.set_range([-10, 0, 100])
    assert s.get_domain() == [-10, 0, 100]


def test_identity_10():
    s = d3.scale_identity()
    assert s.get_domain() == [0, 1]
    assert s.get_range() == [0, 1]
    assert s(0.5) == 0.5


def test_identity_11():
    s = d3.scale_identity().set_domain([datetime(1990, 1, 1), datetime(1991, 1, 1)])
    assert isinstance(s.get_domain()[0], datetime)
    assert isinstance(s.get_domain()[1], datetime)
    assert s.get_domain()[0] == datetime(1990, 1, 1)
    assert s.get_domain()[1] == datetime(1991, 1, 1)
    assert isinstance(s(datetime(1989, 10, 20)), datetime)
    assert s(datetime(1989, 10, 20)) == datetime(1989, 10, 20)
    s.set_domain(["0", "1"])
    assert isinstance(s.get_domain()[0], str)
    assert isinstance(s.get_domain()[1], str)
    assert s(0.5) == 0.5
    s.set_domain([0, 1])
    assert isinstance(s.get_domain()[0], int)
    assert isinstance(s.get_domain()[1], int)
    assert s(0.5) == 0.5
    s.set_range([datetime(1990, 1, 1), datetime(1991, 1, 1)])
    assert isinstance(s.get_range()[0], datetime)
    assert isinstance(s.get_range()[1], datetime)
    assert s.get_range()[0] == datetime(1990, 1, 1)
    assert s.get_range()[1] == datetime(1991, 1, 1)
    assert isinstance(s(datetime(1989, 10, 20)), datetime)
    assert s(datetime(1989, 10, 20)) == datetime(1989, 10, 20)
    s.set_range(["0", "1"])
    assert isinstance(s.get_range()[0], str)
    assert isinstance(s.get_range()[1], str)
    assert s(0.5) == 0.5
    s.set_range([0, 1])
    assert isinstance(s.get_range()[0], int)
    assert isinstance(s.get_range()[1], int)
    assert s(0.5) == 0.5


def test_identity_12():
    s = d3.scale_identity().set_domain({1, 2})
    assert s.get_domain() == [1, 2]
    assert s.get_range() == [1, 2]


def test_identity_13():
    s = d3.scale_identity().set_domain([-10, 0, 100])
    assert s.get_domain() == [-10, 0, 100]
    assert s(-5) == -5
    assert s(50) == 50
    assert s(75) == 75
    s.set_range([-10, 0, 100])
    assert s.get_range() == [-10, 0, 100]
    assert s(-5) == -5
    assert s(50) == 50
    assert s(75) == 75


def test_identity_14():
    s = d3.scale_identity().set_domain([math.inf, math.nan])
    assert s(42) == 42
    assert s.invert(-42) == -42


def test_identity_15():
    s = d3.scale_identity()
    assert list(map(s.tick_format(1), s.ticks(1))) == ["0", "1"]
    assert list(map(s.tick_format(2), s.ticks(2))) == ["0.0", "0.5", "1.0"]
    assert list(map(s.tick_format(5), s.ticks(5))) == [
        "0.0",
        "0.2",
        "0.4",
        "0.6",
        "0.8",
        "1.0",
    ]
    assert list(map(s.tick_format(10), s.ticks(10))) == [
        "0.0",
        "0.1",
        "0.2",
        "0.3",
        "0.4",
        "0.5",
        "0.6",
        "0.7",
        "0.8",
        "0.9",
        "1.0",
    ]
    s.set_domain([1, 0])
    assert list(map(s.tick_format(1), s.ticks(1))) == ["0", "1"][::-1]
    assert list(map(s.tick_format(2), s.ticks(2))) == ["0.0", "0.5", "1.0"][::-1]
    assert (
        list(map(s.tick_format(5), s.ticks(5)))
        == ["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"][::-1]
    )
    assert (
        list(map(s.tick_format(10), s.ticks(10)))
        == [
            "0.0",
            "0.1",
            "0.2",
            "0.3",
            "0.4",
            "0.5",
            "0.6",
            "0.7",
            "0.8",
            "0.9",
            "1.0",
        ][::-1]
    )


def test_identity_16():
    s = d3.scale_identity().set_domain([0.123456789, 1.23456789])
    assert s.tick_format(1)(s.ticks(1)[0]) == "1"
    assert s.tick_format(2)(s.ticks(2)[0]) == "0.5"
    assert s.tick_format(4)(s.ticks(4)[0]) == "0.2"
    assert s.tick_format(8)(s.ticks(8)[0]) == "0.2"
    assert s.tick_format(16)(s.ticks(16)[0]) == "0.15"
    assert s.tick_format(32)(s.ticks(32)[0]) == "0.15"
    assert s.tick_format(64)(s.ticks(64)[0]) == "0.14"
    assert s.tick_format(128)(s.ticks(128)[0]) == "0.13"
    assert s.tick_format(256)(s.ticks(256)[0]) == "0.125"


def test_identity_17():
    s1 = d3.scale_identity()
    s2 = s1.copy()
    s3 = s1.copy()
    s1.set_domain([1, 2])
    assert s2.get_domain() == [0, 1]
    s2.set_domain([2, 3])
    assert s1.get_domain() == [1, 2]
    assert s2.get_domain() == [2, 3]
    s4 = s3.copy()
    s3.set_range([1, 2])
    assert s4.get_range() == [0, 1]
    s4.set_range([2, 3])
    assert s3.get_range() == [1, 2]
    assert s4.get_range() == [2, 3]
