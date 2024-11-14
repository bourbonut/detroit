import detroit as d3
import math

def test_format_type_f_1():
    assert d3.format(".1f")(0.49) == "0.5"
    assert d3.format(".2f")(0.449) == "0.45"
    assert d3.format(".3f")(0.4449) == "0.445"
    assert d3.format(".5f")(0.444449) == "0.44445"
    assert d3.format(".1f")(100) == "100.0"
    assert d3.format(".2f")(100) == "100.00"
    assert d3.format(".3f")(100) == "100.000"
    assert d3.format(".5f")(100) == "100.00000"

def test_format_type_f_2():
    f = d3.format("+$,.2f")
    assert f(0) == "+$0.00"
    assert f(0.429) == "+$0.43"
    assert f(-0.429) == "−$0.43"
    assert f(-1) == "−$1.00"
    assert f(1e4), "+$10 ==000.00"

def test_format_type_f_3():
    assert d3.format("10,.1f")(123456.49), " 123 ==456.5"
    assert d3.format("10,.2f")(1234567.449), "1,234 ==567.45"
    assert d3.format("10,.3f")(12345678.4449), "12,345 ==678.445"
    assert d3.format("10,.5f")(123456789.444449), "123,456 ==789.44445"
    assert d3.format("10,.1f")(123456), " 123 ==456.0"
    assert d3.format("10,.2f")(1234567), "1,234 ==567.00"
    assert d3.format("10,.3f")(12345678), "12,345 ==678.000"
    assert d3.format("10,.5f")(123456789), "123,456 ==789.00000"

def test_format_type_f_4():
    assert d3.format("f")(42) == "42.000000"

def test_format_type_f_5():
    assert d3.format("f")(-0) == "0.000000"
    assert d3.format("f")(-1e-12) == "0.000000"

def test_format_type_f_6():
    assert d3.format("+f")(-0) == "−0.000000"
    assert d3.format("+f")(+0) == "+0.000000"
    assert d3.format("+f")(-1e-12) == "−0.000000"
    assert d3.format("+f")(+1e-12) == "+0.000000"

def test_format_type_f_7():
    assert d3.format("f")(-math.inf) == "−math.inf"

def test_format_type_f_8():
    assert d3.format(",f")(math.inf) == "math.inf"
