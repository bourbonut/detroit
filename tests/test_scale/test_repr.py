import detroit as d3
import pytest


functions = [
    d3.scale_band,
    d3.scale_diverging,
    d3.scale_diverging,
    d3.scale_diverging_log,
    d3.scale_diverging_log,
    d3.scale_diverging_pow,
    d3.scale_diverging_pow,
    d3.scale_diverging_sqrt,
    d3.scale_diverging_sqrt,
    d3.scale_diverging_symlog,
    d3.scale_diverging_symlog,
    d3.scale_identity,
    d3.scale_linear,
    d3.scale_log,
    d3.scale_ordinal,
    d3.scale_point,
    d3.scale_pow,
    d3.scale_quantile,
    d3.scale_quantize,
    d3.scale_radial,
    d3.scale_sequential,
    d3.scale_sequential_log,
    d3.scale_sequential_pow,
    d3.scale_sequential_quantile,
    d3.scale_sequential_sqrt,
    d3.scale_sequential_symlog,
    d3.scale_sqrt,
    d3.scale_symlog,
    d3.scale_threshold,
    d3.scale_time,
]

@pytest.mark.parametrize("function", functions)
def test_str(function):
    assert "<detroit.scale" not in str(function())

@pytest.mark.parametrize("function", functions)
def test_repr(function):
    assert "<detroit.scale" not in repr(function())
