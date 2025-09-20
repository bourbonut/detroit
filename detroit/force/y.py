from collections.abc import Callable
from math import isnan
from typing import TypeVar
from .constant import constant
from ..array import argpass
from ..types import SimulationNode, SimulationNodeFunction

TForceY = TypeVar("ForceY", bound="ForceY")

class ForceY:

    def __init__(self, y: SimulationNodeFunction[float]):
        self._y = y
        self._strength = constant(0.1)
        self._nodes = None
        self._strengths = None
        self._yz = None

    def __call__(self, alpha: float):
        for i, node in enumerate(self._nodes):
            node["vy"] += (self._yz[i] - node["y"]) * self._strengths[i] * alpha

    def _initialize(self):
        if self._nodes is None:
            return

        self._strengths = [None] * len(self._nodes)
        self._yz = [None] * len(self._nodes)
        for i, node in enumerate(self._nodes):
            self._yz[i] = y = self._y(node, i, self._nodes)
            self._strengths[i] = 0 if isnan(y) else self._strength(node, i, self._nodes)

    def initialize(self, nodes: list[SimulationNode], random: Callable[[None], float]):
        self._nodes = nodes
        self._initialize()

    def set_strength(self, strength: SimulationNodeFunction[float] | float) -> TForceY:
        """
        Sets the strength accessor to the specified number or function,
        re-evaluates the strength accessor for each node, and returns this
        force.

        The strength determines how much to increment the node's y-velocity:
        :code:`(y - node["y"]) * strength`. For example, a value of :math:`0.1`
        indicates that the node should move a tenth of the way from its current
        x-position to the target y-position with each application. Higher
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
        ForceY
            Itself
        """
        if callable(strength):
            self._strength = argpass(strength)
        else:
            self._strength = constant(strength)
        self._initialize()
        return self

    def y(self, y: SimulationNodeFunction[float] | float) -> TForceY:
        """
        Sets the y-coordinate accessor to the specified number or function,
        re-evaluates the y-accessor for each node, and returns this force.

        Parameters
        ----------
        y : SimulationNodeFunction[float] | float
            y-coordinate function or constant value. If it is a function, it takes
            the following arguments:

            * **node** (:code:`SimulationNode`) - the node element
            * **i** (:code:`int`) - the index of the node
            * **nodes** (:code:`list[SimulationNode]`) - the list of nodes

            It returns the y-coordinate value (:code:`float`)
            
        Returns
        -------
        ForceY
            Itself
        """
        if callable(y):
            self._y = argpass(y)
        else:
            self._y = constant(y)
        self._initialize()
        return self

    def get_strength(self):
        return self._strength

    def get_y(self):
        return self._y

def force_y(y: SimulationNodeFunction[float] | float | None = None):
    """
    The y-position force pushes nodes towards a desired position along the
    given dimension with a configurable strength.

    The strength of the force is proportional to the one-dimensional distance
    between the node's position and the target position. While these forces can
    be used to position individual nodes, they are intended primarily for
    global forces that apply to all (or most) nodes.

    Parameters
    ----------
    y : SimulationNodeFunction[float] | float | None
        y-coordinate function or constant value. If it is a function, it takes
        the following arguments:

        * **node** (:code:`SimulationNode`) - the node element
        * **i** (:code:`int`) - the index of the node
        * **nodes** (:code:`list[SimulationNode]`) - the list of nodes

        It returns the y-coordinate value (:code:`float`)

    Returns
    -------
    ForceY
        Force object
    """
    if not callable(y):
        y = constant(0 if y is None else y)
    else:
        y = argpass(y)

    return ForceY(argpass(y))
