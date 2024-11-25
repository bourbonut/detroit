from .linear import LinearBase
import math


class Identity(LinearBase):
    """
    Build a new identity scale with the specified range (and by extension, domain).
    """

    def __init__(self, domain=None):
        self._domain = list(domain) if domain is not None else [0, 1]
        self._unknown = None

    def __call__(self, x):
        unvalid_type = x is None or (isinstance(x, float) and math.isnan(x))
        return self._unknown if unvalid_type else x

    def invert(self, x):
        return self(x)

    def set_domain(self, domain):
        self._domain = list(domain)
        return self

    @property
    def domain(self):
        return self._domain

    def set_range(self, range_vals):
        return self.set_domain(range_vals)

    @property
    def range(self):
        return self._domain

    def set_unknown(self, unknown):
        self._unknown = unknown
        return self

    @property
    def unknown(self):
        return self._unknown

    def copy(self):
        return Identity(self._domain).set_unknown(self._unknown)


def scale_identity(domain=None):
    return Identity(domain=domain)
