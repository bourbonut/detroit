from collections.abc import Callable
from typing import Any, TypeVar
from ..path import Path
from ..array import argpass
from .chord import ChordItem, ChordValue

from math import cos, sin, pi

HALF_PI = pi * 0.5
EPSILON = 1e-6

TRibbon = TypeVar("Ribbon", bound="Ribbon")


def constant(x: Any) -> Callable[..., Any]:
    def f(*args: Any) -> Any:
        return x

    return f


def default_source(d: ChordItem) -> float:
    return d.source


def default_target(d: ChordItem) -> float:
    return d.target


def default_radius(d: dict[str, float]) -> float:
    return d["radius"]


def default_start_angle(d: ChordValue) -> float:
    return d.start_angle


def default_end_angle(d: ChordValue) -> float:
    return d.end_angle


def default_pad_angle(d: ChordValue) -> float:
    return 0


def default_arrow_head_radius(d: ChordValue) -> float:
    return 10


class Ribbon:
    """
    Ribbon generator

    Parameters
    ----------
    head_radius : Callable[..., float] | None
        Arrow head radius accessor function
    """
    def __init__(self, head_radius: Callable[..., float] | None = None):
        self._head_radius = argpass(head_radius) if callable(head_radius) else None
        self._source = argpass(default_source)
        self._target = argpass(default_target)
        self._source_radius = argpass(default_radius)
        self._target_radius = argpass(default_radius)
        self._start_angle = argpass(default_start_angle)
        self._end_angle = argpass(default_end_angle)
        self._pad_angle = argpass(default_pad_angle)
        self._context = None

    def __call__(self, *args: Any) -> str | None:
        """
        Generates a ribbon for the given arguments. The arguments are
        arbitrary; they are propagated to the ribbon generator's accessor
        functions along with the this object.

        Parameters
        ----------
        *args : Any
            Additional arguments passed through ribbon generator's accessor
            methods

        Returns
        -------
        str | None
            Generated ribbon path
        """
        s = self._source(*args)
        t = self._target(*args)
        ap = self._pad_angle(*args) * 0.5
        argv = list(args).copy() if len(args) > 0 else [None]
        argv[0] = s
        sr = self._source_radius(*argv)
        sa0 = self._start_angle(*argv) - HALF_PI
        sa1 = self._end_angle(*argv) - HALF_PI
        argv[0] = t
        tr = self._target_radius(*argv)
        ta0 = self._start_angle(*argv) - HALF_PI
        ta1 = self._end_angle(*argv) - HALF_PI

        if self._context is None:
            self._context = buffer = Path()

        if ap > EPSILON:
            if abs(sa1 - sa0) > ap * 2 + EPSILON:
                if sa1 > sa0:
                    sa0 += ap
                    sa1 -= ap
                else:
                    sa0 -= ap
                    sa1 += ap
            else:
                sa0 = sa1 = (sa0 + sa1) / 2
            if abs(ta1 - ta0) > ap * 2 + EPSILON:
                if ta1 > ta0:
                    ta0 += ap
                    ta1 -= ap
                else:
                    ta0 -= ap
                    ta1 += ap
            else:
                ta0 = ta1 = (ta0 + ta1) / 2

        self._context.move_to(sr * cos(sa0), sr * sin(sa0))
        self._context.arc(0, 0, sr, sa0, sa1)
        if sa0 != ta0 or sa1 != ta1:
            if self._head_radius is None:
                self._context.quadratic_curve_to(0, 0, tr * cos(ta0), tr * sin(ta0))
                self._context.arc(0, 0, tr, ta0, ta1)
            else:
                hr = self.head_radius(*args)
                tr2 = tr - hr
                ta2 = (ta0 + ta1) / 2
                self._context.quadratic_curve_to(0, 0, tr2 * cos(ta0), tr2 * sin(ta0))
                self._context.line_to(tr * cos(ta2), tr * sin(ta2))
                self._context.line_to(tr2 * cos(ta1), tr2 * sin(ta1))
        self._context.quadratic_curve_to(0, 0, sr * cos(sa0), sr * sin(sa0))
        self._context.close_path()

        if buffer:
            self._context = None
            return str(buffer) or None

    def set_head_radius(self, head_radius: Callable[..., float] | float | None = None) -> TRibbon:
        """
        Sets the arrowhead radius accessor to the specified function and
        returns this ribbon generator.

        Parameters
        ----------
        head_radius : Callable[..., float] | float | None
            Arrow head radius accessor function

        Returns
        -------
        TRibbon
            Itself
        """
        if head_radius is None:
            self._head_radius = None
            return self
        if callable(head_radius):
            self._head_radius = head_radius
        else:
            self._head_radius = constant(head_radius)
        self._head_radius = argpass(self._head_radius)
        return self

    def set_radius(self, radius: Callable[..., float] | float) -> TRibbon:
        """
        Sets the source and target radius accessor to the specified function
        and returns this ribbon generator.

        Parameters
        ----------
        radius : Callable[..., float] | float
            Radius function or constant value

        Returns
        -------
        TRibbon
            Itself
        """
        if callable(radius):
            self._source_radius = radius
            self._target_radius = radius
        else:
            radius = constant(radius)
            self._source_radius = radius
            self._target_radius = radius
        self._source_radius = argpass(self._source_radius)
        self._target_radius = argpass(self._target_radius)
        return self

    def set_source_radius(self, source_radius: Callable[..., float] | float) -> TRibbon:
        """
        Sets the source radius accessor to the specified function and returns
        this ribbon generator.

        Parameters
        ----------
        source_radius : Callable[..., float] | float
            Source radius function

        Returns
        -------
        TRibbon
            Itself
        """
        if callable(source_radius):
            self._source_radius = source_radius
        else:
            self._source_radius = constant(source_radius)
        self._source_radius = argpass(self._source_radius)
        return self

    def set_target_radius(self, target_radius: Callable[..., float] | float) -> TRibbon:
        """
        Sets the target radius accessor to the specified function and returns
        this ribbon generator.

        Parameters
        ----------
        target_radius : Callable[..., float] | float
            Target radius function

        Returns
        -------
        TRibbon
            Itself
        """
        if callable(target_radius):
            self._target_radius = target_radius
        else:
            self._target_radius = constant(target_radius)
        self._target_radius = argpass(self._target_radius)
        return self

    def set_start_angle(self, start_angle: Callable[..., float] | float) -> TRibbon:
        """
        Sets the start angle accessor to the specified function and returns
        this ribbon generator.

        Parameters
        ----------
        start_angle : Callable[..., float] | float
            Start angle function or constant value

        Returns
        -------
        TRibbon
            Itself
        """
        if callable(start_angle):
            self._start_angle = start_angle
        else:
            self._start_angle = constant(start_angle)
        self._start_angle = argpass(self._start_angle)
        return self

    def set_end_angle(self, end_angle: Callable[..., float] | float) -> TRibbon:
        """
        Sets the end angle accessor to the specified function and returns
        this ribbon generator.

        Parameters
        ----------
        end_angle : Callable[..., float] | float
            End angle function or constant value

        Returns
        -------
        TRibbon
            Itself
        """
        if callable(end_angle):
            self._end_angle = end_angle
        else:
            self._end_angle = constant(end_angle)
        self._end_angle = argpass(self._end_angle)
        return self

    def set_pad_angle(self, pad_angle: Callable[..., float] | float) -> TRibbon:
        """
        Sets the pad angle accessor to the specified function and returns this
        ribbon generator

        Parameters
        ----------
        pad_angle : Callable[..., float] | float
            Pad angle function or constant value

        Returns
        -------
        TRibbon
            Itself
        """
        if callable(pad_angle):
            self._pad_angle = pad_angle
        else:
            self._pad_angle = constant(pad_angle)
        self._pad_angle = argpass(self._pad_angle)
        return self

    def set_source(self, source: Callable[..., float] | float) -> TRibbon:
        """
        Sets the source accessor to the specified function and returns this
        ribbon generator.

        Parameters
        ----------
        source : Callable[..., float] | float
            Source function or constant function

        Returns
        -------
        TRibbon
            Itself
        """
        self._source = argpass(source)
        return self

    def set_target(self, target: Callable[..., float] | float) -> TRibbon:
        """
        Sets the target accessor to the specified function and returns this
        ribbon generator.

        Parameters
        ----------
        target : Callable[..., float] | float
            Target function or constant function

        Returns
        -------
        TRibbon
            Itself
        """
        self._target = argpass(target)
        return self

    def set_context(self, context: Any | None = None) -> TRibbon:
        """
        If context is specified, sets the context and returns this ribbon
        generator. If the context is not :code:`None`, then the generated
        ribbon is rendered to this context as a sequence of path method calls.
        Otherwise, a path data string representing the generated ribbon is
        returned.

        Parameters
        ----------
        context : Any | None
            Context value

        Returns
        -------
        TRibbon
            Itself
        """
        self._context = context
        return self

    def get_head_radius(self) -> Callable[..., float]:
        return self._head_radius

    def get_radius(self) -> Callable[..., float]:
        return self._source_radius

    def get_source_radius(self) -> Callable[..., float]:
        return self._source_radius

    def get_target_radius(self) -> Callable[..., float]:
        return self._target_radius

    def get_start_angle(self) -> Callable[..., float]:
        return self._start_angle

    def get_end_angle(self) -> Callable[..., float]:
        return self._end_angle

    def get_pad_angle(self) -> Callable[..., float]:
        return self._pad_angle

    def get_source(self) -> Callable[..., float]:
        return self._source

    def get_target(self) -> Callable[..., float]:
        return self._target

    def get_context(self) -> Any | None:
        return self._context


def ribbon() -> Ribbon:
    """
    Creates a new ribbon generator with the default settings.

    Returns
    -------
    Ribbon
        Ribbon generator
    """
    return Ribbon(None)


def ribbon_arrow() -> Ribbon:
    """
    Creates a new arrow ribbon generator with the default settings.
    See also :func:`d3.chord_directed <detroit.chord_directed>`.

    Returns
    -------
    Ribbon
        Ribbon generator
    """
    return Ribbon(default_arrow_head_radius)
