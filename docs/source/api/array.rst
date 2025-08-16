Array
=====

.. autofunction:: detroit.extent
.. autofunction:: detroit.nice

Set operations
--------------

.. autofunction:: detroit.difference
.. autofunction:: detroit.union
.. autofunction:: detroit.intersection
.. autofunction:: detroit.superset
.. autofunction:: detroit.subset
.. autofunction:: detroit.disjoint

Blur functions
--------------

.. autofunction:: detroit.blur
.. autofunction:: detroit.blur2
.. autofunction:: detroit.blur_image

Tick functions
--------------

.. autofunction:: detroit.tick_increment
.. autofunction:: detroit.tick_step
.. autofunction:: detroit.ticks

Group functions
---------------

.. autofunction:: detroit.group
.. autofunction:: detroit.groups
.. autofunction:: detroit.index
.. autofunction:: detroit.indexes
.. autofunction:: detroit.rollup
.. autofunction:: detroit.rollups

Bin functions
-------------

.. autofunction:: detroit.bin

.. autoclass:: detroit.array.bin.Bin

.. autoclass:: detroit.array.bin.bin

   .. automethod:: __call__
   .. automethod:: set_value
   .. automethod:: set_domain
   .. automethod:: set_thresholds

Threshold functions
-------------------

.. autofunction:: detroit.threshold_freedman_diaconis
.. autofunction:: detroit.threshold_scott
.. autofunction:: detroit.threshold_sturges
