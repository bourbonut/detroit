import detroit as d3
from math import inf, sqrt

SQRT2 = sqrt(2)


def test_find_1():
    dx = 17
    dy = 17
    q = d3.quadtree()
    for i in range(dx * dy):
        q.add([i % dx, i // dx])
    assert q.find(0.1, 0.1) == [0, 0]
    assert q.find(7.1, 7.1) == [7, 7]
    assert q.find(0.1, 15.9) == [0, 16]
    assert q.find(15.9, 15.9) == [16, 16]


def test_find_2():
    q = d3.quadtree([[0, 0], [100, 0], [0, 100], [100, 100]])
    assert q.find(20, 20, inf) == [0, 0]
    assert q.find(20, 20, 20 * SQRT2 + 1e-6) == [0, 0]
    assert q.find(20, 20, 20 * SQRT2 - 1e-6) is None
    assert q.find(0, 20, 20 + 1e-6) == [0, 0]
    assert q.find(0, 20, 20 - 1e-6) is None
    assert q.find(20, 0, 20 + 1e-6) == [0, 0]
    assert q.find(20, 0, 20 - 1e-6) is None


def test_find_3():
    q = d3.quadtree([[0, 0], [100, 0], [0, 100], [100, 100]])
    assert q.find(20, 20, None) == [0, 0]
