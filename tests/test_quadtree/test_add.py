import detroit as d3


def test_add_1():
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


def test_add_2():
    q = d3.quadtree().set_extent([[0, 0], [1, 1]])
    assert q.add([0, 0]).get_root() == {"data": [0, 0]}
    assert q.add([1, 1]).get_root() == [
        {"data": [0, 0]},
        None,
        None,
        {"data": [1, 1]},
    ]
    assert q.add([1, 0]).get_root() == [
        {"data": [0, 0]},
        {"data": [1, 0]},
        None,
        {"data": [1, 1]},
    ]
    assert q.add([0, 1]).get_root() == [
        {"data": [0, 0]},
        {"data": [1, 0]},
        {"data": [0, 1]},
        {"data": [1, 1]},
    ]


def test_add_3():
    q = d3.quadtree().set_extent([[0, 0], [2, 2]])
    assert q.add([1, -1]).get_extent() == [[0, -4], [8, 4]]


def test_add_4():
    q = d3.quadtree().set_extent([[0, 0], [2, 2]])
    assert q.add([3, 1]).get_extent() == [[0, 0], [4, 4]]


def test_add_5():
    q = d3.quadtree().set_extent([[0, 0], [2, 2]])
    assert q.add([1, 3]).get_extent() == [[0, 0], [4, 4]]


def test_add_6():
    q = d3.quadtree().set_extent([[0, 0], [2, 2]])
    assert q.add([-1, 1]).get_extent() == [[-4, 0], [4, 8]]


def test_add_7():
    q = d3.quadtree().set_extent([[0, 0], [1, 1]])
    assert q.add([0, 0]).get_root() == {"data": [0, 0]}
    assert q.add([1, 0]).get_root() == [
        {"data": [0, 0]},
        {"data": [1, 0]},
        None,
        None,
    ]
    assert q.add([0, 1]).get_root() == [
        {"data": [0, 0]},
        {"data": [1, 0]},
        {"data": [0, 1]},
        None,
    ]
    assert q.add([0, 1]).get_root() == [
        {"data": [0, 0]},
        {"data": [1, 0]},
        {"data": [0, 1], "next": {"data": [0, 1]}},
        None,
    ]


def test_add_8():
    q = d3.quadtree().add([1, 2])
    assert q.get_extent() == [[1, 2], [2, 3]]
