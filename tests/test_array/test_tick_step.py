import detroit as d3
import math
import pytest

@pytest.mark.skip
def test_tick_step_none():
  assert math.isnan(d3.tick_step(math.nan, 1, 1))
  assert math.isnan(d3.tick_step(0, math.nan, 1))
  assert math.isnan(d3.tick_step(0, 1, math.nan))
  assert math.isnan(d3.tick_step(math.nan, math.nan, 1))
  assert math.isnan(d3.tick_step(0, math.nan, math.nan))
  assert math.isnan(d3.tick_step(math.nan, 1, math.nan))
  assert math.isnan(d3.tick_step(math.nan, math.nan, math.nan))
  assert math.isnan(d3.tick_step(1, 1, -1))
  assert math.isnan(d3.tick_step(1, 1, 0))
  assert math.isnan(d3.tick_step(1, 1, math.nan))

@pytest.mark.skip
def test_tick_step_infinity():
  assert d3.tick_step(1, 1, 1) ==  0
  assert d3.tick_step(1, 1, 10) ==  0
  assert d3.tick_step(0, 1, -1) ==  math.inf
  assert d3.tick_step(0, 1, 0) ==  math.inf

def test_tick_step_1():
  assert d3.tick_step(  0,  1, 10) ==  0.1
  assert d3.tick_step(  0,  1,  9) ==  0.1
  assert d3.tick_step(  0,  1,  8) ==  0.1
  assert d3.tick_step(  0,  1,  7) ==  0.2
  assert d3.tick_step(  0,  1,  6) ==  0.2
  assert d3.tick_step(  0,  1,  5) ==  0.2
  assert d3.tick_step(  0,  1,  4) ==  0.2
  assert d3.tick_step(  0,  1,  3) ==  0.5
  assert d3.tick_step(  0,  1,  2) ==  0.5
  assert d3.tick_step(  0,  1,  1) ==  1.0
  assert d3.tick_step(  0, 10, 10) ==  1
  assert d3.tick_step(  0, 10,  9) ==  1
  assert d3.tick_step(  0, 10,  8) ==  1
  assert d3.tick_step(  0, 10,  7) ==  2
  assert d3.tick_step(  0, 10,  6) ==  2
  assert d3.tick_step(  0, 10,  5) ==  2
  assert d3.tick_step(  0, 10,  4) ==  2
  assert d3.tick_step(  0, 10,  3) ==  5
  assert d3.tick_step(  0, 10,  2) ==  5
  assert d3.tick_step(  0, 10,  1) ==  10
  assert d3.tick_step(-10, 10, 10) ==   2
  assert d3.tick_step(-10, 10,  9) ==   2
  assert d3.tick_step(-10, 10,  8) ==   2
  assert d3.tick_step(-10, 10,  7) ==   2
  assert d3.tick_step(-10, 10,  6) ==   5
  assert d3.tick_step(-10, 10,  5) ==   5
  assert d3.tick_step(-10, 10,  4) ==   5
  assert d3.tick_step(-10, 10,  3) ==   5
  assert d3.tick_step(-10, 10,  2) ==  10
  assert d3.tick_step(-10, 10,  1) ==  20

def test_tick_step_2():
  assert d3.tick_step(  0,  1, 10) ==  -d3.tick_step( 1,   0, 10)
  assert d3.tick_step(  0,  1,  9) ==  -d3.tick_step( 1,   0,  9)
  assert d3.tick_step(  0,  1,  8) ==  -d3.tick_step( 1,   0,  8)
  assert d3.tick_step(  0,  1,  7) ==  -d3.tick_step( 1,   0,  7)
  assert d3.tick_step(  0,  1,  6) ==  -d3.tick_step( 1,   0,  6)
  assert d3.tick_step(  0,  1,  5) ==  -d3.tick_step( 1,   0,  5)
  assert d3.tick_step(  0,  1,  4) ==  -d3.tick_step( 1,   0,  4)
  assert d3.tick_step(  0,  1,  3) ==  -d3.tick_step( 1,   0,  3)
  assert d3.tick_step(  0,  1,  2) ==  -d3.tick_step( 1,   0,  2)
  assert d3.tick_step(  0,  1,  1) ==  -d3.tick_step( 1,   0,  1)
  assert d3.tick_step(  0, 10, 10) ==  -d3.tick_step(10,   0, 10)
  assert d3.tick_step(  0, 10,  9) ==  -d3.tick_step(10,   0,  9)
  assert d3.tick_step(  0, 10,  8) ==  -d3.tick_step(10,   0,  8)
  assert d3.tick_step(  0, 10,  7) ==  -d3.tick_step(10,   0,  7)
  assert d3.tick_step(  0, 10,  6) ==  -d3.tick_step(10,   0,  6)
  assert d3.tick_step(  0, 10,  5) ==  -d3.tick_step(10,   0,  5)
  assert d3.tick_step(  0, 10,  4) ==  -d3.tick_step(10,   0,  4)
  assert d3.tick_step(  0, 10,  3) ==  -d3.tick_step(10,   0,  3)
  assert d3.tick_step(  0, 10,  2) ==  -d3.tick_step(10,   0,  2)
  assert d3.tick_step(  0, 10,  1) ==  -d3.tick_step(10,   0,  1)
  assert d3.tick_step(-10, 10, 10) ==  -d3.tick_step(10, -10, 10)
  assert d3.tick_step(-10, 10,  9) ==  -d3.tick_step(10, -10,  9)
  assert d3.tick_step(-10, 10,  8) ==  -d3.tick_step(10, -10,  8)
  assert d3.tick_step(-10, 10,  7) ==  -d3.tick_step(10, -10,  7)
  assert d3.tick_step(-10, 10,  6) ==  -d3.tick_step(10, -10,  6)
  assert d3.tick_step(-10, 10,  5) ==  -d3.tick_step(10, -10,  5)
  assert d3.tick_step(-10, 10,  4) ==  -d3.tick_step(10, -10,  4)
  assert d3.tick_step(-10, 10,  3) ==  -d3.tick_step(10, -10,  3)
  assert d3.tick_step(-10, 10,  2) ==  -d3.tick_step(10, -10,  2)
  assert d3.tick_step(-10, 10,  1) ==  -d3.tick_step(10, -10,  1)
