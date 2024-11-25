import detroit as d3
from datetime import datetime


def test_time_sunday_floor():
    assert d3.time_sunday.floor(datetime(2010, 12, 31, 23, 59, 59)) == datetime(
        2010, 12, 26
    )
    assert d3.time_sunday.floor(datetime(2011, 1, 1, 0, 0, 0)) == datetime(2010, 12, 26)
    assert d3.time_sunday.floor(datetime(2011, 1, 1, 0, 0, 1)) == datetime(2010, 12, 26)
    assert d3.time_sunday.floor(datetime(2011, 1, 1, 23, 59, 59)) == datetime(
        2010, 12, 26
    )
    assert d3.time_sunday.floor(datetime(2011, 1, 2, 0, 0, 0)) == datetime(2011, 1, 2)
    assert d3.time_sunday.floor(datetime(2011, 1, 2, 0, 0, 1)) == datetime(2011, 1, 2)
    assert d3.time_sunday.floor(datetime(2011, 3, 13, 1)) == datetime(2011, 3, 13)
    assert d3.time_sunday.floor(datetime(2011, 11, 6, 1)) == datetime(2011, 11, 6)
    assert d3.time_sunday.floor(datetime(9, 11, 6, 7)) == datetime(9, 11, 1)
    assert d3.time_sunday.ceil(datetime(2010, 12, 31, 23, 59, 59)) == datetime(
        2011, 1, 2
    )
    assert d3.time_sunday.ceil(datetime(2011, 1, 1, 0, 0, 0)) == datetime(2011, 1, 2)
    assert d3.time_sunday.ceil(datetime(2011, 1, 1, 0, 0, 1)) == datetime(2011, 1, 2)
    assert d3.time_sunday.ceil(datetime(2011, 1, 1, 23, 59, 59)) == datetime(2011, 1, 2)
    assert d3.time_sunday.ceil(datetime(2011, 1, 2, 0, 0, 0)) == datetime(2011, 1, 2)
    assert d3.time_sunday.ceil(datetime(2011, 1, 2, 0, 0, 1)) == datetime(2011, 1, 9)


def test_time_sunday_ceil():
    assert d3.time_sunday.ceil(datetime(2011, 3, 13, 1)) == datetime(2011, 3, 20)
    assert d3.time_sunday.ceil(datetime(2011, 11, 6, 1)) == datetime(2011, 11, 13)


def test_time_sunday_offset():
    assert d3.time_sunday.offset(datetime(2010, 12, 31, 23, 59, 59, 999), +1), datetime(
        2011, 1, 7, 23, 59, 59, 999
    )
    assert d3.time_sunday.offset(datetime(2010, 12, 31, 23, 59, 59, 456), -2), datetime(
        2010, 12, 17, 23, 59, 59, 456
    )
    assert d3.time_sunday.offset(datetime(2010, 12, 1), -1), datetime(2010, 11, 24)
    assert d3.time_sunday.offset(datetime(2011, 1, 1), -2), datetime(2010, 12, 18)
    assert d3.time_sunday.offset(datetime(2011, 1, 1), -1), datetime(2010, 12, 25)
    assert d3.time_sunday.offset(datetime(2010, 11, 24), +1), datetime(2010, 12, 1)
    assert d3.time_sunday.offset(datetime(2010, 12, 18), +2), datetime(2011, 1, 1)
    assert d3.time_sunday.offset(datetime(2010, 12, 25), +1), datetime(2011, 1, 1)
    assert d3.time_sunday.offset(datetime(2010, 12, 31, 23, 59, 59, 999), 0), datetime(
        2010, 12, 31, 23, 59, 59, 999
    )
    assert d3.time_sunday.offset(datetime(2010, 12, 31, 23, 59, 58, 0), 0), datetime(
        2010, 12, 31, 23, 59, 58, 0
    )


def test_time_sunday_range():
    assert d3.time_sunday.range(datetime(2011, 12, 1), datetime(2012, 1, 15)) == [
        datetime(2011, 12, 4),
        datetime(2011, 12, 11),
        datetime(2011, 12, 18),
        datetime(2011, 12, 25),
        datetime(2012, 1, 1),
        datetime(2012, 1, 8),
    ]

    assert d3.time_sunday.range(
        datetime(2011, 12, 1, 12, 23), datetime(2012, 1, 14, 12, 23)
    ) == [
        datetime(2011, 12, 4),
        datetime(2011, 12, 11),
        datetime(2011, 12, 18),
        datetime(2011, 12, 25),
        datetime(2012, 1, 1),
        datetime(2012, 1, 8),
    ]

    assert d3.time_sunday.range(datetime(2011, 12, 1), datetime(2012, 1, 15)) == [
        datetime(2011, 12, 4),
        datetime(2011, 12, 11),
        datetime(2011, 12, 18),
        datetime(2011, 12, 25),
        datetime(2012, 1, 1),
        datetime(2012, 1, 8),
    ]

    assert d3.time_sunday.range(datetime(2011, 12, 10), datetime(2011, 11, 4)) == []
    assert d3.time_sunday.range(datetime(2011, 11, 1), datetime(2011, 11, 1)) == []

    assert d3.time_sunday.range(datetime(2011, 12, 1), datetime(2012, 1, 15), 2), [
        datetime(2011, 12, 4),
        datetime(2011, 12, 18),
        datetime(2012, 1, 1),
    ]


def test_time_sunday_count():
    #     January 2014
    # Su Mo Tu We Th Fr Sa
    #           1  2  3  4
    #  5  6  7  8  9 10 11
    # 12 13 14 15 16 17 18
    # 19 20 21 22 23 24 25
    # 26 27 28 29 30 31
    assert d3.time_sunday.count(datetime(2014, 1, 1), datetime(2014, 1, 4)) == 0
    assert d3.time_sunday.count(datetime(2014, 1, 1), datetime(2014, 1, 5)) == 1
    assert d3.time_sunday.count(datetime(2014, 1, 1), datetime(2014, 1, 6)) == 1
    assert d3.time_sunday.count(datetime(2014, 1, 1), datetime(2014, 1, 12)) == 2

    #       January 2012
    # Su Mo Tu We Th Fr Sa
    #  1  2  3  4  5  6  7
    #  8  9 10 11 12 13 14
    # 15 16 17 18 19 20 21
    # 22 23 24 25 26 27 28
    # 29 30 31
    assert d3.time_sunday.count(datetime(2012, 1, 1), datetime(2012, 1, 7)) == 1
    assert d3.time_sunday.count(datetime(2012, 1, 1), datetime(2012, 1, 8)) == 2
    assert d3.time_sunday.count(datetime(2012, 1, 1), datetime(2012, 1, 9)) == 2

    assert d3.time_sunday.count(datetime(2011, 1, 1), datetime(2011, 3, 13, 1)) == 11
    assert d3.time_sunday.count(datetime(2011, 1, 1), datetime(2011, 3, 13, 3)) == 11
    assert d3.time_sunday.count(datetime(2011, 1, 1), datetime(2011, 3, 13, 4)) == 11
    assert d3.time_sunday.count(datetime(2011, 1, 1), datetime(2011, 11, 6, 0)) == 45
    assert d3.time_sunday.count(datetime(2011, 1, 1), datetime(2011, 11, 6, 1)) == 45
    assert d3.time_sunday.count(datetime(2011, 1, 1), datetime(2011, 11, 6, 2)) == 45
