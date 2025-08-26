from operator import itemgetter

from detroit.array import argpass


def test_argpass_1():
    args = [10, 1, [0, 10, 20]]

    def f(d, i):
        return d + i

    assert argpass(f) == f
    assert argpass(f)(*args) == 11


def test_argpass_2():
    get_x = itemgetter(0)
    args = [[0.2, -0.8], 0, [[0.2, -0.8], [0.9, 0.7]]]
    assert argpass(get_x) == get_x
    assert argpass(get_x)(*args) == 0.2
