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
from typing import TypeVar
from math import sqrt
from .constant import constant
from .jiggle import jiggle
from ..array import argpass
from ..types import T, SimulationNode, SimulationLink, SimulationNodeFunction, SimulationLinkFunction

TForceLink = TypeVar("ForceLink", bound="ForceLink")

def index(d: SimulationNode) -> int:
    return d["index"]

def find(node_by_id: dict[T, SimulationNode], node_id: T) -> SimulationNode:
    node = node_by_id.get(node_id)
    if node is None:
        raise RuntimeError(f"Node not found: {node_id}")
    return node

class ForceLink:
    def __init__(self, links: list[SimulationLink]):
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


    def _default_strength(self, link: SimulationLink, i: int, links: list[SimulationLink]) -> float:
        return 1 / min(
            self._count[link["source"]["index"]],
            self._count[link["target"]["index"]],
        )

    def __call__(self, alpha: float):
        for k in range(self._iterations):
            for i, link in enumerate(self._links):
                source = link["source"]
                target = link["target"]

                x = (target["x"] + target["vx"] - source["x"] - source["vx"]) or jiggle(self._random)
                y = (target["y"] + target["vy"] - source["y"] - source["vy"]) or jiggle(self._random)

                length = sqrt(x * x + y * y)
                length = (length - self._distances[i]) / length * alpha * self._strengths[i]

                x *= length
                y *= length

                b = self._bias[i]
                target["vx"] -= x * b
                target["vy"] -= y * b

                b = 1 - b
                source["vx"] += x * b
                source["vy"] += y * b

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

    def initialize(self, nodes: list[SimulationNode], random: Callable[[None], float]):
        self._nodes = nodes
        self._random = random
        self._initialize()

    def set_links(self, links: list[SimulationLink]) -> TForceLink:
        """
        Sets the array of links associated with this force, recomputes the
        distance and strength parameters for each link, and returns this force.

        Each link is an object with the following properties:

        * **source** - the link's source node; see simulation.nodes
        * **target** - the link's target node; see simulation.nodes
        * **index** - the zero-based index into links, assigned by this method

        For convenience, a link's source and target properties may be
        initialized using numeric or string identifiers rather than object
        references.

        Parameters
        ----------
        links : list[SimulationLink]
            List of links

        Returns
        -------
        ForceLink
            Itself
        """
        self._links = links
        self._initialize()
        return self

    def set_id(self, id_func: SimulationNodeFunction[int]) -> TForceLink:
        """
        Sets the node ID accessor to the specified function and returns this
        force.

        Parameters
        ----------
        id_func : SimulationNodeFunction[int]
            ID accessor function which takes the following arguments:

            * **node** (:code:`SimulationNode`) - the node element
            * **i** (:code:`int`) - the index of the node
            * **nodes** (:code:`list[SimulationNode]`) - the list of nodes

            It returns the ID value (:code:`int`)

        Returns
        -------
        ForceLink
            Itself
        """
        self._id = argpass(id_func)
        return self

    def set_iterations(self, iterations: int) -> TForceLink:
        """
        Sets the number of iterations per application to the specified number
        and returns this force.

        Parameters
        ----------
        iterations : int
            Number of iterations

        Returns
        -------
        ForceLink
            Itself
        """
        self._iterations = iterations
        return self

    def set_strength(self, strength: SimulationLinkFunction[float] | float) -> TForceLink:
        """
        Sets the strength accessor to the specified number or function,
        re-evaluates the strength accessor for each link, and returns this
        force.

        Parameters
        ----------
        strength : SimulationLinkFunction[float] | float
            Strength function or constant value. If it is a function, it takes
            the following arguments:

            * **link** (:code:`SimulationLink`) - the link element
            * **i** (:code:`int`) - the index of the node
            * **links** (:code:`list[SimulationLink]`) - the list of links

            It returns the strength value (:code:`float`)

        Returns
        -------
        ForceLink
            Itself
        """
        if callable(strength):
            self._strength = argpass(strength)
        else:
            self._strength = constant(strength)
        self._initialize_strength()
        return self

    def set_distance(self, distance: SimulationNodeFunction[float] | float) -> TForceLink:
        """
        Sets the distance accessor to the specified number or function,
        re-evaluates the distance accessor for each link, and returns this
        force.

        Parameters
        ----------
        distance : SimulationNodeFunction[float] | float
            Distance function or constant value. If it is a function, it takes
            the following arguments:

            * **node** (:code:`SimulationNode`) - the node element
            * **i** (:code:`int`) - the index of the node
            * **nodes** (:code:`list[SimulationNode]`) - the list of nodes

            It returns the distance value (:code:`float`)

        Returns
        -------
        ForceLink
            Itself
        """
        if callable(distance):
            self._distance = argpass(distance)
        else:
            self._distance = constant(distance)
        self._initialize_distance()
        return self

    def get_links(self) -> list[SimulationLink]:
        return self._links

    def get_id(self) -> SimulationNodeFunction[int]:
        return self._id

    def get_iterations(self) -> int:
        return self._iterations

    def get_strength(self) -> SimulationNodeFunction[float]:
        return self._strength

    def get_distance(self) -> SimulationNodeFunction[float]:
        return self._distance

def force_link(links: list[SimulationLink] | None = None) -> ForceLink:
    """
    The link force pushes linked nodes together or apart according to the
    desired link distance. The strength of the force is proportional to the
    difference between the linked nodes' distance and the target distance,
    similar to a spring force.

    Parameters
    ----------
    links : list[SimulationLink] | None
        List of links

    Returns
    -------
    ForceLink
        Force object
    """
    if links is None:
        links = []
    return ForceLink(links)
