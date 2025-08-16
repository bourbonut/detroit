from datetime import datetime

import detroit as d3


def test_subset_1():
    assert d3.subset([2], [1, 2]) is True
    assert d3.subset([3, 4], [2, 3]) is False
    assert d3.subset([], [1]) is True


def test_subset_2():
    assert (
        d3.subset(
            [datetime.strptime("2021-01-02", "%Y-%m-%d")],
            [
                datetime.strptime("2021-01-01", "%Y-%m-%d"),
                datetime.strptime("2021-01-02", "%Y-%m-%d"),
            ],
        )
        is True
    )
    assert (
        d3.subset(
            [
                datetime.strptime("2021-01-03", "%Y-%m-%d"),
                datetime.strptime("2021-01-04", "%Y-%m-%d"),
            ],
            [
                datetime.strptime("2021-01-02", "%Y-%m-%d"),
                datetime.strptime("2021-01-03", "%Y-%m-%d"),
            ],
        )
        is False
    )
    assert d3.subset([], [datetime.strptime("2021-01-01", "%Y-%m-%d")]) is True
