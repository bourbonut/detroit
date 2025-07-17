from math import sqrt


def symbol_square(context, size):
    w = sqrt(size)
    x = -w / 2
    context.rect(x, x, w, w)
