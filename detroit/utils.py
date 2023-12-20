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

class js:
    """
    Useful class to remove quotes when string is represented

    Example

    print([js("(x) => x / 1000")]) # [(x) => x / 1000]
    # instead of ["(x) => x / 1000"]
    """
    def __init__(self, string: str):
        self.string = string

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string


def wrap_method_data(self, method, datum, header):
    """
    Decorator used to generate a method to the `Data` class
    automatically given the class and a name of the method
    """
    def wrapper():
        return Data(datum, method, header)
    return wrapper()

class Data:

    def __init__(self, data, method=None, header="data"):
        self.method = method
        self.header = header
        self.data = data
        if isinstance(data, dict):
            for method, datum in data.items():
                setattr(self, method, wrap_method_data(self, method, datum, header))

    def __str__(self):
        if self.method is None:
            return str(js(f"{self.header}"))
        return str(js(f"{self.header}.{self.method}"))

    def __repr__(self):
        return str(js(str(self)))

    def __getitem__(self, item):
        index = 0 if isinstance(item, str) else item
        return Data(self.data[index], method=None, header=f"{self.header}.{self.method}[{item}]")

    def __add__(self, item):
        return f"{self} + {item}"

    def __sub__(self, item):
        return f"{self} - {item}"

    def __mul__(self, item):
        return f"{self} * {item}"

    def __div__(self, item):
        return f"{self} / {item}"


def arrange(obj):
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
