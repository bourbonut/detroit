from .exponent import exponent


def precision_prefix(step, value):
    return max(0, max(-8, min(8, exponent(value) // 3)) * 3 - exponent(abs(step)))
