import detroit as d3


def reflect(p):
    return [p[1], p[0]]


def test_monotone_y_1():
    line = d3.line().set_curve(d3.curve_monotone_y)
    assert line([]) is None
    assert line([reflect(x) for x in [[0, 1]]]) == "M1,0Z"
    assert line([reflect(x) for x in [[0, 1], [1, 3]]]) == "M1,0L3,1"
    assert (
        line([reflect(x) for x in [[0, 1], [1, 3], [2, 1]]])
        == "M1,0C2,0.333,3,0.667,3,1C3,1.333,2,1.667,1,2"
    )
    assert (
        line([reflect(x) for x in [[0, 1], [1, 3], [2, 1], [3, 3]]])
        == "M1,0C2,0.333,3,0.667,3,1C3,1.333,1,1.667,1,2C1,2.333,2,2.667,3,3"
    )


def test_monotone_y_2():
    line = d3.line().set_curve(d3.curve_monotone_y)
    assert (
        line(
            [
                reflect(x)
                for x in [[0, 200], [100, 100], [200, 100], [300, 300], [400, 300]]
            ]
        )
        == "M200,0C150,33.333,100,66.667,100,100C100,133.333,100,166.667,100,200C100,233.333,300,266.667,300,300C300,333.333,300,366.667,300,400"
    )


def test_monotone_y_3():
    line = d3.line().set_curve(d3.curve_monotone_y)
    assert (
        line([reflect(x) for x in [[0, 200], [0, 100], [100, 100], [200, 0]]])
        == "M200,0C200,0,100,0,100,0C100,33.333,100,66.667,100,100C100,133.333,50,166.667,0,200"
    )
    assert (
        line([reflect(x) for x in [[0, 200], [100, 100], [100, 0], [200, 0]]])
        == "M200,0C183.333,33.333,166.667,66.667,100,100C100,100,0,100,0,100C0,133.333,0,166.667,0,200"
    )
    assert (
        line([reflect(x) for x in [[0, 200], [100, 100], [200, 100], [200, 0]]])
        == "M200,0C150,33.333,100,66.667,100,100C100,133.333,100,166.667,100,200C100,200,0,200,0,200"
    )


def test_monotone_y_4():
    line = d3.line().set_curve(d3.curve_monotone_y)
    assert (
        line([reflect(x) for x in [[0, 200], [100, 150], [100, 50], [200, 0]]])
        == "M200,0C191.667,33.333,183.333,66.667,150,100C150,100,50,100,50,100C16.667,133.333,8.333,166.667,0,200"
    )
    assert (
        line([reflect(x) for x in [[200, 0], [100, 50], [100, 150], [0, 200]]])
        == "M0,200C8.333,166.667,16.667,133.333,50,100C50,100,150,100,150,100C183.333,66.667,191.667,33.333,200,0"
    )


def test_monotone_y_5():
    line = d3.line().set_curve(d3.curve_monotone_y)
    p = line(
        [reflect(x) for x in [[0, 200], [50, 200], [100, 100], [150, 0], [200, 0]]]
    )
    assert (
        line(
            [
                reflect(x)
                for x in [[0, 200], [0, 200], [50, 200], [100, 100], [150, 0], [200, 0]]
            ]
        )
        == p
    )
    assert (
        line(
            [
                reflect(x)
                for x in [
                    [0, 200],
                    [50, 200],
                    [50, 200],
                    [100, 100],
                    [150, 0],
                    [200, 0],
                ]
            ]
        )
        == p
    )
    assert (
        line(
            [
                reflect(x)
                for x in [
                    [0, 200],
                    [50, 200],
                    [100, 100],
                    [100, 100],
                    [150, 0],
                    [200, 0],
                ]
            ]
        )
        == p
    )
    assert (
        line(
            [
                reflect(x)
                for x in [[0, 200], [50, 200], [100, 100], [150, 0], [150, 0], [200, 0]]
            ]
        )
        == p
    )
    assert (
        line(
            [
                reflect(x)
                for x in [[0, 200], [50, 200], [100, 100], [150, 0], [200, 0], [200, 0]]
            ]
        )
        == p
    )


def test_monotone_y_6():
    area = d3.area().set_curve(d3.curve_monotone_y)
    assert area([reflect(x) for x in []]) is None
    assert area([reflect(x) for x in [[0, 1]]]) == "M1,0L1,0Z"
    assert area([reflect(x) for x in [[0, 1], [1, 3]]]) == "M1,0L3,1L3,0L1,0Z"
    assert (
        area([reflect(x) for x in [[0, 1], [1, 3], [2, 1]]])
        == "M1,0C2,0.333,3,0.667,3,1C3,1.333,2,1.667,1,2L1,0C1,0,3,0,3,0C3,0,1,0,1,0Z"
    )
    assert (
        area([reflect(x) for x in [[0, 1], [1, 3], [2, 1], [3, 3]]])
        == "M1,0C2,0.333,3,0.667,3,1C3,1.333,1,1.667,1,2C1,2.333,2,2.667,3,3L3,0C3,0,1,0,1,0C1,0,3,0,3,0C3,0,1,0,1,0Z"
    )
