from collections.abc import Iterator
from typing import Any, Generic, TypeVar

from ..types import T

TSerie = TypeVar("Serie", bound="Serie")
TSeries = TypeVar("Series", bound="Series")


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
        """
        Returns the value of a specific index

        Parameters
        ----------
        index : int
            Index value

        Returns
        -------
        float
            Value
        """
        return self._values[index]

    def __setitem__(self, index: int, value: float):
        """
        Sets the value at a specific index

        Parameters
        ----------
        index : int
            Index value
        value : float
            Value
        """
        self._values[index] = value

    def __len__(self) -> int:
        """
        Returns the length of the serie

        Returns
        -------
        int
            Length of serie
        """
        return len(self._values)

    def __eq__(self, serie: TSerie | Any) -> bool:
        """
        Checks if another series value is the same as the current values.

        Parameters
        ----------
        serie : Serie[T] | Any
            Other serie

        Returns
        -------
        bool
            True if two series are the same
        """
        if not isinstance(serie, Serie):
            return False
        return self._values == serie._values and self.data == serie.data

    def __str__(self) -> str:
        """
        Formats the class to a string.

        Returns
        -------
        str
           String representing the current class
        """
        return f"Serie({self._values}, data={self.data})"

    def __repr__(self):
        return str(self)


class Series(Generic[T]):
    """
    List of :code:`Serie` associated to a :code:`key` and an :code:`index`

    Parameters
    ----------
    series: list[Serie[T]] | None
        List of series
    """

    def __init__(self, series: list[Serie[T]] | None = None):
        self._series = series or []
        self.key = None
        self.index = None

    def __getitem__(self, index: int) -> Serie[T]:
        """
        Gets a serie given an index

        Parameters
        ----------
        index : int
            Index value

        Returns
        -------
        Serie[T]
            Serie value
        """
        return self._series[index]

    def __setitem__(self, index: int, serie: Serie[T]):
        """
        Sets a serie at a specific index

        Parameters
        ----------
        index : int
            Index value
        serie : Serie[T]
            Serie value
        """
        self._series[index] = serie

    def __len__(self) -> int:
        """
        Returns the length of the serie

        Returns
        -------
        int
            Length
        """
        return len(self._series)

    def __eq__(self, series: TSeries | Any) -> bool:
        """
        Checks if another series value is the same as the current values.

        Parameters
        ----------
        series : Series[T] | Any
            Other series

        Returns
        -------
        bool
            True if two series are the same
        """
        if not isinstance(series, Series):
            return False
        return (
            self._series == series._series
            and self.key == series.key
            and self.index == series.index
        )

    def __iter__(self) -> Iterator[Serie[T]]:
        """
        Returns an iterator of :code:`Serie`.

        Returns
        -------
        Iterator[Serie[T]]
            Iterator
        """
        return iter(self._series)

    def append(self, serie: Serie[T]):
        """
        Appends a serie to the current list of series.

        Parameters
        ----------
        serie : Serie[T]
            Serie value
        """
        self._series.append(serie)

    def __str__(self) -> str:
        """
        Formats the class to a string.

        Returns
        -------
        str
           String representing the current class
        """
        return f"Series({self._series}, key={self.key}, index={self.index})"

    def __repr__(self):
        return str(self)
