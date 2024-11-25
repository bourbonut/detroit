import detroit as d3


def test_format_type_g_1():
    assert d3.format(".1g")(0.049) == "0.05"
    assert d3.format(".1g")(0.49) == "0.5"
    assert d3.format(".2g")(0.449) == "0.45"
    assert d3.format(".3g")(0.4449) == "0.445"
    assert d3.format(".5g")(0.444449) == "0.44445"
    assert d3.format(".1g")(100) == "1e+02"
    assert d3.format(".2g")(100) == "1e+02"
    assert d3.format(".3g")(100) == "100"
    assert d3.format(".5g")(100) == "100"
    assert d3.format(".5g")(100.2) == "100.2"
    assert d3.format(".2g")(0.002) == "0.002"


def test_format_type_g_2():
    f = d3.format(",.12g")
    assert f(0) == "0"
    assert f(42) == "42"
    assert f(42000000) == "42,000,000"
    assert f(420000000) == "420,000,000"
    assert f(-4) == "-4"
    assert f(-42) == "-42"
    assert f(-4200000) == "-4,200,000"
    assert f(-42000000) == "-42,000,000"
