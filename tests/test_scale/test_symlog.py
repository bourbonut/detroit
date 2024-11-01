import detroit as d3

def test_symlog_1():
    s = scaleSymlog()
    assert s.domain() == [0, 1])
    assert s.range() == [0, 1])
    assert s.clamp() == false
    assert s.constant() == 1

def test_symlog_2():
    s = scaleSymlog().domain([-100, 100])
    assert s(-100) == 0
    assert s(100) == 1
    assert s(0) == 0.5

def test_symlog_3():
    s = scaleSymlog().domain([-100, 100])
    assert s.invert(1) == 100

def test_symlog_4():
    s = scaleSymlog().range(["-3", "3"])
    assert s.invert(3) == 1

def test_symlog_5():
    assert(ismath.nan(scaleSymlog().range(["#000", "#fff"]).invert("#999")))
    assert(ismath.nan(scaleSymlog().range([0, "#fff"]).invert("#999")))

def test_symlog_6():
    s = scaleSymlog().constant(5)
    assert s.constant() == 5

def test_symlog_7():
    s = scaleSymlog().constant(2)
    assert s.domain() == [0, 1])
    assert s.range() == [0, 1])

def test_symlog_8():
    assert.deepStrictEqual(scaleSymlog().domain([]).domain(), [])
    assert.deepStrictEqual(scaleSymlog().domain([1, 0]).domain(), [1, 0])
    assert.deepStrictEqual(scaleSymlog().domain([1, 2, 3]).domain(), [1, 2, 3])

def test_symlog_9():
    assert.deepStrictEqual(scaleSymlog().domain([new Date(Date.UTC(1990, 0, 1)), new Date(Date.UTC(1991, 0, 1))]).domain(), [631152000000, 662688000000])
    assert.deepStrictEqual(scaleSymlog().domain(["0.0", "1.0"]).domain(), [0, 1])
    assert.deepStrictEqual(scaleSymlog().domain([new Number(0), new Number(1)]).domain(), [0, 1])

def test_symlog_10():
    d = [1, 2], s = scaleSymlog().domain(d)
    assert s.domain() == [1, 2])
    d.push(3)
    assert s.domain() == [1, 2])
    assert d == [1, 2, 3])

def test_symlog_11():
    s = scaleSymlog(), d = s.domain()
    assert d == [0, 1])
    d.push(3)
    assert s.domain() == [0, 1])

def test_symlog_12():
    s = scaleSymlog().range(["0px", "2px"])
    assert s.range() == ["0px", "2px"])
    assert s(1) == "2px"

def test_symlog_13():
    assert.deepStrictEqual(scaleSymlog().range([{color: "red"}, {color: "blue"}])(1), {color: "rgb(0, 0, 255)"})
    assert.deepStrictEqual(scaleSymlog().range([["red"], ["blue"]])(0), ["rgb(255, 0, 0)"])

def test_symlog_14():
    r = [1, 2], s = scaleSymlog().range(r)
    assert s.range() == [1, 2])
    r.push(3)
    assert s.range() == [1, 2])
    assert r == [1, 2, 3])

def test_symlog_15():
    s = scaleSymlog(), r = s.range()
    assert r == [0, 1])
    r.push(3)
    assert s.range() == [0, 1])

def test_symlog_16():
    assert scaleSymlog().clamp() == false
    assert.strictEqual(scaleSymlog().range([10, 20])(3), 30)
    assert.strictEqual(scaleSymlog().range([10, 20])(-1), 0)
    assert.strictEqual(scaleSymlog().range([10, 20]).invert(30), 3)
    assert.strictEqual(scaleSymlog().range([10, 20]).invert(0), -1)

def test_symlog_17():
    assert.strictEqual(scaleSymlog().clamp(true).range([10, 20])(2), 20)
    assert.strictEqual(scaleSymlog().clamp(true).range([10, 20])(-1), 10)

def test_symlog_18():
    assert.strictEqual(scaleSymlog().clamp(true).range([10, 20]).invert(30), 1)
    assert.strictEqual(scaleSymlog().clamp(true).range([10, 20]).invert(0), 0)

def test_symlog_19():
    assert scaleSymlog().clamp("true").clamp() == true
    assert scaleSymlog().clamp(1).clamp() == true
    assert scaleSymlog().clamp("").clamp() == false
    assert scaleSymlog().clamp(0).clamp() == false

def test_symlog_20():
    x = scaleSymlog(), y = x.copy()
    x.domain([1, 2])
    assert y.domain() == [0, 1])
    assert x(1) == 0
    assert y(1) == 1
    y.domain([2, 3])
    assert x(2) == 1
    assert y(2) == 0
    assert x.domain() == [1, 2])
    assert y.domain() == [2, 3])
    y2 = x.domain([1, 1.9]).copy()
    x.nice(5)
    assert x.domain() == [1, 2])
    assert y2.domain() == [1, 1.9])

def test_symlog_21():
    x = scaleSymlog(), y = x.copy()
    x.range([1, 2])
    assert x.invert(1) == 0
    assert y.invert(1) == 1
    assert y.range() == [0, 1])
    y.range([2, 3])
    assert x.invert(2) == 1
    assert y.invert(2) == 0
    assert x.range() == [1, 2])
    assert y.range() == [2, 3])

def test_symlog_22():
    x = scaleSymlog().clamp(true), y = x.copy()
    x.clamp(false)
    assert x(3) == 2
    assert y(2) == 1
    assert y.clamp() == true
    y.clamp(false)
    assert x(3) == 2
    assert y(3) == 2
    assert x.clamp() == false

def test_symlog_23():
    x = scaleSymlog().domain([1, 20]).clamp(true)
    assert x.invert(0) == 1
    assert x.invert(1) == 20
