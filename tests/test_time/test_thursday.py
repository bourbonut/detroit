import detroit as d3
from datetime import datetime

def test_unknown():
  assert.strictEqual(time_thursdays, time_thursday.range);


def test_time_thursday_floor():
  assert time_thursday.floor(datetime(2011,  0,  4, 23, 59, 59)) == datetime(2010, 11, 30)
  assert time_thursday.floor(datetime(2011,  0,  5,  0,  0,  0)) == datetime(2010, 11, 30)
  assert time_thursday.floor(datetime(2011,  0,  5,  0,  0,  1)) == datetime(2010, 11, 30)
  assert time_thursday.floor(datetime(2011,  0,  5, 23, 59, 59)) == datetime(2010, 11, 30)
  assert time_thursday.floor(datetime(2011,  0,  6,  0,  0,  0)) == datetime(2011,  0,  6)
  assert time_thursday.floor(datetime(2011,  0,  6,  0,  0,  1)) == datetime(2011,  0,  6)


def test_unknown():
  #       January 2012
  # Su Mo Tu We Th Fr Sa
  #  1  2  3  4  5  6  7
  #  8  9 10 11 12 13 14
  # 15 16 17 18 19 20 21
  # 22 23 24 25 26 27 28
  # 29 30 31
  assert time_thursday.count(datetime(2012,  0,  1), datetime(2012,  0,  4)) == 0
  assert time_thursday.count(datetime(2012,  0,  1), datetime(2012,  0,  5)) == 1
  assert time_thursday.count(datetime(2012,  0,  1), datetime(2012,  0,  6)) == 1
  assert time_thursday.count(datetime(2012,  0,  1), datetime(2012,  0, 12)) == 2

  #     January 2015
  # Su Mo Tu We Th Fr Sa
  #              1  2  3
  #  4  5  6  7  8  9 10
  # 11 12 13 14 15 16 17
  # 18 19 20 21 22 23 24
  # 25 26 27 28 29 30 31
  assert time_thursday.count(datetime(2015,  0,  1), datetime(2015,  0,  7)) == 0
  assert time_thursday.count(datetime(2015,  0,  1), datetime(2015,  0,  8)) == 1
  assert time_thursday.count(datetime(2015,  0,  1), datetime(2015,  0,  9)) == 1


def test_time_thursday_count():
  assert time_thursday.count(datetime(2011,  0,  1), datetime(2011,  2, 13,  1)) == 10
  assert time_thursday.count(datetime(2011,  0,  1), datetime(2011,  2, 13,  3)) == 10
  assert time_thursday.count(datetime(2011,  0,  1), datetime(2011,  2, 13,  4)) == 10
  assert time_thursday.count(datetime(2011,  0,  1), datetime(2011, 10,  6,  0)) == 44
  assert time_thursday.count(datetime(2011,  0,  1), datetime(2011, 10,  6,  1)) == 44
  assert time_thursday.count(datetime(2011,  0,  1), datetime(2011, 10,  6,  2)) == 44

