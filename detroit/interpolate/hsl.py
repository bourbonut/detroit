from ..coloration import hsl as color_hsl
from .color import color, hue

class HSLInterpolator:
    def __init__(self, func):
        self.func = func

    def __call__(self, start, end):
        start = color_hsl(start)
        end = color_hsl(end)
        h = self.func(start.h, end.h)
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

interpolate_hsl = HSLInterpolator(hue)
interpolate_hsl_long = HSLInterpolator(color)
