import detroit as d3
from math import isnan, nan

def test_diverging_1():
  series = [
    [[1, 2], [2, 4], [3, 4]],
    [[0, 3], [0, 4], [0, 2]],
    [[0, 5], [0, 2], [0, 4]]
  ]
  d3.stack_offset_diverging(series, d3.stack_order_none(series))
  assert series == [
    [[0, 1], [0, 2], [0, 1]],
    [[1, 4], [2, 6], [1, 3]],
    [[4, 9], [6, 8], [3, 7]]
  ]

def test_diverging_2():
  series = [
    [[1, 2], [2, 4], [3, 4]]
  ]
  d3.stack_offset_diverging(series, d3.stack_order_none(series))
  assert series == [
    [[0, 1], [0, 2], [0, 1]]
  ]

def test_diverging_3():
  series = [
    [[0, 1], [0,   2], [0, 1]],
    [[0, 3], [0, nan], [0, 2]],
    [[0, 5], [0,   2], [0, 4]]
  ]
  d3.stack_offset_diverging(series, d3.stack_order_none(series))
  assert isnan(series[1][1][1])
  series[1][1][1] = nan
  assert series == [
    [[0, 1], [0,   2], [0, 1]],
    [[1, 4], [0, nan], [1, 3]],
    [[4, 9], [2,   4], [3, 7]]
  ]

def test_diverging_4():
  series = [
    [[0, 1], [0, 2], [0, 1]],
    [[0, 3], [0, 4], [0, 2]],
    [[0, 5], [0, 2], [0, 4]]
  ]
  d3.stack_offset_diverging(series, d3.stack_order_reverse(series))
  assert series == [
    [[8, 9], [6, 8], [6, 7]],
    [[5, 8], [2, 6], [4, 6]],
    [[0, 5], [0, 2], [0, 4]]
  ]

def test_diverging_5():
  series = [
    [[0,  1], [0, -2], [0, -1]],
    [[0, -3], [0, -4], [0, -2]],
    [[0, -5], [0, -2], [0,  4]]
  ]
  d3.stack_offset_diverging(series, d3.stack_order_none(series))
  assert series == [
    [[ 0,  1], [-2,  0], [-1,  0]],
    [[-3,  0], [-6, -2], [-3, -1]],
    [[-8, -3], [-8, -6], [ 0,  4]]
  ]

def test_diverging_6():
  series = [
    [[0, 1], [0, 2], [0, -1]],
    [[0, 3], [0, 0], [0, 0]],
    [[0, 5], [0, 2], [0, 4]]
  ]
  d3.stack_offset_diverging(series, d3.stack_order_none(series))
  assert series == [
    [[0, 1], [0, 2], [-1, 0]],
    [[1, 4], [0, 0], [0, 0]],
    [[4, 9], [2, 4], [0, 4]]
  ]
