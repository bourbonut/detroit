import detroit as d3
from datetime import datetime

def test_time_friday_floor():
  assert d3.time_friday.floor(datetime(2011,  1,  5, 23, 59, 59)) == datetime(2010, 12, 31)
  assert d3.time_friday.floor(datetime(2011,  1,  6,  0,  0,  0)) == datetime(2010, 12, 31)
  assert d3.time_friday.floor(datetime(2011,  1,  6,  0,  0,  1)) == datetime(2010, 12, 31)
  assert d3.time_friday.floor(datetime(2011,  1,  6, 23, 59, 59)) == datetime(2010, 12, 31)
  assert d3.time_friday.floor(datetime(2011,  1,  7,  0,  0,  0)) == datetime(2011,  1,  7)
  assert d3.time_friday.floor(datetime(2011,  1,  7,  0,  0,  1)) == datetime(2011,  1,  7)


def test_time_friday_count():
  #     January 2012
  # Su Mo Tu We Th Fr Sa
  #  1  2  3  4  5  6  7
  #  8  9 10 11 12 13 14
  # 15 16 17 18 19 20 21
  # 22 23 24 25 26 27 28
  # 29 30 31
  # assert d3.time_friday.count(datetime(2012,  1,  1), datetime(2012,  1,  5)) == 0
  # assert d3.time_friday.count(datetime(2012,  1,  1), datetime(2012,  1,  6)) == 1
  # assert d3.time_friday.count(datetime(2012,  1,  1), datetime(2012,  1,  7)) == 1
  # assert d3.time_friday.count(datetime(2012,  1,  1), datetime(2012,  1, 13)) == 2

  #     January 2010
  # Su Mo Tu We Th Fr Sa
  #                 1  2
  #  3  4  5  6  7  8  9
  # 10 11 12 13 14 15 16
  # 17 18 19 20 21 22 23
  # 24 25 26 27 28 29 30
  # 31
  assert d3.time_friday.count(datetime(2010,  1,  1), datetime(2010,  1,  7)) == 1
  assert d3.time_friday.count(datetime(2010,  1,  1), datetime(2010,  1,  8)) == 2
  assert d3.time_friday.count(datetime(2010,  1,  1), datetime(2010,  1,  9)) == 2

  assert d3.time_friday.count(datetime(2011,  1,  1), datetime(2011,  3, 13,  1)) == 10
  assert d3.time_friday.count(datetime(2011,  1,  1), datetime(2011,  3, 13,  3)) == 10
  assert d3.time_friday.count(datetime(2011,  1,  1), datetime(2011,  3, 13,  4)) == 10
  assert d3.time_friday.count(datetime(2011,  1,  1), datetime(2011, 11,  6,  0)) == 44
  assert d3.time_friday.count(datetime(2011,  1,  1), datetime(2011, 11,  6,  1)) == 44
  assert d3.time_friday.count(datetime(2011,  1,  1), datetime(2011, 11,  6,  2)) == 44

