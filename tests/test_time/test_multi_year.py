import detroit as d3
from datetime import datetime

def test_time_multi_year_every_floor():
  assert d3.time_year.every(10).floor(datetime(2009, 12, 31, 23, 59, 59)) == datetime(2000,  1,  1)
  assert d3.time_year.every(10).floor(datetime(2010,  1,  1,  0,  0,  0)) == datetime(2010,  1,  1)
  assert d3.time_year.every(10).floor(datetime(2010,  1,  1,  0,  0,  1)) == datetime(2010,  1,  1)


def test_time_multi_year_every_ceil():
  assert d3.time_year.every(100).ceil(datetime(1999, 12, 31, 23, 59, 59)) == datetime(2000,  1,  1)
  assert d3.time_year.every(100).ceil(datetime(2000,  1,  1,  0,  0,  0)) == datetime(2000,  1,  1)
  assert d3.time_year.every(100).ceil(datetime(2000,  1,  1,  0,  0,  1)) == datetime(2100,  1,  1)


def test_time_multi_year_offset():
  assert d3.time_year.every(5).offset(datetime(2010, 12, 31, 23, 59, 59, 999), +1), datetime(2015, 12, 31, 23, 59, 59, 999)
  assert d3.time_year.every(5).offset(datetime(2010, 12, 31, 23, 59, 59, 456), -2), datetime(2000, 12, 31, 23, 59, 59, 456)


def test_time_multi_year_range():
  assert d3.time_year.every(10).range(datetime(2010, 1, 1), datetime(2031, 1, 1)) == [
    datetime(2010, 1, 1),
    datetime(2020, 1, 1),
    datetime(2030, 1, 1)
  ]

