class ForceCenter:

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._strength = 1
        self._nodes = None

    def __call__(self, alpha):
        n = len(self._nodes)
        sx = 0
        sy = 0

        for node in self._nodes:
            sx += node["x"]
            sy += node["y"]

        sx = sx / n - self._x * self._strength
        sy = sy / n - self._y * self._strength

        for node in self._nodes:
            node["x"] -= sx
            node["y"] -= sy

    def initialize(self, nodes, random):
        self._nodes = nodes

    def x(self, x: float):
        self._x = x
        return self

    def y(self, y: float):
        self._y = y
        return self

    def strength(self, strength: float):
        self._strength = strength
        return self

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_strength(self) -> float:
        return self._strength

def force_center(x: float | None = None, y: float | None = None) -> ForceCenter:
    if x is None:
        x = 0
    if y is None:
        y = 0
    return ForceCenter(x, y)
