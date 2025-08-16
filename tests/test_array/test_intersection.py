from datetime import datetime

import detroit as d3


def test_intersection_1():
    assert d3.intersection([1, 2, 3, 2, 1]) == set([1, 2, 3])


def test_intersection_2():
    assert d3.intersection([1, 2], [2, 3, 1]) == set([1, 2])
    assert d3.intersection([2, 1, 3], [4, 3, 1]) == set([1, 3])


def test_intersection_3():
    assert d3.intersection([1, 2], [2, 1], [2, 3]) == set([2])


def test_intersection_4():
    assert d3.intersection(set([1, 2, 3])) == set([1, 2, 3])


def test_intersection_5():
    assert d3.intersection(
        [
            datetime.strptime("2021-01-01", "%Y-%m-%d"),
            datetime.strptime("2021-01-03", "%Y-%m-%d"),
        ],
        [
            datetime.strptime("2021-01-01", "%Y-%m-%d"),
            datetime.strptime("2021-01-02", "%Y-%m-%d"),
        ],
    ) == set([datetime.strptime("2021-01-01", "%Y-%m-%d")])
