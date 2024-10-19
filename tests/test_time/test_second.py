import detroit as d3
from datetime import datetime

def test_time_second_floor():
  assert time_second.floor(datetime(2010, 11, 31, 23, 59, 59, 999)) == datetime(2010, 11, 31, 23, 59, 59)
  assert time_second.floor(datetime(2011,  0,  1,  0,  0,  0,   0)) == datetime(2011,  0,  1,  0,  0,  0)
  assert time_second.floor(datetime(2011,  0,  1,  0,  0,  0,   1)) == datetime(2011,  0,  1,  0,  0,  0)


def test_time_second_round():
  assert time_second.round(datetime(2010, 11, 31, 23, 59, 59, 999)) == datetime(2011,  0,  1,  0,  0,  0)
  assert time_second.round(datetime(2011,  0,  1,  0,  0,  0, 499)) == datetime(2011,  0,  1,  0,  0,  0)
  assert time_second.round(datetime(2011,  0,  1,  0,  0,  0, 500)) == datetime(2011,  0,  1,  0,  0,  1)


def test_time_second_ceil():
  assert time_second.ceil(datetime(2010, 11, 31, 23, 59, 59, 999)) == datetime(2011,  0,  1,  0,  0,  0)
  assert time_second.ceil(datetime(2011,  0,  1,  0,  0,  0,   0)) == datetime(2011,  0,  1,  0,  0,  0)
  assert time_second.ceil(datetime(2011,  0,  1,  0,  0,  0,   1)) == datetime(2011,  0,  1,  0,  0,  1)


def test_unknown():
  const d = datetime(2010, 11, 31, 23, 59, 59, 999);
  time_second.offset(d, +1);
  assert.deepStrictEqual(d, datetime(2010, 11, 31, 23, 59, 59, 999));


def test_time_second_offset():
  assert time_second.offset(datetime(2010, 11, 31, 23, 59, 59, 999), +1), datetime(2011,  0,  1,  0,  0,  0, 999)
  assert time_second.offset(datetime(2010, 11, 31, 23, 59, 59, 456), -2), datetime(2010, 11, 31, 23, 59, 57, 456)


def test_time_second_offset():
  assert time_second.offset(datetime(2010, 11, 31, 23, 59, 59), -1), datetime(2010, 11, 31, 23, 59, 58)
  assert time_second.offset(datetime(2011,  0,  1,  0,  0,  0), -2), datetime(2010, 11, 31, 23, 59, 58)
  assert time_second.offset(datetime(2011,  0,  1,  0,  0,  0), -1), datetime(2010, 11, 31, 23, 59, 59)


def test_time_second_offset():
  assert time_second.offset(datetime(2010, 11, 31, 23, 59, 58), +1), datetime(2010, 11, 31, 23, 59, 59)
  assert time_second.offset(datetime(2010, 11, 31, 23, 59, 58), +2), datetime(2011,  0,  1,  0,  0,  0)
  assert time_second.offset(datetime(2010, 11, 31, 23, 59, 59), +1), datetime(2011,  0,  1,  0,  0,  0)


def test_time_second_offset():
  assert time_second.offset(datetime(2010, 11, 31, 23, 59, 59, 999), 0), datetime(2010, 11, 31, 23, 59, 59, 999)
  assert time_second.offset(datetime(2010, 11, 31, 23, 59, 58,   0), 0), datetime(2010, 11, 31, 23, 59, 58,   0)


def test_unknown():
  assert.deepStrictEqual(time_second.range(datetime(2010, 11, 31, 23, 59, 59), datetime(2011, 0, 1, 0, 0, 2)) == [
    datetime(2010, 11, 31, 23, 59, 59),
    datetime(2011, 0, 1, 0, 0, 0),
    datetime(2011, 0, 1, 0, 0, 1)
  ]);


def test_time_second_range():
  assert time_second.range(datetime(2010, 11, 31, 23, 59, 59), datetime(2011, 0, 1, 0, 0, 2))[0], datetime(2010, 11, 31, 23, 59, 59)


def test_time_second_range():
  assert time_second.range(datetime(2010, 11, 31, 23, 59, 59), datetime(2011, 0, 1, 0, 0, 2))[2], datetime(2011, 0, 1, 0, 0, 1)


def test_unknown():
  assert.deepStrictEqual(time_second.range(datetime(2011, 1, 1, 12, 0, 7), datetime(2011, 1, 1, 12, 1, 7), 15), [
    datetime(2011, 1, 1, 12, 0, 7),
    datetime(2011, 1, 1, 12, 0, 22),
    datetime(2011, 1, 1, 12, 0, 37),
    datetime(2011, 1, 1, 12, 0, 52)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_second.range(datetime(2011, 2, 13, 9, 59, 59), datetime(2011, 2, 13, 10, 0, 2)) == [
    datetime(2011, 2, 13, 9, 59, 59),
    datetime(2011, 2, 13, 10, 0, 0),
    datetime(2011, 2, 13, 10, 0, 1)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_second.range(datetime(2011, 10, 6, 8, 59, 59), datetime(2011, 10, 6, 9, 0, 2)) == [
    datetime(2011, 10, 6, 8, 59, 59),
    datetime(2011, 10, 6, 9, 0, 0),
    datetime(2011, 10, 6, 9, 0, 1)
  ]);


def test_time_second_every():
  assert time_second.every(15).range(datetime(2008, 11, 30, 12, 36, 47), datetime(2008, 11, 30, 12, 37, 57)) == [datetime(2008, 11, 30, 12, 37, 0), datetime(2008, 11, 30, 12, 37, 15), datetime(2008, 11, 30, 12, 37, 30), datetime(2008, 11, 30, 12, 37, 45)]
  assert time_second.every(30).range(datetime(2008, 11, 30, 12, 36, 47), datetime(2008, 11, 30, 12, 37, 57)) == [datetime(2008, 11, 30, 12, 37, 0), datetime(2008, 11, 30, 12, 37, 30)]


def test_unknown():
  assert.deepStrictEqual(time_second.range(new Date(1478422800000 - 2 * 1e3), new Date(1478422800000 + 2 * 1e3)) == [
    new Date(1478422798000), # Sun Nov  6 2016  1:59:58 GMT-0700 (PDT)
    new Date(1478422799000), # Sun Nov  6 2016  1:59:59 GMT-0700 (PDT)
    new Date(1478422800000), # Sun Nov  6 2016  1:00:00 GMT-0800 (PDT)
    new Date(1478422801000)  # Sun Nov  6 2016  1:00:01 GMT-0800 (PDT)
  ]);

