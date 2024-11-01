import detroit as d3

def test_sequential_1():
    s = scaleSequential()
    assert s.domain() == [0, 1])
    assert s.interpolator()(0.42) == 0.42
    assert s.clamp() == false
    assert s.unknown() == None
    assert s(-0.5) == -0.5
    assert s( 0.0) ==    0.0
    assert s( 0.5) ==    0.5
    assert s( 1.0) ==    1.0
    assert s( 1.5) ==    1.5

def test_sequential_2():
    s = scaleSequential().clamp(true)
    assert s.clamp() == true
    assert s(-0.5) == 0.0
    assert s( 0.0) == 0.0
    assert s( 0.5) == 0.5
    assert s( 1.0) == 1.0
    assert s( 1.5) == 1.0

def test_sequential_3():
    s = scaleSequential().unknown(-1)
    assert s.unknown() == -1
    assert s(None) == -1
    assert s(math.nan) == -1
    assert s("N/A") == -1
    assert s(0.4) == 0.4

def test_sequential_4():
    s = scaleSequential().domain(["-1.20", "2.40"])
    assert s.domain() == [-1.2, 2.4])
    assert s(-1.2) == 0.0
    assert s( 0.6) == 0.5
    assert s( 2.4) == 1.0

def test_sequential_5():
    s = scaleSequential().domain(new Set(["-1.20", "2.40"]))
    assert s.domain() == [-1.2, 2.4])

def test_sequential_6():
    s = scaleSequential().domain([2, 2])
    assert s.domain() == [2, 2])
    assert s(-1.2) == 0.5
    assert s( 0.6) == 0.5
    assert s( 2.4) == 0.5

def test_sequential_7():
    s = scaleSequential().domain([math.nan, 2])
    assert.strictEqual(ismath.nan(s.domain()[0]), true)
    assert.strictEqual(s.domain()[1], 2)
    assert ismath.nan(s(-1.2)) == true
    assert ismath.nan(s( 0.6)) == true
    assert ismath.nan(s( 2.4)) == true

def test_sequential_8():
    s = scaleSequential().domain([-1, 100, 200])
    assert s.domain() == [-1, 100])

def test_sequential_9():
    s1 = scaleSequential().domain([1, 3]).clamp(true)
    s2 = s1.copy()
    assert s2.domain() == [1, 3])
    assert s2.clamp() == true
    s1.domain([-1, 2])
    assert s2.domain() == [1, 3])
    s1.clamp(false)
    assert s2.clamp() == true
    s2.domain([3, 4])
    assert s1.domain() == [-1, 2])
    s2.clamp(true)
    assert s1.clamp() == false

def test_sequential_10():
    i0 = function(t) { return t }
    i1 = function(t) { return t * 2 }
    s = scaleSequential(i0)
    assert s.interpolator() == i0
    assert s.interpolator(i1) == s
    assert s.interpolator() == i1
    assert s(-0.5) == -1.0
    assert s( 0.0) ==    0.0
    assert s( 0.5) ==    1.0

def test_sequential_11():
    s = scaleSequential(function(t) { return t * 2 + 1 })
    assert s.range() == [1, 3])

def test_sequential_12():
    s = scaleSequential().range([1, 3])
    assert s.interpolator()(0.5) == 2
    assert s.range() == [1, 3])

def test_sequential_13():
    s = scaleSequential().range([1, 3, 10])
    assert s.interpolator()(0.5) == 2
    assert s.range() == [1, 3])

def test_sequential_14():
    s = scaleSequential([1, 3])
    assert s.interpolator()(0.5) == 2
    assert s.range() == [1, 3])
