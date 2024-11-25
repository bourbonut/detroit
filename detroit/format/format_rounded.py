from .format_decimal import format_decimal_parts


def format_rounded(x, p):
    d = format_decimal_parts(x, p)
    if not d:
        return str(x)
    coefficient, exponent = d
    if exponent < 0:
        return "0." + "0" * (-1 - exponent) + coefficient
    elif len(coefficient) > exponent + 1:
        return coefficient[: exponent + 1] + "." + coefficient[exponent + 1 :]
    else:
        return coefficient + "0" * (exponent - len(coefficient) + 1)
