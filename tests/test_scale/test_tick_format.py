import detroit as d3
import math

def test_tick_format_1():
    assert d3.tick_format(0, 1, 10)(0.2) == "0.2"
    assert d3.tick_format(0, 1, 20)(0.2) == "0.20"
    assert d3.tick_format(-100, 100, 10)(-20) == "−20"

def test_tick_format_2():
    assert d3.tick_format(0, 1, 10, "+f")(0.2) == "+0.2"
    assert d3.tick_format(0, 1, 20, "+f")(0.2) == "+0.20"
    assert d3.tick_format(0, 1, 10, "+%")(0.2) == "+20%"
    assert d3.tick_format(0.19, 0.21, 10, "+%")(0.2) == "+20.0%"

def test_tick_format_3():
    assert d3.tick_format(0, 9, 10, "")(2.10) == "2"
    assert d3.tick_format(0, 9, 100, "")(2.01) == "2"
    assert d3.tick_format(0, 9, 100, "")(2.11) == "2.1"
    assert d3.tick_format(0, 9, 10, "e")(2.10) == "2e+0"
    assert d3.tick_format(0, 9, 100, "e")(2.01) == "2.0e+0"
    assert d3.tick_format(0, 9, 100, "e")(2.11) == "2.1e+0"
    assert d3.tick_format(0, 9, 10, "g")(2.10) == "2"
    assert d3.tick_format(0, 9, 100, "g")(2.01) == "2.0"
    assert d3.tick_format(0, 9, 100, "g")(2.11) == "2.1"
    assert d3.tick_format(0, 9, 10, "r")(2.10e6) == "2000000"
    assert d3.tick_format(0, 9, 100, "r")(2.01e6) == "2000000"
    assert d3.tick_format(0, 9, 100, "r")(2.11e6) == "2100000"
    assert d3.tick_format(0, 0.9, 10, "p")(0.210) == "20%"
    assert d3.tick_format(0.19, 0.21, 10, "p")(0.201) == "20.1%"

def test_tick_format_4():
    assert d3.tick_format(0, 1e6, 10, "$s")(0.51e6) == "$0.5M"
    assert d3.tick_format(0, 1e6, 100, "$s")(0.501e6) == "$0.50M"

def test_tick_format_5():
    f = d3.tick_format(0, math.nan, 10)
    assert str(f) == " >-,f"
    assert f(0.12), "0.120000"
