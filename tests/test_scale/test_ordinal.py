from datetime import datetime
import detroit as d3


def test_ordinal_1():
    s = d3.scale_ordinal()
    assert s.get_domain() == []
    assert s.get_range() == []
    assert s(0) is None
    assert s.get_unknown() is None
    assert s.get_domain() == [0]


def test_ordinal_2():
    s = (
        d3.scale_ordinal()
        .set_domain([0, 1])
        .set_range(["foo", "bar"])
        .set_unknown(None)
    )
    assert s(0) == "foo"
    assert s(1) == "bar"
    s.set_range(["a", "b", "c"])
    assert s(0) == "a"
    assert s("0") == "c"  # TODO : should be None
    assert s((0,)) == "a"  # TODO : should be None
    assert s(1) == "b"
    assert s(1) == "b"
    assert s(2) == "b"  # TODO : should be None


def test_ordinal_3():
    s = d3.scale_ordinal().set_range(["foo", "bar"])
    assert s.get_domain() == []
    assert s(0) == "foo"
    assert s.get_domain() == [0]
    assert s(1) == "bar"
    assert s.get_domain() == [0, 1]
    assert s(0) == "foo"
    assert s.get_domain() == [0, 1]


def test_ordinal_4():
    domain = ["red", "green"]
    s = d3.scale_ordinal().set_domain(domain)
    domain.append("blue")
    assert s.get_domain() == ["red", "green"]


def test_ordinal_5():
    s = d3.scale_ordinal().set_domain(["red", "green"])
    domain = s.get_domain()
    s("blue")
    assert domain == ["red", "green"]


def test_ordinal_6():
    s = d3.scale_ordinal().set_domain({"red", "green"})
    assert sorted(s.get_domain()) == sorted(["red", "green"])


def test_ordinal_7():
    s = d3.scale_ordinal().set_range(["foo", "bar"])
    assert s(1) == "foo"
    assert s(0) == "bar"
    assert s.get_domain() == [1, 0]
    s.set_domain(["0", "1"])
    assert s("0") == "foo"  # it changed!
    assert s("1") == "bar"
    assert s.get_domain() == ["0", "1"]


def test_ordinal_8():
    s = d3.scale_ordinal().set_domain(["foo"]).set_range([42, 43, 44])
    assert s("foo") == 42


def test_ordinal_9():
    s = d3.scale_ordinal().set_domain([0, 1])
    assert s.get_domain() == [0, 1]
    assert isinstance(s.get_domain()[0], int)
    assert isinstance(s.get_domain()[1], int)


def test_ordinal_10():
    s = d3.scale_ordinal()
    s(datetime(1970, 2, 1))
    s(datetime(2001, 4, 13))
    s(datetime(1970, 2, 1))
    s(datetime(2001, 4, 13))
    assert s.get_domain() == [datetime(1970, 2, 1), datetime(2001, 4, 13)]


def test_ordinal_11():
    s = d3.scale_ordinal().set_domain(
        [
            datetime(1970, 3, 1),
            datetime(2001, 5, 13),
            datetime(1970, 3, 1),
            datetime(2001, 5, 13),
        ]
    )
    s(datetime(1970, 3, 1))
    s(datetime(1999, 12, 31))
    assert s.get_domain() == [
        datetime(1970, 3, 1),
        datetime(2001, 5, 13),
        datetime(1999, 12, 31),
    ]


def test_ordinal_12():
    s = d3.scale_ordinal()
    s("foo")
    s("bar")
    s("baz")
    assert s.get_domain() == ["foo", "bar", "baz"]
    s.set_domain(["baz", "bar"])
    s("foo")
    assert s.get_domain() == ["baz", "bar", "foo"]
    s.set_domain(["baz", "foo"])
    assert s.get_domain() == ["baz", "foo"]
    s.set_domain([])
    s("foo")
    s("bar")
    assert s.get_domain() == ["foo", "bar"]


def test_ordinal_13():
    range_ = ["red", "green"]
    s = d3.scale_ordinal().set_range(range_)
    range_.append("blue")
    assert s.get_range() == ["red", "green"]


def test_ordinal_14():
    s = d3.scale_ordinal().set_range({"red", "green"})
    assert sorted(s.get_range()) == sorted(["red", "green"])


def test_ordinal_15():
    s = d3.scale_ordinal().set_range(["red", "green"])
    range_ = s.get_range()
    assert range_ == ["red", "green"]
    range_.append("blue")
    assert s.get_range() == ["red", "green"]


def test_ordinal_16():
    s = d3.scale_ordinal()
    assert s(0) is None
    assert s(1) is None
    s.set_range(["foo", "bar"])
    assert s(1) == "bar"
    assert s(0) == "foo"


def test_ordinal_17():
    s = d3.scale_ordinal().set_range(["a", "b", "c"])
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
    s = (
        d3.scale_ordinal()
        .set_domain(["foo", "bar"])
        .set_unknown("gray")
        .set_range(["red", "blue"])
    )
    assert s("foo") == "red"
    assert s("bar") == "blue"
    assert s("baz") == "gray"
    assert s("quux") == "gray"


def test_ordinal_19():
    s = (
        d3.scale_ordinal()
        .set_domain(["foo", "bar"])
        .set_unknown(None)
        .set_range(["red", "blue"])
    )
    assert s("baz") == "red"
    assert s.get_domain() == ["foo", "bar", "baz"]


def test_ordinal_20():
    s1 = (
        d3.scale_ordinal()
        .set_domain([1, 2])
        .set_range(["red", "green"])
        .set_unknown("gray")
    )
    s2 = s1.copy()
    assert s2.get_domain() == s1.get_domain()
    assert s2.get_range() == s1.get_range()
    assert s2.get_unknown() == s1.get_unknown()


def test_ordinal_21():
    s1 = d3.scale_ordinal().set_range(["foo", "bar"])
    s2 = s1.copy()
    s1.set_domain([1, 2])
    assert s2.get_domain() == []
    assert s1(1) == "foo"
    assert s2(1) == "foo"
    s2.set_domain([2, 3])
    assert s1(2) == "bar"
    assert s2(2) == "foo"
    assert s1.get_domain() == [1, 2]
    assert s2.get_domain() == [2, 3]


def test_ordinal_22():
    s1 = d3.scale_ordinal().set_range(["foo", "bar"])
    s2 = s1.copy()
    s1.set_range(["bar", "foo"])
    assert s1(1) == "bar"
    assert s2(1) == "foo"
    assert s2.get_range() == ["foo", "bar"]
    s2.set_range(["foo", "baz"])
    assert s1(2) == "foo"
    assert s2(2) == "baz"
    assert s1.get_range() == ["bar", "foo"]
    assert s2.get_range() == ["foo", "baz"]
