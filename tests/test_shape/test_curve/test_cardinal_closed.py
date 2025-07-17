import detroit as d3


def test_cardinal_closed_1():
    line = d3.line().curve(d3.curve_cardinal_closed)
    assert line([]) is None
    assert line([[0, 1]]) == "M0,1Z"
    assert line([[0, 1], [1, 3]]) == "M1,3L0,1Z"
    assert (
        line([[0, 1], [1, 3], [2, 1]])
        == "M1,3C1.333,3,2.167,1.333,2,1C1.833,0.667,0.167,0.667,0,1C-0.167,1.333,0.667,3,1,3"
    )
    assert (
        line([[0, 1], [1, 3], [2, 1], [3, 3]])
        == "M1,3C1.333,3,1.667,1,2,1C2.333,1,3.333,3,3,3C2.667,3,0.333,1,0,1C-0.333,1,0.667,3,1,3"
    )


def test_cardinal_closed_2():
    line = d3.line().curve(d3.curve_cardinal_closed(0))
    assert d3.line().curve(d3.curve_cardinal_closed)(
        [[0, 1], [1, 3], [2, 1], [3, 3]]
    ) == line([[0, 1], [1, 3], [2, 1], [3, 3]])


def test_cardinal_closed_3():
    assert (
        d3.line().curve(d3.curve_cardinal_closed(0.5))([[0, 1], [1, 3], [2, 1], [3, 3]])
        == "M1,3C1.167,3,1.833,1,2,1C2.167,1,3.167,3,3,3C2.833,3,0.167,1,0,1C-0.167,1,0.833,3,1,3"
    )


def test_cardinal_closed_4():
    line = d3.line().curve(d3.curve_cardinal_closed(0.5))
    assert d3.line().curve(d3.curve_cardinal_closed(0.5))(
        [[0, 1], [1, 3], [2, 1], [3, 3]]
    ) == line([[0, 1], [1, 3], [2, 1], [3, 3]])


def test_cardinal_closed_5():
    area = d3.area().curve(d3.curve_cardinal_closed)
    assert area([]) is None
    assert area([[0, 1]]) == "M0,1ZM0,0Z"
    assert area([[0, 1], [1, 3]]) == "M1,3L0,1ZM0,0L1,0Z"
    assert (
        area([[0, 1], [1, 3], [2, 1]])
        == "M1,3C1.333,3,2.167,1.333,2,1C1.833,0.667,0.167,0.667,0,1C-0.167,1.333,0.667,3,1,3M1,0C0.667,0,-0.167,0,0,0C0.167,0,1.833,0,2,0C2.167,0,1.333,0,1,0"
    )
    assert (
        area([[0, 1], [1, 3], [2, 1], [3, 3]])
        == "M1,3C1.333,3,1.667,1,2,1C2.333,1,3.333,3,3,3C2.667,3,0.333,1,0,1C-0.333,1,0.667,3,1,3M2,0C1.667,0,1.333,0,1,0C0.667,0,-0.333,0,0,0C0.333,0,2.667,0,3,0C3.333,0,2.333,0,2,0"
    )


def test_cardinal_closed_6():
    area = d3.area().curve(d3.curve_cardinal_closed(0))
    assert d3.area().curve(d3.curve_cardinal_closed)(
        [[0, 1], [1, 3], [2, 1], [3, 3]]
    ) == area([[0, 1], [1, 3], [2, 1], [3, 3]])


def test_cardinal_closed_7():
    assert (
        d3.area().curve(d3.curve_cardinal_closed(0.5))([[0, 1], [1, 3], [2, 1], [3, 3]])
        == "M1,3C1.167,3,1.833,1,2,1C2.167,1,3.167,3,3,3C2.833,3,0.167,1,0,1C-0.167,1,0.833,3,1,3M2,0C1.833,0,1.167,0,1,0C0.833,0,-0.167,0,0,0C0.167,0,2.833,0,3,0C3.167,0,2.167,0,2,0"
    )


def test_cardinal_closed_8():
    area = d3.area().curve(d3.curve_cardinal_closed(0.5))
    assert d3.area().curve(d3.curve_cardinal_closed(0.5))(
        [[0, 1], [1, 3], [2, 1], [3, 3]]
    ) == area([[0, 1], [1, 3], [2, 1], [3, 3]])
