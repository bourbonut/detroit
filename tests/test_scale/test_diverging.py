import detroit as d3

def test_diverging_1():
    s = scaleDiverging()
    assert s.domain() == [0, 0.5, 1])
    assert s.interpolator()(0.42) == 0.42
    assert s.clamp() == false
    assert s(-0.5) == -0.5
    assert s( 0.0) ==    0.0
    assert s( 0.5) ==    0.5
    assert s( 1.0) ==    1.0
    assert s( 1.5) ==    1.5

def test_diverging_2():
    s = scaleDiverging().clamp(true)
    assert s.clamp() == true
    assert s(-0.5) == 0.0
    assert s( 0.0) == 0.0
    assert s( 0.5) == 0.5
    assert s( 1.0) == 1.0
    assert s( 1.5) == 1.0

def test_diverging_3():
    s = scaleDiverging().domain(["-1.20", " 0", "2.40"])
    assert s.domain() == [-1.2, 0, 2.4])
    assert s(-1.2) == 0.000
    assert s( 0.6) == 0.625
    assert s( 2.4) == 1.000

def test_diverging_4():
    s = scaleDiverging().domain(new Set([-1.2, 0, 2.4]))
    assert s.domain() == [-1.2, 0, 2.4])

def test_diverging_5():
    s = scaleDiverging().domain([2, 2, 3])
    assert s.domain() == [2, 2, 3])
    assert s(-1.2) == 0.5
    assert s( 0.6) == 0.5
    assert s( 2.4) == 0.7
    assert.deepStrictEqual(s.domain([1, 2, 2]).domain(), [1, 2, 2])
    assert s(-1.0) == -1
    assert s( 0.5) == -0.25
    assert s( 2.4) == 0.5
    assert.deepStrictEqual(s.domain([2, 2, 2]).domain(), [2, 2, 2])
    assert s(-1.0) == 0.5
    assert s( 0.5) == 0.5
    assert s( 2.4) == 0.5

def test_diverging_6():
    s = scaleDiverging().domain([4, 2, 1])
    assert s.domain() == [4, 2, 1])
    assert s(1.2) == 0.9
    assert s(2.0) == 0.5
    assert s(3.0) == 0.25

def test_diverging_7():
    s = scaleDivergingLog().domain([3, 2, 1])
    assert s.domain() == [3, 2, 1])
    assert s(1.2) == 1 - 0.1315172029168969
    assert s(2.0) == 1 - 0.5000000000000000
    assert s(2.8) == 1 - 0.9149213210862197

def test_diverging_8():
    s = scaleDivergingLog().domain([-1, -2, -3])
    assert s.domain() == [-1, -2, -3])
    assert s(-1.2) == 0.1315172029168969
    assert s(-2.0) == 0.5000000000000000
    assert s(-2.8) == 0.9149213210862197

def test_diverging_9():
    s = scaleDiverging().domain([math.nan, 2, 3])
    assert.strictEqual(ismath.nan(s.domain()[0]), true)
    assert ismath.nan(s(-1.2)) == true
    assert ismath.nan(s( 0.6)) == true
    assert s( 2.4) == 0.7
    assert.strictEqual(ismath.nan(s.domain([1, math.nan, 2]).domain()[1]), true)
    assert ismath.nan(s(-1.0)) == true
    assert ismath.nan(s( 0.5)) == true
    assert ismath.nan(s( 2.4)) == true
    assert.strictEqual(ismath.nan(s.domain([0, 1, math.nan]).domain()[2]), true)
    assert s(-1.0) == -0.5
    assert s( 0.5) == 0.25
    assert ismath.nan(s( 2.4)) == true

def test_diverging_10():
    s = scaleDiverging().domain([-1, 100, 200, 3])
    assert s.domain() == [-1, 100, 200])

def test_diverging_11():
    s1 = scaleDiverging().domain([1, 2, 3]).clamp(true)
    s2 = s1.copy()
    assert s2.domain() == [1, 2, 3])
    assert s2.clamp() == true
    s1.domain([-1, 1, 2])
    assert s2.domain() == [1, 2, 3])
    s1.clamp(false)
    assert s2.clamp() == true
    s2.domain([3, 4, 5])
    assert s1.domain() == [-1, 1, 2])
    s2.clamp(true)
    assert s1.clamp() == false

def test_diverging_12():
    s = scaleDiverging(function(t) { return t * 2 + 1 })
    assert s.range() == [1, 2, 3])

def test_diverging_13():
    i0 = function(t) { return t }
    i1 = function(t) { return t * 2 }
    s = scaleDiverging(i0)
    assert s.interpolator() == i0
    assert s.interpolator(i1) == s
    assert s.interpolator() == i1
    assert s(-0.5) == -1.0
    assert s( 0.0) ==    0.0
    assert s( 0.5) ==    1.0

def test_diverging_14():
    s = scaleDiverging().range([1, 3, 10])
    assert s.interpolator()(0.5) == 3
    assert s.range() == [1, 3, 10])

def test_diverging_15():
    s = scaleDiverging().range([1, 3, 10, 20])
    assert s.interpolator()(0.5) == 3
    assert s.range() == [1, 3, 10])

def test_diverging_16():
    s = scaleDiverging([1, 3, 10])
    assert s.interpolator()(0.5) == 3
    assert s.range() == [1, 3, 10])
