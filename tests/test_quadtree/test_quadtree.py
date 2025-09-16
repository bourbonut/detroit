import detroit as d3
from detroit.quadtree.quadtree import Quadtree


def test_quadtree_1():
    q = d3.quadtree()
    assert isinstance(q, Quadtree)

    def foo(*args):
        raise ValueError()

    assert q.visit(foo) == q
    assert q.size() == 0
    assert q.get_extent() is None
    assert q.get_root() is None
    assert q.data() == []


def test_quadtree_2():
    q = d3.quadtree([[0, 0], [1, 1]])
    assert isinstance(q, Quadtree)
    assert q.get_root(), [{"data": [0, 0]}, None, None, None, {"data": [1, 1]}]


def test_quadtree_3():
    q = d3.quadtree(
        [{"x": 0, "y": 0}, {"x": 1, "y": 1}], lambda d: d["x"], lambda d: d["y"]
    )
    assert isinstance(q, Quadtree)
    assert q.get_root(), [
        {"data": {"x": 0, "y": 0}},
        None,
        None,
        None,
        {"data": {"x": 1, "y": 1}},
    ]
