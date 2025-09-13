import detroit as d3

def test_area_1():
    assert d3.polygon_area([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]) == 1

def test_area_2():
    assert d3.polygon_area([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]) == -1
    assert d3.polygon_area([[1, 1], [3, 2], [2, 3], [1, 1]]) == -1.5

def test_area_3():
    assert d3.polygon_area([[0, 0], [0, 1], [1, 1], [1, 0]]) == 1

def test_area_4():
    assert d3.polygon_area([[0, 0], [1, 0], [1, 1], [0, 1]]) == -1
    assert d3.polygon_area([[1, 1], [3, 2], [2, 3]]) == -1.5

def test_area_5():
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

    assert d3.polygon_area(points) == 1e16 - 5e7
