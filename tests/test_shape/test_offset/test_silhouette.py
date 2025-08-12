from math import isnan, nan

import detroit as d3


def test_silhouette_1():
  series = [
    [[0, 1], [0, 2], [0, 1]],
    [[0, 3], [0, 4], [0, 2]],
    [[0, 5], [0, 2], [0, 4]]
  ]
  d3.stack_offset_silhouette(series, d3.stack_order_none(series))
  assert series == [
    [[0 - 9 / 2, 1 - 9 / 2], [0 - 8 / 2, 2 - 8 / 2], [0 - 7 / 2, 1 - 7 / 2]],
    [[1 - 9 / 2, 4 - 9 / 2], [2 - 8 / 2, 6 - 8 / 2], [1 - 7 / 2, 3 - 7 / 2]],
    [[4 - 9 / 2, 9 - 9 / 2], [6 - 8 / 2, 8 - 8 / 2], [3 - 7 / 2, 7 - 7 / 2]]
  ]

def test_silhouette_2():
  series = [
    [[0, 1], [0,   2], [0, 1]],
    [[0, 3], [0, nan], [0, 2]],
    [[0, 5], [0,   2], [0, 4]]
  ]
  d3.stack_offset_silhouette(series, d3.stack_order_none(series))
  assert isnan(series[1][1][1])
  series[1][1][1] = nan
  assert series == [
    [[0 - 9 / 2, 1 - 9 / 2], [0 - 4 / 2, 2 - 4 / 2], [0 - 7 / 2, 1 - 7 / 2]],
    [[1 - 9 / 2, 4 - 9 / 2], [2 - 4 / 2,       nan], [1 - 7 / 2, 3 - 7 / 2]],
    [[4 - 9 / 2, 9 - 9 / 2], [2 - 4 / 2, 4 - 4 / 2], [3 - 7 / 2, 7 - 7 / 2]]
  ]

def test_silhouette_3():
  series = [
    [[0, 1], [0, 2], [0, 1]],
    [[0, 3], [0, 4], [0, 2]],
    [[0, 5], [0, 2], [0, 4]]
  ]
  d3.stack_offset_silhouette(series, d3.stack_order_reverse(series))
  assert series == [
    [[8 - 9 / 2, 9 - 9 / 2], [6 - 8 / 2, 8 - 8 / 2], [6 - 7 / 2, 7 - 7 / 2]],
    [[5 - 9 / 2, 8 - 9 / 2], [2 - 8 / 2, 6 - 8 / 2], [4 - 7 / 2, 6 - 7 / 2]],
    [[0 - 9 / 2, 5 - 9 / 2], [0 - 8 / 2, 2 - 8 / 2], [0 - 7 / 2, 4 - 7 / 2]]
  ]
