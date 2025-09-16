import detroit as d3


def test_data_1():
    q = d3.quadtree()
    assert q.data() == []
    q.add([0, 0]).add([1, 2])
    assert q.data() == [[0, 0], [1, 2]]


def test_data_2():
    q = d3.quadtree()
    q.add([0, 0]).add([0, 0])
    assert q.data() == [[0, 0], [0, 0]]
