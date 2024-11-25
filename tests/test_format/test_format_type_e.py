import detroit as d3
import math


def test_format_type_e_1():
    f = d3.format("e")
    assert f(0) == "0.000000e+00"
    assert f(42) == "4.200000e+01"
    assert f(42000000) == "4.200000e+07"
    assert f(420000000) == "4.200000e+08"
    assert f(-4) == "-4.000000e+00"
    assert f(-42) == "-4.200000e+01"
    assert f(-4200000) == "-4.200000e+06"
    assert f(-42000000) == "-4.200000e+07"
    assert d3.format(".0e")(42) == "4e+01"
    assert d3.format(".3e")(42) == "4.200e+01"


def test_format_type_e_2():
    assert d3.format("1e")(-0) == "0.000000e+00"
    assert d3.format("1e")(-1e-12) == "-1.000000e-12"


def test_format_type_e_3():
    assert d3.format(",e")(math.inf) == "inf"


def test_format_type_e_4():
    assert d3.format(".3e")(-math.inf) == "-inf"
