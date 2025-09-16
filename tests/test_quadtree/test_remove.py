import detroit as d3


def test_remove_1():
    p0 = [1, 1]
    q = d3.quadtree().add(p0)
    assert q.remove(p0) == q
    assert q.get_root() is None


def test_remove_2():
    p0 = [1, 1]
    q = d3.quadtree().add(p0)
    assert q.remove(p0) == q
    assert q.get_extent() == [[1, 1], [2, 2]]
    assert q.get_root() is None
    assert p0, [1, 1]


def test_remove_3():
    p0 = [1, 1]
    p1 = [1, 1]
    q = d3.quadtree().add_all([p0, p1])
    assert q.remove(p0) == q
    assert q.get_extent() == [[1, 1], [2, 2]]
    assert q.get_root()["data"] == p1
    assert p0, [1, 1]
    assert p1, [1, 1]


def test_remove_4():
    p0 = [1, 1]
    p1 = [1, 1]
    q = d3.quadtree().add_all([p0, p1])
    assert q.remove(p1) == q
    assert q.get_extent() == [[1, 1], [2, 2]]
    assert q.get_root()["data"] == p0
    assert p0, [1, 1]
    assert p1, [1, 1]


def test_remove_5():
    p0 = [0, 0]
    p1 = [1, 1]
    q = d3.quadtree().add_all([p0, p1])
    assert q.remove(p0) == q
    assert q.get_extent() == [[0, 0], [2, 2]]
    assert q.get_root()["data"] == p1
    assert p0, [0, 0]
    assert p1, [1, 1]


def test_remove_6():
    p0 = [0, 0]
    p1 = [1, 1]
    q = d3.quadtree().add_all([p0, p1])
    assert q.remove(p1) == q
    assert q.get_extent() == [[0, 0], [2, 2]]
    assert q.get_root()["data"] == p0
    assert p0, [0, 0]
    assert p1, [1, 1]


def test_remove_7():
    p0 = [0, 0]
    p1 = [1, 1]
    q0 = d3.quadtree().add(p0)
    q1 = d3.quadtree().add(p1)
    assert q0.remove(p1) == q0
    assert q0.get_extent() == [[0, 0], [1, 1]]
    assert q0.get_root()["data"] == p0
    assert q1.get_root()["data"] == p1


def test_remove_8():
    p0 = [0, 0]
    p1 = [0, 0]
    q0 = d3.quadtree().add(p0)
    q1 = d3.quadtree().add(p1)
    assert q0.remove(p1) == q0
    assert q0.get_extent() == [[0, 0], [1, 1]]
    assert q0.get_root()["data"] == p0
    assert q1.get_root()["data"] == p1


def test_remove_9():
    q = d3.quadtree().set_extent([[0, 0], [959, 959]])
    q.add_all(
        [
            [630, 438],
            [715, 464],
            [523, 519],
            [646, 318],
            [434, 620],
            [570, 489],
            [520, 345],
            [459, 443],
            [346, 405],
            [529, 444],
        ]
    )
    assert q.remove(q.find(546, 440)) == q
    assert q.get_extent() == [[0, 0], [1024, 1024]]
    assert q.get_root() == [
        [None, None, None, [None, None, {"data": [346, 405]}, {"data": [459, 443]}]],
        [
            None,
            None,
            [
                {"data": [520, 345]},
                {"data": [646, 318]},
                [
                    None,
                    {"data": [630, 438]},
                    {"data": [570, 489]},
                    None,
                ],
                {"data": [715, 464]},
            ],
            None,
        ],
        {"data": [434, 620]},
        {"data": [523, 519]},
    ]
