import detroit as d3


def y(d):
    return d["y"]


def test_y_1():
    q = d3.quadtree().y(y).add({0: 1, "y": 2})
    assert q.get_extent() == [[1, 2], [2, 3]]


def test_y_2():
    q = d3.quadtree().y(y).add_all([{0: 1, "y": 2}])
    assert q.get_extent() == [[1, 2], [2, 3]]


def test_y_3():
    p0 = {0: 0, "y": 1}
    p1 = {0: 1, "y": 2}
    q = d3.quadtree().y(y)
    assert q.add(p0).get_root() == {"data": {0: 0, "y": 1}}
    assert q.add(p1).get_root() == [
        {"data": {0: 0, "y": 1}},
        None,
        None,
        {"data": {0: 1, "y": 2}},
    ]
    assert q.remove(p1).get_root() == {"data": {0: 0, "y": 1}}
    assert q.remove(p0).get_root() is None
