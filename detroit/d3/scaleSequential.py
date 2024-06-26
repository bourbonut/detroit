# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class scaleSequential:
    def __init__(self, content="scaleSequential"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def interpolator(self, interpolator=None):
        """
        If interpolator is specified, sets the scale’s interpolator to the specified function.
        .. code:: javascript

            const color = d3.scaleSequential().interpolator(d3.interpolateBlues);

        If interpolator is not specified, returns the scale’s current interpolator.
        .. code:: javascript

            color.interpolator() // d3.interpolateBlues


        See more informations `here <https://d3js.org/d3-scale/sequential#sequential_interpolator>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (interpolator,))))
        return scaleSequential(content=f"{self.content}.interpolator({arguments})")


    def range(self, range=None):
        """
        See linear.range. If range is specified, the given two-element array is converted to an
        interpolator function using interpolate.
        .. code:: javascript

            const color = d3.scaleSequential().range(["red", "blue"]);

        The above is equivalent to:
        .. code:: javascript

            const color = d3.scaleSequential(d3.interpolate("red", "blue"));


        See more informations `here <https://d3js.org/d3-scale/sequential#sequential_range>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (range,))))
        return scaleSequential(content=f"{self.content}.range({arguments})")


    def rangeRound(self, range=None):
        """
        See linear.rangeRound. If range is specified, implicitly uses interpolateRound as the
        interpolator.

        See more informations `here <https://d3js.org/d3-scale/sequential#sequential_rangeRound>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (range,))))
        return scaleSequential(content=f"{self.content}.rangeRound({arguments})")


    def domain(self, domain=None):
        """
        Auto generated method
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (domain,))))
        return scaleSequential(content=f"{self.content}.domain({arguments})")


    def nice(self):
        """
        Auto generated method
        """
        return scaleSequential(content=f"{self.content}.nice()")

