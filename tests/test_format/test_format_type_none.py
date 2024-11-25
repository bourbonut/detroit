import detroit as d3
import math

def test_format_type_none_1():
    assert d3.format(".1")(4.9) == "5"
    assert d3.format(".1")(0.49) == "0.5"
    assert d3.format(".2")(4.9) == "4.9"
    assert d3.format(".2")(0.49) == "0.49"
    assert d3.format(".2")(0.449) == "0.45"
    assert d3.format(".3")(4.9) == "4.9"
    assert d3.format(".3")(0.49) == "0.49"
    assert d3.format(".3")(0.449) == "0.449"
    assert d3.format(".3")(0.4449) == "0.445"
    assert d3.format(".5")(0.444449) == "0.44445"

def test_format_type_none_2():
    assert d3.format(".5")(10) == "10"
    assert d3.format(".5")(100) == "100"
    assert d3.format(".5")(1000) == "1000"
    assert d3.format(".5")(21010) == "21010"
    assert d3.format(".5")(1.10001) == "1.1"
    assert d3.format(".5")(1.10001e6) == "1.1e+06"
    assert d3.format(".6")(1.10001) == "1.10001"
    assert d3.format(".6")(1.10001e6) == "1.10001e+06"

def test_format_type_none_3():
    assert d3.format(".5")(1.00001) == "1"
    assert d3.format(".5")(1.00001e6) == "1e+06"
    assert d3.format(".6")(1.00001) == "1.00001"
    assert d3.format(".6")(1.00001e6) == "1.00001e+06"

def test_format_type_none_4():
    f = d3.format("$")
    assert f(0) == "$0"
    assert f(.042) == "$0.042"
    assert f(.42) == "$0.42"
    assert f(4.2) == "$4.2"
    assert f(-.042) == "-$0.042"
    assert f(-.42) == "-$0.42"
    assert f(-4.2) == "-$4.2"

def test_format_type_none_5():
    f = d3.format("($")
    assert f(0) == "$0"
    assert f(.042) == "$0.042"
    assert f(.42) == "$0.42"
    assert f(4.2) == "$4.2"
    assert f(-.042) == "($0.042)"
    assert f(-.42) == "($0.42)"
    assert f(-4.2) == "($4.2)"

def test_format_type_none_6():
    assert d3.format("")(-0) == "0"

def test_format_type_none_7():
    assert d3.format("")(-math.inf) == "-inf"
