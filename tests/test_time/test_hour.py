import detroit as d3
from datetime import datetime


def test_time_hour_floor():
    assert d3.time_hour.floor(datetime(2010, 12, 31, 23, 59)) == datetime(
        2010, 12, 31, 23
    )
    assert d3.time_hour.floor(datetime(2011, 1, 1, 0, 0)) == datetime(2011, 1, 1, 0)
    assert d3.time_hour.floor(datetime(2011, 1, 1, 0, 1)) == datetime(2011, 1, 1, 0)
    assert d3.time_hour.floor(datetime(2011, 3, 13, 8, 59)) == datetime(2011, 3, 13, 8)
    assert d3.time_hour.floor(datetime(2011, 3, 13, 9, 0)) == datetime(2011, 3, 13, 9)
    assert d3.time_hour.floor(datetime(2011, 3, 13, 9, 1)) == datetime(2011, 3, 13, 9)
    assert d3.time_hour.floor(datetime(2011, 3, 13, 9, 59)) == datetime(2011, 3, 13, 9)
    assert d3.time_hour.floor(datetime(2011, 3, 13, 10, 0)) == datetime(2011, 3, 13, 10)
    assert d3.time_hour.floor(datetime(2011, 3, 13, 10, 1)) == datetime(2011, 3, 13, 10)
    assert d3.time_hour.floor(datetime(2011, 11, 6, 7, 59)) == datetime(2011, 11, 6, 7)
    assert d3.time_hour.floor(datetime(2011, 11, 6, 8, 0)) == datetime(2011, 11, 6, 8)
    assert d3.time_hour.floor(datetime(2011, 11, 6, 8, 1)) == datetime(2011, 11, 6, 8)
    assert d3.time_hour.floor(datetime(2011, 11, 6, 8, 59)) == datetime(2011, 11, 6, 8)
    assert d3.time_hour.floor(datetime(2011, 11, 6, 9, 0)) == datetime(2011, 11, 6, 9)
    assert d3.time_hour.floor(datetime(2011, 11, 6, 9, 1)) == datetime(2011, 11, 6, 9)


def test_time_hour_ceil():
    assert d3.time_hour.ceil(datetime(2010, 12, 31, 23, 59)) == datetime(2011, 1, 1, 0)
    assert d3.time_hour.ceil(datetime(2011, 1, 1, 0, 0)) == datetime(2011, 1, 1, 0)
    assert d3.time_hour.ceil(datetime(2011, 1, 1, 0, 1)) == datetime(2011, 1, 1, 1)
    assert d3.time_hour.ceil(datetime(2011, 3, 13, 8, 59)) == datetime(2011, 3, 13, 9)
    assert d3.time_hour.ceil(datetime(2011, 3, 13, 9, 0)) == datetime(2011, 3, 13, 9)
    assert d3.time_hour.ceil(datetime(2011, 3, 13, 9, 1)) == datetime(2011, 3, 13, 10)
    assert d3.time_hour.ceil(datetime(2011, 3, 13, 9, 59)) == datetime(2011, 3, 13, 10)
    assert d3.time_hour.ceil(datetime(2011, 3, 13, 10, 0)) == datetime(2011, 3, 13, 10)
    assert d3.time_hour.ceil(datetime(2011, 3, 13, 10, 1)) == datetime(2011, 3, 13, 11)
    assert d3.time_hour.ceil(datetime(2011, 11, 6, 7, 59)) == datetime(2011, 11, 6, 8)
    assert d3.time_hour.ceil(datetime(2011, 11, 6, 8, 0)) == datetime(2011, 11, 6, 8)
    assert d3.time_hour.ceil(datetime(2011, 11, 6, 8, 1)) == datetime(2011, 11, 6, 9)
    assert d3.time_hour.ceil(datetime(2011, 11, 6, 8, 59)) == datetime(2011, 11, 6, 9)
    assert d3.time_hour.ceil(datetime(2011, 11, 6, 9, 0)) == datetime(2011, 11, 6, 9)
    assert d3.time_hour.ceil(datetime(2011, 11, 6, 9, 1)) == datetime(2011, 11, 6, 10)


def test_time_hour_offset():
    d = datetime(2010, 12, 31, 23, 59, 59, 999)
    assert d3.time_hour.offset(d, 1) == datetime(2011, 1, 1, 0, 59, 59, 999)
    assert d3.time_hour.offset(datetime(2010, 12, 31, 23, 59, 59, 999), +1) == datetime(
        2011, 1, 1, 0, 59, 59, 999
    )
    assert d3.time_hour.offset(datetime(2010, 12, 31, 23, 59, 59, 456), -2) == datetime(
        2010, 12, 31, 21, 59, 59, 456
    )
    assert d3.time_hour.offset(datetime(2010, 12, 31, 12), -1) == datetime(
        2010, 12, 31, 11
    )
    assert d3.time_hour.offset(datetime(2011, 1, 1, 1), -2) == datetime(
        2010, 12, 31, 23
    )
    assert d3.time_hour.offset(datetime(2011, 1, 1, 0), -1) == datetime(
        2010, 12, 31, 23
    )
    assert d3.time_hour.offset(datetime(2010, 12, 31, 11), +1) == datetime(
        2010, 12, 31, 12
    )
    assert d3.time_hour.offset(datetime(2010, 12, 31, 23), +2) == datetime(
        2011, 1, 1, 1
    )
    assert d3.time_hour.offset(datetime(2010, 12, 31, 23), +1) == datetime(
        2011, 1, 1, 0
    )
    assert d3.time_hour.offset(datetime(2010, 12, 31, 23, 59, 59, 999), 0) == datetime(
        2010, 12, 31, 23, 59, 59, 999
    )
    assert d3.time_hour.offset(datetime(2010, 12, 31, 23, 59, 58, 0), 0) == datetime(
        2010, 12, 31, 23, 59, 58, 0
    )


def test_time_hour_range():
    assert d3.time_hour.range(
        datetime(2010, 12, 31, 12, 30), datetime(2010, 12, 31, 15, 30)
    ) == [
        datetime(2010, 12, 31, 13),
        datetime(2010, 12, 31, 14),
        datetime(2010, 12, 31, 15),
    ]

    assert d3.time_hour.range(datetime(2010, 12, 31, 23), datetime(2011, 1, 1, 2))[
        0
    ] == datetime(2010, 12, 31, 23)
    assert d3.time_hour.range(datetime(2010, 12, 31, 23), datetime(2011, 1, 1, 2))[
        2
    ] == datetime(2011, 1, 1, 1)
    assert d3.time_hour.range(datetime(2011, 2, 1, 1), datetime(2011, 2, 1, 13), 3) == [
        datetime(2011, 2, 1, 1),
        datetime(2011, 2, 1, 4),
        datetime(2011, 2, 1, 7),
        datetime(2011, 2, 1, 10),
    ]

    # assert d3.time_hour.range(datetime(2011, 3, 13, 1), datetime(2011, 3, 13, 5)) == [
    #   datetime(2011, 3, 13, 9),
    #   datetime(2011, 3, 13, 10),
    #   datetime(2011, 3, 13, 11)
    # ]
    # assert d3.time_hour.range(datetime(2011, 11, 6, 0), datetime(2011, 11, 6, 2)) == [
    #   datetime(2011, 11, 6, 7),
    #   datetime(2011, 11, 6, 8),
    #   datetime(2011, 11, 6, 9)
    # ]

    assert d3.time_hour.range(
        datetime.fromtimestamp(1478415600), datetime.fromtimestamp(1478430000)
    ) == [
        datetime.fromtimestamp(1478415600),  # Sun Nov  6 2016  0:00:00 GMT-0700 (PDT)
        datetime.fromtimestamp(1478419200),  # Sun Nov  6 2016  1:00:00 GMT-0700 (PDT)
        datetime.fromtimestamp(1478422800),  # Sun Nov  6 2016  1:00:00 GMT-0800 (PDT)
        datetime.fromtimestamp(1478426400),  # Sun Nov  6 2016  2:00:00 GMT-0800 (PDT)
    ]


def test_time_hour_every():
    expected_values = [
        datetime(2008, 12, 30, 16),
        datetime(2008, 12, 30, 20),
        datetime(2008, 12, 31, 0),
        datetime(2008, 12, 31, 4),
        datetime(2008, 12, 31, 8),
        datetime(2008, 12, 31, 12),
    ]
    assert (
        d3.time_hour.every(4).range(
            datetime(2008, 12, 30, 12, 47), datetime(2008, 12, 31, 13, 57)
        )
        == expected_values
    )
    expected_values = [datetime(2008, 12, 31, 0), datetime(2008, 12, 31, 12)]
    assert (
        d3.time_hour.every(12).range(
            datetime(2008, 12, 30, 12, 47), datetime(2008, 12, 31, 13, 57)
        )
        == expected_values
    )
