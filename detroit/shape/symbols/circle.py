from math import pi, sqrt


def symbol_circle(context, size):
    r = sqrt(size / pi)
    context.move_to(r, 0)
    context.arc(0, 0, r, 0, 2 * pi)
