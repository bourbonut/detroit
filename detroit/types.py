from datetime import datetime
from typing import TypeVar, TypeAlias, Protocol, Generic, Any
from collections.abc import Callable

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
TScaler = TypeVar("TScaler", bound="Scaler")
TSeqScaler = TypeVar("TSeqScaler", bound="SeqScaler")
Number: TypeAlias = int | float
GenValue: TypeAlias = datetime | str | int | float

# Type definition for :code:`Formatter`: a function which takes a string to be
# formatted and returns the formatted value.
Formatter: TypeAlias = Callable[[str], T]

class Scaler(Protocol[U, V]):

    def __call__(self, x: U) -> V:
        ...

    def get_domain(self) -> list[U]:
        ...

    def get_range(self) -> list[V]:
        ...

    def set_domain(self, domain: list[U]) -> TScaler:
        ...

    def set_range(self, range_vals: list[V]) -> TScaler:
        ...

class ContScaler(Scaler[U, V]):
    def invert(self, y: V) -> U:
        ...

    def get_interpolate(self) -> Callable[[V, V], V]:
        ...

    def get_clamp(self) -> bool:
        ...

    def get_unknown(self) -> Any:
        ...

    def set_interpolate(self, interpolate: Callable[[V, V], V]) -> TScaler:
        ...

    def set_clamp(self, clamp: bool) -> TScaler:
        ...

    def set_unknown(self, clamp: Any) -> TScaler:
        ...

class SeqScaler(Scaler[U, V]):

    def set_interpolator(self, interpolator: Callable[[U], V]) -> TSeqScaler:
        ...
