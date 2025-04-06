Time
====

Generation of time ticks
------------------------

.. autofunction:: detroit.time_ticks

.. autoclass:: detroit.time.ticks.Ticker

   .. automethod:: ticks
   .. automethod:: tick_interval

------------

Manipulation of date times segmented by time unit
-------------------------------------------------

The following classes are all derived by :class:`TimeInterval <detroit.time.interval.TimeInterval>` class.
Each of them is defined for a specific time unit.
For example, the function :func:`d3.time_day <detroit.time_day>` helps to manipulate dates only based on days by truncating inputs as day time or by generating day times.

.. autofunction:: detroit.time_millisecond
.. autofunction:: detroit.time_second
.. autofunction:: detroit.time_day
.. autofunction:: detroit.time_hour
.. autofunction:: detroit.time_minute
.. autofunction:: detroit.time_month
.. autofunction:: detroit.time_year
.. autofunction:: detroit.time_week
.. autofunction:: detroit.time_sunday
.. autofunction:: detroit.time_monday
.. autofunction:: detroit.time_tuesday
.. autofunction:: detroit.time_wednesday
.. autofunction:: detroit.time_thursday
.. autofunction:: detroit.time_friday
.. autofunction:: detroit.time_saturday

.. autoclass:: detroit.time.interval.TimeInterval

   .. automethod:: __call__
   .. automethod:: interval
   .. automethod:: every
   .. automethod:: ceil
   .. automethod:: round
   .. automethod:: range
   .. automethod:: filter

A common method to these classes is :code:`count`. For example, it counts the number of days for :func:`time_day`:

.. code:: python

   >>> from datetime import datetime
   >>> d3.time_day.count(datetime(2008, 1, 1), datetime(2008, 12, 31))
   365
