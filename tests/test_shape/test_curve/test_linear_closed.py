import detroit as d3

def test_linear_closed_1():
  line = d3.line().curve(d3.curve_linear_closed)
  assert line([]) is None
  assert line([[0, 1]]) == "M0,1Z"
  assert line([[0, 1], [2, 3]]) == "M0,1L2,3Z"
  assert line([[0, 1], [2, 3], [4, 5]]) == "M0,1L2,3L4,5Z"
