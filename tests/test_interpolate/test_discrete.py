import detroit as d3
import math


def test_discrete_1():
    i = d3.interpolate_discrete(list("abcde"))
    assert i(-1) == "a"
    assert i(0) == "a"
    assert i(0.19) == "a"
    assert i(0.21) == "b"
    assert i(1) == "e"


def test_discrete_2():
    i = d3.interpolate_discrete([0, 1])
    assert i(-1) == 0
    assert i(0) == 0
    assert i(0.49) == 0
    assert i(0.51) == 1
    assert i(1) == 1
    assert i(2) == 1


# def test_discrete_3():
#     i = d3.interpolate_discrete([0, 1])
#     assert i(math.nan) == None
