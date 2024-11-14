import detroit as d3

def test_point_1():
    s = d3.scale_point()
    assert s.domain() == []
    assert s.range() == [0, 1]
    assert s.bandwidth() == 0
    assert s.step() == 1
    assert s.round() is False
    assert s.padding() == 0
    assert s.align() == 0.5

def test_point_2():
    s = d3.scale_point()
    assert s.paddingInner is None
    assert s.paddingOuter is None

def test_point_3():
    p = d3.scale_point().domain(["foo", "bar"]).range([0, 960])
    b = d3.scale_band().domain(["foo", "bar"]).range([0, 960]).paddingInner(1)
    assert p.domain().map(p) == b.domain().map(b)
    assert p.bandwidth() == b.bandwidth()
    assert p.step() == b.step()

def test_point_4():
    p = d3.scale_point().domain(["foo", "bar"]).range([0, 960]).padding(0.5)
    b = d3.scale_band().domain(["foo", "bar"]).range([0, 960]).paddingInner(1).paddingOuter(0.5)
    assert p.domain().map(p) == b.domain().map(b)
    assert p.bandwidth() == b.bandwidth()
    assert p.step() == b.step()

def test_point_5():
    s = d3.scale_point()
    assert s.domain() == []
    assert s.range() == [0, 1]
    assert s.bandwidth() == 0
    assert s.step() == 1
    assert s.round() is False
    assert s.padding() == 0
    assert s.align() == 0.5
