from math import floor

from ...color import cubehelix
from ...interpolate import interpolate_cubehelix_long

interpolate_warm = interpolate_cubehelix_long(
    cubehelix(-100, 0.75, 0.35), cubehelix(80, 1.50, 0.8)
)
interpolate_cool = interpolate_cubehelix_long(
    cubehelix(260, 0.75, 0.35), cubehelix(80, 1.50, 0.8)
)


def interpolate_rainbow(t):
    if t < 0 or t > 1:
        t -= floor(t)
    ts = abs(t - 0.5)
    c = cubehelix(360 * t - 100, 1.5 - 1.5 * ts, 0.8 - 0.9 * ts)
    return str(c)
