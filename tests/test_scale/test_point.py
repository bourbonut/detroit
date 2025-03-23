import detroit as d3


def test_point_1():
    s = d3.scale_point()
    assert s.get_domain() == []
    assert s.get_range() == [0, 1]
    assert s.get_bandwidth() == 0
    assert s.get_step() == 1
    assert s.get_round() is False
    assert s.get_padding() == 1
    assert s.get_align() == 0.5


def test_point_2():
    s = d3.scale_point()
    assert s.get_padding_inner() == 1
    assert s.get_padding_outer() == 0


def test_point_3():
    p = d3.scale_point().set_domain(["foo", "bar"]).set_range([0, 960])
    b = (
        d3.scale_band()
        .set_domain(["foo", "bar"])
        .set_range([0, 960])
        .set_padding_inner(1)
    )
    assert list(map(p, p.get_domain())) == list(map(b, b.get_domain()))
    assert p.get_bandwidth() == b.get_bandwidth()
    assert p.get_step() == b.get_step()


def test_point_4():
    p = d3.scale_point().set_domain(["foo", "bar"]).set_range([0, 960]).set_padding(0.5)
    b = (
        d3.scale_band()
        .set_domain(["foo", "bar"])
        .set_range([0, 960])
        .set_padding_inner(0.5)
        .set_padding_outer(0.5)
    )
    assert list(map(p, p.get_domain())) == list(map(b, b.get_domain()))
    assert p.get_bandwidth() == b.get_bandwidth()
    assert p.get_step() == b.get_step()


def test_point_5():
    s = d3.scale_point()
    assert s.get_domain() == []
    assert s.get_range() == [0, 1]
    assert s.get_bandwidth() == 0
    assert s.get_step() == 1
    assert s.get_round() is False
    assert s.get_padding() == 1
    assert s.get_align() == 0.5
