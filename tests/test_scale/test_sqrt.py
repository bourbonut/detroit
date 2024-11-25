import math

import detroit as d3


def test_sqrt_1():
    s = d3.scale_sqrt()
    assert s.domain == [0, 1]
    assert s.range == [0, 1]
    assert s.clamp is False
    assert s.exponent == 0.5
    assert s.interpolate({"array": ["red"]}, {"array": ["blue"]})(0.5) == {
        "array": ["rgb(128, 0, 128)"]
    }


def test_sqrt_2():
    assert math.isclose(d3.scale_sqrt()(0.5), 1 / math.sqrt(2), rel_tol=1e-6)
