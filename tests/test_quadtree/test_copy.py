import detroit as d3


def test_copy_1():
    q0 = d3.quadtree().add_all([[0, 0], [1, 0], [0, 1], [1, 1]])
    assert q0.copy().get_root() == q0.get_root()


def test_copy_2():
    q0 = d3.quadtree().set_extent([[0, 0], [1, 1]])
    q1 = q0.copy()
    q0.add([2, 2])
    assert q1.get_extent() == [[0, 0], [2, 2]]
    q1.add([-1, -1])
    assert q0.get_extent() == [[0, 0], [4, 4]]


def test_copy_3():
    q0 = d3.quadtree().set_extent([[0, 0], [1, 1]])
    q1 = q0.copy()
    p0 = [2, 2]
    q0.add(p0)
    assert q1.get_root() is None
    q2 = q0.copy()
    assert q0.get_root() == {"data": [2, 2]}
    assert q2.get_root() == {"data": [2, 2]}
    assert q0.remove(p0) == q0
    assert q0.get_root() is None
    assert q2.get_root() == {"data": [2, 2]}


def test_copy_4():
    p0 = [1, 1]
    p1 = [2, 2]
    p2 = [3, 3]
    q0 = d3.quadtree().set_extent([[0, 0], [4, 4]]).add_all([p0, p1])
    q1 = q0.copy()
    q0.add(p2)
    assert q0.get_extent() == [[0, 0], [8, 8]]
    assert q0.get_root(), [
        [
            {"data": [1, 1]},
            None,
            None,
            None,
            [{"data": [2, 2]}, None, None, None, {"data": [3, 3]}],
        ],
        None,
        None,
        None,
        None,
        None,
    ]
    assert q1.get_extent() == [[0, 0], [8, 8]]
    assert q1.get_root(), [
        [{"data": [1, 1]}, None, None, None, {"data": [2, 2]}],
        None,
        None,
        None,
        None,
        None,
    ]
    q3 = q0.copy()
    q0.remove(p2)
    assert q3.get_extent() == [[0, 0], [8, 8]]
    assert q3.get_root(), [
        [
            {"data": [1, 1]},
            None,
            None,
            None,
            [{"data": [2, 2]}, None, None, None, {"data": [3, 3]}],
        ],
        None,
        None,
        None,
        None,
        None,
    ]
