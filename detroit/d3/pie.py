# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class pie:
    def __init__(self, content="pie"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def value(self, value=None):
        """
        Source · If value is specified, sets the value accessor to the specified function or
        number and returns this pie generator.
        .. code:: javascript

            const pie = d3.pie().value((d) => d.value);

        When a pie is generated, the value accessor will be invoked for each element in the
        input data array, being passed the element d, the index i, and the array data as three
        arguments.
        If value is not specified, returns the current value accessor.
        .. code:: javascript

            pie.value() // (d) => d.value

        The value accessor defaults to:
        .. code:: javascript

            function value(d) {
              return d;
            }

        The default value accessor assumes that the input data are numbers, or that they are
        coercible to numbers using valueOf. If your data are not numbers, then you should
        specify an accessor that returns the corresponding numeric value for a given datum. For
        example, given a CSV file with number and name fields:
        .. code:: javascript

            number,name
            4,Locke
            8,Reyes
            15,Ford
            16,Jarrah
            23,Shephard
            42,Kwon

        You might say:
        .. code:: javascript

            const data = await d3.csv("lost.csv", d3.autoType);
            const pie = d3.pie().value((d) => d.number);
            const arcs = pie(data);

        This is similar to mapping your data to values before invoking the pie generator:
        .. code:: javascript

            const arcs = d3.pie()(data.map((d) => d.number));

        The benefit of an accessor is that the input data remains associated with the returned
        objects, thereby making it easier to access other fields of the data, for example to
        set the color or to add text labels.

        See more informations `here <https://d3js.org/d3-shape/pie#pie_value>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (value,))))
        return pie(content=f"{self.content}.value({arguments})")


    def sort(self, compare=None):
        """
        Source · If compare is specified, sets the data comparator to the specified function
        and returns this pie generator.
        .. code:: javascript

            const pie = d3.pie().sort((a, b) => d3.ascending(a.name, b.name));

        The data comparator takes two arguments a and b, each elements from the input data
        array. If the arc for a should be before the arc for b, then the comparator must return
        a number less than zero; if the arc for a should be after the arc for b, then the
        comparator must return a number greater than zero; returning zero means that the
        relative order of a and b is unspecified.
        If compare is not specified, returns the current data comparator.
        .. code:: javascript

            pie.sort() // (a, b) => d3.ascending(a.name, b.name))

        The data comparator defaults to null. If both the data comparator and the value
        comparator are null, then arcs are positioned in the original input order. Setting the
        data comparator implicitly sets the value comparator to null.
        Sorting does not affect the order of the generated arc array which is always in the
        same order as the input data array; it only affects the computed angles of each arc.
        The first arc starts at the start angle and the last arc ends at the end angle.

        See more informations `here <https://d3js.org/d3-shape/pie#pie_sort>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (compare,))))
        return pie(content=f"{self.content}.sort({arguments})")


    def sortValues(self, compare=None):
        """
        Source · If compare is specified, sets the value comparator to the specified function
        and returns this pie generator.
        .. code:: javascript

            const pie = d3.pie().sortValue(d3.ascending);

        The value comparator is similar to the data comparator, except the two arguments a and
        b are values derived from the input data array using the value accessor rather than the
        data elements. If the arc for a should be before the arc for b, then the comparator
        must return a number less than zero; if the arc for a should be after the arc for b,
        then the comparator must return a number greater than zero; returning zero means that
        the relative order of a and b is unspecified.
        If compare is not specified, returns the current value comparator.
        .. code:: javascript

            pie.sortValue() // d3.ascending

        The value comparator defaults to descending. If both the data comparator and the value
        comparator are null, then arcs are positioned in the original input order. Setting the
        value comparator implicitly sets the data comparator to null.
        Sorting does not affect the order of the generated arc array which is always in the
        same order as the input data array; it merely affects the computed angles of each arc.
        The first arc starts at the start angle and the last arc ends at the end angle.

        See more informations `here <https://d3js.org/d3-shape/pie#pie_sortValues>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (compare,))))
        return pie(content=f"{self.content}.sortValues({arguments})")


    def startAngle(self, angle=None):
        """
        Source · If angle is specified, sets the overall start angle of the pie to the
        specified function or number and returns this pie generator.
        .. code:: javascript

            const pie = d3.pie().startAngle(0);

        The start angle is the overall start angle of the pie, i.e., the start angle of the
        first arc. It is typically expressed as a constant number but can also be expressed as
        a function of data. When a function, the start angle accessor is invoked once, being
        passed the same arguments and this context as the pie generator.
        If angle is not specified, returns the current start angle accessor.
        .. code:: javascript

            pie.startAngle() // () => 0

        The start angle accessor defaults to:
        .. code:: javascript

            function startAngle() {
              return 0;
            }

        Angles are in radians, with 0 at -y (12 o’clock) and positive angles proceeding
        clockwise.

        See more informations `here <https://d3js.org/d3-shape/pie#pie_startAngle>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (angle,))))
        return pie(content=f"{self.content}.startAngle({arguments})")


    def endAngle(self, angle=None):
        """
        Source · If angle is specified, sets the overall end angle of the pie to the specified
        function or number and returns this pie generator.
        .. code:: javascript

            const pie = d3.pie().endAngle(Math.PI);

        The end angle here means the overall end angle of the pie, i.e., the end angle of the
        last arc. It is typically expressed as a constant number but can also be expressed as a
        function of data. When a function, the end angle accessor is invoked once, being passed
        the same arguments and this context as the pie generator.
        If angle is not specified, returns the current end angle accessor.
        .. code:: javascript

            pie.endAngle() // () => Math.PI

        The end angle accessor defaults to:
        .. code:: javascript

            function endAngle() {
              return 2 * Math.PI;
            }

        Angles are in radians, with 0 at -y (12 o’clock) and positive angles proceeding
        clockwise. The value of the end angle is constrained to startAngle ± τ, such that
        |endAngle - startAngle| ≤ τ.

        See more informations `here <https://d3js.org/d3-shape/pie#pie_endAngle>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (angle,))))
        return pie(content=f"{self.content}.endAngle({arguments})")


    def padAngle(self, angle=None):
        """
        Pad angle:0.030
        Examples · Source · If angle is specified, sets the pad angle to the specified function
        or number and returns this pie generator.
        .. code:: javascript

            const pie = d3.pie().padAngle(0.03);

        The pad angle specifies the angular separation in radians between adjacent arcs. The
        total amount of padding is the specified angle times the number of elements in the
        input data array, and at most |endAngle - startAngle|; the remaining space is divided
        proportionally by value such that the relative area of each arc is preserved.
        The pad angle is typically expressed as a constant number but can also be expressed as
        a function of data. When a function, the pad angle accessor is invoked once, being
        passed the same arguments and this context as the pie generator.
        If angle is not specified, returns the current pad angle accessor.
        .. code:: javascript

            pie.padAngle() // () => 0.03

        The pad angle accessor defaults to:
        .. code:: javascript

            function padAngle() {
              return 0;
            }


        See more informations `here <https://d3js.org/d3-shape/pie#pie_padAngle>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (angle,))))
        return pie(content=f"{self.content}.padAngle({arguments})")
