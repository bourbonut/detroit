import detroit as d3


def test_none_1():
    assert d3.stack_order_none(list(range(4))) == [0, 1, 2, 3]
