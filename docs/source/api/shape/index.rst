Shapes
======

Visualizations can be represented by discrete graphical marks such as symbols, arcs, lines, and areas.

Each shape generator exposes accessors that control how the input data are mapped to a visual representation.
For example, you might define a line generator for a time series by scaling fields of your data to fit the chart:

.. code:: python

   line = d3.line().x(lambda d: x(d["date"])).y(lambda d: y(d["value"]))

This line generator can then be used to compute the :code:`d` attribute of an SVG path element:

.. code:: python

   svg.attr("d", line(data))

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   arcs
   areas
   lines
   pies
   stack
   symbols
