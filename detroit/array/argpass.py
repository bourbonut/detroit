from collections.abc import Callable
from inspect import signature
from operator import itemgetter
from typing import Any


class argpass:
    """
    Determines the number of arguments needed by the given function and returns
    a wrapper function which selects the correct number of arguments.

    Parameters
    ----------
    func : Callable[[list[Any]], Any]
        Function to decorate
    """

    def __init__(self, func: Callable[[list[Any]], Any]):
        self._func = func
        self._nargs = (
            1 if isinstance(func, itemgetter) else len(signature(func).parameters)
        )

    def __call__(self, *args: Any) -> Any:
        """
        Calls the function with the correct number of arguments

        Parameters
        ----------
        *args : Any
            Arbitrary arguments

        Returns
        -------
        Any
            Result of the function call
        """
        return self._func(*args[: self._nargs])

    def __eq__(self, other: Any) -> bool:
        """
        Returns :code:`True` if the inner function equals :code:`other`.

        Parameters
        ----------
        other : Any
            Input object

        Returns
        -------
        bool
            :code:`True` if the inner function equals :code:`other`
        """
        if isinstance(other, argpass):
            return self._func == other._func
        elif callable(other):
            return self._func == other
        else:
            return False
