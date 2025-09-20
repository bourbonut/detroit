import detroit as d3
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

def test_link_1(data):
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
    )
    f.tick(10)
    expected = [
        {
            "id": 1,
            "name": "A",
            "index": 0,
            "x": 12.165177982023216,
            "y": 1.3919775324002606,
            "vy": -0.015417783217525925,
            "vx": 0.0853712691535829,
        },
        {
            "id": 2,
            "name": "B",
            "index": 1,
            "x": -16.922430045866108,
            "y": 7.228664522553369,
            "vy": -0.07626215843950207,
            "vx": 0.011849111240271968,
        },
        {
            "id": 3,
            "name": "C",
            "index": 2,
            "x": 4.214331051921006,
            "y": -14.92712079575815,
            "vy": 0.003351491430000983,
            "vx": -0.09997835294543132,
        },
        {
            "id": 4,
            "name": "D",
            "index": 3,
            "x": 5.813947867772528,
            "y": 14.577837035591324,
            "vy": 0.08574953121458115,
            "vx": -0.03275363159882636,
        },
        {
            "id": 5,
            "name": "E",
            "index": 4,
            "x": -17.25364035507001,
            "y": -4.835843512972531,
            "vy": 0.04764780682535138,
            "vx": 0.07398387642271567,
        },
        {
            "id": 6,
            "name": "F",
            "index": 5,
            "x": 29.626459380484654,
            "y": -22.996613275631898,
            "vy": -0.04676624061162874,
            "vx": 0.04280933058349649,
        },
        {
            "id": 7,
            "name": "G",
            "index": 6,
            "x": -4.431507838725603,
            "y": 34.516784658111135,
            "vy": -0.05543555952842146,
            "vx": -0.03404047297389664,
        },
        {
            "id": 8,
            "name": "H",
            "index": 7,
            "x": -21.761407069785637,
            "y": -29.903383698918248,
            "vy": -0.04454931917470618,
            "vx": -0.07475715457167968,
        },
        {
            "id": 9,
            "name": "I",
            "index": 8,
            "x": 35.12472438384858,
            "y": 8.153552740863415,
            "vy": 0.009840118018971571,
            "vx": -0.04981414738726892,
        },
        {
            "id": 10,
            "name": "J",
            "index": 9,
            "x": -33.41899444737327,
            "y": 20.436934671757523,
            "vy": 0.001704337857068319,
            "vx": 0.00038562753241027986,
        },
    ]
    assert len(data["nodes"]) == len(expected)
    for actual, expected in zip(data["nodes"], expected):
        assert node_equal(actual, expected), f"{actual}, {expected}"
