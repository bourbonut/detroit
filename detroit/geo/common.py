from abc import ABC, abstractmethod
from typing import Protocol, TypeAlias
from ..types import Point2D

class SpatialTransform(Protocol):
    """
    Describes a spatial transformation
    """
    def __call__(self, x: float, y: float) -> Point2D:
        """
        Transforms the x and y values into two new values.

        Parameters
        ----------
        x : float
            x value
        y : float
            y value

        Returns
        -------
        Point2D
            New values
        """
        ...

    def invert(self, x: float, y: float) -> Point2D:
        """
        Optional method which makes the invert transformation.

        Parameters
        ----------
        x : float
            x value
        y : float
            y value

        Returns
        -------
        Point2D
            Inverted values
        """
        ...

class Projection(Protocol):
    """
    Raw projections are point transformation functions that are used to
    implement custom projections; they typically passed to geoProjection or
    geoProjectionMutator. They are exposed here to facilitate the derivation of
    related projections. Raw projections take spherical coordinates
    :code:`[lambda, phi]` in radians (not degrees!) and return a point
    :code:`[x, y]`, typically in the unit square centered around the origin.
    """
    def __call__(self, lambda_: float, phi: float) -> Point2D:
        """
        Projects the specified point :code:`[lambda, phi]` in radians,
        returning a new point :code:`[x, y]` in unitless coordinates.

        Parameters
        ----------
        lambda_ : float
            :math:`\\lambda` value
        phi : float
            :math:`\\phi` value

        Returns
        -------
        Point2D
            New point
        """
        ...

    def invert(self, x: float, y: float) -> Point2D:
        """
        Optional method: the inverse of the projection.

        Parameters
        ----------
        x : float
            x value
        y : float
            y value

        Returns
        -------
        Point2D
            :code:`[lambda, phi]` coordinates in radians
        """
        ...

class LineStream(ABC):

    @abstractmethod
    def line_start(self):
        """
        Indicates the start of a new line segment. Zero or more points will
        follow.
        """
        ...

    @abstractmethod
    def line_end(self):
        """
        Indicates the end of the current line segment.
        """
        ...

    @abstractmethod
    def point(self, x: float, y: float):
        """
        Indicates a new point in the current line segment with the given x- and
        y-values.

        Parameters
        ----------
        x : float
            x value
        y : float
            y value
        """
        ...

class PolygonStream(LineStream):
    
    @abstractmethod
    def polygon_start(self):
        """
        Indicates the start of a new polygon.
        """
        ...

    @abstractmethod
    def polygon_end(self):
        """
        Indicates the end of the current polygon.
        """
        ...

Stream: TypeAlias = LineStream | PolygonStream
