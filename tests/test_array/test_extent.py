import math

import detroit as d3


def box(obj):
    return {"value": obj}


def unbox(obj, *args):
    return obj["value"]


def test_extent_1():
    assert d3.extent([1]) == [1, 1]
    assert d3.extent([5, 1, 2, 3, 4]) == [1, 5]
    assert d3.extent([20, 3]) == [3, 20]
    assert d3.extent([3, 20]) == [3, 20]


def test_extent_2():
    assert d3.extent(["c", "a", "b"]) == ["a", "c"]
    assert d3.extent(["20", "3"]) == ["20", "3"]
    assert d3.extent(["3", "20"]) == ["20", "3"]


def test_extent_3():
    assert d3.extent([20, 3]) == [3, 20]
    assert d3.extent([20, 3]) == [3, 20]


def test_extent_none_1():
    assert d3.extent([math.nan, 1, 2, 3, 4, 5]) == [1, 5]
    assert d3.extent([1, 2, 3, 4, 5, math.nan]) == [1, 5]
    assert d3.extent([10, None, 3, None, 5, math.nan]) == [3, 10]
    assert d3.extent([-1, None, -3, None, -5, math.nan]) == [-5, -1]


def test_extent_none_2():
    assert d3.extent([]) == [None, None]
    assert d3.extent([None]) == [None, None]
    assert d3.extent([math.nan]) == [None, None]
    assert d3.extent([math.nan, math.nan]) == [None, None]


def test_extent_list():
    assert d3.extent(list(map(box, [1])), unbox) == [1, 1]
    assert d3.extent(list(map(box, [5, 1, 2, 3, 4])), unbox) == [1, 5]
    assert d3.extent(list(map(box, [20, 3])), unbox) == [3, 20]
    assert d3.extent(list(map(box, [3, 20])), unbox) == [3, 20]
    assert d3.extent(list(map(box, ["c", "a", "b"])), unbox) == ["a", "c"]
    assert d3.extent(list(map(box, ["20", "3"])), unbox) == ["20", "3"]
    assert d3.extent(list(map(box, ["3", "20"])), unbox) == ["20", "3"]


def test_extent_list_none_1():
    assert d3.extent(list(map(box, [math.nan, 1, 2, 3, 4, 5])), unbox) == [1, 5]
    assert d3.extent(list(map(box, [1, 2, 3, 4, 5, math.nan])), unbox) == [1, 5]
    assert d3.extent(list(map(box, [10, None, 3, None, 5, math.nan])), unbox) == [3, 10]
    assert d3.extent(list(map(box, [-1, None, -3, None, -5, math.nan])), unbox) == [
        -5,
        -1,
    ]


def test_extent_list_none_2():
    assert d3.extent(list(map(box, [])), unbox) == [None, None]
    assert d3.extent(list(map(box, [None])), unbox) == [None, None]
    assert d3.extent(list(map(box, [None])), unbox) == [None, None]
    assert d3.extent(list(map(box, [math.nan])), unbox) == [None, None]
    assert d3.extent(list(map(box, [math.nan, math.nan])), unbox) == [None, None]


def test_extent_result_1():
    results = []
    array = ["a", "b", "c"]
    d3.extent(array, lambda d, i, array: results.append([d, i, array]))
    assert results == [["a", 0, array], ["b", 1, array], ["c", 2, array]]


def test_extent_result_2():
    results = []
    d3.extent([1, 2], lambda d, i, array: results.append(None))
    assert results == [None, None]
