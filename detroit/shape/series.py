from typing import Generic
from ..types import U, V

class Serie(Generic[U, V]):
    
    def __init__(self, values: list[U], data: V):
        self._values = values
        self.data = data

    def __getitem__(self, index: int) -> U:
        return self._values[index]

    def __setitem__(self, index: int, value: U):
        self._values[index] = value

class Series:

    def __init__(self):
        self._series: list[Serie] = []
        self.key = None
        self.index = None

    def __getitem__(self, index: int):
        return self._series[index]

    def __setitem__(self, index: int, serie: Serie):
        self._series[index] = serie

    def append(self, serie: Serie):
        self._series.append(serie)

