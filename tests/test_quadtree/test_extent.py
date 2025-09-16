import detroit as d3
from math import nan


def test_extent_1():
    assert d3.quadtree().set_extent([[0, 1], [2, 6]]).get_extent() == [[0, 1], [8, 9]]


def test_extent_2():
    q = d3.quadtree()
    assert q.cover(0, 0).get_extent() == [[0, 0], [1, 1]]
    assert q.cover(2, 4).get_extent() == [[0, 0], [8, 8]]


def test_extent_3():
    q = d3.quadtree()
    q.add([0, 0])
    assert q.get_extent() == [[0, 0], [1, 1]]
    q.add([2, 4])
    assert q.get_extent() == [[0, 0], [8, 8]]


def test_extent_4():
    assert d3.quadtree().set_extent([[0, 1], [2, 6]]).get_extent() == [[0, 1], [8, 9]]


def test_extent_5():
    assert d3.quadtree().set_extent([[1, nan], [nan, 0]]).get_extent() is None
    assert d3.quadtree().set_extent([[nan, 1], [0, nan]]).get_extent() is None
    assert d3.quadtree().set_extent([[nan, nan], [nan, nan]]).get_extent() is None


def test_extent_6():
    assert d3.quadtree().set_extent([[1, 1], [0, 0]]).get_extent() == [[0, 0], [2, 2]]


def test_extent_7():
    assert d3.quadtree().set_extent([[nan, 0], [1, 1]]).get_extent() == [[1, 1], [2, 2]]
    assert d3.quadtree().set_extent([[0, nan], [1, 1]]).get_extent() == [[1, 1], [2, 2]]
    assert d3.quadtree().set_extent([[0, 0], [nan, 1]]).get_extent() == [[0, 0], [1, 1]]
    assert d3.quadtree().set_extent([[0, 0], [1, nan]]).get_extent() == [[0, 0], [1, 1]]


def test_extent_8():
    assert d3.quadtree().set_extent([[0, 0], [0, 0]]).get_extent() == [[0, 0], [1, 1]]
    assert d3.quadtree().set_extent([[1, 1], [1, 1]]).get_extent() == [[1, 1], [2, 2]]
