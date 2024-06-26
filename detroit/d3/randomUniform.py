# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class randomUniform:
    def __init__(self, content="randomUniform"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def source(self, source=None):
        """
        .. code:: javascript

            const seed = 0.44871573888282423; // any number in [0, 1)
            const random = d3.randomNormal.source(d3.randomLcg(seed))(0, 1);
            random(); // -0.6253955998897069

        Examples · Returns the same type of function for generating random numbers but where
        the given random number generator source is used as the source of randomness instead of
        Math.random. The given random number generator must implement the same interface as
        Math.random and only return values in the range [0, 1). This is useful when a seeded
        random number generator is preferable to Math.random.

        See more informations `here <https://d3js.org/d3-random#random_source>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (source,))))
        return randomUniform(content=f"{self.content}.source({arguments})")

