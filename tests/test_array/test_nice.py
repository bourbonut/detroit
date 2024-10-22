import detroit as d3
import math
import pytest

@pytest.mark.skip
def test_nice_none():
  assert d3.nice(math.nan, 1, 1) ==  [math.nan, 1]
  assert d3.nice(0, math.nan, 1) ==  [0, math.nan]
  assert d3.nice(0, 1, math.nan) ==  [0, 1]
  assert d3.nice(math.nan, math.nan, 1) ==  [math.nan, math.nan]
  assert d3.nice(0, math.nan, math.nan) ==  [0, math.nan]
  assert d3.nice(math.nan, 1, math.nan) ==  [math.nan, 1]
  assert d3.nice(math.nan, math.nan, math.nan) ==  [math.nan, math.nan]
  assert d3.nice(1, 1, -1) ==  [1, 1]
  assert d3.nice(1, 1, math.nan) ==  [1, 1]

@pytest.mark.skip
def test_nice_infinity():
  assert d3.nice(1, 1, 0) ==  [1, 1]
  assert d3.nice(1, 1, 1) ==  [1, 1]
  assert d3.nice(1, 1, 10) ==  [1, 1]
  assert d3.nice(0, 1, -1) ==  [0, 1]
  assert d3.nice(0, 1, 0) ==  [0, 1]
  assert d3.nice(0, 1, math.inf) ==  [0, 1]

def test_nice():
  assert d3.nice(0.132, 0.876, 1000) ==  [0.132, 0.876]
  assert d3.nice(0.132, 0.876, 100) ==  [0.13, 0.88]
  assert d3.nice(0.132, 0.876, 30) ==  [0.12, 0.88]
  assert d3.nice(0.132, 0.876, 10) ==  [0.1, 0.9]
  assert d3.nice(0.132, 0.876, 6) ==  [0.1, 0.9]
  assert d3.nice(0.132, 0.876, 5) ==  [0, 1]
  assert d3.nice(0.132, 0.876, 1) ==  [0, 1]
  assert d3.nice(132, 876, 1000) ==  [132, 876]
  assert d3.nice(132, 876, 100) ==  [130, 880]
  assert d3.nice(132, 876, 30) ==  [120, 880]
  assert d3.nice(132, 876, 10) ==  [100, 900]
  assert d3.nice(132, 876, 6) ==  [100, 900]
  assert d3.nice(132, 876, 5) ==  [0, 1000]
  assert d3.nice(132, 876, 1) ==  [0, 1000]

