from __future__ import annotations
from typing import Any, NewType, Optional, Union, Tuple
from markupsafe import Markup

try:
    import polars as pl
    POLARS_INSTALLED = True
except:
    POLARS_INSTALLED = False
try:
    import pandas as pd
    PANDAS_INSTALLED = True
except:
    PANDAS_INSTALLED = False

DataFrameLike = NewType("DataFrameLike", Any)

class js:
    """
    Useful class to remove quotes when string is represented

    Parameters
    ----------
    string: str
        string to display

    Examples
    --------
    >>> print(["(x) => x / 1000"])
    ["(x) => x / 1000"]
    >>> print([js("(x) => x / 1000")])
    [(x) => x / 1000]
    """
    def __init__(self, string: str):
        self.string = string

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string


class Data:
    """
    Useful recursive class to simplify syntax when writing Javascript codelike

    Parameters
    ----------
    data: dict
        data values
    method: Optional[str]
        current method name
    header: str
        prefix string used as memory string (it should not be changed)

    Examples
    --------
    >>> values = {
    ...     "allzeta": [1],
    ...     "alldata": [
    ...         {
    ...             "key": 1,
    ...             "values": [{"x": 1, "y": 2}],
    ...         }
    ...     ]
    ... }
    >>> data = Data(values)
    >>> print(data.alldata[0].key)
    data.alldata[0].key
    >>> print(data.alldata[0].values.data)
    [{"x": 1, "y": 2}]

    Notes
    -----
    Use the function :code:`arrange` to convert input values into exploitable structure.
    """
    def __init__(self, data: dict, method:Optional[str]=None, header:str="data"):
        self.method = method
        self.header = header
        self.data = data
        if isinstance(data, dict):
            for method, datum in data.items():
                setattr(self, method, Data(datum, method, header))

    def __str__(self):
        if self.method is None:
            return str(js(f"{self.header}"))
        return str(js(f"{self.header}.{self.method}"))

    def __repr__(self):
        return str(js(str(self)))

    def __getitem__(self, item):
        index = 0 if isinstance(item, str) else item
        return Data(self.data[index], method=None, header=f"{self.header}.{self.method}[{item}]")

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __contains__(self, item):
        return item in self.data

    @staticmethod
    def arrange(obj: Union[dict, DataFrameLike, Data, Tuple[list, list], Tuple[list, list, list]]) -> Data:
        """
        Return a :code:`Data` where input is transformed into an exploitable dictionary for the class :code:`Data`

        Parameters
        ----------
        obj : Union[dict, DataFrameLike, Data, Tuple[list, list], Tuple[list, list, list]]
            Input data 

        Returns
        -------
        Data
           :code:`Data` from :code:`obj`
        """
        return Data(arrange(obj))

DataInput = Union[dict, DataFrameLike, Data, Tuple[list, list], Tuple[list, list, list]]

def arrange(obj: DataInput) -> dict:
    """
    Convert input data into an exploitable data structure for future operations

    Parameters
    ----------
    obj : DataInput
       Input data 

    Returns
    -------
    dict
       dictionary containing input data 

    Examples
    --------

    Using `polars`:

    >>> import polars as pl
    >>> df = pl.DataFrame(
    ...     {
    ...         "A": [1, 2, 3, 4, 5],
    ...         "fruits": ["banana", "banana", "apple", "apple", "banana"],
    ...         "B": [5, 4, 3, 2, 1],
    ...         "cars": ["beetle", "audi", "beetle", "beetle", "beetle"],
    ...     }
    ... )
    >>> arrange(df)
    [{'A': 1, 'fruits': 'banana', 'B': 5, 'cars': 'beetle'}, {'A': 2, 'fruits': 'banana', 'B': 4, 'cars': 'audi'}, {'A': 3, 'fruits': 'apple', 'B': 3, 'cars': 'beetle'}, {'A': 4, 'fruits': 'apple', 'B': 2, 'cars': 'beetle'}, {'A': 5, 'fruits': 'banana', 'B': 1, 'cars': 'beetle'}]

    Using `pandas`:

    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         "A": [1, 2, 3, 4, 5],
    ...         "fruits": ["banana", "banana", "apple", "apple", "banana"],
    ...         "B": [5, 4, 3, 2, 1],
    ...         "cars": ["beetle", "audi", "beetle", "beetle", "beetle"],
    ...     }
    ... )
    >>> arrange(df)
    [{'A': 1, 'fruits': 'banana', 'B': 5, 'cars': 'beetle'}, {'A': 2, 'fruits': 'banana', 'B': 4, 'cars': 'audi'}, {'A': 3, 'fruits': 'apple', 'B': 3, 'cars': 'beetle'}, {'A': 4, 'fruits': 'apple', 'B': 2, 'cars': 'beetle'}, {'A': 5, 'fruits': 'banana', 'B': 1, 'cars': 'beetle'}]

    Other usages :

    >>> arrange([[1, 2, 3], [4, 5, 6]])
    [{"x": 1, "y": 4}, {"x": 2, "y": 5}, {"x": 3, "y": 6}]
    >>> arrange([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    [{"x": 1, "y": 4, "z": 7}, {"x": 2, "y": 5, "z": 8}, {"x": 3, "y": 6, "z": 9}]
    """
    if POLARS_INSTALLED and isinstance(obj, pl.DataFrame):
        return obj.to_dicts()
    elif PANDAS_INSTALLED and isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient="records")
    elif isinstance(obj, Data):
        return obj.data
    elif isinstance(obj, list):
        if len(obj) == 1:
            obj = obj[0]
            if isinstance(obj, list):
                return [{"x": i, "y": item} for i, item in enumerate(obj)]
        elif len(obj) == 2:
            x, y = obj
            if isinstance(x, list) and isinstance(y, list):
                assert len(x) == len(y), "All inputs must have the same length."
                return [{"x": xi, "y": yi} for xi, yi in zip(x, y)]
            else:
                raise TypeError(f"Only Tuple[list, list] type supported.")
        elif len(obj) == 3:
            x, y, z = obj
            if all(map(lambda e: isinstance(e, list), (x, y, z))):
                assert len(x) == len(y) == len(z), "All inputs must have the same length."
                return [{"x": xi, "y": yi, "z": zi} for xi, yi, zi in zip(x, y, z)]
            else:
                raise TypeError(f"Only Tuple[list, list, list] type supported.")
    return obj
