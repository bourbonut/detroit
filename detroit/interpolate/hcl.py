from ..coloration import hcl as color_hcl
from .color import color, hue

class HLCInterpolator:
    def __init__(self, func):
        self.func = func

    def __call__(self, start, end):
        start = color_hcl(start)
        end = color_hcl(end)
        h = self.func(start.h, end.h)
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

interpolate_hcl = HLCInterpolator(hue)
interpolate_hcl_long = HLCInterpolator(color)
