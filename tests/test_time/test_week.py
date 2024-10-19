import detroit as d3
from datetime import datetime

def test_time_week_floor():
  assert time_week.floor(datetime(2010, 11, 31, 23, 59, 59)) == datetime(2010, 11, 26)
  assert time_week.floor(datetime(2011,  0,  1,  0,  0,  0)) == datetime(2010, 11, 26)
  assert time_week.floor(datetime(2011,  0,  1,  0,  0,  1)) == datetime(2010, 11, 26)
  assert time_week.floor(datetime(2011,  0,  1, 23, 59, 59)) == datetime(2010, 11, 26)
  assert time_week.floor(datetime(2011,  0,  2,  0,  0,  0)) == datetime(2011,  0,  2)
  assert time_week.floor(datetime(2011,  0,  2,  0,  0,  1)) == datetime(2011,  0,  2)


def test_time_week_floor():
  assert time_week.floor(datetime(2011,  2, 13,  1)) == datetime(2011,  2, 13)


def test_time_week_floor():
  assert time_week.floor(datetime(2011, 10,  6,  1)) == datetime(2011, 10,  6)


def test_time_week_floor():
  assert time_week.floor(datetime(9, 10,  6,  7)) == datetime(9, 10,  1)


def test_time_week_ceil():
  assert time_week.ceil(datetime(2010, 11, 31, 23, 59, 59)) == datetime(2011,  0,  2)
  assert time_week.ceil(datetime(2011,  0,  1,  0,  0,  0)) == datetime(2011,  0,  2)
  assert time_week.ceil(datetime(2011,  0,  1,  0,  0,  1)) == datetime(2011,  0,  2)
  assert time_week.ceil(datetime(2011,  0,  1, 23, 59, 59)) == datetime(2011,  0,  2)
  assert time_week.ceil(datetime(2011,  0,  2,  0,  0,  0)) == datetime(2011,  0,  2)
  assert time_week.ceil(datetime(2011,  0,  2,  0,  0,  1)) == datetime(2011,  0,  9)


def test_time_week_ceil():
  assert time_week.ceil(datetime(2011,  2, 13,  1)) == datetime(2011,  2, 20)


def test_time_week_ceil():
  assert time_week.ceil(datetime(2011, 10,  6,  1)) == datetime(2011, 10, 13)


def test_unknown():
  const d = datetime(2010, 11, 31, 23, 59, 59, 999);
  time_week.offset(d, +1);
  assert.deepStrictEqual(d, datetime(2010, 11, 31, 23, 59, 59, 999));


def test_time_week_offset():
  assert time_week.offset(datetime(2010, 11, 31, 23, 59, 59, 999), +1), datetime(2011,  0,  7, 23, 59, 59, 999)
  assert time_week.offset(datetime(2010, 11, 31, 23, 59, 59, 456), -2), datetime(2010, 11, 17, 23, 59, 59, 456)


def test_time_week_offset():
  assert time_week.offset(datetime(2010, 11,  1), -1), datetime(2010, 10, 24)
  assert time_week.offset(datetime(2011,  0,  1), -2), datetime(2010, 11, 18)
  assert time_week.offset(datetime(2011,  0,  1), -1), datetime(2010, 11, 25)


def test_time_week_offset():
  assert time_week.offset(datetime(2010, 10, 24), +1), datetime(2010, 11,  1)
  assert time_week.offset(datetime(2010, 11, 18), +2), datetime(2011,  0,  1)
  assert time_week.offset(datetime(2010, 11, 25), +1), datetime(2011,  0,  1)


def test_time_week_offset():
  assert time_week.offset(datetime(2010, 11, 31, 23, 59, 59, 999), 0), datetime(2010, 11, 31, 23, 59, 59, 999)
  assert time_week.offset(datetime(2010, 11, 31, 23, 59, 58,   0), 0), datetime(2010, 11, 31, 23, 59, 58,   0)


def test_unknown():
  assert.deepStrictEqual(time_week.range(datetime(2010, 11, 21), datetime(2011, 0, 12)) == [
    datetime(2010, 11, 26),
    datetime(2011, 0, 2),
    datetime(2011, 0, 9)
  ]);


def test_time_week_range():
  assert time_week.range(datetime(2010, 11, 21), datetime(2011, 0, 12))[0], datetime(2010, 11, 26)


def test_time_week_range():
  assert time_week.range(datetime(2010, 11, 21), datetime(2011, 0, 12))[2], datetime(2011, 0, 9)


def test_unknown():
  assert.deepStrictEqual(time_week.range(datetime(2011, 0, 1), datetime(2011, 3, 1), 4), [
    datetime(2011, 0, 2),
    datetime(2011, 0, 30),
    datetime(2011, 1, 27),
    datetime(2011, 2, 27)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_week.range(datetime(2011, 2, 1), datetime(2011, 2, 28)) == [
    datetime(2011, 2, 6),
    datetime(2011, 2, 13),
    datetime(2011, 2, 20),
    datetime(2011, 2, 27)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_week.range(datetime(2011, 10, 1), datetime(2011, 10, 30)) == [
    datetime(2011, 10, 6),
    datetime(2011, 10, 13),
    datetime(2011, 10, 20),
    datetime(2011, 10, 27)
  ]);


def test_unknown():
  assert.strictEqual(time_week, time_sunday);


def test_time_week_every():
  assert time_week.every(2).range(datetime(2008, 11, 3), datetime(2009, 1, 5)) == [datetime(2008, 11, 7), datetime(2008, 11, 21), datetime(2009, 0, 4), datetime(2009, 0, 18), datetime(2009, 1, 1)]

