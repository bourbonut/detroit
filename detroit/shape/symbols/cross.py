from math import sqrt


def symbol_cross(context, size):
    r = sqrt(size / 5) / 2
    context.move_to(-3 * r, -r)
    context.line_to(-r, -r)
    context.line_to(-r, -3 * r)
    context.line_to(r, -3 * r)
    context.line_to(r, -r)
    context.line_to(3 * r, -r)
    context.line_to(3 * r, r)
    context.line_to(r, r)
    context.line_to(r, 3 * r)
    context.line_to(-r, 3 * r)
    context.line_to(-r, r)
    context.line_to(-3 * r, r)
    context.close_path()
