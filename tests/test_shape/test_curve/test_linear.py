import detroit as d3


def test_linear_1():
    line = d3.line()
    assert line([]) is None
    assert line([[0, 1]]) == "M0,1Z"
    assert line([[0, 1], [2, 3]]) == "M0,1L2,3"
    assert line([[0, 1], [2, 3], [4, 5]]) == "M0,1L2,3L4,5"


def test_linear_2():
    area = d3.area()
    assert area([]) is None
    assert area([[0, 1]]) == "M0,1L0,0Z"
    assert area([[0, 1], [2, 3]]) == "M0,1L2,3L2,0L0,0Z"
    assert area([[0, 1], [2, 3], [4, 5]]) == "M0,1L2,3L4,5L4,0L2,0L0,0Z"
