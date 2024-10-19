import detroit as d3
from datetime import datetime

def test_unknown():
  assert.strictEqual(time_months, time_month.range);


def test_time_month_floor():
  assert time_month.floor(datetime(2010, 11, 31, 23, 59, 59)) == datetime(2010, 11,  1)
  assert time_month.floor(datetime(2011,  0,  1,  0,  0,  0)) == datetime(2011,  0,  1)
  assert time_month.floor(datetime(2011,  0,  1,  0,  0,  1)) == datetime(2011,  0,  1)


def test_time_month_floor():
  assert time_month.floor(datetime(2011,  2, 13,  1)) == datetime(2011,  2,  1)


def test_time_month_floor():
  assert time_month.floor(datetime(2011, 10,  6,  1)) == datetime(2011, 10,  1)


def test_time_month_floor():
  assert time_month.floor(datetime(9, 10,  6,  7)) == datetime(9, 10,  1)


def test_time_month_ceil():
  assert time_month.ceil(datetime(2010, 11, 31, 23, 59, 59)) == datetime(2011,  0,  1)
  assert time_month.ceil(datetime(2011,  0,  1,  0,  0,  0)) == datetime(2011,  0,  1)
  assert time_month.ceil(datetime(2011,  0,  1,  0,  0,  1)) == datetime(2011,  1,  1)


def test_time_month_ceil():
  assert time_month.ceil(datetime(2011,  2, 13,  1)) == datetime(2011,  3,  1)


def test_time_month_ceil():
  assert time_month.ceil(datetime(2011, 10,  6,  1)) == datetime(2011, 11,  1)


def test_unknown():
  const d = datetime(2010, 11, 31, 23, 59, 59, 999);
  time_month.offset(d, +1);
  assert.deepStrictEqual(d, datetime(2010, 11, 31, 23, 59, 59, 999));


def test_time_month_offset():
  assert time_month.offset(datetime(2010, 11, 31, 23, 59, 59, 999), +1), datetime(2011,  0, 31, 23, 59, 59, 999)
  assert time_month.offset(datetime(2010, 11, 31, 23, 59, 59, 456), -2), datetime(2010,  9, 31, 23, 59, 59, 456)


def test_time_month_offset():
  assert time_month.offset(datetime(2010, 11,  1), -1), datetime(2010, 10,  1)
  assert time_month.offset(datetime(2011,  0,  1), -2), datetime(2010, 10,  1)
  assert time_month.offset(datetime(2011,  0,  1), -1), datetime(2010, 11,  1)


def test_time_month_offset():
  assert time_month.offset(datetime(2010, 10,  1), +1), datetime(2010, 11,  1)
  assert time_month.offset(datetime(2010, 10,  1), +2), datetime(2011,  0,  1)
  assert time_month.offset(datetime(2010, 11,  1), +1), datetime(2011,  0,  1)


def test_time_month_offset():
  assert time_month.offset(datetime(2010, 11, 31, 23, 59, 59, 999), 0), datetime(2010, 11, 31, 23, 59, 59, 999)
  assert time_month.offset(datetime(2010, 11, 31, 23, 59, 58,   0), 0), datetime(2010, 11, 31, 23, 59, 58,   0)


def test_unknown():
  assert.strictEqual(time_months, time_month.range);


def test_time_month_floor():
  assert time_month.floor(datetime(2010, 11, 31, 23)) == datetime(2010, 11,  1)
  assert time_month.floor(datetime(2011,  0,  1,  0)) == datetime(2011,  0,  1)
  assert time_month.floor(datetime(2011,  0,  1,  1)) == datetime(2011,  0,  1)


def test_time_month_floor():
  assert time_month.floor(datetime(2011,  2, 13,  7)) == datetime(2011,  2,  1)
  assert time_month.floor(datetime(2011,  2, 13,  8)) == datetime(2011,  2,  1)
  assert time_month.floor(datetime(2011,  2, 13,  9)) == datetime(2011,  2,  1)
  assert time_month.floor(datetime(2011,  2, 13, 10)) == datetime(2011,  2,  1)
  assert time_month.floor(datetime(2011, 10,  6,  7)) == datetime(2011, 10,  1)
  assert time_month.floor(datetime(2011, 10,  6,  8)) == datetime(2011, 10,  1)
  assert time_month.floor(datetime(2011, 10,  6,  9)) == datetime(2011, 10,  1)
  assert time_month.floor(datetime(2011, 10,  6, 10)) == datetime(2011, 10,  1)


def test_time_month_floor():
  assert time_month.floor(datetime(9, 10,  6,  7)) == datetime(9, 10,  1)


def test_time_month_round():
  assert time_month.round(datetime(2010, 11, 16, 12)) == datetime(2011,  0,  1)
  assert time_month.round(datetime(2010, 11, 16, 11)) == datetime(2010, 11,  1)


def test_time_month_round():
  assert time_month.round(datetime(2011,  2, 13,  7)) == datetime(2011,  2,  1)
  assert time_month.round(datetime(2011,  2, 13,  8)) == datetime(2011,  2,  1)
  assert time_month.round(datetime(2011,  2, 13,  9)) == datetime(2011,  2,  1)
  assert time_month.round(datetime(2011,  2, 13, 20)) == datetime(2011,  2,  1)
  assert time_month.round(datetime(2011, 10,  6,  7)) == datetime(2011, 10,  1)
  assert time_month.round(datetime(2011, 10,  6,  8)) == datetime(2011, 10,  1)
  assert time_month.round(datetime(2011, 10,  6,  9)) == datetime(2011, 10,  1)
  assert time_month.round(datetime(2011, 10,  6, 20)) == datetime(2011, 10,  1)


def test_time_month_round():
  assert time_month.round(datetime(2012,  2,  1,  0)) == datetime(2012,  2,  1)
  assert time_month.round(datetime(2012,  2,  1,  0)) == datetime(2012,  2,  1)


def test_time_month_ceil():
  assert time_month.ceil(datetime(2010, 10, 30, 23)) == datetime(2010, 11,  1)
  assert time_month.ceil(datetime(2010, 11,  1,  1)) == datetime(2011,  0,  1)
  assert time_month.ceil(datetime(2011, 1, 1)) == datetime(2011, 1, 1)
  assert time_month.ceil(datetime(2011, 2, 1)) == datetime(2011, 2, 1)
  assert time_month.ceil(datetime(2011, 3, 1)) == datetime(2011, 3, 1)


def test_time_month_ceil():
  assert time_month.ceil(datetime(2011,  2, 13,  7)) == datetime(2011,  3,  1)
  assert time_month.ceil(datetime(2011,  2, 13,  8)) == datetime(2011,  3,  1)
  assert time_month.ceil(datetime(2011,  2, 13,  9)) == datetime(2011,  3,  1)
  assert time_month.ceil(datetime(2011,  2, 13, 10)) == datetime(2011,  3,  1)
  assert time_month.ceil(datetime(2011, 10,  6,  7)) == datetime(2011, 11,  1)
  assert time_month.ceil(datetime(2011, 10,  6,  8)) == datetime(2011, 11,  1)
  assert time_month.ceil(datetime(2011, 10,  6,  9)) == datetime(2011, 11,  1)
  assert time_month.ceil(datetime(2011, 10,  6, 10)) == datetime(2011, 11,  1)


def test_time_month_ceil():
  assert time_month.ceil(datetime(2012,  2,  1,  0)) == datetime(2012,  2,  1)
  assert time_month.ceil(datetime(2012,  2,  1,  0)) == datetime(2012,  2,  1)


def test_time_month_offset():
  assert time_month.offset(datetime(2010, 11, 31, 23, 59, 59, 999)) == datetime(2011,  0, 31, 23, 59, 59, 999)


def test_unknown():
  const d = datetime(2010, 11, 31, 23, 59, 59, 999);
  time_month.offset(d, +1);
  assert.deepStrictEqual(d, datetime(2010, 11, 31, 23, 59, 59, 999));


def test_time_month_offset():
  assert time_month.offset(datetime(2010, 11, 31, 23, 59, 59, 999), +1), datetime(2011,  0, 31, 23, 59, 59, 999)
  assert time_month.offset(datetime(2010, 11, 31, 23, 59, 59, 456), -2), datetime(2010,  9, 31, 23, 59, 59, 456)


def test_time_month_offset():
  assert time_month.offset(datetime(2010, 11, 31), -1), datetime(2010, 10, 31)
  assert time_month.offset(datetime(2011,  0,  1), -2), datetime(2010, 10,  1)
  assert time_month.offset(datetime(2011,  0,  1), -1), datetime(2010, 11,  1)


def test_time_month_offset():
  assert time_month.offset(datetime(2010, 11, 31), +1), datetime(2011,  0, 31)
  assert time_month.offset(datetime(2010, 11, 30), +2), datetime(2011,  1, 30)
  assert time_month.offset(datetime(2010, 11, 30), +1), datetime(2011,  0, 30)


def test_time_month_offset():
  assert time_month.offset(datetime(2010, 11, 31, 23, 59, 59, 999), 0), datetime(2010, 11, 31, 23, 59, 59, 999)
  assert time_month.offset(datetime(2010, 11, 31, 23, 59, 58,   0), 0), datetime(2010, 11, 31, 23, 59, 58,   0)


def test_unknown():
  assert.deepStrictEqual(time_month.range(datetime(2011, 11,  1), datetime(2012,  5,  1)) == [
    datetime(2011, 11,  1),
    datetime(2012,  0,  1),
    datetime(2012,  1,  1),
    datetime(2012,  2,  1),
    datetime(2012,  3,  1),
    datetime(2012,  4,  1)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_month.range(datetime(2011, 10,  4,  2), datetime(2012,  4, 10, 13)) == [
    datetime(2011, 11,  1),
    datetime(2012,  0,  1),
    datetime(2012,  1,  1),
    datetime(2012,  2,  1),
    datetime(2012,  3,  1),
    datetime(2012,  4,  1)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_month.range(+datetime(2011, 10,  4), +datetime(2012,  1,  7)) == [
    datetime(2011, 11,  1),
    datetime(2012,  0,  1),
    datetime(2012,  1,  1)
  ]);


def test_time_month_range():
  assert time_month.range(new Date(NaN), Infinity), []


def test_time_month_range():
  assert time_month.range(datetime(2011, 11, 10), datetime(2011, 10,  4)) == []
  assert time_month.range(datetime(2011, 10,  1), datetime(2011, 10,  1)) == []


def test_unknown():
  assert.deepStrictEqual(time_month.range(datetime(2010, 10, 31), datetime(2011, 2, 1)) == [
    datetime(2010, 11, 1),
    datetime(2011, 0, 1),
    datetime(2011, 1, 1)
  ]);


def test_time_month_range():
  assert time_month.range(datetime(2010, 10, 31), datetime(2011, 2, 1))[0], datetime(2010, 11, 1)


def test_time_month_range():
  assert time_month.range(datetime(2010, 10, 31), datetime(2011, 2, 1))[2], datetime(2011, 1, 1)


def test_unknown():
  assert.deepStrictEqual(time_month.range(datetime(2011, 1, 1), datetime(2012, 1, 1), 3), [
    datetime(2011, 1, 1),
    datetime(2011, 4, 1),
    datetime(2011, 7, 1),
    datetime(2011, 10, 1)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_month.range(datetime(2011, 0, 1), datetime(2011, 4, 1)) == [
    datetime(2011, 0, 1),
    datetime(2011, 1, 1),
    datetime(2011, 2, 1),
    datetime(2011, 3, 1)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_month.range(datetime(2011, 9, 1), datetime(2012, 1, 1)) == [
    datetime(2011, 9, 1),
    datetime(2011, 10, 1),
    datetime(2011, 11, 1),
    datetime(2012, 0, 1)
  ]);


def test_time_month_count():
  assert time_month.count(datetime(2011,  0,  1), datetime(2011,  4,  1)) == 4
  assert time_month.count(datetime(2011,  0,  1), datetime(2011,  3, 30)) == 3
  assert time_month.count(datetime(2010, 11, 31), datetime(2011,  3, 30)) == 4
  assert time_month.count(datetime(2010, 11, 31), datetime(2011,  4,  1)) == 5
  assert time_month.count(datetime(2009, 11, 31), datetime(2012,  4,  1)) == 29
  assert time_month.count(datetime(2012,  4,  1), datetime(2009, 11, 31)) == -29


def test_time_month_every():
  assert time_month.every(3).range(datetime(2008, 11, 3), datetime(2010, 6, 5)) == [datetime(2009, 0, 1), datetime(2009, 3, 1), datetime(2009, 6, 1), datetime(2009, 9, 1), datetime(2010, 0, 1), datetime(2010, 3, 1), datetime(2010, 6, 1)]

