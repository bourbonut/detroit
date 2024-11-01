import detroit as d3

def test_threshold_1():
    x = scaleThreshold()
    assert x.domain() == [0.5])
    assert x.range() == [0, 1])
    assert x(0.50) == 1
    assert x(0.49) == 0

def test_threshold_2():
    x = scaleThreshold().domain([1/3, 2/3]).range(["a", "b", "c"])
    assert x(0) == "a"
    assert x(0.2) == "a"
    assert x(0.4) == "b"
    assert x(0.6) == "b"
    assert x(0.8) == "c"
    assert x(1) == "c"

def test_threshold_3():
    x = scaleThreshold().domain([1/3, 2/3]).range(["a", "b", "c"])
    assert x() == None
    assert x(None) == None
    assert x(math.nan) == None
    assert x(None) == None

def test_threshold_4():
    x = scaleThreshold().domain(["10", "2"]).range([0, 1, 2])
    assert.strictEqual(x.domain()[0], "10")
    assert.strictEqual(x.domain()[1], "2")
    assert x("0") == 0
    assert x("12") == 1
    assert x("3") == 2

def test_threshold_5():
    x = scaleThreshold().domain(new Set(["10", "2"])).range([0, 1, 2])
    assert x.domain() == ["10", "2"])

def test_threshold_6():
    a = {}, b = {}, c = {}, x = scaleThreshold().domain([1/3, 2/3]).range([a, b, c])
    assert x(0) == a
    assert x(0.2) == a
    assert x(0.4) == b
    assert x(0.6) == b
    assert x(0.8) == c
    assert x(1) == c

def test_threshold_7():
    x = scaleThreshold().domain(["10", "2"]).range(new Set([0, 1, 2]))
    assert x.range() == [0, 1, 2])

def test_threshold_8():
    a = {}, b = {}, c = {}, x = scaleThreshold().domain([1/3, 2/3]).range([a, b, c])
    assert x.invertExtent(a) == [None, 1/3])
    assert x.invertExtent(b) == [1/3, 2/3])
    assert x.invertExtent(c) == [2/3, None])
    assert.deepStrictEqual(x.invertExtent({}), [None, None])
