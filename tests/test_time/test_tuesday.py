import detroit as d3
from datetime import datetime

def test_unknown():
  assert.strictEqual(time_tuesdays, time_tuesday.range);


def test_time_tuesday_floor():
  assert time_tuesday.floor(datetime(2011,  0,  2, 23, 59, 59)) == datetime(2010, 11, 28)
  assert time_tuesday.floor(datetime(2011,  0,  3,  0,  0,  0)) == datetime(2010, 11, 28)
  assert time_tuesday.floor(datetime(2011,  0,  3,  0,  0,  1)) == datetime(2010, 11, 28)
  assert time_tuesday.floor(datetime(2011,  0,  3, 23, 59, 59)) == datetime(2010, 11, 28)
  assert time_tuesday.floor(datetime(2011,  0,  4,  0,  0,  0)) == datetime(2011,  0,  4)
  assert time_tuesday.floor(datetime(2011,  0,  4,  0,  0,  1)) == datetime(2011,  0,  4)


def test_unknown():
  #     January 2014
  # Su Mo Tu We Th Fr Sa
  #           1  2  3  4
  #  5  6  7  8  9 10 11
  # 12 13 14 15 16 17 18
  # 19 20 21 22 23 24 25
  # 26 27 28 29 30 31
  assert time_tuesday.count(datetime(2014,  0,  1), datetime(2014,  0,  6)) == 0
  assert time_tuesday.count(datetime(2014,  0,  1), datetime(2014,  0,  7)) == 1
  assert time_tuesday.count(datetime(2014,  0,  1), datetime(2014,  0,  8)) == 1
  assert time_tuesday.count(datetime(2014,  0,  1), datetime(2014,  0, 14)) == 2

  #     January 2013
  # Su Mo Tu We Th Fr Sa
  #        1  2  3  4  5
  #  6  7  8  9 10 11 12
  # 13 14 15 16 17 18 19
  # 20 21 22 23 24 25 26
  # 27 28 29 30 31
  assert time_tuesday.count(datetime(2013,  0,  1), datetime(2013,  0,  7)) == 0
  assert time_tuesday.count(datetime(2013,  0,  1), datetime(2013,  0,  8)) == 1
  assert time_tuesday.count(datetime(2013,  0,  1), datetime(2013,  0,  9)) == 1


def test_time_tuesday_count():
  assert time_tuesday.count(datetime(2011,  0,  1), datetime(2011,  2, 13,  1)) == 10
  assert time_tuesday.count(datetime(2011,  0,  1), datetime(2011,  2, 13,  3)) == 10
  assert time_tuesday.count(datetime(2011,  0,  1), datetime(2011,  2, 13,  4)) == 10
  assert time_tuesday.count(datetime(2011,  0,  1), datetime(2011, 10,  6,  0)) == 44
  assert time_tuesday.count(datetime(2011,  0,  1), datetime(2011, 10,  6,  1)) == 44
  assert time_tuesday.count(datetime(2011,  0,  1), datetime(2011, 10,  6,  2)) == 44

