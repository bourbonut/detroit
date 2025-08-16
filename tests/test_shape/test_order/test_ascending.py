from math import nan

import detroit as d3


def test_ascending_1():
    assert d3.stack_order_ascending(
        [[[0, 1], [0, 2], [0, 3]], [[0, 2], [0, 3], [0, 4]], [[0, 0], [0, 1], [0, 2]]]
    ) == [2, 0, 1]


def test_ascending_2():
    assert d3.stack_order_ascending(
        [
            [[0, 1], [0, 2], [0, nan], [0, 3]],
            [[0, 2], [0, 3], [0, nan], [0, 4]],
            [[0, 0], [0, 1], [0, nan], [0, 2]],
        ]
    ) == [2, 0, 1]
