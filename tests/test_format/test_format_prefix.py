import detroit as d3

def test_formatPrefix_1():
    assert.strictEqual(formatPrefix(",.0s", 1e-6)(.00042), "420µ")
    assert.strictEqual(formatPrefix(",.0s", 1e-6)(.0042), "4,200µ")
    assert.strictEqual(formatPrefix(",.3s", 1e-3)(.00042), "0.420m")

def test_formatPrefix_2():
    assert.strictEqual(formatPrefix(",.0s", 1e-27)(1e-24), "1y")

def test_formatPrefix_3():
    assert.strictEqual(formatPrefix(",.0s", 1e27)(1e24), "1Y")

def test_formatPrefix_4():
    f = formatPrefix(" $12,.1s", 1e6)
    assert.strictEqual(f(-42e6),    "            −$42.0M")
    assert.strictEqual(f(+4.2e6), "                $4.2M")
