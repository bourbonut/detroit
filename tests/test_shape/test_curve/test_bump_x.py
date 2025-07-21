import detroit as d3


def test_bump_x_1():
    line = d3.line().set_curve(d3.curve_bump_x)
    assert line([]) is None
    assert line([[0, 1]]) == "M0,1Z"
    assert line([[0, 1], [1, 3]]) == "M0,1C0.500,1,0.500,3,1,3"
    assert (
        line([[0, 1], [1, 3], [2, 1]]) == "M0,1C0.500,1,0.500,3,1,3C1.500,3,1.500,1,2,1"
    )


def test_bump_x_2():
    area = d3.area().set_curve(d3.curve_bump_x)
    assert area([]) is None
    assert area([[0, 1]]) == "M0,1L0,0Z"
    assert area([[0, 1], [1, 3]]) == "M0,1C0.500,1,0.500,3,1,3L1,0C0.500,0,0.500,0,0,0Z"
    assert (
        area([[0, 1], [1, 3], [2, 1]])
        == "M0,1C0.500,1,0.500,3,1,3C1.500,3,1.500,1,2,1L2,0C1.500,0,1.500,0,1,0C0.500,0,0.500,0,0,0Z"
    )
