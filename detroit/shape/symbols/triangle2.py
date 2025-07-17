from math import sqrt

SQRT_3 = sqrt(3)


def symbol_triangle2(context, size):
    s = sqrt(size) * 0.6824
    t = s / 2
    u = (s * SQRT_3) / 2
    context.move_to(0, -s)
    context.line_to(u, t)
    context.line_to(-u, t)
    context.close_path()
