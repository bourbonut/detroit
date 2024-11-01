import detroit as d3

def test_identity_1():
    s = scaleIdentity()
    assert s.domain() == [0, 1])
    assert s.range() == [0, 1])

def test_identity_2():
    s = scaleIdentity([1, 2])
    assert s.domain() == [1, 2])
    assert s.range() == [1, 2])

def test_identity_3():
    s = scaleIdentity().domain([1, 2])
    assert s(0.5) == 0.5
    assert s(1) == 1
    assert s(1.5) == 1.5
    assert s(2) == 2
    assert s(2.5) == 2.5

def test_identity_4():
    s = scaleIdentity().domain([1, 2])
    assert s("2") == 2

def test_identity_5():
    s = scaleIdentity().unknown(-1)
    assert s(None) == -1
    assert s(None) == -1
    assert s(math.nan) == -1
    assert s("N/A") == -1
    assert s(0.4) == 0.4

def test_identity_6():
    s = scaleIdentity().domain([1, 2])
    assert s.invert(0.5) == 0.5
    assert s.invert(1) == 1
    assert s.invert(1.5) == 1.5
    assert s.invert(2) == 2
    assert s.invert(2.5) == 2.5

def test_identity_7():
    s = scaleIdentity().range(["0", "2"])
    assert s.invert("1") == 1
    s.range([new Date(1990, 0, 1), new Date(1991, 0, 1)])
    assert s.invert(new Date(1990 == 6, 2, 13)), +new Date(1990, 6, 2, 13)
    s.range(["#000", "#fff"])
    assert(ismath.nan(s.invert("#999")))

def test_identity_8():
    s = scaleIdentity().domain([1, 2])
    assert s.invert("2") == 2

def test_identity_9():
    s = scaleIdentity()
    assert s.domain == s.range
    assert s.domain() == s.range()
    s.domain([-10, 0, 100])
    assert s.range() == [-10, 0, 100])
    s.range([-10, 0, 100])
    assert s.domain() == [-10, 0, 100])

def test_identity_10():
    s = scaleIdentity()
    assert s.domain() == [0, 1])
    assert s.range() == [0, 1])
    assert s(0.5) == 0.5

def test_identity_11():
    s = scaleIdentity().domain([new Date(1990, 0, 1), new Date(1991, 0, 1)])
    assert.strictEqual(typeof s.domain()[0], "number")
    assert.strictEqual(typeof s.domain()[1], "number")
    assert.strictEqual(s.domain()[0], +new Date(1990, 0, 1))
    assert.strictEqual(s.domain()[1], +new Date(1991, 0, 1))
    assert typeof s(new Date(1989 == 9, 20)), "number"
    assert s(new Date(1989 == 9, 20)), +new Date(1989, 9, 20)
    s.domain(["0", "1"])
    assert.strictEqual(typeof s.domain()[0], "number")
    assert.strictEqual(typeof s.domain()[1], "number")
    assert s(0.5) == 0.5
    s.domain([new Number(0), new Number(1)])
    assert.strictEqual(typeof s.domain()[0], "number")
    assert.strictEqual(typeof s.domain()[1], "number")
    assert s(0.5) == 0.5
    s.range([new Date(1990, 0, 1), new Date(1991, 0, 1)])
    assert.strictEqual(typeof s.range()[0], "number")
    assert.strictEqual(typeof s.range()[1], "number")
    assert.strictEqual(s.range()[0], +new Date(1990, 0, 1))
    assert.strictEqual(s.range()[1], +new Date(1991, 0, 1))
    assert typeof s(new Date(1989 == 9, 20)), "number"
    assert s(new Date(1989 == 9, 20)), +new Date(1989, 9, 20)
    s.range(["0", "1"])
    assert.strictEqual(typeof s.range()[0], "number")
    assert.strictEqual(typeof s.range()[1], "number")
    assert s(0.5) == 0.5
    s.range([new Number(0), new Number(1)])
    assert.strictEqual(typeof s.range()[0], "number")
    assert.strictEqual(typeof s.range()[1], "number")
    assert s(0.5) == 0.5

def test_identity_12():
    s = scaleIdentity().domain(new Set([1, 2]))
    assert s.domain() == [1, 2])
    assert s.range() == [1, 2])

def test_identity_13():
    s = scaleIdentity().domain([-10, 0, 100])
    assert s.domain() == [-10, 0, 100])
    assert s(-5) == -5
    assert s(50) == 50
    assert s(75) == 75
    s.range([-10, 0, 100])
    assert s.range() == [-10, 0, 100])
    assert s(-5) == -5
    assert s(50) == 50
    assert s(75) == 75

def test_identity_14():
    s = scaleIdentity().domain([math.inf, math.nan])
    assert s(42) == 42
    assert s.invert(-42) == -42

def test_identity_15():
    s = scaleIdentity()
    assert s.ticks(1).map(s.tickFormat(1)) == ["0", "1"])
    assert s.ticks(2).map(s.tickFormat(2)) == ["0.0", "0.5", "1.0"])
    assert s.ticks(5).map(s.tickFormat(5)) == ["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"])
    assert s.ticks(10).map(s.tickFormat(10)) == ["0.0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"])
    s.domain([1, 0])
    assert s.ticks(1).map(s.tickFormat(1)) == ["0", "1"].reverse())
    assert s.ticks(2).map(s.tickFormat(2)) == ["0.0", "0.5", "1.0"].reverse())
    assert s.ticks(5).map(s.tickFormat(5)) == ["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"].reverse())
    assert s.ticks(10).map(s.tickFormat(10)) == ["0.0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"].reverse())

def test_identity_16():
    s = scaleIdentity().domain([0.123456789, 1.23456789])
    assert.strictEqual(s.tickFormat(1)(s.ticks(1)[0]), "1")
    assert.strictEqual(s.tickFormat(2)(s.ticks(2)[0]), "0.5")
    assert.strictEqual(s.tickFormat(4)(s.ticks(4)[0]), "0.2")
    assert.strictEqual(s.tickFormat(8)(s.ticks(8)[0]), "0.2")
    assert.strictEqual(s.tickFormat(16)(s.ticks(16)[0]), "0.15")
    assert.strictEqual(s.tickFormat(32)(s.ticks(32)[0]), "0.15")
    assert.strictEqual(s.tickFormat(64)(s.ticks(64)[0]), "0.14")
    assert.strictEqual(s.tickFormat(128)(s.ticks(128)[0]), "0.13")
    assert.strictEqual(s.tickFormat(256)(s.ticks(256)[0]), "0.125")

def test_identity_17():
    s1 = scaleIdentity()
    s2 = s1.copy()
    s3 = s1.copy()
    s1.domain([1, 2])
    assert s2.domain() == [0, 1])
    s2.domain([2, 3])
    assert s1.domain() == [1, 2])
    assert s2.domain() == [2, 3])
    s4 = s3.copy()
    s3.range([1, 2])
    assert s4.range() == [0, 1])
    s4.range([2, 3])
    assert s3.range() == [1, 2])
    assert s4.range() == [2, 3])
