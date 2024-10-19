import detroit as d3
from datetime import datetime

def test_time_millisecond_every():
  assert time_millisecond.every(50).range(datetime(2008, 11, 30, 12, 36, 0, 947), datetime(2008, 11, 30, 12, 36, 1, 157)) == [datetime(2008, 11, 30, 12, 36, 0, 950), datetime(2008, 11, 30, 12, 36, 1, 0), datetime(2008, 11, 30, 12, 36, 1, 50), datetime(2008, 11, 30, 12, 36, 1, 100), datetime(2008, 11, 30, 12, 36, 1, 150)]
  assert time_millisecond.every(100).range(datetime(2008, 11, 30, 12, 36, 0, 947), datetime(2008, 11, 30, 12, 36, 1, 157)) == [datetime(2008, 11, 30, 12, 36, 1, 0), datetime(2008, 11, 30, 12, 36, 1, 100)]
  assert time_millisecond.every(50).range(datetime(2008, 11, 30, 12, 36, 0, 947), datetime(2008, 11, 30, 12, 36, 1, 157)) == [datetime(2008, 11, 30, 12, 36, 0, 950), datetime(2008, 11, 30, 12, 36, 1, 0), datetime(2008, 11, 30, 12, 36, 1, 50), datetime(2008, 11, 30, 12, 36, 1, 100), datetime(2008, 11, 30, 12, 36, 1, 150)]
  assert time_millisecond.every(100).range(datetime(2008, 11, 30, 12, 36, 0, 947), datetime(2008, 11, 30, 12, 36, 1, 157)) == [datetime(2008, 11, 30, 12, 36, 1, 0), datetime(2008, 11, 30, 12, 36, 1, 100)]

