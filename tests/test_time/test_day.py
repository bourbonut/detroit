import detroit as d3
from datetime import datetime

def test_time_day_floor():
  assert d3.time_day.floor(datetime(2010, 12, 31, 23)) == datetime(2010, 12, 31)
  assert d3.time_day.floor(datetime(2011,  1,  1,  0)) == datetime(2011,  1,  1)
  assert d3.time_day.floor(datetime(2011,  1,  1,  1)) == datetime(2011,  1,  1)
  assert d3.time_day.floor(datetime(2011,  3, 13,  7)) == datetime(2011,  3, 13)
  assert d3.time_day.floor(datetime(2011,  3, 13,  8)) == datetime(2011,  3, 13)
  assert d3.time_day.floor(datetime(2011,  3, 13,  9)) == datetime(2011,  3, 13)
  assert d3.time_day.floor(datetime(2011,  3, 13, 10)) == datetime(2011,  3, 13)
  assert d3.time_day.floor(datetime(2011, 11,  6,  7)) == datetime(2011, 11,  6)
  assert d3.time_day.floor(datetime(2011, 11,  6,  8)) == datetime(2011, 11,  6)
  assert d3.time_day.floor(datetime(2011, 11,  6,  9)) == datetime(2011, 11,  6)
  assert d3.time_day.floor(datetime(2011, 11,  6, 10)) == datetime(2011, 11,  6)
  assert d3.time_day.floor(datetime(   9, 11,  6,  7)) == datetime(   9, 11,  6)

def test_time_day_round():
  assert d3.time_day.round(datetime(2010, 12, 30, 13)) == datetime(2010, 12, 31)
  assert d3.time_day.round(datetime(2010, 12, 30, 11)) == datetime(2010, 12, 30)
  assert d3.time_day.round(datetime(2011,  3, 13,  7)) == datetime(2011,  3, 13)
  assert d3.time_day.round(datetime(2011,  3, 13,  8)) == datetime(2011,  3, 13)
  assert d3.time_day.round(datetime(2011,  3, 13,  9)) == datetime(2011,  3, 13)
  assert d3.time_day.round(datetime(2011,  3, 13, 20)) == datetime(2011,  3, 14)
  assert d3.time_day.round(datetime(2011, 11,  6,  7)) == datetime(2011, 11,  6)
  assert d3.time_day.round(datetime(2011, 11,  6,  8)) == datetime(2011, 11,  6)
  assert d3.time_day.round(datetime(2011, 11,  6,  9)) == datetime(2011, 11,  6)
  assert d3.time_day.round(datetime(2011, 11,  6, 20)) == datetime(2011, 11,  7)
  assert d3.time_day.round(datetime(2012,  3,  1,  0)) == datetime(2012,  3,  1)
  assert d3.time_day.round(datetime(2012,  3,  1,  0)) == datetime(2012,  3,  1)


def test_time_day_ceil():
  assert d3.time_day.ceil(datetime(2010, 12, 30, 23)) == datetime(2010, 12, 31)
  assert d3.time_day.ceil(datetime(2010, 12, 31,  0)) == datetime(2010, 12, 31)
  assert d3.time_day.ceil(datetime(2010, 12, 31,  1)) == datetime(2011,  1,  1)
  assert d3.time_day.ceil(datetime(2011,  3, 13,  7)) == datetime(2011,  3, 14)
  assert d3.time_day.ceil(datetime(2011,  3, 13,  8)) == datetime(2011,  3, 14)
  assert d3.time_day.ceil(datetime(2011,  3, 13,  9)) == datetime(2011,  3, 14)
  assert d3.time_day.ceil(datetime(2011,  3, 13, 10)) == datetime(2011,  3, 14)
  assert d3.time_day.ceil(datetime(2011, 11,  6,  7)) == datetime(2011, 11,  7)
  assert d3.time_day.ceil(datetime(2011, 11,  6,  8)) == datetime(2011, 11,  7)
  assert d3.time_day.ceil(datetime(2011, 11,  6,  9)) == datetime(2011, 11,  7)
  assert d3.time_day.ceil(datetime(2011, 11,  6, 10)) == datetime(2011, 11,  7)
  assert d3.time_day.ceil(datetime(2012,  3,  1,  0)) == datetime(2012,  3,  1)
  assert d3.time_day.ceil(datetime(2012,  3,  1,  0)) == datetime(2012,  3,  1)


def test_time_day_offset():
  assert d3.time_day.offset(datetime(2011, 12, 31, 23, 59, 59, 999), 0) == datetime(2011,  12,  31, 23, 59, 59, 999)
  d = datetime(2010, 12, 31, 23, 59, 59, 999)
  assert d3.time_day.offset(d, 1) == datetime(2011, 1, 1, 23, 59, 59, 999)
  assert d3.time_day.offset(datetime(2010, 12, 31, 23, 59, 59, 999), +1), datetime(2011,  1,  1, 23, 59, 59, 999)
  assert d3.time_day.offset(datetime(2010, 12, 31, 23, 59, 59, 456), -2), datetime(2010, 12, 29, 23, 59, 59, 456)
  assert d3.time_day.offset(datetime(2010, 12, 31), -1), datetime(2010, 12, 30)
  assert d3.time_day.offset(datetime(2011,  1,  1), -2), datetime(2010, 12, 30)
  assert d3.time_day.offset(datetime(2011,  1,  1), -1), datetime(2010, 12, 31)
  assert d3.time_day.offset(datetime(2010, 12, 31), +1), datetime(2011,  1,  1)
  assert d3.time_day.offset(datetime(2010, 12, 30), +2), datetime(2011,  1,  1)
  assert d3.time_day.offset(datetime(2010, 12, 30), +1), datetime(2010, 12, 31)
  assert d3.time_day.offset(datetime(2010, 12, 31, 23, 59, 59, 999), 0), datetime(2010, 12, 31, 23, 59, 59, 999)
  assert d3.time_day.offset(datetime(2010, 12, 31, 23, 59, 58,   0), 0), datetime(2010, 12, 31, 23, 59, 58,   0)


def test_time_day_range():
  assert d3.time_day.range(datetime(2011, 11,  4), datetime(2011, 11, 10)) == [
    datetime(2011, 11,  4),
    datetime(2011, 11,  5),
    datetime(2011, 11,  6),
    datetime(2011, 11,  7),
    datetime(2011, 11,  8),
    datetime(2011, 11,  9)
  ]

  assert d3.time_day.range(datetime(2011, 11,  4,  2), datetime(2011, 11, 10, 13)) == [
    datetime(2011, 11,  5),
    datetime(2011, 11,  6),
    datetime(2011, 11,  7),
    datetime(2011, 11,  8),
    datetime(2011, 11,  9),
    datetime(2011, 11, 10)
  ]

  assert d3.time_day.range(datetime(2011, 11,  4), datetime(2011, 11,  7)) == [
    datetime(2011, 11,  4),
    datetime(2011, 11,  5),
    datetime(2011, 11,  6)
  ]


  assert d3.time_day.range(datetime(2011, 11, 10), datetime(2011, 11,  4)) == []
  assert d3.time_day.range(datetime(2011, 11, 10), datetime(2011, 11, 10)) == []


  assert d3.time_day.range(datetime(2011, 11,  4,  2), datetime(2011, 11, 14, 13), 3) == [
    datetime(2011, 11,  5),
    datetime(2011, 11,  8),
    datetime(2011, 11, 11),
    datetime(2011, 11, 14)
  ]

  assert d3.time_day.range(datetime(2011,  1,  1,  0), datetime(2011,  5,  9,  0), 0) == []
  assert d3.time_day.range(datetime(2011,  1,  1,  0), datetime(2011,  5,  9,  0), -1) == []


def test_time_day_count():
  assert d3.time_day.count(datetime(2011,  1,  1,  0), datetime(2011,  5,  9,  0)) == 128
  assert d3.time_day.count(datetime(2011,  1,  1,  1), datetime(2011,  5,  9,  0)) == 127
  assert d3.time_day.count(datetime(2010, 12, 31, 23), datetime(2011,  5,  9,  0)) == 128
  assert d3.time_day.count(datetime(2011,  1,  1,  0), datetime(2011,  5,  8, 23)) == 127
  assert d3.time_day.count(datetime(2011,  1,  1,  0), datetime(2011,  5,  9,  1)) == 128
  assert d3.time_day.count(datetime(2011,  1,  1), datetime(2011,  3, 13,  1)) == 71
  assert d3.time_day.count(datetime(2011,  1,  1), datetime(2011,  3, 13,  3)) == 71
  assert d3.time_day.count(datetime(2011,  1,  1), datetime(2011,  3, 13,  4)) == 71
  assert d3.time_day.count(datetime(2011,  1,  1), datetime(2011, 11,  6,  0)) == 309
  assert d3.time_day.count(datetime(2011,  1,  1), datetime(2011, 11,  6,  1)) == 309
  assert d3.time_day.count(datetime(2011,  1,  1), datetime(2011, 11,  6,  2)) == 309


  # date = datetime(2011, 5, 9);
  # assert d3.time_day.count(d3.time_year(date), date) == 128

  assert d3.time_day.count(datetime(1999,  1,  1), datetime(1999, 12, 31)) == 364
  assert d3.time_day.count(datetime(2000,  1,  1), datetime(2000, 12, 31)) == 365 # leap year
  assert d3.time_day.count(datetime(2001,  1,  1), datetime(2001, 12, 31)) == 364
  assert d3.time_day.count(datetime(2002,  1,  1), datetime(2002, 12, 31)) == 364
  assert d3.time_day.count(datetime(2003,  1,  1), datetime(2003, 12, 31)) == 364
  assert d3.time_day.count(datetime(2004,  1,  1), datetime(2004, 12, 31)) == 365 # leap year
  assert d3.time_day.count(datetime(2005,  1,  1), datetime(2005, 12, 31)) == 364
  assert d3.time_day.count(datetime(2006,  1,  1), datetime(2006, 12, 31)) == 364
  assert d3.time_day.count(datetime(2007,  1,  1), datetime(2007, 12, 31)) == 364
  assert d3.time_day.count(datetime(2008,  1,  1), datetime(2008, 12, 31)) == 365 # leap year
  assert d3.time_day.count(datetime(2009,  1,  1), datetime(2009, 12, 31)) == 364
  assert d3.time_day.count(datetime(2010,  1,  1), datetime(2010, 12, 31)) == 364
  assert d3.time_day.count(datetime(2011,  1,  1), datetime(2011, 12, 31)) == 364


def test_time_day_every():
    assert d3.time_day.every(3).range(datetime(2008, 12, 30, 0, 12), datetime(2009, 1, 5, 23, 48)) == [datetime(2009, 1, 3)]
    assert d3.time_day.every(5).range(datetime(2008, 12, 30, 0, 12), datetime(2009, 1, 6, 23, 48)) == [datetime(2009, 1, 5)]
    assert d3.time_day.every(7).range(datetime(2008, 12, 30, 0, 12), datetime(2009, 1, 8, 23, 48)) == []
