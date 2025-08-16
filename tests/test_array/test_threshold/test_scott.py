import detroit as d3


def test_threshold_scott():
    assert d3.threshold_scott([4, 3, 2, 1, None], 1, 4) == 2
    assert d3.threshold_scott([1, 1, 1, 1], 1, 4) == 1
    assert d3.threshold_scott([1], 1, 4) == 1
    assert d3.threshold_scott([], 1, 4) == 1
