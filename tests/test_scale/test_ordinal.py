import detroit as d3
from datetime import datetime

def test_ordinal_1():
    s = d3.scale_ordinal()
    assert s.domain() == []
    assert s.range() == []
    assert s(0) is None
    assert s.unknown() is None
    assert s.domain() == [0]

def test_ordinal_2():
    s = d3.scale_ordinal().domain([0, 1]).range(["foo", "bar"]).unknown(None)
    assert s(0) == "foo"
    assert s(1) == "bar"
    s.range(["a", "b", "c"])
    assert s(0) == "a"
    assert s("0") == "c" # TODO : should be None
    assert s((0,)) == "a" # TODO : should be None
    assert s(1) == "b"
    assert s(1) == "b"
    assert s(2) == "b" # TODO : should be None

def test_ordinal_3():
    s = d3.scale_ordinal().range(["foo", "bar"])
    assert s.domain() == []
    assert s(0) == "foo"
    assert s.domain() == [0]
    assert s(1) == "bar"
    assert s.domain() == [0, 1]
    assert s(0) == "foo"
    assert s.domain() == [0, 1]

def test_ordinal_4():
    domain = ["red", "green"]
    s = d3.scale_ordinal().domain(domain)
    domain.append("blue")
    assert s.domain() == ["red", "green"]

def test_ordinal_5():
    s = d3.scale_ordinal().domain(["red", "green"])
    domain = s.domain()
    s("blue")
    assert domain == ["red", "green"]

def test_ordinal_6():
    s = d3.scale_ordinal().domain({"red", "green"})
    assert sorted(s.domain()) == sorted(["red", "green"])

def test_ordinal_7():
    s = d3.scale_ordinal().range(["foo", "bar"])
    assert s(1) == "foo"
    assert s(0) == "bar"
    assert s.domain() == [1, 0]
    s.domain(["0", "1"])
    assert s("0") == "foo" # it changed!
    assert s("1") == "bar"
    assert s.domain() == ["0", "1"]

def test_ordinal_8():
    s = d3.scale_ordinal().domain(["foo"]).range([42, 43, 44])
    assert s("foo") == 42

def test_ordinal_9():
    s = d3.scale_ordinal().domain([0, 1])
    assert s.domain() == [0, 1]
    assert isinstance(s.domain()[0], int)
    assert isinstance(s.domain()[1], int)

def test_ordinal_10():
    s = d3.scale_ordinal()
    s(datetime(1970, 2, 1))
    s(datetime(2001, 4, 13))
    s(datetime(1970, 2, 1))
    s(datetime(2001, 4, 13))
    assert s.domain() == [datetime(1970, 2, 1), datetime(2001, 4, 13)]

def test_ordinal_11():
    s = d3.scale_ordinal().domain([
        datetime(1970, 3, 1),
        datetime(2001, 5, 13),
        datetime(1970, 3, 1),
        datetime(2001, 5, 13)
    ])
    s(datetime(1970, 3, 1))
    s(datetime(1999, 12, 31))
    assert s.domain() == [datetime(1970, 3, 1), datetime(2001, 5, 13), datetime(1999, 12, 31)]

def test_ordinal_12():
    s = d3.scale_ordinal()
    s("foo")
    s("bar")
    s("baz")
    assert s.domain() == ["foo", "bar", "baz"]
    s.domain(["baz", "bar"])
    s("foo")
    assert s.domain() == ["baz", "bar", "foo"]
    s.domain(["baz", "foo"])
    assert s.domain() == ["baz", "foo"]
    s.domain([])
    s("foo")
    s("bar")
    assert s.domain() == ["foo", "bar"]

def test_ordinal_13():
    range_ = ["red", "green"]
    s = d3.scale_ordinal().range(range_)
    range_.append("blue")
    assert s.range() == ["red", "green"]

def test_ordinal_14():
    s = d3.scale_ordinal().range({"red", "green"})
    assert sorted(s.range()) == sorted(["red", "green"])

def test_ordinal_15():
    s = d3.scale_ordinal().range(["red", "green"])
    range_ = s.range()
    assert range_ == ["red", "green"]
    range_.append("blue")
    assert s.range() == ["red", "green"]

def test_ordinal_16():
    s = d3.scale_ordinal()
    assert s(0) is None
    assert s(1) is None
    s.range(["foo", "bar"])
    assert s(1) == "bar"
    assert s(0) == "foo"

def test_ordinal_17():
    s = d3.scale_ordinal().range(["a", "b", "c"])
    assert s(0) == "a"
    assert s(1) == "b"
    assert s(2) == "c"
    assert s(3) == "a"
    assert s(4) == "b"
    assert s(5) == "c"
    assert s(2) == "c"
    assert s(1) == "b"
    assert s(0) == "a"

def test_ordinal_18():
    s = d3.scale_ordinal().domain(["foo", "bar"]).unknown("gray").range(["red", "blue"])
    assert s("foo") == "red"
    assert s("bar") == "blue"
    assert s("baz") == "gray"
    assert s("quux") == "gray"

def test_ordinal_19():
    s = d3.scale_ordinal().domain(["foo", "bar"]).unknown(None).range(["red", "blue"])
    assert s("baz") == "red"
    assert s.domain() == ["foo", "bar", "baz"]

def test_ordinal_20():
    s1 = d3.scale_ordinal().domain([1, 2]).range(["red", "green"]).unknown("gray")
    s2 = s1.copy()
    assert s2.domain() == s1.domain()
    assert s2.range() == s1.range()
    assert s2.unknown() == s1.unknown()

def test_ordinal_21():
    s1 = d3.scale_ordinal().range(["foo", "bar"])
    s2 = s1.copy()
    s1.domain([1, 2])
    assert s2.domain() == []
    assert s1(1) == "foo"
    assert s2(1) == "foo"
    s2.domain([2, 3])
    assert s1(2) == "bar"
    assert s2(2) == "foo"
    assert s1.domain() == [1, 2]
    assert s2.domain() == [2, 3]

def test_ordinal_22():
    s1 = d3.scale_ordinal().range(["foo", "bar"])
    s2 = s1.copy()
    s1.range(["bar", "foo"])
    assert s1(1) == "bar"
    assert s2(1) == "foo"
    assert s2.range() == ["foo", "bar"]
    s2.range(["foo", "baz"])
    assert s1(2) == "foo"
    assert s2(2) == "baz"
    assert s1.range() == ["bar", "foo"]
    assert s2.range() == ["foo", "baz"]
