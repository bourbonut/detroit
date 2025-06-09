from typing import Generic
from collections.abc import Iterator
from ..types import T

class Serie(Generic[T]):
    """
    Point of a :code:`Series`

    Parameters
    ----------
    values : list[float]
        Point coordinates
    data : T
        Data value associated to this point
    """
    def __init__(self, values: list[float], data: T):
        self._values = values
        self.data = data

    def __getitem__(self, index: int) -> float:
        return self._values[index]

    def __setitem__(self, index: int, value: float):
        self._values[index] = value

    def __len__(self) -> int:
        return len(self._values)

    def __eq__(self, serie):
        if not isinstance(serie, Serie):
            return False
        return self._values == serie._values and self.data == serie.data

    def __str__(self):
        return f"Serie({self._values}, data={self.data})"

    def __repr__(self):
        return str(self)

class Series:
    """
    List of :code:`Serie` associated to a :code:`key` and an :code:`index`
    """
    def __init__(self, series: list[Serie] | None = None):
        self._series = series or []
        self.key = None
        self.index = None

    def __getitem__(self, index: int):
        return self._series[index]

    def __setitem__(self, index: int, serie: Serie):
        self._series[index] = serie

    def __len__(self) -> int:
        return len(self._series)

    def __eq__(self, series):
        if not isinstance(series, Series):
            return False
        return (
            self._series == series._series and
            self.key == series.key and
            self.index == series.index
        )

    def __iter__(self) -> Iterator[Serie]:
        return iter(self._series)

    def append(self, serie: Serie):
        self._series.append(serie)

    def __str__(self):
        return f"Series({self._series}, key={self.key}, index={self.index})"

    def __repr__(self):
        return str(self)
