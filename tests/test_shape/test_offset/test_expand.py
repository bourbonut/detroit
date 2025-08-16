from math import isnan, nan

import detroit as d3


def test_expand_1():
    series = [
        [[0, 1], [0, 2], [0, 1]],
        [[0, 3], [0, 4], [0, 2]],
        [[0, 5], [0, 2], [0, 4]],
    ]
    d3.stack_offset_expand(series, d3.stack_order_none(series))
    assert series == [
        [[0 / 9, 1 / 9], [0 / 8, 2 / 8], [0 / 7, 1 / 7]],
        [[1 / 9, 4 / 9], [2 / 8, 6 / 8], [1 / 7, 3 / 7]],
        [[4 / 9, 9 / 9], [6 / 8, 8 / 8], [3 / 7, 7 / 7]],
    ]


def test_expand_2():
    series = [
        [[0, 1], [0, 2], [0, 1]],
        [[0, 3], [0, nan], [0, 2]],
        [[0, 5], [0, 2], [0, 4]],
    ]
    d3.stack_offset_expand(series, d3.stack_order_none(series))
    assert isnan(series[1][1][1])
    series[1][1][1] = nan
    assert series == [
        [[0 / 9, 1 / 9], [0 / 4, 2 / 4], [0 / 7, 1 / 7]],
        [[1 / 9, 4 / 9], [2 / 4, nan], [1 / 7, 3 / 7]],
        [[4 / 9, 9 / 9], [2 / 4, 4 / 4], [3 / 7, 7 / 7]],
    ]


def test_expand_3():
    series = [
        [[0, 1], [0, 2], [0, 1]],
        [[0, 3], [0, 4], [0, 2]],
        [[0, 5], [0, 2], [0, 4]],
    ]
    d3.stack_offset_expand(series, d3.stack_order_reverse(series))
    assert series == [
        [[8 / 9, 9 / 9], [6 / 8, 8 / 8], [6 / 7, 7 / 7]],
        [[5 / 9, 8 / 9], [2 / 8, 6 / 8], [4 / 7, 6 / 7]],
        [[0 / 9, 5 / 9], [0 / 8, 2 / 8], [0 / 7, 4 / 7]],
    ]
