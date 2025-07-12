import detroit as d3
from detroit.shape.curves.step import curve_step

def test_step_1():
  line = d3.line().curve(curve_step)
  assert line([]) is None
  assert line([[0, 1]]) == "M0,1Z"
  assert line([[0, 1], [2, 3]]) == "M0,1L1,1L1,3L2,3"
  assert line([[0, 1], [2, 3], [4, 5]]) == "M0,1L1,1L1,3L3,3L3,5L4,5"

def test_step_2():
  area = d3.area().curve(curve_step)
  assert area([]) is None
  assert area([[0, 1]]) == "M0,1L0,0Z"
  assert area([[0, 1], [2, 3]]) == "M0,1L1,1L1,3L2,3L2,0L1,0L1,0L0,0Z"
  assert area([[0, 1], [2, 3], [4, 5]]) == "M0,1L1,1L1,3L3,3L3,5L4,5L4,0L3,0L3,0L1,0L1,0L0,0Z"
