from math import sqrt


def symbol_times(context, size):
    r = sqrt(size - min(size / 6, 1.7)) * 0.6189
    context.move_to(-r, -r)
    context.line_to(r, r)
    context.move_to(-r, r)
    context.line_to(r, -r)
