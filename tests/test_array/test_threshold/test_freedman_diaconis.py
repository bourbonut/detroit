import detroit as d3


def test_threshold_freedman_diaconis():
    assert d3.threshold_freedman_diaconis([4, 3, 2, 1, None], 1, 4) == 2
    assert d3.threshold_freedman_diaconis([1, 1, 1, 1], 1, 4) == 1
    assert d3.threshold_freedman_diaconis([1], 1, 4) == 1
    assert d3.threshold_freedman_diaconis([], 1, 4) == 1
