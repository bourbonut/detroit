from __future__ import annotations

from typing import Iterator

from .utils import js
from .d3 import d3

class Script:
    """
    Class which stores javascript lines of code useful to render
    or save a visualization with :code:`d3` syntax

    Examples
    --------

    >>> from detroit import Script, svg, d3
    >>> script = Script()
    >>> script("svg", d3.select(script.plot_id))
    svg
    >>> script(svg.append("g"))
    >>> print(script)
    var svg = d3.select('#myplot')
    svg.append('g')
    """

    def __init__(self):
        self.code = []
        self.id = "myplot"

    def __call__(self, *args):
        if len(args) > 2:
            raise ValueError("Too many arguments (len(args) > 2)")
        elif len(args) == 2:
            self.code.append(str(js(f"var {args[0]} = {args[1]}")))
            return type(args[1])(args[0])
        elif len(args) == 1:
            self.code.append(str(js(f"{args[0]}")))
        else:
            raise ValueError("No argument supplied")

    @property
    def plot_id(self):
        """
        Return the id formatted for selection
        """
        return f"#{self.id}"

    @staticmethod
    def multiple(nb: int) -> Iterator[Script]:
        """
        Generate multiple :code:`Script`

        Parameters
        ----------
        nb : int
            number of script

        Returns
        -------
        Iterator[Script]
            multiple :code:`Script`   
        """
        for i in range(nb):
            script = Script()
            script.id = f"plot-{i}"
            yield script

    def __str__(self):
        return "\n".join(map(str, self.code))

class function:
    """
    Useful class to simplify inline functions

    Examples
    --------

    >>> from detroit import function
    >>> function("d")("x(d.x)")
    function(d){
      return x(d.x);
    }
    """
    def __init__(self, *args, name:str=None):
        self.args = args
        self.name = name
        self.code = []
        self.set_signature()

    def set_signature(self):
        arguments = ", ".join(self.args)
        if self.name is None:
            self.signature = f"function({arguments})"
        else:
            self.signature = f"function {self.name}({arguments})"

    def __call__(self, *args, return_:bool=True):
        if len(args) > 2:
            raise ValueError("Too many arguments (len(args) > 2)")
        elif len(args) == 2:
            self.code.append(str(js(f"var {args[0]} = {args[1]}")))
            return type(args[1])(args[0])
        elif len(args) == 1:
            if return_:
                self.code.append("return " + str(js(f"{args[0]}")) + ";")
            else:
                self.code.append(str(js(f"{args[0]}")))
        else:
            raise ValueError("No argument supplied")
        return self

    def inline(self, arg):
        return js(self.signature + "{ return " + arg + "; }")

    def __str__(self):
        return self.signature + "{\n  " + "\n  ".join(map(str, self.code)) + "\n}"

    def call(self, *args):
        arguments = ", ".join(map("received_data.{}".format, args))
        return js(f"{self.name}({arguments})")
