from datetime import datetime

import detroit as d3


def test_time_month_floor():
    assert d3.time_month.floor(datetime(2010, 12, 31, 23, 59, 59)) == datetime(
        2010, 12, 1
    )
    assert d3.time_month.floor(datetime(2011, 1, 1, 0, 0, 0)) == datetime(2011, 1, 1)
    assert d3.time_month.floor(datetime(2011, 1, 1, 0, 0, 1)) == datetime(2011, 1, 1)
    assert d3.time_month.floor(datetime(2011, 3, 13, 1)) == datetime(2011, 3, 1)
    assert d3.time_month.floor(datetime(2011, 11, 6, 1)) == datetime(2011, 11, 1)
    assert d3.time_month.floor(datetime(9, 11, 6, 7)) == datetime(9, 11, 1)
    assert d3.time_month.floor(datetime(2010, 12, 31, 23)) == datetime(2010, 12, 1)
    assert d3.time_month.floor(datetime(2011, 1, 1, 0)) == datetime(2011, 1, 1)
    assert d3.time_month.floor(datetime(2011, 1, 1, 1)) == datetime(2011, 1, 1)
    assert d3.time_month.floor(datetime(2011, 3, 13, 7)) == datetime(2011, 3, 1)
    assert d3.time_month.floor(datetime(2011, 3, 13, 8)) == datetime(2011, 3, 1)
    assert d3.time_month.floor(datetime(2011, 3, 13, 9)) == datetime(2011, 3, 1)
    assert d3.time_month.floor(datetime(2011, 3, 13, 10)) == datetime(2011, 3, 1)
    assert d3.time_month.floor(datetime(2011, 11, 6, 7)) == datetime(2011, 11, 1)
    assert d3.time_month.floor(datetime(2011, 11, 6, 8)) == datetime(2011, 11, 1)
    assert d3.time_month.floor(datetime(2011, 11, 6, 9)) == datetime(2011, 11, 1)
    assert d3.time_month.floor(datetime(2011, 11, 6, 10)) == datetime(2011, 11, 1)
    assert d3.time_month.floor(datetime(9, 11, 6, 7)) == datetime(9, 11, 1)


def test_time_month_ceil():
    assert d3.time_month.ceil(datetime(2010, 12, 31, 23, 59, 59)) == datetime(
        2011, 1, 1
    )
    assert d3.time_month.ceil(datetime(2011, 1, 1, 0, 0, 0)) == datetime(2011, 1, 1)
    assert d3.time_month.ceil(datetime(2011, 1, 1, 0, 0, 1)) == datetime(2011, 2, 1)
    assert d3.time_month.ceil(datetime(2011, 3, 13, 1)) == datetime(2011, 4, 1)
    assert d3.time_month.ceil(datetime(2011, 11, 6, 1)) == datetime(2011, 12, 1)
    assert d3.time_month.ceil(datetime(2010, 11, 30, 23)) == datetime(2010, 12, 1)
    assert d3.time_month.ceil(datetime(2010, 12, 1, 1)) == datetime(2011, 1, 1)
    assert d3.time_month.ceil(datetime(2011, 2, 1)) == datetime(2011, 2, 1)
    assert d3.time_month.ceil(datetime(2011, 3, 1)) == datetime(2011, 3, 1)
    assert d3.time_month.ceil(datetime(2011, 4, 1)) == datetime(2011, 4, 1)
    assert d3.time_month.ceil(datetime(2011, 3, 13, 7)) == datetime(2011, 4, 1)
    assert d3.time_month.ceil(datetime(2011, 3, 13, 8)) == datetime(2011, 4, 1)
    assert d3.time_month.ceil(datetime(2011, 3, 13, 9)) == datetime(2011, 4, 1)
    assert d3.time_month.ceil(datetime(2011, 3, 13, 10)) == datetime(2011, 4, 1)
    assert d3.time_month.ceil(datetime(2011, 11, 6, 7)) == datetime(2011, 12, 1)
    assert d3.time_month.ceil(datetime(2011, 11, 6, 8)) == datetime(2011, 12, 1)
    assert d3.time_month.ceil(datetime(2011, 11, 6, 9)) == datetime(2011, 12, 1)
    assert d3.time_month.ceil(datetime(2011, 11, 6, 10)) == datetime(2011, 12, 1)
    assert d3.time_month.ceil(datetime(2012, 3, 1, 0)) == datetime(2012, 3, 1)
    assert d3.time_month.ceil(datetime(2012, 3, 1, 0)) == datetime(2012, 3, 1)


def test_time_month_offset():
    assert d3.time_month.offset(datetime(2010, 12, 31, 23, 59, 59, 999), +1), datetime(
        2011, 1, 31, 23, 59, 59, 999
    )
    assert d3.time_month.offset(datetime(2010, 12, 31, 23, 59, 59, 456), -2), datetime(
        2010, 10, 31, 23, 59, 59, 456
    )
    assert d3.time_month.offset(datetime(2010, 12, 1), -1), datetime(2010, 11, 1)
    assert d3.time_month.offset(datetime(2011, 1, 1), -2), datetime(2010, 11, 1)
    assert d3.time_month.offset(datetime(2011, 1, 1), -1), datetime(2010, 12, 1)
    assert d3.time_month.offset(datetime(2010, 11, 1), +1), datetime(2010, 12, 1)
    assert d3.time_month.offset(datetime(2010, 11, 1), +2), datetime(2011, 1, 1)
    assert d3.time_month.offset(datetime(2010, 12, 1), +1), datetime(2011, 1, 1)
    assert d3.time_month.offset(datetime(2010, 12, 31, 23, 59, 59, 999), 0), datetime(
        2010, 12, 31, 23, 59, 59, 999
    )
    assert d3.time_month.offset(datetime(2010, 12, 31, 23, 59, 58, 0), 0), datetime(
        2010, 12, 31, 23, 59, 58, 0
    )
    assert d3.time_month.offset(datetime(2010, 12, 31, 23, 59, 59, 999), +1), datetime(
        2011, 1, 31, 23, 59, 59, 999
    )
    assert d3.time_month.offset(datetime(2010, 12, 31, 23, 59, 59, 456), -2), datetime(
        2010, 10, 31, 23, 59, 59, 456
    )
    assert d3.time_month.offset(datetime(2010, 12, 31), -1), datetime(2010, 11, 31)
    assert d3.time_month.offset(datetime(2011, 1, 1), -2), datetime(2010, 11, 1)
    assert d3.time_month.offset(datetime(2011, 1, 1), -1), datetime(2010, 12, 1)
    assert d3.time_month.offset(datetime(2010, 12, 31), +1), datetime(2011, 1, 31)
    assert d3.time_month.offset(datetime(2010, 12, 30), +2), datetime(2011, 2, 30)
    assert d3.time_month.offset(datetime(2010, 12, 30), +1), datetime(2011, 1, 30)
    assert d3.time_month.offset(datetime(2010, 12, 31, 23, 59, 59, 999), 0), datetime(
        2010, 12, 31, 23, 59, 59, 999
    )
    assert d3.time_month.offset(datetime(2010, 12, 31, 23, 59, 58, 0), 0), datetime(
        2010, 12, 31, 23, 59, 58, 0
    )


def test_time_month_round():
    assert d3.time_month.round(datetime(2010, 12, 16, 12)) == datetime(2011, 1, 1)
    assert d3.time_month.round(datetime(2010, 12, 16, 11)) == datetime(2010, 12, 1)
    assert d3.time_month.round(datetime(2011, 3, 13, 7)) == datetime(2011, 3, 1)
    assert d3.time_month.round(datetime(2011, 3, 13, 8)) == datetime(2011, 3, 1)
    assert d3.time_month.round(datetime(2011, 3, 13, 9)) == datetime(2011, 3, 1)
    assert d3.time_month.round(datetime(2011, 3, 13, 20)) == datetime(2011, 3, 1)
    assert d3.time_month.round(datetime(2011, 11, 6, 7)) == datetime(2011, 11, 1)
    assert d3.time_month.round(datetime(2011, 11, 6, 8)) == datetime(2011, 11, 1)
    assert d3.time_month.round(datetime(2011, 11, 6, 9)) == datetime(2011, 11, 1)
    assert d3.time_month.round(datetime(2011, 11, 6, 20)) == datetime(2011, 11, 1)
    assert d3.time_month.round(datetime(2012, 3, 1, 0)) == datetime(2012, 3, 1)
    assert d3.time_month.round(datetime(2012, 3, 1, 0)) == datetime(2012, 3, 1)


def test_time_month_range():
    assert d3.time_month.range(datetime(2011, 12, 1), datetime(2012, 6, 1)) == [
        datetime(2011, 12, 1),
        datetime(2012, 1, 1),
        datetime(2012, 2, 1),
        datetime(2012, 3, 1),
        datetime(2012, 4, 1),
        datetime(2012, 5, 1),
    ]
    assert d3.time_month.range(datetime(2011, 11, 4, 2), datetime(2012, 5, 10, 13)) == [
        datetime(2011, 12, 1),
        datetime(2012, 1, 1),
        datetime(2012, 2, 1),
        datetime(2012, 3, 1),
        datetime(2012, 4, 1),
        datetime(2012, 5, 1),
    ]
    assert d3.time_month.range(datetime(2011, 11, 4), datetime(2012, 2, 7)) == [
        datetime(2011, 12, 1),
        datetime(2012, 1, 1),
        datetime(2012, 2, 1),
    ]
    assert d3.time_month.range(datetime(2011, 12, 10), datetime(2011, 11, 4)) == []
    assert d3.time_month.range(datetime(2011, 11, 1), datetime(2011, 11, 1)) == []
    assert d3.time_month.range(datetime(2010, 11, 30), datetime(2011, 3, 1)) == [
        datetime(2010, 12, 1),
        datetime(2011, 1, 1),
        datetime(2011, 2, 1),
    ]
    assert d3.time_month.range(datetime(2010, 11, 30), datetime(2011, 3, 1))[0], (
        datetime(2010, 12, 1)
    )
    assert d3.time_month.range(datetime(2010, 11, 30), datetime(2011, 3, 1))[2], (
        datetime(2011, 2, 1)
    )
    assert d3.time_month.range(datetime(2011, 2, 1), datetime(2012, 2, 1), 3) == [
        datetime(2011, 2, 1),
        datetime(2011, 5, 1),
        datetime(2011, 8, 1),
        datetime(2011, 11, 1),
    ]
    assert d3.time_month.range(datetime(2011, 1, 1), datetime(2011, 5, 1)) == [
        datetime(2011, 1, 1),
        datetime(2011, 2, 1),
        datetime(2011, 3, 1),
        datetime(2011, 4, 1),
    ]
    assert d3.time_month.range(datetime(2011, 10, 1), datetime(2012, 2, 1)) == [
        datetime(2011, 10, 1),
        datetime(2011, 11, 1),
        datetime(2011, 12, 1),
        datetime(2012, 1, 1),
    ]


def test_time_month_count():
    assert d3.time_month.count(datetime(2011, 1, 1), datetime(2011, 5, 1)) == 4
    assert d3.time_month.count(datetime(2011, 1, 1), datetime(2011, 4, 30)) == 3
    assert d3.time_month.count(datetime(2010, 12, 31), datetime(2011, 4, 30)) == 4
    assert d3.time_month.count(datetime(2010, 12, 31), datetime(2011, 5, 1)) == 5
    assert d3.time_month.count(datetime(2009, 12, 31), datetime(2012, 5, 1)) == 29
    assert d3.time_month.count(datetime(2012, 5, 1), datetime(2009, 12, 31)) == -29


def test_time_month_every():
    assert d3.time_month.every(3).range(
        datetime(2008, 12, 3), datetime(2010, 7, 5)
    ) == [
        datetime(2009, 1, 1),
        datetime(2009, 4, 1),
        datetime(2009, 7, 1),
        datetime(2009, 10, 1),
        datetime(2010, 1, 1),
        datetime(2010, 4, 1),
        datetime(2010, 7, 1),
    ]
