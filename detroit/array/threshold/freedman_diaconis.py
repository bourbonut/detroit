import math
from statistics import quantiles


def threshold_freedman_diaconis(values, mini, maxi):
    values = [v for v in values if v is not None]
    c = len(values)
    if len(values) <= 1:
        d = 0
    else:
        q = quantiles(values, n=4, method="inclusive")
        d = q[2] - q[0]
    return math.ceil((maxi - mini) / (2 * d * (c ** (-1 / 3)))) if c and d else 1
