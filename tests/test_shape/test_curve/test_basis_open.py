import detroit as d3

def test_basis_open_1():
  line = d3.line().curve(d3.curve_basis_open)
  assert line([]) is None
  assert line([[0, 0]]) is None
  assert line([[0, 0], [0, 10]]) is None
  assert line([[0, 0], [0, 10], [10, 10]]) == "M1.667,8.333Z"
  assert line([[0, 0], [0, 10], [10, 10], [10, 0]]) == "M1.667,8.333C3.333,10,6.667,10,8.333,8.333"
  assert line([[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]) == "M1.667,8.333C3.333,10,6.667,10,8.333,8.333C10,6.667,10,3.333,8.333,1.667"

def test_basis_open_2():
  area = d3.area().curve(d3.curve_basis_open)
  assert area([]) is None
  assert area([[0, 1]]) is None
  assert area([[0, 1], [1, 3]]) is None
  assert area([[0, 0], [0, 10], [10, 10]]) == "M1.667,8.333L1.667,0Z"
  assert area([[0, 0], [0, 10], [10, 10], [10, 0]]) == "M1.667,8.333C3.333,10,6.667,10,8.333,8.333L8.333,0C6.667,0,3.333,0,1.667,0Z"
  assert area([[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]) == "M1.667,8.333C3.333,10,6.667,10,8.333,8.333C10,6.667,10,3.333,8.333,1.667L8.333,0C10,0,10,0,8.333,0C6.667,0,3.333,0,1.667,0Z"
