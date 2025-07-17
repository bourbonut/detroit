import detroit as d3

def test_catmull_rom_open_1():
  line = d3.line().curve(d3.curve_catmull_rom_open)
  assert line([]) is None
  assert line([[0, 1]]) is None
  assert line([[0, 1], [1, 3]]) is None
  assert line([[0, 1], [1, 3], [2, 1]]) == "M1,3Z"
  assert line([[0, 1], [1, 3], [2, 1], [3, 3]]) == "M1,3C1.333,3,1.667,1,2,1"

def test_catmull_rom_open_2():
  line = d3.line().curve(d3.curve_catmull_rom_open(1))
  assert line([]) is None
  assert line([[0, 1]]) is None
  assert line([[0, 1], [1, 3]]) is None
  assert line([[0, 1], [1, 3], [2, 1]]) == "M1,3Z"
  assert line([[0, 1], [1, 3], [2, 1], [3, 3]]) == "M1,3C1.333,3,1.667,1,2,1"

def test_catmull_rom_open_3():
  line = d3.line().curve(d3.curve_catmull_rom_open(0.5))
  assert d3.line().curve(d3.curve_catmull_rom_open)([[0, 1], [1, 3], [2, 1], [3, 3]]) == line([[0, 1], [1, 3], [2, 1], [3, 3]])

def test_catmull_rom_open_4():
  line = d3.line().curve(d3.curve_catmull_rom_open(0.5))
  assert d3.line().curve(d3.curve_catmull_rom_open(0.5))([[0, 1], [1, 3], [2, 1], [3, 3]]) == line([[0, 1], [1, 3], [2, 1], [3, 3]])

def test_catmull_rom_open_5():
  area = d3.area().curve(d3.curve_catmull_rom_open(0.5))
  assert area([]) is None
  assert area([[0, 1]]) is None
  assert area([[0, 1], [1, 3]]) is None
  assert area([[0, 1], [1, 3], [2, 1]]) == "M1,3L1,0Z"
  assert area([[0, 1], [1, 3], [2, 1], [3, 3]]) == "M1,3C1.333,3,1.667,1,2,1L2,0C1.667,0,1.333,0,1,0Z"

def test_catmull_rom_open_6():
  area = d3.area().curve(d3.curve_catmull_rom_open(0.5))
  assert d3.area().curve(d3.curve_catmull_rom_open)([[0, 1], [1, 3], [2, 1], [3, 3]]) == area([[0, 1], [1, 3], [2, 1], [3, 3]])

def test_catmull_rom_open_7():
  area = d3.area().curve(d3.curve_catmull_rom_open(0.5))
  assert d3.area().curve(d3.curve_catmull_rom_open(0.5))([[0, 1], [1, 3], [2, 1], [3, 3]]) == area([[0, 1], [1, 3], [2, 1], [3, 3]])
