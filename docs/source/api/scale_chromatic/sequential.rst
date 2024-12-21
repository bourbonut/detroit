Sequential schemes
==================

Sequential color schemes are available as continuous interpolators (often used with :code:`d3.scale_sequential`) and as discrete schemes (often used with :code:`d3.scale_ordinal`).

Each discrete scheme, such as :code:`d3.SCHEME_BLUES`, is represented as an array of arrays of hexadecimal color strings. The :math:`k`-th element of this array contains the color scheme of size :math:`k`; for example, :code:`d3.SCHEME_BRBG[9]` contains an array of nine strings representing the nine colors of the brown-blue-green diverging color scheme. Diverging color schemes support a size :math:`k` ranging from 3 to 11.

To create a diverging continuous color scale using the `blues` color scheme:

.. code:: python

   color = d3.scale_sequential(d3.interpolate_blues)

To create a diverging discrete nine-color scale using the PiYG color scheme:

.. code:: python

   color = d3.scale_ordinal(d3.SCHEME_BLUES[9])

.. autofunction:: detroit.interpolate_blues

.. image:: ../../figures/scheme_blues.png

.. autofunction:: detroit.interpolate_greens

.. image:: ../../figures/scheme_greens.png

.. autofunction:: detroit.interpolate_greys

.. image:: ../../figures/scheme_greys.png

.. autofunction:: detroit.interpolate_oranges

.. image:: ../../figures/scheme_oranges.png

.. autofunction:: detroit.interpolate_purples

.. image:: ../../figures/scheme_purples.png

.. autofunction:: detroit.interpolate_reds

.. image:: ../../figures/scheme_reds.png

.. autofunction:: detroit.interpolate_turbo

.. image:: ../../figures/scheme_turbo.png

.. autofunction:: detroit.interpolate_viridis

.. image:: ../../figures/scheme_viridis.png

.. autofunction:: detroit.interpolate_inferno

.. image:: ../../figures/scheme_inferno.png

.. autofunction:: detroit.interpolate_magma

.. image:: ../../figures/scheme_magma.png

.. autofunction:: detroit.interpolate_plasma

.. image:: ../../figures/scheme_plasma.png

.. autofunction:: detroit.interpolate_cividis

.. image:: ../../figures/scheme_cividis.png

.. autofunction:: detroit.interpolate_warm

.. image:: ../../figures/scheme_warm.png

.. autofunction:: detroit.interpolate_cool

.. image:: ../../figures/scheme_cool.png

.. autofunction:: detroit.interpolate_cubehelix_default

.. image:: ../../figures/scheme_cubehelix_default.png

.. autofunction:: detroit.interpolate_bugn

.. image:: ../../figures/scheme_bugn.png

.. autofunction:: detroit.interpolate_bupu

.. image:: ../../figures/scheme_bupu.png

.. autofunction:: detroit.interpolate_gnbu

.. image:: ../../figures/scheme_gnbu.png

.. autofunction:: detroit.interpolate_orrd

.. image:: ../../figures/scheme_orrd.png

.. autofunction:: detroit.interpolate_pubugn

.. image:: ../../figures/scheme_pubugn.png

.. autofunction:: detroit.interpolate_pubu

.. image:: ../../figures/scheme_pubu.png

.. autofunction:: detroit.interpolate_purd

.. image:: ../../figures/scheme_purd.png

.. autofunction:: detroit.interpolate_rdpu

.. image:: ../../figures/scheme_rdpu.png

.. autofunction:: detroit.interpolate_ylgnbu

.. image:: ../../figures/scheme_ylgnbu.png

.. autofunction:: detroit.interpolate_ylgn

.. image:: ../../figures/scheme_ylgn.png

.. autofunction:: detroit.interpolate_ylorbr

.. image:: ../../figures/scheme_ylorbr.png

.. autofunction:: detroit.interpolate_ylorrd

.. image:: ../../figures/scheme_ylorrd.png

.. autodata:: detroit.SCHEME_BLUES

.. image:: ../../figures/discrete_scheme_blues.png

.. autodata:: detroit.SCHEME_GREENS

.. image:: ../../figures/discrete_scheme_greens.png

.. autodata:: detroit.SCHEME_GREYS

.. image:: ../../figures/discrete_scheme_greys.png

.. autodata:: detroit.SCHEME_ORANGES

.. image:: ../../figures/discrete_scheme_oranges.png

.. autodata:: detroit.SCHEME_PURPLES

.. image:: ../../figures/discrete_scheme_purples.png

.. autodata:: detroit.SCHEME_REDS

.. image:: ../../figures/discrete_scheme_reds.png

.. autodata:: detroit.SCHEME_BUGN

.. image:: ../../figures/discrete_scheme_bugn.png

.. autodata:: detroit.SCHEME_BUPU

.. image:: ../../figures/discrete_scheme_bupu.png

.. autodata:: detroit.SCHEME_GNBU

.. image:: ../../figures/discrete_scheme_gnbu.png

.. autodata:: detroit.SCHEME_ORRD

.. image:: ../../figures/discrete_scheme_orrd.png

.. autodata:: detroit.SCHEME_PUBUGN

.. image:: ../../figures/discrete_scheme_pubugn.png

.. autodata:: detroit.SCHEME_PUBU

.. image:: ../../figures/discrete_scheme_pubu.png

.. autodata:: detroit.SCHEME_PURD

.. image:: ../../figures/discrete_scheme_purd.png

.. autodata:: detroit.SCHEME_RDPU

.. image:: ../../figures/discrete_scheme_rdpu.png

.. autodata:: detroit.SCHEME_YLGNBU

.. image:: ../../figures/discrete_scheme_ylgnbu.png

.. autodata:: detroit.SCHEME_YLGN

.. image:: ../../figures/discrete_scheme_ylgn.png

.. autodata:: detroit.SCHEME_YLORBR

.. image:: ../../figures/discrete_scheme_ylorbr.png

.. autodata:: detroit.SCHEME_YLORRD

.. image:: ../../figures/discrete_scheme_ylorrd.png
