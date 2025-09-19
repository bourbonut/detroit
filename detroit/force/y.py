from math import isnan
from .constant import constant
from ..array import argpass

class ForceY:

    def __init__(self, y):
        self._y = y
        self._strength = constant(0.1)
        self._nodes = None
        self._strengths = None
        self._yz = None

    def __call__(self, alpha):
        for i, node in enumerate(self._nodes):
            node["vy"] += (self._yz[i] - node["y"]) * self._strengths[i] * alpha

    def _initialize(self):
        if self._nodes is None:
            return

        self._strengths = [None] * len(self._nodes)
        self._yz = [None] * len(self._nodes)
        for i, node in enumerate(self._nodes):
            self._yz[i] = y = self._y(node, i, self._nodes)
            self._strengths[i] = 0 if isnan(y) else self._strength(node, i, self._nodes)

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

    def y(self, y):
        if callable(y):
            self._y = y
        else:
            self._y = constant(y)
        self._y = argpass(self._y)
        self._initialize()
        return self

    def get_strength(self):
        return self._strength

    def get_y(self):
        return self._y

def force_y(y = None):
    if not callable(y):
        y = constant(0 if y is None else y)

    return ForceY(argpass(y))
