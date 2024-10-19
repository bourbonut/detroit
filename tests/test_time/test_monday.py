import detroit as d3
from datetime import datetime

def test_unknown():
  assert.strictEqual(time_mondays, time_monday.range);


def test_time_monday_floor():
  assert time_monday.floor(datetime(2011,  0,  1, 23, 59, 59)) == datetime(2010, 11, 27)
  assert time_monday.floor(datetime(2011,  0,  2,  0,  0,  0)) == datetime(2010, 11, 27)
  assert time_monday.floor(datetime(2011,  0,  2,  0,  0,  1)) == datetime(2010, 11, 27)
  assert time_monday.floor(datetime(2011,  0,  2, 23, 59, 59)) == datetime(2010, 11, 27)
  assert time_monday.floor(datetime(2011,  0,  3,  0,  0,  0)) == datetime(2011,  0,  3)
  assert time_monday.floor(datetime(2011,  0,  3,  0,  0,  1)) == datetime(2011,  0,  3)


def test_unknown():
  assert.deepStrictEqual(time_monday.range(datetime(2011, 11,  1), datetime(2012,  0, 15), 2), [
    datetime(2011, 11,  5),
    datetime(2011, 11, 19),
    datetime(2012,  0,  2)
  ]);


def test_unknown():
  #     January 2014
  # Su Mo Tu We Th Fr Sa
  #           1  2  3  4
  #  5  6  7  8  9 10 11
  # 12 13 14 15 16 17 18
  # 19 20 21 22 23 24 25
  # 26 27 28 29 30 31
  assert time_monday.count(datetime(2014,  0,  1), datetime(2014,  0,  5)) == 0
  assert time_monday.count(datetime(2014,  0,  1), datetime(2014,  0,  6)) == 1
  assert time_monday.count(datetime(2014,  0,  1), datetime(2014,  0,  7)) == 1
  assert time_monday.count(datetime(2014,  0,  1), datetime(2014,  0, 13)) == 2

  #     January 2018
  # Su Mo Tu We Th Fr Sa
  #     1  2  3  4  5  6
  #  7  8  9 10 11 12 13
  # 14 15 16 17 18 19 20
  # 21 22 23 24 25 26 27
  # 28 29 30 31
  assert time_monday.count(datetime(2018,  0,  1), datetime(2018,  0,  7)) == 0
  assert time_monday.count(datetime(2018,  0,  1), datetime(2018,  0,  8)) == 1
  assert time_monday.count(datetime(2018,  0,  1), datetime(2018,  0,  9)) == 1


def test_time_monday_count():
  assert time_monday.count(datetime(2011,  0,  1), datetime(2011,  2, 13,  1)) == 10
  assert time_monday.count(datetime(2011,  0,  1), datetime(2011,  2, 13,  3)) == 10
  assert time_monday.count(datetime(2011,  0,  1), datetime(2011,  2, 13,  4)) == 10
  assert time_monday.count(datetime(2011,  0,  1), datetime(2011, 10,  6,  0)) == 44
  assert time_monday.count(datetime(2011,  0,  1), datetime(2011, 10,  6,  1)) == 44
  assert time_monday.count(datetime(2011,  0,  1), datetime(2011, 10,  6,  2)) == 44

