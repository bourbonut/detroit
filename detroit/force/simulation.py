from .lcg import lcg
from math import pi, sqrt, isnan, cos, sin, inf, nan

def x(d):
    return d["x"]

def y(d):
    return d["y"]

INITIAL_RADIUS = 10
INITIAL_ANGLE = pi * (3 - sqrt(5))

class ForceSimulation:

    def __init__(self, nodes):
        self._nodes = nodes
        self._alpha = 1
        self._alpha_min = 0.001
        self._alpha_decay = 1 - pow(self._alpha_min, 1 / 300)
        self._alpha_target = 0
        self._velocity_decay = 0.6
        self._forces = {}
        self._random = lcg()
        self._initialize_nodes()


    def tick(self, iterations = None):
        if iterations is None:
            iterations = 1

        for k in range(iterations):
            self._alpha += (self._alpha_target - self._alpha) * self._alpha_decay

            for force in self._forces.values():
                force(self._alpha)

            for node in self._nodes:
                if node.get("fx") is None:
                    node["vx"] *= self._velocity_decay
                    node["x"] += node["vx"]
                else:
                    node["x"] = node["fx"]
                    node["vx"] = 0

                if node.get("fy") is None:
                    node["vy"] *= self._velocity_decay
                    node["y"] += node["vy"]
                else:
                    node["y"] = node["fy"]
                    node["vy"] = 0

        return self

    def _initialize_nodes(self):
        for i, node in enumerate(self._nodes):
            node["index"] = i
            if fx := node.get("fx"):
                node["x"] = fx
            if fy := node.get("fy"):
                node["y"] = fy
            if isnan(node.get("x", nan)) or isnan(node.get("y", nan)):
                radius = INITIAL_RADIUS * sqrt(0.5 + i)
                angle = i * INITIAL_ANGLE
                node["x"] = radius * cos(angle)
                node["y"] = radius * sin(angle)
            if isnan(node.get("vx", nan)) or isnan(node.get("vy", nan)):
                node["vx"] = 0
                node["vy"] = 0

    def _initialize_force(self, force):
        if hasattr(force, "initialize"):
            force.initialize(self._nodes, self._random)
        return force

    def find(self, x, y, radius = None):
        if radius is None:
            radius = inf
        else:
            radius *= radius

        closest = None
        for node in self._nodes:
            dx = x - node["x"]
            dy = y - node["y"]
            d2 = dx * dx + dy * dy
            if d2 < radius:
                closest = node
                radius = d2

        return closest

    def set_nodes(self, nodes):
        self._nodes = nodes
        self._initialize_nodes()
        for force in self._forces.values():
            self._initialize_force(force)
        return self

    def set_alpha(self, alpha):
        self._alpha = alpha
        return self

    def set_alpha_min(self, alpha_min):
        self._alpha_min = alpha_min
        return self

    def set_alpha_decay(self, alpha_decay):
        self._alpha_decay = alpha_decay
        return self

    def alpha_target(self, alpha_target):
        self._alpha_target = alpha_target
        return self

    def set_velocity_decay(self, velocity_decay):
        self._velocity_decay = 1 - velocity_decay
        return self

    def set_random_source(self, random_source):
        self._random = random_source
        for force in self._forces:
            self._initialize_force(force)
        return self

    def set_force(self, name, force = None):
        if force is None:
            self._forces.pop(name)
        else:
            self._forces[name] = self._initialize_force(force)
        return self

    def get_alpha(self):
        return self._alpha

    def get_alpha_min(self):
        return self._alpha_min

    def get_alpha_decay(self):
        return self._alpha_decay

    def get_alpha_target(self):
        return self._alpha_target

    def get_velocity_decay(self):
        return 1 - self._velocity_decay
    
    def get_random_source(self):
        return self._random

    def get_force(self, name: str):
        return self._forces.get(name)

    def get_nodes(self):
        return self._nodes

def force_simulation(nodes=None):
    if nodes is None:
        nodes = []
    return ForceSimulation(nodes)
