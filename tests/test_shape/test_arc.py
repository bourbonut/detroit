import detroit as d3
from math import pi, inf


def test_arc_1():
    expected = {"that": {}, "args": [42]}
    actual = {}

    def test_function(*args):
        actual["that"] = args[0]
        actual["args"] = args[1]
        return 0

    d3.arc().set_inner_radius(test_function)({}, [42])
    assert actual == expected


def test_arc_2():
    expected = {"that": {}, "args": [42]}
    actual = {}

    def test_function(*args):
        actual["that"] = args[0]
        actual["args"] = args[1]
        return 0

    d3.arc().set_outer_radius(test_function)({}, [42])
    assert actual == expected


def test_arc_3():
    expected = {"that": {}, "args": [42]}
    actual = {}

    def test_function(*args):
        actual["that"] = args[0]
        actual["args"] = args[1]
        return 0

    d3.arc().set_outer_radius(100).set_corner_radius(test_function)({}, [42])
    assert actual == expected


def test_arc_4():
    expected = {"that": {}, "args": [42]}
    actual = {}

    def test_function(*args):
        actual["that"] = args[0]
        actual["args"] = args[1]
        return 0

    d3.arc().set_start_angle(test_function)({}, [42])
    assert actual == expected


def test_arc_5():
    expected = {"that": {}, "args": [42]}
    actual = {}

    def test_function(*args):
        actual["that"] = args[0]
        actual["args"] = args[1]
        return 0

    d3.arc().set_end_angle(test_function)({}, [42])
    assert actual == expected


def test_arc_6():
    expected = {"that": {}, "args": [42]}
    actual = {}

    def test_function(*args):
        actual["that"] = args[0]
        actual["args"] = args[1]
        return 0

    d3.arc().set_outer_radius(100).set_start_angle(pi / 2).set_pad_angle(test_function)(
        {}, [42]
    )
    assert actual == expected


def test_arc_7():
    expected = {"that": {}, "args": [42]}
    actual = {}

    def test_function(*args):
        actual["that"] = args[0]
        actual["args"] = args[1]
        return 0

    d3.arc().set_outer_radius(100).set_start_angle(pi / 2).set_pad_angle(
        0.1
    ).set_pad_radius(test_function)({}, [42])
    assert actual == expected


def test_arc_8():
    a = d3.arc()
    local_round = lambda x: round(x * 1e6) / 1e6
    assert list(
        map(
            local_round,
            a.set_inner_radius(0)
            .set_outer_radius(100)
            .set_start_angle(0)
            .set_end_angle(pi)
            .centroid(),
        )
    ) == [50, 0]
    assert list(
        map(
            local_round,
            a.set_inner_radius(0)
            .set_outer_radius(100)
            .set_start_angle(0)
            .set_end_angle(pi / 2)
            .centroid(),
        )
    ) == [35.355339, -35.355339]
    assert list(
        map(
            local_round,
            a.set_inner_radius(50)
            .set_outer_radius(100)
            .set_start_angle(0)
            .set_end_angle(-pi)
            .centroid(),
        )
    ) == [-75, -0]
    assert list(
        map(
            local_round,
            a.set_inner_radius(50)
            .set_outer_radius(100)
            .set_start_angle(0)
            .set_end_angle(-pi / 2)
            .centroid(),
        )
    ) == [-53.033009, -53.033009]


def test_arc_9():
    expected = {"that": {}, "args": [42]}
    actual = {}

    def test_function(*args):
        actual["that"] = args[0]
        actual["args"] = args[1]
        return 0

    d3.arc().set_inner_radius(test_function)({}, [42])
    assert actual == expected


def test_arc_10():
    expected = {"that": {}, "args": [42]}
    actual = {}

    def test_function(*args):
        actual["that"] = args[0]
        actual["args"] = args[1]
        return 0

    d3.arc().set_outer_radius(test_function)({}, [42])
    assert actual == expected


def test_arc_11():
    expected = {"that": {}, "args": [42]}
    actual = {}

    def test_function(*args):
        actual["that"] = args[0]
        actual["args"] = args[1]
        return 0

    d3.arc().set_start_angle(test_function)({}, [42])
    assert actual == expected


def test_arc_12():
    expected = {"that": {}, "args": [42]}
    actual = {}

    def test_function(*args):
        actual["that"] = args[0]
        actual["args"] = args[1]
        return 0

    d3.arc().set_end_angle(test_function)({}, [42])
    assert actual == expected


def test_arc_13():
    a = d3.arc().set_inner_radius(0).set_outer_radius(0)
    assert a.set_start_angle(0).set_end_angle(2 * pi)() == "M0,0Z"
    assert a.set_start_angle(0).set_end_angle(0)() == "M0,0Z"


def test_arc_14():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(-pi / 2)()
        == "M0,-100A100,100,0,0,0,-100,0L0,0Z"
    )


def test_arc_15():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(2 * pi)()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100Z"
    )
    assert (
        a.set_start_angle(0).set_end_angle(3 * pi)()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100Z"
    )
    assert (
        a.set_start_angle(-2 * pi).set_end_angle(0)()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100Z"
    )
    assert (
        a.set_start_angle(-pi).set_end_angle(pi)()
        == "M0,100A100,100,0,1,1,0,-100A100,100,0,1,1,0,100Z"
    )
    assert (
        a.set_start_angle(-3 * pi).set_end_angle(0)()
        == "M0,100A100,100,0,1,1,0,-100A100,100,0,1,1,0,100Z"
    )


def test_arc_16():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(-2 * pi)()
        == "M0,-100A100,100,0,1,0,0,100A100,100,0,1,0,0,-100Z"
    )
    assert (
        a.set_start_angle(0).set_end_angle(-3 * pi)()
        == "M0,-100A100,100,0,1,0,0,100A100,100,0,1,0,0,-100Z"
    )
    assert (
        a.set_start_angle(2 * pi).set_end_angle(0)()
        == "M0,-100A100,100,0,1,0,0,100A100,100,0,1,0,0,-100Z"
    )
    assert (
        a.set_start_angle(pi).set_end_angle(-pi)()
        == "M0,100A100,100,0,1,0,0,-100A100,100,0,1,0,0,100Z"
    )
    assert (
        a.set_start_angle(3 * pi).set_end_angle(0)()
        == "M0,100A100,100,0,1,0,0,-100A100,100,0,1,0,0,100Z"
    )


def test_arc_17():
    a = d3.arc().set_inner_radius(50).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(2 * pi)()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100M0,-50A50,50,0,1,0,0,50A50,50,0,1,0,0,-50Z"
    )
    assert (
        a.set_start_angle(0).set_end_angle(3 * pi)()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100M0,50A50,50,0,1,0,0,-50A50,50,0,1,0,0,50Z"
    )
    assert (
        a.set_start_angle(-2 * pi).set_end_angle(0)()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100M0,-50A50,50,0,1,0,0,50A50,50,0,1,0,0,-50Z"
    )
    assert (
        a.set_start_angle(-pi).set_end_angle(pi)()
        == "M0,100A100,100,0,1,1,0,-100A100,100,0,1,1,0,100M0,50A50,50,0,1,0,0,-50A50,50,0,1,0,0,50Z"
    )
    assert (
        a.set_start_angle(-3 * pi).set_end_angle(0)()
        == "M0,100A100,100,0,1,1,0,-100A100,100,0,1,1,0,100M0,-50A50,50,0,1,0,0,50A50,50,0,1,0,0,-50Z"
    )


def test_arc_18():
    a = d3.arc().set_inner_radius(50).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(-2 * pi)()
        == "M0,-100A100,100,0,1,0,0,100A100,100,0,1,0,0,-100M0,-50A50,50,0,1,1,0,50A50,50,0,1,1,0,-50Z"
    )
    assert (
        a.set_start_angle(0).set_end_angle(-3 * pi)()
        == "M0,-100A100,100,0,1,0,0,100A100,100,0,1,0,0,-100M0,50A50,50,0,1,1,0,-50A50,50,0,1,1,0,50Z"
    )
    assert (
        a.set_start_angle(2 * pi).set_end_angle(0)()
        == "M0,-100A100,100,0,1,0,0,100A100,100,0,1,0,0,-100M0,-50A50,50,0,1,1,0,50A50,50,0,1,1,0,-50Z"
    )
    assert (
        a.set_start_angle(pi).set_end_angle(-pi)()
        == "M0,100A100,100,0,1,0,0,-100A100,100,0,1,0,0,100M0,50A50,50,0,1,1,0,-50A50,50,0,1,1,0,50Z"
    )
    assert (
        a.set_start_angle(3 * pi).set_end_angle(0)()
        == "M0,100A100,100,0,1,0,0,-100A100,100,0,1,0,0,100M0,-50A50,50,0,1,1,0,50A50,50,0,1,1,0,-50Z"
    )


def test_arc_19():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(pi / 2)()
        == "M0,-100A100,100,0,0,1,100,0L0,0Z"
    )
    assert (
        a.set_start_angle(2 * pi).set_end_angle(5 * pi / 2)()
        == "M0,-100A100,100,0,0,1,100,0L0,0Z"
    )
    assert (
        a.set_start_angle(-pi).set_end_angle(-pi / 2)()
        == "M0,100A100,100,0,0,1,-100,0L0,0Z"
    )


def test_arc_20():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(-pi / 2)()
        == "M0,-100A100,100,0,0,0,-100,0L0,0Z"
    )
    assert (
        a.set_start_angle(-2 * pi).set_end_angle(-5 * pi / 2)()
        == "M0,-100A100,100,0,0,0,-100,0L0,0Z"
    )
    assert (
        a.set_start_angle(pi).set_end_angle(pi / 2)()
        == "M0,100A100,100,0,0,0,100,0L0,0Z"
    )


def test_arc_21():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(3 * pi / 2)()
        == "M0,-100A100,100,0,1,1,-100,0L0,0Z"
    )
    assert (
        a.set_start_angle(2 * pi).set_end_angle(7 * pi / 2)()
        == "M0,-100A100,100,0,1,1,-100,0L0,0Z"
    )
    assert (
        a.set_start_angle(-pi).set_end_angle(pi / 2)()
        == "M0,100A100,100,0,1,1,100,0L0,0Z"
    )


def test_arc_22():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(-3 * pi / 2)()
        == "M0,-100A100,100,0,1,0,100,0L0,0Z"
    )
    assert (
        a.set_start_angle(-2 * pi).set_end_angle(-7 * pi / 2)()
        == "M0,-100A100,100,0,1,0,100,0L0,0Z"
    )
    assert (
        a.set_start_angle(pi).set_end_angle(-pi / 2)()
        == "M0,100A100,100,0,1,0,-100,0L0,0Z"
    )


def test_arc_23():
    a = d3.arc().set_inner_radius(50).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(pi / 2)()
        == "M0,-100A100,100,0,0,1,100,0L50,0A50,50,0,0,0,0,-50Z"
    )
    assert (
        a.set_start_angle(2 * pi).set_end_angle(5 * pi / 2)()
        == "M0,-100A100,100,0,0,1,100,0L50,0A50,50,0,0,0,0,-50Z"
    )
    assert (
        a.set_start_angle(-pi).set_end_angle(-pi / 2)()
        == "M0,100A100,100,0,0,1,-100,0L-50,0A50,50,0,0,0,0,50Z"
    )


def test_arc_24():
    a = d3.arc().set_inner_radius(50).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(-pi / 2)()
        == "M0,-100A100,100,0,0,0,-100,0L-50,0A50,50,0,0,1,0,-50Z"
    )
    assert (
        a.set_start_angle(-2 * pi).set_end_angle(-5 * pi / 2)()
        == "M0,-100A100,100,0,0,0,-100,0L-50,0A50,50,0,0,1,0,-50Z"
    )
    assert (
        a.set_start_angle(pi).set_end_angle(pi / 2)()
        == "M0,100A100,100,0,0,0,100,0L50,0A50,50,0,0,1,0,50Z"
    )


def test_arc_25():
    a = d3.arc().set_inner_radius(50).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(3 * pi / 2)()
        == "M0,-100A100,100,0,1,1,-100,0L-50,0A50,50,0,1,0,0,-50Z"
    )
    assert (
        a.set_start_angle(2 * pi).set_end_angle(7 * pi / 2)()
        == "M0,-100A100,100,0,1,1,-100,0L-50,0A50,50,0,1,0,0,-50Z"
    )
    assert (
        a.set_start_angle(-pi).set_end_angle(pi / 2)()
        == "M0,100A100,100,0,1,1,100,0L50,0A50,50,0,1,0,0,50Z"
    )


def test_arc_26():
    a = d3.arc().set_inner_radius(50).set_outer_radius(100)
    assert (
        a.set_start_angle(0).set_end_angle(-3 * pi / 2)()
        == "M0,-100A100,100,0,1,0,100,0L50,0A50,50,0,1,1,0,-50Z"
    )
    assert (
        a.set_start_angle(-2 * pi).set_end_angle(-7 * pi / 2)()
        == "M0,-100A100,100,0,1,0,100,0L50,0A50,50,0,1,1,0,-50Z"
    )
    assert (
        a.set_start_angle(pi).set_end_angle(-pi / 2)()
        == "M0,100A100,100,0,1,0,-100,0L-50,0A50,50,0,1,1,0,50Z"
    )


def test_arc_27():
    a = d3.arc().set_inner_radius(0).set_outer_radius(0).set_corner_radius(5)
    assert a.set_start_angle(0).set_end_angle(2 * pi)() == "M0,0Z"
    assert a.set_start_angle(0).set_end_angle(0)() == "M0,0Z"


def test_arc_28():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100).set_corner_radius(5)
    assert (
        a.set_start_angle(0).set_end_angle(2 * pi)()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100Z"
    )
    assert (
        a.set_start_angle(0).set_end_angle(3 * pi)()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100Z"
    )
    assert (
        a.set_start_angle(-2 * pi).set_end_angle(0)()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100Z"
    )
    assert (
        a.set_start_angle(-pi).set_end_angle(pi)()
        == "M0,100A100,100,0,1,1,0,-100A100,100,0,1,1,0,100Z"
    )
    assert (
        a.set_start_angle(-3 * pi).set_end_angle(0)()
        == "M0,100A100,100,0,1,1,0,-100A100,100,0,1,1,0,100Z"
    )


def test_arc_29():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100).set_corner_radius(5)
    assert (
        a.set_start_angle(0).set_end_angle(-2 * pi)()
        == "M0,-100A100,100,0,1,0,0,100A100,100,0,1,0,0,-100Z"
    )
    assert (
        a.set_start_angle(0).set_end_angle(-3 * pi)()
        == "M0,-100A100,100,0,1,0,0,100A100,100,0,1,0,0,-100Z"
    )
    assert (
        a.set_start_angle(2 * pi).set_end_angle(0)()
        == "M0,-100A100,100,0,1,0,0,100A100,100,0,1,0,0,-100Z"
    )
    assert (
        a.set_start_angle(pi).set_end_angle(-pi)()
        == "M0,100A100,100,0,1,0,0,-100A100,100,0,1,0,0,100Z"
    )
    assert (
        a.set_start_angle(3 * pi).set_end_angle(0)()
        == "M0,100A100,100,0,1,0,0,-100A100,100,0,1,0,0,100Z"
    )


def test_arc_30():
    a = d3.arc().set_inner_radius(50).set_outer_radius(100).set_corner_radius(5)
    assert (
        a.set_start_angle(0).set_end_angle(2 * pi)()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100M0,-50A50,50,0,1,0,0,50A50,50,0,1,0,0,-50Z"
    )
    assert (
        a.set_start_angle(0).set_end_angle(3 * pi)()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100M0,50A50,50,0,1,0,0,-50A50,50,0,1,0,0,50Z"
    )
    assert (
        a.set_start_angle(-2 * pi).set_end_angle(0)()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100M0,-50A50,50,0,1,0,0,50A50,50,0,1,0,0,-50Z"
    )
    assert (
        a.set_start_angle(-pi).set_end_angle(pi)()
        == "M0,100A100,100,0,1,1,0,-100A100,100,0,1,1,0,100M0,50A50,50,0,1,0,0,-50A50,50,0,1,0,0,50Z"
    )
    assert (
        a.set_start_angle(-3 * pi).set_end_angle(0)()
        == "M0,100A100,100,0,1,1,0,-100A100,100,0,1,1,0,100M0,-50A50,50,0,1,0,0,50A50,50,0,1,0,0,-50Z"
    )


def test_arc_31():
    a = d3.arc().set_inner_radius(50).set_outer_radius(100).set_corner_radius(5)
    assert (
        a.set_start_angle(0).set_end_angle(-2 * pi)()
        == "M0,-100A100,100,0,1,0,0,100A100,100,0,1,0,0,-100M0,-50A50,50,0,1,1,0,50A50,50,0,1,1,0,-50Z"
    )
    assert (
        a.set_start_angle(0).set_end_angle(-3 * pi)()
        == "M0,-100A100,100,0,1,0,0,100A100,100,0,1,0,0,-100M0,50A50,50,0,1,1,0,-50A50,50,0,1,1,0,50Z"
    )
    assert (
        a.set_start_angle(2 * pi).set_end_angle(0)()
        == "M0,-100A100,100,0,1,0,0,100A100,100,0,1,0,0,-100M0,-50A50,50,0,1,1,0,50A50,50,0,1,1,0,-50Z"
    )
    assert (
        a.set_start_angle(pi).set_end_angle(-pi)()
        == "M0,100A100,100,0,1,0,0,-100A100,100,0,1,0,0,100M0,50A50,50,0,1,1,0,-50A50,50,0,1,1,0,50Z"
    )
    assert (
        a.set_start_angle(3 * pi).set_end_angle(0)()
        == "M0,100A100,100,0,1,0,0,-100A100,100,0,1,0,0,100M0,-50A50,50,0,1,1,0,50A50,50,0,1,1,0,-50Z"
    )


def test_arc_32():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100).set_corner_radius(5)
    assert (
        a.set_start_angle(0).set_end_angle(pi / 2).digits(6)()
        == "M0,-94.868330A5,5,0,0,1,5.263158,-99.861400A100,100,0,0,1,99.861400,-5.263158A5,5,0,0,1,94.868330,0L0,0Z"
    )
    assert (
        a.set_start_angle(2 * pi).set_end_angle(5 * pi / 2)()
        == "M0,-94.868330A5,5,0,0,1,5.263158,-99.861400A100,100,0,0,1,99.861400,-5.263158A5,5,0,0,1,94.868330,0L0,0Z"
    )
    assert (
        a.set_start_angle(-pi).set_end_angle(-pi / 2)()
        == "M0,94.868330A5,5,0,0,1,-5.263158,99.861400A100,100,0,0,1,-99.861400,5.263158A5,5,0,0,1,-94.868330,0L0,0Z"
    )


def test_arc_33():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100).set_corner_radius(5)
    assert (
        a.set_start_angle(0).set_end_angle(-pi / 2).digits(6)()
        == "M0,-94.868330A5,5,0,0,0,-5.263158,-99.861400A100,100,0,0,0,-99.861400,-5.263158A5,5,0,0,0,-94.868330,0L0,0Z"
    )
    assert (
        a.set_start_angle(-2 * pi).set_end_angle(-5 * pi / 2)()
        == "M0,-94.868330A5,5,0,0,0,-5.263158,-99.861400A100,100,0,0,0,-99.861400,-5.263158A5,5,0,0,0,-94.868330,0L0,0Z"
    )
    assert (
        a.set_start_angle(pi).set_end_angle(pi / 2)()
        == "M0,94.868330A5,5,0,0,0,5.263158,99.861400A100,100,0,0,0,99.861400,5.263158A5,5,0,0,0,94.868330,0L0,0Z"
    )


def test_arc_34():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100).set_corner_radius(5)
    assert (
        a.set_start_angle(0).set_end_angle(3 * pi / 2).digits(6)()
        == "M0,-94.868330A5,5,0,0,1,5.263158,-99.861400A100,100,0,1,1,-99.861400,5.263158A5,5,0,0,1,-94.868330,0L0,0Z"
    )
    assert (
        a.set_start_angle(2 * pi).set_end_angle(7 * pi / 2)()
        == "M0,-94.868330A5,5,0,0,1,5.263158,-99.861400A100,100,0,1,1,-99.861400,5.263158A5,5,0,0,1,-94.868330,0L0,0Z"
    )
    assert (
        a.set_start_angle(-pi).set_end_angle(pi / 2)()
        == "M0,94.868330A5,5,0,0,1,-5.263158,99.861400A100,100,0,1,1,99.861400,-5.263158A5,5,0,0,1,94.868330,0L0,0Z"
    )


def test_arc_35():
    a = d3.arc().set_inner_radius(0).set_outer_radius(100).set_corner_radius(5)
    assert (
        a.set_start_angle(0).set_end_angle(-3 * pi / 2).digits(6)()
        == "M0,-94.868330A5,5,0,0,0,-5.263158,-99.861400A100,100,0,1,0,99.861400,5.263158A5,5,0,0,0,94.868330,0L0,0Z"
    )
    assert (
        a.set_start_angle(-2 * pi).set_end_angle(-7 * pi / 2)()
        == "M0,-94.868330A5,5,0,0,0,-5.263158,-99.861400A100,100,0,1,0,99.861400,5.263158A5,5,0,0,0,94.868330,0L0,0Z"
    )
    assert (
        a.set_start_angle(pi).set_end_angle(-pi / 2)()
        == "M0,94.868330A5,5,0,0,0,5.263158,99.861400A100,100,0,1,0,-99.861400,-5.263158A5,5,0,0,0,-94.868330,0L0,0Z"
    )


def test_arc_36():
    a = d3.arc().set_inner_radius(50).set_outer_radius(100).set_corner_radius(5)
    assert (
        a.set_start_angle(0).set_end_angle(pi / 2).digits(6)()
        == "M0,-94.868330A5,5,0,0,1,5.263158,-99.861400A100,100,0,0,1,99.861400,-5.263158A5,5,0,0,1,94.868330,0L54.772256,0A5,5,0,0,1,49.792960,-4.545455A50,50,0,0,0,4.545455,-49.792960A5,5,0,0,1,0,-54.772256Z"
    )
    assert (
        a.set_start_angle(2 * pi).set_end_angle(5 * pi / 2)()
        == "M0,-94.868330A5,5,0,0,1,5.263158,-99.861400A100,100,0,0,1,99.861400,-5.263158A5,5,0,0,1,94.868330,0L54.772256,0A5,5,0,0,1,49.792960,-4.545455A50,50,0,0,0,4.545455,-49.792960A5,5,0,0,1,0,-54.772256Z"
    )
    assert (
        a.set_start_angle(-pi).set_end_angle(-pi / 2)()
        == "M0,94.868330A5,5,0,0,1,-5.263158,99.861400A100,100,0,0,1,-99.861400,5.263158A5,5,0,0,1,-94.868330,0L-54.772256,0A5,5,0,0,1,-49.792960,4.545455A50,50,0,0,0,-4.545455,49.792960A5,5,0,0,1,0,54.772256Z"
    )


def test_arc_37():
    a = d3.arc().set_inner_radius(50).set_outer_radius(100).set_corner_radius(5)
    assert (
        a.set_start_angle(0).set_end_angle(-pi / 2).digits(6)()
        == "M0,-94.868330A5,5,0,0,0,-5.263158,-99.861400A100,100,0,0,0,-99.861400,-5.263158A5,5,0,0,0,-94.868330,0L-54.772256,0A5,5,0,0,0,-49.792960,-4.545455A50,50,0,0,1,-4.545455,-49.792960A5,5,0,0,0,0,-54.772256Z"
    )
    assert (
        a.set_start_angle(-2 * pi).set_end_angle(-5 * pi / 2)()
        == "M0,-94.868330A5,5,0,0,0,-5.263158,-99.861400A100,100,0,0,0,-99.861400,-5.263158A5,5,0,0,0,-94.868330,0L-54.772256,0A5,5,0,0,0,-49.792960,-4.545455A50,50,0,0,1,-4.545455,-49.792960A5,5,0,0,0,0,-54.772256Z"
    )
    assert (
        a.set_start_angle(pi).set_end_angle(pi / 2)()
        == "M0,94.868330A5,5,0,0,0,5.263158,99.861400A100,100,0,0,0,99.861400,5.263158A5,5,0,0,0,94.868330,0L54.772256,0A5,5,0,0,0,49.792960,4.545455A50,50,0,0,1,4.545455,49.792960A5,5,0,0,0,0,54.772256Z"
    )


def test_arc_38():
    a = d3.arc().set_inner_radius(50).set_outer_radius(100).set_corner_radius(5)
    assert (
        a.set_start_angle(0).set_end_angle(3 * pi / 2).digits(6)()
        == "M0,-94.868330A5,5,0,0,1,5.263158,-99.861400A100,100,0,1,1,-99.861400,5.263158A5,5,0,0,1,-94.868330,0L-54.772256,0A5,5,0,0,1,-49.792960,4.545455A50,50,0,1,0,4.545455,-49.792960A5,5,0,0,1,0,-54.772256Z"
    )
    assert (
        a.set_start_angle(2 * pi).set_end_angle(7 * pi / 2)()
        == "M0,-94.868330A5,5,0,0,1,5.263158,-99.861400A100,100,0,1,1,-99.861400,5.263158A5,5,0,0,1,-94.868330,0L-54.772256,0A5,5,0,0,1,-49.792960,4.545455A50,50,0,1,0,4.545455,-49.792960A5,5,0,0,1,0,-54.772256Z"
    )
    assert (
        a.set_start_angle(-pi).set_end_angle(pi / 2)()
        == "M0,94.868330A5,5,0,0,1,-5.263158,99.861400A100,100,0,1,1,99.861400,-5.263158A5,5,0,0,1,94.868330,0L54.772256,0A5,5,0,0,1,49.792960,-4.545455A50,50,0,1,0,-4.545455,49.792960A5,5,0,0,1,0,54.772256Z"
    )


def test_arc_39():
    a = d3.arc().set_inner_radius(50).set_outer_radius(100).set_corner_radius(5)
    assert (
        a.set_start_angle(0).set_end_angle(-3 * pi / 2).digits(6)()
        == "M0,-94.868330A5,5,0,0,0,-5.263158,-99.861400A100,100,0,1,0,99.861400,5.263158A5,5,0,0,0,94.868330,0L54.772256,0A5,5,0,0,0,49.792960,4.545455A50,50,0,1,1,-4.545455,-49.792960A5,5,0,0,0,0,-54.772256Z"
    )
    assert (
        a.set_start_angle(-2 * pi).set_end_angle(-7 * pi / 2)()
        == "M0,-94.868330A5,5,0,0,0,-5.263158,-99.861400A100,100,0,1,0,99.861400,5.263158A5,5,0,0,0,94.868330,0L54.772256,0A5,5,0,0,0,49.792960,4.545455A50,50,0,1,1,-4.545455,-49.792960A5,5,0,0,0,0,-54.772256Z"
    )
    assert (
        a.set_start_angle(pi).set_end_angle(-pi / 2)()
        == "M0,94.868330A5,5,0,0,0,5.263158,99.861400A100,100,0,1,0,-99.861400,-5.263158A5,5,0,0,0,-94.868330,0L-54.772256,0A5,5,0,0,0,-49.792960,-4.545455A50,50,0,1,1,4.545455,49.792960A5,5,0,0,0,0,54.772256Z"
    )


def test_arc_40():
    a = d3.arc().set_corner_radius(inf).set_start_angle(0).set_end_angle(pi / 2)
    assert (
        a.set_inner_radius(90).set_outer_radius(100).digits(6)()
        == "M0,-94.868330A5,5,0,0,1,5.263158,-99.861400A100,100,0,0,1,99.861400,-5.263158A5,5,0,0,1,94.868330,0L94.868330,0A5,5,0,0,1,89.875260,-4.736842A90,90,0,0,0,4.736842,-89.875260A5,5,0,0,1,0,-94.868330Z"
    )
    assert (
        a.set_inner_radius(100).set_outer_radius(90)()
        == "M0,-94.868330A5,5,0,0,1,5.263158,-99.861400A100,100,0,0,1,99.861400,-5.263158A5,5,0,0,1,94.868330,0L94.868330,0A5,5,0,0,1,89.875260,-4.736842A90,90,0,0,0,4.736842,-89.875260A5,5,0,0,1,0,-94.868330Z"
    )


def test_arc_41():
    a = d3.arc().set_corner_radius(inf).set_start_angle(0).set_end_angle(pi / 2)
    assert (
        a.set_inner_radius(10).set_outer_radius(100).digits(6)()
        == "M0,-41.421356A41.421356,41.421356,0,1,1,41.421356,0L24.142136,0A24.142136,24.142136,0,0,1,0,-24.142136Z"
    )
    assert (
        a.set_inner_radius(100).set_outer_radius(10)()
        == "M0,-41.421356A41.421356,41.421356,0,1,1,41.421356,0L24.142136,0A24.142136,24.142136,0,0,1,0,-24.142136Z"
    )


def test_arc_42():
    a = (
        d3.arc()
        .set_inner_radius(0)
        .set_outer_radius(0)
        .set_start_angle(0)
        .set_end_angle(2 * pi)
        .set_pad_angle(0.1)
    )
    assert a() == "M0,0Z"


def test_arc_43():
    a = (
        d3.arc()
        .set_inner_radius(0)
        .set_outer_radius(100)
        .set_start_angle(0)
        .set_end_angle(2 * pi)
        .set_pad_angle(0.1)
    )
    assert a() == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100Z"


def test_arc_44():
    a = (
        d3.arc()
        .set_inner_radius(50)
        .set_outer_radius(100)
        .set_start_angle(0)
        .set_end_angle(2 * pi)
        .set_pad_angle(0.1)
    )
    assert (
        a()
        == "M0,-100A100,100,0,1,1,0,100A100,100,0,1,1,0,-100M0,-50A50,50,0,1,0,0,50A50,50,0,1,0,0,-50Z"
    )


def test_arc_45():
    a = (
        d3.arc()
        .set_inner_radius(0)
        .set_outer_radius(100)
        .set_start_angle(0)
        .set_end_angle(pi / 2)
        .set_pad_angle(0.1)
        .digits(6)
    )
    assert a() == "M4.997917,-99.875026A100,100,0,0,1,99.875026,-4.997917L0,0Z"


def test_arc_46():
    a = (
        d3.arc()
        .set_inner_radius(50)
        .set_outer_radius(100)
        .set_start_angle(0)
        .set_end_angle(pi / 2)
        .set_pad_angle(0.1)
        .digits(6)
    )
    assert (
        a()
        == "M5.587841,-99.843758A100,100,0,0,1,99.843758,-5.587841L49.686779,-5.587841A50,50,0,0,0,5.587841,-49.686779Z"
    )


def test_arc_47():
    a = (
        d3.arc()
        .set_inner_radius(10)
        .set_outer_radius(100)
        .set_start_angle(0)
        .set_end_angle(pi / 2)
        .set_pad_angle(0.2)
        .digits(6)
    )
    assert (
        a()
        == "M10.033134,-99.495408A100,100,0,0,1,99.495408,-10.033134L7.071068,-7.071068Z"
    )


def test_arc_48():
    a = (
        d3.arc()
        .set_inner_radius(0)
        .set_outer_radius(100)
        .set_start_angle(0)
        .set_end_angle(pi / 2)
        .set_pad_angle(0.1)
        .set_corner_radius(10)
        .digits(6)
    )
    assert (
        a()
        == "M4.470273,-89.330939A10,10,0,0,1,16.064195,-98.701275A100,100,0,0,1,98.701275,-16.064195A10,10,0,0,1,89.330939,-4.470273L0,0Z"
    )


def test_arc_49():
    a = (
        d3.arc()
        .set_inner_radius(50)
        .set_outer_radius(100)
        .set_start_angle(0)
        .set_end_angle(pi / 2)
        .set_pad_angle(0.1)
        .set_corner_radius(10)
        .digits(6)
    )
    assert (
        a()
        == "M5.587841,-88.639829A10,10,0,0,1,17.319823,-98.488698A100,100,0,0,1,98.488698,-17.319823A10,10,0,0,1,88.639829,-5.587841L57.939790,-5.587841A10,10,0,0,1,48.283158,-12.989867A50,50,0,0,0,12.989867,-48.283158A10,10,0,0,1,5.587841,-57.939790Z"
    )


def test_arc_50():
    a = (
        d3.arc()
        .set_inner_radius(10)
        .set_outer_radius(100)
        .set_start_angle(0)
        .set_end_angle(pi / 2)
        .set_pad_angle(0.2)
        .set_corner_radius(10)
        .digits(6)
    )
    assert (
        a()
        == "M9.669396,-88.145811A10,10,0,0,1,21.849183,-97.583878A100,100,0,0,1,97.583878,-21.849183A10,10,0,0,1,88.145811,-9.669396L7.071068,-7.071068Z"
    )


def test_arc_51():
    a = (
        d3.arc()
        .set_inner_radius(15)
        .set_outer_radius(24)
        .set_pad_angle(0)
        .set_start_angle(1.2 - 1e-8)
        .set_end_angle(1.2)
        .set_corner_radius(4)
    )
    assert a() == "M22.369,-8.697L13.981,-5.435Z"
