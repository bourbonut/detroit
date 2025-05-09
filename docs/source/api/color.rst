Color
=====

Functions
---------

.. autofunction:: detroit.color
.. autofunction:: detroit.rgb
.. autofunction:: detroit.hsl
.. autofunction:: detroit.cubehelix
.. autofunction:: detroit.lab
.. autofunction:: detroit.gray
.. autofunction:: detroit.hcl
.. autofunction:: detroit.lch

------------

Classes
-------

.. autoclass:: detroit.color.color.Color

   .. automethod:: format_hex
   .. automethod:: format_hex_8
   .. automethod:: format_hsl
   .. automethod:: format_rgb

.. autoclass:: detroit.color.color.RGB

   .. automethod:: brighter
   .. automethod:: darker
   .. automethod:: rgb
   .. automethod:: clamp
   .. automethod:: displayable
   .. automethod:: format_hex
   .. automethod:: format_hex_8
   .. automethod:: format_rgb

.. autoclass:: detroit.color.color.HSL

   .. automethod:: brighter
   .. automethod:: darker
   .. automethod:: rgb
   .. automethod:: clamp
   .. automethod:: displayable
   .. automethod:: format_hsl

.. autoclass:: detroit.color.cubehelix.Cubehelix

   .. automethod:: brighter
   .. automethod:: darker
   .. automethod:: rgb

.. autoclass:: detroit.color.lab.LAB

   .. automethod:: brighter
   .. automethod:: darker
   .. automethod:: rgb

.. autoclass:: detroit.color.lab.HCL

   .. automethod:: brighter
   .. automethod:: darker
   .. automethod:: rgb
