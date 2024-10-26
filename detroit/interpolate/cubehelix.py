from d3_color import cubehelix as colorCubehelix
from .color import color, hue

def cubehelix(hue_func):
    def cubehelixGamma(y):
        y = float(y)

        def interpolator(start, end):
            start = colorCubehelix(start)
            end = colorCubehelix(end)
            h = hue_func(start.h, end.h)
            s = color(start.s, end.s)
            l = color(start.l, end.l)
            opacity = color(start.opacity, end.opacity)

            def interpolate(t):
                start.h = h(t)
                start.s = s(t)
                start.l = l(t ** y)
                start.opacity = opacity(t)
                return str(start)

            return interpolate

        interpolator.gamma = cubehelixGamma
        return interpolator

    return cubehelixGamma(1)

cubehelix_default = cubehelix(hue)
cubehelixLong = cubehelix(color)
