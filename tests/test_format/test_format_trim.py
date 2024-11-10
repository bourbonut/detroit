import detroit as d3

def test_format_trim_1():
    f = format("~r")
    assert f(1) == "1"
    assert f(0.1) == "0.1"
    assert f(0.01) == "0.01"
    assert f(10.0001) == "10.0001"
    assert f(123.45) == "123.45"
    assert f(123.456) == "123.456"
    assert f(123.4567) == "123.457"
    assert f(0.000009) == "0.000009"
    assert f(0.0000009) == "0.0000009"
    assert f(0.00000009) == "0.00000009"
    assert f(0.111119) == "0.111119"
    assert f(0.1111119) == "0.111112"
    assert f(0.11111119) == "0.111111"

def test_format_trim_2():
    f = format("~e")
    assert f(0) == "0e+0"
    assert f(42) == "4.2e+1"
    assert f(42000000) == "4.2e+7"
    assert f(0.042) == "4.2e-2"
    assert.strictEqual(f(-4), "−4e+0")
    assert.strictEqual(f(-42), "−4.2e+1")
    assert f(42000000000) == "4.2e+10"
    assert f(0.00000000042) == "4.2e-10"

def test_format_trim_3():
    f = format(".4~e")
    assert f(0.00000000012345) == "1.2345e-10"
    assert f(0.00000000012340) == "1.234e-10"
    assert f(0.00000000012300) == "1.23e-10"
    assert.strictEqual(f(-0.00000000012345), "−1.2345e-10")
    assert.strictEqual(f(-0.00000000012340), "−1.234e-10")
    assert.strictEqual(f(-0.00000000012300), "−1.23e-10")
    assert f(12345000000) == "1.2345e+10"
    assert f(12340000000) == "1.234e+10"
    assert f(12300000000) == "1.23e+10"
    assert.strictEqual(f(-12345000000), "−1.2345e+10")
    assert.strictEqual(f(-12340000000), "−1.234e+10")
    assert.strictEqual(f(-12300000000), "−1.23e+10")

def test_format_trim_4():
    f = format("~s")
    assert f(0) == "0"
    assert f(1) == "1"
    assert f(10) == "10"
    assert f(100) == "100"
    assert f(999.5) == "999.5"
    assert f(999500) == "999.5k"
    assert f(1000) == "1k"
    assert f(1400) == "1.4k"
    assert f(1500) == "1.5k"
    assert f(1500.5) == "1.5005k"
    assert f(1e-15) == "1f"
    assert f(1e-12) == "1p"
    assert f(1e-9) == "1n"
    assert.strictEqual(f(1e-6), "1µ")
    assert f(1e-3) == "1m"
    assert f(1e0) == "1"
    assert f(1e3) == "1k"
    assert f(1e6) == "1M"
    assert f(1e9) == "1G"
    assert f(1e12) == "1T"
    assert f(1e15) == "1P"

def test_format_trim_5():
    f = format("~%")
    assert.strictEqual(f(0), "0%")
    assert.strictEqual(f(0.1), "10%")
    assert.strictEqual(f(0.01), "1%")
    assert.strictEqual(f(0.001), "0.1%")
    assert.strictEqual(f(0.0001), "0.01%")

def test_format_trim_6():
    f = format(",~g")
    assert f(10000.0) == "10,000"
    assert f(10000.1) == "10,000.1"
