import detroit as d3
from datetime import datetime
import pytest


def test_time_ticks_test_1():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 12, 1, 0), datetime(2011, 1, 1, 12, 4, 4), d3.time_minute
    ) == [
        datetime(2011, 1, 1, 12, 1),
        datetime(2011, 1, 1, 12, 2),
        datetime(2011, 1, 1, 12, 3),
        datetime(2011, 1, 1, 12, 4),
    ]


def test_time_ticks_test_2():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 33, 4),
        d3.time_minute.every(10),
    ) == [
        datetime(2011, 1, 1, 12, 0),
        datetime(2011, 1, 1, 12, 10),
        datetime(2011, 1, 1, 12, 20),
        datetime(2011, 1, 1, 12, 30),
    ]


def test_time_ticks_test_3():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 0, 1), 4
    ) == [
        datetime(2011, 1, 1, 12, 0, 0, 0),
        datetime(2011, 1, 1, 12, 0, 0, 200000),
        datetime(2011, 1, 1, 12, 0, 0, 400000),
        datetime(2011, 1, 1, 12, 0, 0, 600000),
        datetime(2011, 1, 1, 12, 0, 0, 800000),
        datetime(2011, 1, 1, 12, 0, 1, 0),
    ]


def test_time_ticks_test_4():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 0, 4), 4
    ) == [
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 0, 1),
        datetime(2011, 1, 1, 12, 0, 2),
        datetime(2011, 1, 1, 12, 0, 3),
        datetime(2011, 1, 1, 12, 0, 4),
    ]


def test_time_ticks_test_5():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 0, 20), 4
    ) == [
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 0, 5),
        datetime(2011, 1, 1, 12, 0, 10),
        datetime(2011, 1, 1, 12, 0, 15),
        datetime(2011, 1, 1, 12, 0, 20),
    ]


def test_time_ticks_test_6():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 0, 50), 4
    ) == [
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 0, 15),
        datetime(2011, 1, 1, 12, 0, 30),
        datetime(2011, 1, 1, 12, 0, 45),
    ]


def test_time_ticks_test_7():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 1, 50), 4
    ) == [
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 0, 30),
        datetime(2011, 1, 1, 12, 1, 0),
        datetime(2011, 1, 1, 12, 1, 30),
    ]


def test_time_ticks_test_8():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 12, 0, 27), datetime(2011, 1, 1, 12, 4, 12), 4
    ) == [
        datetime(2011, 1, 1, 12, 1),
        datetime(2011, 1, 1, 12, 2),
        datetime(2011, 1, 1, 12, 3),
        datetime(2011, 1, 1, 12, 4),
    ]


def test_time_ticks_test_9():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 12, 3, 27), datetime(2011, 1, 1, 12, 21, 12), 4
    ) == [
        datetime(2011, 1, 1, 12, 5),
        datetime(2011, 1, 1, 12, 10),
        datetime(2011, 1, 1, 12, 15),
        datetime(2011, 1, 1, 12, 20),
    ]


def test_time_ticks_test_10():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 12, 8, 27), datetime(2011, 1, 1, 13, 4, 12), 4
    ) == [
        datetime(2011, 1, 1, 12, 15),
        datetime(2011, 1, 1, 12, 30),
        datetime(2011, 1, 1, 12, 45),
        datetime(2011, 1, 1, 13, 0),
    ]


def test_time_ticks_test_11():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 12, 28, 27), datetime(2011, 1, 1, 14, 4, 12), 4
    ) == [
        datetime(2011, 1, 1, 12, 30),
        datetime(2011, 1, 1, 13, 0),
        datetime(2011, 1, 1, 13, 30),
        datetime(2011, 1, 1, 14, 0),
    ]


def test_time_ticks_test_12():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 12, 28, 27), datetime(2011, 1, 1, 16, 34, 12), 4
    ), [
        datetime(2011, 1, 1, 13, 0),
        datetime(2011, 1, 1, 14, 0),
        datetime(2011, 1, 1, 15, 0),
        datetime(2011, 1, 1, 16, 0),
    ]


def test_time_ticks_test_13():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 14, 28, 27), datetime(2011, 1, 2, 1, 34, 12), 4
    ), [
        datetime(2011, 1, 1, 15, 0),
        datetime(2011, 1, 1, 18, 0),
        datetime(2011, 1, 1, 21, 0),
        datetime(2011, 1, 2, 0, 0),
    ]


def test_time_ticks_test_14():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 16, 28, 27), datetime(2011, 1, 2, 14, 34, 12), 4
    ) == [
        datetime(2011, 1, 1, 18, 0),
        datetime(2011, 1, 2, 0, 0),
        datetime(2011, 1, 2, 6, 0),
        datetime(2011, 1, 2, 12, 0),
    ]


def test_time_ticks_test_15():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 16, 28, 27), datetime(2011, 1, 3, 21, 34, 12), 4
    ) == [
        datetime(2011, 1, 2, 0, 0),
        datetime(2011, 1, 2, 12, 0),
        datetime(2011, 1, 3, 0, 0),
        datetime(2011, 1, 3, 12, 0),
    ]


def test_time_ticks_test_16():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 16, 28, 27), datetime(2011, 1, 5, 21, 34, 12), 4
    ) == [
        datetime(2011, 1, 2, 0, 0),
        datetime(2011, 1, 3, 0, 0),
        datetime(2011, 1, 4, 0, 0),
        datetime(2011, 1, 5, 0, 0),
    ]


def test_time_ticks_test_17():
    assert d3.time_ticks(
        datetime(2011, 1, 2, 16, 28, 27), datetime(2011, 1, 9, 21, 34, 12), 4
    ) == [
        datetime(2011, 1, 3, 0, 0),
        datetime(2011, 1, 5, 0, 0),
        datetime(2011, 1, 7, 0, 0),
        datetime(2011, 1, 9, 0, 0),
    ]


def test_time_ticks_test_18():
    assert d3.time_ticks(
        datetime(2011, 1, 1, 16, 28, 27), datetime(2011, 1, 23, 21, 34, 12), 4
    ) == [
        datetime(2011, 1, 2, 0, 0),
        datetime(2011, 1, 9, 0, 0),
        datetime(2011, 1, 16, 0, 0),
        datetime(2011, 1, 23, 0, 0),
    ]


def test_time_ticks_test_19():
    assert d3.time_ticks(datetime(2011, 1, 18), datetime(2011, 5, 2), 4) == [
        datetime(2011, 2, 1, 0, 0),
        datetime(2011, 3, 1, 0, 0),
        datetime(2011, 4, 1, 0, 0),
        datetime(2011, 5, 1, 0, 0),
    ]


def test_time_ticks_test_20():
    assert d3.time_ticks(datetime(2010, 12, 18), datetime(2011, 11, 2), 4) == [
        datetime(2011, 1, 1, 0, 0),
        datetime(2011, 4, 1, 0, 0),
        datetime(2011, 7, 1, 0, 0),
        datetime(2011, 10, 1, 0, 0),
    ]


def test_time_ticks_test_21():
    assert d3.time_ticks(datetime(2010, 12, 18), datetime(2014, 3, 2), 4) == [
        datetime(2011, 1, 1, 0, 0),
        datetime(2012, 1, 1, 0, 0),
        datetime(2013, 1, 1, 0, 0),
        datetime(2014, 1, 1, 0, 0),
    ]


def test_time_ticks_test_22():
    with pytest.raises(ValueError):
        assert d3.time_ticks(datetime(1, 12, 18), datetime(2014, 3, 2), 6) == [
            datetime(500, 1, 1, 0, 0),
            datetime(1000, 1, 1, 0, 0),
            datetime(1500, 1, 1, 0, 0),
            datetime(2000, 1, 1, 0, 0),
        ]


def test_time_ticks_test_23():
    assert d3.time_ticks(datetime(2014, 3, 2), datetime(2014, 3, 2), 6) == [
        datetime(2014, 3, 2)
    ]
    assert d3.time_ticks(datetime(2014, 3, 2), datetime(2010, 12, 18), 4) == [
        datetime(2014, 1, 1, 0, 0),
        datetime(2013, 1, 1, 0, 0),
        datetime(2012, 1, 1, 0, 0),
        datetime(2011, 1, 1, 0, 0),
    ]
    assert d3.time_ticks(datetime(2011, 11, 2), datetime(2010, 12, 18), 4) == [
        datetime(2011, 10, 1, 0, 0),
        datetime(2011, 7, 1, 0, 0),
        datetime(2011, 4, 1, 0, 0),
        datetime(2011, 1, 1, 0, 0),
    ]
