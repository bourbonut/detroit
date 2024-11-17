from .linear import LinearBase
from .number import number
import math

class Identity(LinearBase):
    """
    Build a new identity scale with the specified range (and by extension, domain).
    """

    def __init__(self, domain=None):
        self._domain = list(map(float, domain)) if domain is not None else [0, 1]
        self._unknown = None

    def __call__(self, x):
        unvalid_type = x is None or (isinstance(x, float) and math.isnan(x))
        return self._unknown if unvalid_type else x

    def invert(self, x):
        return self(x)

    def domain(self, *args):
        if args:
            self._domain = list(map(number, args[0]))
            return self
        else:
            return self._domain 

    def range(self, *args):
        return self.domain(*args)

    def unknown(self, *args):
        if args:
            self._unknown = args[0]
            return self
        else:
            return self._unknown

    def copy(self):
        return Identity(self._domain).unknown(self._unknown)

scale_identity = Identity
