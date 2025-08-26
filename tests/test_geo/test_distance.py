import detroit as d3

def in_delta(actual, expected, delta=1e6):
    if isinstance(expected, list):
        n = len(expected)
        if len(actual) != n:
            return False
        for i in range(n):
            if not in_delta(actual[i], expected[i], delta):
                return False
        return True
    else:
        return actual >= expected - delta and actual <= expected + delta

def test_distance_1():
  assert d3.geo_distance([0, 0], [0, 0]) == 0
  assert in_delta(d3.geo_distance([118 + 24 / 60, 33 + 57 / 60], [73 + 47 / 60, 40 + 38 / 60]), 3973 / 6371, 0.5)

def test_distance_2():
  assert d3.geo_distance([0, 0], [0, 1e-12]) > 0
