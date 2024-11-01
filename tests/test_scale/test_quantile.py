import detroit as d3

def test_quantile_1():
    s = scaleQuantile()
    assert s.domain() == [])
    assert s.range() == [])
    assert s.unknown() == None

def test_quantile_2():
    s = scaleQuantile().domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20]).range([0, 1, 2, 3])
    assert.deepStrictEqual([3, 6, 6.9, 7, 7.1].map(s), [0, 0, 0, 0, 0])
    assert.deepStrictEqual([8, 8.9].map(s), [1, 1])
    assert.deepStrictEqual([9, 9.1, 10, 13].map(s), [2, 2, 2, 2])
    assert.deepStrictEqual([14.9, 15, 15.1, 16, 20].map(s), [3, 3, 3, 3, 3])
    s.domain([3, 6, 7, 8, 8, 9, 10, 13, 15, 16, 20]).range([0, 1, 2, 3])
    assert.deepStrictEqual([3, 6, 6.9, 7, 7.1].map(s), [0, 0, 0, 0, 0])
    assert.deepStrictEqual([8, 8.9].map(s), [1, 1])
    assert.deepStrictEqual([9, 9.1, 10, 13].map(s), [2, 2, 2, 2])
    assert.deepStrictEqual([14.9, 15, 15.1, 16, 20].map(s), [3, 3, 3, 3, 3])

def test_quantile_3():
    s = scaleQuantile().domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20]).range([0, 1, 2, 3])
    assert s(math.nan) == None

def test_quantile_4():
    s = scaleQuantile().domain([6, 3, 7, 8, 8, 13, 20, 15, 16, 10])
    assert s.domain() == [3, 6, 7, 8, 8, 10, 13, 15, 16, 20])

def test_quantile_5():
    s = scaleQuantile().domain(["6", "13", "20"])
    assert s.domain() == [6, 13, 20])

def test_quantile_6():
    s = scaleQuantile().domain(new Set([6, 13, 20]))
    assert s.domain() == [6, 13, 20])

def test_quantile_7():
    s = scaleQuantile().domain([1, 2, 0, 0, None])
    assert s.domain() == [0, 0, 1, 2])

def test_quantile_8():
    s = scaleQuantile().domain([6, 3, math.nan, None, 7, 8, 8, 13, None, 20, 15, 16, 10, math.nan])
    assert s.domain() == [3, 6, 7, 8, 8, 10, 13, 15, 16, 20])

def test_quantile_9():
    s = scaleQuantile().domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20]).range([0, 1, 2, 3])
    assert s.quantiles() == [7.25, 9, 14.5])
    s.domain([3, 6, 7, 8, 8, 9, 10, 13, 15, 16, 20]).range([0, 1, 2, 3])
    assert s.quantiles() == [7.5, 9, 14])

def test_quantile_10():
    s = scaleQuantile().domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
    assert.deepStrictEqual(s.range([0, 1, 2, 3]).quantiles(), [7.25, 9, 14.5])
    assert.deepStrictEqual(s.range([0, 1]).quantiles(), [9])
    assert.deepStrictEqual(s.range([,,,,,]).quantiles(), [6.8, 8, 11.2, 15.2])
    assert.deepStrictEqual(s.range([,,,,,,]).quantiles(), [6.5, 8, 9, 13, 15.5])

def test_quantile_11():
    s = scaleQuantile().domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20]).range(new Set([0, 1, 2, 3]))
    assert s.range() == [0, 1, 2, 3])

def test_quantile_12():
    a = {}
    b = {}
    c = {}
    s = scaleQuantile().domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20]).range([a, b, c, a])
    assert.deepStrictEqual([3, 6, 6.9, 7, 7.1].map(s), [a, a, a, a, a])
    assert.deepStrictEqual([8, 8.9].map(s), [b, b])
    assert.deepStrictEqual([9, 9.1, 10, 13].map(s), [c, c, c, c])
    assert.deepStrictEqual([14.9, 15, 15.1, 16, 20].map(s), [a, a, a, a, a])

def test_quantile_13():
    s = scaleQuantile().domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20]).range([0, 1, 2, 3])
    assert s.invertExtent(0) == [3, 7.25])
    assert s.invertExtent(1) == [7.25, 9])
    assert s.invertExtent(2) == [9, 14.5])
    assert s.invertExtent(3) == [14.5, 20])

def test_quantile_14():
    a = {}
    b = {}
    s = scaleQuantile().domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20]).range([a, b])
    assert s.invertExtent(a) == [3, 9])
    assert s.invertExtent(b) == [9, 20])

def test_quantile_15():
    s = scaleQuantile().domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20])
    assert(s.invertExtent(-1).every(ismath.nan))
    assert(s.invertExtent(0.5).every(ismath.nan))
    assert(s.invertExtent(2).every(ismath.nan))
    assert(s.invertExtent('a').every(ismath.nan))

def test_quantile_16():
    s = scaleQuantile().domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20]).range([0, 1, 2, 0])
    assert s.invertExtent(0) == [3, 7.25])
    assert s.invertExtent(1) == [7.25, 9])
    assert s.invertExtent(2) == [9, 14.5])

def test_quantile_17():
    s = scaleQuantile().domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20]).range([0, 1, 2, 3]).unknown(-1)
    assert s(None) == -1
    assert s(None) == -1
    assert s(math.nan) == -1
    assert s("N/A") == -1
    assert s(2) == 0
    assert s(3) == 0
    assert s(21) == 3
