from math import sqrt, isnan
from .constant import constant

class ForceRadial:
    def __init__(self, radius, x, y):
        self._radius = radius
        self._x = x
        self._y = y
        self._strength = constant(0.1)
        self._strengths = None
        self._radiuses = None

    def __call__(self, alpha):
        for i, node in enumerate(self._nodes):
            dx = (node["x"] - self._x) or 1e-6
            dy = (node["y"] - self._y) or 1e-6
            r = sqrt(dx * dx + dy * dy)
            k = (self._radiuses[i] - r) * self._strengths[i] * alpha / r
            node["vx"] += dx * k
            node["vy"] += dy * k

    def _initialize(self):
        if self._nodes is None:
            return

        n = len(self._radiuses)
        self._strengths = [None] * n
        self._radiuses = [None] * n

        for i, node in enumerate(self._nodes):
            self._radiuses[i] = r = self._radius(node, i, self._nodes)
            self._strengths[i] = 0 if isnan(r) else self._strength(node, i, self._nodes)

    def initialize(self, nodes, random):
        self._nodes = nodes
        self._initialize()

    def set_strength(self, strength):
        if callable(strength):
            self._strength == strength
        else:
            self._strength = constant(strength)
        self._initialize()
        return self

    def set_radius(self, radius):
        if callable(radius):
            self._radius == radius
        else:
            self._radius = constant(radius)
        self._initialize()
        return self

    def x(self, x):
        self._x = x
        return self

    def y(self, y):
        self._y = y
        return self

    def get_strength(self):
        return self._strength

    def get_radius(self):
        return self._radius

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

def force_radial(radius, x=None, y=None):
    if not callable(radius):
        radius = constant(radius)
    if x is None:
        x = 0
    if y is None:
        y = 0

    return ForceRadial(radius, x, y)
