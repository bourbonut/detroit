from collections.abc import Callable
from operator import itemgetter
from typing import Any, Generic, TypeVar

from ..array import argpass
from ..selection import Selection
from ..types import Accessor, Number, T
from .constant import constant
from .curves import Curve, curve_bump_radial, curve_bump_x, curve_bump_y
from .path import WithPath
from .point import x as point_x
from .point import y as point_y

TLink = TypeVar("Link", bound="Link")

link_source = itemgetter("source")
link_target = itemgetter("target")


class Link(Generic[T], WithPath):
    """
    The link shape generates a smooth cubic Bézier curve from a source point to
    a target point. The tangents of the curve at the start and end are either
    vertical or horizontal.

    Parameters
    ----------
    curve : Callable[[Selection], Curve]
        Curve factory function

    Returns
    -------
    Link
        New link generator
    """

    def __init__(self, curve: Callable[[Selection], Curve]):
        super().__init__()
        self._source = argpass(link_source)
        self._target = argpass(link_target)
        self._x = argpass(point_x)
        self._y = argpass(point_y)
        self._context = None
        self._output = None
        self._curve = curve

    def __call__(self, *args: Any) -> str | None:
        """

        Parameters
        ----------
        args : Any
            Extra arguments passed through :code:`source` function,
            :code:`target` function, :code:`x` function and :code:`y` function.

        Returns
        -------
        str | None
            Generated link if the link is not associated to a context
        """
        buffer = None
        args = list(args)
        s = self._source(*args)
        t = self._target(*args)
        if self._context is None:
            buffer = self._path()
            self._output = self._curve(buffer)
        self._output.line_start()
        args[0] = s
        x = self._x(*args)
        y = self._y(*args)
        self._output.point(x, y)
        args[0] = t
        x = self._x(*args)
        y = self._y(*args)
        self._output.point(x, y)
        self._output.line_end()
        if buffer:
            self._output = None
            return str(buffer) or None

    def set_source(self, source: Accessor[T, float]) -> TLink:
        """
        Sets the source function

        Parameters
        ----------
        source : Accessor[T, float]
            Source accessor function

        Returns
        -------
        TLink
            Itself
        """
        self._source = argpass(source)
        return self

    def set_target(self, target: Accessor[T, float]) -> TLink:
        """
        Sets the target function

        Parameters
        ----------
        target : Accessor[T, float]
            Target accessor function

        Returns
        -------
        TLink
            Itself
        """
        self._target = argpass(target)
        return self

    def x(self, x: Accessor[T, float] | Number) -> TLink:
        """
        Sets x accessor function

        Parameters
        ----------
        x : Accessor[T, float] | Number
            x accessor function

        Returns
        -------
        Link
            Itself
        """
        if callable(x):
            self._x = x
        else:
            self._x = constant(x)
        self._x = argpass(self._x)
        return self

    def y(self, y: Accessor[T, float] | Number) -> TLink:
        """
        Sets y accessor function

        Parameters
        ----------
        y : Accessor[T, float] | Number
            y accessor function

        Returns
        -------
        Link
            Itself
        """
        if callable(y):
            self._y = y
        else:
            self._y = constant(y)
        self._y = argpass(self._y)
        return self

    def set_context(self, context: Selection | None = None) -> TLink:
        """
        Sets the context.

        Parameters
        ----------
        context : Selection | None
            Selection

        Returns
        -------
        Link
            Itself
        """
        if context is None:
            self._context = None
            self._output = None
        else:
            self._context = context
            self._output = self._curve(self._context)
        return self

    def get_source(self) -> Accessor[T, float]:
        return self._source

    def get_target(self) -> Accessor[T, float]:
        return self._target

    def get_x(self) -> Accessor[T, float]:
        return self._x

    def get_y(self) -> Accessor[T, float]:
        return self._y

    def get_context(self) -> Selection:
        return self._context


def link_horizontal() -> Link:
    """
    Shorthand for link with :func:`d3.curve_bump_x <curve_bump_x>`; suitable
    for visualizing links in a tree diagram rooted on the left edge of the
    display.

    Returns
    -------
    Link
        Horizontal link generator
    """
    return Link(curve_bump_x)


def link_vertical() -> Link:
    """
    Shorthand for link :func:`d3.curve_bump_y <curve_bump_y>`; suitable for
    visualizing links in a tree diagram rooted on the top edge of the display.

    Returns
    -------
    Link
        Vertical link generator
    """
    return Link(curve_bump_y)


def link_radial() -> Link:
    """
    Returns a new link generator with radial tangents.

    Returns
    -------
    Link
        Radial link generator
    """
    link = Link(curve_bump_radial)
    link.angle = link.x
    link.radius = link.y
    link.get_angle = link.get_x
    link.get_radius = link.get_y
    return link
