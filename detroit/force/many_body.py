from collections.abc import Callable
from math import inf, sqrt
from typing import TypeVar

from ..array import argpass
from ..quadtree import quadtree
from ..types import SimulationNode, SimulationNodeFunction
from .constant import constant
from .jiggle import jiggle
from .simulation import x, y

TForceManyBody = TypeVar("ForceManyBody", bound="ForceManyBody")

class Apply:

    def __init__(
        self,
        alpha: float,
        strengths: list[float],
        distance_min_2: float,
        distance_max_2: float,
        theta2: float,
        random: Callable[[None], float],
    ):
        self._alpha = alpha
        self._strengths = strengths
        self._distance_min_2 = distance_min_2
        self._distance_max_2 = distance_max_2
        self._theta2 = theta2
        self._random = random
        self._node = None

    def __call__(self, quad: list[dict] | dict, x1: float, y1: float, x2: float, y2: float):
        value = quad["value"] if isinstance(quad, dict) else quad[4]["value"]
        if not value:
            return True
    
        qx = quad["x"] if isinstance(quad, dict) else quad[4]["x"]
        qy = quad["y"] if isinstance(quad, dict) else quad[4]["y"]
        x = qx - self._node["x"]
        y = qy - self._node["y"]
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
                self._node["vx"] += x * value * self._alpha / length
                self._node["vy"] += y * value * self._alpha / length
            return True
        elif isinstance(quad, list) or length >= self._distance_max_2:
            return
        if quad["data"] != self._node or quad.get("next"):
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

    def update(self, node: SimulationNode):
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

    def __call__(self, alpha: float):
        tree = quadtree(self._nodes, x, y).visit_after(self._accumulate)
        self._alpha = alpha
        apply = Apply(
            self._alpha,
            self._strengths,
            self._distance_min_2,
            self._distance_max_2,
            self._theta2,
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

    def _accumulate(self, quad: list[dict] | dict):
        strength = 0
        weight = 0

        if isinstance(quad, list):
            x = 0
            y = 0
            for q in quad:
                if not q:
                    continue
                if isinstance(q, dict):
                    value = q["value"]
                    qx = q["x"]
                    qy = q["y"]
                else: # fifth element of a quad as a list
                    value = q[4]["value"]
                    qx = q[4]["x"]
                    qy = q[4]["y"]
                if value:
                    c = abs(value)
                    strength += value
                    weight += c
                    x += c * qx
                    y += c * qy
            if len(quad) == 4:
                quad.append({"x": x / weight, "y": y / weight})
            else:
                quad[4]["x"] = x / weight
                quad[4]["y"] = y / weight
            quad[4]["value"] = strength
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

    def initialize(self, nodes: list[SimulationNode], random: Callable[[None], float]):
        self._nodes = nodes
        self._random = random
        self._initialize()

    def set_strength(self, strength: SimulationNodeFunction[float] | float) -> TForceManyBody:
        """
        Sets the strength accessor to the specified number or function,
        re-evaluates the strength accessor for each node, and returns this
        force. A positive value causes nodes to attract each other, similar to
        gravity, while a negative value causes nodes to repel each other,
        similar to electrostatic charge.

        Parameters
        ----------
        strength : SimulationNodeFunction[float] | float
            Strength function or constant value. If it is a function, it takes
            the following arguments:

            * **node** (:code:`SimulationNode`) - the node element
            * **i** (:code:`int`) - the index of the node
            * **nodes** (:code:`list[SimulationNode]`) - the list of nodes

            It returns the strength value (:code:`float`)

        Returns
        -------
        ForceManyBody
            Itself
        """
        if callable(strength):
            self._strength = argpass(strength)
        else:
            self._strength = constant(strength)
        self._initialize()
        return self

    def set_distance_min(self, distance_min: float) -> TForceManyBody:
        """
        Sets the minimum distance between nodes over which this force is
        considered.

        A minimum distance establishes an upper bound on the strength of the
        force between two nearby nodes, avoiding instability. In particular, it
        avoids an infinitely-strong force if two nodes are exactly coincident;
        in this case, the direction of the force is random.

        Parameters
        ----------
        distance_min : float
            Minimum distance value   

        Returns
        -------
        ForceManyBody
            Itself
        """
        self._distance_min_2 = distance_min * distance_min
        return self

    def set_distance_max(self, distance_max: float) -> TForceManyBody:
        """
        sets the maximum distance between nodes over which this force is
        considered.

        Specifying a finite maximum distance improves performance and produces
        a more localized layout.

        Parameters
        ----------
        distance_max : float
            Maximum distance value   

        Returns
        -------
        ForceManyBody
            Itself
        """
        self._distance_max_2 = distance_max * distance_max
        return self

    def set_theta(self, theta: float) -> TForceManyBody:
        """
        Sets the Barnes-Hut approximation criterion to the specified number and
        returns this force.

        To accelerate computation, this force implements the `Barnes - Hut
        approximation
        <https://en.wikipedia.org/wiki/Barnes%E2%80%93Hut_simulation>`_ which
        takes :math:`O(n \\cdot \\log(n))` per application where :math:`n` is
        the number of nodes. For each application, a quadtree stores the
        current node positions; then for each node, the combined force of all
        other nodes on the given node is computed. For a cluster of nodes that
        is far away, the charge force can be approximated by treating the
        cluster as a single, larger node. The theta parameter determines the
        accuracy of the approximation: if the ratio :math:`w / l` of the width
        w of the quadtree cell to the distance :math:`l` from the node to the
        cell's center of mass is less than :math:`\\theta`, all nodes in the
        given cell are treated as a single node rather than individually.

        Parameters
        ----------
        theta : float
            Barnes-Hut approximation criterion value

        Returns
        -------
        ForceManyBody
            Itself
        """
        self._theta2 = theta * theta
        return self

    def get_strength(self) -> SimulationNodeFunction[float]:
        return self._strength

    def get_distance_min(self) -> float:
        return sqrt(self._distance_min_2)

    def get_distance_max(self) -> float:
        return sqrt(self._distance_max_2)

    def get_theta(self) -> float:
        return sqrt(self._theta2)

def force_many_body() -> ForceManyBody:
    """
    The many-body (or n-body) force applies mutually amongst all nodes. It can
    be used to simulate gravity (attraction) if the strength is positive, or
    electrostatic charge (repulsion) if the strength is negative. This
    implementation uses a quadtree and the Barnes–Hut approximation to greatly
    improve performance; the accuracy can be customized using the theta
    parameter.

    Unlike the link force, which only affect two linked nodes, the charge force
    is global: every node affects every other node, even if they are on
    disconnected subgraphs.

    Returns
    -------
    ForceManyBody
        Force object
    """
    return ForceManyBody()
