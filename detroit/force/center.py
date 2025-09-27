from collections.abc import Callable
from typing import TypeVar
from ..types import SimulationNode

TForceCenter = TypeVar("ForceCenter", bound="ForceCenter")

class ForceCenter:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y
        self._strength = 1
        self._nodes = None

    def __call__(self, alpha: float | None = None):
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

    def initialize(self, nodes: list[SimulationNode], random: Callable[[None], float]):
        self._nodes = nodes

    def x(self, x: float) -> TForceCenter:
        """
        Sets the x-coordinate of the centering position to the specified number
        and returns this force.

        Parameters
        ----------
        x : float
            X-coordinate of the centering position

        Returns
        -------
        ForceCenter
            Itself
        """
        self._x = x
        return self

    def y(self, y: float) -> TForceCenter:
        """
        Sets the y-coordinate of the centering position to the specified number
        and returns this force.

        Parameters
        ----------
        y : float
            Y-coordinate of the centering position

        Returns
        -------
        ForceCenter
            Itself
        """
        self._y = y
        return self

    def set_strength(self, strength: float) -> TForceCenter:
        """
        Sets the center force's strength. A reduced strength of e.g. 0.05
        softens the movements on interactive graphs in which new nodes enter or
        exit the graph.

        Parameters
        ----------
        strength : float
            Strength value

        Returns
        -------
        ForceCenter
            Itself
        """
        self._strength = strength
        return self

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_strength(self) -> float:
        return self._strength

def force_center(x: float | None = None, y: float | None = None) -> ForceCenter:
    """
    The center force translates nodes uniformly so that the mean position of
    all nodes (the center of mass if all nodes have equal weight) is at the
    given position :math:`(x,y)`. This force modifies the positions of nodes on
    each application; it does not modify velocities, as doing so would
    typically cause the nodes to overshoot and oscillate around the desired
    center. This force helps keep nodes in the center of the viewport, and
    unlike the position forces, it does not distort their relative positions.

    Parameters
    ----------
    x : float | None
        X-coordinate of the centering position
    y : float | None
        Y-coordinate of the centering position

    Returns
    -------
    ForceCenter
        Force object
    """
    if x is None:
        x = 0
    if y is None:
        y = 0
    return ForceCenter(x, y)
