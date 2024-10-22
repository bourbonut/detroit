from detroit.array.threshold import threshold_sturges

def test_threshold_sturges():
  assert threshold_sturges([4, 3, 2, 1, None], 1, 4) == 3
  assert threshold_sturges([1], 1, 4) == 1
  assert threshold_sturges([], 1, 4) == 1
