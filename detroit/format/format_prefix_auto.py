from .format_decimal import format_decimal_parts


class FormatPrefixAuto:
    def __init__(self):
        self.prefix_exponent = 0

    def __call__(self, x, p):
        d = format_decimal_parts(x, p)
        if not d:
            return str(x)
        coefficient, exponent = d
        self.prefix_exponent = max(-8, min(8, exponent // 3)) * 3
        i = exponent - self.prefix_exponent + 1
        n = len(coefficient)
        if i == n:
            return coefficient
        elif i > n:
            return coefficient + "0" * (i - n)
        elif i > 0:
            return coefficient[:i] + "." + coefficient[i:]
        else:
            return "0." + "0" * (-i) + format_decimal_parts(x, max(0, p + i - 1))[0]


prefix_auto = FormatPrefixAuto()


def format_prefix_auto(x, p):
    return prefix_auto(x, p)
