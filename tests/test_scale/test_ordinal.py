import detroit as d3

def test_ordinal_1():
    s = scaleOrdinal()
    assert s.domain() == [])
    assert s.range() == [])
    assert s(0) == None
    assert s.unknown() == scaleImplicit
    assert s.domain() == [0])

def test_ordinal_2():
    s = scaleOrdinal().domain([0, 1]).range(["foo", "bar"]).unknown(None)
    assert s(0) == "foo"
    assert s(1) == "bar"
    s.range(["a", "b", "c"])
    assert s(0) == "a"
    assert s("0") == None
    assert.strictEqual(s([0]), None)
    assert s(1) == "b"
    assert s(new Number(1)) == "b"
    assert s(2) == None

def test_ordinal_3():
    s = scaleOrdinal().range(["foo", "bar"])
    assert s.domain() == [])
    assert s(0) == "foo"
    assert s.domain() == [0])
    assert s(1) == "bar"
    assert s.domain() == [0, 1])
    assert s(0) == "foo"
    assert s.domain() == [0, 1])

def test_ordinal_4():
    domain = ["red", "green"]
    s = scaleOrdinal().domain(domain)
    domain.push("blue")
    assert s.domain() == ["red", "green"])

def test_ordinal_5():
    s = scaleOrdinal().domain(["red", "green"])
    domain = s.domain()
    s("blue")
    assert domain == ["red", "green"])

def test_ordinal_6():
    s = scaleOrdinal().domain(new Set(["red", "green"]))
    assert s.domain() == ["red", "green"])

def test_ordinal_7():
    s = scaleOrdinal().range(["foo", "bar"])
    assert s(1) == "foo"
    assert s(0) == "bar"
    assert s.domain() == [1, 0])
    s.domain(["0", "1"])
    assert s("0") == "foo" // it changed!
    assert s("1") == "bar"
    assert s.domain() == ["0", "1"])

def test_ordinal_8():
    s = scaleOrdinal().domain(["foo"]).range([42, 43, 44])
    assert s(new String("foo")) == 42
    assert.strictEqual(s({valueOf: function() { return "foo" }}), 42)
    assert.strictEqual(s({valueOf: function() { return "bar" }}), 43)

def test_ordinal_9():
    s = scaleOrdinal().domain([0, 1])
    assert s.domain() == [0, 1])
    assert.strictEqual(typeof s.domain()[0], "number")
    assert.strictEqual(typeof s.domain()[1], "number")

def test_ordinal_10():
    s = scaleOrdinal().domain(["__proto__", "hasOwnProperty"]).range([42, 43])
    assert.strictEqual(s("__proto__"), 42)
    assert s("hasOwnProperty") == 43
    assert s.domain() == ["__proto__", "hasOwnProperty"])

def test_ordinal_11():
    s = scaleOrdinal()
    s(new Date(1970, 2, 1))
    s(new Date(2001, 4, 13))
    s(new Date(1970, 2, 1))
    s(new Date(2001, 4, 13))
    assert s.domain() == [new Date(1970, 2, 1), new Date(2001, 4, 13)])

def test_ordinal_12():
    s = scaleOrdinal().domain([
        new Date(1970, 2, 1),
        new Date(2001, 4, 13),
        new Date(1970, 2, 1),
        new Date(2001, 4, 13)
    ])
    s(new Date(1970, 2, 1))
    s(new Date(1999, 11, 31))
    assert s.domain() == [new Date(1970, 2, 1), new Date(2001, 4, 13), new Date(1999, 11, 31)])

def test_ordinal_13():
    s = scaleOrdinal().domain(["__proto__", "hasOwnProperty"]).range([42, 43])
    assert.strictEqual(s("__proto__"), 42)
    assert s("hasOwnProperty") == 43
    assert s.domain() == ["__proto__", "hasOwnProperty"])

def test_ordinal_14():
    s = scaleOrdinal()
    s("foo")
    s("bar")
    s("baz")
    assert s.domain() == ["foo", "bar", "baz"])
    s.domain(["baz", "bar"])
    s("foo")
    assert s.domain() == ["baz", "bar", "foo"])
    s.domain(["baz", "foo"])
    assert s.domain() == ["baz", "foo"])
    s.domain([])
    s("foo")
    s("bar")
    assert s.domain() == ["foo", "bar"])

def test_ordinal_15():
    range = ["red", "green"]
    s = scaleOrdinal().range(range)
    range.push("blue")
    assert s.range() == ["red", "green"])

def test_ordinal_16():
    s = scaleOrdinal().range(new Set(["red", "green"]))
    assert s.range() == ["red", "green"])

def test_ordinal_17():
    s = scaleOrdinal().range(["red", "green"])
    range = s.range()
    assert range == ["red", "green"])
    range.push("blue")
    assert s.range() == ["red", "green"])

def test_ordinal_18():
    s = scaleOrdinal()
    assert s(0) == None
    assert s(1) == None
    s.range(["foo", "bar"])
    assert s(1) == "bar"
    assert s(0) == "foo"

def test_ordinal_19():
    s = scaleOrdinal().range(["a", "b", "c"])
    assert s(0) == "a"
    assert s(1) == "b"
    assert s(2) == "c"
    assert s(3) == "a"
    assert s(4) == "b"
    assert s(5) == "c"
    assert s(2) == "c"
    assert s(1) == "b"
    assert s(0) == "a"

def test_ordinal_20():
    s = scaleOrdinal().domain(["foo", "bar"]).unknown("gray").range(["red", "blue"])
    assert s("foo") == "red"
    assert s("bar") == "blue"
    assert s("baz") == "gray"
    assert s("quux") == "gray"

def test_ordinal_21():
    s = scaleOrdinal().domain(["foo", "bar"]).unknown(None).range(["red", "blue"])
    assert s("baz") == None
    assert s.domain() == ["foo", "bar"])

def test_ordinal_22():
    s1 = scaleOrdinal().domain([1, 2]).range(["red", "green"]).unknown("gray")
    s2 = s1.copy()
    assert s2.domain() == s1.domain()
    assert s2.range() == s1.range()
    assert s2.unknown() == s1.unknown()

def test_ordinal_23():
    s1 = scaleOrdinal().range(["foo", "bar"])
    s2 = s1.copy()
    s1.domain([1, 2])
    assert s2.domain() == [])
    assert s1(1) == "foo"
    assert s2(1) == "foo"
    s2.domain([2, 3])
    assert s1(2) == "bar"
    assert s2(2) == "foo"
    assert s1.domain() == [1, 2])
    assert s2.domain() == [2, 3])

def test_ordinal_24():
    s1 = scaleOrdinal().range(["foo", "bar"])
    s2 = s1.copy()
    s1.range(["bar", "foo"])
    assert s1(1) == "bar"
    assert s2(1) == "foo"
    assert s2.range() == ["foo", "bar"])
    s2.range(["foo", "baz"])
    assert s1(2) == "foo"
    assert s2(2) == "baz"
    assert s1.range() == ["bar", "foo"])
    assert s2.range() == ["foo", "baz"])
