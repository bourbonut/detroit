from collections.abc import Callable
from typing import TypeVar

from ..path import Path
from .constant import constant
from .path import WithPath
from .symbols import (
    symbol_asterisk,
    symbol_circle,
    symbol_cross,
    symbol_diamond,
    symbol_diamond2,
    symbol_plus,
    symbol_square,
    symbol_square2,
    symbol_star,
    symbol_times,
    symbol_triangle,
    symbol_triangle2,
    symbol_wye,
)

# Symbols which are designed to be filled
SYMBOLS_FILL = [
    symbol_circle,
    symbol_cross,
    symbol_diamond,
    symbol_square,
    symbol_star,
    symbol_triangle,
    symbol_wye,
]

# Symbols which are designed to be stroked (with a width of 1.5px and round caps).
SYMBOLS_STROKE = [
    symbol_asterisk,
    symbol_circle,
    symbol_diamond2,
    symbol_plus,
    symbol_square2,
    symbol_times,
    symbol_triangle2,
]

TSymbol = TypeVar("Symbol", bound="Symbol")


class Symbol(WithPath):
    """
    Builds a new symbol generator of the specified symbol type and size.

    Parameters
    ----------
    symbol_type : Callable[[Path, int | float], None] | None
        Symbol type - default :code:`symbol_circle`
    size : Callable[[], int | float] | int | float | None
        Size - Default :code:`64`
    """

    def __init__(
        self,
        symbol_type: Callable[[Path, int | float], None] | None = None,
        size: Callable[[], int | float] | int | float | None = None,
    ):
        super().__init__()
        self._context = None
        self._symbol_type = symbol_type or symbol_circle
        self._size = size if callable(size) else constant(size or 64)

    def __call__(self) -> str | None:
        """
        Generates a symbol. With the default settings,
        invoking the symbol generator produces a circle
        of 64 square pixels.

        Returns
        -------
        str | None
            Symbol path
        """
        if self._context is None:
            buffer = self._path()
            self._context = buffer

        self._symbol_type(self._context, self._size())

        if buffer:
            self._context = None
            return str(buffer)

    def set_symbol_type(
        self, symbol_type: Callable[[Path, int | float], None]
    ) -> TSymbol:
        """
        Sets the symbol type and returns this symbol generator.

        Parameters
        ----------
        symbol_type : Callable[[Path, int | float], None]
            Symbol type

        Returns
        -------
        Symbol
            Itself
        """
        self._symbol_type = symbol_type
        return self

    @property
    def symbol_type(self):
        return self._symbol_type

    def set_size(self, size: Callable[[], int | float] | int | float) -> TSymbol:
        """
        Sets the size of the symbol and returns this symbol generator.

        Parameters
        ----------
        size : Callable[[], int | float] | int | float
            Size function or constant

        Returns
        -------
        Symbol
            Itself
        """
        self._size = size if callable(size) else constant(size)
        return self

    @property
    def size(self):
        return self._size

    def set_context(self, context: Path) -> TSymbol:
        """
        Sets the context and returns this symbol generator.

        Parameters
        ----------
        context : Path
            Context

        Returns
        -------
        Symbol
            Itself
        """
        self._context = context
        return self
