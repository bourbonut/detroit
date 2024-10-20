import detroit as d3
from datetime import datetime

def test_time_year_floor():
  assert d3.time_year.floor(datetime(2010, 12, 31, 23, 59, 59)) == datetime(2010,  1,  1)
  assert d3.time_year.floor(datetime(2011,  1,  1,  0,  0,  0)) == datetime(2011,  1,  1)
  assert d3.time_year.floor(datetime(2011,  1,  1,  0,  0,  1)) == datetime(2011,  1,  1)
  assert d3.time_year.floor(datetime(9, 11,  6,  7)) == datetime(9,  1,  1)


def test_time_year_ceil():
  assert d3.time_year.ceil(datetime(2010, 12, 31, 23, 59, 59)) == datetime(2011,  1,  1)
  assert d3.time_year.ceil(datetime(2011,  1,  1,  0,  0,  0)) == datetime(2011,  1,  1)
  assert d3.time_year.ceil(datetime(2011,  1,  1,  0,  0,  1)) == datetime(2012,  1,  1)


def test_time_year_offset():
  assert d3.time_year.offset(datetime(2010, 12, 31, 23, 59, 59, 999), +1), datetime(2011, 12, 31, 23, 59, 59, 999)
  assert d3.time_year.offset(datetime(2010, 12, 31, 23, 59, 59, 456), -2), datetime(2008, 12, 31, 23, 59, 59, 456)
  assert d3.time_year.offset(datetime(2010, 12,  1), -1), datetime(2009, 12,  1)
  assert d3.time_year.offset(datetime(2011,  1,  1), -2), datetime(2009,  1,  1)
  assert d3.time_year.offset(datetime(2011,  1,  1), -1), datetime(2010,  1,  1)
  assert d3.time_year.offset(datetime(2009, 12,  1), +1), datetime(2010, 12,  1)
  assert d3.time_year.offset(datetime(2009,  1,  1), +2), datetime(2011,  1,  1)
  assert d3.time_year.offset(datetime(2010,  1,  1), +1), datetime(2011,  1,  1)
  assert d3.time_year.offset(datetime(2010, 12, 31, 23, 59, 59, 999), 0), datetime(2010, 12, 31, 23, 59, 59, 999)
  assert d3.time_year.offset(datetime(2010, 12, 31, 23, 59, 58,   0), 0), datetime(2010, 12, 31, 23, 59, 58,   0)


# def test_time_year_every():
#   assert d3.time_year.every(5).range(datetime(2008, 1, 1), datetime(2023, 1, 1)) == [datetime(2010, 1, 1), datetime(2016, 1, 1), datetime(2020, 1, 1)]

def test_time_year_range():
  assert d3.time_year.range(datetime(2010, 1, 1), datetime(2013, 1, 1)) == [
    datetime(2010, 1, 1),
    datetime(2011, 1, 1),
    datetime(2012, 1, 1)
  ]
  assert d3.time_year.range(datetime(2010, 1, 1), datetime(2013, 1, 1))[0], datetime(2010, 1, 1)
  assert d3.time_year.range(datetime(2010, 1, 1), datetime(2013, 1, 1))[2], datetime(2012, 1, 1)

  assert d3.time_year.range(datetime(2009, 1, 1), datetime(2029, 1, 1), 5), [
    datetime(2009, 1, 1),
    datetime(2014, 1, 1),
    datetime(2019, 1, 1),
    datetime(2024, 1, 1),
  ]

