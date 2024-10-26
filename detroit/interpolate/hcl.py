from d3_color import hcl as colorHcl
from .color import color, hue

def hcl(hue_func):
    def interpolator(start, end):
        start = colorHcl(start)
        end = colorHcl(end)
        h = hue_func(start.h, end.h)
        c = color(start.c, end.c)
        l = color(start.l, end.l)
        opacity = color(start.opacity, end.opacity)

        def interpolate(t):
            start.h = h(t)
            start.c = c(t)
            start.l = l(t)
            start.opacity = opacity(t)
            return str(start)

        return interpolate

    return interpolator

hcl_default = hcl(hue)
hclLong = hcl(color)
