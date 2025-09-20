from collections.abc import Callable
from math import isnan
from typing import TypeVar
from .constant import constant
from ..array import argpass
from ..types import SimulationNode, SimulationNodeFunction

TForceX = TypeVar("ForceX", bound="ForceX")

class ForceX:

    def __init__(self, x: SimulationNodeFunction[float]):
        self._x = x
        self._strength = constant(0.1)
        self._nodes = None
        self._strengths = None
        self._xz = None

    def __call__(self, alpha: float):
        for i, node in enumerate(self._nodes):
            node["vx"] += (self._xz[i] - node["x"]) * self._strengths[i] * alpha

    def _initialize(self):
        if self._nodes is None:
            return

        self._strengths = [None] * len(self._nodes)
        self._xz = [None] * len(self._nodes)
        for i, node in enumerate(self._nodes):
            self._xz[i] = x = self._x(node, i, self._nodes)
            self._strengths[i] = 0 if isnan(x) else self._strength(node, i, self._nodes)

    def initialize(self, nodes: list[SimulationNode], random: Callable[[None], float]):
        self._nodes = nodes
        self._initialize()

    def set_strength(self, strength: SimulationNodeFunction[float] | float) -> TForceX:
        """
        Sets the strength accessor to the specified number or function,
        re-evaluates the strength accessor for each node, and returns this
        force.

        The strength determines how much to increment the node's x-velocity:
        :code:`(x - node["x"]) * strength`. For example, a value of :math:`0.1`
        indicates that the node should move a tenth of the way from its current
        x-position to the target x-position with each application. Higher
        values moves nodes more quickly to the target position, often at the
        expense of other forces or constraints. A value outside the range
        :math:`[0,1]` is not recommended.

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
        ForceX
            Itself
        """
        if callable(strength):
            self._strength = argpass(strength)
        else:
            self._strength = constant(strength)
        self._initialize()
        return self

    def x(self, x: SimulationNodeFunction[float] | float) -> TForceX:
        """
        Sets the x-coordinate accessor to the specified number or function,
        re-evaluates the x-accessor for each node, and returns this force.

        Parameters
        ----------
        x : SimulationNodeFunction[float] | float
            x-coordinate function or constant value. If it is a function, it takes
            the following arguments:

            * **node** (:code:`SimulationNode`) - the node element
            * **i** (:code:`int`) - the index of the node
            * **nodes** (:code:`list[SimulationNode]`) - the list of nodes

            It returns the x-coordinate value (:code:`float`)
            
        Returns
        -------
        ForceX
            Itself
        """
        if callable(x):
            self._x = argpass(x)
        else:
            self._x = constant(x)
        self._initialize()
        return self

    def get_strength(self) -> SimulationNodeFunction[float]:
        return self._strength

    def get_x(self) -> SimulationNodeFunction[float]:
        return self._x

def force_x(x: SimulationNodeFunction[float] | float | None = None) -> ForceX:
    """
    The x-position force pushes nodes towards a desired position along the
    given dimension with a configurable strength.

    The strength of the force is proportional to the one-dimensional distance
    between the node's position and the target position. While these forces can
    be used to position individual nodes, they are intended primarily for
    global forces that apply to all (or most) nodes.

    Parameters
    ----------
    x : SimulationNodeFunction[float] | float | None
        x-coordinate function or constant value. If it is a function, it takes
        the following arguments:

        * **node** (:code:`SimulationNode`) - the node element
        * **i** (:code:`int`) - the index of the node
        * **nodes** (:code:`list[SimulationNode]`) - the list of nodes

        It returns the x-coordinate value (:code:`float`)

    Returns
    -------
    ForceX
        Force object
    """
    if not callable(x):
        x = constant(0 if x is None else x)
    else:
        x = argpass(x)

    return ForceX(argpass(x))
