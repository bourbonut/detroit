from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Generic

from ..types import U, V


class Scaler(Generic[U, V], ABC):
    """
    Protocol class which represents Scaler class
    """

    @abstractmethod
    def __call__(self, x: U) -> V:
        """
        Scales a value.

        Parameters
        ----------
        x : U
            Value to transform

        Returns
        -------
        V
            Scaled value
        """
        ...

    @abstractmethod
    def get_domain(self) -> list[U]:
        """
        Returns the domain values.

        Returns
        -------
        list[U]
            Domain values
        """
        ...

    @abstractmethod
    def get_range(self) -> list[V]:
        """
        Returns the range values.

        Returns
        -------
        list[V]
            Range values
        """
        ...

    @abstractmethod
    def set_domain(self, domain: list[U]) -> Scaler[U, V]:
        """
        Sets the domain and returns the scaler updated.

        Parameters
        ----------
        domain : list[U]
            Domain values to set

        Returns
        -------
        Scaler[U, V]
            Itself
        """
        ...

    @abstractmethod
    def set_range(self, range_vals: list[V]) -> Scaler[U, V]:
        """
        Sets the range and returns the scaler updated.

        Parameters
        ----------
        range_vals : list[V]
            Range values to set

        Returns
        -------
        Scaler[U, V]
            Itself
        """
        ...


class ContinuousScaler(Scaler[U, V]):
    """
    Protocol class which represents Continuous Scaler class
    """

    @abstractmethod
    def invert(self, y: V) -> U:
        """
        Makes the opposite operation of :code:`__call__`.

        Parameters
        ----------
        y : V
            Scaled value

        Returns
        -------
        U
            Original value
        """
        ...

    @abstractmethod
    def get_interpolate(self) -> Callable[[V, V], Callable[[float], V]]:
        """
        Gets the interpolator function.

        Returns
        -------
        Callable[[V, V], Callable[[float], V]]
            Interpolate function
        """
        ...

    @abstractmethod
    def get_clamp(self) -> bool:
        """
        Returns if clamp is set on.

        Returns
        -------
        bool
            Clamp status
        """
        ...

    @abstractmethod
    def get_unknown(self) -> Any:
        """
        Returns the default value when :code:`__call__` takes a
        :code:`math.nan`.

        Returns
        -------
        Any
            Unknown value
        """
        ...

    @abstractmethod
    def set_interpolate(
        self, interpolate: Callable[[V, V], Callable[[float], V]]
    ) -> ContinuousScaler[U, V]:
        """
        Sets the interpolator function and returns the scaler updated.

        Parameters
        ----------
        interpolate : Callable[[V, V], Callable[[float], V]]
            Interpolate function

        Returns
        -------
        ContinuousScaler[U, V]
            Itself
        """
        ...

    @abstractmethod
    def set_clamp(self, clamp: bool) -> ContinuousScaler[U, V]:
        """
        Sets the clamp status and returns the scaler updated.

        Parameters
        ----------
        clamp : bool
            Clamp status

        Returns
        -------
        ContinuousScaler[U, V]
            Itself
        """
        ...

    @abstractmethod
    def set_unknown(self, unknown: Any) -> ContinuousScaler[U, V]:
        """
        Sets the unknown value when a :code:`math.nan` is encountered
        and returns the scaler updated.

        Parameters
        ----------
        unknown : Any
            Unknown value to set

        Returns
        -------
        ContinuousScaler[U, V]
            Itself
        """
        ...


class SequentialScaler(Scaler[U, V]):
    """
    Protocol class which represents Sequential Scaler class
    """

    @abstractmethod
    def set_interpolator(
        self, interpolator: Callable[[U], V]
    ) -> SequentialScaler[U, V]:
        """
        Sets the interpolator function and returns the scaler updated.

        Parameters
        ----------
        interpolator : Callable[[U], V]
            Interpolator function

        Returns
        -------
        SequentialScaler[U, V]
            Itself
        """
        ...
