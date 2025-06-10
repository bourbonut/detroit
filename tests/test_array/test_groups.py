import detroit as d3
import pytest


@pytest.fixture
def data():
    return [
        {"name": "jim", "amount": "34.0", "date": "11/12/2015"},
        {"name": "carl", "amount": "120.11", "date": "11/12/2015"},
        {"name": "stacy", "amount": "12.01", "date": "01/04/2016"},
        {"name": "stacy", "amount": "34.05", "date": "01/04/2016"},
    ]


def test_groups_1(data):
    assert d3.groups(data, lambda d: d["name"]) == [
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


def test_groups_2(data):
    assert d3.groups(data, lambda d: d["name"], lambda d: d["amount"]) == [
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
