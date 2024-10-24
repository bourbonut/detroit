import numpy as np

def interpolate_cubehelix_long(c1, c2):
    def interpolate(t):
        return c1 * (1 - t) + c2 * t
    return interpolate

def cubehelix(h, s, l):
    return np.array([h, s, l])

warm = interpolate_cubehelix_long(cubehelix(-100, 0.75, 0.35), cubehelix(80, 1.50, 0.8))
cool = interpolate_cubehelix_long(cubehelix(260, 0.75, 0.35), cubehelix(80, 1.50, 0.8))

def rainbow(t):
    if t < 0 or t > 1:
        t -= np.floor(t)
    ts = np.abs(t - 0.5)
    c = cubehelix(360 * t - 100, 1.5 - 1.5 * ts, 0.8 - 0.9 * ts)
    return c
