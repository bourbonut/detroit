Export
======

SVG
---

One feature of :code:`detroit` is to export **completly** your visualization to :code:`.svg` file (not easily feasible with `Observable platform <https://observablehq.com/@observablehq>`_).

.. code::

   save(data, plot, "output.svg") # add grid argument for multiple plots

PNG
---

.. code::

   save(data, plot, "output.png", scale_factor=2) # add grid argument for multiple plots


:code:`scale_factor` controls the quality of the image.

PDF
---

.. code::

   save(data, plot, "output.pdf") # add grid argument for multiple plots

.. warning::

   The page layout is not customizable or can not be changed.
