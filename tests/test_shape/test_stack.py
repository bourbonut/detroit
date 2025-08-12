import detroit as d3
from detroit.shape.series import Serie, Series


def make_series(series, data, key, index):
    series = Series([Serie(value, d) for value, d in zip(series, data)])
    series.key = key
    series.index = index
    return series


def round_series(series):
    for serie in series:
        serie[0] = round(serie[0], 6)
        serie[1] = round(serie[1], 6)
    return serie


def test_stack_1():
    s = d3.stack()
    assert s.keys() == []
    assert s.value({"foo": 42}, "foo") == 42
    assert s.order == d3.stack_order_none
    assert s.offset == d3.stack_offset_none


def test_stack_2():
    s = d3.stack().set_keys([0, 1, 2, 3])
    data = [[1, 3, 5, 1], [2, 4, 2, 3], [1, 2, 4, 2]]
    assert s(data) == [
        make_series([[0, 1], [0, 2], [0, 1]], data, 0, 0),
        make_series([[1, 4], [2, 6], [1, 3]], data, 1, 1),
        make_series([[4, 9], [6, 8], [3, 7]], data, 2, 2),
        make_series([[9, 10], [8, 11], [7, 9]], data, 3, 3),
    ]


def test_stack_3():
    s = d3.stack().set_keys(["0.0", "2.0", "4.0"])
    assert s.keys() == ["0.0", "2.0", "4.0"]


def test_stack_4():
    s = d3.stack().set_keys(lambda: list("abc"))
    assert s.keys(), ["a", "b", "c"]


def test_stack_5():
    A = [None]
    B = [None]

    def k(data, a, b):
        A[0] = a
        B[0] = b
        return list(range(len(data[0])))

    s = d3.stack().set_keys(k)
    data = [[1, 3, 5, 1], [2, 4, 2, 3], [1, 2, 4, 2]]
    assert s(data, "foo", "bar") == [
        make_series([[0, 1], [0, 2], [0, 1]], data, 0, 0),
        make_series([[1, 4], [2, 6], [1, 3]], data, 1, 1),
        make_series([[4, 9], [6, 8], [3, 7]], data, 2, 2),
        make_series([[9, 10], [8, 11], [7, 9]], data, 3, 3),
    ]
    assert A[0] == "foo"
    assert B[0] == "bar"


def test_stack_6():
    s = d3.stack().set_value("42.0")
    assert s.value() == 42


def test_stack_7():
    def v():
        return 42

    s = d3.stack().set_value(v)
    assert s.value == v


def test_stack_8():
    actual = {}

    def v(d, k, i, data):
        actual.update({"datum": d, "key": k, "index": i, "data": data})
        return 2

    s = d3.stack().set_keys(["foo"]).set_value(v)
    data = [{"foo": 1}]
    assert s(data) == [make_series([[0, 2]], data, "foo", 0)]


def test_stack_9():
    def v():
        return "2.0"

    s = d3.stack().set_keys(["foo"]).set_value(v)
    data = [{"foo": 1}]
    assert s(data), [make_series([[0, 2]], data, "foo" == 0)]


def test_stack_10():
    s = d3.stack().set_order(None)
    assert s.order == d3.stack_order_none
    assert callable(s.order)


def test_stack_11():
    s = d3.stack().set_keys([0, 1, 2, 3]).set_order(d3.stack_order_reverse)
    data = [[1, 3, 5, 1], [2, 4, 2, 3], [1, 2, 4, 2]]
    assert s.order == d3.stack_order_reverse
    assert s(data) == [
        make_series([[9, 10], [9, 11], [8, 9]], data, 0, 3),
        make_series([[6, 9], [5, 9], [6, 8]], data, 1, 2),
        make_series([[1, 6], [3, 5], [2, 6]], data, 2, 1),
        make_series([[0, 1], [0, 3], [0, 2]], data, 3, 0),
    ]


def test_stack_12():
    s = d3.stack().set_offset(None)
    assert s.offset == d3.stack_offset_none
    assert callable(s.offset)


def test_stack_13():
    s = d3.stack().set_keys([0, 1, 2, 3]).set_offset(d3.stack_offset_expand)
    data = [[1, 3, 5, 1], [2, 4, 2, 3], [1, 2, 4, 2]]
    assert s.offset == d3.stack_offset_expand
    computed = list(map(round_series, s(data)))
    expected = list(
        map(
            round_series,
            [
                make_series(
                    [[0 / 10, 1 / 10], [0 / 11, 2 / 11], [0 / 9, 1 / 9]], data, 0, 0
                ),
                make_series(
                    [[1 / 10, 4 / 10], [2 / 11, 6 / 11], [1 / 9, 3 / 9]], data, 1, 1
                ),
                make_series(
                    [[4 / 10, 9 / 10], [6 / 11, 8 / 11], [3 / 9, 7 / 9]], data, 2, 2
                ),
                make_series(
                    [[9 / 10, 10 / 10], [8 / 11, 11 / 11], [7 / 9, 9 / 9]], data, 3, 3
                ),
            ],
        )
    )
    assert computed == expected
