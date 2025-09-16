import detroit as d3


def x(d):
    return d["x"]


def test_x_1():
    q = d3.quadtree().x(x).add({"x": 1, 1: 2})
    assert q.get_extent() == [[1, 2], [2, 3]]


def test_x_2():
    q = d3.quadtree().x(x).add_all([{"x": 1, 1: 2}])
    assert q.get_extent() == [[1, 2], [2, 3]]


def test_x_3():
    p0 = {"x": 0, 1: 1}
    p1 = {"x": 1, 1: 2}
    q = d3.quadtree().x(x)
    assert q.add(p0).get_root() == {"data": {"x": 0, 1: 1}}
    assert q.add(p1).get_root() == [
        {"data": {"x": 0, 1: 1}},
        None,
        None,
        {"data": {"x": 1, 1: 2}},
    ]
    assert q.remove(p1).get_root() == {"data": {"x": 0, 1: 1}}
    assert q.remove(p0).get_root() is None
