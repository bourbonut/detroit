from d3_color import rgb as colorRgb
from .basis import basis
from .basisClosed import basisClosed
from .color import nogamma, gamma

def rgbGamma(y):
    color = gamma(y)

    def rgb(start, end):
        start = colorRgb(start)
        end = colorRgb(end)
        r = color(start.r, end.r)
        g = color(start.g, end.g)
        b = color(start.b, end.b)
        opacity = nogamma(start.opacity, end.opacity)
        
        def interpolate(t):
            start.r = r(t)
            start.g = g(t)
            start.b = b(t)
            start.opacity = opacity(t)
            return str(start)
        
        return interpolate

    rgb.gamma = rgbGamma
    return rgb

rgb = rgbGamma(1)

def rgbSpline(spline):
    def interpolate(colors):
        n = len(colors)
        r = [0] * n
        g = [0] * n
        b = [0] * n
        
        for i, color in enumerate(colors):
            color = colorRgb(color)
            r[i] = color.r or 0
            g[i] = color.g or 0
            b[i] = color.b or 0
        
        r_spline = spline(r)
        g_spline = spline(g)
        b_spline = spline(b)
        
        color = colorRgb()
        color.opacity = 1
        
        def interpolate(t):
            color.r = r_spline(t)
            color.g = g_spline(t)
            color.b = b_spline(t)
            return str(color)
        
        return interpolate
    
    return interpolate

rgbBasis = rgbSpline(basis)
rgbBasisClosed = rgbSpline(basisClosed)
