import detroit as d3


def test_bundle_1():
    line = d3.line().set_curve(d3.curve_bundle(0.85))
    assert d3.line().set_curve(d3.curve_bundle)(
        [[0, 1], [1, 3], [2, 1], [3, 3]]
    ) == line([[0, 1], [1, 3], [2, 1], [3, 3]])


def test_bundle_2():
    assert (
        d3.line().set_curve(d3.curve_bundle(0.5))([[0, 1], [1, 3], [2, 1], [3, 3]])
        == "M0,1L0.167,1.222C0.333,1.444,0.667,1.889,1,2C1.333,2.111,1.667,1.889,2,2C2.333,2.111,2.667,2.556,2.833,2.778L3,3"
    )


def test_bundle_3():
    line = d3.line().set_curve(d3.curve_bundle(0.5))
    assert d3.line().set_curve(d3.curve_bundle(0.5))(
        [[0, 1], [1, 3], [2, 1], [3, 3]]
    ) == line([[0, 1], [1, 3], [2, 1], [3, 3]])
