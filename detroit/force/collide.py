# Since Javascript accepts weird stuff, I had to make the same programming
# "errors" / "mistakes" in order to keep as simple as possible the code. These
# "mistakes" are adding attributes to array object. For instance, in
# Javascript, you can do
# ```js
# var myarray = [1, 2, 3];
# myarray.data = 42
# ```
# In Python, this would raise an error. However, in this specific algorihm,
# lists have a fixed length of 4. I have used this assumption and I dynamically
# add a fifth element (of type `dict`) in `quad` objects in order to *mimic*
# the same behavior.
from collections.abc import Callable
from math import sqrt, nan
from typing import TypeVar

from ..array import argpass
from ..quadtree import quadtree
from ..types import SimulationNode, SimulationNodeFunction
from .constant import constant
from .jiggle import jiggle

TForceCollide = TypeVar("ForceCollide", bound="ForceCollide")

def x(d: dict[str, float]) -> float:
    return d["x"] + d["vx"]

def y(d: dict[str, float]) -> float:
    return d["y"] + d["vy"]

def quadr(quad: dict | list) -> float:
    return quad["r"] if isinstance(quad, dict) else quad[4]["r"]

class Apply:
    def __init__(self, strength: float, random: Callable[[None], float]):
        self._random = random
        self._strength = strength
        self._node = None
        self._xi = nan
        self._yi = nan
        self._ri = nan
        self._ri2 = nan

    def __call__(self, quad: dict | list[dict], x0: float, y0: float, x1: float, y1: float):
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

    def update(self, node: dict, xi: float, yi: float, ri: float, ri2: float):
        self._node = node
        self._xi = xi
        self._yi = yi
        self._ri = ri
        self._ri2 = ri2

class ForceCollide:

    def __init__(self, radius: SimulationNodeFunction[float]):
        self._radius = radius
        self._nodes = None
        self._radii = None
        self._random = None
        self._strength = 1
        self._iterations = 1

    def __call__(self, alpha: float | None = None):
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

    def _prepare(self, quad: dict | list[dict]):
        if isinstance(quad, dict) and quad["data"]:
            r = quad["r"] = self._radii[quad["data"]["index"]]
            return r
        if len(quad) == 4:
            quad.append({"r": 0})
        else: # it assumes there is a fifth element of type `dict`
            quad[4]["r"] = 0
        for i in range(4):
            if quad[i] and quadr(quad[i]) > quad[4]["r"]:
                quad[4]["r"] = quadr(quad[i])

    def _initialize(self):
        if self._nodes is None:
            return
        self._radii = [None] * len(self._nodes)
        for i, node in enumerate(self._nodes):
            self._radii[node["index"]] = self._radius(node, i, self._nodes)

    def initialize(self, nodes: list[SimulationNode], random: Callable[[None], float]):
        self._nodes = nodes
        self._random = random
        self._initialize()

    def set_iterations(self, iterations: int) -> TForceCollide:
        """
        Sets the number of iterations per application to the specified number
        and returns this force.

        Increasing the number of iterations greatly increases the rigidity of
        the constraint and avoids partial overlap of nodes, but also increases
        the runtime cost to evaluate the force.

        Parameters
        ----------
        iterations : int
            Iterations value

        Returns
        -------
        ForceCollide
            Itself
        """
        self._iterations = iterations
        return self

    def set_stength(self, strength: float) -> TForceCollide:
        """
        Sets the force strength to the specified number in the range
        :math:`[0,1]` and returns this force.

        Overlapping nodes are resolved through iterative relaxation. For each
        node, the other nodes that are anticipated to overlap at the next tick
        (using the anticipated positions :math:`(x + v_x,y + v_y)`) are
        determined; the node's velocity is then modified to push the node out
        of each overlapping node. The change in velocity is dampened by the
        force's strength such that the resolution of simultaneous overlaps can
        be blended together to find a stable solution.

        Parameters
        ----------
        strength : float
            Strength value in the range :math:`[0, 1]`

        Returns
        -------
        ForceCollide
            Itself
        """
        self._strength = strength
        return self

    def set_radius(self, radius: SimulationNodeFunction[float] | float) -> TForceCollide:
        """
        Sets the radius accessor to the specified number or function,
        re-evaluates the radius accessor for each node, and returns this force.

        The radius accessor is invoked for each node in the simulation, being
        passed the node and its zero-based index. The resulting number is then
        stored internally, such that the radius of each node is only recomputed
        when the force is initialized or when this method is called with a new
        radius, and not on every application of the force.

        Parameters
        ----------
        radius : SimulationNodeFunction[float] | float
            Radius function or constant value. If it is a function, it takes
            the following arguments:

            * **node** (:code:`SimulationNode`) - the node element
            * **i** (:code:`int`) - the index of the node
            * **nodes** (:code:`list[SimulationNode]`) - the list of nodes

            It returns a radius value (:code:`float`).

        Returns
        -------
        ForceCollide
            Itself
        """
        if callable(radius):
            self._radius = argpass(radius)
        else:
            self._radius = constant(radius)
        self._initialize()
        return self

    def get_iterations(self) -> int:
        return self._iterations

    def get_strength(self) -> float:
        return self._strength

    def get_radius(self) -> SimulationNodeFunction[float]:
        return self._radius

def force_collide(
    radius: SimulationNodeFunction[float] | float | None = None
) -> ForceCollide:
    """
    The collide force treats nodes as circles with a given radius, rather than
    points, and prevents nodes from overlapping. More formally, two nodes *a*
    and *b* are separated so that the distance between :code:`a` and :code:`b`
    is at least :code:`radius(a) + radius(b)`. To reduce jitter, this is by
    default a "soft" constraint with a configurable strength and iteration
    count.

    Parameters
    ----------
    radius : SimulationNodeFunction[float] | float | None
        Radius function or constant value. If it is a function, it takes
        the following arguments:

        * **node** (:code:`SimulationNode`) - the node element
        * **i** (:code:`int`) - the index of the node
        * **nodes** (:code:`list[SimulationNode]`) - the list of nodes

        It returns a radius value (:code:`float`). If :code:`radius` is not
        specified, the default value is a constant function which returns
        :code:`1`.

    Returns
    -------
    ForceCollide
        Force object
    """
    if not callable(radius):
        radius = constant(1 if radius is None else radius)
    else:
        radius = argpass(radius)
    return ForceCollide(radius)
