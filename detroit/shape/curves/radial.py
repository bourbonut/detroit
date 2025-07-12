from .linear import curve_linear
from math import cos, sin

class RadialCurve:

    def __init__(self, curve):
        self._curve = curve

    def area_start(self):
        self._curve.area_start()

    def area_end(self):
        self._curve.area_end()

    def line_start(self):
        self._curve.line_start()

    def line_end(self):
        self._curve.line_end()
    
    def point(self, a, r):
        self._curve.point(r * sin(a), -r * cos(a))


def curve_radial(curve):
    def radial(context):
        return RadialCurve(curve(context))

    return radial

def curve_radial_linear(context):
    return curve_radial(curve_linear)
