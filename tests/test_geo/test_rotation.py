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

def test_rotation_1():
  rotation = d3.geo_rotation([90, 0])([0, 0])
  assert in_delta(rotation[0], 90, 1e-6)
  assert in_delta(rotation[1], 0, 1e-6)

def test_rotation_2():
  rotation = d3.geo_rotation([90, 0])([150, 0])
  assert in_delta(rotation[0], -120, 1e-6)
  assert in_delta(rotation[1], 0, 1e-6)

def test_rotation_3():
  rotation = d3.geo_rotation([-45, 45])([0, 0])
  assert in_delta(rotation[0], -54.73561, 1e-6)
  assert in_delta(rotation[1], 30, 1e-6)

def test_rotation_4():
  rotation = d3.geo_rotation([-45, 45]).invert([-54.73561, 30])
  assert in_delta(rotation[0], 0, 1e-6)
  assert in_delta(rotation[1], 0, 1e-6)

def test_rotation_5():
  rotate = d3.geo_rotation([0, 0])
  assert rotate([180,0])[0] == 180
  assert rotate([-180,0])[0] == -180
  assert rotate([360,0])[0] == 0
  assert in_delta(rotate([2562,0])[0], 42, 1e-10)
  assert in_delta(rotate([-2562,0])[0], -42, 1e-10)
