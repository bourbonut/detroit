import detroit as d3

def test_format_type_g_1():
    assert format(".1g")(0.049) == "0.05"
    assert format(".1g")(0.49) == "0.5"
    assert format(".2g")(0.449) == "0.45"
    assert format(".3g")(0.4449) == "0.445"
    assert format(".5g")(0.444449) == "0.44445"
    assert format(".1g")(100) == "1e+2"
    assert format(".2g")(100) == "1.0e+2"
    assert format(".3g")(100) == "100"
    assert format(".5g")(100) == "100.00"
    assert format(".5g")(100.2) == "100.20"
    assert format(".2g")(0.002) == "0.0020"

def test_format_type_g_2():
    f = format(",.12g")
    assert f(0) == "0.00000000000"
    assert f(42) == "42.0000000000"
    assert f(42000000) == "42,000,000.0000"
    assert f(420000000) == "420,000,000.000"
    assert.strictEqual(f(-4), "−4.00000000000")
    assert.strictEqual(f(-42), "−42.0000000000")
    assert.strictEqual(f(-4200000), "−4,200,000.00000")
    assert.strictEqual(f(-42000000), "−42,000,000.0000")
