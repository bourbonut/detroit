from math import inf, sqrt
from ..quadtree import quadtree
from .constant import constant
from .jiggle import jiggle
from .simulation import x, y


class Apply:

    def __init__(self, alpha, strengths, distance_min_2, distance_max_2, random):
        self._alpha = alpha
        self._strengths = strengths
        self._distance_min_2 = distance_min_2
        self._distance_max_2 = distance_max_2
        self._random = random
        self._node = None

    def __call__(self, quad, x1, y1, x2, y2):
        if quad["value"] is None:
            return True
    
        x = quad["x"] - self._node["x"]
        y = quad["y"] - self._node["y"]
        w = x2 - x1
        length = x * x + y * y

        if w * w / self._theta2 < length:
            if length < self._distance_max_2:
                if x == 0:
                    x = jiggle(self._random)
                    length += x * x
                if y == 0:
                    y = jiggle(self._random)
                    length += y * y
                if length < self._distance_min_2:
                    length = sqrt(self._distance_min_2 * length)
                self._node["vx"] += x * quad["value"] * self._alpha / length
                self._node["vy"] += y * quad["value"] * self._alpha / length
            return True
        elif isinstance(quad, list) or length >= self._distance_max_2:
            return
        if quad["data"] != self._node or quad["next"]:
            if x == 0:
                x = jiggle(self._random)
                length += x * x
            if y == 0:
                y = jiggle(self._random)
                length += y * y
            if length < self._distance_min_2:
                length = sqrt(self._distance_min_2 * length)

        while quad["data"] != self._node:
            w = self._strengths[quad["data"]["index"]] * self._alpha / length
            self._node["vx"] += x * w
            self._node["vy"] += y * w
            quad = quad.get("next")
            if quad is None:
                break

    def update(self, node):
        self._node = node

class ForceManyBody:

    def __init__(self):
        self._nodes = None
        self._node = None
        self._random = None
        self._alpha = None
        self._strength = constant(-30)
        self._strengths = None
        self._distance_min_2 = 1
        self._distance_max_2 = inf
        self._theta2 = 0.81

    def __call__(self, alpha):
        tree = quadtree(self._nodes, x, y).visit_after(self._accumulate)
        self._alpha = alpha
        apply = Apply(
            self._alpha,
            self._strengths,
            self._distance_min_2,
            self._distance_max_2,
            self._random,
        )
        for node in self._nodes:
            apply.update(node)
            tree.visit(apply)

    def _initialize(self):
        if self._nodes is None:
            return
        self._strengths = [None] * len(self._nodes)
        for i, node in enumerate(self._nodes):
            self._strengths[node["index"]] = self._strength(node, i, self._nodes)

    def _accumulate(self, quad):
        strength = 0
        weight = 0

        if isinstance(quad, list):
            x = 0
            y = 0
            for q in quad:
                if q and abs(q["value"]):
                    c = abs(q["value"])
                    strength += q["value"]
                    weight += c
                    x += c * q["x"]
                    y += c * q["y"]
            quad["x"] = x / weight
            quad["y"] = y / weight
        else:
            q = quad
            q["x"] = q["data"]["x"]
            q["y"] = q["data"]["y"]
            while True:
                strength += self._strengths[q["data"]["index"]]
                q = q.get("next")
                if q is None:
                    break
        quad["value"] = strength

    def initialize(self, nodes, random):
        self._nodes = nodes
        self._random = random
        self._initialize()

    def set_strength(self, strength):
        if callable(strength):
            self._strength == strength
        else:
            self._strength = constant(strength)
        self._initialize()
        return self

    def set_distance_min(self, distance_min):
        self._distance_min_2 = distance_min * distance_min
        return self

    def set_distance_max(self, distance_max):
        self._distance_max_2 = distance_max * distance_max
        return self

    def set_theta(self, theta):
        self._theta2 = theta * theta
        return self

    def get_strength(self):
        return self._strength

    def get_distance_min(self):
        return sqrt(self._distance_min_2)

    def get_distance_max(self):
        return sqrt(self._distance_max_2)

    def get_theta(self):
        return sqrt(self._theta2)

def force_many_body():
    return ForceManyBody()
