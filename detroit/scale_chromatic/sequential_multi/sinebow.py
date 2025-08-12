from math import pi, sin

from ...color import rgb


def interpolate_sinebow(t):
    t = (0.5 - t) * pi

    x = sin(t)
    r = 255 * x * x

    x = sin(t + pi / 3)
    g = 255 * x * x

    x = sin(t + pi * 2 / 3)
    b = 255 * x * x
    return str(rgb(int(r), int(g), int(b)))
