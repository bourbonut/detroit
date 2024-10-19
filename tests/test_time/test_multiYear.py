import detroit as d3
from datetime import datetime

def test_time_year_every():
  assert time_year.every(10).floor(datetime(2009, 11, 31, 23, 59, 59)) == datetime(2000,  0,  1)
  assert time_year.every(10).floor(datetime(2010,  0,  1,  0,  0,  0)) == datetime(2010,  0,  1)
  assert time_year.every(10).floor(datetime(2010,  0,  1,  0,  0,  1)) == datetime(2010,  0,  1)


def test_time_year_every():
  assert time_year.every(100).ceil(datetime(1999, 11, 31, 23, 59, 59)) == datetime(2000,  0,  1)
  assert time_year.every(100).ceil(datetime(2000,  0,  1,  0,  0,  0)) == datetime(2000,  0,  1)
  assert time_year.every(100).ceil(datetime(2000,  0,  1,  0,  0,  1)) == datetime(2100,  0,  1)


def test_unknown():
  const d = datetime(2010, 11, 31, 23, 59, 59, 999);
  time_year.every(5).offset(d, +1);
  assert.deepStrictEqual(d, datetime(2010, 11, 31, 23, 59, 59, 999));


def test_time_year_every():
  assert time_year.every(5).offset(datetime(2010, 11, 31, 23, 59, 59, 999), +1), datetime(2015, 11, 31, 23, 59, 59, 999)
  assert time_year.every(5).offset(datetime(2010, 11, 31, 23, 59, 59, 456), -2), datetime(2000, 11, 31, 23, 59, 59, 456)


def test_unknown():
  const decade = time_year.every(10);
  assert.strictEqual(decade.count, undefined);
  assert.strictEqual(decade.every, undefined);


def test_unknown():
  assert.deepStrictEqual(time_year.every(10).range(datetime(2010, 0, 1), datetime(2031, 0, 1)) == [
    datetime(2010, 0, 1),
    datetime(2020, 0, 1),
    datetime(2030, 0, 1)
  ]);

