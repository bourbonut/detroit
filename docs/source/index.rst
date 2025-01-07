Detroit's documentation!
========================

:code:`detroit` is a Python implementation of `d3js <https://d3js.org/>`_.

Installation
------------

.. code:: shell

   pip install detroit

Major differencies
------------------

Most of :code:`d3js` API are the same with :code:`detroit` with **snake case** . However, every time you must set something, you should add the prefix :code:`set_` to the method name.
For instance :

.. code:: javascript

   // d3js
   d3.scaleLinear().domain([0, 10]).range([0, 920])


.. code:: python

   # detroit
   d3.scale_linear().set_domain([0, 10]).set_range([0, 920])

* :code:`scaleLinear` becomes :code:`scale_linear`
* :code:`domain` becomes :code:`set_domain`
* :code:`range` becomes :code:`set_range`

If you need to access the value of :code:`domain` for instance, you can use the *property* :code:`domain` like so :

.. code:: python

   >>> x = d3.scale_linear().set_domain([0, 10]).set_range([0, 920])
   >>> x.domain
   [0, 10]
   >>> x.range
   [0, 920]

Table of Content
----------------

.. toctree::
   :maxdepth: 2

   line
   area
   scatter
   bar
   histogram
   api/index
