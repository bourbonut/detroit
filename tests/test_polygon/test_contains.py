import detroit as d3


def test_contains_1():
    assert (
        d3.polygon_contains([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]], [0.5, 0.5])
        is True
    )
    assert (
        d3.polygon_contains([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]], [1.5, 0.5])
        is False
    )
    assert (
        d3.polygon_contains([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]], [-0.5, 0.5])
        is False
    )
    assert (
        d3.polygon_contains([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]], [0.5, 1.5])
        is False
    )
    assert (
        d3.polygon_contains([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]], [0.5, -0.5])
        is False
    )


def test_contains_2():
    assert (
        d3.polygon_contains([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], [0.5, 0.5])
        is True
    )
    assert d3.polygon_contains([[1, 1], [3, 2], [2, 3], [1, 1]], [1.5, 1.5]) is True


def test_contains_3():
    assert d3.polygon_contains([[0, 0], [0, 1], [1, 1], [1, 0]], [0.5, 0.5]) is True


def test_contains_4():
    assert d3.polygon_contains([[0, 0], [1, 0], [1, 1], [0, 1]], [0.5, 0.5]) is True
    assert d3.polygon_contains([[1, 1], [3, 2], [2, 3]], [1.5, 1.5]) is True
