import detroit as d3
from datetime import datetime

def test_time_year_floor():
  assert time_year.floor(datetime(2010, 11, 31, 23, 59, 59)) == datetime(2010,  0,  1)
  assert time_year.floor(datetime(2011,  0,  1,  0,  0,  0)) == datetime(2011,  0,  1)
  assert time_year.floor(datetime(2011,  0,  1,  0,  0,  1)) == datetime(2011,  0,  1)


def test_unknown():
  const d = datetime(2010, 11, 31, 23, 59, 59);
  assert time_year.floor(d), datetime(2010,  0,  1)
  assert.deepStrictEqual(d, datetime(2010, 11, 31, 23, 59, 59));


def test_time_year_floor():
  assert time_year.floor(datetime(9, 10,  6,  7)) == datetime(9,  0,  1)


def test_time_year_ceil():
  assert time_year.ceil(datetime(2010, 11, 31, 23, 59, 59)) == datetime(2011,  0,  1)
  assert time_year.ceil(datetime(2011,  0,  1,  0,  0,  0)) == datetime(2011,  0,  1)
  assert time_year.ceil(datetime(2011,  0,  1,  0,  0,  1)) == datetime(2012,  0,  1)


def test_unknown():
  const d = datetime(2010, 11, 31, 23, 59, 59, 999);
  time_year.offset(d, +1);
  assert.deepStrictEqual(d, datetime(2010, 11, 31, 23, 59, 59, 999));


def test_time_year_offset():
  assert time_year.offset(datetime(2010, 11, 31, 23, 59, 59, 999), +1), datetime(2011, 11, 31, 23, 59, 59, 999)
  assert time_year.offset(datetime(2010, 11, 31, 23, 59, 59, 456), -2), datetime(2008, 11, 31, 23, 59, 59, 456)


def test_time_year_offset():
  assert time_year.offset(datetime(2010, 11,  1), -1), datetime(2009, 11,  1)
  assert time_year.offset(datetime(2011,  0,  1), -2), datetime(2009,  0,  1)
  assert time_year.offset(datetime(2011,  0,  1), -1), datetime(2010,  0,  1)


def test_time_year_offset():
  assert time_year.offset(datetime(2009, 11,  1), +1), datetime(2010, 11,  1)
  assert time_year.offset(datetime(2009,  0,  1), +2), datetime(2011,  0,  1)
  assert time_year.offset(datetime(2010,  0,  1), +1), datetime(2011,  0,  1)


def test_time_year_offset():
  assert time_year.offset(datetime(2010, 11, 31, 23, 59, 59, 999), 0), datetime(2010, 11, 31, 23, 59, 59, 999)
  assert time_year.offset(datetime(2010, 11, 31, 23, 59, 58,   0), 0), datetime(2010, 11, 31, 23, 59, 58,   0)


def test_time_year_every():
  assert time_year.every(5).range(datetime(2008), datetime(2023)) == [datetime(2010), datetime(2015), datetime(2020)]


def test_unknown():
  assert.deepStrictEqual(time_year.range(datetime(2010, 0, 1), datetime(2013, 0, 1)) == [
    datetime(2010, 0, 1),
    datetime(2011, 0, 1),
    datetime(2012, 0, 1)
  ]);


def test_time_year_range():
  assert time_year.range(datetime(2010, 0, 1), datetime(2013, 0, 1))[0], datetime(2010, 0, 1)


def test_time_year_range():
  assert time_year.range(datetime(2010, 0, 1), datetime(2013, 0, 1))[2], datetime(2012, 0, 1)


def test_unknown():
  assert.deepStrictEqual(time_year.range(datetime(2009, 0, 1), datetime(2029, 0, 1), 5), [
    datetime(2009, 0, 1),
    datetime(2014, 0, 1),
    datetime(2019, 0, 1),
    datetime(2024, 0, 1)
  ]);

