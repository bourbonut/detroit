import detroit as d3
from datetime import datetime

def test_difference_1():
  assert d3.difference([1, 2, 3], [2, 1]) == set([3])
  assert d3.difference([1, 2], [2, 3, 1]) == set([])
  assert d3.difference([2, 1, 3], [4, 3, 1]) == set([2])

def test_difference_2():
  assert d3.difference(set([1, 2, 3]), set([1])) == set([2, 3])

def test_difference_3():
  assert d3.difference([datetime.strptime("2021-01-01", "%Y-%m-%d"), datetime.strptime("2021-01-02", "%Y-%m-%d"), datetime.strptime("2021-01-03", "%Y-%m-%d")], [datetime.strptime("2021-01-02", "%Y-%m-%d"), datetime.strptime("2021-01-01", "%Y-%m-%d")]) == set([datetime.strptime("2021-01-03", "%Y-%m-%d")])
  assert d3.difference([datetime.strptime("2021-01-01", "%Y-%m-%d"), datetime.strptime("2021-01-02", "%Y-%m-%d")], [datetime.strptime("2021-01-02", "%Y-%m-%d"), datetime.strptime("2021-01-03", "%Y-%m-%d"), datetime.strptime("2021-01-01", "%Y-%m-%d")]) == set([])
  assert d3.difference([datetime.strptime("2021-01-02", "%Y-%m-%d"), datetime.strptime("2021-01-01", "%Y-%m-%d"), datetime.strptime("2021-01-03", "%Y-%m-%d")], [datetime.strptime("2021-01-04", "%Y-%m-%d"), datetime.strptime("2021-01-03", "%Y-%m-%d"), datetime.strptime("2021-01-01", "%Y-%m-%d")]) == set([datetime.strptime("2021-01-02", "%Y-%m-%d")])
