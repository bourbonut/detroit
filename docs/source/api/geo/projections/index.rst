Projections
===========

Constructors
------------

.. autofunction:: detroit.geo_projection
.. autofunction:: detroit.geo_projection_mutator

Projection classes
------------------

.. autoclass:: detroit.geo.common.RawProjection

   .. automethod:: __call__
   .. automethod:: invert

.. autoclass:: detroit.geo.common.Projection

   .. automethod:: __call__
   .. automethod:: invert
   .. automethod:: stream
   .. automethod:: set_preclip
   .. automethod:: set_postclip
   .. automethod:: set_clip_angle
   .. automethod:: set_clip_extent
   .. automethod:: scale
   .. automethod:: translate
   .. automethod:: rotate
   .. automethod:: set_center
   .. automethod:: set_angle
   .. automethod:: set_reflect_x
   .. automethod:: set_reflect_y
   .. automethod:: set_precision
   .. automethod:: fit_extent
   .. automethod:: fit_size
   .. automethod:: fit_width
   .. automethod:: fit_height

Clipping functions
------------------

.. autofunction:: detroit.geo_clip_antimeridian
.. autofunction:: detroit.geo_clip_circle
.. autofunction:: detroit.geo_clip_rectangle

Transform function
------------------

.. autofunction:: detroit.geo_transform

.. autoclass:: detroit.geo.transform.GeoTransform

   .. automethod:: stream

.. autoclass:: detroit.geo.transform.GeoTransformer

   .. automethod:: __call__
   .. automethod:: __str__

.. autoclass:: detroit.geo.transform.TransformStream

   .. automethod:: point
   .. automethod:: sphere
   .. automethod:: line_start
   .. automethod:: line_end
   .. automethod:: polygon_start
   .. automethod:: polygon_end

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   azimuthal
   conic
   cylindrical
