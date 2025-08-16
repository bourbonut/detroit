from math import nan

import detroit as d3


def test_descending_1():
    assert d3.stack_order_descending(
        [[[0, 1], [0, 2], [0, 3]], [[0, 2], [0, 3], [0, 4]], [[0, 0], [0, 1], [0, 2]]]
    ) == [1, 0, 2]


def test_descending_2():
    assert d3.stack_order_descending(
        [
            [[0, 1], [0, 2], [0, 3], [0, nan]],
            [[0, 2], [0, 3], [0, 4], [0, nan]],
            [[0, 0], [0, 1], [0, 2], [0, nan]],
        ]
    ) == [1, 0, 2]
