import detroit as d3
import pytest
from math import nan

def in_delta(actual, expected, delta = 1e6):
    if isinstance(expected, list):
        n = len(expected)
        if len(actual) != n:
            return False
        for i in range(n):
            if not(actual[i] >= expected[i] - delta and actual[i] <= expected[i] + delta):
                return False
        return True
    else:
        return actual >= expected - delta and actual <= expected + delta

def test_density_1():
    assert d3.contour_density().set_size([1, 2]).get_size() == [1, 2]
    assert d3.contour_density().set_size([0, 0]).get_size() == [0, 0]
    assert d3.contour_density().set_size([1.5, 2.5]).get_size() == [1.5, 2.5]
    with pytest.raises(ValueError):
        d3.contour_density().set_size([0, -1])

def test_density_2():
    c = d3.contour_density()
    assert c([]) == []

@pytest.mark.skip
def test_density_3():
    c = d3.contour_density().set_thresholds([0.00001, 0.0001])
    for p in [[100, 100], [100.5, 102]]:
        contour = c([p])
        assert contour.length == 2
        for b in contour:
            a = d3.polygon_centroid(b["coordinates"][0][0])
            assert in_delta(a[0], p[0], 0.1)
            assert in_delta(a[1], p[1], 0.1)

def test_density_4():
    points = [[1, 0], [0, 1], [1, 1]]
    c = d3.contour_density().set_size([1, 1])
    c1 = c(points)
    values1 = list(map(lambda d: d["value"], c1))
    c2 = c.set_thresholds(values1)(points)
    values2 = list(map(lambda d: d["value"], c2))
    assert values1 == values2

def test_density_5():
    points = [[1, 0, 1], [0, 1, -2], [1, 1, nan]]
    c = d3.contour_density().set_size([1, 1]).set_weight(lambda d: d[2])(points)
    assert len(c) == 27

def test_density_6():
    points = [[1, 0], [0, 1], [1, 1]]
    c = d3.contour_density().set_cell_size(16)
    c1 = c(points)
    values1 = list(map(lambda d: d["value"], c1))
    c2 = c.set_thresholds(values1)(points)
    values2 = list(map(lambda d: d["value"], c2))
    assert values1 == values2

@pytest.mark.skip
def test_density_7():
    faithful = tsv("data/faithful.tsv")

    width = 960,
    height = 500
    margin_top = 20
    margin_right = 30
    margin_bottom = 30
    margin_left = 40

    x = (
        d3.scale_linear()
        .set_domain(d3.extent(faithful, lambda d: d["waiting"]))
        .nice()
        .set_range_round([margin_left, width - margin_right])
    )

    y = (
        d3.scale_linear()
        .set_domain(d3.extent(faithful, lambda d: d["eruptions"]))
        .nice()
        .set_range_round([height - margin_bottom, margin_top])
    )

    contour = (
        d3.contour_density()
        .x(lambda d: x(d.waiting))
        .y(lambda d: y(d.eruptions))
        .set_size([width, height])
        .set_bandwidth(30)
        (faithful)
    )

    assert list(map(lambda c: c.value, contour)) == d3.ticks(0.0002, 0.0059, 30)

@pytest.mark.skip
def test_density_8():
    faithful = tsv("data/faithful.tsv")

    width = 960
    height = 500
    margin_top = 20
    margin_right = 30
    margin_bottom = 30
    margin_left = 40

    x = (
        d3.scale_linear()
        .set_domain(d3.extent(faithful, lambda d: d.waiting))
        .nice()
        .set_range_round([margin_left, width - margin_right])
    )

    y = (
        d3.scale_linear()
        .set_domain(d3.extent(faithful, lambda d: d.eruptions))
        .nice()
        .set_range_round([height - margin_bottom, margin_top])
    )

    contour = (
        d3.contour_density()
        .x(lambda d: x(d.waiting))
        .y(lambda d: y(d.eruptions))
        .set_size([width, height])
        .set_bandwidth(30)
        .set_contours(faithful)
    )

    for value in d3.ticks(0.0002, 0.006, 30):
        assert contour(value)["value"] == value
