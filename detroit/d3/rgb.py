# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class rgb:
    def __init__(self, content="rgb"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def clamp(self):
        """
        .. code:: javascript

            d3.rgb(300, 200, 100).clamp() // {r: 255, g: 200, b: 100, opacity: 1}

        Source · Returns a new RGB color where the r, g, and b channels are clamped to the
        range [0, 255] and rounded to the nearest integer value, and the opacity is clamped to
        the range [0, 1].

        See more informations `here <https://d3js.org/d3-color#rgb_clamp>`_.
        """
        return rgb(content=f"{self.content}.clamp()")

