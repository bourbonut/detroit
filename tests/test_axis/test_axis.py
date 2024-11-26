import detroit as d3


def test_axis_1():
    s = d3.scale_linear()
    a = d3.axis_left(s)
    assert a.scale == s
    assert a.tick_arguments == []
    assert a.tick_values is None
    assert a.tick_format is None
    assert a.tick_size_inner == 6
    assert a.tick_size_outer == 6
    assert a.tick_padding == 3


def test_axis_2():
    a = d3.axis_left(d3.scale_linear()).set_ticks(20)
    assert a.tick_arguments == [20]
    a.set_ticks()
    assert a.tick_arguments == []


def test_axis_3():
    a = d3.axis_left(d3.scale_linear()).set_tick_arguments([])
    assert a.tick_arguments == []


def test_axis_4():
    a = d3.axis_left(d3.scale_linear()).set_tick_arguments([20])
    v = a.tick_arguments
    v.append(10)
    assert a.tick_arguments == [20]


def test_axis_5():
    a = d3.axis_left(d3.scale_linear()).set_tick_values([1, 2, 3])
    assert a.tick_values == [1, 2, 3]
    a.set_tick_values([])
    assert a.tick_values == []


def test_axis_6():
    a = d3.axis_left(d3.scale_linear()).set_tick_values([1, 2, 3])
    assert a.tick_values == [1, 2, 3]


def test_axis_7():
    v = [1, 2, 3]
    a = d3.axis_left(d3.scale_linear()).set_tick_values(v)
    v.append(4)
    assert a.tick_values == [1, 2, 3, 4]


def test_axis_8():
    a = d3.axis_left(d3.scale_linear()).set_tick_values([1, 2, 3])
    v = a.tick_values
    v.append(4)
    assert a.tick_values == [1, 2, 3, 4]


def test_axis_9():
    a = d3.axis_left(d3.scale_linear()).set_tick_values({1, 2, 3})
    assert a.tick_values == {1, 2, 3}
