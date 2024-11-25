import detroit as d3


def test_format_type_r_1():
    assert d3.format(".2r")(0) == "0.0"
    assert d3.format(".1r")(0.049) == "0.05"
    assert d3.format(".1r")(-0.049) == "-0.05"
    assert d3.format(".1r")(0.49) == "0.5"
    assert d3.format(".1r")(-0.49) == "-0.5"
    assert d3.format(".2r")(0.449) == "0.45"
    assert d3.format(".3r")(0.4449) == "0.445"
    assert d3.format(".3r")(1.00) == "1.00"
    assert d3.format(".3r")(0.9995) == "1.00"
    assert d3.format(".5r")(0.444449) == "0.44445"
    assert d3.format("r")(123.45) == "123.450"
    assert d3.format(".1r")(123.45) == "100"
    assert d3.format(".2r")(123.45) == "120"
    assert d3.format(".3r")(123.45) == "123"
    assert d3.format(".4r")(123.45) == "123.5"
    assert d3.format(".5r")(123.45) == "123.45"
    assert d3.format(".6r")(123.45) == "123.450"
    assert d3.format(".1r")(0.9) == "0.9"
    assert d3.format(".1r")(0.09) == "0.09"
    assert d3.format(".1r")(0.949) == "0.9"
    assert d3.format(".1r")(0.0949) == "0.09"
    assert d3.format(".1r")(0.0000000129) == "0.00000001"
    assert d3.format(".2r")(0.0000000129) == "0.000000013"
    assert d3.format(".2r")(0.00000000129) == "0.0000000013"
    assert d3.format(".3r")(0.00000000129) == "0.00000000129"
    assert d3.format(".4r")(0.00000000129) == "0.000000001290"
    assert d3.format(".10r")(0.9999999999) == "0.9999999999"
    assert d3.format(".15r")(0.999999999999999) == "0.999999999999999"


def test_format_type_r_2():
    f = d3.format(".2r")
    assert f(1e-22) == "0.00000000000000000000010"
