from collections.abc import Callable
from math import sqrt, isnan
from typing import TypeVar
from .constant import constant
from ..array import argpass
from ..types import SimulationNode, SimulationNodeFunction

TForceRadial = TypeVar("ForceRadial", bound="ForceRadial")

class ForceRadial:
    def __init__(self, radius: SimulationNodeFunction[float], x: float, y: float):
        self._radius = radius
        self._x = x
        self._y = y
        self._strength = constant(0.1)
        self._strengths = None
        self._radiuses = None

    def __call__(self, alpha: float):
        for i, node in enumerate(self._nodes):
            dx = (node["x"] - self._x) or 1e-6
            dy = (node["y"] - self._y) or 1e-6
            r = sqrt(dx * dx + dy * dy)
            k = (self._radiuses[i] - r) * self._strengths[i] * alpha / r
            node["vx"] += dx * k
            node["vy"] += dy * k

    def _initialize(self):
        if self._nodes is None:
            return

        n = len(self._nodes)
        self._strengths = [None] * n
        self._radiuses = [None] * n

        for i, node in enumerate(self._nodes):
            self._radiuses[i] = r = self._radius(node, i, self._nodes)
            self._strengths[i] = 0 if isnan(r) else self._strength(node, i, self._nodes)

    def initialize(self, nodes: list[SimulationNode], random: Callable[[None], float]):
        self._nodes = nodes
        self._initialize()

    def set_strength(self, strength: SimulationNodeFunction[float] | float) -> TForceRadial:
        """
        Sets the strength accessor to the specified number or function,
        re-evaluates the strength accessor for each node, and returns this
        force. The strength determines how much to increment the node's x- and
        y-velocity.
    
        For example, a value of :math:`0.1` indicates that the node should move
        a tenth of the way from its current position to the closest point on
        the circle with each application. Higher values moves nodes more
        quickly to the target position, often at the expense of other forces or
        constraints. A value outside the range :math:`[0,1]` is not
        recommended.

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
        ForceRadial
            Itself
        """
        if callable(strength):
            self._strength = argpass(strength)
        else:
            self._strength = constant(strength)
        self._initialize()
        return self

    def set_radius(self, radius: SimulationNodeFunction[float] | float) -> TForceRadial:
        """
        Sets the circle radius to the specified number or function,
        re-evaluates the radius accessor for each node, and returns this force.

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
        ForceRadial
            Force object
        """
        if callable(radius):
            self._radius = argpass(radius)
        else:
            self._radius = constant(radius)
        self._initialize()
        return self

    def x(self, x: float) -> TForceRadial:
        """
        Sets the x-coordinate of the circle center to the specified number and
        returns this force.

        Parameters
        ----------
        x : float
            X-coordinate of circle center   

        Returns
        -------
        ForceRadial
            Itself
        """
        self._x = x
        return self

    def y(self, y: float) -> TForceRadial:
        """
        Sets the y-coordinate of the circle center to the specified number and
        returns this force.

        Parameters
        ----------
        y : float
            y-coordinate of circle center   

        Returns
        -------
        ForceRadial
            Itself
        """
        self._y = y
        return self

    def get_strength(self) -> SimulationNodeFunction[float]:
        return self._strength

    def get_radius(self) -> SimulationNodeFunction[float]:
        return self._radius

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

def force_radial(
    radius: SimulationNodeFunction[float] | float,
    x: float | None = None,
    y: float | None = None,
) -> ForceRadial:
    """
    Creates a new position force towards a circle of the specified radius
    centered at :math`(x,y)`. If x and y are not specified, they default to
    :code:`(0,0)`.

    Parameters
    ----------
    radius : SimulationNodeFunction[float] | float
        Radius function or constant value. If it is a function, it takes
        the following arguments:

        * **node** (:code:`SimulationNode`) - the node element
        * **i** (:code:`int`) - the index of the node
        * **nodes** (:code:`list[SimulationNode]`) - the list of nodes

        It returns a radius value (:code:`float`).

    x : float | None
        X-coordinate of circle center
    y : float | None
        Y-coordinate of circle center

    Returns
    -------
    ForceRadial
        Force object
    """
    if not callable(radius):
        radius = constant(radius)
    else:
        radius = argpass(radius)
    if x is None:
        x = 0
    if y is None:
        y = 0

    return ForceRadial(radius, x, y)
