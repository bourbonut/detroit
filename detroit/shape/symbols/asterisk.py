from math import sqrt

SQRT_3 = sqrt(3)


def symbol_asterisk(context, size):
    r = sqrt(size + min(size / 28, 0.75)) * 0.59436
    t = r / 2
    u = t * SQRT_3
    context.move_to(0, r)
    context.line_to(0, -r)
    context.move_to(-u, -t)
    context.line_to(u, t)
    context.move_to(-u, t)
    context.line_to(u, -t)
