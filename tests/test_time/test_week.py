from datetime import datetime

import detroit as d3


def test_time_week_floor():
    assert d3.time_week.floor(datetime(2010, 12, 31, 23, 59, 59)) == datetime(
        2010, 12, 26
    )
    assert d3.time_week.floor(datetime(2011, 1, 1, 0, 0, 0)) == datetime(2010, 12, 26)
    assert d3.time_week.floor(datetime(2011, 1, 1, 0, 0, 1)) == datetime(2010, 12, 26)
    assert d3.time_week.floor(datetime(2011, 1, 1, 23, 59, 59)) == datetime(
        2010, 12, 26
    )
    assert d3.time_week.floor(datetime(2011, 1, 2, 0, 0, 0)) == datetime(2011, 1, 2)
    assert d3.time_week.floor(datetime(2011, 1, 2, 0, 0, 1)) == datetime(2011, 1, 2)
    assert d3.time_week.floor(datetime(2011, 3, 13, 1)) == datetime(2011, 3, 13)
    assert d3.time_week.floor(datetime(2011, 11, 6, 1)) == datetime(2011, 11, 6)
    assert d3.time_week.floor(datetime(9, 11, 6, 7)) == datetime(9, 11, 1)


def test_time_week_ceil():
    assert d3.time_week.ceil(datetime(2010, 12, 31, 23, 59, 59)) == datetime(2011, 1, 2)
    assert d3.time_week.ceil(datetime(2011, 1, 1, 0, 0, 0)) == datetime(2011, 1, 2)
    assert d3.time_week.ceil(datetime(2011, 1, 1, 0, 0, 1)) == datetime(2011, 1, 2)
    assert d3.time_week.ceil(datetime(2011, 1, 1, 23, 59, 59)) == datetime(2011, 1, 2)
    assert d3.time_week.ceil(datetime(2011, 1, 2, 0, 0, 0)) == datetime(2011, 1, 2)
    assert d3.time_week.ceil(datetime(2011, 1, 2, 0, 0, 1)) == datetime(2011, 1, 9)
    assert d3.time_week.ceil(datetime(2011, 3, 13, 1)) == datetime(2011, 3, 20)
    assert d3.time_week.ceil(datetime(2011, 11, 6, 1)) == datetime(2011, 11, 13)


def test_time_week_offset():
    assert d3.time_week.offset(datetime(2010, 12, 31, 23, 59, 59, 999), +1), datetime(
        2011, 1, 7, 23, 59, 59, 999
    )
    assert d3.time_week.offset(datetime(2010, 12, 31, 23, 59, 59, 456), -2), datetime(
        2010, 12, 17, 23, 59, 59, 456
    )
    assert d3.time_week.offset(datetime(2010, 12, 1), -1), datetime(2010, 11, 24)
    assert d3.time_week.offset(datetime(2011, 1, 1), -2), datetime(2010, 12, 18)
    assert d3.time_week.offset(datetime(2011, 1, 1), -1), datetime(2010, 12, 25)
    assert d3.time_week.offset(datetime(2010, 11, 24), +1), datetime(2010, 12, 1)
    assert d3.time_week.offset(datetime(2010, 12, 18), +2), datetime(2011, 1, 1)
    assert d3.time_week.offset(datetime(2010, 12, 25), +1), datetime(2011, 1, 1)
    assert d3.time_week.offset(datetime(2010, 12, 31, 23, 59, 59, 999), 0), datetime(
        2010, 12, 31, 23, 59, 59, 999
    )
    assert d3.time_week.offset(datetime(2010, 12, 31, 23, 59, 58, 0), 0), datetime(
        2010, 12, 31, 23, 59, 58, 0
    )


def test_time_week_range():
    assert d3.time_week.range(datetime(2010, 12, 21), datetime(2011, 1, 12)) == [
        datetime(2010, 12, 26),
        datetime(2011, 1, 2),
        datetime(2011, 1, 9),
    ]
    assert d3.time_week.range(datetime(2010, 12, 21), datetime(2011, 1, 12))[
        0
    ], datetime(2010, 12, 26)
    assert d3.time_week.range(datetime(2010, 12, 21), datetime(2011, 1, 12))[
        2
    ], datetime(2011, 1, 9)

    assert d3.time_week.range(datetime(2011, 1, 1), datetime(2011, 4, 1), 4), [
        datetime(2011, 1, 2),
        datetime(2011, 1, 30),
        datetime(2011, 2, 27),
        datetime(2011, 3, 27),
    ]

    assert d3.time_week.range(datetime(2011, 3, 1), datetime(2011, 3, 28)) == [
        datetime(2011, 3, 6),
        datetime(2011, 3, 13),
        datetime(2011, 3, 20),
        datetime(2011, 3, 27),
    ]

    assert d3.time_week.range(datetime(2011, 11, 1), datetime(2011, 11, 30)) == [
        datetime(2011, 11, 6),
        datetime(2011, 11, 13),
        datetime(2011, 11, 20),
        datetime(2011, 11, 27),
    ]


def test_time_week_every():
    assert d3.time_week.every(2).range(
        datetime(2008, 12, 3), datetime(2009, 2, 5), 2
    ) == [
        datetime(2008, 12, 7),
        datetime(2008, 12, 21),
        datetime(2009, 1, 4),
        datetime(2009, 1, 18),
        datetime(2009, 2, 1),
    ]
