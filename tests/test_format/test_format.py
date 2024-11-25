import detroit as d3
import pytest


def test_format_1():
    assert isinstance(d3.format("d")(0), str)


def test_format_2():
    assert str(d3.format("d")) == " >-d"


def test_format_3():
    with pytest.raises(ValueError):
        assert d3.format("foo")
    with pytest.raises(ValueError):
        assert d3.format(".-2s")
    with pytest.raises(ValueError):
        assert d3.format(".f")


def test_format_4():
    assert d3.format(".30f")(0) == "0.00000000000000000000"
    assert d3.format(".0g")(1) == "1"


def test_format_5():
    assert d3.format("n")(123456.78) == "123,457"
    assert d3.format(",g")(123456.78) == "123,457"


def test_format_6():
    assert d3.format("012")(123.456) == "00000123.456"
    assert d3.format("0=12")(123.456) == "00000123.456"
