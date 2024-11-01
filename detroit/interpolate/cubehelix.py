from ..coloration import cubehelix as color_cubehelix
from .color import color, hue

class CubeHelixInterpolator:

    def __init__(self, func):
        self.func = func
        self.gamma = 1

    def __call__(self, start, end):
        start = color_cubehelix(start)
        end = color_cubehelix(end)
        h = self.func(start.h, end.h)
        s = color(start.s, end.s)
        l = color(start.l, end.l)
        opacity = color(start.opacity, end.opacity)

        def interpolate(t):
            start.h = h(t)
            start.s = s(t)
            start.l = l(t ** self.gamma)
            start.opacity = opacity(t)
            return str(start)

        return interpolate

    def set_gamma(self, gamma):
        self.gamma = gamma
        return self

interpolate_cubehelix = CubeHelixInterpolator(hue)
interpolate_cubehelix_long = CubeHelixInterpolator(color)
