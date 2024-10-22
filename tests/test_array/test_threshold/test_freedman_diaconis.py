from detroit.array.threshold import threshold_freedman_diaconis

def test_threshold_freedman_diaconis():
  assert threshold_freedman_diaconis([4, 3, 2, 1, None], 1, 4) == 2
  assert threshold_freedman_diaconis([1, 1, 1, 1], 1, 4) == 1
  assert threshold_freedman_diaconis([1], 1, 4) == 1
  assert threshold_freedman_diaconis([], 1, 4) == 1
