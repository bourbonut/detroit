from datetime import datetime
from itertools import starmap

import pytest

import detroit as d3


def entries(map_obj, depth):
    if depth > 0:
        return list(starmap(lambda k, v: (k, entries(v, depth - 1)), map_obj.items()))
    else:
        return map_obj


@pytest.fixture
def data():
    return [
        {"name": "jim", "amount": "34.0", "date": "11/12/2015"},
        {"name": "carl", "amount": "120.11", "date": "11/12/2015"},
        {"name": "stacy", "amount": "12.01", "date": "01/04/2016"},
        {"name": "stacy", "amount": "34.05", "date": "01/04/2016"},
    ]


def test_group_1(data):
    assert entries(d3.group(data, lambda d: d["name"]), 1) == [
        ("jim", [{"name": "jim", "amount": "34.0", "date": "11/12/2015"}]),
        ("carl", [{"name": "carl", "amount": "120.11", "date": "11/12/2015"}]),
        (
            "stacy",
            [
                {"name": "stacy", "amount": "12.01", "date": "01/04/2016"},
                {"name": "stacy", "amount": "34.05", "date": "01/04/2016"},
            ],
        ),
    ]


def test_group_2(data):
    assert entries(d3.group(data, lambda d: d["name"], lambda d: d["amount"]), 2) == [
        ("jim", [("34.0", [{"name": "jim", "amount": "34.0", "date": "11/12/2015"}])]),
        (
            "carl",
            [("120.11", [{"name": "carl", "amount": "120.11", "date": "11/12/2015"}])],
        ),
        (
            "stacy",
            [
                ("12.01", [{"name": "stacy", "amount": "12.01", "date": "01/04/2016"}]),
                ("34.05", [{"name": "stacy", "amount": "34.05", "date": "01/04/2016"}]),
            ],
        ),
    ]


def test_group_3(data):
    a1 = datetime(2001, 1, 1)
    a2 = datetime(2001, 1, 1)
    b = datetime(2002, 1, 1)
    result = d3.group([[a1, 1], [a2, 2], [b, 3]], lambda d: d[0])
    assert result.get(a1) == [[a1, 1], [a2, 2]]
    assert result.get(a2) == [[a1, 1], [a2, 2]]
    assert result.get(b) == [[b, 3]]
    assert result.get(a1) == [[a1, 1], [a2, 2]]
    assert result.get(a2) == [[a1, 1], [a2, 2]]
    assert result.get(b) == [[b, 3]]
    assert list(result)[0] == a1
    assert list(result)[1] == b
