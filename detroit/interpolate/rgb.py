from ..coloration import rgb as color_rgb
from .basis import basis
from .basis_closed import basis_closed
from .color import gamma, color as nogamma

class RGBGammaInterpolator:
    def __init__(self, y):
        self.color = gamma(y)

    def __call__(self, start, end):
        start = color_rgb(start)
        end = color_rgb(end)
        r = self.color(start.r, end.r)
        g = self.color(start.g, end.g)
        b = self.color(start.b, end.b)
        opacity = nogamma(start.opacity, end.opacity)
        
        def interpolate(t):
            start.r = r(t)
            start.g = g(t)
            start.b = b(t)
            start.opacity = opacity(t)
            return str(start)
        
        return interpolate

    def set_gamma(self, y):
        self.color = gamma(y)
        return self

interpolate_rgb = RGBGammaInterpolator(1)

class RGBSplineInterpolator:
    def __init__(self, spline):
        self.spline = spline

    def __call__(self, colors):
        n = len(colors)
        r = [0] * n
        g = [0] * n
        b = [0] * n
        
        for i, color in enumerate(colors):
            color = color_rgb(color)
            r[i] = color.r or 0
            g[i] = color.g or 0
            b[i] = color.b or 0
        
        r_spline = self.spline(r)
        g_spline = self.spline(g)
        b_spline = self.spline(b)
        
        color = color_rgb()
        color.opacity = 1
        
        def interpolate(t):
            color.r = r_spline(t)
            color.g = g_spline(t)
            color.b = b_spline(t)
            return str(color)
        
        return interpolate
    
interpolate_rgb_basis = RGBSplineInterpolator(basis)
interpolate_rgb_basis_closed = RGBSplineInterpolator(basis_closed)
