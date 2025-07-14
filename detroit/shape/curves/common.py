from math import isnan
from ...types import Number

def isvaluable(x: Number | None) -> bool:
    return x is not None and not isnan(x) and x
