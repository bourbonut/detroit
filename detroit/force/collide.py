from math import sqrt, nan
from ..quadtree import quadtree
from .jiggle import jiggle
from .constant import constant

def x(d):
    return d["x"] + d["vx"]

def y(d):
    return d["y"] + d["vy"]

def quadr(quad):
    return quad["r"] if isinstance(quad, dict) else quad[4]

class Apply:
    def __init__(self, strength, random):
        self._random = random
        self._strength = strength
        self._node = None
        self._xi = nan
        self._yi = nan
        self._ri = nan
        self._ri2 = nan

    def __call__(self, quad, x0, y0, x1, y1):
        rj = quadr(quad)
        r = self._ri + rj
        if isinstance(quad, dict) and quad["data"]:
            data = quad["data"]
            if data["index"] > self._node["index"]:
                x = self._xi - data["x"] - data["vx"]
                y = self._yi - data["y"] - data["vy"]
                length = x * x + y * y
                if length < r * r:
                    if x == 0:
                        x = jiggle(self._random)
                        length += x * x
                    if y == 0:
                        y = jiggle(self._random)
                        length += y * y

                    length = sqrt(length)
                    length = (r - length) / length * self._strength
                    x *= length
                    y *= length
                    rj *= rj
                    r = rj / (self._ri2  + rj)
                    self._node["vx"] += x * r
                    self._node["vy"] += y * r

                    r = 1 - r
                    data["vx"] -= x * r
                    data["vy"] -= y * r
            return
        return x0 > self._xi + r or x1 < self._xi - r or y0 > self._yi + r or y1 < self._yi - r

    def update(self, node, xi, yi, ri, ri2):
        self._node = node
        self._xi = xi
        self._yi = yi
        self._ri = ri
        self._ri2 = ri2

class ForceCollide:

    def __init__(self, radius):
        self._radius = radius
        self._nodes = None
        self._radii = None
        self._random = None
        self._strength = 1
        self._iterations = 1

    def __call__(self, alpha):
        apply = Apply(self._strength, self._random)
        for k in range(self._iterations):
            tree = quadtree(self._nodes, x, y).visit_after(self._prepare)
            for node in self._nodes:
                ri = self._radii[node["index"]]
                ri2 = ri * ri
                xi = node["x"] + node["vx"]
                yi = node["y"] + node["vy"]
                apply.update(node, xi, yi, ri, ri2)
                tree.visit(apply)

    def _prepare(self, quad):
        if isinstance(quad, dict) and quad["data"]:
            r = quad["r"] = self._radii[quad["data"]["index"]]
            return r
        quad.append(0)
        for i in range(4):
            if quad[i] and quadr(quad[i]) > quad[4]:
                quad[4] = quadr(quad[i])

    def _initialize(self):
        if self._nodes is None:
            return
        self._radii = [None] * len(self._nodes)
        for i, node in enumerate(self._nodes):
            self._radii[node["index"]] = self._radius(node, i, self._nodes)

    def initialize(self, nodes, random):
        self._nodes = nodes
        self._random = random
        self._initialize()

    def set_iterations(self, iterations: int):
        self._iterations = iterations
        return self

    def set_stength(self, strength: float):
        self._strength = strength
        return self

    def set_radius(self, radius):
        if callable(radius):
            self._radius = radius
        else:
            self._radius = constant(radius)
        self._initialize()
        return self

    def get_iterations(self) -> int:
        return self._iterations

    def get_strength(self) -> float:
        return self._strength

    def get_radius(self):
        return self._radius

def force_collide(radius=None):
    if not callable(radius):
        radius = constant(1 if radius is None else radius)
    return ForceCollide(radius)
