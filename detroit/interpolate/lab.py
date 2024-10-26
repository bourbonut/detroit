from d3_color import lab as colorLab
from .color import color

def lab(start, end):
    start = colorLab(start)
    end = colorLab(end)
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
