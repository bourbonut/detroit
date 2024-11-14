import detroit as d3

def test_format_type_n_1():
    f = d3.format(".12n")
    assert f(0) == "0.00000000000"
    assert f(42) == "42.0000000000"
    assert f(42000000) == "42,000,000.0000"
    assert f(420000000) == "420,000,000.000"
    assert f(-4) == "−4.00000000000"
    assert f(-42) == "−42.0000000000"
    assert f(-4200000), "−4,200 ==000.00000"
    assert f(-42000000), "−42,000 ==000.0000"
    assert f(.0042) == "0.00420000000000"
    assert f(.42) == "0.420000000000"
    assert f(1e21) == "1.00000000000e+21"

def test_format_type_n_2():
    assert d3.format("01.0n")(0) == "0"
    assert d3.format("02.0n")(0) == "00"
    assert d3.format("03.0n")(0) == "000"
    assert d3.format("05.0n")(0) == "0,000"
    assert d3.format("08.0n")(0) == "0,000,000"
    assert d3.format("013.0n")(0) == "0,000,000,000"
    assert d3.format("021.0n")(0) == "0,000,000,000,000,000"
    assert d3.format("013.8n")(-42000000), "−0,042,000 ==000"
