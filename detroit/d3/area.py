# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class area:
    def __init__(self, content="area"):
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
        Source · If x is specified, sets x0 to x and x1 to null and returns this area
        generator.
        .. code:: javascript

            const area = d3.area().x((d) => x(d.Date));

        If x is not specified, returns the current x0 accessor.
        .. code:: javascript

            area.x() // (d) => x(d.Date)


        See more informations `here <https://d3js.org/d3-shape/area#area_x>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (x,))))
        return area(content=f"{self.content}.x({arguments})")


    def x0(self, x=None):
        """
        Source · If x is specified, sets the x0 accessor to the specified function or number
        and returns this area generator.
        .. code:: javascript

            const area = d3.area().x0(x(0));

        When an area is generated, the x0 accessor will be invoked for each defined element in
        the input data array, being passed the element d, the index i, and the array data as
        three arguments.
        If x is not specified, returns the current x0 accessor.
        .. code:: javascript

            area.x0() // () => 20

        The x0 accessor defaults to:
        .. code:: javascript

            function x(d) {
              return d[0];
            }

        The default x0 accessor assumes that the input data are two-element arrays of numbers
        [[x0, y0], [x1, y1], …]. If your data are in a different format, or if you wish to
        transform the data before rendering, then you should specify a custom accessor as shown
        above.

        See more informations `here <https://d3js.org/d3-shape/area#area_x0>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (x,))))
        return area(content=f"{self.content}.x0({arguments})")


    def x1(self, x=None):
        """
        Source · If x is specified, sets the x1 accessor to the specified function or number
        and returns this area generator.
        .. code:: javascript

            const area = d3.area().x1((d) => x(d.Close));

        When an area is generated, the x1 accessor will be invoked for each defined element in
        the input data array, being passed the element d, the index i, and the array data as
        three arguments.
        If x is not specified, returns the current x1 accessor.
        .. code:: javascript

            area.x1() // (d) => x(d.Close)

        The x1 accessor defaults to null, indicating that the previously-computed x0 value
        should be reused for the x1 value; this default is intended for horizontally-oriented
        areas.

        See more informations `here <https://d3js.org/d3-shape/area#area_x1>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (x,))))
        return area(content=f"{self.content}.x1({arguments})")


    def y(self, y=None):
        """
        Source · If y is specified, sets y0 to y and y1 to null and returns this area
        generator.
        .. code:: javascript

            const area = d3.area().y((d) => y(d.Date));

        If y is not specified, returns the current y0 accessor.
        .. code:: javascript

            area.y() // (d) => y(d.Date)


        See more informations `here <https://d3js.org/d3-shape/area#area_y>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (y,))))
        return area(content=f"{self.content}.y({arguments})")


    def y0(self, y=None):
        """
        Source · If y is specified, sets the y0 accessor to the specified function or number
        and returns this area generator.
        .. code:: javascript

            const area = d3.area().y0(y(0));

        When an area is generated, the y0 accessor will be invoked for each defined element in
        the input data array, being passed the element d, the index i, and the array data as
        three arguments. For a horizontally-oriented area with a constant baseline (i.e., an
        area that is not stacked, and not a ribbon or band), y0 is typically set to the output
        of the y scale for zero.
        If y is not specified, returns the current y0 accessor.
        .. code:: javascript

            area.y0() // () => 360

        The y0 accessor defaults to:
        .. code:: javascript

            function y() {
              return 0;
            }

        In the default SVG coordinate system, note that the default zero represents the top of
        the chart rather than the bottom, producing a flipped (or “hanging”) area.

        See more informations `here <https://d3js.org/d3-shape/area#area_y0>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (y,))))
        return area(content=f"{self.content}.y0({arguments})")


    def y1(self, y=None):
        """
        Source · If y is specified, sets the y1 accessor to the specified function or number
        and returns this area generator.
        .. code:: javascript

            const area = d3.area().y1((d) => y(d.Close));

        When an area is generated, the y1 accessor will be invoked for each defined element in
        the input data array, being passed the element d, the index i, and the array data as
        three arguments.
        If y is not specified, returns the current y1 accessor.
        .. code:: javascript

            area.y1() // (d) => y(d.Close)

        The y1 accessor defaults to:
        .. code:: javascript

            function y(d) {
              return d[1];
            }

        The default y1 accessor assumes that the input data are two-element arrays of numbers
        [[x0, y0], [x1, y1], …]. If your data are in a different format, or if you wish to
        transform the data before rendering, then you should specify a custom accessor as shown
        above. A null accessor is also allowed, indicating that the previously-computed y0
        value should be reused for the y1 value; this can be used for a vertically-oriented
        area, as when time goes down↓ instead of right→.

        See more informations `here <https://d3js.org/d3-shape/area#area_y1>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (y,))))
        return area(content=f"{self.content}.y1({arguments})")


    def defined(self, defined=None):
        """
        Examples · Source · If defined is specified, sets the defined accessor to the specified
        function or boolean and returns this area generator.
        .. code:: javascript

            const area = d3.area().defined((d) => !isNaN(d.Close));

        When an area is generated, the defined accessor will be invoked for each element in the
        input data array, being passed the element d, the index i, and the array data as three
        arguments. If the given element is defined (i.e., if the defined accessor returns a
        truthy value for this element), the x0, x1, y0 and y1 accessors will subsequently be
        evaluated and the point will be added to the current area segment. Otherwise, the
        element will be skipped, the current area segment will be ended, and a new area segment
        will be generated for the next defined point. As a result, the generated area may have
        several discrete segments.
        If defined is not specified, returns the current defined accessor.
        .. code:: javascript

            area.defined() // (d) => !isNaN(d.Close)

        The defined accessor defaults to the constant true, and assumes that the input data is
        always defined:
        .. code:: javascript

            function defined() {
              return true;
            }

        Note that if an area segment consists of only a single point, it may appear invisible
        unless rendered with rounded or square line caps. In addition, some curves such as
        curveCardinalOpen only render a visible segment if it contains multiple points.

        See more informations `here <https://d3js.org/d3-shape/area#area_defined>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (defined,))))
        return area(content=f"{self.content}.defined({arguments})")


    def curve(self, curve=None):
        """
        Source · If curve is specified, sets the curve factory and returns this area generator.
        .. code:: javascript

            const area = d3.area().curve(d3.curveStep);

        If curve is not specified, returns the current curve factory, which defaults to
        curveLinear.
        .. code:: javascript

            area.curve() // d3.curveStep


        See more informations `here <https://d3js.org/d3-shape/area#area_curve>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (curve,))))
        return area(content=f"{self.content}.curve({arguments})")


    def context(self, context=None):
        """
        Source · If context is specified, sets the context and returns this area generator.
        .. code:: javascript

            const context = canvas.getContext("2d");
            const area = d3.area().context(context);

        If context is not specified, returns the current context.
        .. code:: javascript

            area.context() // context

        The context defaults to null. If the context is not null, then the generated area is
        rendered to this context as a sequence of path method calls. Otherwise, a path data
        string representing the generated area is returned.

        See more informations `here <https://d3js.org/d3-shape/area#area_context>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (context,))))
        return area(content=f"{self.content}.context({arguments})")


    def digits(self, digits=None):
        """
        Source · If digits is specified, sets the maximum number of digits after the decimal
        separator and returns this area generator.
        .. code:: javascript

            const area = d3.area().digits(3);

        If digits is not specified, returns the current maximum fraction digits, which defaults
        to 3.
        .. code:: javascript

            area.digits() // 3

        This option only applies when the associated context is null, as when this area
        generator is used to produce path data.

        See more informations `here <https://d3js.org/d3-shape/area#area_digits>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (digits,))))
        return area(content=f"{self.content}.digits({arguments})")


    def lineX0(self):
        """
        An alias for area.lineY0.

        See more informations `here <https://d3js.org/d3-shape/area#area_lineX0>`_.
        """
        return area(content=f"{self.content}.lineX0()")


    def lineY0(self):
        """
        Source · Returns a new line generator that has this area generator’s current defined
        accessor, curve and context. The line’s x-accessor is this area’s x0-accessor, and the
        line’s y-accessor is this area’s y0-accessor.

        See more informations `here <https://d3js.org/d3-shape/area#area_lineY0>`_.
        """
        return area(content=f"{self.content}.lineY0()")


    def lineX1(self):
        """
        Source · Returns a new line generator that has this area generator’s current defined
        accessor, curve and context. The line’s x-accessor is this area’s x1-accessor, and the
        line’s y-accessor is this area’s y0-accessor.

        See more informations `here <https://d3js.org/d3-shape/area#area_lineX1>`_.
        """
        return area(content=f"{self.content}.lineX1()")


    def lineY1(self):
        """
        Source · Returns a new line generator that has this area generator’s current defined
        accessor, curve and context. The line’s x-accessor is this area’s x0-accessor, and the
        line’s y-accessor is this area’s y1-accessor.

        See more informations `here <https://d3js.org/d3-shape/area#area_lineY1>`_.
        """
        return area(content=f"{self.content}.lineY1()")
