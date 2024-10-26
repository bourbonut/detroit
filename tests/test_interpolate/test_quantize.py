import detroit as d3
from detroit.interpolate.quantize import quantize

def test_quantize_1():
    assert quantize(d3.interpolate_number(0, 1), 5) == [
        0 / 4,
        1 / 4,
        2 / 4,
        3 / 4,
        4 / 4,
    ]
    # assert quantize(interpolateRgb("steelblue", "brown"), 5) == [
    #     "rgb(70, 130, 180)",
    #     "rgb(94, 108, 146)",
    #     "rgb(118, 86, 111)",
    #     "rgb(141, 64, 77)",
    #     "rgb(165, 42, 42)",
    # ]
