from itertools import starmap

import detroit as d3
import pytest


def entries(map_obj, depth):
    if depth > 0:
        return list(starmap(lambda k, v: (k, entries(v, depth - 1)), map_obj.items()))
    else:
        return map_obj


@pytest.fixture
def data():
    return [
        {"name": "jim", "amount": 34.0, "date": "11/12/2015"},
        {"name": "carl", "amount": 120.11, "date": "11/12/2015"},
        {"name": "stacy", "amount": 12.01, "date": "01/04/2016"},
        {"name": "stacy", "amount": 34.05, "date": "01/04/2016"},
    ]


def test_index_1(data):
    assert d3.indexes(data, lambda d: d["amount"]) == [
        (34.0, {"name": "jim", "amount": 34.0, "date": "11/12/2015"}),
        (120.11, {"name": "carl", "amount": 120.11, "date": "11/12/2015"}),
        (12.01, {"name": "stacy", "amount": 12.01, "date": "01/04/2016"}),
        (34.05, {"name": "stacy", "amount": 34.05, "date": "01/04/2016"}),
    ]
    assert d3.indexes(data, lambda d: d["name"], lambda d: d["amount"]) == [
        ("jim", [(34.0, {"name": "jim", "amount": 34.0, "date": "11/12/2015"})]),
        ("carl", [(120.11, {"name": "carl", "amount": 120.11, "date": "11/12/2015"})]),
        (
            "stacy",
            [
                (12.01, {"name": "stacy", "amount": 12.01, "date": "01/04/2016"}),
                (34.05, {"name": "stacy", "amount": 34.05, "date": "01/04/2016"}),
            ],
        ),
    ]


def test_index_2(data):
    assert entries(d3.index(data, lambda d: d["amount"]), 1) == d3.indexes(
        data, lambda d: d["amount"]
    )
    assert entries(
        d3.index(data, lambda d: d["name"], lambda d: d["amount"]), 2
    ) == d3.indexes(data, lambda d: d["name"], lambda d: d["amount"])


def test_index_3(data):
    with pytest.raises(IndexError) as excinfo:
        d3.index(data, lambda d: d["name"])
    assert str(excinfo.value) == "Duplicate key"
    with pytest.raises(IndexError) as excinfo:
        d3.index(data, lambda d: d["date"])
    assert str(excinfo.value) == "Duplicate key"
