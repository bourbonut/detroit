Sequential scales
=================

.. autofunction:: detroit.scale_sequential
.. autofunction:: detroit.scale_sequential_log
.. autofunction:: detroit.scale_sequential_symlog
.. autofunction:: detroit.scale_sequential_pow
.. autofunction:: detroit.scale_sequential_sqrt

.. autoclass:: detroit.scale.sequential.Sequential

   .. automethod:: __call__
   .. automethod:: set_domain
   .. automethod:: set_range
   .. automethod:: set_range_round
   .. automethod:: set_interpolator
   .. automethod:: set_clamp
   .. automethod:: set_unknown

.. autoclass:: detroit.scale.sequential.SequentialLinear

   .. automethod:: ticks
   .. automethod:: tick_format
   .. automethod:: nice

.. autoclass:: detroit.scale.sequential.SequentialLog

   .. automethod:: ticks
   .. automethod:: tick_format
   .. automethod:: nice

.. autoclass:: detroit.scale.sequential.SequentialSymlog

   .. automethod:: set_constant

.. autoclass:: detroit.scale.sequential.SequentialPow

   .. automethod:: set_exponent
   .. automethod:: ticks
   .. automethod:: tick_format
   .. automethod:: nice
