from datetime import datetime
from typing import TypeVar, TypeAlias, Protocol, Generic, Any
from collections.abc import Callable

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
TScaler = TypeVar("Itself", bound="Scaler")
TContinuousScaler = TypeVar("Itself", bound="ContinuousScaler")
TSequentialScaler = TypeVar("Itself", bound="SequentialScaler")
Number: TypeAlias = int | float
GenValue: TypeAlias = datetime | str | int | float

# Type definition for :code:`Formatter`: a function which takes a string to be
# formatted and returns the formatted value.
Formatter: TypeAlias = Callable[[str], T]

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

class Scaler(Protocol[U, V]):
    """
    Protocol class which represents Scaler class
    """

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

    def get_domain(self) -> list[U]:
        """
        Returns the domain values.

        Returns
        -------
        list[U]
            Domain values
        """
        ...

    def get_range(self) -> list[V]:
        """
        Returns the range values.

        Returns
        -------
        list[V]
            Range values
        """
        ...

    def set_domain(self, domain: list[U]) -> TScaler:
        """
        Sets the domain and returns the scaler updated.

        Parameters
        ----------
        domain : list[U]
            Domain values to set

        Returns
        -------
        Scaler
            Itself
        """
        ...

    def set_range(self, range_vals: list[V]) -> TScaler:
        """
        Sets the range and returns the scaler updated.

        Parameters
        ----------
        range_vals : list[V]
            Range values to set

        Returns
        -------
        Scaler
            Itself
        """
        ...

class ContinuousScaler(Scaler[U, V], Generic[U, V]):
    """
    Protocol class which represents Continuous Scaler class
    """
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

    def get_interpolate(self) -> Callable[[V], V]:
        """
        Gets the interpolator function.

        Returns
        -------
        Callable[[V], V]
            Interpolate function
        """
        ...

    def get_clamp(self) -> bool:
        """
        Returns if clamp is set on.

        Returns
        -------
        bool
            Clamp status
        """
        ...

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

    def set_interpolate(self, interpolate: Callable[[V], V]) -> TContinuousScaler:
        """
        Sets the interpolator function and returns the scaler updated.

        Parameters
        ----------
        interpolate : Callable[[V], V]
            Interpolate function

        Returns
        -------
        ContinuousScaler
            Itself
        """
        ...

    def set_clamp(self, clamp: bool) -> TContinuousScaler:
        """
        Sets the clamp status and returns the scaler updated.

        Parameters
        ----------
        clamp : bool
            Clamp status

        Returns
        -------
        ContinuousScaler
            Itself
        """
        ...

    def set_unknown(self, unknown: Any) -> TContinuousScaler:
        """
        Sets the unknown value when a :code:`math.nan` is encountered
        and returns the scaler updated.

        Parameters
        ----------
        unknown : Any
            Unknown value to set

        Returns
        -------
        ContinuousScaler
            Itself
        """
        ...

class SequentialScaler(Scaler[U, V], Generic[U, V]):
    """
    Protocol class which represents Sequential Scaler class
    """

    def set_interpolator(self, interpolator: Callable[[U], V]) -> TSequentialScaler:
        """
        Sets the interpolator function and returns the scaler updated.

        Parameters
        ----------
        interpolator : Callable[[U], V]
            Interpolator function

        Returns
        -------
        SequentialScaler
            Itself
        """
        ...
