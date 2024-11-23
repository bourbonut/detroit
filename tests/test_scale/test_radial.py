import detroit as d3
import math
import pytest

def test_radial_1():
    s = d3.scale_radial()
    assert s.domain() == [0, 1]
    assert s.range() == [0, 1]
    assert s.clamp() is False
    assert s.round() is False

def test_radial_2():
    s = d3.scale_radial([100, 200])
    assert s.domain() == [0, 1]
    assert s.range() == [100, 200]
    assert s(0.5) == 158.11388300841898

def test_radial_3():
    s = d3.scale_radial([1, 2], [10, 20])
    assert s.domain() == [1, 2]
    assert s.range() == [10, 20]
    assert s(1.5) == 15.811388300841896

def test_radial_4():
    assert d3.scale_radial([1, 2])(0.5) == 1.5811388300841898

def test_radial_5():
    assert d3.scale_radial().domain([-10, 0]).range([2, 3, 4]).clamp(True)(-5) == 2.5495097567963922
    assert d3.scale_radial().domain([-10, 0]).range([2, 3, 4]).clamp(True)(50) == 3

def test_radial_6():
    assert d3.scale_radial().domain([-10, 0, 100]).range([2, 3]).clamp(True)(-5) == 2.5495097567963922
    assert d3.scale_radial().domain([-10, 0, 100]).range([2, 3]).clamp(True)(50) == 3

def test_radial_7():
    assert d3.scale_radial().domain([0, 0]).range([1, 2])(0) == 1.5811388300841898
    assert d3.scale_radial().domain([0, 0]).range([2, 1])(1) == 1.5811388300841898

def test_radial_8():
    s = d3.scale_radial().domain([1, 2])
    assert s.domain() == [1, 2]
    assert s(0.5) == -0.7071067811865476
    assert s(1.0) ==    0.0
    assert s(1.5) ==    0.7071067811865476
    assert s(2.0) ==    1.0
    assert s(2.5) ==    1.224744871391589
    assert s.invert(-0.5) == 0.75
    assert s.invert( 0.0) == 1.0
    assert s.invert( 0.5) == 1.25
    assert s.invert( 1.0) == 2.0
    assert s.invert( 1.5) == 3.25

def test_radial_9():
    s = d3.scale_radial()
    with pytest.raises(TypeError):
        assert s(math.nan) is None
    with pytest.raises(TypeError):
        assert s(None) is None
    with pytest.raises(ValueError):
        assert s("foo") is None
    with pytest.raises(TypeError):
        assert s({}) is None

def test_radial_10():
    with pytest.raises(TypeError):
        assert d3.scale_radial().unknown("foo")(math.nan) == "foo"

def test_radial_11():
    assert d3.scale_radial([-1, -2])(0.5) == -1.5811388300841898

def test_radial_12():
    assert d3.scale_radial([-1, -2]).clamp(True)(-0.5) == -1
    assert d3.scale_radial().clamp(True)(-0.5) == 0
    assert d3.scale_radial([-0.25, 0], [1, 2]).clamp(True)(-0.5) == 1
