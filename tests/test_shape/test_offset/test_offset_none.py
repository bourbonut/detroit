from math import isnan, nan

import detroit as d3


def test_none_1():
    series = [
        [[1, 2], [2, 4], [3, 4]],
        [[0, 3], [0, 4], [0, 2]],
        [[0, 5], [0, 2], [0, 4]],
    ]
    d3.stack_offset_none(series, d3.stack_order_none(series))
    assert series == [
        [[1, 2], [2, 4], [3, 4]],
        [[2, 5], [4, 8], [4, 6]],
        [[5, 10], [8, 10], [6, 10]],
    ]


def test_none_2():
    series = [
        [[0, 1], [0, 2], [0, 1]],
        [[0, 3], [0, nan], [0, 2]],
        [[0, 5], [0, 2], [0, 4]],
    ]
    d3.stack_offset_none(series, d3.stack_order_none(series))
    assert isnan(series[1][1][1])
    series[1][1][1] = nan
    assert series == [
        [[0, 1], [0, 2], [0, 1]],
        [[1, 4], [2, nan], [1, 3]],
        [[4, 9], [2, 4], [3, 7]],
    ]


def test_none_3():
    series = [
        [[0, 1], [0, 2], [0, 1]],
        [[0, 3], [0, 4], [0, 2]],
        [[0, 5], [0, 2], [0, 4]],
    ]
    d3.stack_offset_none(series, d3.stack_order_reverse(series))
    assert series == [
        [[8, 9], [6, 8], [6, 7]],
        [[5, 8], [2, 6], [4, 6]],
        [[0, 5], [0, 2], [0, 4]],
    ]
