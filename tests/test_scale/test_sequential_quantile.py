import detroit as d3


def test_sequentialQuantile_1():
    s = d3.scale_sequential_quantile().set_domain([0, 1, 2, 3, 10])
    assert s(-1) == 0
    assert s(0) == 0
    assert s(1) == 0.25
    assert s(10) == 1
    assert s(20) == 1


def test_sequentialQuantile_2():
    s = d3.scale_sequential_quantile().set_domain([0, 2, 9, 0.1, 10])
    assert s.domain == [0, 0.1, 2, 9, 10]


def test_sequentialQuantile_3():
    s = d3.scale_sequential_quantile().set_domain([0, 2, 9, 0.1, 10])
    assert s.range == [0 / 4, 1 / 4, 2 / 4, 3 / 4, 4 / 4]


def test_sequentialQuantile_4():
    s = d3.scale_sequential_quantile().set_domain([2 * i / 1999 for i in range(2000)])
    assert s.quantiles(4) == [0, 0.5, 1, 1.5, 2]
