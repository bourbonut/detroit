import detroit as d3

def test_format_type_e_1():
    f = format("e")
    assert f(0) == "0.000000e+0"
    assert f(42) == "4.200000e+1"
    assert f(42000000) == "4.200000e+7"
    assert f(420000000) == "4.200000e+8"
    assert.strictEqual(f(-4), "−4.000000e+0")
    assert.strictEqual(f(-42), "−4.200000e+1")
    assert.strictEqual(f(-4200000), "−4.200000e+6")
    assert.strictEqual(f(-42000000), "−4.200000e+7")
    assert.strictEqual(format(".0e")(42), "4e+1")
    assert.strictEqual(format(".3e")(42), "4.200e+1")

def test_format_type_e_2():
    assert format("1e")(-0) == "0.000000e+0"
    assert.strictEqual(format("1e")(-1e-12), "−1.000000e-12")

def test_format_type_e_3():
    assert.strictEqual(format(",e")(math.inf), "math.inf")

def test_format_type_e_4():
    assert.strictEqual(format(".3e")(-math.inf), "−math.inf")
