import detroit as d3


def test_threshold_sturges():
    assert d3.threshold_sturges([4, 3, 2, 1, None], 1, 4) == 3
    assert d3.threshold_sturges([1], 1, 4) == 1
    assert d3.threshold_sturges([], 1, 4) == 1
