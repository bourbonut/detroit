from datetime import datetime

import detroit as d3


def test_time_parse_string():
    p = d3.time_parse("%m/%d/%Y, %H:%M:%S")
    assert p("1/1/1990, 12:00:00") == datetime(1990, 1, 1, 12, 0)
    assert p("1/2/1990, 12:00:00") == datetime(1990, 1, 2, 12, 0)
    assert p("1/3/1990, 12:00:00") == datetime(1990, 1, 3, 12, 0)
    assert p("1/4/1990, 12:00:00") == datetime(1990, 1, 4, 12, 0)
    assert p("1/5/1990, 12:00:00") == datetime(1990, 1, 5, 12, 0)
    assert p("1/6/1990, 12:00:00") == datetime(1990, 1, 6, 12, 0)
    assert p("1/7/1990, 12:00:00") == datetime(1990, 1, 7, 12, 0)


def test_time_parse_string_1():
    p = d3.time_parse("%a %m/%d/%Y")
    assert p("Sun 01/01/1990") == datetime(1990, 1, 1)
    assert p("Wed 02/03/1991") == datetime(1991, 2, 3)


def test_time_parse_string_2():
    p = d3.time_parse("%A %m/%d/%Y")
    assert p("Sunday 01/01/1990") == datetime(1990, 1, 1)
    assert p("Wednesday 02/03/1991") == datetime(1991, 2, 3)
    assert p("Caturday 03/10/2010") is None


def test_time_parse_string_2():
    p = d3.time_parse("%U %Y")
    assert p("00 1990") == datetime(1990, 1, 1)
    assert p("05 1991") == datetime(1991, 1, 1)
    assert p("01 1995") == datetime(1995, 1, 1)


def test_time_parse_string_3():
    p = d3.time_parse("%a %U %Y")
    assert p("Mon 00 1990") == datetime(1990, 1, 1)
    assert p("Sun 05 1991") == datetime(1991, 2, 3)
    assert p("Sun 01 1995") == datetime(1995, 1, 1)


def test_time_parse_string_4():
    p = d3.time_parse("%A %U %Y")
    assert p("Monday 00 1990") == datetime(1990, 1, 1)
    assert p("Sunday 05 1991") == datetime(1991, 2, 3)
    assert p("Sunday 01 1995") == datetime(1995, 1, 1)


def test_time_parse_string_5():
    p = d3.time_parse("%w %U %Y")
    assert p("1 00 1990") == datetime(1990, 1, 1)
    assert p("0 05 1991") == datetime(1991, 2, 3)
    assert p("0 01 1995") == datetime(1995, 1, 1)
