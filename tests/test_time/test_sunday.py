import detroit as d3
from datetime import datetime

def test_unknown():
  assert.strictEqual(time_sundays, time_sunday.range);


def test_time_sunday_floor():
  assert time_sunday.floor(datetime(2010, 11, 31, 23, 59, 59)) == datetime(2010, 11, 26)
  assert time_sunday.floor(datetime(2011,  0,  1,  0,  0,  0)) == datetime(2010, 11, 26)
  assert time_sunday.floor(datetime(2011,  0,  1,  0,  0,  1)) == datetime(2010, 11, 26)
  assert time_sunday.floor(datetime(2011,  0,  1, 23, 59, 59)) == datetime(2010, 11, 26)
  assert time_sunday.floor(datetime(2011,  0,  2,  0,  0,  0)) == datetime(2011,  0,  2)
  assert time_sunday.floor(datetime(2011,  0,  2,  0,  0,  1)) == datetime(2011,  0,  2)


def test_time_sunday_floor():
  assert time_sunday.floor(datetime(2011,  2, 13,  1)) == datetime(2011,  2, 13)
  assert time_sunday.floor(datetime(2011, 10,  6,  1)) == datetime(2011, 10,  6)


def test_time_sunday_floor():
  assert time_sunday.floor(datetime(9, 10,  6,  7)) == datetime(9, 10,  1)


def test_time_sunday_ceil():
  assert time_sunday.ceil(datetime(2010, 11, 31, 23, 59, 59)) == datetime(2011,  0,  2)
  assert time_sunday.ceil(datetime(2011,  0,  1,  0,  0,  0)) == datetime(2011,  0,  2)
  assert time_sunday.ceil(datetime(2011,  0,  1,  0,  0,  1)) == datetime(2011,  0,  2)
  assert time_sunday.ceil(datetime(2011,  0,  1, 23, 59, 59)) == datetime(2011,  0,  2)
  assert time_sunday.ceil(datetime(2011,  0,  2,  0,  0,  0)) == datetime(2011,  0,  2)
  assert time_sunday.ceil(datetime(2011,  0,  2,  0,  0,  1)) == datetime(2011,  0,  9)


def test_time_sunday_ceil():
  assert time_sunday.ceil(datetime(2011,  2, 13,  1)) == datetime(2011,  2, 20)
  assert time_sunday.ceil(datetime(2011, 10,  6,  1)) == datetime(2011, 10, 13)


def test_time_sunday_offset():
  assert time_sunday.offset(datetime(2010, 11, 31, 23, 59, 59, 999)) == datetime(2011,  0,  7, 23, 59, 59, 999)


def test_unknown():
  const d = datetime(2010, 11, 31, 23, 59, 59, 999);
  time_sunday.offset(d, +1);
  assert.deepStrictEqual(d, datetime(2010, 11, 31, 23, 59, 59, 999));


def test_time_sunday_offset():
  assert time_sunday.offset(datetime(2010, 11, 31, 23, 59, 59, 999), +1), datetime(2011,  0,  7, 23, 59, 59, 999)
  assert time_sunday.offset(datetime(2010, 11, 31, 23, 59, 59, 456), -2), datetime(2010, 11, 17, 23, 59, 59, 456)


def test_time_sunday_offset():
  assert time_sunday.offset(datetime(2010, 11,  1), -1), datetime(2010, 10, 24)
  assert time_sunday.offset(datetime(2011,  0,  1), -2), datetime(2010, 11, 18)
  assert time_sunday.offset(datetime(2011,  0,  1), -1), datetime(2010, 11, 25)


def test_time_sunday_offset():
  assert time_sunday.offset(datetime(2010, 10, 24), +1), datetime(2010, 11,  1)
  assert time_sunday.offset(datetime(2010, 11, 18), +2), datetime(2011,  0,  1)
  assert time_sunday.offset(datetime(2010, 11, 25), +1), datetime(2011,  0,  1)


def test_time_sunday_offset():
  assert time_sunday.offset(datetime(2010, 11, 31, 23, 59, 59, 999), 0), datetime(2010, 11, 31, 23, 59, 59, 999)
  assert time_sunday.offset(datetime(2010, 11, 31, 23, 59, 58,   0), 0), datetime(2010, 11, 31, 23, 59, 58,   0)


def test_unknown():
  assert.deepStrictEqual(time_sunday.range(datetime(2011, 11,  1), datetime(2012,  0, 15)) == [
    datetime(2011, 11,  4),
    datetime(2011, 11, 11),
    datetime(2011, 11, 18),
    datetime(2011, 11, 25),
    datetime(2012,  0,  1),
    datetime(2012,  0,  8)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_sunday.range(datetime(2011, 11,  1, 12, 23), datetime(2012,  0, 14, 12, 23)) == [
    datetime(2011, 11,  4),
    datetime(2011, 11, 11),
    datetime(2011, 11, 18),
    datetime(2011, 11, 25),
    datetime(2012,  0,  1),
    datetime(2012,  0,  8)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_sunday.range(+datetime(2011, 11,  1), +datetime(2012,  0, 15)) == [
    datetime(2011, 11,  4),
    datetime(2011, 11, 11),
    datetime(2011, 11, 18),
    datetime(2011, 11, 25),
    datetime(2012,  0,  1),
    datetime(2012,  0,  8)
  ]);


def test_time_sunday_range():
  assert time_sunday.range(new Date(NaN), Infinity), []


def test_time_sunday_range():
  assert time_sunday.range(datetime(2011, 11, 10), datetime(2011, 10,  4)) == []
  assert time_sunday.range(datetime(2011, 10,  1), datetime(2011, 10,  1)) == []


def test_unknown():
  assert.deepStrictEqual(time_sunday.range(datetime(2011, 11,  1), datetime(2012,  0, 15), 2), [
    datetime(2011, 11,  4),
    datetime(2011, 11, 18),
    datetime(2012,  0,  1)
  ]);


def test_unknown():
  #     January 2014
  # Su Mo Tu We Th Fr Sa
  #           1  2  3  4
  #  5  6  7  8  9 10 11
  # 12 13 14 15 16 17 18
  # 19 20 21 22 23 24 25
  # 26 27 28 29 30 31
  assert time_sunday.count(datetime(2014,  0,  1), datetime(2014,  0,  4)) == 0
  assert time_sunday.count(datetime(2014,  0,  1), datetime(2014,  0,  5)) == 1
  assert time_sunday.count(datetime(2014,  0,  1), datetime(2014,  0,  6)) == 1
  assert time_sunday.count(datetime(2014,  0,  1), datetime(2014,  0, 12)) == 2

  #       January 2012
  # Su Mo Tu We Th Fr Sa
  #  1  2  3  4  5  6  7
  #  8  9 10 11 12 13 14
  # 15 16 17 18 19 20 21
  # 22 23 24 25 26 27 28
  # 29 30 31
  assert time_sunday.count(datetime(2012,  0,  1), datetime(2012,  0,  7)) == 0
  assert time_sunday.count(datetime(2012,  0,  1), datetime(2012,  0,  8)) == 1
  assert time_sunday.count(datetime(2012,  0,  1), datetime(2012,  0,  9)) == 1


def test_time_sunday_count():
  assert time_sunday.count(datetime(2011,  0,  1), datetime(2011,  2, 13,  1)) == 11
  assert time_sunday.count(datetime(2011,  0,  1), datetime(2011,  2, 13,  3)) == 11
  assert time_sunday.count(datetime(2011,  0,  1), datetime(2011,  2, 13,  4)) == 11
  assert time_sunday.count(datetime(2011,  0,  1), datetime(2011, 10,  6,  0)) == 45
  assert time_sunday.count(datetime(2011,  0,  1), datetime(2011, 10,  6,  1)) == 45
  assert time_sunday.count(datetime(2011,  0,  1), datetime(2011, 10,  6,  2)) == 45

