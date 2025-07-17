import detroit as d3


def test_catmull_rom_1():
    line = d3.line().curve(d3.curve_catmull_rom)
    assert line([]) is None
    assert line([[0, 1]]) == "M0,1Z"
    assert line([[0, 1], [1, 3]]) == "M0,1L1,3"
    assert line([[0, 1], [1, 3], [2, 1]]) == "M0,1C0,1,0.667,3,1,3C1.333,3,2,1,2,1"
    assert (
        line([[0, 1], [1, 3], [2, 1], [3, 3]])
        == "M0,1C0,1,0.667,3,1,3C1.333,3,1.667,1,2,1C2.333,1,3,3,3,3"
    )


def test_catmull_rom_2():
    line = d3.line().curve(d3.curve_catmull_rom(1))
    assert line([]) is None
    assert line([[0, 1]]) == "M0,1Z"
    assert line([[0, 1], [1, 3]]) == "M0,1L1,3"
    assert line([[0, 1], [1, 3], [2, 1]]) == "M0,1C0,1,0.667,3,1,3C1.333,3,2,1,2,1"
    assert (
        line([[0, 1], [1, 3], [2, 1], [3, 3]])
        == "M0,1C0,1,0.667,3,1,3C1.333,3,1.667,1,2,1C2.333,1,3,3,3,3"
    )


def test_catmull_rom_3():
    line = d3.line().curve(d3.curve_catmull_rom(0.5))
    assert d3.line().curve(d3.curve_catmull_rom)(
        [[0, 1], [1, 3], [2, 1], [3, 3]]
    ) == line([[0, 1], [1, 3], [2, 1], [3, 3]])


def test_catmull_rom_4():
    line = d3.line().curve(d3.curve_catmull_rom(0.5))
    assert d3.line().curve(d3.curve_catmull_rom(0.5))(
        [[0, 1], [1, 3], [2, 1], [3, 3]]
    ) == line([[0, 1], [1, 3], [2, 1], [3, 3]])


def test_catmull_rom_5():
    a = d3.area().curve(d3.curve_catmull_rom(0))
    assert a([]) is None
    assert a([[0, 1]]) == "M0,1L0,0Z"
    assert a([[0, 1], [1, 3]]) == "M0,1L1,3L1,0L0,0Z"
    assert (
        a([[0, 1], [1, 3], [2, 1]])
        == "M0,1C0,1,0.667,3,1,3C1.333,3,2,1,2,1L2,0C2,0,1.333,0,1,0C0.667,0,0,0,0,0Z"
    )
    assert (
        a([[0, 1], [1, 3], [2, 1], [3, 3]])
        == "M0,1C0,1,0.667,3,1,3C1.333,3,1.667,1,2,1C2.333,1,3,3,3,3L3,0C3,0,2.333,0,2,0C1.667,0,1.333,0,1,0C0.667,0,0,0,0,0Z"
    )


def test_catmull_rom_6():
    area = d3.area().curve(d3.curve_catmull_rom(0.5))
    assert d3.area().curve(d3.curve_catmull_rom)(
        [[0, 1], [1, 3], [2, 1], [3, 3]]
    ) == area([[0, 1], [1, 3], [2, 1], [3, 3]])


def test_catmull_rom_7():
    area = d3.area().curve(d3.curve_catmull_rom(0.5))
    assert d3.area().curve(d3.curve_catmull_rom(0.5))(
        [[0, 1], [1, 3], [2, 1], [3, 3]]
    ) == area([[0, 1], [1, 3], [2, 1], [3, 3]])
