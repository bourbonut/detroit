import detroit as d3


def test_centroid_1():
    assert d3.polygon_centroid([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]) == [0.5, 0.5]


def test_centroid_2():
    assert d3.polygon_centroid([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]) == [0.5, 0.5]
    assert d3.polygon_centroid([[1, 1], [3, 2], [2, 3], [1, 1]]) == [2, 2]


def test_centroid_3():
    assert d3.polygon_centroid([[0, 0], [0, 1], [1, 1], [1, 0]]) == [0.5, 0.5]


def test_centroid_4():
    assert d3.polygon_centroid([[0, 0], [1, 0], [1, 1], [0, 1]]) == [0.5, 0.5]
    assert d3.polygon_centroid([[1, 1], [3, 2], [2, 3]]) == [2, 2]


def test_centroid_5():
    stop = 1e8
    step = 1e4
    points = []

    value = 0
    while value < stop:
        points.append([0, value])
        value += step

    value = 0
    while value < stop:
        points.append([value, stop])
        value += step

    value = stop - step
    while value >= 0:
        points.append([stop, value])
        value -= step

    value = stop - step
    while value >= 0:
        points.append([value, 0])
        value -= step
    assert d3.polygon_centroid(points) == [49999999.75000187, 49999999.75001216]
