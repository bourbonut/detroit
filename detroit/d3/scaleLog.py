# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class scaleLog:
    def __init__(self, content="scaleLog"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def base(self, base=None):
        """
        Examples · Source · If base is specified, sets the base for this logarithmic scale to
        the specified value.
        .. code:: javascript

            const x = d3.scaleLog([1, 1024], [0, 960]).base(2);

        If base is not specified, returns the current base, which defaults to 10. Note that due
        to the nature of a logarithmic transform, the base does not affect the encoding of the
        scale; it only affects which ticks are chosen.

        See more informations `here <https://d3js.org/d3-scale/log#log_base>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (base,))))
        return scaleLog(content=f"{self.content}.base({arguments})")


    def ticks(self, count=None):
        """
        Examples · Source · Like linear.ticks, but customized for a log scale.
        .. code:: javascript

            const x = d3.scaleLog([1, 100], [0, 960]);
            const T = x.ticks(); // [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        If the base is an integer, the returned ticks are uniformly spaced within each integer
        power of base; otherwise, one tick per power of base is returned. The returned ticks
        are guaranteed to be within the extent of the domain. If the orders of magnitude in the
        domain is greater than count, then at most one tick per power is returned. Otherwise,
        the tick values are unfiltered, but note that you can use log.tickFormat to filter the
        display of tick labels. If count is not specified, it defaults to 10.

        See more informations `here <https://d3js.org/d3-scale/log#log_ticks>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (count,))))
        return scaleLog(content=f"{self.content}.ticks({arguments})")


    def tickFormat(self, count=None, specifier=None):
        """
        Examples · Source · Like linear.tickFormat, but customized for a log scale. The
        specified count typically has the same value as the count that is used to generate the
        tick values.
        .. code:: javascript

            const x = d3.scaleLog([1, 100], [0, 960]);
            const T = x.ticks(); // [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, …]
            const f = x.tickFormat();
            T.map(f); // ["1", "2", "3", "4", "5", "", "", "", "", "10", …]

        If there are too many ticks, the formatter may return the empty string for some of the
        tick labels; however, note that the ticks are still shown to convey the logarithmic
        transform accurately. To disable filtering, specify a count of Infinity.
        When specifying a count, you may also provide a format specifier or format function.
        For example, to get a tick formatter that will display 20 ticks of a currency, say
        log.tickFormat(20, "$,f"). If the specifier does not have a defined precision, the
        precision will be set automatically by the scale, returning the appropriate format.
        This provides a convenient way of specifying a format whose precision will be
        automatically set by the scale.

        See more informations `here <https://d3js.org/d3-scale/log#log_tickFormat>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (count, specifier))))
        return scaleLog(content=f"{self.content}.tickFormat({arguments})")


    def nice(self):
        """
        Auto generated method
        """
        return scaleLog(content=f"{self.content}.nice()")


    def domain(self, domain=None):
        """
        Auto generated method
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (domain,))))
        return scaleLog(content=f"{self.content}.domain({arguments})")
