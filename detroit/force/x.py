from math import isnan
from .constant import constant
from ..array import argpass

class ForceX:

    def __init__(self, x):
        self._x = x
        self._strength = constant(0.1)
        self._nodes = None
        self._strengths = None
        self._xz = None

    def __call__(self, alpha):
        for i, node in enumerate(self._nodes):
            node["vx"] += (self._xz[i] - node["x"]) * self._strengths[i] * alpha

    def _initialize(self):
        if self._nodes is None:
            return

        self._strengths = [None] * len(self._nodes)
        self._xz = [None] * len(self._nodes)
        for i, node in enumerate(self._nodes):
            self._xz[i] = x = self._x(node, i, self._nodes)
            self._strengths[i] = 0 if isnan(x) else self._strength(node, i, self._nodes)

    def initialize(self, nodes, random):
        self._nodes = nodes
        self._initialize()

    def set_strength(self, strength):
        if callable(strength):
            self._strength = strength
        else:
            self._strength = constant(strength)
        self._initialize()
        return self

    def x(self, x):
        if callable(x):
            self._x = x
        else:
            self._x = constant(x)
        self._x = argpass(self._x)
        self._initialize()
        return self

    def get_strength(self):
        return self._strength

    def get_x(self):
        return self._x

def force_x(x = None):
    if not callable(x):
        x = constant(0 if x is None else x)

    return ForceX(argpass(x))
