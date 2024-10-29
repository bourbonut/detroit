import detroit as d3
from detroit.coloration.lab import LAB
import math

def approx_equal(actual, l, a, b, opacity):
    c1 = isinstance(actual, LAB)
    c2 = math.isnan(actual.l) or l - 1e-6 <= actual.l and actual.l <= l + 1e-6
    c3 = math.isnan(actual.a) or a - 1e-6 <= actual.a and actual.a <= a + 1e-6
    c4 = math.isnan(actual.b) or b - 1e-6 <= actual.b and actual.b <= b + 1e-6
    c5 = math.isnan(actual.opacity) or round(actual.opacity) == round(opacity)
    return all((c1, c2, c3, c4, c5))

def test_gray_1():
    assert approx_equal(d3.gray(120), 120, 0, 0, 1)
    assert approx_equal(d3.gray(120, 0.5), 120, 0, 0, 0.5)
    assert approx_equal(d3.gray(120), 120, 0, 0, 1)
    assert approx_equal(d3.gray(120), 120, 0, 0, 1)
