from datetime import datetime

import detroit as d3


def test_time_thursday_floor():
    assert d3.time_thursday.floor(datetime(2011, 1, 4, 23, 59, 59)) == datetime(
        2010, 12, 30
    )
    assert d3.time_thursday.floor(datetime(2011, 1, 5, 0, 0, 0)) == datetime(
        2010, 12, 30
    )
    assert d3.time_thursday.floor(datetime(2011, 1, 5, 0, 0, 1)) == datetime(
        2010, 12, 30
    )
    assert d3.time_thursday.floor(datetime(2011, 1, 5, 23, 59, 59)) == datetime(
        2010, 12, 30
    )
    assert d3.time_thursday.floor(datetime(2011, 1, 6, 0, 0, 0)) == datetime(2011, 1, 6)
    assert d3.time_thursday.floor(datetime(2011, 1, 6, 0, 0, 1)) == datetime(2011, 1, 6)


def test_time_thursday_count():
    #       January 2012
    # Su Mo Tu We Th Fr Sa
    #  1  2  3  4  5  6  7
    #  8  9 10 11 12 13 14
    # 15 16 17 18 19 20 21
    # 22 23 24 25 26 27 28
    # 29 30 31
    assert d3.time_thursday.count(datetime(2012, 1, 1), datetime(2012, 1, 4)) == 0
    assert d3.time_thursday.count(datetime(2012, 1, 1), datetime(2012, 1, 5)) == 1
    assert d3.time_thursday.count(datetime(2012, 1, 1), datetime(2012, 1, 6)) == 1
    assert d3.time_thursday.count(datetime(2012, 1, 1), datetime(2012, 1, 12)) == 2

    #     January 2015
    # Su Mo Tu We Th Fr Sa
    #              1  2  3
    #  4  5  6  7  8  9 10
    # 11 12 13 14 15 16 17
    # 18 19 20 21 22 23 24
    # 25 26 27 28 29 30 31
    assert d3.time_thursday.count(datetime(2015, 1, 1), datetime(2015, 1, 7)) == 1
    assert d3.time_thursday.count(datetime(2015, 1, 1), datetime(2015, 1, 8)) == 2
    assert d3.time_thursday.count(datetime(2015, 1, 1), datetime(2015, 1, 9)) == 2

    assert d3.time_thursday.count(datetime(2011, 1, 1), datetime(2011, 3, 13, 1)) == 10
    assert d3.time_thursday.count(datetime(2011, 1, 1), datetime(2011, 3, 13, 3)) == 10
    assert d3.time_thursday.count(datetime(2011, 1, 1), datetime(2011, 3, 13, 4)) == 10
    assert d3.time_thursday.count(datetime(2011, 1, 1), datetime(2011, 11, 6, 0)) == 44
    assert d3.time_thursday.count(datetime(2011, 1, 1), datetime(2011, 11, 6, 1)) == 44
    assert d3.time_thursday.count(datetime(2011, 1, 1), datetime(2011, 11, 6, 2)) == 44
