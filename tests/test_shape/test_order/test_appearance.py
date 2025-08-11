import detroit as d3
from math import nan

def test_appearance_1():
  assert d3.stack_order_appearance([
    [[0, 0], [0, 0], [0, 1]],
    [[0, 3], [0, 2], [0, 0]],
    [[0, 0], [0, 4], [0, 0]],
  ]) == [1, 2, 0]

def test_appearance_2():
  assert d3.stack_order_appearance([
    [[0, nan], [0, nan], [0, 1]],
    [[0, 3], [0, 2], [0, nan]],
    [[0, nan], [0, 4], [0, nan]],
  ]) == [1, 2, 0]
