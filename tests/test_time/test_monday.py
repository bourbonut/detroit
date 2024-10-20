import detroit as d3
from datetime import datetime

def test_time_monday_floor():
  assert d3.time_monday.floor(datetime(2011,  1,  1, 23, 59, 59)) == datetime(2010, 12, 27)
  assert d3.time_monday.floor(datetime(2011,  1,  2,  0,  0,  0)) == datetime(2010, 12, 27)
  assert d3.time_monday.floor(datetime(2011,  1,  2,  0,  0,  1)) == datetime(2010, 12, 27)
  assert d3.time_monday.floor(datetime(2011,  1,  2, 23, 59, 59)) == datetime(2010, 12, 27)
  assert d3.time_monday.floor(datetime(2011,  1,  3,  0,  0,  0)) == datetime(2011,  1,  3)
  assert d3.time_monday.floor(datetime(2011,  1,  3,  0,  0,  1)) == datetime(2011,  1,  3)


def test_time_monday_range():
  assert d3.time_monday.range(datetime(2011, 12,  1), datetime(2012,  1, 15), 2), [
    datetime(2011, 12,  5),
    datetime(2011, 12, 19),
    datetime(2012,  1,  2)
  ]


def test_time_monday_count():
  #     January 2014
  # Su Mo Tu We Th Fr Sa
  #           1  2  3  4
  #  5  6  7  8  9 10 11
  # 12 13 14 15 16 17 18
  # 19 20 21 22 23 24 25
  # 26 27 28 29 30 31
  assert d3.time_monday.count(datetime(2014,  1,  1), datetime(2014,  1,  5)) == 0
  assert d3.time_monday.count(datetime(2014,  1,  1), datetime(2014,  1,  6)) == 1
  assert d3.time_monday.count(datetime(2014,  1,  1), datetime(2014,  1,  7)) == 1
  assert d3.time_monday.count(datetime(2014,  1,  1), datetime(2014,  1, 13)) == 2

  #     January 2018
  # Su Mo Tu We Th Fr Sa
  #     1  2  3  4  5  6
  #  7  8  9 10 11 12 13
  # 14 15 16 17 18 19 20
  # 21 22 23 24 25 26 27
  # 28 29 30 31
  assert d3.time_monday.count(datetime(2018,  1,  1), datetime(2018,  1,  7)) == 1
  assert d3.time_monday.count(datetime(2018,  1,  1), datetime(2018,  1,  8)) == 2
  assert d3.time_monday.count(datetime(2018,  1,  1), datetime(2018,  1,  9)) == 2

  assert d3.time_monday.count(datetime(2011,  1,  1), datetime(2011,  3, 13,  1)) == 10
  assert d3.time_monday.count(datetime(2011,  1,  1), datetime(2011,  3, 13,  3)) == 10
  assert d3.time_monday.count(datetime(2011,  1,  1), datetime(2011,  3, 13,  4)) == 10
  assert d3.time_monday.count(datetime(2011,  1,  1), datetime(2011, 11,  6,  0)) == 44
  assert d3.time_monday.count(datetime(2011,  1,  1), datetime(2011, 11,  6,  1)) == 44
  assert d3.time_monday.count(datetime(2011,  1,  1), datetime(2011, 11,  6,  2)) == 44

