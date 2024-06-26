# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class conic:
    def __init__(self, content="conic"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def parallels(self, parallels=None):
        """
        Source · The two standard parallels that define the map layout in conic projections.

        See more informations `here <https://d3js.org/d3-geo/conic#conic_parallels>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (parallels,))))
        return conic(content=f"{self.content}.parallels({arguments})")

