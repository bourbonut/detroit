from .format_decimal import format_decimal_parts

prefix_exponent = 0

def format_prefix_auto(x, p):
    global prefix_exponent
    d = format_decimal_parts(x, p)
    if not d:
        return str(x)
    coefficient, exponent = d
    prefix_exponent = max(-8, min(8, exponent // 3)) * 3
    i = exponent - prefix_exponent + 1
    n = len(coefficient)
    if i == n:
        return coefficient
    elif i > n:
        return coefficient + "0" * (i - n)
    elif i > 0:
        return coefficient[:i] + "." + coefficient[i:]
    else:
        return "0." + "0" * (-i) + format_decimal_parts(x, max(0, p + i - 1))[0]
