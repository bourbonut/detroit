import detroit as d3
from detroit.color.color import Color
from detroit.color.cubehelix import Cubehelix


def test_cubehelix_1():
    c = d3.cubehelix("steelblue")
    assert isinstance(c, Cubehelix)
    assert isinstance(c, Color)
