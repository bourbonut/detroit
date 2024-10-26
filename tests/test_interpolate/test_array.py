import detroit as d3
import pytest

def test_array_1():
    assert d3.interpolate_array([2, 12], [4, 24])(0.5) == [3., 18.]

def test_array_2():
    assert d3.interpolate_array([[2, 12]], [[4, 24]])(0.5) ==  [[3., 18.]]
    assert d3.interpolate_array([{"foo": [2, 12]}], [{"foo": [4, 24]}])(0.5) == [{"foo": [3, 18]}]

def test_array_3():
    assert d3.interpolate_array([2, 12, 12], [4, 24])(0.5) == [3., 18.]

def test_array_4():
    assert d3.interpolate_array([2, 12], [4, 24, 12])(0.5) == [3 , 18, 12]

@pytest.mark.skip
def test_array_5():
    assert d3.interpolate_array(None, [2, 12])(0.5) == [2, 12]
    assert d3.interpolate_array([2, 12], None)(0.5) == []
    assert d3.interpolate_array(None, None)(0.5) == []

def test_array_6():
    a = [2e+42]
    b = [335]
    assert d3.interpolate_array(a, b)(1) == b
    assert d3.interpolate_array(a, b)(0) == a
