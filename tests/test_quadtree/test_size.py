import detroit as d3


def test_size_1():
    q = d3.quadtree()
    assert q.size() == 0
    q.add([0, 0]).add([1, 2])
    assert q.size() == 2


def test_size_2():
    q = d3.quadtree()
    q.add([0, 0]).add([0, 0])
    assert q.size() == 2
