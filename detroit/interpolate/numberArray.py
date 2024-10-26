import numpy as np

def numberArray(a, b):
    if b is None:
        b = []
    n = min(len(b), len(a)) if a else 0
    c = b.copy()

    def interpolate(t):
        for i in range(n):
            c[i] = a[i] * (1 - t) + b[i] * t
        return c

    return interpolate

def isNumberArray(x):
    return isinstance(x, (np.ndarray, list)) and all(isinstance(i, (int, float)) for i in x)
