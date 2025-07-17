from math import cos, pi, sin, sqrt

KA = 0.89081309152928522810
KR = sin(pi / 10) / sin(7 * pi / 10)
KX = sin(2 * pi / 10) * KR
KY = -cos(2 * pi / 10) * KR


def symbol_star(context, size):
    r = sqrt(size * KA)
    x = KX * r
    y = KY * r
    context.move_to(0, -r)
    context.line_to(x, y)
    for i in range(1, 5):
        a = 2 * pi * i / 5
        c = cos(a)
        s = sin(a)
        context.line_to(s * r, -c * r)
        context.line_to(c * x - s * y, s * x + c * y)
    context.close_path()
