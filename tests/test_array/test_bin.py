import math

import pytest

import detroit as d3
from detroit import ticks
from detroit.array.bin import Bin
from detroit.array.threshold import threshold_sturges


def box(bin_values, x0, x1):
    bin = Bin()
    bin._list = bin_values
    bin.x0 = x0
    bin.x1 = x1
    return bin


def test_bin_simple():
    h = d3.bin()
    assert h.get_value()(42) == 42
    assert h.get_domain() == d3.extent
    assert h.get_thresholds() == threshold_sturges


def test_bin_1():
    h = d3.bin()
    assert h([0, 0, 0, 10, 20, 20]) == [
        box([0, 0, 0], 0, 5),
        box([], 5, 10),
        box([10], 10, 15),
        box([], 15, 20),
        box([20, 20], 20, 25),
    ]


def test_bin_2():
    h = d3.bin()
    assert h(iter([0, 0, 0, 10, 20, 20])) == [
        box([0, 0, 0], 0, 5),
        box([], 5, 10),
        box([10], 10, 15),
        box([], 15, 20),
        box([20, 20], 20, 25),
    ]


def test_bin_3():
    with pytest.raises(ValueError):
        h = d3.bin().set_value(lambda d, i, data: 12)  # Pointless, but for consistency.
        assert h([0, 0, 0, 1, 2, 2]) == [
            box([0, 0, 0, 1, 2, 2], 12, 12),
        ]


def test_bin_4():
    h = d3.bin()
    assert h([0, None, None, math.nan, 10, 20, 20]) == [
        box([0], 0, 5),
        box([], 5, 10),
        box([10], 10, 15),
        box([], 15, 20),
        box([20, 20], 20, 25),
    ]


def test_bin_5():
    h = d3.bin().set_value(lambda d: d["value"])
    a = {"value": 0}
    b = {"value": 10}
    c = {"value": 20}
    assert h([a, a, a, b, c, c]) == [
        box([a, a, a], 0, 5),
        box([], 5, 10),
        box([b], 10, 15),
        box([], 15, 20),
        box([c, c], 20, 25),
    ]


def test_bin_6():
    h = d3.bin().set_domain([0, 20])
    assert list(h.get_domain()()) == [0, 20]
    assert h([1, 2, 2, 10, 18, 18]) == [
        box([1, 2, 2], 0, 5),
        box([], 5, 10),
        box([10], 10, 15),
        box([18, 18], 15, 20),
    ]


def test_bin_7():
    values = [1, 2, 2, 10, 18, 18]
    actual = []

    def domain(values):
        actual[:] = values
        return [0, 20]

    h = d3.bin().set_domain(domain)
    assert h.get_domain() == domain
    assert h(values) == [
        box([1, 2, 2], 0, 5),
        box([], 5, 10),
        box([10], 10, 15),
        box([18, 18], 15, 20),
    ]
    assert actual == values


def test_bin_8():
    h = d3.bin().set_thresholds(3)
    assert h([0, 0, 0, 10, 30, 30]) == [
        box([0, 0, 0], 0, 10),
        box([10], 10, 20),
        box([], 20, 30),
        box([30, 30], 30, 40),
    ]


def test_bin_9():
    h = d3.bin().set_thresholds([10, 20])
    assert h([0, 0, 0, 10, 30, 30]) == [
        box([0, 0, 0], 0, 10),
        box([10], 10, 20),
        box([30, 30], 20, 30),
    ]


def test_bin_10():
    h = d3.bin().set_thresholds([0, 1, 2, 3, 4])
    assert h([0, 1, 2, 3]) == [
        box([0], 0, 1),
        box([1], 1, 2),
        box([2], 2, 3),
        box([3], 3, 3),
    ]


def test_bin_11():
    actual = []
    values = [0, 0, 0, 10, 30, 30]

    def domain(values, x0, x1):
        actual[:] = [values, x0, x1]
        return [10, 20]

    h = d3.bin().set_thresholds(domain)
    assert h(values) == [
        box([0, 0, 0], 0, 10),
        box([10], 10, 20),
        box([30, 30], 20, 30),
    ]
    assert actual, [values, 0, 30]
    assert h.set_thresholds(lambda values, x0, x1: 5)(values) == [
        box([0, 0, 0], 0, 5),
        box([], 5, 10),
        box([10], 10, 15),
        box([], 15, 20),
        box([], 20, 25),
        box([], 25, 30),
        box([30, 30], 30, 35),
    ]


def test_bin_12():
    h = d3.bin().set_domain([0, 1]).set_thresholds(5)
    assert list(map(lambda b: [b.x0, b.x1], h([]))) == [
        [0.0, 0.2],
        [0.2, 0.4],
        [0.4, 0.6],
        [0.6, 0.8],
        [0.8, 1.0],
    ]


def test_bin_13():
    h = d3.bin()
    assert h([9.8, 10, 11, 12, 13, 13.2]) == [
        box([9.8], 9, 10),
        box([10], 10, 11),
        box([11], 11, 12),
        box([12], 12, 13),
        box([13, 13.2], 13, 14),
    ]


def test_bin_14():
    h = d3.bin().set_thresholds(10)
    assert h([9.8, 10, 11, 12, 13, 13.2]) == [
        box([9.8], 9.5, 10),
        box([10], 10, 10.5),
        box([], 10.5, 11),
        box([11], 11, 11.5),
        box([], 11.5, 12),
        box([12], 12, 12.5),
        box([], 12.5, 13),
        box([13, 13.2], 13, 13.5),
    ]


def test_bin_15():
    h = d3.bin().set_thresholds(10).set_domain([9.7, 13.3])
    assert h([9.8, 10, 11, 12, 13, 13.2]) == [
        box([9.8], 9.7, 10),
        box([10], 10, 10.5),
        box([], 10.5, 11),
        box([11], 11, 11.5),
        box([], 11.5, 12),
        box([12], 12, 12.5),
        box([], 12.5, 13),
        box([13, 13.2], 13, 13.3),
    ]


def test_bin_16():
    h = d3.bin().set_thresholds(10).set_domain([9.5, 13.5])
    assert h([9.8, 10, 11, 12, 13, 13.2]) == [
        box([9.8], 9.5, 10),
        box([10], 10, 10.5),
        box([], 10.5, 11),
        box([11], 11, 11.5),
        box([], 11.5, 12),
        box([12], 12, 12.5),
        box([], 12.5, 13),
        box([13, 13.2], 13, 13.5),
    ]


def test_bin_17():
    h = d3.bin().set_thresholds(10)
    assert h([1, 2, 3, 4, 5]) == [
        box([1], 1, 1.5),
        box([], 1.5, 2),
        box([2], 2, 2.5),
        box([], 2.5, 3),
        box([3], 3, 3.5),
        box([], 3.5, 4),
        box([4], 4, 4.5),
        box([], 4.5, 5),
        box([5], 5, 5.5),
    ]


# def test_bin_17():
#     height = csvParse(await readFile("./test/data/athletes.csv", "utf8")).filter(d => d.height).map(d => +d.height)
#     d3.bins = d3.bin().thresholds(57)(height)
#     assert d3.bins.map(b => b.length) == [1, 0, 0, 0, 0, 0, 2, 1, 2, 1, 1, 4, 11, 7, 13, 39, 78, 93, 119, 193, 354, 393, 573, 483, 651, 834, 808, 763, 627, 648, 833, 672, 578, 498, 395, 425, 278, 235, 182, 128, 91, 69, 43, 29, 21, 23, 3, 3, 1, 1, 1]


@pytest.mark.parametrize(
    "n", [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
)
def test_bin_18(n):
    assert all(
        map(lambda d: len(d._list) == 1, d3.bin().set_thresholds(n)(ticks(1, 2, n)))
    )


def test_bin_19():
    assert d3.bin().set_domain([4, 5])([5]) == [box([5], 4, 5)]
    eights = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    assert d3.bin().set_domain([3, 8])(eights) == [
        box([], 3, 4),
        box([], 4, 5),
        box([], 5, 6),
        box([], 6, 7),
        box(eights, 7, 8),
    ]


def test_bin_20():
    thresholds = [3, 4, 5, 6]
    b = d3.bin().set_domain([4, 5]).set_thresholds(thresholds)
    assert b([5]) == [box([], 4, 5), box([5], 5, 5)]
    assert thresholds == [3, 4, 5, 6]
    assert b.get_thresholds()() == [3, 4, 5, 6]


def test_bin_21():
    thresholds = [3, 4, 5, 6]
    b = d3.bin().set_domain([4, 5]).set_thresholds(lambda values, x0, x1: thresholds)
    assert b.get_thresholds()(None, None, None) == [3, 4, 5, 6]
    assert b([5]) == [box([], 4, 5), box([5], 5, 5)]
    assert thresholds == [3, 4, 5, 6]
