import detroit as d3

def test_format_type_none_1():
    assert format(".1")(4.9) == "5"
    assert format(".1")(0.49) == "0.5"
    assert format(".2")(4.9) == "4.9"
    assert format(".2")(0.49) == "0.49"
    assert format(".2")(0.449) == "0.45"
    assert format(".3")(4.9) == "4.9"
    assert format(".3")(0.49) == "0.49"
    assert format(".3")(0.449) == "0.449"
    assert format(".3")(0.4449) == "0.445"
    assert format(".5")(0.444449) == "0.44445"

def test_format_type_none_2():
    assert format(".5")(10) == "10"
    assert format(".5")(100) == "100"
    assert format(".5")(1000) == "1000"
    assert format(".5")(21010) == "21010"
    assert format(".5")(1.10001) == "1.1"
    assert format(".5")(1.10001e6) == "1.1e+6"
    assert format(".6")(1.10001) == "1.10001"
    assert format(".6")(1.10001e6) == "1.10001e+6"

def test_format_type_none_3():
    assert format(".5")(1.00001) == "1"
    assert format(".5")(1.00001e6) == "1e+6"
    assert format(".6")(1.00001) == "1.00001"
    assert format(".6")(1.00001e6) == "1.00001e+6"

def test_format_type_none_4():
    f = format("$")
    assert.strictEqual(f(0), "$0")
    assert.strictEqual(f(.042), "$0.042")
    assert.strictEqual(f(.42), "$0.42")
    assert.strictEqual(f(4.2), "$4.2")
    assert.strictEqual(f(-.042), "−$0.042")
    assert.strictEqual(f(-.42), "−$0.42")
    assert.strictEqual(f(-4.2), "−$4.2")

def test_format_type_none_5():
    f = format("($")
    assert.strictEqual(f(0), "$0")
    assert.strictEqual(f(.042), "$0.042")
    assert.strictEqual(f(.42), "$0.42")
    assert.strictEqual(f(4.2), "$4.2")
    assert.strictEqual(f(-.042), "($0.042)")
    assert.strictEqual(f(-.42), "($0.42)")
    assert.strictEqual(f(-4.2), "($4.2)")

def test_format_type_none_6():
    assert format("")(-0) == "0"

def test_format_type_none_7():
    assert.strictEqual(format("")(-math.inf), "−math.inf")
