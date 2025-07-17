from math import sqrt


def symbol_diamond2(context, size):
    r = sqrt(size) * 0.62625
    context.move_to(0, -r)
    context.line_to(r, 0)
    context.line_to(0, r)
    context.line_to(-r, 0)
    context.close_path()
