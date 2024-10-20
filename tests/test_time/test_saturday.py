import detroit as d3
from datetime import datetime

def test_time_saturday_floor():
  assert d3.time_saturday.floor(datetime(2011,  1,  6, 23, 59, 59)) == datetime(2011,  1,  1)
  assert d3.time_saturday.floor(datetime(2011,  1,  7,  0,  0,  0)) == datetime(2011,  1,  1)
  assert d3.time_saturday.floor(datetime(2011,  1,  7,  0,  0,  1)) == datetime(2011,  1,  1)
  assert d3.time_saturday.floor(datetime(2011,  1,  7, 23, 59, 59)) == datetime(2011,  1,  1)
  assert d3.time_saturday.floor(datetime(2011,  1,  8,  0,  0,  0)) == datetime(2011,  1,  8)
  assert d3.time_saturday.floor(datetime(2011,  1,  8,  0,  0,  1)) == datetime(2011,  1,  8)


def test_time_saturday_count():
  #       January 2012
  # Su Mo Tu We Th Fr Sa
  #  1  2  3  4  5  6  7
  #  8  9 10 11 12 13 14
  # 15 16 17 18 19 20 21
  # 22 23 24 25 26 27 28
  # 29 30 31
  assert d3.time_saturday.count(datetime(2012,  1,  1), datetime(2012,  1,  6)) == 0
  assert d3.time_saturday.count(datetime(2012,  1,  1), datetime(2012,  1,  7)) == 1
  assert d3.time_saturday.count(datetime(2012,  1,  1), datetime(2012,  1,  8)) == 1
  assert d3.time_saturday.count(datetime(2012,  1,  1), datetime(2012,  1, 14)) == 2

  #     January 2011
  # Su Mo Tu We Th Fr Sa
  #                    1
  #  2  3  4  5  6  7  8
  #  9 10 11 12 13 14 15
  # 16 17 18 19 20 21 22
  # 23 24 25 26 27 28 29
  # 30 31
  assert d3.time_saturday.count(datetime(2011,  1,  1), datetime(2011,  1,  7)) == 1
  assert d3.time_saturday.count(datetime(2011,  1,  1), datetime(2011,  1,  8)) == 2
  assert d3.time_saturday.count(datetime(2011,  1,  1), datetime(2011,  1,  9)) == 2


  assert d3.time_saturday.count(datetime(2011,  1,  1), datetime(2011,  3, 13,  1)) == 11
  assert d3.time_saturday.count(datetime(2011,  1,  1), datetime(2011,  3, 13,  3)) == 11
  assert d3.time_saturday.count(datetime(2011,  1,  1), datetime(2011,  3, 13,  4)) == 11
  assert d3.time_saturday.count(datetime(2011,  1,  1), datetime(2011, 11,  6,  0)) == 45
  assert d3.time_saturday.count(datetime(2011,  1,  1), datetime(2011, 11,  6,  1)) == 45
  assert d3.time_saturday.count(datetime(2011,  1,  1), datetime(2011, 11,  6,  2)) == 45

