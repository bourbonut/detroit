import detroit as d3


def test_point_1():
    s = d3.scale_point()
    assert s.domain == []
    assert s.range == [0, 1]
    assert s.bandwidth == 0
    assert s.step == 1
    assert s.round is False
    assert s.padding == 1
    assert s.align == 0.5


def test_point_2():
    s = d3.scale_point()
    assert s.padding_inner == 1
    assert s.padding_outer == 0


def test_point_3():
    p = d3.scale_point().set_domain(["foo", "bar"]).set_range([0, 960])
    b = (
        d3.scale_band()
        .set_domain(["foo", "bar"])
        .set_range([0, 960])
        .set_padding_inner(1)
    )
    assert list(map(p, p.domain)) == list(map(b, b.domain))
    assert p.bandwidth == b.bandwidth
    assert p.step == b.step


def test_point_4():
    p = d3.scale_point().set_domain(["foo", "bar"]).set_range([0, 960]).set_padding(0.5)
    b = (
        d3.scale_band()
        .set_domain(["foo", "bar"])
        .set_range([0, 960])
        .set_padding_inner(0.5)
        .set_padding_outer(0.5)
    )
    assert list(map(p, p.domain)) == list(map(b, b.domain))
    assert p.bandwidth == b.bandwidth
    assert p.step == b.step


def test_point_5():
    s = d3.scale_point()
    assert s.domain == []
    assert s.range == [0, 1]
    assert s.bandwidth == 0
    assert s.step == 1
    assert s.round is False
    assert s.padding == 1
    assert s.align == 0.5
