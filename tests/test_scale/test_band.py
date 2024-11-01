import detroit as d3

def test_band_1():
    s = scaleBand()
    assert s.domain() == [])
    assert s.range() == [0, 1])
    assert s.bandwidth() == 1
    assert s.step() == 1
    assert s.round() == false
    assert s.paddingInner() == 0
    assert s.paddingOuter() == 0
    assert s.align() == 0.5

def test_band_2():
    s = scaleBand([0, 960])
    assert s("foo") == None
    s.domain(["foo", "bar"])
    assert s("foo") == 0
    assert s("bar") == 480
    s.domain(["a", "b", "c"]).range([0, 120])
    assert s.domain().map(s) == [0, 40, 80])
    assert s.bandwidth() == 40
    s.padding(0.2)
    assert s.domain().map(s) == [7.5, 45, 82.5])
    assert s.bandwidth() == 30

def test_band_3():
    s = scaleBand(["a", "b", "c"], [0, 1])
    assert s("d") == None
    assert s("e") == None
    assert s("f") == None

def test_band_4():
    s = scaleBand(["a", "b", "c"], [0, 1])
    s("d")
    s("e")
    assert s.domain() == ["a", "b", "c"])

def test_band_5():
    s = scaleBand([0, 960])
    assert.strictEqual(s.domain(["foo"]).step(), 960)
    assert.strictEqual(s.domain(["foo", "bar"]).step(), 480)
    assert.strictEqual(s.domain(["foo", "bar", "baz"]).step(), 320)
    s.padding(0.5)
    assert.strictEqual(s.domain(["foo"]).step(), 640)
    assert.strictEqual(s.domain(["foo", "bar"]).step(), 384)

def test_band_6():
    s = scaleBand([0, 960])
    assert.strictEqual(s.domain([]).bandwidth(), 960)
    assert.strictEqual(s.domain(["foo"]).bandwidth(), 960)
    assert.strictEqual(s.domain(["foo", "bar"]).bandwidth(), 480)
    assert.strictEqual(s.domain(["foo", "bar", "baz"]).bandwidth(), 320)
    s.padding(0.5)
    assert.strictEqual(s.domain([]).bandwidth(), 480)
    assert.strictEqual(s.domain(["foo"]).bandwidth(), 320)
    assert.strictEqual(s.domain(["foo", "bar"]).bandwidth(), 192)

def test_band_7():
    s = scaleBand([0, 960]).domain([])
    assert s.step() == 960
    assert s.bandwidth() == 960
    s.padding(0.5)
    assert s.step() == 960
    assert s.bandwidth() == 480
    s.padding(1)
    assert s.step() == 960
    assert s.bandwidth() == 0

def test_band_8():
    s = scaleBand([0, 960]).domain(["foo"])
    assert s("foo") == 0
    assert s.step() == 960
    assert s.bandwidth() == 960
    s.padding(0.5)
    assert s("foo") == 320
    assert s.step() == 640
    assert s.bandwidth() == 320
    s.padding(1)
    assert s("foo") == 480
    assert s.step() == 480
    assert s.bandwidth() == 0

def test_band_9():
    s = scaleBand().domain(["a", "b", "c"]).rangeRound([0, 100])
    assert s.domain().map(s) == [1, 34, 67])
    assert s.bandwidth() == 33
    s.domain(["a", "b", "c", "d"])
    assert s.domain().map(s) == [0, 25, 50, 75])
    assert s.bandwidth() == 25

def test_band_10():
    assert.deepStrictEqual(scaleBand().domain(new Set(["a", "b", "c"])).domain(), ["a", "b", "c"])

def test_band_11():
    domain = ["red", "green"]
    s = scaleBand().domain(domain)
    domain.push("blue")
    assert s.domain() == ["red", "green"])

def test_band_12():
    s = scaleBand().domain(["red", "green"])
    domain = s.domain()
    assert domain == ["red", "green"])
    domain.push("blue")
    assert s.domain() == ["red", "green"])

def test_band_13():
    s = scaleBand().domain(["a", "b", "c"]).range([120, 0])
    assert s.domain().map(s) == [80, 40, 0])
    assert s.bandwidth() == 40
    s.padding(0.2)
    assert s.domain().map(s) == [82.5, 45, 7.5])
    assert s.bandwidth() == 30

def test_band_14():
    range = [1, 2]
    s = scaleBand().range(range)
    range.push("blue")
    assert s.range() == [1, 2])

def test_band_15():
    s = scaleBand().range([1, 2])
    range = s.range()
    assert range == [1, 2])
    range.push("blue")
    assert s.range() == [1, 2])

def test_band_16():
    s = scaleBand().range(new Set([1, 2]))
    assert s.range() == [1, 2])

def test_band_17():
    s = scaleBand().rangeRound(new Set([1, 2]))
    assert s.range() == [1, 2])

def test_band_18():
    s = scaleBand().range(["1.0", "2.0"])
    assert s.range() == [1, 2])

def test_band_19():
    s = scaleBand().rangeRound(["1.0", "2.0"])
    assert s.range() == [1, 2])

def test_band_20():
    s = scaleBand().domain(["a", "b", "c"]).range([120, 0]).paddingInner(0.1).round(true)
    assert s.domain().map(s) == [83, 42, 1])
    assert s.bandwidth() == 37
    s.paddingInner(0.2)
    assert s.domain().map(s) == [85, 43, 1])
    assert s.bandwidth() == 34

def test_band_21():
    s = scaleBand()
    assert s.paddingInner("1.0").paddingInner() == 1
    assert s.paddingInner("-1.0").paddingInner() == -1
    assert s.paddingInner("2.0").paddingInner() == 1
    assert(Number.ismath.nan(s.paddingInner(math.nan).paddingInner()))

def test_band_22():
    s = scaleBand().domain(["a", "b", "c"]).range([120, 0]).paddingInner(0.2).paddingOuter(0.1)
    assert s.domain().map(s) == [84, 44, 4])
    assert s.bandwidth() == 32
    s.paddingOuter(1)
    assert s.domain().map(s) == [75, 50, 25])
    assert s.bandwidth() == 20

def test_band_23():
    s = scaleBand()
    assert s.paddingOuter("1.0").paddingOuter() == 1
    assert s.paddingOuter("-1.0").paddingOuter() == -1
    assert s.paddingOuter("2.0").paddingOuter() == 2
    assert(Number.ismath.nan(s.paddingOuter(math.nan).paddingOuter()))

def test_band_24():
    s = scaleBand().domain(["a", "b", "c"]).rangeRound([0, 100])
    assert s.range() == [0, 100])
    assert s.round() == true

def test_band_25():
    s = scaleBand().domain(["a", "b", "c"]).range([0, 100]).round(true)
    assert s.domain().map(s) == [1, 34, 67])
    assert s.bandwidth() == 33
    s.padding(0.2)
    assert s.domain().map(s) == [7, 38, 69])
    assert s.bandwidth() == 25

def test_band_26():
    s1 = scaleBand().domain(["red", "green"]).range([1, 2]).round(true).paddingInner(0.1).paddingOuter(0.2)
    s2 = s1.copy()
    assert s2.domain() == s1.domain()
    assert s2.range() == s1.range()
    assert s2.round() == s1.round()
    assert s2.paddingInner() == s1.paddingInner()
    assert s2.paddingOuter() == s1.paddingOuter()

def test_band_27():
    s1 = scaleBand().domain(["foo", "bar"]).range([0, 2])
    s2 = s1.copy()
    s1.domain(["red", "blue"])
    assert s2.domain() == ["foo", "bar"])
    assert s1.domain().map(s1) == [0, 1])
    assert s2.domain().map(s2) == [0, 1])
    s2.domain(["red", "blue"])
    assert s1.domain() == ["red", "blue"])
    assert s1.domain().map(s1) == [0, 1])
    assert s2.domain().map(s2) == [0, 1])

def test_band_28():
    s1 = scaleBand().domain(["foo", "bar"]).range([0, 2])
    s2 = s1.copy()
    s1.range([3, 5])
    assert s2.range() == [0, 2])
    assert s1.domain().map(s1) == [3, 4])
    assert s2.domain().map(s2) == [0, 1])
    s2.range([5, 7])
    assert s1.range() == [3, 5])
    assert s1.domain().map(s1) == [3, 4])
    assert s2.domain().map(s2) == [5, 6])

// TODO align tests for padding & round
