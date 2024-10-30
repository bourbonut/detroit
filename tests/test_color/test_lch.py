import detroit as d3
from detroit.coloration.lab import HCL
import math

def approx_equal(actual, h, c, l, opacity):
    c1 = isinstance(actual, HCL)
    c2 = math.isnan(actual.h) or h - 1e-6 <= actual.h and actual.h <= h + 1e-6
    c3 = math.isnan(actual.c) or c - 1e-6 <= actual.c and actual.c <= c + 1e-6
    c4 = math.isnan(actual.l) or l - 1e-6 <= actual.l and actual.l <= l + 1e-6
    c5 = math.isnan(actual.opacity) or round(actual.opacity) == round(opacity)
    return all((c1, c2, c3, c4, c5))

def test_lch_1():
    assert approx_equal(d3.lch("#abc"), 252.37145234745182, 11.223567114593477, 74.96879980931759, 1)
    assert approx_equal(d3.lch(d3.rgb("#abc")), 252.37145234745182, 11.223567114593477, 74.96879980931759, 1)

def test_lch_2():
    assert approx_equal(d3.lch(74, 11, 252), 252, 11, 74, 1)
    assert approx_equal(d3.lch(74, 11, 252), 252, 11, 74, 1)
    assert approx_equal(d3.lch(74, 11, 252, 1), 252, 11, 74, 1)
    assert approx_equal(d3.lch(74, 11, 252, 1), 252, 11, 74, 1)
    assert approx_equal(d3.lch(74, 11, 252, 0.5), 252, 11, 74, 0.5)
