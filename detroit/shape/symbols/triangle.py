from math import sqrt

SQRT_3 = sqrt(3)


def symbol_triangle(context, size):
    y = -sqrt(size / (SQRT_3 * 3))
    context.move_to(0, y * 2)
    context.line_to(-SQRT_3 * y, -y)
    context.line_to(SQRT_3 * y, -y)
    context.close_path()
