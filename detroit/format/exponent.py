from .format_decimal import format_decimal_parts
import math

def exponent(x):
    result = format_decimal_parts(abs(x), None)
    return math.nan if result is None else result[1]