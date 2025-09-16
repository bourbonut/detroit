import detroit as d3
from math import nan


def test_add_all_1():
    q = d3.quadtree()
    assert q.add([0, 0]).get_root() == {"data": [0, 0]}
    assert q.add([0.9, 0.9]).get_root() == [
        {"data": [0, 0]},
        None,
        None,
        {"data": [0.9, 0.9]},
    ]
    assert q.add([0.9, 0.0]).get_root() == [
        {"data": [0, 0]},
        {"data": [0.9, 0]},
        None,
        {"data": [0.9, 0.9]},
    ]
    assert q.add([0.0, 0.9]).get_root() == [
        {"data": [0, 0]},
        {"data": [0.9, 0]},
        {"data": [0, 0.9]},
        {"data": [0.9, 0.9]},
    ]
    assert q.add([0.4, 0.4]).get_root() == [
        [{"data": [0, 0]}, None, None, {"data": [0.4, 0.4]}],
        {"data": [0.9, 0]},
        {"data": [0, 0.9]},
        {"data": [0.9, 0.9]},
    ]


def test_add_all_2():
    q = d3.quadtree()
    assert q.add_all([[nan, 0], [0, nan]]).get_root() is None
    assert q.get_extent() is None
    assert q.add_all([[0, 0], [0.9, 0.9]]).get_root() == [
        {"data": [0, 0]},
        None,
        None,
        {"data": [0.9, 0.9]},
    ]
    assert q.add_all([[nan, 0], [0, nan]]).get_root() == [
        {"data": [0, 0]},
        None,
        None,
        {"data": [0.9, 0.9]},
    ]
    assert q.get_extent() == [[0, 0], [1, 1]]


def test_add_all_3():
    q = d3.quadtree()
    assert q.add_all([]).get_root() is None
    assert q.get_extent() is None
    assert q.add_all([[0, 0], [1, 1]]).get_root() == [
        {"data": [0, 0]},
        None,
        None,
        {"data": [1, 1]},
    ]
    assert q.add_all([]).get_root() == [
        {"data": [0, 0]},
        None,
        None,
        {"data": [1, 1]},
    ]
    assert q.get_extent() == [[0, 0], [2, 2]]


def test_add_all_4():
    q = d3.quadtree().add_all([[0.4, 0.4], [0, 0], [0.9, 0.9]])
    assert q.get_root() == [
        [{"data": [0, 0]}, None, None, {"data": [0.4, 0.4]}],
        None,
        None,
        {"data": [0.9, 0.9]},
    ]


def test_add_all_5():
    q = d3.quadtree().add_all(set([(0.4, 0.4), (0, 0), (0.9, 0.9)]))
    assert q.get_root() == [
        [{"data": (0, 0)}, None, None, {"data": (0.4, 0.4)}],
        None,
        None,
        {"data": (0.9, 0.9)},
    ]


def test_add_all_6():
    q = d3.quadtree(set([(0.4, 0.4), (0, 0), (0.9, 0.9)]))
    assert q.get_root() == [
        [{"data": (0, 0)}, None, None, {"data": (0.4, 0.4)}],
        None,
        None,
        {"data": (0.9, 0.9)},
    ]
