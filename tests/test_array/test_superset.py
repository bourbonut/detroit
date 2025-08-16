from datetime import datetime

import detroit as d3


def test_superset_1():
    assert d3.superset([1, 2], [2]) is True
    assert d3.superset([2, 3], [3, 4]) is False
    assert d3.superset([1], []) is True


def test_superset_2():
    assert d3.superset([1, 3, 5, 7], [1, 3, 5]) is True


def test_superset_3():
    assert d3.superset([1, 3, 5], [1, 3, 2]) is False


def test_superset_4():
    assert (
        d3.superset(
            [
                datetime.strptime("2021-01-01", "%Y-%m-%d"),
                datetime.strptime("2021-01-02", "%Y-%m-%d"),
            ],
            [datetime.strptime("2021-01-02", "%Y-%m-%d")],
        )
        is True
    )
    assert (
        d3.superset(
            [
                datetime.strptime("2021-01-02", "%Y-%m-%d"),
                datetime.strptime("2021-01-03", "%Y-%m-%d"),
            ],
            [
                datetime.strptime("2021-01-03", "%Y-%m-%d"),
                datetime.strptime("2021-01-04", "%Y-%m-%d"),
            ],
        )
        is False
    )
    assert d3.superset([datetime.strptime("2021-01-01", "%Y-%m-%d")], []) is True
