# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class forceCenter:
    def __init__(self, content="forceCenter"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def x(self, x=None):
        """
        Source · If x is specified, sets the x-coordinate of the centering position to the
        specified number and returns this force. If x is not specified, returns the current
        x-coordinate, which defaults to zero.

        See more informations `here <https://d3js.org/d3-force/center#center_x>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (x,))))
        return forceCenter(content=f"{self.content}.x({arguments})")


    def y(self, y=None):
        """
        Source · If y is specified, sets the y coordinate of the centering position to the
        specified number and returns this force. If y is not specified, returns the current y
        coordinate, which defaults to zero.

        See more informations `here <https://d3js.org/d3-force/center#center_y>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (y,))))
        return forceCenter(content=f"{self.content}.y({arguments})")


    def strength(self, strength=None):
        """
        Examples · Source · If strength is specified, sets the center force’s strength. A
        reduced strength of e.g. 0.05 softens the movements on interactive graphs in which new
        nodes enter or exit the graph. If strength is not specified, returns the force’s
        current strength, which defaults to 1.

        See more informations `here <https://d3js.org/d3-force/center#center_strength>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (strength,))))
        return forceCenter(content=f"{self.content}.strength({arguments})")

