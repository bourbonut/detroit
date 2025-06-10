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
        {"name": "jim", "amount": "3400", "date": "11/12/2015"},
        {"name": "carl", "amount": "12011", "date": "11/12/2015"},
        {"name": "stacy", "amount": "1201", "date": "01/04/2016"},
        {"name": "stacy", "amount": "3405", "date": "01/04/2016"},
    ]


def test_rollups_1(data):
    assert d3.rollups(data, len, lambda d: d["name"]) == [
        ("jim", 1),
        ("carl", 1),
        ("stacy", 2),
    ]
    assert d3.rollups(
        data, lambda v: sum(map(lambda d: int(d["amount"]), v)), lambda d: d["name"]
    ) == [("jim", 3400), ("carl", 12011), ("stacy", 4606)]


def test_rollups_2(data):
    assert d3.rollups(data, len, lambda d: d["name"], lambda d: d["amount"]) == [
        ("jim", [("3400", 1)]),
        ("carl", [("12011", 1)]),
        ("stacy", [("1201", 1), ("3405", 1)]),
    ]
