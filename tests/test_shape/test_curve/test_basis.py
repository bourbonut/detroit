import detroit as d3


def test_basis_1():
    line = d3.line().curve(d3.curve_basis)
    assert line([]) is None
    assert line([[0, 1]]) == "M0,1Z"
    assert line([[0, 1], [1, 3]]) == "M0,1L1,3"
    assert (
        line([[0, 1], [1, 3], [2, 1]])
        == "M0,1L0.167,1.333C0.333,1.667,0.667,2.333,1,2.333C1.333,2.333,1.667,1.667,1.833,1.333L2,1"
    )


def test_basis_2():
    area = d3.area().curve(d3.curve_basis)
    assert area([]) is None
    assert area([[0, 1]]) == "M0,1L0,0Z"
    assert area([[0, 1], [1, 3]]) == "M0,1L1,3L1,0L0,0Z"
    assert (
        area([[0, 1], [1, 3], [2, 1]])
        == "M0,1L0.167,1.333C0.333,1.667,0.667,2.333,1,2.333C1.333,2.333,1.667,1.667,1.833,1.333L2,1L2,0L1.833,0C1.667,0,1.333,0,1,0C0.667,0,0.333,0,0.167,0L0,0Z"
    )
