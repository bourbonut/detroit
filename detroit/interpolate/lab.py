from ..coloration import lab as color_lab
from .color import color

def interpolate_lab(start, end):
    start = color_lab(start)
    end = color_lab(end)
    l = color(start.l, end.l)
    a = color(start.a, end.a)
    b = color(start.b, end.b)
    opacity = color(start.opacity, end.opacity)

    def interpolate(t):
        start.l = l(t)
        start.a = a(t)
        start.b = b(t)
        start.opacity = opacity(t)
        return str(start)

    return interpolate
