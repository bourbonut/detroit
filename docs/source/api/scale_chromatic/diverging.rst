Diverging schemes
=================

Diverging color schemes are available as continuous interpolators (often used with :code:`d3.scale_sequential`) and as discrete schemes (often used with :code:`d3.scale_ordinal`).

Each discrete scheme, such as :code:`d3.SCHEME_BRBG`, is represented as an array of arrays of hexadecimal color strings. The :math:`k`-th element of this array contains the color scheme of size :math:`k`; for example, :code:`d3.SCHEME_BRBG[9]` contains an array of nine strings representing the nine colors of the brown-blue-green diverging color scheme. Diverging color schemes support a size :math:`k` ranging from 3 to 11.

To create a diverging continuous color scale using the `piyg` color scheme:

.. code:: python

   color = d3.scale_sequential(d3.interpolate_piyg)

To create a diverging discrete nine-color scale using the PiYG color scheme:

.. code:: python

   color = d3.scale_ordinal(d3.SCHEME_PIYG[9])

.. autofunction:: detroit.interpolate_brbg

.. image:: ../../figures/scheme_brbg.png

.. autofunction:: detroit.interpolate_prgn

.. image:: ../../figures/scheme_prgn.png

.. autofunction:: detroit.interpolate_piyg

.. image:: ../../figures/scheme_piyg.png

.. autofunction:: detroit.interpolate_puor

.. image:: ../../figures/scheme_puor.png

.. autofunction:: detroit.interpolate_rdbu

.. image:: ../../figures/scheme_rdbu.png

.. autofunction:: detroit.interpolate_rdgy

.. image:: ../../figures/scheme_rdgy.png

.. autofunction:: detroit.interpolate_rdylbu

.. image:: ../../figures/scheme_rdylbu.png

.. autofunction:: detroit.interpolate_rdylgn

.. image:: ../../figures/scheme_rdylgn.png

.. autofunction:: detroit.interpolate_spectral

.. image:: ../../figures/scheme_spectral.png

.. autodata:: detroit.SCHEME_BRBG

.. image:: ../../figures/discrete_scheme_brbg.png

.. autodata:: detroit.SCHEME_PRGN

.. image:: ../../figures/discrete_scheme_prgn.png

.. autodata:: detroit.SCHEME_PIYG

.. image:: ../../figures/discrete_scheme_piyg.png

.. autodata:: detroit.SCHEME_PUOR

.. image:: ../../figures/discrete_scheme_puor.png

.. autodata:: detroit.SCHEME_RDBU

.. image:: ../../figures/discrete_scheme_rdbu.png

.. autodata:: detroit.SCHEME_RDGY

.. image:: ../../figures/discrete_scheme_rdgy.png

.. autodata:: detroit.SCHEME_RDYLBU

.. image:: ../../figures/discrete_scheme_rdylbu.png

.. autodata:: detroit.SCHEME_RDYLGN

.. image:: ../../figures/discrete_scheme_rdylgn.png

.. autodata:: detroit.SCHEME_SPECTRAL

.. image:: ../../figures/discrete_scheme_spectral.png
