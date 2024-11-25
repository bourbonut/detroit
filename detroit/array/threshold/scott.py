import math
from statistics import stdev


def threshold_scott(values, mini, maxi):
    values = [v for v in values if v is not None]
    c = len(values)
    if len(values) <= 1:
        d = 0
    else:
        d = stdev(values)
    return math.ceil((maxi - mini) * (c ** (1 / 3)) / (3.49 * d)) if c and d else 1
