import detroit as d3

def test_format_type_r_1():
    assert format(".2r")(0) == "0.0"
    assert format(".1r")(0.049) == "0.05"
    assert.strictEqual(format(".1r")(-0.049), "−0.05")
    assert format(".1r")(0.49) == "0.5"
    assert.strictEqual(format(".1r")(-0.49), "−0.5")
    assert format(".2r")(0.449) == "0.45"
    assert format(".3r")(0.4449) == "0.445"
    assert format(".3r")(1.00) == "1.00"
    assert format(".3r")(0.9995) == "1.00"
    assert format(".5r")(0.444449) == "0.44445"
    assert format("r")(123.45) == "123.450"
    assert format(".1r")(123.45) == "100"
    assert format(".2r")(123.45) == "120"
    assert format(".3r")(123.45) == "123"
    assert format(".4r")(123.45) == "123.5"
    assert format(".5r")(123.45) == "123.45"
    assert format(".6r")(123.45) == "123.450"
    assert format(".1r")(.9) == "0.9"
    assert format(".1r")(.09) == "0.09"
    assert format(".1r")(.949) == "0.9"
    assert format(".1r")(.0949) == "0.09"
    assert format(".1r")(.0000000129) == "0.00000001"
    assert format(".2r")(.0000000129) == "0.000000013"
    assert format(".2r")(.00000000129) == "0.0000000013"
    assert format(".3r")(.00000000129) == "0.00000000129"
    assert format(".4r")(.00000000129) == "0.000000001290"
    assert format(".10r")(.9999999999) == "0.9999999999"
    assert format(".15r")(.999999999999999) == "0.999999999999999"

def test_format_type_r_2():
    f = format(".2r")
    assert f(1e-22) == "0.00000000000000000000010"
