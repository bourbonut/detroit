import detroit as d3
from .expected import expected_many_body
import pytest

def node_equal(actual, expected, delta=1e-6):
    return (
        actual["index"] == expected["index"]
        and actual["name"] == expected["name"]
        and actual["id"] == expected["id"]
        and abs(actual["x"] - expected["x"]) < delta
        and abs(actual["vx"] - expected["vx"]) < delta
        and abs(actual["y"] - expected["y"]) < delta
        and abs(actual["vy"] - expected["vy"]) < delta
    )

@pytest.fixture
def data():
    return {
        "nodes": [
            {"id": 1, "name": "A"},
            {"id": 2, "name": "B"},
            {"id": 3, "name": "C"},
            {"id": 4, "name": "D"},
            {"id": 5, "name": "E"},
            {"id": 6, "name": "F"},
            {"id": 7, "name": "G"},
            {"id": 8, "name": "H"},
            {"id": 9, "name": "I"},
            {"id": 10, "name": "J"},
        ],
        "links": [
            {"source": 1, "target": 2},
            {"source": 1, "target": 5},
            {"source": 1, "target": 6},
            {"source": 2, "target": 3},
            {"source": 2, "target": 7},
            {"source": 3, "target": 4},
            {"source": 8, "target": 3},
            {"source": 4, "target": 5},
            {"source": 4, "target": 9},
            {"source": 5, "target": 10},
        ],
    }

def test_many_body_1(data):
    expected = expected_many_body()
    f = (
        d3.force_simulation(data["nodes"])
        .set_force(
            "link",
            (
                d3.force_link()
                .set_id(lambda d: d["id"])
                .set_links(data["links"])
            )
        )
        .set_force("charge", d3.force_many_body().set_strength(-400))
    )
    f.tick(10)
    assert len(data["nodes"]) == len(expected)
    for actual, expected in zip(data["nodes"], expected):
        assert node_equal(actual, expected), f"{actual}, {expected}"
