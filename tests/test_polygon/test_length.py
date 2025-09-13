import detroit as d3
from math import sqrt

def test_length_1():
    assert d3.polygon_length([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]) == 4

def test_length_2():
    assert d3.polygon_length([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]) == 4
    assert d3.polygon_length([[1, 1], [3, 2], [2, 3], [1, 1]]) == sqrt(20) + sqrt(2)

def test_length_3():
    assert d3.polygon_length([[0, 0], [0, 1], [1, 1], [1, 0]]) == 4

def test_length_4():
    assert d3.polygon_length([[0, 0], [1, 0], [1, 1], [0, 1]]) == 4
    assert d3.polygon_length([[1, 1], [3, 2], [2, 3]]) == sqrt(20) + sqrt(2)
