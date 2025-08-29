from functools import reduce
from math import inf, nan
from operator import iadd

import pytest

import detroit as d3


def values(items, times):
    return reduce(iadd, ([item] * time for item, time in zip(items, times)), [])


def test_contours_1():
    c = d3.contours().set_size([10, 10]).set_thresholds([0.5])
    assert c([0] * 100) == [{"type": "MultiPolygon", "value": 0.5, "coordinates": []}]


def test_contours_2():
    c = d3.contours().set_size([10, 10]).set_thresholds([0.5])
    items = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    times = [33, 3, 7, 3, 7, 3, 7, 3, 7, 3, 24]
    assert c(values(items, times)) == [
        {
            "type": "MultiPolygon",
            "value": 0.5,
            "coordinates": [
                [
                    [
                        [6, 7.5],
                        [6, 6.5],
                        [6, 5.5],
                        [6, 4.5],
                        [6, 3.5],
                        [5.5, 3],
                        [4.5, 3],
                        [3.5, 3],
                        [3, 3.5],
                        [3, 4.5],
                        [3, 5.5],
                        [3, 6.5],
                        [3, 7.5],
                        [3.5, 8],
                        [4.5, 8],
                        [5.5, 8],
                        [6, 7.5],
                    ]
                ]
            ],
        }
    ]


def test_contours_3():
    c = d3.contours().set_size([10, 10])
    items = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    times = [33, 3, 7, 3, 7, 3, 7, 3, 7, 3, 24]
    assert c.contour(values(items, times), 0.5) == {
        "type": "MultiPolygon",
        "value": 0.5,
        "coordinates": [
            [
                [
                    [6, 7.5],
                    [6, 6.5],
                    [6, 5.5],
                    [6, 4.5],
                    [6, 3.5],
                    [5.5, 3],
                    [4.5, 3],
                    [3.5, 3],
                    [3, 3.5],
                    [3, 4.5],
                    [3, 5.5],
                    [3, 6.5],
                    [3, 7.5],
                    [3.5, 8],
                    [4.5, 8],
                    [5.5, 8],
                    [6, 7.5],
                ]
            ]
        ],
    }


def test_contours_4():
    c = d3.contours().set_smooth(False).set_size([10, 10]).set_thresholds([0.5])
    items = [0, 2, 1, 2, 0, 2, 0, 1, 2, 1, 0, 2, 0, 2, 1, 2, 0]
    times = [33, 1, 1, 1, 7, 3, 7, 1, 1, 1, 7, 3, 7, 1, 1, 1, 24]
    assert c(values(items, times)) == [
        {
            "type": "MultiPolygon",
            "value": 0.5,
            "coordinates": [
                [
                    [
                        [6, 7.5],
                        [6, 6.5],
                        [6, 5.5],
                        [6, 4.5],
                        [6, 3.5],
                        [5.5, 3],
                        [4.5, 3],
                        [3.5, 3],
                        [3, 3.5],
                        [3, 4.5],
                        [3, 5.5],
                        [3, 6.5],
                        [3, 7.5],
                        [3.5, 8],
                        [4.5, 8],
                        [5.5, 8],
                        [6, 7.5],
                    ]
                ]
            ],
        }
    ]


def test_contours_5():
    c = d3.contours().set_size([10, 10]).set_thresholds([0.5])
    items = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    times = [33, 3, 7, 1, 1, 1, 7, 1, 1, 1, 7, 1, 1, 1, 7, 3, 24]
    assert c(values(items, times)) == [
        {
            "type": "MultiPolygon",
            "value": 0.5,
            "coordinates": [
                [
                    [
                        [6, 7.5],
                        [6, 6.5],
                        [6, 5.5],
                        [6, 4.5],
                        [6, 3.5],
                        [5.5, 3],
                        [4.5, 3],
                        [3.5, 3],
                        [3, 3.5],
                        [3, 4.5],
                        [3, 5.5],
                        [3, 6.5],
                        [3, 7.5],
                        [3.5, 8],
                        [4.5, 8],
                        [5.5, 8],
                        [6, 7.5],
                    ],
                    [
                        [4.5, 7],
                        [4, 6.5],
                        [4, 5.5],
                        [4, 4.5],
                        [4.5, 4],
                        [5, 4.5],
                        [5, 5.5],
                        [5, 6.5],
                        [4.5, 7],
                    ],
                ]
            ],
        }
    ]


def test_contours_6():
    c = d3.contours().set_size([10, 10]).set_thresholds([0.5])
    items = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    times = [33, 2, 1, 1, 6, 2, 1, 1, 6, 2, 1, 1, 6, 2, 1, 1, 6, 2, 1, 1, 23]
    assert c(values(items, times)) == [
        {
            "type": "MultiPolygon",
            "value": 0.5,
            "coordinates": [
                [
                    [
                        [5, 7.5],
                        [5, 6.5],
                        [5, 5.5],
                        [5, 4.5],
                        [5, 3.5],
                        [4.5, 3],
                        [3.5, 3],
                        [3, 3.5],
                        [3, 4.5],
                        [3, 5.5],
                        [3, 6.5],
                        [3, 7.5],
                        [3.5, 8],
                        [4.5, 8],
                        [5, 7.5],
                    ]
                ],
                [
                    [
                        [7, 7.5],
                        [7, 6.5],
                        [7, 5.5],
                        [7, 4.5],
                        [7, 3.5],
                        [6.5, 3],
                        [6, 3.5],
                        [6, 4.5],
                        [6, 5.5],
                        [6, 6.5],
                        [6, 7.5],
                        [6.5, 8],
                        [7, 7.5],
                    ]
                ],
            ],
        }
    ]


def test_contours_7():
    c = d3.contours().set_size([10, 10]).set_thresholds([0.5])
    items = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    times = [31, 3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 42]
    assert c(values(items, times)) == [
        {
            "type": "MultiPolygon",
            "value": 0.5,
            "coordinates": [
                [
                    [
                        [4, 5.5],
                        [4, 4.5],
                        [4, 3.5],
                        [3.5, 3],
                        [2.5, 3],
                        [1.5, 3],
                        [1, 3.5],
                        [1, 4.5],
                        [1, 5.5],
                        [1.5, 6],
                        [2.5, 6],
                        [3.5, 6],
                        [4, 5.5],
                    ],
                    [[2.5, 5], [2, 4.5], [2.5, 4], [3, 4.5], [2.5, 5]],
                ],
                [
                    [
                        [8, 5.5],
                        [8, 4.5],
                        [8, 3.5],
                        [7.5, 3],
                        [6.5, 3],
                        [5.5, 3],
                        [5, 3.5],
                        [5, 4.5],
                        [5, 5.5],
                        [5.5, 6],
                        [6.5, 6],
                        [7.5, 6],
                        [8, 5.5],
                    ],
                    [[6.5, 5], [6, 4.5], [6.5, 4], [7, 4.5], [6.5, 5]],
                ],
            ],
        }
    ]


def test_contours_8():
    assert d3.contours().set_size([1, 2]).get_size() == [1, 2]
    assert d3.contours().set_size([0, 0]).get_size() == [0, 0]
    assert d3.contours().set_size([1.5, 2.5]).get_size() == [1, 2]
    with pytest.raises(ValueError):
        d3.contours().set_size([0, -1])


def test_contours_9():
    c = d3.contours().set_size([10, 10]).set_thresholds(20)
    items = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    times = [31, 3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 42]
    assert list(map(lambda d: d["value"], c(values(items, times)))) == [
        0,
        0.05,
        0.1,
        0.15,
        0.2,
        0.25,
        0.3,
        0.35,
        0.4,
        0.45,
        0.5,
        0.55,
        0.6,
        0.65,
        0.7,
        0.75,
        0.8,
        0.85,
        0.9,
        0.95,
    ]


def test_contours_10():
    c = d3.contours().set_size([10, 10]).set_thresholds(20)
    items = [0, -inf, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, inf, 0]
    times = [11, 1, 19, 3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 30, 1, 11]
    assert list(map(lambda d: d["value"], c(values(items, times)))) == [
        0,
        0.05,
        0.1,
        0.15,
        0.2,
        0.25,
        0.3,
        0.35,
        0.4,
        0.45,
        0.5,
        0.55,
        0.6,
        0.65,
        0.7,
        0.75,
        0.8,
        0.85,
        0.9,
        0.95,
    ]


def test_contours_11():
    c = d3.contours().set_size([10, 10])
    items = [1, -inf, 1, nan, 1, 2, 1, nan, 1, 2, -inf, 2, 1, 2, 1]
    times = [11, 1, 31, 1, 22, 3, 3, 1, 3, 1, 1, 1, 7, 3, 11]
    assert c.contour(values(items, times), 0) == {
        "type": "MultiPolygon",
        "value": 0,
        "coordinates": [
            [
                [
                    [10, 9.5],
                    [10, 8.5],
                    [10, 7.5],
                    [10, 6.5],
                    [10, 5.5],
                    [10, 4.5],
                    [10, 3.5],
                    [10, 2.5],
                    [10, 1.5],
                    [10, 0.5],
                    [9.5, 0],
                    [8.5, 0],
                    [7.5, 0],
                    [6.5, 0],
                    [5.5, 0],
                    [4.5, 0],
                    [3.5, 0],
                    [2.5, 0],
                    [1.5, 0],
                    [0.5, 0],
                    [0, 0.5],
                    [0, 1.5],
                    [0, 2.5],
                    [0, 3.5],
                    [0, 4.5],
                    [0, 5.5],
                    [0, 6.5],
                    [0, 7.5],
                    [0, 8.5],
                    [0, 9.5],
                    [0.5, 10],
                    [1.5, 10],
                    [2.5, 10],
                    [3.5, 10],
                    [4.5, 10],
                    [5.5, 10],
                    [6.5, 10],
                    [7.5, 10],
                    [8.5, 10],
                    [9.5, 10],
                    [10, 9.5],
                ],
                [[1.5, 2.5], [0.5, 1.5], [1.5, 0.5], [2.5, 1.5], [1.5, 2.5]],
                [[3.5, 5.5], [2.5, 4.5], [3.5, 3.5], [4.5, 4.5], [3.5, 5.5]],
                [[2.5, 8.5], [1.5, 7.5], [2.5, 6.5], [3.5, 7.5], [2.5, 8.5]],
                [[7.5, 8.5], [6.5, 7.5], [7.5, 6.5], [8.5, 7.5], [7.5, 8.5]],
            ]
        ],
    }


def test_contours_12():
    c = d3.contours().set_size([10, 10]).set_thresholds([0.5])
    items = [0, 1, 0, 1, inf, 1, 0, 1, 0, 1, inf, 1, 0, 1, 0]
    times = [33, 3, 7, 1, 1, 1, 7, 3, 7, 1, 1, 1, 7, 3, 24]
    assert c(values(items, times)) == [
        {
            "type": "MultiPolygon",
            "value": 0.5,
            "coordinates": [
                [
                    [
                        [6, 7.5],
                        [6, 6.5],
                        [6, 5.5],
                        [6, 4.5],
                        [6, 3.5],
                        [5.5, 3],
                        [4.5, 3],
                        [3.5, 3],
                        [3, 3.5],
                        [3, 4.5],
                        [3, 5.5],
                        [3, 6.5],
                        [3, 7.5],
                        [3.5, 8],
                        [4.5, 8],
                        [5.5, 8],
                        [6, 7.5],
                    ]
                ]
            ],
        }
    ]


def test_contours_13():
    for value in [nan, "a string"]:
        with pytest.raises(ValueError):
            d3.contours().set_size([3, 3]).contour([1, 2, 3, 4, 5, 6, 7, 8, 9], value)


def test_contours_14():
    assert list(
        map(
            lambda c: c["value"],
            d3.contours()
            .set_size([2, 1])
            .set_thresholds(14)([-149.76192742819748, 321.19300631539585]),
        )
    ) == [-150, -100, -50, 0, 50, 100, 150, 200, 250, 300]
    assert list(
        map(
            lambda c: c["value"],
            d3.contours()
            .set_size([2, 1])
            .set_thresholds(5)([-149.76192742819748, 321.19300631539585]),
        )
    ) == [-200, -100, 0, 100, 200, 300]
    assert list(
        map(
            lambda c: c["value"],
            d3.contours()
            .set_size([2, 1])
            .set_thresholds(14)([149.76192742819748, -321.19300631539585]),
        )
    ) == [-350, -300, -250, -200, -150, -100, -50, 0, 50, 100]
    assert list(
        map(
            lambda c: c["value"],
            d3.contours()
            .set_size([2, 1])
            .set_thresholds(5)([149.76192742819748, -321.19300631539585]),
        )
    ) == [-400, -300, -200, -100, 0, 100]
    assert list(
        map(
            lambda c: c["value"],
            d3.contours().set_size([2, 1]).set_thresholds(12)([-29, 50]),
        )
    ) == [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
    assert list(
        map(
            lambda c: c["value"],
            d3.contours().set_size([2, 1]).set_thresholds(10)([-41, 245]),
        )
    ) == [-50, 0, 50, 100, 150, 200]
    assert list(
        map(
            lambda c: c["value"],
            d3.contours().set_size([2, 1]).set_thresholds(9)([-22, 242]),
        )
    ) == [-50, 0, 50, 100, 150, 200]
