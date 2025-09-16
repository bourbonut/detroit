import detroit as d3
from math import nan


def test_cover_1():
    assert d3.quadtree().cover(1, 2).get_extent() == [[1, 2], [2, 3]]


def test_cover_2():
    assert d3.quadtree().cover(0, 0).cover(1, 2).get_extent() == [[0, 0], [4, 4]]


def test_cover_3():
    assert d3.quadtree().cover(0, 0).cover(nan, 2).get_extent() == [[0, 0], [1, 1]]


def test_cover_4():
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(-1, -1).get_extent() == [
        [-4, -4],
        [4, 4],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(1, -1).get_extent() == [
        [0, -4],
        [8, 4],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(3, -1).get_extent() == [
        [0, -4],
        [8, 4],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(3, 1).get_extent() == [
        [0, 0],
        [4, 4],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(3, 3).get_extent() == [
        [0, 0],
        [4, 4],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(1, 3).get_extent() == [
        [0, 0],
        [4, 4],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(-1, 3).get_extent() == [
        [-4, 0],
        [4, 8],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(-1, 1).get_extent() == [
        [-4, 0],
        [4, 8],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(-3, -3).get_extent() == [
        [-4, -4],
        [4, 4],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(3, -3).get_extent() == [
        [0, -4],
        [8, 4],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(5, -3).get_extent() == [
        [0, -4],
        [8, 4],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(5, 3).get_extent() == [
        [0, 0],
        [8, 8],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(5, 5).get_extent() == [
        [0, 0],
        [8, 8],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(3, 5).get_extent() == [
        [0, 0],
        [8, 8],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(-3, 5).get_extent() == [
        [-4, 0],
        [4, 8],
    ]
    assert d3.quadtree().cover(0, 0).cover(2, 2).cover(-3, 3).get_extent() == [
        [-4, 0],
        [4, 8],
    ]


def test_cover_5():
    q = d3.quadtree().add([0, 0]).add([2, 2])
    assert q.get_root(), [{"data": [0, 0]}, None, None, {"data": [2, 2]}]
    assert q.copy().cover(3, 3).get_root(), [
        {"data": [0, 0]},
        None,
        None,
        {"data": [2, 2]},
    ]
    assert q.copy().cover(-1, 3).get_root(), [
        None,
        [{"data": [0, 0]}, None, None, {"data": [2, 2]}],
        None,
        None,
    ]
    assert q.copy().cover(3, -1).get_root(), [
        None,
        None,
        [{"data": [0, 0]}, None, None, {"data": [2, 2]}],
        None,
    ]
    assert q.copy().cover(-1, -1).get_root(), [
        None,
        None,
        None,
        [{"data": [0, 0]}, None, None, {"data": [2, 2]}],
    ]
    assert q.copy().cover(5, 5).get_root(), [
        [{"data": [0, 0]}, None, None, {"data": [2, 2]}],
        None,
        None,
        None,
    ]
    assert q.copy().cover(-3, 5).get_root(), [
        None,
        [{"data": [0, 0]}, None, None, {"data": [2, 2]}],
        None,
        None,
    ]
    assert q.copy().cover(5, -3).get_root(), [
        None,
        [{"data": [0, 0]}, None, None, {"data": [2, 2]}],
        None,
        None,
    ]
    assert q.copy().cover(-3, -3).get_root(), [
        None,
        None,
        None,
        [{"data": [0, 0]}, None, None, {"data": [2, 2]}],
    ]


def test_cover_6():
    q = d3.quadtree().cover(0, 0).add([2, 2])
    assert q.get_root() == {"data": [2, 2]}
    assert q.copy().cover(3, 3).get_root() == {"data": [2, 2]}
    assert q.copy().cover(-1, 3).get_root() == {"data": [2, 2]}
    assert q.copy().cover(3, -1).get_root() == {"data": [2, 2]}
    assert q.copy().cover(-1, -1).get_root() == {"data": [2, 2]}
    assert q.copy().cover(5, 5).get_root() == {"data": [2, 2]}
    assert q.copy().cover(-3, 5).get_root() == {"data": [2, 2]}
    assert q.copy().cover(5, -3).get_root() == {"data": [2, 2]}
    assert q.copy().cover(-3, -3).get_root() == {"data": [2, 2]}


def test_cover_7():
    q = d3.quadtree().cover(0, 0).cover(2, 2)
    assert q.get_root() is None
    assert q.copy().cover(3, 3).get_root() is None
    assert q.copy().cover(-1, 3).get_root() is None
    assert q.copy().cover(3, -1).get_root() is None
    assert q.copy().cover(-1, -1).get_root() is None
    assert q.copy().cover(5, 5).get_root() is None
    assert q.copy().cover(-3, 5).get_root() is None
    assert q.copy().cover(5, -3).get_root() is None
    assert q.copy().cover(-3, -3).get_root() is None


def test_cover_8():
    # Expect no crash
    d3.quadtree([[1e23, 0]])
