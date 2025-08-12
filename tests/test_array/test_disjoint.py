import detroit as d3
from datetime import datetime

def test_disjoint_1():
  assert d3.disjoint([1], [2]) is True
  assert d3.disjoint([2, 3], [3, 4]) is False
  assert d3.disjoint([1], []) is True

def test_disjoint_2():
  assert d3.disjoint([1, 3, 5, 7], [0, 2, 4, 5]) is False

def test_disjoint_3():
  assert d3.disjoint([2], [1, 3, 2]) is False

def test_disjoint_4():
  assert d3.disjoint([datetime.strptime("2021-01-01", "%Y-%m-%d")], [datetime.strptime("2021-01-02", "%Y-%m-%d")]) is True
  assert d3.disjoint([datetime.strptime("2021-01-02", "%Y-%m-%d"), datetime.strptime("2021-01-03", "%Y-%m-%d")], [datetime.strptime("2021-01-03", "%Y-%m-%d"), datetime.strptime("2021-01-04", "%Y-%m-%d")]) is False
  assert d3.disjoint([datetime.strptime("2021-01-01", "%Y-%m-%d")], []) is True
