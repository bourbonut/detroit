import detroit as d3

def test_bump_y_1():
  line = d3.line().curve(d3.curve_bump_y)
  assert line([]) is None
  assert line([[0, 1]]) == "M0,1Z"
  assert line([[0, 1], [1, 3]]) == "M0,1C0,2,1,2,1,3"
  assert line([[0, 1], [1, 3], [2, 1]]) == "M0,1C0,2,1,2,1,3C1,2,2,2,2,1"

def test_bump_y_2():
  area = d3.area().curve(d3.curve_bump_y)
  assert area([]) is None
  assert area([[0, 1]]) == "M0,1L0,0Z"
  assert area([[0, 1], [1, 3]]) == "M0,1C0,2,1,2,1,3L1,0C1,0,0,0,0,0Z"
  assert area([[0, 1], [1, 3], [2, 1]]) == "M0,1C0,2,1,2,1,3C1,2,2,2,2,1L2,0C2,0,1,0,1,0C1,0,0,0,0,0Z"
