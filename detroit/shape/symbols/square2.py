from math import sqrt


def symbol_square2(context, size):
    r = sqrt(size) * 0.4431
    context.move_to(r, r)
    context.line_to(r, -r)
    context.line_to(-r, -r)
    context.line_to(-r, r)
    context.close_path()
