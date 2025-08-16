from datetime import datetime

import detroit as d3


def test_union_1():
    assert d3.union([1, 2, 3, 2, 1]) == set([1, 2, 3])


def test_union_2():
    assert d3.union([1, 2], [2, 3, 1]) == set([1, 2, 3])


def test_union_3():
    assert d3.union([1], [2], [2, 3], [1]) == set([1, 2, 3])


def test_union_4():
    assert d3.union(set([1, 2, 3])) == set([1, 2, 3])
    assert d3.union([1, 2, 3]) == set([1, 2, 3])


def test_union_5():
    assert d3.union(
        [
            datetime.strptime("2021-01-01", "%Y-%m-%d"),
            datetime.strptime("2021-01-01", "%Y-%m-%d"),
            datetime.strptime("2021-01-02", "%Y-%m-%d"),
        ]
    ) == set(
        [
            datetime.strptime("2021-01-01", "%Y-%m-%d"),
            datetime.strptime("2021-01-02", "%Y-%m-%d"),
        ]
    )
    assert d3.union(
        [
            datetime.strptime("2021-01-01", "%Y-%m-%d"),
            datetime.strptime("2021-01-03", "%Y-%m-%d"),
        ],
        [
            datetime.strptime("2021-01-01", "%Y-%m-%d"),
            datetime.strptime("2021-01-02", "%Y-%m-%d"),
        ],
    ) == set(
        [
            datetime.strptime("2021-01-01", "%Y-%m-%d"),
            datetime.strptime("2021-01-02", "%Y-%m-%d"),
            datetime.strptime("2021-01-03", "%Y-%m-%d"),
        ]
    )
