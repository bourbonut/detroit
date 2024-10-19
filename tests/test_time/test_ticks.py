import detroit as d3
from datetime import datetime

def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 12, 1, 0), datetime(2011, 0, 1, 12, 4, 4), time_minute), [
    datetime(2011, 0, 1, 12, 1),
    datetime(2011, 0, 1, 12, 2),
    datetime(2011, 0, 1, 12, 3),
    datetime(2011, 0, 1, 12, 4)
  ]);


def test_time_ticks_():
  assert time_ticks(NaN, NaN, 10), []


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 12, 0, 0), datetime(2011, 0, 1, 12, 33, 4), time_minute.every(10)) == [
    datetime(2011, 0, 1, 12, 0),
    datetime(2011, 0, 1, 12, 10),
    datetime(2011, 0, 1, 12, 20),
    datetime(2011, 0, 1, 12, 30)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 12, 0, 0), datetime(2011, 0, 1, 12, 0, 1), 4), [
    datetime(2011, 0, 1, 12, 0, 0,   0),
    datetime(2011, 0, 1, 12, 0, 0, 200),
    datetime(2011, 0, 1, 12, 0, 0, 400),
    datetime(2011, 0, 1, 12, 0, 0, 600),
    datetime(2011, 0, 1, 12, 0, 0, 800),
    datetime(2011, 0, 1, 12, 0, 1,   0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 12, 0, 0), datetime(2011, 0, 1, 12, 0, 4), 4), [
    datetime(2011, 0, 1, 12, 0, 0),
    datetime(2011, 0, 1, 12, 0, 1),
    datetime(2011, 0, 1, 12, 0, 2),
    datetime(2011, 0, 1, 12, 0, 3),
    datetime(2011, 0, 1, 12, 0, 4)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 12, 0, 0), datetime(2011, 0, 1, 12, 0, 20), 4), [
    datetime(2011, 0, 1, 12, 0, 0),
    datetime(2011, 0, 1, 12, 0, 5),
    datetime(2011, 0, 1, 12, 0, 10),
    datetime(2011, 0, 1, 12, 0, 15),
    datetime(2011, 0, 1, 12, 0, 20)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 12, 0, 0), datetime(2011, 0, 1, 12, 0, 50), 4), [
    datetime(2011, 0, 1, 12, 0, 0),
    datetime(2011, 0, 1, 12, 0, 15),
    datetime(2011, 0, 1, 12, 0, 30),
    datetime(2011, 0, 1, 12, 0, 45)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 12, 0, 0), datetime(2011, 0, 1, 12, 1, 50), 4), [
    datetime(2011, 0, 1, 12, 0, 0),
    datetime(2011, 0, 1, 12, 0, 30),
    datetime(2011, 0, 1, 12, 1, 0),
    datetime(2011, 0, 1, 12, 1, 30)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 12, 0, 27), datetime(2011, 0, 1, 12, 4, 12), 4), [
    datetime(2011, 0, 1, 12, 1),
    datetime(2011, 0, 1, 12, 2),
    datetime(2011, 0, 1, 12, 3),
    datetime(2011, 0, 1, 12, 4)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 12, 3, 27), datetime(2011, 0, 1, 12, 21, 12), 4), [
    datetime(2011, 0, 1, 12, 5),
    datetime(2011, 0, 1, 12, 10),
    datetime(2011, 0, 1, 12, 15),
    datetime(2011, 0, 1, 12, 20)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 12, 8, 27), datetime(2011, 0, 1, 13, 4, 12), 4), [
    datetime(2011, 0, 1, 12, 15),
    datetime(2011, 0, 1, 12, 30),
    datetime(2011, 0, 1, 12, 45),
    datetime(2011, 0, 1, 13, 0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 12, 28, 27), datetime(2011, 0, 1, 14, 4, 12), 4), [
    datetime(2011, 0, 1, 12, 30),
    datetime(2011, 0, 1, 13, 0),
    datetime(2011, 0, 1, 13, 30),
    datetime(2011, 0, 1, 14, 0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 12, 28, 27), datetime(2011, 0, 1, 16, 34, 12), 4), [
    datetime(2011, 0, 1, 13, 0),
    datetime(2011, 0, 1, 14, 0),
    datetime(2011, 0, 1, 15, 0),
    datetime(2011, 0, 1, 16, 0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 14, 28, 27), datetime(2011, 0, 2, 1, 34, 12), 4), [
    datetime(2011, 0, 1, 15, 0),
    datetime(2011, 0, 1, 18, 0),
    datetime(2011, 0, 1, 21, 0),
    datetime(2011, 0, 2, 0, 0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 16, 28, 27), datetime(2011, 0, 2, 14, 34, 12), 4), [
    datetime(2011, 0, 1, 18, 0),
    datetime(2011, 0, 2, 0, 0),
    datetime(2011, 0, 2, 6, 0),
    datetime(2011, 0, 2, 12, 0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 16, 28, 27), datetime(2011, 0, 3, 21, 34, 12), 4), [
    datetime(2011, 0, 2, 0, 0),
    datetime(2011, 0, 2, 12, 0),
    datetime(2011, 0, 3, 0, 0),
    datetime(2011, 0, 3, 12, 0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 16, 28, 27), datetime(2011, 0, 5, 21, 34, 12), 4), [
    datetime(2011, 0, 2, 0, 0),
    datetime(2011, 0, 3, 0, 0),
    datetime(2011, 0, 4, 0, 0),
    datetime(2011, 0, 5, 0, 0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 2, 16, 28, 27), datetime(2011, 0, 9, 21, 34, 12), 4), [
    datetime(2011, 0, 3, 0, 0),
    datetime(2011, 0, 5, 0, 0),
    datetime(2011, 0, 7, 0, 0),
    datetime(2011, 0, 9, 0, 0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 1, 16, 28, 27), datetime(2011, 0, 23, 21, 34, 12), 4), [
    datetime(2011, 0, 2, 0, 0),
    datetime(2011, 0, 9, 0, 0),
    datetime(2011, 0, 16, 0, 0),
    datetime(2011, 0, 23, 0, 0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2011, 0, 18), datetime(2011, 4, 2), 4), [
    datetime(2011, 1, 1, 0, 0),
    datetime(2011, 2, 1, 0, 0),
    datetime(2011, 3, 1, 0, 0),
    datetime(2011, 4, 1, 0, 0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2010, 11, 18), datetime(2011, 10, 2), 4), [
    datetime(2011, 0, 1, 0, 0),
    datetime(2011, 3, 1, 0, 0),
    datetime(2011, 6, 1, 0, 0),
    datetime(2011, 9, 1, 0, 0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(2010, 11, 18), datetime(2014, 2, 2), 4), [
    datetime(2011, 0, 1, 0, 0),
    datetime(2012, 0, 1, 0, 0),
    datetime(2013, 0, 1, 0, 0),
    datetime(2014, 0, 1, 0, 0)
  ]);


def test_unknown():
  assert.deepStrictEqual(time_ticks(datetime(0, 11, 18), datetime(2014, 2, 2), 6), [
    datetime( 500, 0, 1, 0, 0),
    datetime(1000, 0, 1, 0, 0),
    datetime(1500, 0, 1, 0, 0),
    datetime(2000, 0, 1, 0, 0)
  ]);


def test_time_ticks_datetime():
  assert time_ticks(datetime(2014, 2, 2), datetime(2014, 2, 2), 6), [datetime(2014, 2, 2)]


def test_time_ticks_datetime():
  assert time_ticks(datetime(2014, 2, 2), datetime(2010, 11, 18), 4), [datetime(2014, 0, 1, 0, 0), datetime(2013, 0, 1, 0, 0), datetime(2012, 0, 1, 0, 0), datetime(2011, 0, 1, 0, 0)]
  assert time_ticks(datetime(2011, 10, 2), datetime(2010, 11, 18), 4), [datetime(2011, 9, 1, 0, 0), datetime(2011, 6, 1, 0, 0), datetime(2011, 3, 1, 0, 0), datetime(2011, 0, 1, 0, 0)]

