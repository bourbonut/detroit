from math import sqrt


def symbol_plus(context, size):
    r = sqrt(size - min(size / 7, 2)) * 0.87559
    context.move_to(-r, 0)
    context.line_to(r, 0)
    context.move_to(0, r)
    context.line_to(0, -r)
