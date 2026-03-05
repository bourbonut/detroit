from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any, Protocol, SupportsFloat, TypeAlias, TypedDict, TypeVar

from lxml import etree  # type: ignore

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
Number: TypeAlias = int | float
GenValue: TypeAlias = datetime | str | int | float
IntoFloat: TypeAlias = datetime | SupportsFloat
Point2D: TypeAlias = tuple[float, float]
Point3D: TypeAlias = tuple[float, float, float]
Vec2D: TypeAlias = tuple[float, float]
Vec3D: TypeAlias = tuple[float, float, float]
GeoJSON: TypeAlias = dict[str, Any]

# Type definition for :code:`Formatter`: a function which takes a string to be
# formatted and returns the formatted value.
Formatter: TypeAlias = Callable[[str], T]

EtreeFunction: TypeAlias = Callable[[etree.Element, U, int, list[etree.Element]], V]


class Interval(Protocol):
    """
    Protocol class which represents Interval class
    """

    @staticmethod
    def floor(x: float) -> float:
        """
        Apply floor procedure on x value

        Parameters
        ----------
        x : float
            Input

        Returns
        -------
        float
            Output
        """
        ...

    @staticmethod
    def ceil(x: float) -> float:
        """
        Apply ceil procedure on x value

        Parameters
        ----------
        x : float
            Input

        Returns
        -------
        float
            Output
        """
        ...


Accessor = (
    Callable[[U], V]
    | Callable[[U, int], V]
    | Callable[[U, int, list[etree.Element]], V]
)

# class Accessor(Protocol[U, V]):
#     """
#     Protocol which describes how an accessor is defined.
#
#     Accessors are found in differents modules of :code:`detroit` when a
#     function iterates over an array of values and only specific values must be
#     processed.
#
#     Therefore, an accessor behaves like a function. However, the signature of
#     the function can be flexible. The function can take one, two or three
#     arguments.
#
#     The first argument represents a value of the iterated array.
#     The second argument represents the index of the node.
#     The last and third argument is the group of nodes where :code:`node ==
#     group[i]`.
#
#     Examples
#     --------
#
#     The following functions are valid "accessors":
#
#     >>> lambda d: d["weights"]
#     >>> lambda d, i: i * d["length"]
#     >>> lambda d, _, group: len(group) + d["count"]
#     """
#
#     @overload
#     def __call__(self, d: U) -> V: ...
#
#     @overload
#     def __call__(self, d: U, i: int) -> V: ...
#
#     @overload
#     def __call__(self, d: U, i: int, group: list[etree.Element]) -> V: ...
#
#     def __call__(self, *args) -> V:
#         """
#         Given at least one argument, returns a processed value.
#
#         Parameters
#         ----------
#         d : U
#             Represents a value of :code:`data` such as :code:`d = data[i]`.
#         i : int
#             Index of the node (i.e. :code:`node == group[i]`)
#         group : list[etree.Element]
#             Group of selected nodes
#
#         Returns
#         -------
#         V
#             A desired value
#         """
#         ...


class MultiPolygonGeoJSON(TypedDict):
    """
    Describes a contour as GeoJSON MultiPolygon geometry objects

    Attributes
    ----------
    type : str
        Type of contour (ex: :code:`"MultiPolygon"`)
    value : str
        Threshold value; the input values are greater than or equal to this
        value.
    coordinates : list[list[tuple[int, int]]]
        Coordinates of contours
    """

    type: str
    value: float
    coordinates: list[list[Point2D]]


class SimulationNode(TypedDict):
    """
    Describes a simulation's node.

    Attributes
    ----------
    index : int
        The node's zero-based index into nodes
    x : float
        The node's current x-position
    y : float
        The node's current y-position
    vx : float
        The node's current x-velocity
    vy : float
        The node's current y-velocity
    fx : float
        The node's fixed x-position
    fy : float
        The node's fixed y-position
    """

    index: int
    x: float
    y: float
    vx: float
    vy: float
    fx: float
    fy: float


class SimulationLink(TypedDict):
    """
    Describes a simulation's link.

    Attributes
    ----------
    source : SimulationNode
        The link's source node
    target : SimulationNode
        The link's target node
    index : int
        The zero-based index into links
    """

    source: dict
    target: dict
    index: int


SimulationNodeFunction: TypeAlias = Callable[
    [SimulationNode, int, list[SimulationNode]], T
]
SimulationLinkFunction: TypeAlias = Callable[
    [SimulationLink, int, list[SimulationLink]], T
]


class Force(Protocol):
    """
    Protocol class which represents Force object
    """

    def initialize(
        self,
        nodes: list[SimulationNode],
        random: Callable[[None], float],
    ):
        """
        Initializes the force.

        Parameters
        ----------
        nodes : list[SimulationNode]
            List of simulation nodes
        random : Callable[[None], float]
            Function which returns a random number
        """
        ...

    def __call__(self, alpha: float | None):
        """
        Applies the force on simulation nodes.

        Parameters
        ----------
        alpha : float | None
            Parameter used during the call.
        """
        ...
