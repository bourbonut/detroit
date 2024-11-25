import detroit as d3


# A generalization from µ to all prefixes:
# assert d3.precision_prefix(1e-6, 1e-6), 0 // 1µ
# assert d3.precision_prefix(1e-6, 1e-7), 0 // 10µ
# assert d3.precision_prefix(1e-6, 1e-8), 0 // 100µ
def test_precision_prefix_1():
    for i in range(-24, 24 + 1, 3):
        for j in range(i, i + 3):
            assert d3.precision_prefix(10**i, 10**j) == 0


# A generalization from µ to all prefixes:
# assert d3.precision_prefix(1e-9, 1e-6), 3 // 0.001µ
# assert d3.precision_prefix(1e-8, 1e-6), 2 // 0.01µ
# assert d3.precision_prefix(1e-7, 1e-6), 1 // 0.1µ
def test_precision_prefix_2():
    for i in range(-24, 24 + 1, 3):
        for j in range(i - 4, i):
            assert d3.precision_prefix(10**j, 10**i) == i - j


def test_precision_prefix_3():
    assert d3.precision_prefix(1e-24, 1e-24) == 0  # 1y
    assert d3.precision_prefix(1e-25, 1e-25) == 1  # 0.1y
    assert d3.precision_prefix(1e-26, 1e-26) == 2  # 0.01y
    assert d3.precision_prefix(1e-27, 1e-27) == 3  # 0.001y
    assert d3.precision_prefix(1e-28, 1e-28) == 4  # 0.0001y


def test_precision_prefix_4():
    assert d3.precision_prefix(1e24, 1e24) == 0  # 1Y
    assert d3.precision_prefix(1e24, 1e25) == 0  # 10Y
    assert d3.precision_prefix(1e24, 1e26) == 0  # 100Y
    assert d3.precision_prefix(1e24, 1e27) == 0  # 1000Y
    assert d3.precision_prefix(1e23, 1e27) == 1  # 1000.0Y
