import detroit as d3

def test_catmull_rom_closed_1():
  line = d3.line().curve(d3.curve_catmull_rom_closed)
  assert line([]) is None
  assert line([[0, 1]]) == "M0,1Z"
  assert line([[0, 1], [1, 3]]) == "M1,3L0,1Z"
  assert line([[0, 1], [1, 3], [2, 1]]) == "M1,3C1.333,3,2.200,1.324,2,1C1.811,0.694,0.189,0.694,0,1C-0.200,1.324,0.667,3,1,3"
  assert line([[0, 1], [1, 3], [2, 1], [3, 3]]) == "M1,3C1.333,3,1.667,1,2,1C2.333,1,3.160,2.858,3,3C2.796,3.180,0.204,0.820,0,1C-0.160,1.142,0.667,3,1,3"

def test_catmull_rom_closed_2():
  line = d3.line().curve(d3.curve_catmull_rom_closed(0))
  assert line([]) is None
  assert line([[0, 1]]) == "M0,1Z"
  assert line([[0, 1], [1, 3]]) == "M1,3L0,1Z"
  assert line([[0, 1], [1, 3], [2, 1]]) == "M1,3C1.333,3,2.167,1.333,2,1C1.833,0.667,0.167,0.667,0,1C-0.167,1.333,0.667,3,1,3"
  assert line([[0, 1], [1, 3], [2, 1], [3, 3]]) == "M1,3C1.333,3,1.667,1,2,1C2.333,1,3.333,3,3,3C2.667,3,0.333,1,0,1C-0.333,1,0.667,3,1,3"

def test_catmull_rom_closed_3():
  line = d3.line().curve(d3.curve_catmull_rom_closed(1))
  assert line([]) is None
  assert line([[0, 1]]) == "M0,1Z"
  assert line([[0, 1], [1, 3]]) == "M1,3L0,1Z"
  assert line([[0, 1], [1, 3], [2, 1]]) == "M1,3C1.333,3,2.236,1.315,2,1C1.789,0.718,0.211,0.718,0,1C-0.236,1.315,0.667,3,1,3"
  assert line([[0, 1], [1, 3], [2, 1], [3, 3]]) == "M1,3C1.333,3,1.667,1,2,1C2.333,1,3.032,2.747,3,3C2.949,3.408,0.051,0.592,0,1C-0.032,1.253,0.667,3,1,3"

def test_catmull_rom_closed_4():
  line = d3.line().curve(d3.curve_catmull_rom_closed(0.5))
  assert d3.line().curve(d3.curve_catmull_rom_closed)([[0, 1], [1, 3], [2, 1], [3, 3]]) == line([[0, 1], [1, 3], [2, 1], [3, 3]])

def test_catmull_rom_closed_5():
  line = d3.line().curve(d3.curve_catmull_rom_closed(0.5))
  assert d3.line().curve(d3.curve_catmull_rom_closed(0.5))([[0, 1], [1, 3], [2, 1], [3, 3]]) == line([[0, 1], [1, 3], [2, 1], [3, 3]])

def test_catmull_rom_closed_6():
  area = d3.area().curve(d3.curve_catmull_rom_closed(0.5))
  assert d3.area().curve(d3.curve_catmull_rom_closed(0.5))([[0, 1], [1, 3], [2, 1], [3, 3]]) == area([[0, 1], [1, 3], [2, 1], [3, 3]])
