from detroit.array.threshold import threshold_scott


def test_threshold_scott():
    assert threshold_scott([4, 3, 2, 1, None], 1, 4) == 2
    assert threshold_scott([1, 1, 1, 1], 1, 4) == 1
    assert threshold_scott([1], 1, 4) == 1
    assert threshold_scott([], 1, 4) == 1
