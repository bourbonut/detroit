from .exponent import exponent

def precision_round(step, max_val):
    step = abs(step)
    max_val = abs(max_val) - step
    return max(0, exponent(max_val) - exponent(step)) + 1
