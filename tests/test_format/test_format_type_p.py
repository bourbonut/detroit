import detroit as d3

def test_format_type_p_1():
    f = format("p")
    assert.strictEqual(f(.00123), "0.123000%")
    assert.strictEqual(f(.0123), "1.23000%")
    assert.strictEqual(f(.123), "12.3000%")
    assert.strictEqual(f(.234), "23.4000%")
    assert.strictEqual(f(1.23), "123.000%")
    assert.strictEqual(f(-.00123), "−0.123000%")
    assert.strictEqual(f(-.0123), "−1.23000%")
    assert.strictEqual(f(-.123), "−12.3000%")
    assert.strictEqual(f(-1.23), "−123.000%")

def test_format_type_p_2():
    f = format("+.2p")
    assert.strictEqual(f(.00123), "+0.12%")
    assert.strictEqual(f(.0123), "+1.2%")
    assert.strictEqual(f(.123), "+12%")
    assert.strictEqual(f(1.23), "+120%")
    assert.strictEqual(f(-.00123), "−0.12%")
    assert.strictEqual(f(-.0123), "−1.2%")
    assert.strictEqual(f(-.123), "−12%")
    assert.strictEqual(f(-1.23), "−120%")
