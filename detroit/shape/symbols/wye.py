from math import sqrt

C = -0.5
S = sqrt(3) / 2
K = 1 / sqrt(12)
A = (K / 2 + 1) * 3


def symbol_wye(context, size):
    r = sqrt(size / A)
    x0 = r / 2
    y0 = r * K
    x1 = x0
    y1 = r * K + r
    x2 = -x1
    y2 = y1
    context.move_to(x0, y0)
    context.line_to(x1, y1)
    context.line_to(x2, y2)
    context.line_to(C * x0 - S * y0, S * x0 + C * y0)
    context.line_to(C * x1 - S * y1, S * x1 + C * y1)
    context.line_to(C * x2 - S * y2, S * x2 + C * y2)
    context.line_to(C * x0 + S * y0, C * y0 - S * x0)
    context.line_to(C * x1 + S * y1, C * y1 - S * x1)
    context.line_to(C * x2 + S * y2, C * y2 - S * x2)
    context.close_path()
