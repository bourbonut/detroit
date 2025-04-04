Types
=====

.. autoclass:: detroit.types.Interval

   .. automethod:: floor
   .. automethod:: ceil

.. autoclass:: detroit.types.Scaler

   .. automethod:: __call__
   .. automethod:: get_domain
   .. automethod:: get_range
   .. automethod:: set_domain
   .. automethod:: set_range

.. autoclass:: detroit.types.ContinuousScaler

   .. automethod:: invert
   .. automethod:: get_interpolate
   .. automethod:: get_clamp
   .. automethod:: get_unknown
   .. automethod:: set_interpolate
   .. automethod:: set_clamp
   .. automethod:: set_unknown

.. autoclass:: detroit.types.SequentialScaler

   .. automethod:: set_interpolator

.. autoclass:: detroit.types.Accessor

   .. automethod:: __call__
