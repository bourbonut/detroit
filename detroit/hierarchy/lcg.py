# https://en.wikipedia.org/wiki/Linear_congruential_generator#Parameters_in_common_use
A = 1664525
C = 1013904223
M = 4294967296 # 2^32

class LCG:

    def __init__(self):
        self._s = 1

    def __call__(self):
        self._s = (A * self._s + C) % M
        return self._s / M

def lcg():
    return LCG()
