from datetime import datetime

import detroit as d3


def test_time_millisecond_every():
    assert d3.time_millisecond.every(50).range(
        datetime(2008, 12, 30, 12, 36, 0, 947000),
        datetime(2008, 12, 30, 12, 36, 1, 157000),
    ) == [
        datetime(2008, 12, 30, 12, 36, 0, 950000),
        datetime(2008, 12, 30, 12, 36, 1, 0),
        datetime(2008, 12, 30, 12, 36, 1, 50000),
        datetime(2008, 12, 30, 12, 36, 1, 100000),
        datetime(2008, 12, 30, 12, 36, 1, 150000),
    ]
    assert d3.time_millisecond.every(100).range(
        datetime(2008, 12, 30, 12, 36, 0, 947000),
        datetime(2008, 12, 30, 12, 36, 1, 157000),
    ) == [
        datetime(2008, 12, 30, 12, 36, 1, 0),
        datetime(2008, 12, 30, 12, 36, 1, 100000),
    ]
    assert d3.time_millisecond.every(50).range(
        datetime(2008, 12, 30, 12, 36, 0, 947000),
        datetime(2008, 12, 30, 12, 36, 1, 157000),
    ) == [
        datetime(2008, 12, 30, 12, 36, 0, 950000),
        datetime(2008, 12, 30, 12, 36, 1, 0),
        datetime(2008, 12, 30, 12, 36, 1, 50000),
        datetime(2008, 12, 30, 12, 36, 1, 100000),
        datetime(2008, 12, 30, 12, 36, 1, 150000),
    ]
    assert d3.time_millisecond.every(100).range(
        datetime(2008, 12, 30, 12, 36, 0, 947000),
        datetime(2008, 12, 30, 12, 36, 1, 157000),
    ) == [
        datetime(2008, 12, 30, 12, 36, 1, 0),
        datetime(2008, 12, 30, 12, 36, 1, 100000),
    ]
