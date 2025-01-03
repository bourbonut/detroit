import detroit as d3


def test_precisionRound_1():
    assert d3.precision_round(0.1, 1.1) == 2  # "1.0", "1.1"
    assert d3.precision_round(0.01, 0.99) == 2  # "0.98", "0.99"
    assert d3.precision_round(0.01, 1.00) == 2  # "0.99", "1.0"
    assert d3.precision_round(0.01, 1.01) == 3  # "1.00", "1.01"
