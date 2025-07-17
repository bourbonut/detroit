from math import sqrt

TAN30 = sqrt(1 / 3)
TAN30_2 = TAN30 * 2


def symbol_diamond(context, size):
    y = sqrt(size / TAN30_2)
    x = y * TAN30
    context.move_to(0, -y)
    context.line_to(x, 0)
    context.line_to(0, y)
    context.line_to(-x, 0)
    context.close_path()
