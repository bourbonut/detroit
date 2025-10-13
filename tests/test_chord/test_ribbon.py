import detroit as d3
from detroit.chord.chord import ChordItem, ChordValue


def test_ribbon_1():
    r = d3.ribbon()
    value = ChordValue(0, 42, 42, 42)
    assert r.get_radius()({"radius": 42}) == 42
    assert r.get_start_angle()(value) == 42
    assert r.get_end_angle()(value) == 42
    assert r.get_context() is None


def test_ribbon_2():
    def foo(d):
        return d["foo"]

    r = d3.ribbon()
    assert r.set_radius(foo) == r
    assert r.get_radius() == foo
    assert r.set_radius(42) == r
    assert r.get_radius()() == 42


def test_ribbon_3():
    def foo(d):
        return d["foo"]

    r = d3.ribbon()
    assert r.set_start_angle(foo) == r
    assert r.get_start_angle() == foo
    assert r.set_start_angle(1.2) == r
    assert r.get_start_angle()() == 1.2


def test_ribbon_4():
    def foo(d):
        return d["foo"]

    r = d3.ribbon()
    assert r.set_end_angle(foo) == r
    assert r.get_end_angle() == foo
    assert r.set_end_angle(1.2) == r
    assert r.get_end_angle()() == 1.2


def test_ribbon_5():
    def foo(d):
        return d["foo"]

    r = d3.ribbon()
    assert r.set_source(foo) == r
    assert r.get_source() == foo


def test_ribbon_6():
    def foo(d):
        return d["foo"]

    r = d3.ribbon()
    assert r.set_target(foo) == r
    assert r.get_target() == foo


def test_ribbon_7():
    r = d3.ribbon().set_radius(240)
    value = ChordItem(
        ChordValue(0, 0.7524114, 1.1212972, 1), ChordValue(0, 1.8617078, 1.9842927, 1)
    )
    assert (
        r(value)
        == "M164.016,-175.210A240,240,0,0,1,216.160,-104.283Q0,0,229.916,68.838A240,240,0,0,1,219.773,96.435Q0,0,164.016,-175.210Z"
    )
