General informations
====================

About :code:`detroit`
---------------------

:code:`detroit` aims to reproduce `d3js <https://d3js.org/>`_ code and `Observable Plot <https://observablehq.com/plot/>`_ code with Python. However, for some complex applications such as applications which need updates and animations written with :code:`d3`, a pure Javascript code is more appropriate to suit the development of the application.

Some python librairies such as `d3blocks <https://github.com/d3blocks/d3blocks>`_ or `d3graphs <https://github.com/erdogant/d3graph>`_ create beautiful complex animated and interative visualizations. Nonetheless, you cannot export the visualization as :code:`.svg` files (for :code:`.png` or :code:`.pdf`, you can do through your browser but it is not compliant in a programming viewpoint). With :code:`detroit`, it is possible and it is even better for :code:`.svg` files than `Observable platform <https://observablehq.com/@observablehq>`_.

Since :code:`detroit` writes and uses Javascript code, you need to know how a little how Javascript code works.

Limitations
-----------

Neither `d3js <https://d3js.org/>`_ nor `Observable Plot <https://observablehq.com/plot/>`_ allows to make 3D plots.

For the moment, :code:`detroit` does not support dynamic updates of data. So, there is no way to make a dymanic visualization which is updated by supplying new data over time. In future, this feature will be added.
Also, interactions with buttons or inputs are not yet possible. However it supports interactions such as `Plot interactions <https://observablehq.com/plot/features/interactions>`_. :code:`d3` interactions will be added in future.

.. warning::

   :code:`detroit` writes text with `jinja <https://pypi.org/project/Jinja2/>`_. If you have large amount of data, it could crash since the most of browsers can hold a maximum of 2 Gb per tabulation. You should try as much to minimize the data needed for your visualization.

Specific variable names with :code:`detroit`
--------------------------------------------

There are some specific names that you must use with :code:`detroit`.

Whatever the variable name of your values is (ex: :code:`df`, :code:`mydata`, :code:`results` ...), the name of the data variable for :code:`detroit` is always :code:`"data"`.

.. code:: python

   data = {"colx": [...], "coly": [...], "values": {"colx": [...], "coly": [...]}}

   # OK
   plot = Plot.dot(js("data"), {"x": "colx", "y": "coly", "stroke": "color"}).plot()
   plot = Plot.dot(js("data.values"), {"x": "colx", "y": "coly", "stroke": "color"}).plot()

   # Not OK
   plot = Plot.dot(js("dataframe.values"), {"x": "colx", "y": "coly", "stroke": "color"}).plot()
   plot = Plot.dot(js("mydata.values"), {"x": "colx", "y": "coly", "stroke": "color"}).plot()
   plot = Plot.dot(js("volcano_results.values"), {"x": "colx", "y": "coly", "stroke": "color"}).plot()

Also, when doing multiple plots with :code:`d3`, there are specific ids that are built by :code:`Script` and that cannot be changed :

.. code:: python

   script = Script()

   # OK
   d3.select(script.plot_id)

   # Not OK
   d3.select("#volcano_id")
  
.. note::

   There is no needed ID for :code:`Plot`.

Jupyter integration
-------------------

You can use :code:`detroit` directly in your Jupyter notebook and render your visualization.

.. image:: figures/jupyter.png
   :align: center
