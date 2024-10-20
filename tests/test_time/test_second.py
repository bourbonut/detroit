import detroit as d3
from datetime import datetime

def test_time_second_floor():
  assert d3.time_second.floor(datetime(2010, 12, 31, 23, 59, 59, 999)) == datetime(2010, 12, 31, 23, 59, 59)
  assert d3.time_second.floor(datetime(2011,  1,  1,  0,  0,  0,   0)) == datetime(2011,  1,  1,  0,  0,  0)
  assert d3.time_second.floor(datetime(2011,  1,  1,  0,  0,  0,   1)) == datetime(2011,  1,  1,  0,  0,  0)


def test_time_second_round():
  assert d3.time_second.round(datetime(2010, 12, 31, 23, 59, 59, 999999)) == datetime(2011,  1,  1,  0,  0,  0)
  assert d3.time_second.round(datetime(2011,  1,  1,  0,  0,  0, 499999)) == datetime(2011,  1,  1,  0,  0,  0)
  assert d3.time_second.round(datetime(2011,  1,  1,  0,  0,  0, 500000)) == datetime(2011,  1,  1,  0,  0,  1)


def test_time_second_ceil():
  assert d3.time_second.ceil(datetime(2010, 12, 31, 23, 59, 59, 999)) == datetime(2011,  1,  1,  0,  0,  0)
  assert d3.time_second.ceil(datetime(2011,  1,  1,  0,  0,  0,   0)) == datetime(2011,  1,  1,  0,  0,  0)
  assert d3.time_second.ceil(datetime(2011,  1,  1,  0,  0,  0,   1)) == datetime(2011,  1,  1,  0,  0,  1)


def test_time_second_offset():
  assert d3.time_second.offset(datetime(2010, 12, 31, 23, 59, 59, 999), +1) == datetime(2011,  1,  1,  0,  0,  0, 999)
  assert d3.time_second.offset(datetime(2010, 12, 31, 23, 59, 59, 456), -2) == datetime(2010, 12, 31, 23, 59, 57, 456)
  assert d3.time_second.offset(datetime(2010, 12, 31, 23, 59, 59), -1) == datetime(2010, 12, 31, 23, 59, 58)
  assert d3.time_second.offset(datetime(2011,  1,  1,  0,  0,  0), -2) == datetime(2010, 12, 31, 23, 59, 58)
  assert d3.time_second.offset(datetime(2011,  1,  1,  0,  0,  0), -1) == datetime(2010, 12, 31, 23, 59, 59)
  assert d3.time_second.offset(datetime(2010, 12, 31, 23, 59, 58), +1) == datetime(2010, 12, 31, 23, 59, 59)
  assert d3.time_second.offset(datetime(2010, 12, 31, 23, 59, 58), +2) == datetime(2011,  1,  1,  0,  0,  0)
  assert d3.time_second.offset(datetime(2010, 12, 31, 23, 59, 59), +1) == datetime(2011,  1,  1,  0,  0,  0)
  assert d3.time_second.offset(datetime(2010, 12, 31, 23, 59, 59, 999), 0) == datetime(2010, 12, 31, 23, 59, 59, 999)
  assert d3.time_second.offset(datetime(2010, 12, 31, 23, 59, 58,   0), 0) == datetime(2010, 12, 31, 23, 59, 58,   0)




def test_time_second_range():
  assert d3.time_second.range(datetime(2010, 12, 31, 23, 59, 59), datetime(2011, 1, 1, 0, 0, 2)) == [
    datetime(2010, 12, 31, 23, 59, 59),
    datetime(2011, 1, 1, 0, 0, 0),
    datetime(2011, 1, 1, 0, 0, 1)
  ]
  assert d3.time_second.range(datetime(2010, 12, 31, 23, 59, 59), datetime(2011, 1, 1, 0, 0, 2))[0], datetime(2010, 12, 31, 23, 59, 59)
  assert d3.time_second.range(datetime(2010, 12, 31, 23, 59, 59), datetime(2011, 1, 1, 0, 0, 2))[2], datetime(2011, 1, 1, 0, 0, 1)
  assert d3.time_second.range(datetime(2011, 2, 1, 12, 0, 7), datetime(2011, 2, 1, 12, 1, 7), 15) == [
    datetime(2011, 2, 1, 12, 0, 7),
    datetime(2011, 2, 1, 12, 0, 22),
    datetime(2011, 2, 1, 12, 0, 37),
    datetime(2011, 2, 1, 12, 0, 52)
  ]
  assert d3.time_second.range(datetime(2011, 3, 13, 9, 59, 59), datetime(2011, 3, 13, 10, 0, 2)) == [
    datetime(2011, 3, 13, 9, 59, 59),
    datetime(2011, 3, 13, 10, 0, 0),
    datetime(2011, 3, 13, 10, 0, 1)
  ]


  assert d3.time_second.range(datetime(2011, 11, 6, 8, 59, 59), datetime(2011, 11, 6, 9, 0, 2)) == [
    datetime(2011, 11, 6, 8, 59, 59),
    datetime(2011, 11, 6, 9, 0, 0),
    datetime(2011, 11, 6, 9, 0, 1)
  ]

  assert d3.time_second.range(datetime.fromtimestamp(1478422798), datetime.fromtimestamp(1478422802)) == [
    datetime.fromtimestamp(1478422798), # Sun Nov  6 2016  1:59:58 GMT-0700 (PDT)
    datetime.fromtimestamp(1478422799), # Sun Nov  6 2016  1:59:59 GMT-0700 (PDT)
    datetime.fromtimestamp(1478422800), # Sun Nov  6 2016  1:00:00 GMT-0800 (PDT)
    datetime.fromtimestamp(1478422801)  # Sun Nov  6 2016  1:00:01 GMT-0800 (PDT)
  ]


def test_time_second_every():
  assert d3.time_second.every(15).range(datetime(2008, 12, 30, 12, 36, 47), datetime(2008, 12, 30, 12, 37, 57)) == [datetime(2008, 12, 30, 12, 37, 15), datetime(2008, 12, 30, 12, 37, 30), datetime(2008, 12, 30, 12, 37, 45)]
  assert d3.time_second.every(30).range(datetime(2008, 12, 30, 12, 36, 47), datetime(2008, 12, 30, 12, 37, 57)) == [datetime(2008, 12, 30, 12, 37, 30)]
