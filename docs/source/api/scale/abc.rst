Abstract classes
================

.. autoclass:: detroit.scale.Scaler

   .. automethod:: __call__
   .. automethod:: get_domain
   .. automethod:: get_range
   .. automethod:: set_domain
   .. automethod:: set_range

.. autoclass:: detroit.scale.ContinuousScaler

   .. automethod:: invert
   .. automethod:: get_interpolate
   .. automethod:: get_clamp
   .. automethod:: get_unknown
   .. automethod:: set_interpolate
   .. automethod:: set_clamp
   .. automethod:: set_unknown

.. autoclass:: detroit.scale.SequentialScaler

   .. automethod:: set_interpolator
