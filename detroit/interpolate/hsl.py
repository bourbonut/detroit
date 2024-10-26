from d3_color import hsl as colorHsl
from .color import color, hue

def hsl(hue_func):
    def interpolator(start, end):
        start = colorHsl(start)
        end = colorHsl(end)
        h = hue_func(start.h, end.h)
        s = color(start.s, end.s)
        l = color(start.l, end.l)
        opacity = color(start.opacity, end.opacity)

        def interpolate(t):
            start.h = h(t)
            start.s = s(t)
            start.l = l(t)
            start.opacity = opacity(t)
            return str(start)

        return interpolate

    return interpolator

hsl_default = hsl(hue)
hslLong = hsl(color)
