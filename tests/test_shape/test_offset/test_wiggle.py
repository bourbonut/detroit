from math import isnan, nan

import detroit as d3


def test_wiggle_1():
    series = [
        [[0, 1], [0, 2], [0, 1]],
        [[0, 3], [0, 4], [0, 2]],
        [[0, 5], [0, 2], [0, 4]],
    ]
    d3.stack_offset_wiggle(series, d3.stack_order_none(series))
    assert list(map(round_series, series)) == list(
        map(
            round_series,
            [
                [[0, 1], [-1, 1], [0.7857143, 1.7857143]],
                [[1, 4], [1, 5], [1.7857143, 3.7857143]],
                [[4, 9], [5, 7], [3.7857143, 7.7857143]],
            ],
        )
    )


def test_wiggle_2():
    series = [
        [[0, 1], [0, 2], [0, 1]],
        [[0, nan], [0, nan], [0, nan]],
        [[0, 3], [0, 4], [0, 2]],
        [[0, 5], [0, 2], [0, 4]],
    ]
    d3.stack_offset_wiggle(series, d3.stack_order_none(series))
    assert isnan(series[1][0][1])
    assert isnan(series[1][1][1])
    assert isnan(series[1][2][1])
    series[1][0][1] = series[1][1][1] = series[1][2][1] = nan
    assert list(map(round_series, series)) == list(
        map(
            round_series,
            [
                [[0, 1], [-1, 1], [0.7857143, 1.7857143]],
                [[1, nan], [1, nan], [1.7857143, nan]],
                [[1, 4], [1, 5], [1.7857143, 3.7857143]],
                [[4, 9], [5, 7], [3.7857143, 7.7857143]],
            ],
        )
    )


def test_wiggle_3():
    series = [
        [[0, 1], [0, 2], [0, 1]],
        [[0, 3], [0, 4], [0, 2]],
        [[0, 5], [0, 2], [0, 4]],
    ]
    d3.stack_offset_wiggle(series, d3.stack_order_reverse(series))
    assert list(map(round_series, series)) == list(
        map(
            round_series,
            [
                [[8, 9], [8, 10], [7.21428571, 8.21428571]],
                [[5, 8], [4, 8], [5.21428571, 7.21428571]],
                [[0, 5], [2, 4], [1.21428571, 5.21428571]],
            ],
        )
    )


def round_series(series):
    return list(
        map(
            lambda point: list(
                map(
                    lambda value: (value if isnan(value) else round(value * 1e6) / 1e6),
                    point,
                ),
            ),
            series,
        )
    )
