import detroit as d3

def test_sqrt_1():
    s = scaleSqrt()
    assert s.domain() == [0, 1])
    assert s.range() == [0, 1])
    assert s.clamp() == false
    assert s.exponent() == 0.5
    assert.deepStrictEqual(s.interpolate()({array: ["red"]}, {array: ["blue"]})(0.5), {array: ["rgb(128, 0, 128)"]})

def test_sqrt_2():
    assert.strictEqual(scaleSqrt()(0.5), Math.SQRT1_2)
