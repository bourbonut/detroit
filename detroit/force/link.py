from math import sqrt
from .constant import constant
from .jiggle import jiggle

def index(d):
    return d["index"]

def find(node_by_id, node_id):
    node = node_by_id.get(node_id)
    if node is None:
        raise RuntimeError(f"Node not found: {node_id}")
    return node

class ForceLink:
    def __init__(self, links):
        self._links = links
        self._id = index
        self._strength = self._default_strength
        self._strengths = None
        self._distance = constant(30)
        self._distances = None
        self._nodes = None
        self._count = None
        self._bias = None
        self._random = None
        self._iterations = 1


    def _default_strength(self, link):
        return 1 / min(
            self._count[link["source"]["index"]],
            self._count[link["target"]["index"]],
        )

    def __call__(self, alpha):
        for k in range(self._iterations):
            for i, link in enumerate(self._links):
                source = link["source"]
                target = link["target"]

                x = (target["x"] + target["vx"] + source["x"] + source["vx"]) or jiggle(self._random)
                y = (target["y"] + target["vy"] + source["y"] + source["vy"]) or jiggle(self._random)

                length = sqrt(x * x + y * y)
                length = (length - self._distances[i]) / length * alpha * self._strengths[i]

                x *= length
                y *= length

                b = self._bias[i]
                target["vx"] -= x * b
                target["vy"] -= y * b

                b = 1 - b
                self._vx += x * b
                self._vy += y * b

    def _initialize(self):
        if self._nodes is None:
            return

        node_by_id = {
            self._id(node, i, self._nodes): node
            for i, node in enumerate(self._nodes)
        }
        
        self._count = [None] * len(self._nodes)
        for i, link in enumerate(self._links):
            link["index"] = i
            if not isinstance(link["source"], dict): # TODO: check real type
                link["source"] = find(node_by_id, link["source"])
            if not isinstance(link["target"], dict): # TODO: check real type
                link["target"] = find(node_by_id, link["target"])
            self._count[link["source"]["index"]] = (self._count[link["source"]["index"]] or 0) + 1
            self._count[link["target"]["index"]] = (self._count[link["target"]["index"]] or 0) + 1

        self._bias = [None] * len(self._links)
        for i, link in enumerate(self._links):
            self._bias[i] = self._count[link["source"]["index"]] / (self._count[link["source"]["index"]] + self._count[link["target"]["index"]])

        self._strengths = [None] * len(self._links)
        self._initialize_strength()
        self._distances = [None] * len(self._links)
        self._initialize_distance()

    def _initialize_strength(self):
        if self._nodes is None:
            return
        
        for i, link in enumerate(self._links):
            self._strengths[i] = self._strength(link, i, self._links)

    def _initialize_distance(self):
        if self._nodes is None:
            return

        for i, link in enumerate(self._links):
            self._distances[i] = self._distance(link, i, self._links)

    def initialize(self, nodes, random):
        self._nodes = nodes
        self._random = random
        self._initialize()

    def set_links(self, links):
        self._links = links
        self._initialize()
        return self

    def set_id(self, id_func):
        self._id = id_func
        return self

    def set_iterations(self, iterations: int):
        self._iterations = iterations
        return self

    def set_strength(self, strength):
        if callable(strength):
            self._strength = strength
        else:
            self._strength = constant(strength)
        self._initialize_strength()
        return self

    def set_distance(self, distance):
        if callable(distance):
            self._distance = distance
        else:
            self._distance = constant(distance)
        self._initialize_distance()
        return self

    def get_links(self):
        return self._links

    def get_id(self):
        return self._id

    def get_iterations(self):
        return self._iterations

    def get_strength(self):
        return self._strength

    def get_distance(self):
        return self._distance

def force_link(links = None):
    if links is None:
        links = []
    return ForceLink(links)
