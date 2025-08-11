import detroit as d3

def test_reverse_1():
  assert d3.stack_order_reverse(list(range(4))) == [3, 2, 1, 0]
