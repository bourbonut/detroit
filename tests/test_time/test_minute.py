from datetime import datetime

import detroit as d3


def test_time_minute_floor():
    assert d3.time_minute.floor(datetime(2010, 12, 31, 23, 59, 59)) == datetime(
        2010, 12, 31, 23, 59
    )
    assert d3.time_minute.floor(datetime(2011, 1, 1, 0, 0, 0)) == datetime(
        2011, 1, 1, 0, 0
    )
    assert d3.time_minute.floor(datetime(2011, 1, 1, 0, 0, 59)) == datetime(
        2011, 1, 1, 0, 0
    )
    assert d3.time_minute.floor(datetime(2011, 1, 1, 0, 1, 0)) == datetime(
        2011, 1, 1, 0, 1
    )


def test_time_minute_ceil():
    assert d3.time_minute.ceil(datetime(2010, 12, 31, 23, 59, 59)) == datetime(
        2011, 1, 1, 0, 0
    )
    assert d3.time_minute.ceil(datetime(2011, 1, 1, 0, 0, 0)) == datetime(
        2011, 1, 1, 0, 0
    )
    assert d3.time_minute.ceil(datetime(2011, 1, 1, 0, 0, 59)) == datetime(
        2011, 1, 1, 0, 1
    )
    assert d3.time_minute.ceil(datetime(2011, 1, 1, 0, 1, 0)) == datetime(
        2011, 1, 1, 0, 1
    )


def test_time_minute_offset():
    assert d3.time_minute.offset(datetime(2010, 12, 31, 23, 59, 59, 999), +1), datetime(
        2011, 1, 1, 0, 0, 59, 999
    )
    assert d3.time_minute.offset(datetime(2010, 12, 31, 23, 59, 59, 456), -2), datetime(
        2010, 12, 31, 23, 57, 59, 456
    )
    assert d3.time_minute.offset(datetime(2010, 12, 31, 23, 12), -1), datetime(
        2010, 12, 31, 23, 11
    )
    assert d3.time_minute.offset(datetime(2011, 1, 1, 0, 1), -2), datetime(
        2010, 12, 31, 23, 59
    )
    assert d3.time_minute.offset(datetime(2011, 1, 1, 0, 0), -1), datetime(
        2010, 12, 31, 23, 59
    )
    assert d3.time_minute.offset(datetime(2010, 12, 31, 23, 11), +1), datetime(
        2010, 12, 31, 23, 12
    )
    assert d3.time_minute.offset(datetime(2010, 12, 31, 23, 59), +2), datetime(
        2011, 1, 1, 0, 1
    )
    assert d3.time_minute.offset(datetime(2010, 12, 31, 23, 59), +1), datetime(
        2011, 1, 1, 0, 0
    )
    assert d3.time_minute.offset(datetime(2010, 12, 31, 23, 59, 59, 999), 0), datetime(
        2010, 12, 31, 23, 59, 59, 999
    )
    assert d3.time_minute.offset(datetime(2010, 12, 31, 23, 59, 58, 0), 0), datetime(
        2010, 12, 31, 23, 59, 58, 0
    )


def test_time_minute_range():
    assert d3.time_minute.range(
        datetime(2010, 12, 31, 23, 59), datetime(2011, 1, 1, 0, 2)
    ) == [
        datetime(2010, 12, 31, 23, 59),
        datetime(2011, 1, 1, 0, 0),
        datetime(2011, 1, 1, 0, 1),
    ]
    assert d3.time_minute.range(
        datetime(2010, 12, 31, 23, 59), datetime(2011, 1, 1, 0, 2)
    )[0] == datetime(2010, 12, 31, 23, 59)

    assert d3.time_minute.range(
        datetime(2010, 12, 31, 23, 59), datetime(2011, 1, 1, 0, 2)
    )[2] == datetime(2011, 1, 1, 0, 1)


def test_unknown():
    assert d3.time_minute.range(
        datetime(2011, 2, 1, 12, 7), datetime(2011, 2, 1, 13, 7), 15
    ) == [
        datetime(2011, 2, 1, 12, 7),
        datetime(2011, 2, 1, 12, 22),
        datetime(2011, 2, 1, 12, 37),
        datetime(2011, 2, 1, 12, 52),
    ]

    assert d3.time_minute.range(
        datetime(2011, 3, 13, 9, 59), datetime(2011, 3, 13, 10, 2)
    ) == [
        datetime(2011, 3, 13, 9, 59),
        datetime(2011, 3, 13, 10, 0),
        datetime(2011, 3, 13, 10, 1),
    ]

    assert d3.time_minute.range(
        datetime(2011, 11, 6, 8, 59), datetime(2011, 11, 6, 9, 2)
    ) == [
        datetime(2011, 11, 6, 8, 59),
        datetime(2011, 11, 6, 9, 0),
        datetime(2011, 11, 6, 9, 1),
    ]

    assert d3.time_minute.range(
        datetime.fromtimestamp(1478422680), datetime.fromtimestamp(1478422920)
    ) == [
        datetime.fromtimestamp(1478422680),  # Sun Nov  6 2016  1:58:00 GMT-0700 (PDT)
        datetime.fromtimestamp(1478422740),  # Sun Nov  6 2016  1:59:00 GMT-0700 (PDT)
        datetime.fromtimestamp(1478422800),  # Sun Nov  6 2016  1:00:00 GMT-0800 (PDT)
        datetime.fromtimestamp(1478422860),  # Sun Nov  6 2016  1:01:00 GMT-0800 (PDT)
    ]


def test_time_minute_every():
    assert d3.time_minute.every(15).range(
        datetime(2008, 12, 30, 12, 47), datetime(2008, 12, 30, 13, 57)
    ) == [
        datetime(2008, 12, 30, 13, 0),
        datetime(2008, 12, 30, 13, 15),
        datetime(2008, 12, 30, 13, 30),
        datetime(2008, 12, 30, 13, 45),
    ]
    assert d3.time_minute.every(30).range(
        datetime(2008, 12, 30, 12, 47), datetime(2008, 12, 30, 13, 57)
    ) == [
        datetime(2008, 12, 30, 13, 0),
        datetime(2008, 12, 30, 13, 30),
    ]
