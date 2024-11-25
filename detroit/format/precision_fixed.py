from .exponent import exponent


def precision_fixed(step):
    return max(0, -exponent(abs(step)))
