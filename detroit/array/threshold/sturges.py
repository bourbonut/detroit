import math


def threshold_sturges(values, *args):
    values = [v for v in values if v is not None]
    if len(values) == 0:
        return 1
    return max(1, math.ceil(math.log(len(values)) / math.log(2)) + 1)
